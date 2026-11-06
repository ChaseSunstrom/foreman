---
id: T-3258
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T00:37:18Z
updated: 2026-11-06T00:37:35Z
base: fd073c44daf9d432d1398e14e3f6f50953d0af6a
base_tree: 1395d0f856bc85c5cb17e6367024623b0efa3931
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T00:37:19Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# Cap Sampo's CPU at 50%: this session's scope (Claude, builders, tests, generators) limited to 8 of 16 CPUs now; a sampo verb that sets and keeps the cap for every session is part of T-3252
## Raw request
> Cap Sampo's CPU at 50%: this session's scope (Claude, builders, tests, generators) limited to 8 of 16 CPUs now; a sampo verb that sets and keeps the cap for every session is part of T-3252
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the session's cgroup has cpu.max 800000 100000 — verify with `cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/kitty-2696-0.scope/cpu.max`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] set CPUQuota=800% on the session's scope
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/kitty-2696-0.scope/cpu.max` → exit 0 · 800000 100000 [ran] [tree 1395d0f856bc] [world 2f1906870a] (2026-11-06T00:37:32Z)
- (ac 1) `cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/kitty-2696-0.scope/cpu.max` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T00:37:32Z [ran] [tree 1395d0f856bc] [world 2f1906870a] (2026-11-06T00:37:33Z)
- (audit edge) `self: one runtime property on the session's own scope; verified cpu.max reads 800000 100000` → runtime only (gone at reboot or a new terminal); the keeping version is T-3252's sampo cpu cap; Ollama, a system service, stays outside the cap [tree 1395d0f856bc] (2026-11-06T00:37:33Z)
- (audit intent) `self: one runtime property on the session's own scope; verified cpu.max reads 800000 100000` → the user asked to cap Sampo's CPU at about 50%: 8 of 16 CPUs [tree 1395d0f856bc] (2026-11-06T00:37:33Z)
- (audit self) `self: one runtime property on the session's own scope; verified cpu.max reads 800000 100000` → no findings [tree 1395d0f856bc] (2026-11-06T00:37:33Z)
## Log
- 2026-11-06T00:37:18Z created
- 2026-11-06T00:37:19Z focused
- 2026-11-06T00:37:19Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T00:37:22Z guard authorization added: system
- 2026-11-06T00:37:35Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3252 [PERFORMANCE L, planned, 7 steps] PERF: Sampo's work shouldn't eat the whole CPU, and should get faster. Measured…
- decision 2026-11-06: No new builder lanes until T-3252's slot pool lands
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-3177 [PERFORMANCE M, deferred, 3 steps] Test runs oversubscribe the machine: each run.py starts 16 workers regardless of load,…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- start here (files T-2746 touched): plugin/tests/test_migrate.py, plugin/lib/fmhomemove.py, plugin/lib/fmcli.py, MASTER.md
## Lessons
- A whole agent session sits in one systemd scope: a CPUQuota there caps Claude, every builder and every job it starts in one move
