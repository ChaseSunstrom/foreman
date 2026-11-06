---
id: T-1044
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmideas.py, plugin/lib/fmhooks.py, plugin/tests/test_reaper.py]
depends_on: []
source: followup
created: 2026-10-16T03:42:08Z
updated: 2026-10-16T05:08:13Z
base: a097503911df4069040b22563cf3ec5157d25c4d
base_tree: c1679e25ac4ff7b6448d1a15b0310db207d15232
verified: strong
---
# Process-group reaper and a startup orphan sweep for the claude -p helpers (ideas, second,
## Raw request
> Process-group reaper and a startup orphan sweep for the claude -p helpers (ideas, second, research, relate): kill the group on timeout, sweep leftovers at SessionStart (T-1029 C6)
## Interpretation
Every `claude -p` helper (ideas, second, research, relate) runs in its own process group. On timeout the whole group is killed, so no grandchild survives. At SessionStart, leftover helpers from dead runs are swept. The breaker half of C6 already exists (`plugin/tests/test_breaker.py`, `fmhooks.paused_hooks`). Rollback and soak are out of scope, per the catalogue row for C6.
## Assumptions (confidence)
## Acceptance criteria
- [x] A child that spawns a grandchild and sleeps is gone, with its grandchild, after the timeout — verify with `python3 plugin/tests/run.py test_reaper`
- [x] `sweep_orphans` kills a registered stale helper, leaves a reused pid and a fresh helper alone, and SessionStart survives a sweep error — verify with `python3 plugin/tests/run.py test_reaper test_relate`
## Non-goals
## Approach (options → choice → why)
(a) patch each caller; (b) one group-aware runner in fmideas plus a pid registry; (c) a systemd scope. Choose (b). All four helpers route through `fmideas.run_child` (fmideas.py:102, a plain `subprocess.run` with `timeout=`, which kills only the leader) and `run_children` (fmideas.py:121-149, `pr.kill()` only). fmsecond (fmsecond.py:54), fmrelate (fmrelate.py:202) and fmresearch (fmresearch.py:247) all go through them, so one fix covers all four. Changes in `plugin/lib/fmideas.py`: - Add `_popen(argv, **kw)` with `start_new_session=True`. It writes `state_dir/children/<pid>` holding the starttime from `/proc/<pid>/stat` and the time started. - Add `_reap(pr)` doing `os.killpg(pr.pid, SIGKILL)`, then `communicate()`, then removing the registry file. - `run_child` uses Popen + `communicate(timeout)`. `run_children` replaces `pr.kill()` with `_reap`. - Add `sweep_orphans(max_age=1800)`. It kills a group only if the pid's starttime matches the registry entry and `/proc/<pid>/cmdline` contains `--no-session-persistence`, which guards against pid reuse. It returns the count. - Call it from `fmhooks.session_start` in a try/except with `log_error`, skipped when `FOREMAN_NO_BACKGROUND` is set.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (new `test_reaper.py`, stub `claude` on PATH as in test_relate.py:34): the stub runs `sleep 300 & wait`. `run_child(timeout=1)` raises ValueError, and the sleep pid is dead (`os.kill(pid, 0)` fails). Registry entries with an old time and a matching cmdline are killed. A pid with a mismatched starttime is not.
2. [x] Implement the helpers in fmideas and move both runners onto them.
3. [x] Hook the sweep into `session_start`.
4. [x] Review fixes: reap every unfinished group on an interrupt, kill a dead leader's verified group, bound the reap's drain, log orphans_reaped
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_reaper` → ✗ exit 1 · Ran 8 tests in 12.6s (3 classes, 16 at a time; slowest: Timeout 12s, Sweep 0s, Hook 0s) / FAILED (3 classes) [ran] [tree 7f884d3ffbdd] (2026-10-16T04:33:01Z)
- (step 2) `python3 plugin/tests/run.py test_reaper.Timeout test_reaper.Sweep test_clean_helpers test_ideas` → ✗ exit 1 · Ran 33 tests in 7.9s (9 classes, 16 at a time; slowest: Ideas 8s, Failures 4s, Timeout 3s) / FAILED (1 classes) [ran] [tree 2a15fa5c0dd1] (2026-10-16T04:34:03Z)
- (step 2) `python3 plugin/tests/run.py test_reaper.Timeout test_reaper.Sweep test_clean_helpers test_ideas` → exit 0 · Ran 33 tests in 4.2s (9 classes, 16 at a time; slowest: Ideas 4s, Failures 3s, Timeout 2s) / OK [ran] [tree 35e2597f2f77] (2026-10-16T04:34:56Z)
- (step 3) `python3 plugin/tests/run.py test_reaper test_relate test_hooks` → exit 0 · Ran 181 tests in 43.1s (29 classes, 16 at a time; slowest: Stop 43s, PreToolUse 27s, SessionStart 23s) / OK [ran] [tree 58133d5d5f9b] (2026-10-16T04:36:04Z)
- (step 3) `python3 plugin/tests/run.py test_reaper test_relate` → exit 0 · Ran 27 tests in 8.6s (9 classes, 16 at a time; slowest: Review 8s, Child 4s, Due 2s) / OK [ran] [tree 58133d5d5f9b] (2026-10-16T04:37:25Z)
- (step 4) `python3 plugin/tests/run.py test_reaper` → ✗ exit 1 · Ran 12 tests in 33.0s (3 classes, 16 at a time; slowest: Timeout 33s, Sweep 1s, Hook 1s) / FAILED (3 classes) [ran] [tree c36a7c760986] (2026-10-16T04:51:15Z)
- (step 4) `python3 plugin/tests/run.py test_reaper test_relate test_clean_helpers test_ideas test_research test_second` → exit 0 · Ran 97 tests in 11.6s (32 classes, 16 at a time; slowest: Review 11s, Timeout 9s, Ideas 7s) / OK [ran] [tree 410637876bde] (2026-10-16T04:55:03Z)
- (step 3) `python3 plugin/tests/run.py test_reaper test_relate` → exit 0 · Ran 31 tests in 14.9s (9 classes, 16 at a time; slowest: Review 15s, Timeout 9s, Child 8s) / OK [ran] [tree 410637876bde] (2026-10-16T04:55:21Z)
- (ac 1) `python3 plugin/tests/run.py test_reaper` → exit 0 · Ran 12 tests in 9.2s (3 classes, 16 at a time; slowest: Timeout 9s, Sweep 1s, Hook 1s) / OK [ran] [tree 0d15b7dc5789] (2026-10-16T05:08:12Z)
- (ac 2) `python3 plugin/tests/run.py test_reaper test_relate` → exit 0 · Ran 31 tests in 11.2s (9 classes, 16 at a time; slowest: Review 11s, Timeout 9s, Child 6s) / OK [ran] [tree 0d15b7dc5789] (2026-10-16T05:08:12Z)
- (step 1) `python3 plugin/tests/run.py test_reaper test_relate test_ideas test_hooks` → exit 0 · Ran 206 tests in 50.0s (33 classes, 16 at a time; slowest: Stop 50s, PreToolUse 29s, SessionStart 24s) / OK [ran] [tree 0d15b7dc5789] (2026-10-16T05:08:12Z)
- (audit intent) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1044-review): 1 MEDIUM (^C left children running) + 3 LOW fixed by the builder test-first; merged --no-ff and criteria re-run here` → a timeout or ^C kills the helper's whole group; SessionStart sweeps leftovers [tree 0d15b7dc5789] (2026-10-16T05:08:12Z)
- (audit adversary) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1044-review): 1 MEDIUM (^C left children running) + 3 LOW fixed by the builder test-first; merged --no-ff and criteria re-run here` → a kill needs the leader's start time and the --no-session-persistence flag (pid reuse guarded); the registry is in Foreman's state, never synced [tree 0d15b7dc5789] (2026-10-16T05:08:12Z)
- (audit edge) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1044-review): 1 MEDIUM (^C left children running) + 3 LOW fixed by the builder test-first; merged --no-ff and criteria re-run here` → no /proc (nothing registered, sweep returns 0), a dead leader with a surviving member, a setsid'd grandchild holding the pipes (bounded drain) [tree 0d15b7dc5789] (2026-10-16T05:08:12Z)
- (audit operator) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1044-review): 1 MEDIUM (^C left children running) + 3 LOW fixed by the builder test-first; merged --no-ff and criteria re-run here` → orphans_reaped event with the count; SessionStart cost is a listdir when nothing is registered [tree 0d15b7dc5789] (2026-10-16T05:08:12Z)
- (audit maintainer) `builder lane, then fm-reviewer five-lens pass on its branch (research T-1044-review): 1 MEDIUM (^C left children running) + 3 LOW fixed by the builder test-first; merged --no-ff and criteria re-run here` → one _popen/_reap/sweep_orphans set in fmideas used by both runners [tree 0d15b7dc5789] (2026-10-16T05:08:12Z)
## Log
- 2026-10-16T03:42:08Z created
- 2026-10-16T04:22:35Z set scope=['plugin/lib/fmideas.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_reaper.py']
- 2026-10-16T04:22:35Z set tier=M
- 2026-10-16T04:23:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1044.builder.md
- 2026-10-16T04:23:33Z focused
- 2026-10-16T05:06:50Z merged worktree-agent-a8aa423fa1a4c452e (3 file(s))
- 2026-10-16T05:06:59Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8aa423fa1a4c452e
- 2026-10-16T05:07:00Z focused
- 2026-10-16T05:07:01Z scope: CHANGELOG.md (its line); the merge of foreman/build into the lane brought other tasks' committed files
- 2026-10-16T05:08:13Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave1-plan-a306a171bb6861f90: === T-1044
- research brainstorm-20261016-catalogue: Source: research/brainstorm-20261015-221834 (3 rounds + 3 deepening rounds, 6 lenses, run past the two earlier
- T-0776 [PERFORMANCE S, done, 2 steps] Foreman's claude -p children carry a hard --max-budget-usd — lesson: a pre-run estimate isn't a cap; pass the hard limit to the chi…
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_hooks.py, plugin/tests/test_ideas.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmhooks.py, plugin/lib/fmideas.py, plugin/tests/test_reaper.py; re-ground the plan against them before editing
## Lessons
- start_new_session protects children from the terminal's signals, so every exit path (BaseException) must reap them itself
## Plan gaps
- added late: Review fixes: reap every unfinished group on an interrupt, kill a dead leader's verified group, bound the reap's drain,…
- failed first: step 1 Failing tests (new `test_reaper.py`, stub `claude` on PATH as in test_relate.py:34): the stub runs …
- failed first: step 2 Implement the helpers in fmideas and move both runners onto them.
- failed first: step 4 Review fixes: reap every unfinished group on an interrupt, kill a dead leader's verified group, bou…
## Files touched
- plugin/tests/test_reaper.py
- plugin/lib/fmideas.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
