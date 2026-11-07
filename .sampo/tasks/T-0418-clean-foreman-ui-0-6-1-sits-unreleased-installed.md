---
id: T-0418
type: CLEAN
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-09T13:33:05Z
updated: 2026-11-06T19:13:41Z
base: 4a9bf49a329a62d797e24dacdb67306687aa8570
base_tree: 94176e91d646b648c8b4d40c838a1ca1135013ed
paused_tree: 94176e91d646b648c8b4d40c838a1ca1135013ed
---
# Update the installed foreman-ui to 0.6.1
## Raw request
> CLEAN: foreman-ui 0.6.1 sits unreleased (installed 0.6.0; fm doctor WARN). Release it: tag the mod's changelog, then update the installed copy — claude plugin update foreman-ui@foreman is the plugin category, so it needs the user's yes (ask at the end of the run)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm doctor's foreman-ui release check passes — verify with `python3 plugin/bin/fm doctor 2>&1 | grep -E 'PASS +foreman-ui release'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] after the user's plugin yes: claude plugin marketplace update foreman; claude plugin update foreman-ui@foreman  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-09T13:33:05Z created
- 2026-10-09T13:33:38Z planned from capture
- 2026-10-09T13:33:38Z blocked: the repo is already 0.6.1; only the installed copy lags, and updating it is the plugin category: needs the user's yes, asked at the end of the run
- 2026-10-09T22:55:05Z set status=planned
- 2026-10-09T22:55:07Z focused
- 2026-10-09T22:56:56Z user approved plugin in Claude Code's permission prompt
- 2026-10-09T22:57:09Z plugin grant used for: claude plugin install changes Claude Code's plugins, MCP servers or config [plugin foreman-ui@foreman]
- 2026-10-10T00:27:29Z blocked: the user declined the grant for claude plugin update foreman-ui@foreman (2026-10-09); the 0.6.1 code already loads in place from the repo, only the recorded version is 0.6.0 — waits for the user's go-ahead
- 2026-11-06T19:13:41Z dropped: superseded: mods/foreman-ui is past 0.6.1 (see its plugin.json) and the code loads in place from the repo; nothing left to update
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Release and changelog (skills/playbooks/references/release/release-and-changelog.md)
- research t0036-operator: The implementation matches its documented contract and is well tested. Findings below are minor. [stale: plugin/uninstall.sh changed since it wa…
- research t0036-adversary: Confirmed: `check()` returns `Block` only when the category isn't in `ctx.allow`. Since `plugin` is in `ctx.allow` (from the earlier grant), `b…
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
## Behaviour lock
no code changes: the user updated the installed foreman-ui to 0.6.1 (claude plugin list: Version 0.6.1, enabled); fm doctor's release check is the whole criterion
