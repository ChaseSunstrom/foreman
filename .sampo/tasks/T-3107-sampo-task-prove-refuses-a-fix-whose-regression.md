---
id: T-3107
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/test_verify_strength.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T03:07:29Z
updated: 2026-11-06T03:53:51Z
---
# sampo task prove accepts a regression test that already existed: with no changed test file it runs the check on the start tree as it was and now
## Raw request
> sampo task prove refuses a FIX whose regression test already existed and was red ('changed no test files: write the test first'), though the start tree vs now with that test is the proof; T-2943 needed a 'Regression test: none' section instead: prove should accept an existing test that is red on the start tree
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo task prove ID --run CMD on a task that changed no test file runs CMD on the start tree (its own tests as they were) and on the current tree: red then green is proved, green on both says it passes without the change; a task with no start commit still refuses — verify with `python3 plugin/tests/run.py test_verify_strength`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test in test_verify_strength: an existing test red on the start tree and green after a code-only fix is proved; 'true' with no changed test says it passes without the change (replacing the 'changed no test files' refusal test)  <- CURRENT
2. [ ] drop the refusal in cli.task_prove: no changed tests means nothing is copied over
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:07:29Z created
- 2026-11-05T03:10:33Z planned from capture
- 2026-11-05T03:10:33Z set approved=True
- 2026-11-05T03:10:33Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_verify_strength.py', 'CHANGELOG.md']
- 2026-11-05T03:10:33Z blocked: after T-3087's merge (cli.py); then a builder slot
- 2026-11-06T03:53:51Z unblocked
## Follow-ups captured
