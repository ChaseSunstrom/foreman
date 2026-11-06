---
id: T-1176
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/tests/test_drive_side.py]
depends_on: []
source: discovered
created: 2026-10-16T12:14:46Z
updated: 2026-10-16T12:37:57Z
base: 42183320cbde03591b6de0255650b62bd1aae88d
base_tree: 12daab8ec8227863e66e6fce9759ec538e8814c6
plan0_at: 2026-10-16T12:21:21Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/tests/test_drive_side.py]
verified: strong
---
# Stop drive: (1) offers 'fm lane brief … launch the builder' for RESEARCH and release tasks
## Raw request
> Stop drive: (1) offers 'fm lane brief … launch the builder' for RESEARCH and release tasks, which a builder can't do (a brainstorm runs fm ideas; a release pushes); (2) doesn't count a running 'fm check --evidence ID' as that task in progress, so it alternates between two tasks that are both waiting on background work
## Interpretation
The Stop drive's side-task suggestion should only offer a builder lane for work a builder can do: not a RESEARCH task (a brainstorm runs fm ideas and grounding in the main thread) and not a release (title starting 'Release'); and a task whose gates are running in the background (fm check --evidence ID started and not finished) is in progress, so the drive neither offers it as a side task nor rotates away from it.
## Assumptions (confidence)
## Acceptance criteria
- [x] the drive never says 'fm lane brief' for a RESEARCH task or a release; a task with a live gate run (gates_running with a live pid) isn't offered as a side task; a stale marker (dead pid) is ignored — verify with `python3 plugin/tests/run.py test_drive_side`
## Non-goals
## Approach (options → choice → why)
Options: (a) _start_how returns the planning/grounding text for RESEARCH and release tasks; fm check --evidence ID writes meta gates_running {task, pid, at} on start and clears it at the end (stale when the pid is gone), and _side_task/the drive skip that task; (b) parse ps for 'fm check' (fragile); (c) only the RESEARCH/release fix. Choice: (a).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_drive_side.py): RESEARCH and release never get a lane line; a live gates_running task isn't offered; a dead pid marker is ignored
2. [x] _start_how and the side-task filter in fmhooks; the gates_running marker in fm check
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_drive_side` → exit 0 · Ran 2 tests in 2.8s (1 classes, 16 at a time; slowest: DriveSide 3s) / OK [ran] [tree 396ae1c06951] (2026-10-16T12:24:49Z)
- (ac 1) `python3 plugin/tests/run.py test_drive_side test_hooks` → exit 0 · Ran 159 tests in 47.5s (21 classes, 16 at a time; slowest: Stop 47s, PreToolUse 22s, SessionStart 15s) / OK [ran] [tree a4513a49c38f] (2026-10-16T12:32:37Z)
- `python3 plugin/tests/run.py test_drive_side` → ✗ exit 1 · Ran 2 tests in 9.9s (1 classes, 16 at a time; slowest: DriveSide 9s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree f036102e0455] (2026-10-16T12:33:05Z)
- `python3 plugin/tests/run.py test_drive_side` → exit 0 · Ran 2 tests in 9.8s (1 classes, 16 at a time; slowest: DriveSide 9s) / OK [ran] [tree f036102e0455] (2026-10-16T12:33:05Z)
- (ac 1) `python3 plugin/tests/run.py test_drive_side` → exit 0 · Ran 2 tests in 10.2s (1 classes, 16 at a time; slowest: DriveSide 10s) / OK [ran] [tree f036102e0455] (2026-10-16T12:33:16Z)
- (step 1) `python3 plugin/tests/run.py test_drive_side` → exit 0 · Ran 2 tests in 10.2s (1 classes, 16 at a time; slowest: DriveSide 10s) / OK [ran] [tree f036102e0455] (2026-10-16T12:33:16Z)
- (audit edge) `self: reviewed merged diff: _start_how gives grounding text for RESEARCH and releases; fm check --evidence writes gates_running {task, pid, at} and clears it after the gates; the drive skips a task whose marker pid is alive; a crash leaves a dead pid, read as stale` → one global marker slot: two concurrent gated checks overwrite each other (accepted); a reused pid reads live (only skips one offer) [tree f036102e0455] (2026-10-16T12:33:16Z)
- (audit self) `self: reviewed merged diff: _start_how gives grounding text for RESEARCH and releases; fm check --evidence writes gates_running {task, pid, at} and clears it after the gates; the drive skips a task whose marker pid is alive; a crash leaves a dead pid, read as stale` → no findings [tree f036102e0455] (2026-10-16T12:33:16Z)
- `python3 plugin/tests/run.py test_drive_side` → exit 0 · Ran 2 tests in 2.5s (1 classes, 16 at a time; slowest: DriveSide 2s) / OK [ran] [tree f036102e0455] (2026-10-16T12:36:39Z)
- (audit edge) `self: reviewed merged diff: _start_how gives grounding text for RESEARCH and releases; fm check --evidence writes gates_running {task, pid, at} and clears it after the gates; the drive skips a task whose marker pid is alive; a crash leaves a dead pid, read as stale` → one global marker slot: two concurrent gated checks overwrite each other (accepted); a reused pid reads live (only skips one offer) [tree f036102e0455] (2026-10-16T12:36:39Z)
- (audit self) `self: reviewed merged diff: _start_how gives grounding text for RESEARCH and releases; fm check --evidence writes gates_running {task, pid, at} and clears it after the gates; the drive skips a task whose marker pid is alive; a crash leaves a dead pid, read as stale` → no findings [tree f036102e0455] (2026-10-16T12:36:39Z)
## Log
- 2026-10-16T12:14:46Z created
- 2026-10-16T12:15:07Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_drive_side.py'], status=planned
- 2026-10-16T12:15:07Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1176.builder.md
- 2026-10-16T12:21:21Z focused
- 2026-10-16T12:31:45Z merged worktree-agent-a369a4b31256dae9f (3 file(s))
- 2026-10-16T12:31:48Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a369a4b31256dae9f
- 2026-10-16T12:31:49Z focused
- 2026-10-16T12:36:36Z scope: CHANGELOG.md line
- 2026-10-16T12:37:56Z done
- 2026-10-16T12:37:57Z committed 1301275e (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0775 [FIX S, done, 2 steps] One-off headless claude -p sessions answer their prompt and stop; they never drive the queue — lesson: a headless session Foreman didn't st…
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_hooks.py
## Files touched
- plugin/tests/test_drive_side.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcli.py
- CHANGELOG.md
