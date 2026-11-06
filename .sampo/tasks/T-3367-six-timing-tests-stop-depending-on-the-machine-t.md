---
id: T-3367
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/tests/test_lanes.py, plugin/tests/test_doctor.py, plugin/tests/test_demo.py, plugin/tests/test_docs.py, plugin/tests/test_cli.py, plugin/tests/test_showpieces.py]
depends_on: []
source: followup
created: 2026-11-06T05:55:41Z
updated: 2026-11-06T05:56:25Z
lane: ~/.claude/foreman/.claude/worktrees/agent-acfb0602c7edc4502
lane_branch: worktree-agent-acfb0602c7edc4502
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:56:25Z
plan0_scope: [plugin/tests/test_lanes.py, plugin/tests/test_doctor.py, plugin/tests/test_demo.py, plugin/tests/test_docs.py, plugin/tests/test_cli.py, plugin/tests/test_showpieces.py]
---
# Six timing tests stop depending on the machine: test_lanes stall test sets the mtime ahead (not now), test_doctor stubs os.cpu_count (closes T-3308), test_demo drops its wall-clock assert for fm's scaled timeout, test_docs Fences scales CHECK_SECONDS, test_cli parallel captures retry on exit 3 and assert all 8, test_showpieces frame count scales with busy_factor
## Raw request
> Six timing tests stop depending on the machine: test_lanes stall test sets the mtime ahead (not now), test_doctor stubs os.cpu_count (closes T-3308), test_demo drops its wall-clock assert for fm's scaled timeout, test_docs Fences scales CHECK_SECONDS, test_cli parallel captures retry on exit 3 and assert all 8, test_showpieces frame count scales with busy_factor
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] they pass under load and with a pinned CPU count — verify with `python3 plugin/tests/run.py --load 48 test_lanes test_doctor test_demo test_docs test_cli test_showpieces`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] the six edits  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:55:41Z created
- 2026-11-06T05:56:22Z focused
- 2026-11-06T05:56:25Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3338 [FIX S, active, 2 steps] Test runner under load: run.py scales each class's timer with busy_factor (the --deadline clamp unchanged) and records a killed class's t…
- T-1730 [FIX M, done, 3 steps] Load-proof tests: hook-call timeouts, redaction and loop-review races, and frame-count windows that fail only with buil… — lesson: Judge an…
- T-2152 [FIX M, done, 3 steps] CI failed on this branch: run 41054274567 — lesson: A test's timing bound should come from a real budget (the hook's configured timeout), n…
- decision 2026-11-05: [costly] T-3177 parked, branch kept (f5e8ec11): the machine-wide test slot pool at 2x cpu matches unpooled at 2 concurrent runs (19.1 vs 18.7 s) and…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
