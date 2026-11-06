---
id: T-3059
type: FIX
tier: S
status: planned
priority: low
scope: [plugin/tests/test_site_build.py]
depends_on: []
source: genesis-review
created: 2026-11-05T00:31:08Z
updated: 2026-11-06T03:53:44Z
trigger: genesis-review
trigger_key: 58187438a6e7bdb0
---
# The site build test proves the published share image is a real PNG, not a symlink the deploy might not follow
## Raw request
> FIX: cross-cutting review gen-4 #3 (what got worse): site/assets/share.png shrank from a real image to 33 bytes (a symlink); the share card published by Pages now depends on the deploy dereferencing it, and no shipped check proves it does. [Bin 226340 -> 33 bytes]
> genesis-review 4:3
> (Filed at low priority: trigger genesis-review has precision 0.10 over its last 20 closed captures; fm triggers shows the record.)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] test_site_build builds the site into a temp dir and checks assets/share.png there is a regular file (not a symlink) over 10 KB starting with the PNG signature; checked live 2026-11-05: the Pages copy is 204,666 bytes, so this pins what works — verify with `python3 plugin/tests/run.py test_site_build`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] the test (green on today's build; red if build.py copied the link itself)  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T00:31:08Z created
- 2026-11-05T04:09:53Z planned from capture
- 2026-11-05T04:09:54Z set approved=True
- 2026-11-05T04:09:54Z set scope=['plugin/tests/test_site_build.py']
- 2026-11-05T04:09:55Z blocked: approved; waits for a builder slot (or the main thread between closes)
- 2026-11-06T03:53:44Z unblocked
## Follow-ups captured
