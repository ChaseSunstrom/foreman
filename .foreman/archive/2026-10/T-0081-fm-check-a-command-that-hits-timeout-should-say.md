---
id: T-0081
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-01T11:12:50Z
updated: 2026-10-02T19:01:08Z
done_in: T-0088
---
# fm check says 'timed out after N s' on a timeout
## Raw request
> fm check: a command that hits --timeout should say 'timed out after N s' (it printed only '✗ exit 1 (600.2 s)'), and the default 600 s per command is too short for this repo's cargo test now — evidence: T-0082 gate failed by timeout and was misread as passing before commit
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] a check command hitting --timeout prints 'timed out after N s' and fails — verify with `python3 -m unittest discover -s plugin/tests -p test_round_i.py -q`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] red test  <- CURRENT
2. [ ] label timeout in fm check output
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-01T11:12:50Z created
- 2026-10-02T18:34:52Z planned from capture
- 2026-10-02T19:01:08Z done in T-0088
## Follow-ups captured
