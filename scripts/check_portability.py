#!/usr/bin/env python3
"""Static package checks, explicitly not native-host loading or model evaluation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

VERSION = re.compile(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?(?:\+[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?\Z')
LINK = re.compile(r'\[[^\]]+\]\(([^)]+)\)')


def check_package(root: Path, retained: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    retained = retained or set()
    def available(path: Path) -> bool:
        try:
            relative = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            return False
        return path.exists() or relative in retained or any(p.startswith(relative.rstrip('/') + '/') for p in retained)
    versions = []
    for folder in ('.claude-plugin', '.codex-plugin', '.cursor-plugin'):
        path = root / folder / 'plugin.json'
        try:
            manifest = json.loads(path.read_text(encoding='utf-8'))
            version = manifest.get('version')
            if manifest.get('name') != 'r-stack': errors.append(f'{folder}: invalid name')
            if not isinstance(version, str) or not VERSION.fullmatch(version):
                errors.append(f'{folder}: invalid semantic version')
            else:
                versions.append(version.split('+', 1)[0])
            for field in ('skills', 'rules', 'commands', 'logo'):
                target = manifest.get(field)
                if target is not None and (not isinstance(target, str) or not available(root / target)):
                    errors.append(f'{folder}: unresolved {field}')
            interface = manifest.get('interface', {})
            if not isinstance(interface, dict):
                errors.append(f'{folder}: invalid interface')
            else:
                for field in ('logo', 'composerIcon'):
                    target = interface.get(field)
                    if target is not None and (not isinstance(target, str) or not available(root / target)):
                        errors.append(f'{folder}: unresolved interface.{field}')
        except (OSError, ValueError, AttributeError) as exc:
            errors.append(f'{folder}: unreadable manifest: {exc}')
    if len(versions) == 3 and len(set(versions)) != 1:
        errors.append('plugin versions disagree across hosts')
    skills = root / 'skills'
    for path in sorted(skills.glob('*/SKILL.md')):
        text = path.read_text(encoding='utf-8')
        name = re.search(r'(?m)^name:\s*([^\s]+)\s*$', text)
        if not text.startswith('---\n') or not name or name.group(1) != path.parent.name:
            errors.append(f'{path.relative_to(root)}: invalid skill frontmatter/name')
        if not re.search(r'(?m)^description:\s*\S', text):
            errors.append(f'{path.relative_to(root)}: missing description')
        agent = path.parent / 'agents/openai.yaml'
        if not available(agent):
            errors.append(f'{path.relative_to(root)}: missing retained host adapter')
        elif agent.is_file():
            adapter = agent.read_text(encoding='utf-8')
            if '$' + path.parent.name not in adapter:
                errors.append(f'{agent.relative_to(root)}: prompt does not reference skill')
    for path in [root / 'WORK_PROFILE.md', *skills.rglob('*.md'), *(root / 'rules').glob('*.mdc'), *(root / 'commands').glob('*.md')]:
        if not path.is_file():
            errors.append(f'{path}: missing instruction file'); continue
        text = path.read_text(encoding='utf-8')
        for target in LINK.findall(text):
            target = target.split('#', 1)[0]
            if target and '://' not in target and not target.startswith('mailto:') and not available(path.parent / target):
                errors.append(f'{path.relative_to(root)}: broken relative link {target}')
        if re.search(r'/home/[^\s/]+/|/Users/[^\s/]+/', text):
            errors.append(f'{path.relative_to(root)}: personal absolute path')
    mode = skills / 'r-stack-mode/SKILL.md'
    mode_text = mode.read_text(encoding='utf-8') if mode.is_file() else ''
    for path in sorted((mode.parent / 'playbooks').glob('*.md')):
        text = path.read_text(encoding='utf-8')
        if f'playbooks/{path.name}' not in mode_text:
            errors.append(f'{path.name}: orphaned playbook')
        if not re.search(r'(?m)^1\.\s+\*\*', text) or not re.search(r'(?i)\b(close|completion|finish)\b', text):
            errors.append(f'{path.name}: missing phase/close gate')
    for relative in ('LICENSE', 'UPSTREAM.md', 'licenses/pstack-MIT.txt', 'licenses/mattpocock-skills-MIT.txt', 'assets/r-stack-icon.png'):
        if not available(root / relative): errors.append(f'{relative}: missing retained provenance/asset')
    for path in (root / 'scripts').glob('*'):
        if path.suffix in ('.py', '.sh') and not path.stat().st_mode & 0o111:
            errors.append(f'{path.name}: script is not executable')
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--retained-manifest', type=Path, help='overlay-only check; absent files are acknowledged, not read')
    a = p.parse_args()
    try:
        retained = set(json.loads(a.retained_manifest.read_text())['retained_paths']) if a.retained_manifest else None
        errors = check_package(a.root, retained)
    except (OSError, ValueError, UnicodeError, KeyError, TypeError) as exc:
        print(f'package input failed: {exc}', file=sys.stderr); return 2
    if errors:
        print('package checks failed:\n' + '\n'.join('- ' + error for error in errors)); return 1
    label = 'overlay references' if a.retained_manifest else 'package structure'
    print(f'{label} passed; native-host loading and model uplift were not tested')
    return 0


if __name__ == '__main__':
    sys.exit(main())
