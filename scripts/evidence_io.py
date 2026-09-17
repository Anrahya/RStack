#!/usr/bin/env python3
"""Small evidence I/O primitives; no model calls and no inferred test verdicts."""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_sha256(value: Any) -> str:
    """Hash JSON by value, independent of whitespace and object key order."""
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':'), allow_nan=False).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def git(root: Path, *args: str) -> bytes:
    return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True, timeout=20).stdout


def workspace_fingerprint(repo: Path) -> str:
    """Hash HEAD, index, tracked and non-ignored untracked content and modes.

    Ignores ignored files and does not follow symlink targets. Submodules are
    rejected. This does NOT identify external services, builds or dependencies.
    The caller must prevent concurrent mutations; a snapshot is not a lock.
    """
    root = repo.resolve(strict=True)
    actual = Path(os.fsdecode(git(root, 'rev-parse', '--show-toplevel')).strip()).resolve()
    if actual != root:
        raise ValueError('--repo must be the Git worktree root')
    try:
        head = git(root, 'rev-parse', '--verify', 'HEAD').strip()
    except subprocess.CalledProcessError:
        git(root, 'status', '--porcelain')  # Distinguish an unborn branch from an unusable repository.
        head = b'UNBORN'
    index = git(root, 'ls-files', '--stage', '-z')
    if any(row.startswith(b'160000 ') for row in index.split(b'\0') if row):
        raise ValueError('submodule snapshot unsupported; use host-provided evidence')
    names = sorted(set(git(root, 'ls-files', '-z', '--cached', '--others', '--exclude-standard').split(b'\0')) - {b''})
    h = hashlib.sha256()
    def frame(data: bytes) -> None:
        h.update(len(data).to_bytes(8, 'big')); h.update(data)
    frame(b'rstack-workspace-v1'); frame(head); frame(index)
    for raw in names:
        relative = Path(os.fsdecode(raw))
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('unsafe Git path')
        path = root / relative
        parent = path.parent
        while parent != root:
            if parent.is_symlink():
                raise ValueError(f'symlink ancestor in input path: {relative}')
            parent = parent.parent
        frame(raw)
        try:
            info = path.lstat()
        except FileNotFoundError:
            frame(b'deleted'); continue
        frame(str(stat.S_IMODE(info.st_mode)).encode())
        if stat.S_ISLNK(info.st_mode):
            frame(b'symlink'); frame(os.fsencode(os.readlink(path)))
        elif stat.S_ISREG(info.st_mode):
            frame(b'file'); frame(bytes.fromhex(sha256_file(path)))
        else:
            raise ValueError(f'unsupported input file type: {relative}')
    return 'sha256:' + h.hexdigest()


def safe_artifact(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or '\\' in relative or '\0' in relative:
        raise ValueError('artifact path must be a non-empty relative POSIX path')
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('artifact path escapes evidence root')
    base = root.resolve(strict=True)
    candidate = base / p
    current = candidate
    while current != base:
        if current.is_symlink():
            raise ValueError('symlink evidence paths are not accepted')
        current = current.parent
    resolved = candidate.resolve(strict=True)
    resolved.relative_to(base)
    if not resolved.is_file():
        raise ValueError('artifact must be a regular file')
    return resolved


def load_verified_artifact(root: Path, descriptor: Any) -> Path:
    if not isinstance(descriptor, dict) or not isinstance(descriptor.get('sha256'), str):
        raise ValueError('artifact needs path and sha256')
    path = safe_artifact(root, descriptor.get('path'))
    if sha256_file(path) != descriptor['sha256']:
        raise ValueError(f'artifact hash mismatch: {descriptor.get("path")}')
    return path


def write_json(path: Path, obj: Any) -> None:
    # Evidence creation is exclusive; retries must use a new E-### identifier.
    with path.open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
