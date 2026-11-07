---
id: T-3534
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-06T21:54:58Z
updated: 2026-11-07T00:48:26Z
group: guard refuses legitimate lane and task work
lane: ~/.claude/foreman.lanes/T-3534
lane_branch: foreman/T-3534
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T00:37:44Z
plan0_scope: []
---
# The brief guard's refusal (96+10 fires of brief:path-py/md today, 14 on worktree paths)…
## Raw request
> FIX: the brief guard's refusal (96+10 fires of brief:path-py/md today, 14 on worktree paths) always says 'no active task in this project, sampo task new' even when the path is in a builder or lane worktree (fmguard.py:304-307, hooks.py:2480): say which lane and task is expected and the focus command instead
## Interpretation
Reading 1 (chosen): a brief refusal for a path inside a lane folder (<main>.lanes/X or <main>/.claude/worktrees/X), from the lane's cwd or the main checkout's, names that lane, the task it belongs to (branch foreman/T-N, or a brief recording its path or branch) and the exact command cd <lane> && sampo focus <ID>; the main checkout's refusal keeps today's text. Reading 2 (ruled out): stop refusing lane edits altogether: the brief guard is the point, only its wording misleads.
## Assumptions (confidence)
## Acceptance criteria
- [ ] A brief refusal in a lane names the lane, its task and cd <lane> && sampo focus <ID>; the main checkout's text is unchanged — verify with `nice -n 10 python3 plugin/tests/run.py -k LaneAutoFocus -k NoTaskGate test_guard test_hooks`
## Non-goals
## Approach (options → choice → why)
1) use what exists: T-3519's _lane_focus already finds a lane's tasks (branch, brief lane/lane_branch); factor that lookup out and reuse it for the refusal text; likely outcome: small diff, one lookup. 2) text in fmguard with its own lane lookup; fails if: fmguard has no briefs (standalone module), so it can't name the task. 3) hooks replaces the whole reason string; fails if: it drops fmguard's appended hints (changelog, focus-late). 4) do less: append a lane line to today's text; fails if: the refusal still leads with 'sampo task new' in the main project, the misleading part. Choice 1 (85%): hooks finds the lane and its tasks with the shared helper and hands (lane, hint) to fmguard on ctx.lane; fmguard's brief branch words it, hints kept.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: lane refusal names lane, task and focus command (lane cwd and main cwd); main-checkout text unchanged
2. [x] Lane lookup helper in hooks shared with _lane_focus; ctx.lane worded by fmguard's brief branch
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py -k test_a_refusal_in_a_lane_names test_guard` → ✗ exit 1 · Ran 1 tests in 2.1s (1 jobs, 16 at a time; slowest: LaneAutoFocus 0s) / FAILED (1 classes: test_guard.LaneAutoFocus) [ran] [tree 44335a55e413] [world 2f1906870a] (2026-11-07T00:38:06Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py -k test_a_refusal_in_a_lane_names test_guard` → exit 0 · Ran 1 tests in 4.0s (1 jobs, 16 at a time; slowest: LaneAutoFocus 2s) / OK [ran] [tree 90e4985a7474] [world 2f1906870a] (2026-11-07T00:41:47Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py -k LaneAutoFocus -k NoTaskGate test_guard test_hooks` → exit 0 · Ran 37 tests in 36.5s (7 jobs, 16 at a time; slowest: NoTaskGateMulti 16s, NoTaskGateClose 14s, NoTaskGateQueue 10s) / OK [ran] [tree 4b5e1972da12] [world 2f1906870a] (2026-11-07T00:42:28Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py -k LaneAutoFocus -k NoTaskGate test_guard test_hooks` → exit 0 · Ran 38 tests in 11.1s (7 jobs, 16 at a time; slowest: NoTaskGateMulti 10s, NoTaskGateClose 6s, NoTaskGateKinds 5s) / OK [ran] [tree e8f63ac6a946] [world 2f1906870a] (2026-11-07T00:48:26Z)
## Log
- 2026-11-06T21:54:58Z created
- 2026-11-07T00:33:47Z planned: it has criteria and steps
- 2026-11-07T00:34:05Z criterion 1 verify: `nice -n 10 python3 plugin/tests/run.py test_guard.LaneAutoFocus test_hooks` → `nice -n 10 python3 plugin/tests/run.py -k LaneAutoFocus -k NoTaskGate test_guard test_hooks`
- 2026-11-07T00:37:24Z lane: ~/.claude/foreman.lanes/T-3534 on foreman/T-3534
- 2026-11-07T00:37:43Z focused
- 2026-11-07T00:37:44Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T00:48:14Z review: cd quotes the lane (shlex.quote); _lane_tasks is None unless the folder is a worktree's own top (plain folder or link: no lane, main checkout's text); _lane_focus hands its lookup back so the refusal reuses it; .. resolved in _lane_dir
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3519 [FIX M, done, 2 steps] Builders hit the brief guard 140 times today, 113 on files inside lane worktrees with no… — lesson: When a guard refuses something whose fi…
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 2–3 steps
