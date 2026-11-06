---
id: T-0824
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T18:37:30Z
updated: 2026-10-14T18:40:47Z
base: 7eb3a6cac4b7c2f7f71bf7930f84f811df0c546f
base_tree: ee7c0734d9be63a8b4b2c698365ccadf944ccaeb
verified: strong
---
# Compact output caps the saved full text (keeps head and tail, marks the cut) so a runaway output can't fill the disk
## Raw request
> Compact output caps the saved full text (keeps head and tail, marks the cut) so a runaway output can't fill the disk
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a full text over the cap is saved as head + tail with a cut marker; under the cap it's saved whole — verify with `python3 plugin/tests/run.py test_compact`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then the cap in plugin/hooks/compact
## Resume here
## Docs impact
none: internal limit
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_compact` → exit 0 · Ran 8 tests in 0.6s (3 classes, 16 at a time; slowest: Install 1s, Compact 0s, PostToolUse 0s) / OK [ran] [tree 383b93960dab] (2026-10-14T18:38:45Z)
- `python3 plugin/tests/run.py test_compact` → ✗ exit 1 · Ran 8 tests in 1.0s (3 classes, 16 at a time; slowest: Install 1s, Compact 0s, PostToolUse 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 383b93960dab] (2026-10-14T18:38:47Z)
- `python3 plugin/tests/run.py test_compact` → exit 0 · Ran 8 tests in 0.6s (3 classes, 16 at a time; slowest: Install 1s, Compact 0s, PostToolUse 0s) / OK [ran] [tree 383b93960dab] (2026-10-14T18:38:47Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                38.7    41.6     150  [0] / SessionEnd                  36.9    39.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 383b93960dab] (2026-10-14T18:40:41Z)
- (ac 1) `python3 plugin/tests/run.py test_compact` → exit 0 · Ran 8 tests in 0.7s (3 classes, 16 at a time; slowest: Install 1s, Compact 0s, PostToolUse 0s) / OK [ran] [tree 383b93960dab] (2026-10-14T18:40:46Z)
- (audit edge) `self: the saved full text keeps its first and last 1M characters with a cut marker; the stub's path and the model-visible compaction are unchanged` → the file name still hashes the uncut text, so two runaways differing only in the middle don't overwrite each other's file [tree 383b93960dab] (2026-10-14T18:40:46Z)
- (audit self) `self: the saved full text keeps its first and last 1M characters with a cut marker; the stub's path and the model-visible compaction are unchanged` → no findings [tree 383b93960dab] (2026-10-14T18:40:46Z)
## Log
- 2026-10-14T18:37:30Z created
- 2026-10-14T18:38:11Z focused
- 2026-10-14T18:40:47Z done
- 2026-10-14T18:40:47Z committed ec6e1de (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- research brainstorm-round2-20261014: 437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run's ideas) in 29 capability clusters, each grounded in the co…
- T-0811 [CLEAN S, done, 1 steps] Fm tidy prunes state/outputs/<session>/ (compact-output's full texts, T-0783) older than 7 — lesson: A state folder that gains a subfolde…
- decision 2026-10-14: Keep the Read hook unscoped (T-0782 dropped)
- similar finished tasks took 1–3 steps
## Lessons
- Every write of untrusted-size data to disk needs a cap, even an opt-in one
## Files touched
- plugin/tests/test_compact.py
- plugin/hooks/compact
