#!/usr/bin/env python3
"""Validate R-Stack's structure, links, and harness-neutral boundary."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
MODE = SKILLS / "r-stack-mode" / "SKILL.md"

FORBIDDEN = {
    "host-specific command": re.compile(r"(?<![\w-])/(?:loop|add-plugin)\b"),
    "host-specific question primitive": re.compile(r"\bAskQuestion\b"),
    "host-specific agent field": re.compile(
        r"\b(?:subagent_type|run_in_background|cloud_base_branch)\b"
    ),
    "Graphite dependency": re.compile(r"\bGraphite\b", re.IGNORECASE),
    "explicit executor slug": re.compile(
        r"\b(?:claude|gemini|gpt|grok|llama|mistral|qwen|deepseek)-"
        r"[a-z0-9][a-z0-9.-]*\b",
        re.IGNORECASE,
    ),
    "executor-selection policy": re.compile(
        r"\bmodel (?:choice|selection|routing|tier)\b|"
        r"\bmodels?\s+(?:per|for)\s+(?:role|lane|subagent)\b",
        re.IGNORECASE,
    ),
    "executor-quality policy": re.compile(
        r"\b(?:cheap|cheaper|fast|faster|strong|stronger|strongest|best|different)"
        r"\s+(?:subagent\s+|agent\s+)?models?\b",
        re.IGNORECASE,
    ),
    "executor override field": re.compile(
        r"(?mi)^\s*(?:model|models|reasoning[_ -]?effort|price|pricing)\s*:"
    ),
}
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD)\b|\[TODO", re.IGNORECASE)
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
VERSION = re.compile(r"^0\.1\.0(?:\+codex\.[0-9A-Za-z.-]+)?$")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_manifest(errors: list[str]) -> None:
    path = ROOT / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"{path}: invalid or unreadable manifest: {exc}")
        return

    if manifest.get("name") != "r-stack":
        fail(errors, f"{path}: name must be r-stack")
    version = manifest.get("version")
    if not isinstance(version, str) or not VERSION.fullmatch(version):
        fail(errors, f"{path}: version must be 0.1.0 with at most one Codex cachebuster")
    if manifest.get("skills") != "./skills/":
        fail(errors, f"{path}: skills must point to ./skills/")


def frontmatter(text: str, path: Path, errors: list[str]) -> str | None:
    if not text.startswith("---\n"):
        fail(errors, f"{path}: missing YAML frontmatter")
        return None
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        fail(errors, f"{path}: unterminated YAML frontmatter")
        return None
    match = re.search(r"(?m)^name:\s*([^\s]+)\s*$", parts[1])
    if not match:
        fail(errors, f"{path}: missing frontmatter name")
        return None
    if not re.search(r"(?m)^description:\s*\S", parts[1]):
        fail(errors, f"{path}: missing frontmatter description")
    return match.group(1)


def check_skills(errors: list[str]) -> None:
    if not SKILLS.is_dir():
        fail(errors, f"{SKILLS}: missing skills directory")
        return

    for skill_dir in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            fail(errors, f"{skill_dir}: missing SKILL.md")
            continue

        text = skill_file.read_text()
        name = frontmatter(text, skill_file, errors)
        if name is not None and name != skill_dir.name:
            fail(errors, f"{skill_file}: name {name!r} does not match directory")

        agent_file = skill_dir / "agents" / "openai.yaml"
        if not agent_file.is_file():
            fail(errors, f"{skill_dir}: missing agents/openai.yaml")
            continue
        agent_text = agent_file.read_text()
        if name is not None and f"$" + name not in agent_text:
            fail(errors, f"{agent_file}: default prompt must mention " + "$" + name)
        short = re.search(r'(?m)^\s*short_description:\s*"([^"]+)"\s*$', agent_text)
        if not short:
            fail(errors, f"{agent_file}: missing quoted short_description")
        elif not 25 <= len(short.group(1)) <= 64:
            fail(errors, f"{agent_file}: short_description must be 25-64 characters")


def instructional_paths() -> list[Path]:
    paths = [ROOT / "WORK_PROFILE.md"]
    paths.extend(sorted(SKILLS.rglob("*.md")))
    paths.extend(sorted(SKILLS.rglob("agents/openai.yaml")))
    return paths


def check_instructions(errors: list[str]) -> None:
    for path in instructional_paths():
        text = path.read_text()
        relative = path.relative_to(ROOT)

        for label, pattern in FORBIDDEN.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                fail(errors, f"{relative}:{line}: {label}: {match.group(0)!r}")

        for match in PLACEHOLDER.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            fail(errors, f"{relative}:{line}: unresolved placeholder: {match.group(0)!r}")

        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).split("#", 1)[0]
            if not target or "://" in target or target.startswith("#"):
                continue
            if not (path.parent / target).resolve().exists():
                line = text.count("\n", 0, match.start()) + 1
                fail(errors, f"{relative}:{line}: broken relative link: {target}")


def check_playbooks(errors: list[str]) -> None:
    playbook_dir = MODE.parent / "playbooks"
    if not playbook_dir.is_dir():
        fail(errors, f"{playbook_dir}: missing playbook directory")
        return

    mode_text = MODE.read_text()
    playbooks = sorted(playbook_dir.glob("*.md"))
    if not playbooks:
        fail(errors, f"{playbook_dir}: no playbooks")

    for path in playbooks:
        target = f"playbooks/{path.name}"
        if target not in mode_text:
            fail(errors, f"{path}: orphaned playbook not routed by r-stack-mode")
        text = path.read_text()
        if not re.search(r"(?m)^1\.\s+\*\*", text):
            fail(errors, f"{path}: playbook must expose numbered phase gates")
        if not re.search(r"(?i)\b(close|completion|finish)\b", text):
            fail(errors, f"{path}: playbook lacks an explicit close condition")


def check_provenance(errors: list[str]) -> None:
    required = [
        ROOT / "UPSTREAM.md",
        ROOT / "LICENSE",
        ROOT / "licenses" / "pstack-MIT.txt",
        ROOT / "licenses" / "mattpocock-skills-MIT.txt",
    ]
    for path in required:
        if not path.is_file():
            fail(errors, f"{path}: missing provenance or license file")


def check_scripts(errors: list[str]) -> None:
    scripts = [
        *sorted((ROOT / "scripts").glob("*.py")),
        *sorted((ROOT / "scripts").glob("*.sh")),
    ]
    for path in scripts:
        if not path.stat().st_mode & 0o111:
            fail(errors, f"{path}: script must be executable")


def main() -> int:
    errors: list[str] = []
    check_manifest(errors)
    check_skills(errors)
    check_instructions(errors)
    check_playbooks(errors)
    check_provenance(errors)
    check_scripts(errors)

    if errors:
        print("R-Stack checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    skill_count = sum(1 for path in SKILLS.iterdir() if path.is_dir())
    playbook_count = sum(1 for path in (MODE.parent / "playbooks").glob("*.md"))
    print(f"R-Stack checks passed ({skill_count} skills, {playbook_count} playbooks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
