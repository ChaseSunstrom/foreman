---
id: T-3591
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T03:29:21Z
updated: 2026-11-07T03:30:15Z
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-07T03:29:31Z
plan0_scope: []
verified: strong
unproven: [meaning, perf-typed]
---
# Cap this session's CPU at 25% now (user 2026-11-06: max 10% target, PC unusable at 100%); lower toward 10% as the efficiency fixes land
## Raw request
> Cap this session's CPU at 25% now (user 2026-11-06: max 10% target, PC unusable at 100%); lower toward 10% as the efficiency fixes land
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the session scope's cpu.max is 400000 100000 — verify with `cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/kitty-2060537-0.scope/cpu.max`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] set CPUQuota=400% on the session scope and measure its use
## Resume here
## Docs impact
none: a runtime setting on this session's systemd scope, no files
## Verification evidence
- (step 1) `cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/kitty-2060537-0.scope/cpu.max` → exit 0 · 400000 100000 [ran] [tree 624d8cb4b78f] [world 2f1906870a] (2026-11-07T03:29:44Z)
- (ac 1) `cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/kitty-2060537-0.scope/cpu.max` → exit 0 · reused: the same command passed on this tree and world at 2026-11-07T03:29:44Z [ran] [tree 624d8cb4b78f] [world 2f1906870a] (2026-11-07T03:30:12Z)
- (audit edge) `cpu.max read back as 400000 100000 on the session scope; the scope's own cpu.stat measured 399% of one core (24% of the machine) over 10 s right after, down from 1179% (73%)` → runtime only (--runtime), so a reboot or a new session starts uncapped; ollama runs as a system service outside this scope and is not capped by it [tree 624d8cb4b78f] (2026-11-07T03:30:12Z)
- (audit intent) `cpu.max read back as 400000 100000 on the session scope; the scope's own cpu.stat measured 399% of one core (24% of the machine) over 10 s right after, down from 1179% (73%)` → an interim ceiling so the PC stays usable while the efficiency work brings real use under the user's 10% target; lowered as fixes land [tree 624d8cb4b78f] (2026-11-07T03:30:12Z)
- (audit self) `cpu.max read back as 400000 100000 on the session scope; the scope's own cpu.stat measured 399% of one core (24% of the machine) over 10 s right after, down from 1179% (73%)` → no findings [tree 624d8cb4b78f] (2026-11-07T03:30:12Z)
## Log
- 2026-11-07T03:29:21Z created
- 2026-11-07T03:29:29Z focused
- 2026-11-07T03:29:31Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-07T03:29:34Z guard authorization added: system
- 2026-11-07T03:30:15Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3258 [FEATURE S, done, 1 steps] Cap Sampo's CPU at 50%: this session's scope (Claude, builders, tests, generators) limited to 8 of 16 CPUs now; a sampo verb that sets …
- T-3294 [FEATURE M, active, 2 steps] Batch spawn, headless: sampo run --parallel N is a rolling pool up to lane max, not batches of 3 with fully disjoint scopes
- decision 2026-11-06: No new builder lanes until T-3252's slot pool lands
- similar finished tasks took 1–4 steps
## Measurements
session scope CPU: 1179% → 399% of one core (73% → 24% of 16 cores), cgroup cpu.stat usage_usec over 10 s
## Lessons
- Measure a session's CPU from its cgroup's cpu.stat, not by sampling processes: short-lived test and hook processes all count there.
