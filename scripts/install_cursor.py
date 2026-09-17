#!/usr/bin/env python3
"""Stage a Cursor copy, retain its predecessor, and never delete the source."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid


def install(source: Path, destination: Path) -> str:
    if destination.is_symlink():
        raise ValueError('refusing a symlink installation target')
    source = source.resolve(strict=True)
    destination = destination.absolute()
    resolved = destination.resolve()
    if source == resolved:
        return 'Already running from the installation; no files changed.'
    if source in resolved.parents or resolved in source.parents:
        raise ValueError('source and installation must not contain each other')
    manifest = source / '.cursor-plugin' / 'plugin.json'
    source_identity = json.loads(manifest.read_text(encoding='utf-8'))
    if not isinstance(source_identity, dict) or source_identity.get('name') != 'r-stack':
        raise ValueError('source is not an R-Stack plugin')
    if destination.exists():
        current = destination / '.cursor-plugin' / 'plugin.json'
        current_identity = json.loads(current.read_text(encoding='utf-8')) if current.is_file() else None
        if not isinstance(current_identity, dict) or current_identity.get('name') != 'r-stack':
            raise ValueError('existing target is not an identified R-Stack install')
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.r-stack-stage-', dir=destination.parent))
    backup: Path | None = None
    try:
        shutil.copytree(source, stage, dirs_exist_ok=True, symlinks=True,
                        ignore=shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache', '*.pyc'))
        if not (stage / 'skills' / 'r-stack-mode' / 'SKILL.md').is_file():
            raise ValueError('staged plugin lacks its entry skill')
        if destination.exists():
            backup = destination.with_name('r-stack-backup-' + uuid.uuid4().hex[:12])
            os.rename(destination, backup)
        try:
            os.rename(stage, destination)
        except OSError:
            if backup is not None and not destination.exists():
                os.rename(backup, destination)
            raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    note = f' Installed predecessor retained at {backup}.' if backup is not None else ''
    return f'Copied R-Stack to {destination}.{note} Native Cursor loading has not been tested by this copy operation.'


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--destination', type=Path, default=Path.home()/'.cursor/plugins/local/r-stack')
    a = p.parse_args()
    try:
        print(install(a.source, a.destination))
    except (OSError, ValueError, UnicodeError) as exc:
        print(f'installation not completed: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
