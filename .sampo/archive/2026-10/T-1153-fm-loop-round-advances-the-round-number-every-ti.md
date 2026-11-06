---
id: T-1153
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmloop.py, plugin/lib/fmcli.py, plugin/tests/test_loop.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-16T10:23:42Z
updated: 2026-10-16T10:53:41Z
base: 532cf708656d09c025ed07fc3121d9b7b678a428
base_tree: d1c78d64a70d9a79685f2ca9aca2ada4f2830dd7
plan0_at: 2026-10-16T10:49:16Z
plan0_scope: [plugin/lib/fmloop.py, plugin/lib/fmcli.py, plugin/tests/test_loop.py, CHANGELOG.md]
verified: strong
---
# Fm loop round advances the round number every time it is called, so reading the round's br
## Raw request
> fm loop round advances the round number every time it is called, so reading the round's brief twice skipped a round (the pane said round 3 during round 2): only fm loop yield (or an explicit --next) should advance it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm loop round with a round open and no yield re-shows that round's brief without advancing; --next (or a recorded yield) starts the next; fm next says --next when a round is open — verify with `python3 plugin/tests/run.py test_loop`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: round twice stays round 1; --next advances; action names --next
2. [x] round_brief(advance) and --next; action text
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_loop` → ✗ exit 1 · Ran 13 tests in 30.2s (3 classes, 16 at a time; slowest: Loop 30s, LoopReview 23s, PipeProgramDebris 1s) / FAILED (1 classes) [ran] [tree f2bdfcaa0041] (2026-10-16T10:50:06Z)
- (step 2) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 13 tests in 22.2s (3 classes, 16 at a time; slowest: Loop 21s, LoopReview 21s, PipeProgramDebris 1s) / OK [ran] [tree 8438e8bdab78] (2026-10-16T10:50:58Z)
- `python3 plugin/tests/run.py test_loop` → ✗ exit 1 · Ran 13 tests in 9.1s (3 classes, 16 at a time; slowest: Loop 8s, LoopReview 7s, PipeProgramDebris 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 40a85aa2fb17] (2026-10-16T10:51:38Z)
- `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 13 tests in 13.9s (3 classes, 16 at a time; slowest: LoopReview 13s, Loop 13s, PipeProgramDebris 0s) / OK [ran] [tree 40a85aa2fb17] (2026-10-16T10:51:38Z)
- (ac 1) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 13 tests in 8.7s (3 classes, 16 at a time; slowest: Loop 9s, LoopReview 8s, PipeProgramDebris 0s) / OK [ran] [tree 40a85aa2fb17] (2026-10-16T10:52:02Z)
- `python3 plugin/tests/run.py test_loop test_help` → exit 0 · Ran 18 tests in 13.4s (5 classes, 16 at a time; slowest: Loop 13s, LoopReview 12s, Help 2s) / OK [ran] [tree 40a85aa2fb17] (2026-10-16T10:52:02Z)
- (audit edge) `self: plain round re-shows the open round's brief (no state write); --next or a recorded yield advances; fm next and the drive say --next for an open round; old states without since fall back to started` → a yield then plain round advances as before; the drive key [round, briefs] is unchanged by a re-show [tree 40a85aa2fb17] (2026-10-16T10:52:02Z)
- (audit self) `self: plain round re-shows the open round's brief (no state write); --next or a recorded yield advances; fm next and the drive say --next for an open round; old states without since fall back to started` → no findings [tree 40a85aa2fb17] (2026-10-16T10:52:02Z)
## Log
- 2026-10-16T10:23:42Z created
- 2026-10-16T10:49:14Z set type=FIX, tier=S
- 2026-10-16T10:49:14Z set scope=['plugin/lib/fmloop.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_loop.py', 'CHANGELOG.md']
- 2026-10-16T10:49:15Z focused
- 2026-10-16T10:51:14Z scope: MASTER.md forever-loop line
- 2026-10-16T10:53:40Z done
- 2026-10-16T10:53:41Z committed 67393bb (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1057-review: MEDIUM** — `plugin/lib/fmloop.py:14,36` — "past every earlier ideas.md" is only the newest 6. [stale: plugin/evals/guard-force-push/prompt.md, pl…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- decision 2026-10-15: Round 5 slate: 7 builds from 54 grounded ideas (snapshot before discarding commands, risk-ranked review, claims audit, keep-going stall count, night…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_loop.py
## Plan gaps
- failed first: step 1 Failing test: round twice stays round 1; --next advances; action names --next
## Files touched
- plugin/tests/test_loop.py
- plugin/lib/fmloop.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
