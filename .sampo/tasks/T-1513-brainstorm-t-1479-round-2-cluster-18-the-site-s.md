---
id: T-1513
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [site, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:42Z
updated: 2026-10-22T20:46:53Z
---
# Brainstorm T-1479 round 2 (cluster 18): the site's hero becomes a single-file WebGL or can
## Raw request
> Brainstorm T-1479 round 2 (cluster 18): the site's hero becomes a single-file WebGL or canvas proof-chain scene fed by site/data/stats.json, with a static poster fallback and reduced motion, built with ui/scene-3d.md (T-1494) and the template (T-1495)
## Interpretation
The site's hero becomes a single-file WebGL scene of the proof chain (tasks as stations, red→green as light travelling the track), fed by site/data/stats.json, with a static poster first, reduced motion, the survival contract from ui/scene-3d.md, and the template from T-1495. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the built index has the scene with a poster, aria-label, reduced-motion path and no external script; site tests pass — verify with `cd plugin/tests && python3 -m unittest test_site 2>/dev/null || python3 site/build.py --check`
## Non-goals
## Approach (options → choice → why)
Options: three.js from a CDN (a dependency the site avoids); chosen: the raw WebGL2 template, built by site/build.py into the page, poster rendered once and committed.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] scene from the template  <- CURRENT
2. [ ] data from stats.json
3. [ ] poster and checks
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:36:42Z created
- 2026-10-22T17:55:55Z set scope=['site', 'CHANGELOG.md']
- 2026-10-22T20:46:53Z dropped: split into T-1609 (poster) and T-1610 (WebGL scene over it), each M
## Follow-ups captured
