---
id: T-0372
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-09T00:01:51Z
updated: 2026-10-09T00:46:53Z
base: 6a3a9c25efcdd1e05a486920ada53f2bfb7ff1f1
base_tree: 3ed35f8b6b2b47092c01f05d1c8ab2d988881bb2
verified: strong
---
# The headless wait nudge only on Claude Code before 2.1.292 (newer claude -p waits for background work itself)
## Raw request
> Claude Code 2.1.292: one-shot claude -p and SDK runs now wait for background commands and wakeups, so Foreman's _headless_wait nudge (T-0310) is redundant there; keep it for older builds or drop it once ≥2.1.292 is the floor
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a headless Stop with background work nudges on 2.1.200 and not on 2.1.295 — verify with `python3 plugin/tests/run.py -k test_a_headless_run_waits_for_its_background_work_itself`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: version-gated nudge with a day-cached claude --version
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_a_headless_run_waits_for_its_background_work_itself` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Stop 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 5af9996c2fbb] (2026-10-09T00:46:48Z)
- `python3 plugin/tests/run.py -k test_a_headless_run_waits_for_its_background_work_itself` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Stop 0s) / OK [ran] [tree 5af9996c2fbb] (2026-10-09T00:46:48Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_headless_run_waits_for_its_background_work_itself` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Stop 0s) / OK [ran] [tree 5af9996c2fbb] (2026-10-09T00:46:49Z)
- (step 1) `python3 plugin/tests/run.py -k test_a_headless_run_waits_for_its_background_work_itself` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Stop 0s) / OK [ran] [tree 5af9996c2fbb] (2026-10-09T00:46:49Z)
- (audit self) `self: the version read happens only on a headless Stop (rare), is cached a day, and unknown → () keeps the nudge (old behaviour)` → no findings [tree 5af9996c2fbb] (2026-10-09T00:46:49Z)
- (audit self) `self: the version read happens only on a headless Stop (rare), is cached a day, and unknown → () keeps the nudge (old behaviour)` → no findings [tree 5af9996c2fbb] (2026-10-09T00:46:53Z)
## Log
- 2026-10-09T00:01:51Z created
- 2026-10-09T00:46:00Z planned from capture
- 2026-10-09T00:46:01Z focused
- 2026-10-09T00:46:53Z done
- 2026-10-09T00:46:53Z committed 29f0c21 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- T-0152 [CLEAN S, done, 1 steps] drive_wait is logged once per wait, not on every Stop
- T-0145 [FEATURE M, done, 3 steps] UI changes reach the running session during a drive: the Stop hook ends the turn once when this session's dev-mods changed, and the rel…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- similar finished tasks took 1–3 steps
- likely tests for the scope: plugin/tests/test_hooks.py
## Behaviour lock
none run before the first edit; the behaviour is locked by test_a_headless_run_waits_for_its_background_work_itself (nudge on 2.1.200, not on 2.1.295; non-headless never) and the full hooks suite, both green after
## Lessons
- When the platform fixes what a workaround covered, gate the workaround on the version instead of deleting it: older installs still need it
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
