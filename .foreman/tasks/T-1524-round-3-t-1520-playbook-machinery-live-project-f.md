---
id: T-1524
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/skills/playbooks/SKILL.md, plugin/tests/test_playbook_machinery.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:43Z
updated: 2026-10-22T20:59:20Z
---
# Round 3 (T-1520): Playbook machinery: live project facts injected at load, inheritance and
## Raw request
> Round 3 (T-1520): Playbook machinery: live project facts injected at load, inheritance and project overlays, a chain router with stage contracts, fm playbooks blame, a preview of a playbook's output, a coverage heatmap by stage and stack, stages bound to guard modes, and a five-rule UI contract gate (c073 c149 c145 c128 a139 a026 b146 a178). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Playbook machinery: live project facts injected at load, inheritance and project overlays, a chain router with stage contracts, fm playbooks blame, a preview of a playbook's output, a coverage heatmap by stage and stack, stages bound to guard modes, and a five-rule UI contract gate (c073 c149 c145 c128 a139 a026 b146 a178). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] an overlay extends a shipped playbook; facts resolve at load; the router names a playbook per stage; blame and preview print — verify with `cd plugin/tests && python3 -m unittest test_playbook_machinery`
## Non-goals
## Approach (options → choice → why)
Options: one big router; chosen: small pieces: facts injected at load (a {{fact}} placeholder resolved from fm map), project overlays (.foreman/playbooks/<name>.md appends to the shipped one), a stage router that names the next playbook from the task's stage, fm playbooks blame (which lines came from which task), a preview that shows the checks a playbook will apply, a coverage heatmap, and a five-rule UI contract gate.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] overlays and facts
3. [ ] router, blame, preview, heatmap
4. [ ] UI contract gate
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:43Z created
- 2026-10-22T17:57:51Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/skills/playbooks/SKILL.md', 'plugin/tests/test_playbook_machinery.py', 'CHANGELOG.md']
- 2026-10-22T20:59:20Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1524
## Follow-ups captured
