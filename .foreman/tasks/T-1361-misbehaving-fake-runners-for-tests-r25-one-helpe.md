---
id: T-1361
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/tests/helpers.py, plugin/tests/test_code_fakes.py, plugin/lib/fmcode.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:52Z
updated: 2026-10-22T16:23:18Z
base: a618859efa0e64990c42595afe7f12cadf637f38
base_tree: 38def7a240fca052194ba892a94ff482ee20e68b
plan0_at: 2026-10-22T15:59:24Z
plan0_scope: [plugin/tests/helpers.py, plugin/tests/test_code_fakes.py, plugin/lib/fmcode.py, CHANGELOG.md]
verified: strong
---
# One helper for misbehaving fake runner CLIs in tests
## Raw request
> Misbehaving fake runners for tests (R25): one helper provides fakes that hang, go silent, prompt on a TTY, print garbage JSON, print usage-limit text, or fork and exit, used by the preflight, stall, lifecycle and failover tests
## Interpretation
fm code tests each hand-write fake CLI scripts (test_code_worker.py:29, test_code_hardening.py:123, test_code_envelope.py:62/82, test_code_bench.py:69). Failure modes fm code must survive — hang, go silent mid-stream, wait on a TTY prompt, print garbage JSON, print a usage-limit message, fork a child and exit — have no shared fakes, so the stall, preflight, lifecycle and failover paths are tested unevenly.
## Assumptions (confidence)
## Acceptance criteria
- [x] every misbehaving mode ends an fm code run within its bound and names the reason — verify with `cd plugin/tests && python3 -m unittest test_code_fakes`
## Non-goals
## Approach (options → choice → why)
A fake_cli(dir, name, mode, **kw) helper in plugin/tests/helpers.py writing a small executable for each mode (hang, silent, tty-prompt, garbage-json, usage-limit, fork-exit, ok); then one test per mode driving fm code with --worker <fake> and asserting it ends bounded with a named reason. Options: a Python fake server (more moving parts) → shell scripts like today's, collected.
## Risks and rollback
## Execution prompt
## Steps
1. [x] helper with the modes
2. [x] one bounded-end test per mode (fix any mode fm code mishandles, or capture it)
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 -c 'import sys; sys.path.insert(0,"plugin/tests"); import helpers; assert len(helpers.FAKE_MODES)==7'` → exit 0 · (no output) [ran] [tree cdb0cebb171f] (2026-10-22T16:04:37Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_code_fakes.py` → ✗ exit 1 · Ran 7 tests in 77.119s / FAILED (failures=1) [ran] [tree cdb0cebb171f] (2026-10-22T16:05:56Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_code_fakes.py` → exit 0 · Ran 7 tests in 59.392s / OK [ran] [tree 6e5134932b35] (2026-10-22T16:10:01Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code_fakes` → exit 0 · Ran 7 tests in 55.111s / OK [ran] [tree 99f4919ff7d5] (2026-10-22T16:20:29Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_fakes` → exit 0 · Ran 7 tests in 52.931s / OK [ran] [tree 99f4919ff7d5] (2026-10-22T16:21:23Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_fakes` → exit 0 · Ran 7 tests in 50.898s / OK [ran] [tree 7e3b02487059] (2026-10-22T16:22:24Z)
- (audit edge) `builder (sonnet); 7 fake modes, one bounded-end test each plus a coverage test; merged; test_code_fakes green twice (55 s).` → fakes sleep 60 s while runs time out at 2 s, so a real hang fails the 40 s bound; the 'timed out after 2 s' assertions are the firm evidence [tree 7e3b02487059] (2026-10-22T16:22:24Z)
- (audit intent) `builder (sonnet); 7 fake modes, one bounded-end test each plus a coverage test; merged; test_code_fakes green twice (55 s).` → preflight/stall/lifecycle paths now share one set of fakes; migrating the older ad-hoc fakes is left (not required) [tree 7e3b02487059] (2026-10-22T16:22:24Z)
- (audit self) `builder (sonnet); 7 fake modes, one bounded-end test each plus a coverage test; merged; test_code_fakes green twice (55 s).` → no findings [tree 7e3b02487059] (2026-10-22T16:22:24Z)
## Log
- 2026-10-21T03:47:52Z created
- 2026-10-22T15:43:36Z planned from capture
- 2026-10-22T15:45:16Z plan: grounded — ad-hoc fakes at test_code_worker.py:29, test_code_hardening.py:123, test_code_envelope.py:62/82, test_code_bench.py:69; goes to a builder when a lane frees
- 2026-10-22T15:59:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1361.builder.md
- 2026-10-22T15:59:23Z focused
- 2026-10-22T16:19:25Z merged worktree-agent-a51edb850c744e435 (2 file(s))
- 2026-10-22T16:19:27Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a51edb850c744e435
- 2026-10-22T16:19:29Z focused
- 2026-10-22T16:23:16Z done
- 2026-10-22T16:23:18Z committed 7ecfc54a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- research T-1320-review: Changes needed. Resume breaks for CLI-planned runs, and the planner's read-only mode is trusted with no check afterwards. [stale: plugin/lib/fmcl…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- decision 2026-10-21: fm code's no-setup default picks only a runner whose read-only mode is verified here (claude); codex/gemini plan only when named, with a note
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/helpers.py, plugin/tests/test_code_fakes.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 2 one bounded-end test per mode (fix any mode fm code mishandles, or capture it)
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_code_fakes.py
- CHANGELOG.md
