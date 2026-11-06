---
id: T-2673
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T21:30:41Z
updated: 2026-11-02T21:51:05Z
builder_model: sonnet
base: b38c5388069b88e883f4e5ef7e79edb0c63dc4a8
base_tree: 25470459a4ab7f3eb27174178a7c22e88a5e43f7
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T21:31:31Z
plan0_scope: []
lane_stop: merged 2026-11-02T21:49:25Z
verified: strong
---
# every list fm cuts at N says how many it left out and the flag that shows them: one helper in fmcore for the fmcli sites that cut silently
## Raw request
> FIX: every list fm cuts at N says how many it left out and the flag that shows them: one helper in fmcore used by the 22 fmcli sites that cut silently
> CONTEXT: Genesis gen-3 Mission 6 (#2 exhaustive thinking), gen-3/mission-exhaustive-thinking.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] c.more(items, n, flag) returns the first n and a 'N left out (FLAG)' line; every fmcli join over a [:N] slice that printed no count uses it, so the silent-site count (22) is 0 by the same scan — verify with `python3 plugin/tests/run.py test_left_out`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: the helper, and a scan of fmcli for join(...[:N]) with no count beside it
2. [x] the helper and the sites
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_left_out 2>&1 | grep -E "^[0-9]+:|Error|FAIL" | head -40` → ✗ exit 1 · FAILED (failures=1, errors=1) / FAILED (1 classes: test_left_out.LeftOut) [ran] [tree 29146c2c993f] [world 2f1906870a] (2026-11-02T21:31:46Z)
- (step 1) `python3 plugin/tests/run.py test_left_out` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: LeftOut 0s) / OK [ran] [tree 43de08930023] [world 2f1906870a] (2026-11-02T21:35:00Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_core test_guard_cases test_left_out test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.08s] [ran] [tree 43de08930023] [world 2f1906870a] (2026-11-02T21:36:16Z)
- `python3 plugin/tests/run.py test_left_out` → ✗ exit 1 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: LeftOut 0s) / FAILED (1 classes: test_left_out.LeftOut) (start tree + this task's tests) [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T21:49:37Z)
- `python3 plugin/tests/run.py test_left_out` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: LeftOut 0s) / OK [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T21:49:37Z)
- (step 2) `python3 plugin/tests/run.py test_left_out test_cli` → exit 0 · Ran 147 tests in 21.4s (45 classes, 16 at a time; slowest: TaskLifecycle 21s, CaptureAndIntake 10s, StateViews 10s) / OK [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T21:49:59Z)
- (step 3) `python3 plugin/tests/run.py test_left_out test_cli` → exit 0 · Ran 147 tests in 24.4s (45 classes, 16 at a time; slowest: TaskLifecycle 24s, CaptureAndIntake 11s, StateViews 11s) / OK [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T21:50:24Z)
- (ac 1) `python3 plugin/tests/run.py test_left_out` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T21:49:37Z [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T21:50:25Z)
- (audit edge) `self: reviewed the builder diff; more() returns '' when nothing is cut, so output only grows when a list was cut; 3 sites marked 'not a list' with their reason, accepted by the scan` → a list of exactly n prints no note; the scan covers fmcli.py only (other modules may still cut silently, captured) [tree 37c80f3d08ed] (2026-11-02T21:50:25Z)
- (audit self) `self: reviewed the builder diff; more() returns '' when nothing is cut, so output only grows when a list was cut; 3 sites marked 'not a list' with their reason, accepted by the scan` → no findings [tree 37c80f3d08ed] (2026-11-02T21:50:25Z)
## Log
- 2026-11-02T21:30:41Z created
- 2026-11-02T21:31:13Z planned from capture
- 2026-11-02T21:31:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2673.builder.md
- 2026-11-02T21:31:30Z focused
- 2026-11-02T21:31:31Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T21:49:25Z merged worktree-agent-aa2e218c50a113274 (3 file(s))
- 2026-11-02T21:49:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa2e218c50a113274
- 2026-11-02T21:49:26Z focused
- 2026-11-02T21:50:24Z scope: plugin/lib/fmcore.py (the more() helper), CHANGELOG.md
- 2026-11-02T21:51:02Z done
- 2026-11-02T21:51:05Z committed 6a4e4a50 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-02: Recommendation: Mission 6 builds three gaps where Foreman drops part of a request's space silently (a grid lens, a count on every cut list, a canary…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2077 [RESEARCH L, blocked, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- similar past tasks were L: consider --tier L
- similar finished tasks took 4–5 steps
## Why not caught
no test asserted on what a cut list leaves unsaid; the scan is that test now
## Files touched
- plugin/tests/test_left_out.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- CHANGELOG.md
