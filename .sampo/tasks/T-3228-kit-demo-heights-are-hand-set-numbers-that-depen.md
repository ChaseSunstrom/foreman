---
id: T-3228
type: CLEAN
tier: S
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T18:13:17Z
updated: 2026-11-06T03:17:30Z
---
# Kit demo heights come from a measured render, not hand-set numbers in ui-kit.html's markers
## Raw request
> kit demo heights are hand-set numbers that depend on installed fonts: measure each demo's height in the render check instead (T-3102 noticed)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] ui-kit.html's markers carry no height (<!-- kit: NAME -->); smallcards.kit() returns each demo's height measured by works.check_html (cached by the demo's text hash), so a different installed font changes the number, not the test — verify with `python3 plugin/tests/run.py test_small_cards`
- [ ] the site's kit.json and the cards page size each demo frame from the measured height, unchanged in shape — verify with `python3 plugin/tests/run.py test_site_build`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: a marker without a height parses and kit() reports the rendered height  <- CURRENT
2. [ ] measure in kit() with a hash-keyed cache; drop the numbers from ui-kit.html; site build reads the measured h
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T18:13:17Z created
- 2026-11-06T03:17:29Z planned from capture
## Follow-ups captured
