---
id: T-3090
type: FIX
tier: S
status: dropped
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/test_cli.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-11-05T00:46:17Z
updated: 2026-11-05T05:12:11Z
---
# sampo check --affected says it started before it runs, and waits at most 60 s for load
## Raw request
> sampo check --affected prints no ✓/✗ when it only waited for load (core.py:510-518, cli.py:5679): print a leading 'affected tests start (N)' line and cap the load wait at 60 s, so a builder's tool timeout never eats the result
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo check --affected prints 'affected tests start (N): <cmd>' (flushed) before the run and waits for load at most 60 s, so a builder's tool timeout sees the start line and then the ✓/✗ line; the full sampo check keeps its 300 s wait — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test in test_cli: --affected under a faked high load prints the start line and passes limit 60 to wait_for_load  <- CURRENT
2. [ ] the start line and wait_for_load(..., limit=60) in cli's affected path
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T00:46:17Z created
- 2026-11-05T02:58:32Z planned from capture
- 2026-11-05T02:58:32Z set approved=True
- 2026-11-05T02:58:33Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_cli.py', 'CHANGELOG.md']
- 2026-11-05T02:58:33Z blocked: after T-3087's merge (cli.py); then a builder slot
- 2026-11-05T05:12:11Z dropped: covered by T-3144 (every targeted run, check --affected included, starts at once; full runs wait at most 60 s)
## Follow-ups captured
