---
id: T-3387
type: SECURITY
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:54:31Z
updated: 2026-11-06T06:54:31Z
---
# fmguard.py:~4186 reads '#!/usr/bin/env -S python3' as interpreter '-S', so kind is None…
## Raw request
> SECURITY: fmguard.py:~4186 reads '#!/usr/bin/env -S python3' as interpreter '-S', so kind is None and a script run by path (./x) is never read: an agent could write an env -S script holding a blocked command and run it. Skip env flags (-S, -i, -u NAME) and NAME=val words when finding the interpreter; test (T-3363 review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T06:54:31Z created
## Follow-ups captured
