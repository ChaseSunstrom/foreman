---
id: T-1789
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmsession.py, plugin/lib/fmcore.py, plugin/tests/test_session.py, plugin/tests/test_gate_friction.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T16:00:37Z
updated: 2026-10-23T16:10:40Z
base: 6aebec4576a30848f79885c0289d75a5ecb1cebd
base_tree: 85150770609ff5e31f13672a0cb96fc2e6bdf070
plan0_at: 2026-10-23T16:08:39Z
plan0_scope: [plugin/lib/fmsession.py, plugin/lib/fmcore.py, plugin/tests/test_session.py, plugin/tests/test_gate_friction.py, CHANGELOG.md]
verified: strong
---
# Flaky: test_session.Session.test_review_fixes failed on a tree then passed on the same tre
## Raw request
> Flaky: test_session.Session.test_review_fixes failed on a tree then passed on the same tree in the 2026-10-23 gate (fm check flagged a race); find the race and fix it
## Interpretation
The gate flagged test_session.Session.test_review_fixes as flaky with no failure text. Reading fmsession.stop found a race: it read the runner's pid before writing the stopped marker, so a runner that set its pid and checked the marker in between was never killed, ran its turn, and its later meta writes put the status back to running (what the test's stop-then-status check would see). Fix the order; and make the flake ledger keep each failure's text so the next flake can be diagnosed after its rerun passed.
## Assumptions (confidence)
## Acceptance criteria
- [x] stop writes its marker before it reads the pid, and a flaky record keeps how the test failed — verify with `python3 plugin/tests/run.py test_session test_gate_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: stop's order, the flake record's why
2. [x] stop: marker first; note_flakes keeps failure_excerpt per test and shows the assertion
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_session test_gate_friction` → ✗ exit 1 · Ran 36 tests in 6.5s (18 classes, 16 at a time; slowest: Session 6s, Typos 2s, Flakes 2s) / FAILED (2 classes) [ran] [tree 71f2df59fd94] (2026-10-23T16:08:51Z)
- (step 1) `python3 plugin/tests/run.py test_session test_gate_friction test_close_gates test_cli test_suite_hygiene` → exit 0 · Ran 178 tests in 23.9s (58 classes, 16 at a time; slowest: TaskLifecycle 24s, CloseGates 17s, StateViews 9s) / OK [ran] [tree 324da8934228] (2026-10-23T16:09:29Z)
- (step 2) `python3 plugin/tests/run.py test_session test_gate_friction test_close_gates test_cli test_suite_hygiene` → exit 0 · Ran 178 tests in 24.3s (58 classes, 16 at a time; slowest: TaskLifecycle 24s, CloseGates 18s, StateViews 9s) / OK [ran] [tree 324da8934228] (2026-10-23T16:09:54Z)
- (ac 1) `python3 plugin/tests/run.py test_session test_gate_friction` → exit 0 · Ran 36 tests in 6.9s (18 classes, 16 at a time; slowest: Session 7s, Typos 2s, Flakes 2s) / OK [ran] [tree 324da8934228] (2026-10-23T16:10:01Z)
- (ac 1) `python3 plugin/tests/run.py test_session test_gate_friction` → exit 0 · Ran 36 tests in 6.7s (18 classes, 16 at a time; slowest: Session 7s, Typos 2s, Flakes 2s) / OK [ran] [tree 324da8934228] (2026-10-23T16:10:18Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the runner sets its pid then checks the marker, so with the marker written first every interleaving either stops the runner itself or leaves a pid stop reads and kills; the flake record's text is redacted and capped at 700 characters a test, 20 tests a gate run` → the flagged flake traced to a real stop/start race in fmsession, fixed at the order of two lines; and the next flake keeps its failure text [tree 324da8934228] (2026-10-23T16:10:18Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the runner sets its pid then checks the marker, so with the marker written first every interleaving either stops the runner itself or leaves a pid stop reads and kills; the flake record's text is redacted and capped at 700 characters a test, 20 tests a gate run` → a stop of a session with no runner writes the marker and finds no pid, as before; a gate output that never names a failing test keeps no why; old flakes.json entries without why still load [tree 324da8934228] (2026-10-23T16:10:18Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): the runner sets its pid then checks the marker, so with the marker written first every interleaving either stops the runner itself or leaves a pid stop reads and kills; the flake record's text is redacted and capped at 700 characters a test, 20 tests a gate run` → the stop path still kills only a pid _alive confirms belongs to this session; failure text kept in local state goes through redact first, so a secret printed by a failing test isn't stored [tree 324da8934228] (2026-10-23T16:10:18Z)
- (audit self) `self review in the main thread (subagents paused by the usage budget): the runner sets its pid then checks the marker, so with the marker written first every interleaving either stops the runner itself or leaves a pid stop reads and kills; the flake record's text is redacted and capped at 700 characters a test, 20 tests a gate run` → no findings [tree 324da8934228] (2026-10-23T16:10:18Z)
## Log
- 2026-10-23T16:00:37Z created
- 2026-10-23T16:08:36Z set scope=['plugin/lib/fmsession.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_session.py', 'plugin/tests/test_gate_friction.py', 'CHANGELOG.md']
- 2026-10-23T16:08:38Z focused
- 2026-10-23T16:10:38Z done
- 2026-10-23T16:10:40Z committed 31101c2a (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0323-review: Changes needed. No path-traversal hole found. Stop, hand-off and the message path have real defects. [stale: plugin/lib/fmcli.py, plugin/lib/fmse…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- research T-0274-review-1: Verdict: approve with nits.** `note_flakes` can't change the exit code or hide a failure. The findings are a regex false-name problem, one miss…
- decision 2026-10-09: T-0476 quarantine skipped: fm check keeps treating a gate flaky 2+ times as failing
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_session.py
## Regression test
test_session.Session.test_stop_marks_before_it_reads_the_pid (stop's first read_meta must see the stopped marker: red before the fix) and test_gate_friction.Flakes.test_a_pass_on_the_in_run_rerun_records_the_names (the flaky record keeps the FAIL block)
## Why not caught
the race needs a runner to set its pid and check the marker between stop's read and write, a window of microseconds that only heavy gate load opened; the flake ledger kept test names but no failure text, so the failure couldn't be read after the rerun passed
## Lessons
- When a flake leaves no text, read the code under test for read-then-write orders before rerunning it
## Plan gaps
- failed first: step 1 red tests: stop's order, the flake record's why
## Files touched
- plugin/lib/fmcore.py
- plugin/lib/fmsession.py
- plugin/tests/test_gate_friction.py
- plugin/tests/test_session.py
- CHANGELOG.md
