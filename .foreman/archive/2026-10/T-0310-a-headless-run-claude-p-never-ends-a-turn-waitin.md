---
id: T-0310
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T18:30:40Z
updated: 2026-10-04T18:33:10Z
base: 59b03fd9a7341de02acb383c931752231f2a9fe6
base_tree: 5397a2eac0cdb48b9deafc511d8e5bae5e85f85a
verified: strong
---
# A headless run (claude -p) never ends a turn waiting on background work it will never hear from
## Raw request
> A headless run (claude -p) never ends a turn waiting on background work it will never hear from
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] under CLAUDE_CODE_ENTRYPOINT=sdk-cli (or fm run) a Stop with background work running is held once with how to wait; interactive sessions still wait for the notification — verify with `python3 plugin/tests/run.py -p test_hooks.py -k Stop`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then a headless-wait nudge in the Stop hook
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_hooks.py -k Stop` → ✗ exit 1 · Ran 31 tests in 14.3s (1 classes, 16 at a time; slowest: Stop 14s) / FAILED (1 classes) [ran] [tree e87a9252b530] (2026-10-04T18:31:00Z)
- (step 1) `python3 plugin/tests/run.py -p test_hooks.py -k Stop` → exit 0 · Ran 31 tests in 14.5s (1 classes, 16 at a time; slowest: Stop 14s) / OK [ran] [tree af1c3f82b7be] (2026-10-04T18:31:36Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.1    32.2     150  [0] / SessionEnd                  27.8    29.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:59 UTC; python3 plugin/tests/run.py → exit 0 · Ran 824 tests in [ran] [tree 3044e8450032] (2026-10-04T18:32:56Z)
- (ac 1) `python3 plugin/tests/run.py -p test_hooks.py -k Stop` → exit 0 · Ran 31 tests in 14.3s (1 classes, 16 at a time; slowest: Stop 14s) / OK [ran] [tree 3044e8450032] (2026-10-04T18:33:10Z)
- (audit intent) `self: red→green Stop (sdk-cli and fm run held once with the headless reason; stop_hook_active lets go; cli unchanged); hooks, unattended and friction suites pass` → the court run's R-T-0201 ended its headless run waiting on a notification that can't come [tree 3044e8450032] (2026-10-04T18:33:10Z)
- (audit edge) `self: red→green Stop (sdk-cli and fm run held once with the headless reason; stop_hook_active lets go; cli unchanged); hooks, unattended and friction suites pass` → headless is CLAUDE_CODE_ENTRYPOINT == sdk-cli or FOREMAN_DRIVE_TASK (SDK sessions with streaming input can still be woken, so they're left alone); once per stop chain, so a task that never finishes can't loop; the engine's background_tasks list wins over Foreman's own events when sent [tree 3044e8450032] (2026-10-04T18:33:10Z)
- (audit self) `self: red→green Stop (sdk-cli and fm run held once with the headless reason; stop_hook_active lets go; cli unchanged); hooks, unattended and friction suites pass` → no findings [tree 3044e8450032] (2026-10-04T18:33:10Z)
## Log
- 2026-10-04T18:30:40Z created
- 2026-10-04T18:30:40Z focused
- 2026-10-04T18:33:10Z done
- 2026-10-04T18:33:10Z committed cc776e4 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0145 [FEATURE M, done, 3 steps] UI changes reach the running session during a drive: the Stop hook ends the turn once when this session's dev-mods changed, and the rel…
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- T-0109 [FEATURE M, done, 3 steps] Background shells visible; mascot drawn like Claude Code's Clawd; mini colored Claudes per subagent — lesson: Mods: module variables re…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
## Lessons
- Wait-for-notification is an interactive-session contract; in print mode the turn is the whole run
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
