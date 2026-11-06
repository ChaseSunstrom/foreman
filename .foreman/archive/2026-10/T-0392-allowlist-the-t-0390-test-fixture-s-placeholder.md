---
id: T-0392
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T02:13:55Z
updated: 2026-10-09T02:14:53Z
base: 5912e401df11a7f4dcb1c97ce74945e377dc19ea
base_tree: 1964906dbff84cae6431c3c9d42ae540ef7e1134
verified: strong
---
# Allowlist the T-0390 test fixture's placeholder secret line (committed in 5912e40 without the marker)
## Raw request
> Allowlist the T-0390 test fixture's placeholder secret line (committed in 5912e40 without the marker)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm secrets reports nothing in plugin/tests/test_hooks.py — verify with `fm secrets`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] add the pragma to the fixture line, commit
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm secrets` → exit 0 · No credentials found (the working tree and Claude config; --history adds git history). [ran] [tree 403072a7a6ad] (2026-10-09T02:14:05Z)
- (ac 1) `fm secrets` → exit 0 · No credentials found (the working tree and Claude config; --history adds git history). [ran] [tree 403072a7a6ad] (2026-10-09T02:14:52Z)
- (audit intent) `self: fm secrets clean; the fixture test still passes` → the placeholder line carries the allowlist marker; no real secret was ever committed (PUT-APPROVAL_SECRET-FROM-.env-HERE) [tree 403072a7a6ad] (2026-10-09T02:14:52Z)
- (audit self) `self: fm secrets clean; the fixture test still passes` → no findings [tree 403072a7a6ad] (2026-10-09T02:14:52Z)
## Log
- 2026-10-09T02:13:55Z created
- 2026-10-09T02:13:55Z focused
- 2026-10-09T02:14:52Z done
- 2026-10-09T02:14:53Z committed 05b98c2 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0132-review: Verdict: changes needed.** I could only read files, so I traced everything by reading the code and ran nothing. [stale: plugin/lib/fmcli.py, plug…
- T-0132 [SECURITY M, done, 5 steps] Credential audit (fm secrets) and task-tagged commits — lesson: A scanner that gates a commit must read exactly what the commit will t…
- playbook Test-Driven Development Workflow (skills/playbooks/references/verify/tdd-workflow.md)
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
- similar past tasks were M: consider --tier M
- the similar finished task took 5 steps
## Regression test
none: a comment marker on a test fixture; fm secrets is the check
## Lessons
- Never run a commit in parallel with the edit it depends on: a refused edit leaves the commit holding the old text
## Files touched
- plugin/tests/test_hooks.py
