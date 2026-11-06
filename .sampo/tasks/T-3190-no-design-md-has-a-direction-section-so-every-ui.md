---
id: T-3190
type: CLEAN
tier: S
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T10:07:44Z
updated: 2026-11-06T03:11:46Z
---
# Repo DESIGN.md records Sampo's direction (## Point of view, ## Direction with audacity bold), so UI edits stop prompting for one
## Raw request
> No DESIGN.md has a '## Direction' section, so every UI edit prompts for one (T-3170 noticed): write the live page's and the site's direction (modern dashboard by default, forge as a setting; crafted, detailed, animated, never cartoonish) into DESIGN.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] DESIGN.md at the repo root has a concrete ## Point of view and a ## Direction naming audacity bold: modern dashboard with real charts by default, the illustrated forge only as a setting; crafted, detailed, animated, never cartoonish; both themes and phone width — verify with `sampo design sprint .`
- [ ] a UI edit in this repo no longer gets the design-direction note (hooks._design_note finds the direction) — verify with `python3 plugin/tests/run.py test_design`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] write DESIGN.md (Point of view, Direction, a pointer to design/sampo/tokens.json for tokens)  <- CURRENT
2. [ ] verify the sprint's brief and direction stages pass
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T10:07:44Z created
- 2026-11-06T03:11:43Z planned from capture
## Follow-ups captured
