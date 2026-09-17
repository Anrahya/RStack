# Migration and boundaries

This is a local reviewable release candidate against
`dfb1799ce69cd732c037539c8b24e72f2bc9f744`. No remote branch, commit, pull request,
installation or native host setting was changed during its creation.

Apply to that checkout only after reviewing the overlay. Stop other writers.
The applicator requires each replaced file to match its audited Git blob and to
have no staged/unstaged edits. New-file collisions and symlink ancestors are
rejected. Unrelated dirty paths remain untouched. A backup journal is retained
outside the repository. Ordinary write failures trigger restoration of replaced
files; abrupt machine failure is not a transactional filesystem guarantee. Read
the journal and restore only named paths from its `originals` folder when needed.
Do not restore unrelated user work or run a broad reset/clean.

Schema 2 is deliberately incompatible with old success receipts. Old records
remain historical. Rebuild a small graph from the original acceptance, then
capture fresh required checks. Do not mechanically rename schema fields and
assume the old evidence now proves completion.

This RC tightens schema 2 before stable release: machine-checked units require
non-empty context pointers and stop conditions, while new records, evidence and
receipts bind to the canonical graph SHA-256. Recapture any earlier RC evidence;
do not copy a calculated hash into an observation made under another contract.

Existing shape, architecture, prototype, resume and reflect capabilities remain
in place. Several existing playbooks and host adapters are preserved unchanged.
The overlay never substitutes a missing icon, discards upstream licenses or
pretends to contain a complete fetched checkout.

Instruction mode remains available without JSON bookkeeping for direct work.
When capture is chosen, use the exact source tree as `--repo` and a separate
evidence directory. Generated logs and receipts must not alter the source
fingerprint. Ignored state, dependency binaries, remote services, clock-dependent
behavior and deployed artifacts need separate environment/target identification.
Do not call a repository hash proof of those external conditions.

The instruction changes, subjective design procedures and recovery heuristics
need real agent trials. Python tests and fixture controls are not substitutes.
Keep this release on hold for claims about cheaper-model superiority until the
predeclared held-out comparison in `EVALUATION.md` succeeds.
