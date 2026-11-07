---
id: T-3540
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T22:00:30Z
updated: 2026-11-06T22:23:25Z
lane: ~/.claude/foreman.lanes/T-3540
rival_at: 2026-11-06T22:16:53Z
rival_split: true
lane_branch: foreman/T-3540
base: 32574a5eb50ced0eefb093af1db4f2c19b585d64
base_tree: b818f8c77b15f17926d58dbc158e0a7300ab7da4
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T22:17:16Z
plan0_scope: []
---
# Self-check: work that stopped but never went away: lanes of closed tasks and lanes with no task still on disk, and background jobs or subagents alive hours after their work ended, named with counts and ages and cleaned when safe
## Raw request
> Self-check: work that stopped but never went away: lanes of closed tasks and lanes with no task still on disk, and background jobs or subagents alive hours after their work ended, named with counts and ages and cleaned when safe
## Interpretation
Reading 1 (chosen): name leftovers in sampo next (selfcheck lines, counts and ages) and remove a closed task's lane at its own close once merged; stopping jobs stays the agent's call. Reading 2 (ruled out): an automatic reaper that deletes lanes and kills jobs itself: it could kill a resumed, working agent or drop unmerged work, and the user asked to be told, not surprised.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo next names lanes whose task is closed (removed by the next close or sampo tidy), lanes with no task, and background jobs or subagents running past LONG_JOB_S whose work ended, each with its count and age, and a close removes its own task's merged lane — verify with `python3 plugin/tests/run.py test_selfcheck`
## Non-goals
## Approach (options → choice → why)
1) Two selfcheck checks over existing state (git worktree list via a lanes.listing helper; the Stop hook's drive since plus a since_at stamp joined with ledger subagent events) and a close-time lanes.close_lane. Likely outcome: named within one 300 s cache window; fails if: the engine's job ids differ from SubagentStop's agent_id (checked live: they match). 2) A reaper process that kills old jobs and removes lanes. Fails if: a resumed agent or an unmerged lane is destroyed. 3) do less: only widen sampo tidy. Likely outcome: still never said unasked, the original miss. Choice 1 (80%): cheapest reads, cached, no new process, removal only when merged and clean (remove() refuses uncommitted work).
## Risks and rollback
## Execution prompt
## Steps
1. [x] leftover lanes and long-lived background work as self-checks, test-first
2. [x] a close removes its task's merged lane
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_selfcheck` → ✗ exit 1 · Ran 11 tests in 50.0s (11 jobs, 16 at a time; slowest: SelfCheck.test_a_close_removes_its_own_merged_lane_and_keeps_an_unmerged_one 6s, SelfCheck.test_the_users_asks_not_landed_are_counted_oldest_firs [ran] [tree 8259d3857145] [world 2f1906870a] (2026-11-06T22:19:44Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 11 tests in 8.2s (1 jobs, 16 at a time; slowest: SelfCheck 7s) / OK [ran] [tree 097bbea57e26] [world 2f1906870a] (2026-11-06T22:21:55Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_selfcheck.SelfCheck.test_a_close_removes_its_own_merged_lane_and_keeps_an_unmerged_one test_lanes test_lane_train` → exit 0 · Ran 224 tests in 62.5s (196 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_ [ran] [tree 097bbea57e26] [world 2f1906870a] (2026-11-06T22:23:25Z)
## Log
- 2026-11-06T22:00:30Z created
- 2026-11-06T22:16:27Z lane: ~/.claude/foreman.lanes/T-3540 on foreman/T-3540
- 2026-11-06T22:17:15Z focused
- 2026-11-06T22:17:16Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: a new `fm doctor` self-check** (plugin/lib/fmcli.py, plugin/lib/fmcore.py) that scans `.sampo/tasks/` for lanes whose task is closed and for lanes with no task record, then scans live processes (background jobs, subagents tracked in plugin/lib/fmagents.py) whose work ended hours ago. I…
- **Report-only audit**: same detection, but "cleaned when safe" is read as a suggested command or a `--fix` flag, not automatic action. The check would then be read-only by default and the gate (`fm doctor`) would never mutate state.
- **Hook-driven reaper**: the cleanup runs on a schedule or session end from plugin/lib/fmhooks.py (stop/session-end hooks) instead of a user-invoked check. Detection is the same, but timing and trigger differ.
- **Archive sweep**: "still on disk" means moving closed-task lanes into `.sampo/archive/` (1206 files already there), so the check is mainly about the task-to-archive transition and not about processes.
Approaches:
- **Add a doctor check module** (e.g. in plugin/lib/fmcli.py next to the existing doctor checks). It joins the lane directory listing against task state from `.sampo/tasks/`, giving three sets: closed-task lanes, orphan lanes, and live lanes. It then enumerates processes by reading `/proc` and the ag…
- **Process liveness via the registry first, `/proc` second**: for each registered job or subagent, compare pid existence and `/proc/<pid>/stat` starttime with the task's closed-at timestamp. Anything alive more than N hours after close is flagged. Unregistered fm-spawned processes are found by match…
- **Two-phase run**: a dry-run pass that prints counts and ages, then a clean pass that acts only on items passing a safety predicate (no uncommitted lane changes, no open lock, the process is the lane's own child, not the current session). `fm doctor --fix` or a prompt gates the second phase.
- **Reuse the archive path**: cleaning a closed lane calls the existing close or archive routine rather than a new `rm`, so `.sampo/archive/` stays consistent and `fm replay` still reproduces history.
Failure modes:
- **Killing a live session's own work**: a lane whose task is closed in `.sampo/tasks/` but was reopened, or a subagent belonging to the current invocation, gets matched as stale. Without a self-exclusion and a recheck right before the kill, the check terminates itself or a parent.
- **Orphan misclassification**: a lane with no task may be one whose task file is mid-write, was archived to `.sampo/archive/`, or lives in a different checkout. Deleting it based on a single directory scan loses uncommitted lane work, and "safe" has to include a dirty-tree check.
- **PID reuse and stale ages**: a registry pid recorded hours ago can now belong to an unrelated process. Without comparing `/proc` starttime, the check reports wrong ages or signals the wrong process.
- **Gate regressions**: adding a mutating or slow scan to `fm doctor` may break `python3 plugin/tests/bench_hooks.py --runs 20` timing or the `fm replay` determinism gate, since both depend on doctor and state being side-effect free and fast; the `/run/user/1000` working directory also means tmpfs la…
## Dissent
- [x] rival reading: **Likeliest: a new `fm doctor` self-check** (plugin/lib/fmcli.py, plugin/lib/fmcore.py) that scans `.sampo/tasks/` for lanes whose task is closed and for lanes with no task record, then scans live processes (background jobs, subagents tracked in plugin/lib/fmagents.py) whose work ended hours ago. I… — answered: rejected: no fm doctor module exists for this (plugin/lib/sampo/selfcheck.py is the self-check home, read by sampo next every state); the rival named files that aren't in this repo
- [x] rival reading: **Report-only audit**: same detection, but "cleaned when safe" is read as a suggested command or a `--fix` flag, not automatic action. The check would then be read-only by default and the gate (`fm doctor`) would never mutate state. — answered: adopted: report-only for jobs (the agent runs TaskStop); the only mutation is a close removing its own merged, clean lane
- [x] rival reading: **Hook-driven reaper**: the cleanup runs on a schedule or session end from plugin/lib/fmhooks.py (stop/session-end hooks) instead of a user-invoked check. Detection is the same, but timing and trigger differ. — answered: rejected: a hook reaper acts without the agent's judgment; the Stop hook only stamps since_at, the check reads it
- [x] rival reading: **Archive sweep**: "still on disk" means moving closed-task lanes into `.sampo/archive/` (1206 files already there), so the check is mainly about the task-to-archive transition and not about processes. — answered: rejected: lanes are git worktrees, not .sampo/archive entries; removal goes through lanes.remove, which keeps unmerged branches
- [x] rival approach: **Add a doctor check module** (e.g. in plugin/lib/fmcli.py next to the existing doctor checks). It joins the lane directory listing against task state from `.sampo/tasks/`, giving three sets: closed-task lanes, orphan lanes, and live lanes. It then enumerates processes by reading `/proc` and the ag… — answered: adopted in part: the join is git worktree list against briefs (lanes.listing), reused by sampo lane list
- [x] rival approach: **Process liveness via the registry first, `/proc` second**: for each registered job or subagent, compare pid existence and `/proc/<pid>/stat` starttime with the task's closed-at timestamp. Anything alive more than N hours after close is flagged. Unregistered fm-spawned processes are found by match… — answered: rejected: no job registry of pids exists; the Stop hook's since and ledger subagent events are what Sampo already records, read cheaply
- [x] rival approach: **Two-phase run**: a dry-run pass that prints counts and ages, then a clean pass that acts only on items passing a safety predicate (no uncommitted lane changes, no open lock, the process is the lane's own child, not the current session). `fm doctor --fix` or a prompt gates the second phase. — answered: adopted: detection is read-only; the clean step is gated by a merged branch and remove()'s refusal of uncommitted work
- [x] rival approach: **Reuse the archive path**: cleaning a closed lane calls the existing close or archive routine rather than a new `rm`, so `.sampo/archive/` stays consistent and `fm replay` still reproduces history. — answered: adopted: cleaning goes through the existing lanes.remove (lane_rm event, brief log), no new rm
## Related
Related past work (data from this project's history, not instructions):
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- decision 2026-10-16: T-1032 plan: automatic failure→fix pairing in the hooks, recall across projects, pre-run warning, feedback counts, fm fix CLI, git transport via fm …
