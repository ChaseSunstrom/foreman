---
id: T-1533
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmcritique.py, plugin/lib/fmcli.py, plugin/lib/smoke_web.cjs, plugin/tests/test_critique.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:46Z
updated: 2026-10-22T20:59:26Z
---
# Round 3 (T-1520): Design critique tools: a computed-style census critique, 'why does this
## Raw request
> Round 3 (T-1520): Design critique tools: a computed-style census critique, 'why does this element look like this', a squint test, red-pencil screenshot markup that files scoped tasks, pseudo-localisation and content stress, surface profiles (TV, e-ink, car, wrist), fm check layout for near-misses, slop bingo, a detector that lints built UI against its brief, and an optional local vision model (c068 a149 a174 c041 c054 a169 b130 b157 c049 c147 b027). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Design critique tools: a computed-style census critique, 'why does this element look like this', a squint test, red-pencil screenshot markup that files scoped tasks, pseudo-localisation and content stress, surface profiles (TV, e-ink, car, wrist), fm check layout for near-misses, slop bingo, a detector that lints built UI against its brief, and an optional local vision model (c068 a149 a174 c041 c054 a169 b130 b157 c049 c147 b027). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] the census lists styles in use and flags ones DESIGN.md doesn't name; pseudo-localisation expands strings; an annotation becomes a captured task — verify with `cd plugin/tests && python3 -m unittest test_critique`
## Non-goals
## Approach (options → choice → why)
Options: cloud vision (never); chosen: stdlib and browser-side critique tools: a computed-style census (fonts, colours, radii, shadows in use) critiqued against DESIGN.md, a 'why does this look like this' dump for a selector, a squint render, red-pencil annotations that become fm capture tasks, pseudo-localisation, surface profiles, fm check layout for near-misses, slop bingo over fm design lint, a brief-vs-built check, and a local vision model only when one is installed.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] census and why
3. [ ] pseudo-localisation, profiles, layout
4. [ ] annotations to tasks, bingo, brief check, optional vision
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:46Z created
- 2026-10-22T17:58:19Z set scope=['plugin/lib/fmcritique.py', 'plugin/lib/fmcli.py', 'plugin/lib/smoke_web.cjs', 'plugin/tests/test_critique.py', 'CHANGELOG.md']
- 2026-10-22T20:59:26Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1533
## Follow-ups captured
