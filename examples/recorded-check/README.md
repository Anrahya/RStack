# Recorded execution, without a model

Run from the installed plugin root in a POSIX shell. This creates a disposable
Git working tree and leaves evidence available for inspection. It does not make a
commit or contact a network. The example's public assertions demonstrate the
recorder, not a representative engineering benchmark or exhaustive sorting test.

```bash
PLUGIN="$PWD"
DEMO=$(mktemp -d)
mkdir "$DEMO/project"
cp examples/recorded-check/app.py examples/recorded-check/check.py "$DEMO/project/"
printf '__pycache__/\n' > "$DEMO/project/.gitignore"
git -C "$DEMO/project" init
GRAPH="$PLUGIN/examples/recorded-check/graph.json"
python3 scripts/run_check.py "$GRAPH" --work W-001 --acceptance A-001 \
  --id E-001 --repo "$DEMO/project" --evidence-root "$DEMO/evidence"
python3 scripts/close_task.py "$GRAPH" --work W-001 --ids E-001 \
  --result 'The declared public behavior passed.' --repo "$DEMO/project" \
  --evidence-root "$DEMO/evidence" --output "$DEMO/receipt.json"
printf 'Inspect retained artifacts at %s\n' "$DEMO"
```

Editing `app.py` after capture makes the same receipt stale. Re-run the receipt
validator with `--repo` to see it reject that receipt. A fresh attempt must use a
new evidence identifier and the actual final source. A missing or failing command
must never become PASS by editing the prose summary.
