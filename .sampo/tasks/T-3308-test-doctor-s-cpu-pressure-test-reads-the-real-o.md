---
id: T-3308
type: FEATURE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T04:01:04Z
updated: 2026-11-06T04:01:04Z
---
# test_doctor's cpu-pressure test reads the real os.cpu_count(), which Python 3.13+ takes…
## Raw request
> test_doctor's cpu-pressure test reads the real os.cpu_count(), which Python 3.13+ takes from PYTHON_CPU_COUNT, so running the suite with PYTHON_CPU_COUNT=2 (the lead's load workaround on 2026-11-06) fails it; pin the CPU count in the test (FOREMAN_HOST cpus=) instead of reading the host
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
- 2026-11-06T04:01:04Z created
## Follow-ups captured
