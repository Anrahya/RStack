#!/usr/bin/env python3
"""Validate an R-Stack JSON evidence receipt."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


WORK_ID = re.compile(r"^W-[0-9]{3,}$")
EVIDENCE_ID = re.compile(r"^E-[0-9]{3,}$")
ACCEPTANCE_ID = re.compile(r"^A-[0-9]{3,}$")
STATUSES = {"PASS", "ISSUES", "BLOCKED", "INCONCLUSIVE"}
BASES = {"observed", "supported-inference", "proposed", "unknown"}
LIST_FIELDS = {"evidence", "mutations", "rejected", "uncertainty", "handoff"}


def add(errors: list[str], location: str, message: str) -> None:
    errors.append(f"{location}: {message}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def assigned_acceptance(graph: Any, work_id: str) -> set[str]:
    if not isinstance(graph, dict):
        return set()
    for unit in graph.get("units", []):
        if isinstance(unit, dict) and unit.get("id") == work_id:
            return {
                claim["id"]
                for claim in unit.get("acceptance", [])
                if isinstance(claim, dict) and isinstance(claim.get("id"), str)
            }
    return set()


def check_receipt(
    receipt: Any,
    graph: Any | None,
    expected_fingerprint: str | None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(receipt, dict):
        return ["$: receipt must be a JSON object"]

    work_id = receipt.get("work_id")
    if not isinstance(work_id, str) or not WORK_ID.fullmatch(work_id):
        add(errors, "$", "work_id must match W-###")

    status = receipt.get("status")
    if status not in STATUSES:
        add(errors, "$", f"status must be one of {sorted(STATUSES)}")
    result = receipt.get("result")
    if not isinstance(result, str) or not result.strip():
        add(errors, "$", "result must be a non-empty string")

    for field in LIST_FIELDS:
        if not isinstance(receipt.get(field), list):
            add(errors, "$", f"{field} must be a list")

    evidence_ids: set[str] = set()
    covered: set[str] = set()
    fingerprints: set[str] = set()
    for index, evidence in enumerate(receipt.get("evidence", [])):
        where = f"$.evidence[{index}]"
        if not isinstance(evidence, dict):
            add(errors, where, "evidence must be an object")
            continue
        evidence_id = evidence.get("id")
        if not isinstance(evidence_id, str) or not EVIDENCE_ID.fullmatch(evidence_id):
            add(errors, where, "id must match E-###")
        elif evidence_id in evidence_ids:
            add(errors, where, f"duplicate evidence id {evidence_id}")
        else:
            evidence_ids.add(evidence_id)

        acceptance = evidence.get("acceptance")
        if not isinstance(acceptance, str) or not ACCEPTANCE_ID.fullmatch(acceptance):
            add(errors, where, "acceptance must match A-###")
        else:
            covered.add(acceptance)

        if evidence.get("basis") not in BASES:
            add(errors, where, f"basis must be one of {sorted(BASES)}")
        for field in (
            "claim",
            "action_or_source",
            "observed_result",
            "location_or_artifact",
            "fingerprint",
        ):
            value = evidence.get(field)
            if not isinstance(value, str) or not value.strip():
                add(errors, where, f"{field} must be a non-empty string")
        fingerprint = evidence.get("fingerprint")
        if isinstance(fingerprint, str) and fingerprint.strip():
            fingerprints.add(fingerprint)

    assigned = assigned_acceptance(graph, work_id) if graph is not None else set()
    if graph is not None and not assigned:
        add(errors, "$", f"work_id {work_id!r} not found in graph")
    if status == "PASS" and assigned - covered:
        add(errors, "$", f"PASS lacks evidence for {sorted(assigned - covered)}")
    if status == "INCONCLUSIVE" and not receipt.get("uncertainty"):
        add(errors, "$", "INCONCLUSIVE requires explicit uncertainty")
    if expected_fingerprint and expected_fingerprint not in fingerprints:
        add(
            errors,
            "$",
            "no evidence item matches the expected final fingerprint "
            f"{expected_fingerprint!r}",
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--graph", type=Path)
    parser.add_argument("--expected-fingerprint")
    args = parser.parse_args()

    try:
        receipt = load_json(args.receipt)
        graph = load_json(args.graph) if args.graph else None
    except (OSError, json.JSONDecodeError) as exc:
        print(f"receipt input is unreadable: {exc}", file=sys.stderr)
        return 2

    errors = check_receipt(receipt, graph, args.expected_fingerprint)
    if errors:
        print("receipt validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"receipt validation passed "
        f"({receipt['work_id']}, {receipt['status']}, {len(receipt['evidence'])} evidence items)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
