---
id: T-2730
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T00:18:56Z
updated: 2026-11-03T00:25:55Z
base: 1949f2acfcd8bd63990ee4495a41dfa71d04883e
base_tree: 9348380af51e2410252b973cca2452d1dc2fe253
plan0_at: 2026-11-03T00:18:57Z
plan0_scope: []
paused_tree: 9348380af51e2410252b973cca2452d1dc2fe253
verified: ok
unproven: [meaning]
---
# Ship 3 commit(s) to main
## Raw request
> Ship 3 commit(s) to main
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] main has them — verify with `fm ship --check 33a6416b 7b8a5a80 1949f2ac`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm ship --check 33a6416b 7b8a5a80 1949f2ac` → exit 0 · origin main has the changes of 33a6416b, 7b8a5a80, 1949f2ac [ran] [tree 58493f86759d] [world 2f1906870a] (2026-11-03T00:25:52Z)
- (ac 1) `fm ship --check 33a6416b 7b8a5a80 1949f2ac` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:25:52Z [ran] [tree 58493f86759d] [world 2f1906870a] (2026-11-03T00:25:53Z)
- (audit self) `fm ship ran the full suite and pushed T-2724, T-2727 and T-2725 to origin main at f801b869; T-2731 landed during the run and waits for the next ship` → no findings [tree 58493f86759d] (2026-11-03T00:25:53Z)
## Log
- 2026-11-03T00:18:56Z created
- 2026-11-03T00:18:56Z focused
- 2026-11-03T00:19:00Z guard authorization added: publish
- 2026-11-03T00:20:13Z paused: focus moved to T-2731
- 2026-11-03T00:25:40Z publish grant used by fm ship
- 2026-11-03T00:25:51Z criterion 1 verify: `fm ship --check` → `fm ship --check 33a6416b 7b8a5a80 1949f2ac`
- 2026-11-03T00:25:55Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2685 [CLEAN S, done, 1 steps] Ship 9 commits to main (Mission 7 briefs, T-2676)
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- decision 2026-11-02: [costly] Release 1.2.51: its push step conflicted because fm ship cherry-picks left foreman/build and main with diverged histories (merge base 2026-…
- similar finished tasks took 1–2 steps
