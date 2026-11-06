---
id: T-2648
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdrill.py, plugin/tests/test_drill.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T20:14:01Z
builder_model: sonnet
base: 647ec35712e54aba72f3a5e9b5be53a59c99b17c
base_tree: 497d54e263425e87795eae263f11ff2940e66c8a
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T20:00:34Z
plan0_scope: [plugin/lib/fmdrill.py, plugin/tests/test_drill.py, CHANGELOG.md]
lane_stop: merged 2026-11-02T20:13:07Z
verified: strong
---
# fm drill gains a fault that drops one ledger event class (every task_done line, say): each reader that leans on it must name what's missing, never crash or report a silent zero
## Raw request
> FEATURE: fm drill gains a drop-one-ledger-class fault the readers must name, not crash on (c15: Ledger resilience: record-class deletion, mutation, torn writes, authorship; value 3, effort M, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the drop-class fault plants a ledger without task_done events, and the drill's verdict fails a reader that crashes or prints a zero rate as if measured, and passes one that says the class is missing — verify with `python3 plugin/tests/run.py test_drill`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the fault kind in fmdrill.KINDS, _plant and _verdict
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_drill 2>&1 | tail -8` → ✗ exit 1 · Ran 10 tests in 9.9s (2 classes, 16 at a time; slowest: Drill 8s, StateErrors 2s) / FAILED (1 classes: test_drill.Drill) [ran] [tree f78e16baff09] [world 2f1906870a] (2026-11-02T20:01:30Z)
- (step 1) `python3 plugin/tests/run.py test_drill` → ✗ exit 1 · Ran 10 tests in 9.4s (2 classes, 16 at a time; slowest: Drill 9s, StateErrors 3s) / FAILED (1 classes: test_drill.Drill) [ran] [tree f78e16baff09] [world 2f1906870a] (2026-11-02T20:01:42Z)
- (ac 1) `python3 plugin/tests/run.py test_drill 2>&1 | tail -30` → ✗ exit 1 · Ran 10 tests in 15.1s (2 classes, 16 at a time; slowest: Drill 14s, StateErrors 3s) / FAILED (1 classes: test_drill.Drill) [ran] [tree 96e83d482cd6] [world 2f1906870a] (2026-11-02T20:02:17Z)
- (ac 1) `python3 plugin/tests/run.py test_drill 2>&1 | tail -20` → ✗ exit 1 · Ran 10 tests in 10.4s (2 classes, 16 at a time; slowest: Drill 10s, StateErrors 2s) / FAILED (1 classes: test_drill.Drill) [ran] [tree 4b32e5a3001e] [world 2f1906870a] (2026-11-02T20:02:33Z)
- (ac 1) `python3 plugin/tests/run.py test_drill 2>&1 | tail -12` → exit 0 · Ran 10 tests in 10.1s (2 classes, 16 at a time; slowest: Drill 10s, StateErrors 2s) / OK [ran] [tree a19d7f3f77dd] [world 2f1906870a] (2026-11-02T20:03:02Z)
- (step 2) `python3 plugin/tests/run.py test_drill` → exit 0 · Ran 10 tests in 10.3s (2 classes, 16 at a time; slowest: Drill 10s, StateErrors 2s) / OK [ran] [tree a19d7f3f77dd] [world 2f1906870a] (2026-11-02T20:03:15Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cost test_cost_forecast test_drill test_economics test_export test_outcomes test_round_g test_trials test_usage_burn && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.39s] [ran] [tree a19d7f3f77dd] [world 2f1906870a] (2026-11-02T20:04:04Z)
- (step 1) `python3 plugin/tests/run.py test_drill` → exit 0 · Ran 10 tests in 7.3s (2 classes, 16 at a time; slowest: Drill 7s, StateErrors 2s) / OK [ran] [tree 7c3c746f5438] [world 2f1906870a] (2026-11-02T20:13:24Z)
- (step 3) `grep -q 'dropped ledger class' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 7c3c746f5438] [world 2f1906870a] (2026-11-02T20:13:24Z)
- (ac 1) `python3 plugin/tests/run.py test_drill` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T20:13:24Z [ran] [tree 7c3c746f5438] [world 2f1906870a] (2026-11-02T20:13:29Z)
- (audit edge) `self: read the builder diff; the verdict runs the real fm outcomes and fm digest against a ledger with every task_done stripped; a faked bare-rate reader is graded missed, not crashed (tested); dropped_class_lines fires only when done tasks exist and no task_done event does` → a ledger missing only some task_done lines still reads as measured (whole-class check, a stated ceiling); fmmandate, fmwatch and fmloop still read silently, captured as T-2660 [tree 7c3c746f5438] (2026-11-02T20:13:29Z)
- (audit self) `self: read the builder diff; the verdict runs the real fm outcomes and fm digest against a ledger with every task_done stripped; a faked bare-rate reader is graded missed, not crashed (tested); dropped_class_lines fires only when done tasks exist and no task_done event does` → no findings [tree 7c3c746f5438] (2026-11-02T20:13:29Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T20:00:14Z planned from capture
- 2026-11-02T20:00:19Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2648.builder.md
- 2026-11-02T20:00:33Z focused
- 2026-11-02T20:00:34Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T20:13:07Z merged worktree-agent-afd6a2003e114d0fa (4 file(s))
- 2026-11-02T20:13:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afd6a2003e114d0fa
- 2026-11-02T20:13:08Z focused
- 2026-11-02T20:13:15Z scope: plugin/lib/fmoutcomes.py and plugin/lib/fmcost.py — the fault's verdict needs the readers to say the class is missing; neither said anything before
- 2026-11-02T20:13:58Z done
- 2026-11-02T20:14:01Z committed 8de81627 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2657 [FEATURE S, done, 3 steps] flakes.json counts each flaky test's fails and passes; fm doctor lists the three worst by fail rate with the command that flakes them —…
- T-2653 [FEATURE S, active, 3 steps] Every nonzero fm exit prints one Next: command, not only a UsageError that carries one: a PolicyError, LockTimeout, CorruptState or V…
- T-2651 [FEATURE S, active, 3 steps] fm task evidence --bench CMD --under MS: a benchmark that is a pass/fail proof, failing when the median is over the threshold (today …
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_drill.py
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_drill.py
- plugin/lib/fmdrill.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmcost.py
- CHANGELOG.md
