---
id: T-3548
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:21:45Z
updated: 2026-11-07T00:51:46Z
lane: ~/.claude/foreman.lanes/T-3548
lane_branch: foreman/T-3548
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T00:37:36Z
plan0_scope: []
---
# A close's reuse of the train's pass (T-3526) never hit: the working tree's code tree…
## Raw request
> FIX: a close's reuse of the train's pass (T-3526) never hit: the working tree's code tree includes untracked files (worktree_tree), and an untracked scripts/ folder sat in the main checkout all day, so every close since reran its linked tests (78-309 s each); a self-check names untracked non-ignored files in the main checkout, and the close's reuse says why it missed (which file differs) instead of silently rerunning
## Interpretation
Reading 1 (chosen): name what breaks the code-tree match (untracked non-ignored files in the main checkout) in a self-check, and make a close's missed reuse say why in one line (files differing from the newest pass, no pass, failed, other gates/env, modules not run). Reading 2 (ruled out): stop counting untracked files in the code tree at all; that changes what every gate pass and snapshot means, and an untracked file a test imports must still invalidate a pass.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the self-check names untracked non-ignored files (grouped, capped) with how to clear them, quiet when none — verify with `nice -n 10 python3 plugin/tests/run.py test_selfcheck`
- [ ] a close whose reuse misses says why in one line: the differing file(s), or no pass — verify with `nice -n 10 python3 plugin/tests/run.py test_close_affected`
## Non-goals
## Approach (options → choice → why)
1) use what exists: _cached_pass already decides every miss; give it an optional why list it appends to at each return None, the code-tree miss naming the files via one git diff --name-only of the recorded and current code trees; the self-check is one git ls-files -o --exclude-standard call with worktree_tree's mirror excludes. Likely outcome: one line per miss, no duplicated logic. 2) a separate _miss_reason re-deriving _cached_pass's conditions; fails if: the two drift and the reason lies. 3) do less: only the self-check, no miss reason; fails if: another tree drift (a stray build file, an edit) again reruns silently for hours. 4) drop untracked files from worktree_tree; fails if: an untracked module a test imports no longer invalidates a pass. Choice 1 (85%): the one function that decides the miss names it; both halves are one git call each.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: the untracked self-check and the close's miss reason
2. [x] selfcheck.untracked, CHECKS += on its own line
3. [x] _cached_pass/_full_pass/_gates_cover name the miss; finish and the linked tests print it
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_selfcheck test_close_affected` → ✗ exit 1 · Ran 13 tests in 6.3s (2 jobs, 16 at a time; slowest: CloseAffectedReuse 5s, SelfCheck 1s) / FAILED (2 classes: test_selfcheck.SelfCheck, test_close_affected.CloseAffectedReuse) [ran] [tree 80eca3d370a0] [world 2f1906870a] (2026-11-07T00:38:05Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_selfcheck test_close_affected` → exit 0 · Ran 13 tests in 69.6s (13 jobs, 16 at a time; slowest: CloseAffectedReuse.test_a_missed_reuse_names_the_files_that_differ 3s, CloseAffectedReuse.test_a_green_full_pass_on_the_same_tree_covers_the_link [ran] [tree 44b39bb7a796] [world 2f1906870a] (2026-11-07T00:43:58Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 8 tests in 2.3s (1 jobs, 16 at a time; slowest: SelfCheck 2s) / OK [ran] [tree 44b39bb7a796] [world 2f1906870a] (2026-11-07T00:44:24Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 8 tests in 4.6s (1 jobs, 16 at a time; slowest: SelfCheck 3s) / OK [ran] [tree de7087897033] [world 2f1906870a] (2026-11-07T00:44:53Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_close_affected test_round_f test_verify_strength test_finish_reuse test_lane_train` → exit 0 · Ran 74 tests in 69.3s (72 jobs, 16 at a time; slowest: Train.test_probes_run_three_at_once_and_leave_out_what_a_serial_run_does 11s, FinishReuse 5s, VerifyStrength.test_a_timed_out_check_kills_its_who [ran] [tree 201869fd6922] [world 2f1906870a] (2026-11-07T00:46:03Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 8 tests in 17.7s (1 jobs, 16 at a time; slowest: SelfCheck 5s) / OK [ran] [tree 201869fd6922] [world 2f1906870a] (2026-11-07T00:46:33Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 8 tests in 31.9s (1 jobs, 16 at a time; slowest: SelfCheck 4s) / OK [ran] [tree 71b4176a19e2] [world 2f1906870a] (2026-11-07T00:51:46Z)
## Log
- 2026-11-07T00:21:45Z created
- 2026-11-07T00:32:14Z planned: it has criteria and steps
- 2026-11-07T00:37:19Z lane: ~/.claude/foreman.lanes/T-3548 on foreman/T-3548
- 2026-11-07T00:37:34Z focused
- 2026-11-07T00:37:36Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2807 [CLEAN M, done, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5) — lesson: Merge overlapping renames by…
- decision 2026-10-31: [costly] Cold read clarification: a line that reports a requirement as unmet, open or unproven doesn't break it; the reader fails only what a line c…
