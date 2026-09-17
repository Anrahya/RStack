#!/usr/bin/env python3
"""Append a real decision to an explicitly requested, local TSV log."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import io
import os
from pathlib import Path
import sys

HEADER = ("ts", "phase", "decision", "why", "evidence", "result")
MAX_BYTES = 10 * 1024 * 1024


def clean_cell(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("log fields must be strings")
    value = " ".join(value.split())
    if not value:
        raise ValueError("log fields must not be empty")
    if len(value) > 16384:
        raise ValueError("a log field is too long")
    if value.startswith(("=", "+", "-", "@")):
        value = "'" + value
    return value


def reject_symlinks(path: Path) -> None:
    for item in (path, *path.parents):
        if item.is_symlink():
            raise ValueError(f"symlink destination or ancestor: {item}")


def append_decision(path: Path, phase: str, decision: str, why: str,
                    evidence: str, result: str) -> None:
    values = [clean_cell(x) for x in (phase, decision, why, evidence, result)]
    path = Path(os.path.abspath(path))
    reject_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + ".lock")
    # Exclusive creation protects only writers using this helper, not arbitrary editors.
    descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as owner:
            owner.write(str(os.getpid()))
        reject_symlinks(path)
        exists = path.exists()
        if exists:
            if not path.is_file() or path.stat().st_nlink != 1:
                raise ValueError("log must be a regular, unshared file")
            if path.stat().st_size > MAX_BYTES:
                raise ValueError("log exceeds the 10 MiB local-helper limit")
            with path.open(encoding="utf-8", newline="") as stream:
                rows = csv.reader(stream, delimiter="\t", strict=True)
                if tuple(next(rows, ())) != HEADER:
                    raise ValueError("existing log has an unexpected header")
                for row in rows:
                    if len(row) != len(HEADER) or any("\n" in x or "\r" in x for x in row):
                        raise ValueError("existing log contains a malformed row")
            with path.open("rb") as stream:
                stream.seek(-1, os.SEEK_END)
                if stream.read(1) != b"\n":
                    raise ValueError("existing log ends with an incomplete row")
        buffer = io.StringIO(newline="")
        writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
        if not exists:
            writer.writerow(HEADER)
        writer.writerow([datetime.now(timezone.utc).isoformat(), *values])
        data = buffer.getvalue().encode("utf-8")
        if (path.stat().st_size if exists else 0) + len(data) > MAX_BYTES:
            raise ValueError("append would exceed the 10 MiB local-helper limit")
        with path.open("ab" if exists else "xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        lock.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    for name in HEADER[1:]:
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    try:
        append_decision(args.path, args.phase, args.decision, args.why, args.evidence, args.result)
    except (OSError, ValueError, csv.Error, UnicodeError) as exc:
        print(f"decision log not written: {exc}", file=sys.stderr)
        return 2
    print(f"Decision appended to {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
