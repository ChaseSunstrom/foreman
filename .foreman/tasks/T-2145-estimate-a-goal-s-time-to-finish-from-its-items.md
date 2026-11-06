---
id: T-2145
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T10:40:19Z
updated: 2026-10-31T07:03:57Z
inferred_deps: [T-2135]
inferred_why: T-2135: estimate uses the goal's items' history
base: eb5a0858c58489b60345aad57b71549ac9b5b8dc
base_tree: fdeae8e9a9b2a4c4c7b1accacc92ec0ef0a2b333
plan0_at: 2026-10-31T06:54:48Z
plan0_scope: []
verified: strong
---
# Estimate a goal's time to finish from its items' history (Mission 4 inbox)
## Raw request
> Estimate a goal's time to finish from its items' history (Mission 4 inbox)
## Interpretation
Mission 4's goal ledger says how many items are done, not how long the rest will take. Each done item links tasks, and each closed task records its active minutes (fmoutcomes.record_close: minutes, attempts), so the history to estimate from is already kept.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm goal show prints 'about X left (median per item over N done items, P25–P75)' from the done items' linked tasks' active minutes, 'no estimate yet' under 3 done items, and --json carries the numbers — verify with `python3 plugin/tests/run.py test_goal`
## Non-goals
## Approach (options → choice → why)
1) fm goal show (and --json) adds 'about Xh left (median Ym per item over N done; range)': remaining items × the median active minutes of the done items' linked tasks, with the 25th–75th percentile as the range, and 'no estimate yet' under 3 done items; 2) a model estimate — rejected: tokens, and no better than the history; 3) per-tier averages across the project — rejected: a goal's own items are the better sample. Choice 1.
## Risks and rollback
Few samples mislead: under 3 done items it says no estimate. Items with no linked task are counted as remaining but not sampled. Rollback: display-only.
## Execution prompt
## Steps
1. [x] red tests from seeded items, links and closes: estimate, range, too-few case, json
2. [x] the estimate in fmmandate.show
3. [x] docs: give MASTER and CHANGELOG lines in the report
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_goal` → ✗ exit 1 · Ran 29 tests in 5.8s (6 classes, 16 at a time; slowest: GoalReview 4s, GoalEstimate 4s, GoalPlan 3s) / FAILED (1 classes) [ran] [tree 0d2cf42b3390] (2026-10-31T06:55:20Z)
- (step 2) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 29 tests in 3.6s (6 classes, 16 at a time; slowest: GoalEstimate 3s, GoalReview 3s, GoalPlan 3s) / OK [ran] [tree 90cae1214785] (2026-10-31T06:55:35Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_goal test_mandate && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [25.79s] [ran] [tree 90cae1214785] (2026-10-31T06:56:06Z)
- `python3 plugin/tests/run.py test_goal` → ✗ exit 1 · Ran 31 tests in 4.3s (7 classes, 16 at a time; slowest: GoalReview 3s, GoalEstimate 3s, GoalPlan 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d32bfd1dca3f] (2026-10-31T07:03:04Z)
- `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 31 tests in 3.5s (7 classes, 16 at a time; slowest: GoalEstimate 3s, GoalReview 3s, GoalPlan 3s) / OK [ran] [tree d32bfd1dca3f] (2026-10-31T07:03:04Z)
- (step 1) `python3 plugin/tests/run.py test_goal test_docs` → exit 0 · Ran 114 tests in 8.2s (29 classes, 16 at a time; slowest: Fences 8s, GoalEstimate 3s, GoalReview 3s) / OK [ran] [tree d32bfd1dca3f] (2026-10-31T07:03:12Z)
- (step 2) `python3 plugin/tests/run.py test_goal test_docs` → exit 0 · Ran 114 tests in 8.2s (29 classes, 16 at a time; slowest: Fences 8s, GoalEstimate 3s, GoalReview 3s) / OK [ran] [tree d32bfd1dca3f] (2026-10-31T07:03:21Z)
- (step 3) `python3 plugin/tests/run.py test_goal test_docs` → exit 0 · Ran 114 tests in 8.3s (29 classes, 16 at a time; slowest: Fences 8s, GoalEstimate 4s, GoalReview 3s) / OK [ran] [tree d32bfd1dca3f] (2026-10-31T07:03:29Z)
- (ac 1) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 31 tests in 3.5s (7 classes, 16 at a time; slowest: GoalEstimate 3s, GoalReview 3s, GoalPlan 3s) / OK [ran] [tree d32bfd1dca3f] (2026-10-31T07:03:40Z)
- (audit intent) `self-review of the diff: minutes come from the task_done ledger events (record_close keeps none), one number per done item summed over its linked tasks; non-numeric values ignored; read-only` → a goal says how long the rest will take, from its own history (test_goal red-to-green) [tree d32bfd1dca3f] (2026-10-31T07:03:40Z)
- (audit edge) `self-review of the diff: minutes come from the task_done ledger events (record_close keeps none), one number per done item summed over its linked tasks; non-numeric values ignored; read-only` → under 3 sampled items or no open item gives no estimate; a reopened task counts its latest close [tree d32bfd1dca3f] (2026-10-31T07:03:40Z)
## Log
- 2026-10-30T10:40:19Z created
- 2026-10-31T06:54:36Z set tier=M
- 2026-10-31T06:54:36Z planned: it has criteria and steps
- 2026-10-31T06:54:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2145.builder.md
- 2026-10-31T06:54:48Z focused
- 2026-10-31T07:02:50Z merged worktree-agent-a72801b51922df463 (2 file(s))
- 2026-10-31T07:02:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a72801b51922df463
- 2026-10-31T07:02:50Z focused
- 2026-10-31T07:03:35Z scope: plugin/lib/fmmandate.py (estimate, estimate_line, show), plugin/tests/test_goal.py, MASTER.md, CHANGELOG.md
- 2026-10-31T07:03:57Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1061 [FEATURE M, done, 2 steps] Calibration ledger: a plan predicts its size (files touched, minutes, attempts); the close — lesson: A self-regulating gate needs one r…
- decision 2026-10-31: [revisited: Mission 4: the goal ledger grows fm mandate] Mission 4 as built: the goal ledger lives on fm mandate's record (one standing goal: text, …
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- T-2144 [FEATURE M, active, 3 steps] Goal remaining distance as one number on the statusline and terminal title (Mission 4…
- similar finished tasks took 2–2 steps
## Lessons
- Estimate from the sample that matters (this goal's items), and say when the sample is too small
## Plan gaps
- failed first: step 1 red tests from seeded items, links and closes: estimate, range, too-few case, json
## Files touched
- plugin/tests/test_goal.py
- plugin/lib/fmmandate.py
- plugin/lib/fmcore.py
- site/pages.py
