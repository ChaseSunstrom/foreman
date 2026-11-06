---
id: T-2895
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/rune.py, site/build.py, site/genesis/genesis.js, plugin/tests/test_genesis.py, plugin/tests/test_site_build.py]
depends_on: []
source: discovered
created: 2026-11-04T04:53:03Z
updated: 2026-11-06T03:53:11Z
---
# sampo genesis export writes each model as its role in the data (from its profile, not its name), so the site pages drop their 'jarvis' word swaps and a repo named jarvis stays itself
## Raw request
> FIX: sampo genesis export maps endpoint and orchestrator names to roles in the data itself, telling a profile name from a repo of the same name, so the pages need no word swap
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] rune.export replaces each model field (a profile name such as jarvis-nothink) with its role from the profile (own or loopback large model: 'a large local model', loopback small: 'a local model', cloud: its family) and the orchestrator with 'the agent', field by field, never by a word match; a repo or project field named jarvis is kept; site/build.py's and genesis.js's jarvis regex swaps are removed and the pages read the same — verify with `python3 plugin/tests/run.py test_genesis test_site_build`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: an export with a jarvis-nothink model field and a 'jarvis (1,853)' repo field: the first becomes its role, the second stays; the pages need no swap  <- CURRENT
2. [ ] the role map in export, the swaps removed from build.py:573 and genesis.js:89
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T04:53:03Z created
- 2026-11-05T03:32:31Z planned from capture
- 2026-11-05T03:32:31Z set approved=True
- 2026-11-05T03:32:31Z set scope=['plugin/lib/sampo/rune.py', 'site/build.py', 'site/genesis/genesis.js', 'plugin/tests/test_genesis.py', 'plugin/tests/test_site_build.py']
- 2026-11-05T03:32:31Z blocked: approved; waits for a builder slot
- 2026-11-06T03:53:11Z unblocked
## Follow-ups captured
