#!/usr/bin/env python3
"""Check standalone skill packaging and declared isolation, not model behavior."""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys

NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CORE = {"r-stack-mode", "investigate", "shape", "architect", "prototype",
        "orchestrate", "verify", "review", "resume", "workflow-eval"}
EFFECTS = {"response-only", "read-only", "scoped-edit", "scoped-write"}
BOUNDARY = "Standalone utility. Do not start or resume R-Stack mode"
REQUIRED = {"bro", "unslop", "technical-writing", "teach", "how", "why", "research",
            "recall", "show-me-your-work", "automate-me", "reflect", "blast-radius",
            "typescript-best-practices", "no-comments", "tdd",
            "create-verification-skill", "maintain-verification-skill"}


def relative_file(root: Path, relative: str) -> Path:
    p = PurePosixPath(relative)
    if (not p.parts or p.is_absolute() or ".." in p.parts or "\\" in relative
            or "\0" in relative):
        raise ValueError(f"unsafe relative path: {relative!r}")
    target = root.joinpath(*p.parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"path escapes skill: {relative!r}")
    return target


def check_toolbox(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        catalog = json.loads((root / "toolbox.json").read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        return [f"toolbox catalog unreadable: {exc}"]
    if not isinstance(catalog, dict):
        return ["catalog must be an object"]
    if (type(catalog.get("schema_version")) is not int or catalog.get("schema_version") != 1
            or catalog.get("policy") != "available-not-mandatory"):
        errors.append("catalog has an unsupported schema or policy")
    raw = catalog.get("utilities")
    if not isinstance(raw, list) or not raw:
        return errors + ["utilities must be a nonempty list"]
    entries: dict[str, dict] = {}
    for entry in raw:
        if not isinstance(entry, dict):
            errors.append("utility must be an object"); continue
        name = entry.get("name")
        if not isinstance(name, str) or not NAME.fullmatch(name) or len(name) > 64:
            errors.append("invalid utility name"); continue
        if name in entries:
            errors.append(f"duplicate utility: {name}"); continue
        entries[name] = entry
        if name in CORE:
            errors.append(f"core workflow skill listed as utility: {name}")
        if entry.get("activation") != "discretionary" or entry.get("lifetime") != "invocation":
            errors.append(f"{name}: utility is not discretionary and invocation-scoped")
        if entry.get("kind") not in ("utility", "shared") or entry.get("effect") not in tuple(EFFECTS):
            errors.append(f"{name}: invalid kind or mutation effect")
        if entry.get("kind") == "shared" and name != "reflect":
            errors.append(f"{name}: unexpected shared workflow entry")
        for field in ("dependencies", "optional_helpers", "references"):
            value = entry.get(field)
            if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
                errors.append(f"{name}: {field} must be a list of strings")
    if REQUIRED - entries.keys():
        errors.append("missing utility entries: " + ", ".join(sorted(REQUIRED - entries.keys())))
    for name, entry in entries.items():
        for field in ("dependencies", "optional_helpers"):
            values = entry.get(field)
            if not isinstance(values, list):
                continue
            for dependency in values:
                if not isinstance(dependency, str):
                    continue
                if dependency in CORE or dependency not in entries:
                    errors.append(f"{name}: {field} reaches a core or missing skill: {dependency}")
        directory = root / "skills" / name
        try:
            text = (directory / "SKILL.md").read_text(encoding="utf-8")
            pieces = text.split("---\n", 2)
            if not text.startswith("---\n") or len(pieces) != 3:
                errors.append(f"{name}: malformed frontmatter"); continue
            front, body = pieces[1:]
            if not re.search(rf"(?m)^name: {re.escape(name)}$", front):
                errors.append(f"{name}: skill name mismatch")
            description = re.search(r"(?m)^description: (.+)$", front)
            if description is None:
                errors.append(f"{name}: missing description")
            else:
                try:
                    value = json.loads(description.group(1))
                    if not isinstance(value, str) or not 1 <= len(value) <= 1024:
                        errors.append(f"{name}: invalid description")
                except ValueError:
                    errors.append(f"{name}: description must be a quoted scalar")
            for pattern in (r"(?m)^disable-model-invocation:\s*true\s*$",
                            r"(?m)^user-invocable:\s*false\s*$",
                            r"(?m)^(?:paths|mode|reminder|allowed-tools):"):
                if re.search(pattern, front, re.I):
                    errors.append(f"{name}: hidden, sticky, path-triggered or permission-granting frontmatter")
            for key in ("kind", "activation", "lifetime", "effect"):
                value = entry.get(key)
                if not isinstance(value, str) or not re.search(rf"(?m)^  rstack-{key}: {re.escape(value)}$", front):
                    errors.append(f"{name}: frontmatter/catalog {key} mismatch")
            if BOUNDARY not in body:
                errors.append(f"{name}: missing standalone boundary")
            if re.search(r"(?mi)^\s*(?:[-*]\s+|[0-9]+[.)]\s+)?(?:invoke|load|call|start|resume)\s+(?:the\s+)?[`/$]*(?:r-stack-mode|orchestrate|workflow-eval)\b", body):
                errors.append(f"{name}: positive core workflow invocation in utility body")
            if len(text.splitlines()) > 500:
                errors.append(f"{name}: skill body exceeds 500 lines")
            refs = entry.get("references")
            if isinstance(refs, list):
                for reference in refs:
                    if not isinstance(reference, str): continue
                    if not relative_file(directory, reference).is_file():
                        errors.append(f"{name}: reference does not exist: {reference}")
                    if reference not in text:
                        errors.append(f"{name}: reference not discoverable from skill body: {reference}")
            adapter = (directory / "agents/openai.yaml").read_text(encoding="utf-8")
            if not re.search(r"(?m)^policy:\n  allow_implicit_invocation: true$", adapter):
                errors.append(f"{name}: implicit invocation not enabled in adapter")
            if "$" + name not in adapter:
                errors.append(f"{name}: adapter prompt names another skill")
            short = re.search(r'(?m)^  short_description: "([^"]+)"$', adapter)
            if not short or not 25 <= len(short.group(1)) <= 64:
                errors.append(f"{name}: invalid adapter short description")
            wrapper = (root / "commands" / (name + ".md")).read_text(encoding="utf-8")
            if f"skills/{name}/SKILL.md" not in wrapper or "Do not start or resume R-Stack mode" not in wrapper:
                errors.append(f"{name}: command wrapper loses standalone scope")
            for path in directory.rglob("*.md"):
                content = path.read_text(encoding="utf-8")
                if re.search(r"(?:/home/|/Users/|~/.cursor/projects/)", content):
                    errors.append(f"{name}: hardcoded personal/transcript path")
                if re.search(r"(?m)^\s*(?:subagent_type|run_in_background|cloud_base_branch|model|models)\s*:", content):
                    errors.append(f"{name}: host-specific execution field")
                for target in LINK.findall(content):
                    target = target.split("#", 1)[0]
                    if not target or "://" in target or target.startswith("mailto:"): continue
                    destination = (path.parent / target).resolve()
                    if not destination.is_relative_to(directory.resolve()) or not destination.is_file():
                        errors.append(f"{name}: reference leaves self-contained skill or is missing: {target}")
        except (OSError, ValueError, UnicodeError) as exc:
            errors.append(f"{name}: unreadable/invalid package: {exc}")
    # Only mandatory edges must be acyclic. Optional helpers may refer to related topics.
    def visit(name: str, active: set[str], done: set[str]) -> None:
        if name in active:
            errors.append(f"mandatory skill dependency cycle: {name}"); return
        if name in done: return
        active.add(name)
        dependencies = entries[name].get("dependencies")
        if isinstance(dependencies, list):
            for dependency in dependencies:
                if isinstance(dependency, str) and dependency in entries:
                    visit(dependency, active, done)
        active.remove(name); done.add(name)
    done: set[str] = set()
    for name in entries: visit(name, set(), done)
    for relative in ("rules/r-stack-workflow.mdc", "skills/r-stack-mode/SKILL.md", "WORK_PROFILE.md"):
        try:
            text = (root / relative).read_text(encoding="utf-8")
            if "## Standalone utility exception" not in text:
                errors.append(f"{relative}: missing entry exception")
            if relative.startswith("rules/"):
                if "## Engineering trigger" not in text or text.index("## Standalone utility exception") > text.index("## Engineering trigger"):
                    errors.append("entry exception must precede engineering trigger")
                for name in entries:
                    if f"`{name}`" not in text:
                        errors.append(f"entry rule missing utility exemption: {name}")
        except (OSError, ValueError, UnicodeError) as exc:
            errors.append(f"{relative}: unreadable entry policy: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check_toolbox(args.root)
    if errors:
        print("Toolbox checks failed:\n" + "\n".join("- " + x for x in errors))
        return 1
    print("Toolbox structure and declared isolation passed. No native host or live model was exercised.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
