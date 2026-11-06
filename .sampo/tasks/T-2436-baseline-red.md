---
id: T-2436
type: FIX
tier: M
status: dropped
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T18:10:04Z
updated: 2026-10-31T18:10:35Z
trigger: baseline
trigger_key: ae8188f74e0fa2a9
baseline: true
---
# Baseline red:…
## Raw request
> Baseline red: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py` fails test_code.Durable.test_a_kill_during_the_check_resumes_at_the_check_without_redoing_the_step, test_code.TaskRun.test_a_task_waiting_for_the_users_yes_runs_nothing_until_it_is_given. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-31T18:10:04Z created
- 2026-10-31T18:10:35Z dropped: duplicate of T-2435 (the same test_code TaskRun/Durable failure, found again by ship87)
## Follow-ups captured
