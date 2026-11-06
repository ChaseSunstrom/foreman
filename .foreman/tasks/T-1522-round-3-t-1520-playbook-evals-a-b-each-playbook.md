---
id: T-1522
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/evals, plugin/tests/test_playbook_evals.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:43Z
updated: 2026-10-22T20:59:19Z
---
# Round 3 (T-1520): Playbook evals: A/B each playbook against none on held-out briefs, ablat
## Raw request
> Round 3 (T-1520): Playbook evals: A/B each playbook against none on held-out briefs, ablate lines that don't earn their place, tune descriptions against the reach set, replay old bug fixtures after a playbook edit, an overnight variant search, and hot-reload against the scripted fake model (ideas a019 a055 a081 b021 b046 c093 c099 b152). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Playbook evals: A/B each playbook against none on held-out briefs, ablate lines that don't earn their place, tune descriptions against the reach set, replay old bug fixtures after a playbook edit, an overnight variant search, and hot-reload against the scripted fake model (ideas a019 a055 a081 b021 b046 c093 c099 b152). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm playbooks eval runs a playbook's held-out briefs with and without it on the fake model and records the lift; ablation reports each section's share — verify with `cd plugin/tests && python3 -m unittest test_playbook_evals`
## Non-goals
## Approach (options → choice → why)
Options: run real model A/B for every playbook on each change (costly); a static lint only (proves nothing); chosen: fm playbooks eval NAME runs a held-out brief set with and without the playbook through the fake-model harness by default and a real model when asked (budgeted by fm budget), recording the lift; ablation drops one section at a time; descriptions tuned against the reach set offline.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] held-out brief sets for the UI playbooks
3. [ ] eval runner and ablation
4. [ ] description tuning against the reach set
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:43Z created
- 2026-10-22T17:57:45Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/evals', 'plugin/tests/test_playbook_evals.py', 'CHANGELOG.md']
- 2026-10-22T20:59:19Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1522
## Follow-ups captured
