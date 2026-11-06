---
id: T-1542
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmpage.py, plugin/templates, site, plugin/tests/test_showpieces.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:49Z
updated: 2026-10-22T20:59:31Z
---
# Round 3 (T-1520): 3D showpieces with the 3D playbook: the repo as a 3D city in fm page, ta
## Raw request
> Round 3 (T-1520): 3D showpieces with the 3D playbook: the repo as a 3D city in fm page, tasks as metaballs that merge when proved, a live 3D task graph in fm code app, the guard as a 3D airlock in demos, the bench as a diorama race or walkable terrain, a 3D lookbook room (a085 c047 c168 c169 c170 b169 c022). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): 3D showpieces with the 3D playbook: the repo as a 3D city in fm page, tasks as metaballs that merge when proved, a live 3D task graph in fm code app, the guard as a 3D airlock in demos, the bench as a diorama race or walkable terrain, a 3D lookbook room (a085 c047 c168 c169 c170 b169 c022). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] each showpiece builds as a single file with a poster, aria-label and reduced-motion path, fed from fixture data — verify with `cd plugin/tests && python3 -m unittest test_showpieces`
## Non-goals
## Approach (options → choice → why)
Options: a game engine; chosen: showpieces built on the WebGL2 template and ui/scene-3d.md: the repo as a 3D city in fm page, tasks as metaballs that merge when proved, a live 3D task graph view (web, with a half-block version in fm code app), the guard as an airlock in demos, the bench as a diorama race or walkable terrain, a 3D lookbook room; each with a poster and reduced motion.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] city and task graph
3. [ ] metaballs, airlock, diorama, terrain
4. [ ] lookbook room
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:49Z created
- 2026-10-22T18:06:08Z set scope=['plugin/lib/fmpage.py', 'plugin/templates', 'site', 'plugin/tests/test_showpieces.py', 'CHANGELOG.md']
- 2026-10-22T20:59:31Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1542
## Follow-ups captured
