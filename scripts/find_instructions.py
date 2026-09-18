#!/usr/bin/env python3
"""List instruction candidates on explicitly supplied edit paths; never execute them."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

NAMES = ('AGENTS.md', 'AGENTS.override.md', 'CLAUDE.md', 'CLAUDE.local.md', '.claude/CLAUDE.md')
RULE_DIRS = ('.claude/rules', '.cursor/rules')


def confined(root: Path, path: Path) -> Path:
    """Reject symlink escapes, including existing ancestors of a new path."""
    try:
        resolved = path.resolve(strict=False)
    except (RuntimeError, OSError) as exc:
        raise ValueError(f'cannot resolve {path}: {exc}') from exc
    if not resolved.is_relative_to(root):
        raise ValueError(f'path resolves outside root: {path}')
    return path


def inspect(root: Path, targets: list[str], directories: list[str] | None = None) -> dict:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('root must be a directory')
    directories = directories or []
    if not targets and not directories:
        raise ValueError('supply at least one exact file or --directory; no whole-repository scan')
    ancestors: set[Path] = {root}
    scoped: list[str] = []
    for name, is_directory in [(n, False) for n in targets] + [(n, True) for n in directories]:
        if not isinstance(name, str) or not name.strip() or '\0' in name:
            raise ValueError('target must be a nonempty path')
        p = Path(name)
        if '..' in p.parts or any(ch in name for ch in '*?[]'):
            raise ValueError(f'use exact paths without traversal or globs: {name}')
        path = confined(root, p if p.is_absolute() else root / p)
        if not path.is_relative_to(root):
            raise ValueError(f'target is not inside root: {name}')
        if '.git' in path.relative_to(root).parts:
            raise ValueError('Git internals are not an edit scope')
        if is_directory and path.exists() and not path.is_dir():
            raise ValueError(f'--directory target is not a directory: {name}')
        if not is_directory and path.exists() and not path.is_file():
            raise ValueError(f'file target is not a file; use --directory: {name}')
        if not is_directory and path.is_symlink():
            raise ValueError(f'edit target is a symlink; inspect logical and resolved instruction paths manually: {name}')
        parent = path if is_directory else path.parent
        if parent.resolve() != parent:
            raise ValueError(f'edit scope traverses a symlink; inspect logical and resolved instruction paths manually: {name}')
        scoped.append(path.relative_to(root).as_posix())
        while True:
            ancestors.add(parent)
            if parent == root:
                break
            parent = parent.parent
    candidates: list[dict] = []
    seen: set[str] = set()
    def add(path: Path, kind: str) -> None:
        confined(root, path)
        if path.is_symlink() and not path.exists():
            raise ValueError(f'broken instruction symlink: {path}')
        if not path.is_file():
            raise ValueError(f'instruction candidate is not a regular file: {path}')
        relative = path.relative_to(root).as_posix()
        if relative not in seen:
            seen.add(relative)
            candidates.append({'path': relative, 'kind': kind,
                               'resolved_path': path.resolve().relative_to(root).as_posix()})
    for parent in sorted(ancestors, key=lambda p: (len(p.relative_to(root).parts), p.as_posix())):
        for name in NAMES:
            path = parent / name
            # Check parent links before querying a possibly external file.
            confined(root, path)
            if path.exists() or path.is_symlink():
                add(path, 'directory-instruction')
        for rule_name in RULE_DIRS:
            rule_dir = confined(root, parent / rule_name)
            if rule_dir.is_symlink():
                raise ValueError(f'rule directory symlink needs manual inspection: {rule_dir}')
            if rule_dir.exists() and not rule_dir.is_dir():
                raise ValueError(f'rules path is not a directory: {rule_dir}')
            if rule_dir.is_dir():
                # Only rule folders on affected ancestors, never unrelated packages.
                stack = [rule_dir]
                while stack:
                    directory = stack.pop()
                    for child in sorted(directory.iterdir()):
                        confined(root, child)
                        if child.is_symlink():
                            if child.is_dir() or not child.exists():
                                raise ValueError(f'rule symlink needs manual inspection: {child}')
                            if child.suffix in ('.md', '.mdc'):
                                add(child, 'conditional-rule-candidate')
                        elif child.is_dir():
                            stack.append(child)
                        elif child.suffix in ('.md', '.mdc'):
                            add(child, 'conditional-rule-candidate')
    return {'schema_version': 1, 'root': str(root), 'targets': sorted(set(scoped)),
            'candidates': candidates, 'limits': [
                'Candidate discovery only: contents were not read and scope/precedence was not resolved.',
                'Read applicable candidates and referenced imports; respect host path-rule matching.',
                'User, managed and outside-root instructions require host discovery; they are not scanned.',
                'Other instruction filenames require explicit discovery from project/host configuration.',
                'Repeat on expanded edit scope. A directory target does not scan its descendant packages.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--directory', action='append', default=[])
    parser.add_argument('paths', nargs='*')
    args = parser.parse_args()
    try:
        result = inspect(args.root, args.paths, args.directory)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f'instruction discovery incomplete: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
