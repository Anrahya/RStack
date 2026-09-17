# A bounded decision trail

Return a rationale in chat unless the user requested a log. For a requested log,
choose its path from the task's existing scratch area or the explicit destination.
This helper does not discover private transcripts or make Git commits.

From the `show-me-your-work` skill directory:

```bash
python3 scripts/log_decision.py /chosen/task/decisions.tsv \
  --phase investigation \
  --decision "Keep the existing storage format" \
  --why "The measured bottleneck is elsewhere" \
  --evidence "artifacts/profile.txt" \
  --result "Decision made; implementation not changed"
```

The example is illustrative. Replace its content with real decisions and artifacts.
The helper adds a current UTC timestamp. Columns are `ts`, `phase`, `decision`,
`why`, `evidence`, `result`. Keep a reason as a concise public rationale, not a
private reasoning transcript. Evidence is a resolvable pointer, not proof merely
because it occupies a cell.

Rows are single-line and append-only. Corrections refer to the earlier row in a new
entry. Formula-like prefixes are quoted for common spreadsheet-import safety; treat
imported text as data and do not enable external links or formulas. This is not a
general spreadsheet sanitizer.

The helper takes an exclusive companion `.lock` file. It fails rather than writes
concurrently. After a crash, investigate ownership before manually removing a stale
lock. It rejects symlinked destinations and malformed existing logs. It is a local
logging helper, not a tamper-proof audit store or a transactional distributed log.

After an I/O failure, inspect the last row before retrying: this append helper does
not provide exactly-once delivery or automatic rollback of a partial disk write.
