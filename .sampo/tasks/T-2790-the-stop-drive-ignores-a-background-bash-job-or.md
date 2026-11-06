---
id: T-2790
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-03T05:36:07Z
updated: 2026-11-03T20:59:38Z
rival_at: 2026-11-03T20:27:54Z
rival_split: true
builder_model: sonnet
base: 5872d04f2fac5d63aaa1e77365b71ed6b180d995
base_tree: f2da5f2502e13a2d0b971402bc857ebb09b22530
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-03T20:33:04Z
plan0_scope: []
lane_stop: merged 2026-11-03T20:56:41Z
verified: strong
---
# The Stop drive ignores a background Bash job or Monitor the main thread is waiting on (a…
## Raw request
> FIX: the Stop drive ignores a background Bash job or Monitor the main thread is waiting on (a queued close run behind a lane merge): with no agent listed it repeats 'fm focus T-2742' every turn, five blocks in a row on 2026-11-02, and focusing would race the close run's own fm focus calls. Count the session's running background shells and monitors as background work, as it counts agents
## Interpretation
The Stop drive counts background work from bg_start/bg_done events. Two kinds of background work never make bg_start: a foreground Bash call the harness moves to the background after its timeout (its tool_response says 'moved to the background (ID: X)', but run_in_background is false), and a Monitor (its response says 'Monitor started (task X'). Separately, with no active task, running jobs don't hold the drive by design (T-0415 comment), so it pushes 'fm focus <next>' on every Stop, racing a queued close script's own fm focus calls. Reading 2: make background work hold the drive even with no active task; ruled out because the design deliberately lets the next task start while jobs run, and a fresh session with an idle watch would never be pushed.
## Assumptions (confidence)
## Acceptance criteria
- [x] a Bash call the harness moved to the background after its timeout, and a Monitor, are recorded as background starts (bg_start) like run_in_background Bash, and their notifications end them — verify with `python3 plugin/tests/run.py test_hooks`
- [x] with no active task and a non-agent background job running, the Stop drive names the next task once per running set, not on every Stop (no repeated 'fm focus' while a queued close run is in flight) — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
1) Record bg_start in PostToolUse for a Bash call the harness moved to the background (response says 'moved to the background (ID: X)') and for a Monitor ('Monitor started (task X'); in the no-active branch, push the next task once per running set (remembered in drive state, as the active branch does with waited). Likely outcome: both gaps close on the existing event model. Fails if a Monitor's 30-min life holds the drive as a service (LONG_JOB_S drops it after 20 min).
2) Read running background work from the transcript each Stop. Likely outcome: same detection. Fails if the transcript is large (8 MB per Stop already) and starts are rewritten; _scan_notices already reads completions, starts are cheaper at PostToolUse.
3) Hold the drive whenever any job runs, active task or not. Likely outcome: no nagging. Fails if: it blocks starting the next task while a watch runs (the T-0415 design).
4) Do less: only record the two missing starts, leave the no-active branch. Likely outcome: active-task waits hold correctly. Fails if: the no-active repeat (the reported symptom) stays.

