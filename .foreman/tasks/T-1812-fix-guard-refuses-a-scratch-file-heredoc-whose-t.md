---
id: T-1812
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-28T07:30:23Z
updated: 2026-10-28T08:18:48Z
---
# FIX: guard refuses a scratch-file heredoc whose target is $VAR/x (_SOURCE_WRITE's path cla
## Raw request
> FIX: guard refuses a scratch-file heredoc whose target is $VAR/x (_SOURCE_WRITE's path class has no $ and the target must be under plugin/) as interpreter code driving Foreman's modules (~20 fires). Fix: accept $VAR, ${VAR} and quoted targets, treat as data when the target's basename appears once; add FORMS. fmguard.py:1852-1870, 2078
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
- 2026-10-28T07:30:23Z created
- 2026-10-28T08:18:48Z dropped: measured 2026-10-28 over every transcript: 7 'driving Foreman's modules' refusals since 10-18, 1 with a $VAR heredoc target, and that command read the file again in a python heredoc (stem named twice, so the proposed rule wouldn't have passed it either). Widening the stem-once exemption beyond plugin/ (where the write is itself core-gated) lets conftest.py, sitecustomize.py or a .pth file run without being named; test_writing_a_foreman_source_file_is_not_driving_it asserts /tmp/x.py + pytest stays refused on purpose. The refusal already says: write in one command, run in the next
## Follow-ups captured
