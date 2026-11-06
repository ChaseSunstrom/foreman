---
id: T-3056
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T00:29:05Z
updated: 2026-11-06T03:52:35Z
---
# Rune's drift check counts a seed line as drifted only when a second cold read confirms it, and records each read's verdict
## Raw request
> Rune's drift cold read flags a different innocuous seed line on each rerun (gen-4: first 'the exam's train split decides…', fair; then 'Frontier digest … read, never cloned', which agrees with gen-0's NEVER): a single cold read is noisy; count a line as drifted only when two reads agree or a second read confirms it, and record each read's verdict
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm genesis drift N runs a second cold read only when the first names lines, and counts as drifted only the lines both reads name verbatim; a line one read names is listed as unconfirmed (advisory, not a failure); drift.md records each read's verdict; a clean first read costs one call as today — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests in test_genesis with a fake child: first read names A, second names B: verdict clean with A and B unconfirmed; both name A: drifted on A; a clean first read makes one call  <- CURRENT
2. [ ] the confirm read in rune.drift and both verdicts in drift.md
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T00:29:05Z created
- 2026-11-05T00:46:17Z recon: rune.py:2984 is one unseeded call; _named (rune.py:2988) only checks the quoted line exists; fix: reply 'DRIFT: <seed line> :: <gen-0 line it breaks>' and ignore hits whose gen-0 part isn't one of gen-0's MUST/NEVER lines
- 2026-11-05T02:57:17Z planned from capture
- 2026-11-05T02:57:18Z set approved=True
- 2026-11-05T02:57:18Z set scope=['plugin/lib/sampo/rune.py', 'plugin/tests/test_genesis.py', 'CHANGELOG.md']
- 2026-11-05T02:57:18Z blocked: planned and approved; waits for a builder slot
- 2026-11-06T03:52:35Z unblocked
## Follow-ups captured
