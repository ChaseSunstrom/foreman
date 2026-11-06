---
id: T-1550
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcodeterm.py, .github/workflows, plugin/tests/test_portability.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:51Z
updated: 2026-10-22T20:59:37Z
---
# Round 3 (T-1520): Portability: fm home export|import between machines, the fm code app on
## Raw request
> Round 3 (T-1520): Portability: fm home export|import between machines, the fm code app on macOS and Windows, a differential parity oracle for ports, and lessons exchanged by git bundle (c034 c103 c019 b155). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Portability: fm home export|import between machines, the fm code app on macOS and Windows, a differential parity oracle for ports, and lessons exchanged by git bundle (c034 c103 c019 b155). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm home export then import into an empty home round-trips state and drops secrets; the parity oracle reports a difference — verify with `cd plugin/tests && python3 -m unittest test_portability`
## Non-goals
## Approach (options → choice → why)
Options: docs only; chosen: fm home export|import (a tarball of state minus secrets, verified on import), fm code app checked on macOS and Windows terminals (CI matrix jobs, Windows console API through ctypes where needed), a differential parity oracle for ports (same inputs through two implementations, outputs compared), and lessons exchanged as git bundles.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] home export and import
3. [ ] macOS/Windows terminal support
4. [ ] parity oracle and lesson bundles
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:51Z created
- 2026-10-22T18:06:25Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcodeterm.py', '.github/workflows', 'plugin/tests/test_portability.py', 'CHANGELOG.md']
- 2026-10-22T20:59:37Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1550
## Follow-ups captured
