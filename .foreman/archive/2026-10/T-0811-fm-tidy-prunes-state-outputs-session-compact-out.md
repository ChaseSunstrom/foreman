---
id: T-0811
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-14T17:44:42Z
updated: 2026-10-14T18:02:26Z
base: faa491cbcd349a83546e8c1683ca9062f242065c
base_tree: 5f647d91911ce4142c25326973ed4422565ec1f1
verified: strong
---
# Fm tidy prunes state/outputs/<session>/ (compact-output's full texts, T-0783) older than 7
## Raw request
> fm tidy prunes state/outputs/<session>/ (compact-output's full texts, T-0783) older than 7 days
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm tidy --apply deletes state/outputs/<session>/ folders and statusline snapshots older than 7 days and leaves sessions/by-pid/ — verify with `python3 plugin/tests/run.py test_tidy`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tidy test, then prune in check_global
## Resume here
## Docs impact
none: tidy finding kinds are self-describing
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 11 tests in 1.6s (5 classes, 16 at a time; slowest: Apply 2s, Repeats 1s, Lanes 1s) / OK [ran] [tree 2039e63e2572] (2026-10-14T18:00:13Z)
- `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 11 tests in 1.9s (5 classes, 16 at a time; slowest: Apply 1s, Repeats 1s, Lanes 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2039e63e2572] (2026-10-14T18:00:16Z)
- `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 11 tests in 1.6s (5 classes, 16 at a time; slowest: Apply 2s, Repeats 1s, Lanes 1s) / OK [ran] [tree 2039e63e2572] (2026-10-14T18:00:16Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                35.3    39.1     150  [0] / SessionEnd                  32.4    36.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 2039e63e2572] (2026-10-14T18:02:12Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 11 tests in 1.6s (5 classes, 16 at a time; slowest: Apply 2s, Repeats 1s, Lanes 1s) / OK [ran] [tree 2039e63e2572] (2026-10-14T18:02:19Z)
- (audit self) `self: tidy now prunes outputs/<session>/ folders older than 7 days and skips directories under sessions/ (by-pid/ would have crashed os.remove after a quiet week)` → no findings [tree 2039e63e2572] (2026-10-14T18:02:19Z)
- (audit self) `self: tidy now prunes outputs/<session>/ folders older than 7 days and skips directories under sessions/ (by-pid/ would have crashed os.remove after a quiet week)` → no findings [tree 2039e63e2572] (2026-10-14T18:02:25Z)
## Log
- 2026-10-14T17:44:42Z created
- 2026-10-14T17:59:42Z set type=CLEAN, tier=S
- 2026-10-14T17:59:45Z focused
- 2026-10-14T18:02:25Z done
- 2026-10-14T18:02:26Z committed edb5d67 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-0703 [FEATURE M, done, 4 steps] Frontier 03 — Model routing, effort and cache economics — lesson: Context per turn, not output, drives spend here: thresholds for compa…
- research brainstorm-20261003-round4: 127 new ideas (6 lenses x 2 rounds, past the 152 of rounds 1-3). Grounded against the code and this session.
- decision 2026-09-26: Full autonomy for the rest of this session; after T-0009 and T-0012..T-0016, run 5 recursive rounds of brainstorm + Foreman self-improvement, each r…
- similar past tasks were M: consider --tier M
## Behaviour lock
test_tidy's 4 existing Apply/DryRun tests ran green before the fmtidy.py edit (the red run failed only the new test) and stay green after
## Lessons
- A state folder that gains a subfolder breaks every prune that assumed files only
## Files touched
- plugin/tests/test_tidy.py
- plugin/lib/fmtidy.py
