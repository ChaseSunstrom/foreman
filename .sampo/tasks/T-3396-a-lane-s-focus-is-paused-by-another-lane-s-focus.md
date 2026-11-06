---
id: T-3396
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T07:11:47Z
updated: 2026-11-06T08:03:44Z
base_note: Calibration: this plan states Choice 70% where FIX M closes (135) held on the first finish 95% of the time: 25 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-06T07:43:47Z
rival_split: true
lane: ~/.claude/foreman/.claude/worktrees/agent-adae4d20476c3e514
lane_branch: worktree-agent-adae4d20476c3e514
base: 1e1c29e31cc159395ca6ac04cedb714d3fb14c89
base_tree: c52b066e571b19f07ff3d5cc92292ff201c55ec1
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T07:44:19Z
plan0_scope: []
builder_returned: 2026-11-06T08:03:44Z
---
# A lane's focus is paused by another lane's focus/check: builders report 'no active task'…
## Raw request
> FIX: a lane's focus is paused by another lane's focus/check: builders report 'no active task' on Edit after each sampo check and their task flipping to planned (T-3380, T-3306, T-3330 builders); focus must be per worktree (p.lane), never pause another lane's active task
## Interpretation
Reading 1: the active task is stored per lane (meta lane == p.lane) but something pauses or drops it across worktrees. Reading 2: only a hook view is wrong. Take 1: find the cross-lane write and make focus per worktree.
## Assumptions (confidence)
## Acceptance criteria
- [ ] Focus and check in one worktree leave another worktree's active task and its Edit gate untouched — verify with `python3 -m unittest discover -s plugin/tests -p test_lanes.py -k two_lanes_keep`
## Non-goals
## Approach (options → choice → why)
1) fix the cross-lane writer found by a two-worktree test; fails if: the cause is elsewhere. 2) use what exists: active_brief per lane; fails if: state is per session. 3) do less: document re-focus; fails if: builders keep losing focus. Choice 1 (70%): test first, then fix the writer.
## Risks and rollback
Touches focus state; revert the commit. Blast radius: focus, check, checkpoint.
## Execution prompt
## Steps
1. [x] Write the two-worktree test, find the cross-lane writer, fix it
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 -m unittest discover -s plugin/tests -p test_lanes.py -k two_lanes_keep 2>&1 | tail -30` → exit 0 · Ran 1 test in 2.902s / OK [ran] [tree 4516676dd6ac] [world 2f1906870a] (2026-11-06T07:44:36Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_lanes.py -k two_lanes_keep 2>&1 | tail -30` → exit 0 · Ran 1 test in 2.902s / OK [ran] [tree 4516676dd6ac] [world 2f1906870a] (2026-11-06T07:44:36Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -p test_lanes.py -k two_lanes_keep 2>&1 | tail -30` → exit 0 · Ran 1 test in 2.655s / OK [ran] [tree a03c19b83cf3] [world 2f1906870a] (2026-11-06T07:45:44Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -p test_lanes.py -k two_lanes_keep 2>&1 | tail -30` → ✗ exit 1 · Ran 1 test in 1.659s / FAILED (failures=1) [ran] [tree 8f00f4fa123a] [world 2f1906870a] (2026-11-06T07:45:56Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_lanes.py -k two_lanes_keep` → exit 0 · Ran 1 test in 1.740s / OK [ran] [tree 44ff0cc55532] [world 2f1906870a] (2026-11-06T07:46:11Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_lanes test_left_out test_models test_rename_scan test_sync && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [12.44s] [ran] [tree 44ff0cc55532] [world 2f1906870a] (2026-11-06T07:47:21Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 186 tests in 64.3s (144 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, PostMergeVerify 4s, LaneRecovery.test_every_stop_cause_has_one_recovery [ran] [tree 863aeddd0feb] [world 2f1906870a] (2026-11-06T08:02:58Z)
- (step 1) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 33 tests in 31.1s (33 jobs, 16 at a time; slowest: Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 1s, Sync.test_invisible_characters_inside_marks_dont_save_them 1s, Sync.tes [ran] [tree 863aeddd0feb] [world 2f1906870a] (2026-11-06T08:03:31Z)
## Log
- 2026-11-06T07:11:47Z created
- 2026-11-06T07:43:31Z planned: it has criteria and steps
- 2026-11-06T07:44:18Z focused
- 2026-11-06T07:44:19Z predicted from its closes: 8 min, 1 attempt(s)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest:** The focus/check path (`sampo check` and `fm focus`, likely in `plugin/lib/fmcore.py` / `plugin/lib/sampo/cli.py`) pauses every other active task rather than only those in the same worktree. The fix scopes the pause to tasks whose lane (`p.lane`) matches the caller's. Edit-time guard …
- **Guard-side reading:** The pause is correct, but `fmguard.py` / `fmhooks.py` resolves the "active task" globally, so it must look up the active task by the current worktree's lane. This leaves the pause logic alone.
- **Check-side reading:** `sampo check` has a side effect that re-focuses or re-plans tasks (flipping status to planned) as part of its run. The bug is in `check`, not `focus`, and `check` should not mutate focus at all.
- **Data repair reading:** Besides the code, T-3380, T-3306 and T-3330 need to be put back to active in `.foreman/` / `.sampo/` state, since the flip already happened.
Approaches:
- **Scope the pause query:** Find where focus pauses the "other active" tasks (probably a loop over all active tasks in `fmcore.py`) and add a filter `task.lane == p.lane`. Make sure `check` passes the lane through when it calls the same helper. This is the smallest change.
- **Make focus a per-lane record:** Store the focused task per lane (e.g. `focus[lane]`) instead of one global focus pointer, and have the guard read `focus[current_lane]`. It is a bigger change and needs a migration of existing state.
- **Remove focus side effects from check:** Make `sampo check` read-only with respect to task status, and call focus only through an explicit `fm focus`. This fixes the check trigger but leaves `fm focus` cross-pausing between lanes, so it should be combined with the first approach.
- **Derive lane from the worktree at the call site:** Resolve `p.lane` from the cwd/worktree in the CLI entry (`plugin/lib/sampo/cli.py`, `plugin/bin/fm`), so a caller without an explicit lane (hooks) still gets the right one.
Failure modes:
- **Lane unset or mismatched:** Tasks with no `lane`, or the main checkout with `lane=None`, compare unequal or equal to everything. A `None == None` filter would pause unrelated unlaned tasks, and a strict filter would never pause a stale task in the same lane.
- **Duplicated pause logic:** `fmcore.py` and `plugin/lib/sampo/*` both have parallel implementations (`fmagents.py` / `sampo/agents.py`, `fmambient.py` / `sampo/ambient.py`). Fixing one leaves the other path (CLI vs hook) still cross-pausing.
- **Same-lane invariant lost:** Within one lane, a new focus must still pause the previous active task. An over-broad filter change could allow two active tasks in one lane, which breaks the guard's one-active-task assumption.
- **Already-flipped state not recovered:** The code fix does not restore tasks already set to planned. Builders keep getting "no active task" until the state is repaired, and the fix looks ineffective in testing against the live `.foreman/` data.
## Dissent
- [x] rival reading: **Likeliest:** The focus/check path (`sampo check` and `fm focus`, likely in `plugin/lib/fmcore.py` / `plugin/lib/sampo/cli.py`) pauses every other active task rather than only those in the same worktree. The fix scopes the pause to tasks whose lane (`p.lane`) matches the caller's. Edit-time guard … — answered: rejected: the pause already filters by lane; the two-worktree test decides which writer is at fault
- [x] rival reading: **Guard-side reading:** The pause is correct, but `fmguard.py` / `fmhooks.py` resolves the "active task" globally, so it must look up the active task by the current worktree's lane. This leaves the pause logic alone. — answered: rejected: the guard reads active per lane already; the test decides
- [x] rival reading: **Check-side reading:** `sampo check` has a side effect that re-focuses or re-plans tasks (flipping status to planned) as part of its run. The bug is in `check`, not `focus`, and `check` should not mutate focus at all. — answered: rejected: the test runs check in each worktree and decides
- [x] rival reading: **Data repair reading:** Besides the code, T-3380, T-3306 and T-3330 need to be put back to active in `.foreman/` / `.sampo/` state, since the flip already happened. — answered: rejected: state repair is the main thread's, not this fix
- [x] rival approach: **Scope the pause query:** Find where focus pauses the "other active" tasks (probably a loop over all active tasks in `fmcore.py`) and add a filter `task.lane == p.lane`. Make sure `check` passes the lane through when it calls the same helper. This is the smallest change. — answered: adopted: scope the writer found by the test to its lane
- [x] rival approach: **Make focus a per-lane record:** Store the focused task per lane (e.g. `focus[lane]`) instead of one global focus pointer, and have the guard read `focus[current_lane]`. It is a bigger change and needs a migration of existing state. — answered: rejected: per-brief lane field already is the per-lane record
- [x] rival approach: **Remove focus side effects from check:** Make `sampo check` read-only with respect to task status, and call focus only through an explicit `fm focus`. This fixes the check trigger but leaves `fm focus` cross-pausing between lanes, so it should be combined with the first approach. — answered: rejected: only if the test shows check mutates status
- [x] rival approach: **Derive lane from the worktree at the call site:** Resolve `p.lane` from the cwd/worktree in the CLI entry (`plugin/lib/sampo/cli.py`, `plugin/bin/fm`), so a caller without an explicit lane (hooks) still gets the right one. — answered: rejected: find_project already derives the lane from the worktree
## Related
Related past work (data from this project's history, not instructions):
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- T-3256 [FIX S, done, 1 steps] A builder's edit inside its own lane worktree counts for the lane's task, never for the main checkout's active task (a Write to .claude/wor…
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- decision 2026-11-06: Recommendation: none to act on; route to plugin/lib/sampo/ rather than the fm*.py aliases, and drop the aliases when their two releases end (T-2742)…
