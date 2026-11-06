---
id: T-1900
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md]
depends_on: [T-1899]
source: discovered
created: 2026-10-29T03:02:31Z
updated: 2026-10-29T04:07:45Z
done_in: T-1905
---
# Fm task set --section reads bare 'done when :: cmd' criteria and unnumbered step lines (th
## Raw request
> fm task set --section reads bare 'done when :: cmd' criteria and unnumbered step lines (the --ac/--step forms); they stayed plain text and fm focus refused T-1899
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] --section reads bare criteria and unnumbered steps — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing test: bare 'works :: cmd' and unnumbered step lines  <- CURRENT
2. [ ] _task_new_forms adds the checkbox and the numbers
3. [ ] CHANGELOG line
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-29T03:02:31Z created
- 2026-10-29T03:05:40Z set type=FIX, tier=S, scope=['plugin/lib/fmcli.py', 'plugin/tests/test_cli.py', 'CHANGELOG.md'], depends_on=['T-1899']
- 2026-10-29T03:05:41Z planned: it has criteria and steps
- 2026-10-29T03:28:53Z batched into T-1905
- 2026-10-29T04:07:45Z done in T-1905 (batch)
## Follow-ups captured
