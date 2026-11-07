---
id: T-3595
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T03:35:12Z
updated: 2026-11-07T03:35:25Z
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-07T03:35:13Z
plan0_scope: []
verified: strong
unproven: [meaning, perf-typed]
---
# Lift this session's CPU ceiling again (user 2026-11-06 21:40: max out the CPU for now; 10% stays the goal of the efficiency work, not a cap)
## Raw request
> Lift this session's CPU ceiling again (user 2026-11-06 21:40: max out the CPU for now; 10% stays the goal of the efficiency work, not a cap)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the session scope's cpu.max is max — verify with `cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/kitty-2060537-0.scope/cpu.max`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] clear CPUQuota on the session scope
## Resume here
## Docs impact
none: a runtime setting, no files
## Verification evidence
- (step 1) `cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/kitty-2060537-0.scope/cpu.max` → exit 0 · max 100000 [ran] [tree 624d8cb4b78f] [world 2f1906870a] (2026-11-07T03:35:21Z)
- (ac 1) `cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/kitty-2060537-0.scope/cpu.max` → exit 0 · reused: the same command passed on this tree and world at 2026-11-07T03:35:21Z [ran] [tree 624d8cb4b78f] [world 2f1906870a] (2026-11-07T03:35:24Z)
- (audit intent) `cpu.max reads 'max 100000' on the session scope after clearing CPUQuota` → the user lifted the ceiling; 10% stays the target every efficiency change is measured against, not a cap [tree 624d8cb4b78f] (2026-11-07T03:35:24Z)
- (audit edge) `cpu.max reads 'max 100000' on the session scope after clearing CPUQuota` → runtime only; T-3592's sampo cpu cap verb will set or clear it from Sampo [tree 624d8cb4b78f] (2026-11-07T03:35:24Z)
- (audit self) `cpu.max reads 'max 100000' on the session scope after clearing CPUQuota` → no findings [tree 624d8cb4b78f] (2026-11-07T03:35:24Z)
## Log
- 2026-11-07T03:35:12Z created
- 2026-11-07T03:35:13Z focused
- 2026-11-07T03:35:13Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-07T03:35:15Z guard authorization added: system
- 2026-11-07T03:35:25Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3591 [PERFORMANCE S, done, 1 steps] Cap this session's CPU at 25% now (user 2026-11-06: max 10% target, PC unusable at 100%); lower toward 10% as the efficiency fixes …
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3592 [FEATURE M, active, 3 steps] PERFORMANCE target (user 2026-11-06): at most 10% of the machine's CPU across ~100…
- decision 2026-11-02: Recommendation: build T-2557 (a goal session's done claim checks each stated Done-when line and requirement against the tree, or names it missing), …
- similar finished tasks took 1–4 steps
## Measurements
session scope cpu.max: 400000 100000 → max (no limit)
## Lessons
- A ceiling the user didn't ask for slows the very pipeline that lands the fixes; measure and fix, cap only on request.
