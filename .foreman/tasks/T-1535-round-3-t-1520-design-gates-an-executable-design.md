---
id: T-1535
type: FEATURE
tier: L
status: dropped
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_design_gates.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:47Z
updated: 2026-10-22T20:59:27Z
---
# Round 3 (T-1520): Design gates: an executable design brief that fails the build, an access
## Raw request
> Round 3 (T-1520): Design gates: an executable design brief that fails the build, an accessibility and motion audit gate, a design-debt sweep, a 'because' line on every token, four checked layers, browser-support baselines, token fuzzing, a look fingerprint and a distance from the anti-reference, a signature motif check, a canary palette that exposes hard-coded colours, a dissonance pass, and a guard against a user's look repeating across projects (a039 a087 a131 a148 a180 a165 a175 b129 b147 b163 b015 c109 c096). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Design gates: an executable design brief that fails the build, an accessibility and motion audit gate, a design-debt sweep, a 'because' line on every token, four checked layers, browser-support baselines, token fuzzing, a look fingerprint and a distance from the anti-reference, a signature motif check, a canary palette that exposes hard-coded colours, a dissonance pass, and a guard against a user's look repeating across projects (a039 a087 a131 a148 a180 a165 a175 b129 b147 b163 b015 c109 c096). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [ ] each gate runs over a fixture project and reports pass/fail with a reason; a gate stays advisory until promoted — verify with `cd plugin/tests && python3 -m unittest test_design_gates`
## Non-goals
## Approach (options → choice → why)
Options: hard blocks everywhere; chosen: gates as fm design checks that a project opts into (advisory by default, blocking once its false-positive rate is measured): an executable brief, an a11y and motion audit, a design-debt sweep, token 'because' lines, layered checks, browser baselines, token fuzzing, a look fingerprint and distance from the anti-reference, a signature-motif check, a canary palette, a dissonance pass and a repeated-look guard across projects.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] brief contract, audit and debt sweep
3. [ ] tokens: because, fuzz, canary palette
4. [ ] fingerprint, anti-reference, motif, dissonance, repeat guard
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:43:47Z created
- 2026-10-22T17:58:25Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_gates.py', 'CHANGELOG.md']
- 2026-10-22T20:59:27Z dropped: split into M/S children (recon, grounded); the parts that wait went to the inbox as follow-ups naming T-1535
## Follow-ups captured
