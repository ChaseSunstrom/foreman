---
id: T-1405
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, plugin/lib/fmtidy.py, plugin/tests/test_crash_hygiene.py, plugin/tests/test_tidy.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-22T16:33:03Z
inferred_deps: [T-1382]
inferred_why: T-1382: named in its request
group: crash handling and durable run recovery
base: 93c28ce9c0b104178b226f8bf840ec60247a3819
base_tree: 86df29348895623dccfc6bbb4106c31168eb274c
plan0_at: 2026-10-22T15:41:36Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, plugin/tests/test_crash_hygiene.py, CHANGELOG.md]
verified: strong
---
# Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor
## Raw request
> FIX: Crash hygiene: faulthandler in long fm verbs, a stale .git/index.lock removed only when no live process owns the repo, and fm doctor probes the filesystem's lock semantics (S18, A28)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a hung verb writes a stack dump; index.lock is removed only with no live owner; doctor reports the filesystem probe
## Interpretation
Today's unclean shutdown showed the gaps: a hung long verb leaves no clue where it stuck; a crashed git leaves .git/index.lock and every later fm commit fails until someone deletes it; and if the state filesystem's flock doesn't exclude (NFS, some FUSE), every Foreman lock silently protects nothing.
## Assumptions (confidence)
## Acceptance criteria
- [x] a long verb writes a stack dump on SIGUSR1 and after its timeout — verify with `cd plugin/tests && python3 -m unittest test_crash_hygiene.StackDumps`
- [x] a stale index.lock with no live git is removed and logged; a fresh one or one with a live git in that repo is kept and named — verify with `cd plugin/tests && python3 -m unittest test_crash_hygiene.IndexLock`
- [x] fm doctor reports the state filesystem's lock probe — verify with `cd plugin/tests && python3 -m unittest test_crash_hygiene.LockProbe`
## Non-goals
## Approach (options → choice → why)
Options per part — (1) stack dumps: faulthandler on SIGUSR1 plus dump_traceback_later(15 min) for the long verbs (check, code, release, bench, sentinel), writing state/logs/stacks/<verb>-<pid>.txt; rejected: a watchdog thread per verb (more code). (2) index.lock: when a Foreman git call fails on an existing index.lock, remove it only if it is older than 10 min and no live process has that repo as cwd running git (scan /proc/*/comm+cwd on Linux; elsewhere never remove, just name it); rejected: always remove (races a live git). (3) doctor: fork a child that holds flock on a probe file under state/, then try LOCK_NB from the parent; PASS when it's refused, FAIL naming the filesystem when it isn't.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] faulthandler for long verbs
3. [x] stale index.lock removal
4. [x] doctor lock probe
## Resume here
<!-- auto -->
- 2026-10-22T15:48:05Z step 1/4: failing tests
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/t1380.edit
- failures met: stopped
## Docs impact
MASTER.md bullet; CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_crash_hygiene 2>&1 | tail -5` → ✗ exit 1 · FAILED (failures=4, errors=6) / fm: the output reports failing tests but the command exited 0 (a pipe such as | tail hides the exit), so it counts as a failure [ran] [tree a01e629aeacb] (2026-10-22T16:02:05Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_crash_hygiene.StackDumps` → exit 0 · Ran 4 tests in 6.159s / OK [ran] [tree 5241099776e0] (2026-10-22T16:06:11Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_crash_hygiene.IndexLock` → exit 0 · Ran 5 tests in 4.874s / OK [ran] [tree 5241099776e0] (2026-10-22T16:06:17Z)
- (step 4) `cd plugin/tests && python3 -m unittest test_crash_hygiene.LockProbe` → exit 0 · Ran 3 tests in 2.688s / OK [ran] [tree 5241099776e0] (2026-10-22T16:06:21Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_crash_hygiene.StackDumps` → exit 0 · Ran 4 tests in 7.586s / OK [ran] [tree 5241099776e0] (2026-10-22T16:06:40Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_crash_hygiene.IndexLock` → exit 0 · Ran 5 tests in 3.445s / OK [ran] [tree 5241099776e0] (2026-10-22T16:06:46Z)
- (ac 3) `cd plugin/tests && python3 -m unittest test_crash_hygiene.LockProbe` → exit 0 · Ran 3 tests in 2.542s / OK [ran] [tree 5241099776e0] (2026-10-22T16:06:50Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_crash_hygiene.StackDumps` → exit 0 · Ran 4 tests in 3.928s / OK [ran] [tree d0d4a6413073] (2026-10-22T16:09:32Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_crash_hygiene test_tidy.Apply.test_prunes_stack_dumps_older_than_two_weeks` → ✗ exit 1 · Ran 20 tests in 8.992s / FAILED (failures=6, errors=1) [ran] [tree 08f9b79f192c] (2026-10-22T16:20:26Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_crash_hygiene.StackDumps` → exit 0 · Ran 5 tests in 3.709s / OK [ran] [tree 3de5c8543cf4] (2026-10-22T16:23:00Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_crash_hygiene.IndexLock` → exit 0 · Ran 10 tests in 1.968s / OK [ran] [tree 3de5c8543cf4] (2026-10-22T16:23:02Z)
- (ac 3) `cd plugin/tests && python3 -m unittest test_crash_hygiene.LockProbe` → exit 0 · Ran 4 tests in 1.164s / OK [ran] [tree 3de5c8543cf4] (2026-10-22T16:23:04Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_tidy` → exit 0 · Ran 30 tests in 27.382s / OK [ran] [tree 3de5c8543cf4] (2026-10-22T16:23:32Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_crash_hygiene.StackDumps` → exit 0 · Ran 5 tests in 4.346s / OK [ran] [tree 9bec6882e811] (2026-10-22T16:27:18Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_crash_hygiene.IndexLock` → exit 0 · Ran 10 tests in 2.355s / OK [ran] [tree 9bec6882e811] (2026-10-22T16:27:22Z)
- (ac 3) `cd plugin/tests && python3 -m unittest test_crash_hygiene.LockProbe` → exit 0 · Ran 4 tests in 1.459s / OK [ran] [tree 9bec6882e811] (2026-10-22T16:27:24Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_crash_hygiene` → exit 0 · Ran 19 tests in 8.331s / OK [ran] [tree 9bec6882e811] (2026-10-22T16:27:33Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_crash_hygiene` → exit 0 · Ran 19 tests in 8.261s / OK [ran] [tree 9bec6882e811] (2026-10-22T16:27:42Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_crash_hygiene` → exit 0 · Ran 19 tests in 8.773s / OK [ran] [tree 9bec6882e811] (2026-10-22T16:27:52Z)
- (step 4) `cd plugin/tests && python3 -m unittest test_crash_hygiene` → exit 0 · Ran 19 tests in 8.275s / OK [ran] [tree 9bec6882e811] (2026-10-22T16:28:01Z)
- `cd plugin/tests && python3 -m unittest test_crash_hygiene` → ✗ exit 1 · Ran 19 tests in 48.093s / FAILED (failures=4, errors=13) (start tree + this task's tests) [ran] [tree 9bec6882e811] (2026-10-22T16:30:04Z)
- `cd plugin/tests && python3 -m unittest test_crash_hygiene` → exit 0 · Ran 19 tests in 7.616s / OK [ran] [tree 9bec6882e811] (2026-10-22T16:30:04Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_crash_hygiene.StackDumps` → exit 0 · Ran 5 tests in 5.558s / OK [ran] [tree c86dc5d08d54] (2026-10-22T16:30:33Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_crash_hygiene.IndexLock` → exit 0 · Ran 10 tests in 2.254s / OK [ran] [tree c86dc5d08d54] (2026-10-22T16:30:33Z)
- (ac 3) `cd plugin/tests && python3 -m unittest test_crash_hygiene.LockProbe` → exit 0 · Ran 4 tests in 1.484s / OK [ran] [tree c86dc5d08d54] (2026-10-22T16:30:33Z)
- (audit intent) `builder (high) test-first; red proved with fm task prove (17 of 19 fail on the start tree); fm-reviewer pass (research T-1405-review): 2 MEDIUM + 4 LOW fixed on the branch; one deviation decided (unreadable own processes block only when they're git: decisions.md); merged; test_crash_hygiene (19), test_tidy, test_doctor green.` → all three DONE-WHEN parts: a hung verb writes a stack dump; index.lock removed only with no live owner; doctor reports the lock probe [tree c86dc5d08d54] (2026-10-22T16:30:33Z)
- (audit adversary) `builder (high) test-first; red proved with fm task prove (17 of 19 fail on the start tree); fm-reviewer pass (research T-1405-review): 2 MEDIUM + 4 LOW fixed on the branch; one deviation decided (unreadable own processes block only when they're git: decisions.md); merged; test_crash_hygiene (19), test_tidy, test_doctor green.` → a lock is removed only when old, not open by any process (fd dev+ino scan), no git in the repo, and unchanged between check and removal; never without /proc [tree c86dc5d08d54] (2026-10-22T16:30:33Z)
- (audit edge) `builder (high) test-first; red proved with fm task prove (17 of 19 fail on the start tree); fm-reviewer pass (research T-1405-review): 2 MEDIUM + 4 LOW fixed on the branch; one deviation decided (unreadable own processes block only when they're git: decisions.md); merged; test_crash_hygiene (19), test_tidy, test_doctor green.` → hidepid=2 hides other users' processes (documented gap); stack dump files of dead pids pruned at start, old ones by tidy [tree c86dc5d08d54] (2026-10-22T16:30:33Z)
- (audit operator) `builder (high) test-first; red proved with fm task prove (17 of 19 fail on the start tree); fm-reviewer pass (research T-1405-review): 2 MEDIUM + 4 LOW fixed on the branch; one deviation decided (unreadable own processes block only when they're git: decisions.md); merged; test_crash_hygiene (19), test_tidy, test_doctor green.` → the doctor probe says what it proves (exclusion between processes on this host) [tree c86dc5d08d54] (2026-10-22T16:30:33Z)
- (audit maintainer) `builder (high) test-first; red proved with fm task prove (17 of 19 fail on the start tree); fm-reviewer pass (research T-1405-review): 2 MEDIUM + 4 LOW fixed on the branch; one deviation decided (unreadable own processes block only when they're git: decisions.md); merged; test_crash_hygiene (19), test_tidy, test_doctor green.` → _lock_holders, _stale_index_lock, _stack_dumps, check_lock_probe [tree c86dc5d08d54] (2026-10-22T16:30:33Z)
- (audit intent) `builder (high) test-first; red proved with fm task prove (17 of 19 fail on the start tree); fm-reviewer pass (research T-1405-review): 2 MEDIUM + 4 LOW fixed on the branch; one deviation decided (unreadable own processes block only when they're git: decisions.md); merged; test_crash_hygiene (19), test_tidy, test_doctor green.` → all three DONE-WHEN parts: a hung verb writes a stack dump; index.lock removed only with no live owner; doctor reports the lock probe [tree c86dc5d08d54] (2026-10-22T16:31:46Z)
- (audit adversary) `builder (high) test-first; red proved with fm task prove (17 of 19 fail on the start tree); fm-reviewer pass (research T-1405-review): 2 MEDIUM + 4 LOW fixed on the branch; one deviation decided (unreadable own processes block only when they're git: decisions.md); merged; test_crash_hygiene (19), test_tidy, test_doctor green.` → a lock is removed only when old, not open by any process (fd dev+ino scan), no git in the repo, and unchanged between check and removal; never without /proc [tree c86dc5d08d54] (2026-10-22T16:31:46Z)
- (audit edge) `builder (high) test-first; red proved with fm task prove (17 of 19 fail on the start tree); fm-reviewer pass (research T-1405-review): 2 MEDIUM + 4 LOW fixed on the branch; one deviation decided (unreadable own processes block only when they're git: decisions.md); merged; test_crash_hygiene (19), test_tidy, test_doctor green.` → hidepid=2 hides other users' processes (documented gap); stack dump files of dead pids pruned at start, old ones by tidy [tree c86dc5d08d54] (2026-10-22T16:31:46Z)
- (audit operator) `builder (high) test-first; red proved with fm task prove (17 of 19 fail on the start tree); fm-reviewer pass (research T-1405-review): 2 MEDIUM + 4 LOW fixed on the branch; one deviation decided (unreadable own processes block only when they're git: decisions.md); merged; test_crash_hygiene (19), test_tidy, test_doctor green.` → the doctor probe says what it proves (exclusion between processes on this host) [tree c86dc5d08d54] (2026-10-22T16:31:46Z)
- (audit maintainer) `builder (high) test-first; red proved with fm task prove (17 of 19 fail on the start tree); fm-reviewer pass (research T-1405-review): 2 MEDIUM + 4 LOW fixed on the branch; one deviation decided (unreadable own processes block only when they're git: decisions.md); merged; test_crash_hygiene (19), test_tidy, test_doctor green.` → _lock_holders, _stale_index_lock, _stack_dumps, check_lock_probe [tree c86dc5d08d54] (2026-10-22T16:31:46Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-22T15:40:34Z planned from capture
- 2026-10-22T15:41:35Z focused
- 2026-10-22T15:48:11Z paused: focus moved to T-1467
- 2026-10-22T15:58:49Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1405.builder.md
- 2026-10-22T15:59:04Z focused
- 2026-10-22T16:09:08Z scope: MASTER.md gets one Crash hygiene bullet documenting the new behaviour (docs impact)
- 2026-10-22T16:20:16Z steer: review nits 1-6 (T-1405-review); scope widened to fmtidy.py + test_tidy.py for the stacks prune
- 2026-10-22T16:26:58Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmtidy.py', 'plugin/tests/test_crash_hygiene.py', 'plugin/tests/test_tidy.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-22T16:27:08Z merged worktree-agent-a733ce8edfeaf3f6d (6 file(s))
- 2026-10-22T16:28:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a733ce8edfeaf3f6d
- 2026-10-22T16:29:00Z focused
- 2026-10-22T16:31:45Z scope: ANDON.md was the builder's uncommitted question in its worktree (answered by decision, then removed with the lane); never in the repo
- 2026-10-22T16:33:00Z done
- 2026-10-22T16:33:03Z committed 95646847 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1410 [FEATURE S, done, 2 steps] fm vetoes prints the command that retracts each veto, and that command removes exactly it — lesson: A record the user can create should…
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, plugin/lib/fmtidy.py, plugin/tests/test_crash_hygiene.py, plugin/tests/test_tidy.py; re-ground the plan against them before editing
## Why not caught
nothing handled a crashed git's index.lock or a hung verb; today's unclean shutdown showed both
## Lessons
- A safety rule written as 'unknown means unsafe' must be checked against the real host: here 31 of the user's own processes are unreadable, so it would have disabled the feature it guards.
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_crash_hygiene.py
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- MASTER.md
- ANDON.md
- plugin/tests/test_tidy.py
- plugin/lib/fmtidy.py
- CHANGELOG.md
