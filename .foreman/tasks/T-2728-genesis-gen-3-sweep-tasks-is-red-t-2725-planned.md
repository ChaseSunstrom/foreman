---
id: T-2728
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-03T00:04:04Z
updated: 2026-11-03T00:17:13Z
genesis_sweep: 3:tasks
base: 1949f2acfcd8bd63990ee4495a41dfa71d04883e
base_tree: 9348380af51e2410252b973cca2452d1dc2fe253
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-03T00:07:07Z
plan0_scope: []
verified: ok
unproven: [meaning]
---
# Genesis gen-3 sweep: tasks is red — T-2725 planned; T-2727 planned
## Raw request
> fm genesis sweep 3: ✗ tasks: T-2725 planned; T-2727 planned
> Done when the rerun's tasks line is ✓.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the sweep's tasks line is ✓ — verify with `grep -q '^Verdict: clean' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fix what the sweep's tasks line names, then rerun fm genesis sweep 3
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `grep -q '^Verdict: clean' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md` → exit 0 · (no output) [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:17:09Z)
- (step 1) `grep -q '^Verdict: clean' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md` → exit 0 · (no output) [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:17:10Z)
- (ac 1) `grep -q '^Verdict: clean' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:17:10Z [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:17:11Z)
- (audit self) `the tasks row listed T-2725 and T-2727 only because they were open; both closed with their rows green, and the rerun sweep reads Verdict: clean` → no findings [tree 9348380af51e] (2026-11-03T00:17:11Z)
## Log
- 2026-11-03T00:04:04Z created
- 2026-11-03T00:07:07Z focused
- 2026-11-03T00:07:07Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-03T00:17:09Z criterion 1 verify: `fm genesis sweep 3` → `grep -q '^Verdict: clean' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md`
- 2026-11-03T00:17:13Z done
## Follow-ups captured
## Regression test
none: the sweep's own rows are the check
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2604 [FIX S, dropped, 1 steps] Genesis gen-2 sweep: tasks is red — T-2601 planned
- T-2113 [FEATURE M, done, 3 steps] fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals… — lesson: A seal file beside the file it seals …
- decision 2026-10-30: Genesis sweep counts briefs (planned/active/verifying/blocked), not captured inbox items, as the tasks gen-0 §7 means; the active task running the s…
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–5 steps
