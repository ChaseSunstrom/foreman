---
id: T-0922
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:25:20Z
updated: 2026-10-15T19:31:25Z
base: ca83b83bb582f9e7cc464a055194e0fcf1a91c23
base_tree: 1516cc256831c43286b09e5ea51e8eb90d0c2285
verified: strong
---
# fm tidy --apply keeps dated backups of the project's state files, the last 5
## Raw request
> fm tidy --apply keeps dated backups of the project's state files, the last 5
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] tidy --apply writes state/backups/<project>-<time>.tar.gz of the briefs, meta and ledger and keeps 5 — verify with `python3 plugin/tests/run.py -k TidyStateBackup`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then the backup in fmtidy
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k TidyStateBackup` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: TidyStateBackup 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f5076ebe4524] (2026-10-15T19:31:22Z)
- `python3 plugin/tests/run.py -k TidyStateBackup` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: TidyStateBackup 0s) / OK [ran] [tree f5076ebe4524] (2026-10-15T19:31:22Z)
- (ac 1) `python3 plugin/tests/run.py -k TidyStateBackup` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: TidyStateBackup 0s) / OK [ran] [tree f5076ebe4524] (2026-10-15T19:31:24Z)
- (step 1) `python3 plugin/tests/run.py -p 'test_tidy.py'` → exit 0 · Ran 10 tests in 1.6s (3 classes, 16 at a time; slowest: Apply 2s, DryRun 1s, TidyStateBackup 0s) / OK [ran] [tree f5076ebe4524] (2026-10-15T19:31:24Z)
- (audit edge) `self: tidy --apply writes backups/<UTC stamp>.tar.gz of tasks/, archive/, meta.json, ledger.jsonl and decisions.md under the project lock (written to .part, then renamed), keeps the newest 5; a dry run writes nothing; derived and reference parts (views, graph, research, audits) stay out` → an interrupted write leaves only a .part file, never a truncated .tar.gz that would count as a kept copy [tree f5076ebe4524] (2026-10-15T19:31:24Z)
- (audit self) `self: tidy --apply writes backups/<UTC stamp>.tar.gz of tasks/, archive/, meta.json, ledger.jsonl and decisions.md under the project lock (written to .part, then renamed), keeps the newest 5; a dry run writes nothing; derived and reference parts (views, graph, research, audits) stay out` → no findings [tree f5076ebe4524] (2026-10-15T19:31:24Z)
## Log
- 2026-10-15T19:25:20Z created
- 2026-10-15T19:30:37Z focused
- 2026-10-15T19:31:25Z done
- 2026-10-15T19:31:25Z committed f3b66c7 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round7-20261015: Probe: `fm ideas` with reliability + delight, 2 rounds, past every earlier ideas.md (brainstorm-20261015-132957): 49 new titles, eac…
- T-0004 [FEATURE M, done, 4 steps] Phase 6: fm tidy and fm doctor
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- similar past tasks were M: consider --tier M
- similar finished tasks took 4–5 steps
## Files touched
- plugin/tests/test_tidy.py
- plugin/lib/fmtidy.py
