---
id: T-2933
type: FIX
tier: S
status: planned
priority: normal
scope: [plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-04T08:30:24Z
updated: 2026-11-06T03:53:24Z
trigger: did-not-hold
trigger_key: d9b7abe3c2d7a06d
group: hook bench gate
---
# fm doctor's hook SLO judges PreToolUse runs taken under 0.5 load per CPU, where the hooks' own speed shows, not runs up to 1.5 that measure the machine
## Raw request
> Fix did not hold: T-2798
> did-not-hold T-2798 e8e5d23829be
> (the failure fm doctor fail hook slo: pretooluse p0 0 ms over the last 0 runs > the 0 ms slo (bench_hooks' budget); over since 0.0.0… hit 2026-11-04 after T-2798 closed: read T-2798's evidence for what it missed and fix the cause, not the symptom)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] check_hook_slo counts only hook_ms runs with load under SLO_LOAD = 0.5 per CPU (measured 2026-11-05 over 7,420 runs: p95 103 ms under 0.25, 121 ms at 0.25-0.5, 174-269 ms at 0.5-1.5, against the 150 ms SLO), says how many it left out and why, and with fewer than 20 such runs reports 'not judged' as a pass; LOAD_BAR's other uses are unchanged — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: 200 runs at load 0.3 under budget and 200 at load 1.2 over it pass; 200 at load 0.3 over budget warn  <- CURRENT
2. [ ] SLO_LOAD in doctor.check_hook_slo
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T08:30:24Z created
- 2026-11-05T03:48:23Z planned from capture
- 2026-11-05T03:48:23Z set approved=True
- 2026-11-05T03:48:24Z set scope=['plugin/lib/sampo/doctor.py', 'plugin/tests/test_doctor.py', 'CHANGELOG.md']
- 2026-11-05T03:48:24Z blocked: approved; waits for a builder slot (or the main thread after T-3131 closes)
- 2026-11-06T03:53:24Z unblocked
## Follow-ups captured
