#!/usr/bin/env python3
"""Validate an R-Stack JSON work graph before dispatch."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any


WORK_ID = re.compile(r"^W-[0-9]{3,}$")
ACCEPTANCE_ID = re.compile(r"^A-[0-9]{3,}$")
DECISION_ID = re.compile(r"^D-[0-9]{3,}$")
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD)\b|\[TODO", re.IGNORECASE)
FORBIDDEN_KEYS = {
    "model",
    "models",
    "model_name",
    "reasoning",
    "reasoning_effort",
    "price",
    "pricing",
    "budget",
}
STRING_FIELDS = {"role", "outcome", "parent_outcome", "authority", "report"}
LIST_FIELDS = {
    "read",
    "write",
    "excluded",
    "context",
    "accepted_decisions",
    "known_facts",
    "assumptions_to_test",
    "requires",
    "produces_for",
    "stop_if",
    "forbidden",
}


def add(errors: list[str], location: str, message: str) -> None:
    errors.append(f"{location}: {message}")


def walk(value: Any, location: str = "$") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield location, str(key), child
            yield from walk(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{location}[{index}]")


def normalized_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")


def check_forbidden(errors: list[str], graph: Any) -> None:
    for location, key, value in walk(graph):
        if normalized_key(key) in FORBIDDEN_KEYS:
            add(errors, location, f"forbidden executor-policy key {key!r}")
        if isinstance(value, str) and PLACEHOLDER.search(value):
            add(errors, f"{location}.{key}", "contains unresolved placeholder")


def require_string(errors: list[str], unit: dict[str, Any], field: str, where: str) -> None:
    value = unit.get(field)
    if not isinstance(value, str) or not value.strip():
        add(errors, where, f"{field} must be a non-empty string")


def require_list(errors: list[str], unit: dict[str, Any], field: str, where: str) -> None:
    value = unit.get(field)
    if not isinstance(value, list):
        add(errors, where, f"{field} must be a list")
    elif any(not isinstance(item, str) or not item.strip() for item in value):
        add(errors, where, f"{field} entries must be non-empty strings")


def path_conflict(left: str, right: str) -> bool:
    left = left.strip().rstrip("/")
    right = right.strip().rstrip("/")
    if not left or not right or left.upper() == "NONE" or right.upper() == "NONE":
        return False
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def transitive_dependencies(units: dict[str, dict[str, Any]], work_id: str) -> set[str]:
    found: set[str] = set()
    frontier = list(units[work_id].get("requires", []))
    while frontier:
        dependency = frontier.pop()
        if dependency in found or dependency not in units:
            continue
        found.add(dependency)
        frontier.extend(units[dependency].get("requires", []))
    return found


def check_graph(graph: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(graph, dict):
        return ["$: graph must be a JSON object"]

    check_forbidden(errors, graph)
    raw_units = graph.get("units")
    if not isinstance(raw_units, list) or not raw_units:
        add(errors, "$", "units must be a non-empty list")
        return errors

    units: dict[str, dict[str, Any]] = {}
    acceptance_owner: dict[str, str] = {}

    for index, raw_unit in enumerate(raw_units):
        where = f"$.units[{index}]"
        if not isinstance(raw_unit, dict):
            add(errors, where, "unit must be an object")
            continue
        work_id = raw_unit.get("id")
        if not isinstance(work_id, str) or not WORK_ID.fullmatch(work_id):
            add(errors, where, "id must match W-###")
            continue
        if work_id in units:
            add(errors, where, f"duplicate work id {work_id}")
            continue
        units[work_id] = raw_unit

        for field in STRING_FIELDS:
            require_string(errors, raw_unit, field, where)
        for field in LIST_FIELDS:
            require_list(errors, raw_unit, field, where)

        acceptance = raw_unit.get("acceptance")
        if not isinstance(acceptance, list) or not acceptance:
            add(errors, where, "acceptance must be a non-empty list")
            continue
        for acceptance_index, claim in enumerate(acceptance):
            claim_where = f"{where}.acceptance[{acceptance_index}]"
            if not isinstance(claim, dict):
                add(errors, claim_where, "acceptance claim must be an object")
                continue
            claim_id = claim.get("id")
            if not isinstance(claim_id, str) or not ACCEPTANCE_ID.fullmatch(claim_id):
                add(errors, claim_where, "id must match A-###")
                continue
            if claim_id in acceptance_owner:
                add(errors, claim_where, f"{claim_id} already owned by {acceptance_owner[claim_id]}")
            acceptance_owner[claim_id] = work_id
            if not isinstance(claim.get("predicate"), str) or not claim["predicate"].strip():
                add(errors, claim_where, "predicate must be a non-empty string")
            verify = claim.get("verify")
            if not isinstance(verify, dict):
                add(errors, claim_where, "verify must be an object")
            else:
                for field in ("action", "expected"):
                    value = verify.get(field)
                    if not isinstance(value, str) or not value.strip():
                        add(errors, claim_where, f"verify.{field} must be non-empty")

    decision_ids: set[str] = set()
    raw_decisions = graph.get("decisions", [])
    if not isinstance(raw_decisions, list):
        add(errors, "$", "decisions must be a list")
        raw_decisions = []
    for index, decision in enumerate(raw_decisions):
        where = f"$.decisions[{index}]"
        if not isinstance(decision, dict):
            add(errors, where, "decision must be an object")
            continue
        decision_id = decision.get("id")
        if not isinstance(decision_id, str) or not DECISION_ID.fullmatch(decision_id):
            add(errors, where, "id must match D-###")
            continue
        if decision_id in decision_ids:
            add(errors, where, f"duplicate decision id {decision_id}")
        decision_ids.add(decision_id)
        if not isinstance(decision.get("text"), str) or not decision["text"].strip():
            add(errors, where, "text must be a non-empty string")

    for work_id, unit in units.items():
        for dependency in unit.get("requires", []):
            if dependency not in units:
                add(errors, work_id, f"unknown dependency {dependency}")
            elif dependency == work_id:
                add(errors, work_id, "unit cannot depend on itself")
        for consumer in unit.get("produces_for", []):
            if consumer.lower() != "final" and consumer not in units:
                add(errors, work_id, f"unknown produces_for target {consumer}")
        for decision_id in unit.get("accepted_decisions", []):
            if decision_id not in decision_ids:
                add(errors, work_id, f"unknown accepted decision {decision_id}")

    for work_id in units:
        dependencies = transitive_dependencies(units, work_id)
        if work_id in dependencies:
            add(errors, work_id, "dependency cycle detected")

    work_ids = sorted(units)
    dependency_cache = {
        work_id: transitive_dependencies(units, work_id) for work_id in work_ids
    }
    for left_index, left_id in enumerate(work_ids):
        for right_id in work_ids[left_index + 1 :]:
            ordered = (
                left_id in dependency_cache[right_id]
                or right_id in dependency_cache[left_id]
            )
            if ordered:
                continue
            for left_path in units[left_id].get("write", []):
                for right_path in units[right_id].get("write", []):
                    if path_conflict(left_path, right_path):
                        add(
                            errors,
                            "$.units",
                            f"unordered write conflict: {left_id} and {right_id} both own "
                            f"{left_path!r}/{right_path!r}",
                        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    args = parser.parse_args()

    try:
        graph = json.loads(args.graph.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"work graph is unreadable: {exc}", file=sys.stderr)
        return 2

    errors = check_graph(graph)
    if errors:
        print("work graph validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"work graph validation passed "
        f"({len(graph['units'])} units, {len(graph.get('decisions', []))} decisions)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