Choice 1 (80%): it fixes both the missing starts and the repeated push with the event model already in place; an unparseable tool_response records nothing, as today.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first: an auto-backgrounded Bash and a Monitor make bg_start; the no-active drive line repeats once per running set
2. [x] record them in PostToolUse; the no-active branch remembers the running set it already pushed for
## Resume here
## Docs impact
none: hook behaviour; no user-facing text changed
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → exit 0 · Ran 252 tests in 48.9s (31 classes, 16 at a time; slowest: Stop 48s, NoTaskGate 28s, PreToolUse 22s) / OK [ran] [tree bb83ded70870] [world 2f1906870a] (2026-11-03T20:34:28Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → exit 0 · Ran 252 tests in 48.9s (31 classes, 16 at a time; slowest: Stop 48s, NoTaskGate 28s, PreToolUse 22s) / OK [ran] [tree bb83ded70870] [world 2f1906870a] (2026-11-03T20:34:28Z)
- (step 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → exit 0 · Ran 252 tests in 48.9s (31 classes, 16 at a time; slowest: Stop 48s, NoTaskGate 28s, PreToolUse 22s) / OK [ran] [tree bb83ded70870] [world 2f1906870a] (2026-11-03T20:34:28Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks 2>&1 | grep -E "^(FAIL|ERROR)|FAILED|OK" | head` → ✗ exit 1 · FAILED (failures=2) / FAILED (1 classes: test_hooks.Stop) [ran] [tree 53fdceb9505a] [world 2f1906870a] (2026-11-03T20:36:15Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks 2>&1 | grep -E "^(FAIL|ERROR)|FAILED|OK" | head` → ✗ exit 1 · FAILED (failures=2) / FAILED (1 classes: test_hooks.Stop) [ran] [tree 53fdceb9505a] [world 2f1906870a] (2026-11-03T20:36:15Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 252 tests in 61.9s (31 classes, 16 at a time; slowest: Stop 62s, NoTaskGate 38s, PreToolUse 31s) / OK [ran] [tree bb83ded70870] [world 2f1906870a] (2026-11-03T20:39:11Z)
- (step 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 252 tests in 57.3s (31 classes, 16 at a time; slowest: Stop 57s, NoTaskGate 37s, PreToolUse 31s) / OK [ran] [tree bb83ded70870] [world 2f1906870a] (2026-11-03T20:40:09Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_hooks && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 404 tests in 59.5s (64 classes, 16 at a time; slowest: Stop 59s, NoTaskGate 39s, PreToolUse 33s) / FAILED (1 classes: test_core.SandboxEnv) [ran] [tree bb83ded70870] [world 2f1906870a] (2026-11-03T20:41:11Z)
- `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 252 tests in 47.6s (31 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 27s, PreToolUse 21s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree 98ce5aa793ab] [world 2f1906870a] (2026-11-03T20:58:26Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 252 tests in 47.2s (31 classes, 16 at a time; slowest: Stop 47s, NoTaskGate 27s, PreToolUse 21s) / OK [ran] [tree 98ce5aa793ab] [world 2f1906870a] (2026-11-03T20:58:26Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:58:26Z [ran] [tree 98ce5aa793ab] [world 2f1906870a] (2026-11-03T20:58:34Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T20:58:26Z [ran] [tree 98ce5aa793ab] [world 2f1906870a] (2026-11-03T20:58:34Z)
- (audit intent) `self: read the diff — PostToolUse records bg_start for 'moved to the background (ID: X)' and 'Monitor started (task X'; unparseable records nothing; _drive's no-active branch remembers the running set it pushed for and returns None for the same set` → the drive no longer repeats 'fm focus' every Stop while background work runs with no task active, and auto-backgrounded Bash and Monitors count as running work [tree 98ce5aa793ab] (2026-11-03T20:58:34Z)
- (audit edge) `self: read the diff — PostToolUse records bg_start for 'moved to the background (ID: X)' and 'Monitor started (task X'; unparseable records nothing; _drive's no-active branch remembers the running set it pushed for and returns None for the same set` → a set over five jobs that changes only in its tail doesn't re-push (same cap as the active branch); a Monitor past LONG_JOB_S is a service and stops holding [tree 98ce5aa793ab] (2026-11-03T20:58:34Z)
- (audit adversary) `self: read the diff — PostToolUse records bg_start for 'moved to the background (ID: X)' and 'Monitor started (task X'; unparseable records nothing; _drive's no-active branch remembers the running set it pushed for and returns None for the same set` → reads only the tool's own response text; no new exec, file or network; PostToolUse p95 37.4→39.9 ms, within noise [tree 98ce5aa793ab] (2026-11-03T20:58:34Z)
## Log
- 2026-11-03T05:36:07Z created
- 2026-11-03T05:37:00Z blocked: waits on the close run in flight: its fix changes the Stop drive the run is being observed with; plan after
- 2026-11-03T20:27:30Z criterion 1 verify: `python3 plugin/tests/run.py test_drive` → `python3 plugin/tests/run.py test_hooks`
- 2026-11-03T20:27:32Z set tier=M
- 2026-11-03T20:28:00Z rival read: considered; kept approach 1 (PostToolUse records starts; the transcript scan already ends them) and took its defensive point: an unparseable tool_response records nothing, as today
- 2026-11-03T20:32:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2790.builder.md
- 2026-11-03T20:33:02Z focused
- 2026-11-03T20:33:04Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-03T20:41:42Z builder done: branch worktree-agent-ac6a357e88baf1068 (1116ba83), test_hooks 252 OK, hook p95 PostToolUse 37.4→39.9 ms, Stop 54.1→55.8 ms; reviewed the diff; merge after ship7 so the ship's gates aren't run against a moving tree
- 2026-11-03T20:56:41Z merged worktree-agent-ac6a357e88baf1068 (2 file(s))
- 2026-11-03T20:56:48Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac6a357e88baf1068
- 2026-11-03T20:56:48Z focused
- 2026-11-03T20:59:38Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: in the Stop-hook drive logic (probably `plugin/lib/fmhooks.py`), the "is there background work?" check counts only agents (likely via `fmagents.py`). Extend it so running background Bash shells and Monitors from the session also count, which suppresses the `fm focus T-2742` re-prompt whi…
- The fix may belong in the drive decision itself (the function that picks "focus this task" as the block reason) rather than in the background-work counter. Then the change is a guard there, such as "if anything is pending, allow stop or stay quiet", rather than a wider count.
- It could mean the Stop hook should not block at all while waiting, and should instead emit a different message ("waiting on background job"). That changes the output contract, not just the count.
- Less likely: the repeat is a missing de-duplication or backoff, since five identical blocks in a row happened. The request names the cause (not counting shells/monitors), so this is a secondary concern.
Approaches:
- Find where agents are counted in the Stop drive (`fmhooks.py`, with helpers in `fmagents.py` or `fmcore.py`). Add a sibling source for running background shells and monitors and fold it into the same "background work" predicate, so every existing agent-gated branch inherits it.
- Read the session's background-task state the way agents are read. That is either the session transcript or a state file Claude Code writes for background shells and monitors. Filter to entries for this session whose status is still running, and ignore finished or killed ones.
- Make the new source defensive: if the transcript or state is missing or unparseable, treat it as zero background work. That keeps today's behaviour instead of making the hook fail.
- Extend `plugin/tests/test_agents.py` or the hooks test with a fixture that has a running shell or monitor and no agent, asserting the Stop drive does not emit `fm focus`. Add a finished-shell case asserting it still does.
Failure modes:
- The hook payload or transcript may not expose background shells or monitors in a stable, parseable form, so the counter reads the wrong field. It would then always return zero and the bug would look fixed in tests but remain in practice.
- Stale entries: a shell that was killed, crashed or exited but is still recorded as running would suppress the drive forever, leaving a stuck session that never gets refocused.
- Session scoping: counting shells from other sessions or from child sessions under `fm-children` would suppress the drive wrongly, or the reverse if the session id comparison is off.
- Hook latency: scanning a large transcript on every Stop event could slow the hook, which `plugin/tests/bench_hooks.py --runs 20` guards against.
## Dissent
- [x] rival reading: Likeliest: in the Stop-hook drive logic (probably `plugin/lib/fmhooks.py`), the "is there background work?" check counts only agents (likely via `fmagents.py`). Extend it so running background Bash shells and Monitors from the session also count, which suppresses the `fm focus T-2742` re-prompt whi… — answered: adopted: the starts of auto-backgrounded Bash and Monitors join bg_start, the same predicate agents and run_in_background Bash use
- [x] rival reading: The fix may belong in the drive decision itself (the function that picks "focus this task" as the block reason) rather than in the background-work counter. Then the change is a guard there, such as "if anything is pending, allow stop or stay quiet", rather than a wider count. — answered: adopted in part: the no-active branch pushes once per running set instead of on every Stop
- [x] rival reading: It could mean the Stop hook should not block at all while waiting, and should instead emit a different message ("waiting on background job"). That changes the output contract, not just the count. — answered: rejected: the active branch already waits silently with a waiting_on line; the output contract stays
- [x] rival reading: Less likely: the repeat is a missing de-duplication or backoff, since five identical blocks in a row happened. The request names the cause (not counting shells/monitors), so this is a secondary concern. — answered: adopted: the once-per-running-set memory is that de-duplication
- [x] rival approach: Find where agents are counted in the Stop drive (`fmhooks.py`, with helpers in `fmagents.py` or `fmcore.py`). Add a sibling source for running background shells and monitors and fold it into the same "background work" predicate, so every existing agent-gated branch inherits it. — answered: adopted: same predicate (_running), via the existing bg_start event
- [x] rival approach: Read the session's background-task state the way agents are read. That is either the session transcript or a state file Claude Code writes for background shells and monitors. Filter to entries for this session whose status is still running, and ignore finished or killed ones. — answered: rejected: the payload's background_tasks list is used when the build sends it; otherwise starts at PostToolUse plus _scan_notices' completions already model it
- [x] rival approach: Make the new source defensive: if the transcript or state is missing or unparseable, treat it as zero background work. That keeps today's behaviour instead of making the hook fail. — answered: adopted: an unparseable tool_response records nothing
- [x] rival approach: Extend `plugin/tests/test_agents.py` or the hooks test with a fixture that has a running shell or monitor and no agent, asserting the Stop drive does not emit `fm focus`. Add a finished-shell case asserting it still does. — answered: adopted: test_hooks cases for a running shell or monitor with no agent, and a finished one
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261009-091631.pack: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just sim…
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- research mission-20261009-091631: Request: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just…
- decision 2026-10-29: Keep the drive offering a new side task each Stop even when one was ignored
- the similar finished task took 3 steps
## Why not caught
the drive tests modelled background work only as run_in_background Bash and agents; no test fed the harness's timeout-move text or a Monitor response
## Lessons
- Background work has three starts (run_in_background, the harness's timeout move, Monitor): a detector keyed on one flag misses the other two
## Files touched
- plugin/lib/sampo/hooks.py
- plugin/tests/test_hooks.py
