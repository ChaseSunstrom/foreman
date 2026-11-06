---
id: T-3270
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/ambient.py, plugin/lib/sampo/cli.py, plugin/tests/test_ambient.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:27:28Z
updated: 2026-11-06T03:46:19Z
builder: 2026-11-06T02:27:41Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a5ab088b88213fd1e
lane_branch: worktree-agent-a5ab088b88213fd1e
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:25Z
plan0_scope: [plugin/lib/sampo/ambient.py, plugin/lib/sampo/cli.py, plugin/tests/test_ambient.py, CHANGELOG.md]
builder_returned: 2026-11-06T03:46:19Z
---
# Moon C-000273: ambient affected-test pass is cached by working tree so the close's affected check reuses it
## Raw request
> Moon C-000273: ambient affected-test pass is cached by working tree so the close's affected check reuses it
## Interpretation
Reading 1 (chosen): ambient (T-0705, opt-in via sampo check ambient on) already runs the affected tests in the background after edits, but its result is only a flip note; the close (_close_affected, cli.py:1656) runs them again. Add a tree-keyed pass verdict that the close reuses. Reading 2 (ruled out): build a new background runner at idle priority, because ambient.after_edit already does the detached run with a host-strain skip; only the cache handoff is missing.
## Assumptions (confidence)
## Acceptance criteria
- [ ] ambient records a verdict keyed by the working-tree id, only when the tree did not change during the run — verify with `python3 plugin/tests/run.py test_ambient`
- [ ] _close_affected skips the rerun when a passing verdict for the same command and same tree exists, and still runs when the tree moved or the verdict was red — verify with `python3 plugin/tests/run.py test_ambient`
- [ ] the reuse is logged on the close (close_affected event, cached=true) so the audit trail shows it — verify with `python3 plugin/tests/run.py test_ambient`
## Non-goals
## Approach (options → choice → why)
1. ambient writes verdict.json {cmd, tree, exit} using core.worktree_tree before and after the run (stored only if equal); ambient.verdict(p, cmd) returns True when the current tree and cmd match a pass; _close_affected skips the run then. Likely outcome: close skips a minute-scale rerun, safe because the tree id covers every working file.
2. Use what exists: ambient._record/last.json and core.worktree_tree already hold the run result and tree id; extend them rather than a new store. Likely outcome: no new module, about 30 lines.
3. Key by the changed-file list plus mtimes. fails if: an edit restoring an earlier mtime or a reverted change is mistaken for the same tree.
4. Make the close wait on a running ambient run and read its result. fails if: the wait stalls a close behind a 600 s run and adds a lock to reason about.
5. Do less: log the ambient pass in the ledger only and leave the close alone. Likely outcome: no time saved, the moon is not delivered.

Choice 1 (86%): option 2's building blocks make option 1 small; only passes are reused so a flake or red still reruns at the close. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] failing tests first: verdict stored with tree; close reuses pass; moved tree and red verdict rerun
2. [x] ambient.py: tree id before and after the run, write verdict.json; ambient.verdict(p, cmd) returns a pass for the current tree
3. [x] cli._close_affected: consult ambient.verdict before running; log cached
4. [ ] CHANGELOG line  <- CURRENT
## Resume here
<!-- auto -->
- 2026-11-06T02:38:50Z step 3/4: cli._close_affected: consult ambient.verdict before running; log cached
- git: worktree-agent-a5ab088b88213fd1e; 3 uncommitted: plugin/lib/sampo/ambient.py, plugin/lib/sampo/cli.py, plugin/tests/test_ambient.py
- touched since last checkpoint: plugin/tests/test_ambient.py
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_ambient` → ✗ exit 1 · Ran 15 tests in 5.4s (15 jobs, 16 at a time; slowest: Ambient.test_a_full_check_waits_for_another_on_this_tree 5s, Ambient.test_a_full_check_waits_for_fm_ships_test_run_but_not_inside_it 5s, Ambient.t [ran] [tree a7be97a01417] [world 2f1906870a] (2026-11-06T02:31:00Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_ambient` → ✗ exit 1 · Ran 15 tests in 71.3s (15 jobs, 16 at a time; slowest: Ambient.test_a_close_reuses_the_ambient_pass_for_the_same_command_and_tree 63s, Ambient.test_a_close_reruns_after_a_red_ambient_run 52s, Ambient. [ran] [tree a4b2d6f52f0a] [world 2f1906870a] (2026-11-06T02:37:14Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_close_gates` → ✗ exit 1 · Ran 16 tests in 83.7s (16 jobs, 16 at a time; slowest: CloseGates.test_a_close_starts_a_full_run_when_the_last_one_is_old 67s, CloseGates.test_a_file_its_scope_log_names_is_committed_with_it 64s, Clos [ran] [tree a4b2d6f52f0a] [world 2f1906870a] (2026-11-06T02:38:48Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_ambient` → ✗ exit 1 · Ran 15 tests in 69.9s (15 jobs, 16 at a time; slowest: Ambient.test_a_close_reuses_the_ambient_pass_for_the_same_command_and_tree 55s, Ambient.test_a_close_reruns_when_the_tree_moved_since_the_pass 52 [ran] [tree a4b2d6f52f0a] [world 2f1906870a] (2026-11-06T02:47:52Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_ambient.Ambient.test_a_close_reuses_the_ambient_pass_for_the_same_command_and_tree test_ambient.Ambient.test_a_close_reruns_when_the_tree_moved_since_the_pass test_ambient.Ambient.test_a_close_reruns_after_a_red_ambient_run` → exit 0 · Ran 3 tests in 101.1s (3 jobs, 16 at a time; slowest: Ambient.test_a_close_reruns_after_a_red_ambient_run 86s, Ambient.test_a_close_reuses_the_ambient_pass_for_the_same_command_and_tree 74s, Ambient.t [ran] [tree a4b2d6f52f0a] [world 2f1906870a] (2026-11-06T02:49:45Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_ambient.Ambient.test_a_clean_ambient_run_records_a_pass_for_the_tree_it_ran_on test_ambient.Ambient.test_a_run_that_moves_the_tree_records_no_verdict` → exit 0 · Ran 2 tests in 91.3s (2 jobs, 16 at a time; slowest: Ambient.test_a_clean_ambient_run_records_a_pass_for_the_tree_it_ran_on 70s, Ambient.test_a_run_that_moves_the_tree_records_no_verdict 67s) / OK [ran] [tree a4b2d6f52f0a] [world 2f1906870a] (2026-11-06T02:51:43Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [135.18s] [ran] [tree a4b2d6f52f0a] [world 2f1906870a] (2026-11-06T02:57:05Z)
- (step 1) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_ambient.Ambient.test_a_run_an_edit_landed_in_writes_no_pass test_ambient.Ambient.test_a_pass_from_another_environment_is_not_reused test_ambient.Ambient.test_a_pass_older_than_the_cache_window_is_not_reused` → ✗ exit 1 · Ran 3 tests in 61.8s (3 jobs, 2 at a time; slowest: Ambient.test_a_pass_from_another_environment_is_not_reused 28s, Ambient.test_a_pass_older_than_the_cache_window_is_not_reused 25s, Ambient.test_a_ru [ran] [tree 4c7e4a92ed14] [world 2f1906870a] (2026-11-06T03:37:45Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_ambient.Ambient.test_a_clean_ambient_run_records_a_pass_for_the_tree_it_ran_on test_ambient.Ambient.test_a_run_that_moves_the_tree_records_no_verdict test_ambient.Ambient.test_a_run_an_edit_landed_in_writes_no_pass test_ambient.Ambient.test_a_pass_from_another_environment_is_not_reused test_ambient.Ambient.test_a_pass_older_than_the_cache_window_is_not_reused` → exit 0 · Ran 5 tests in 56.2s (5 jobs, 2 at a time; slowest: Ambient.test_a_clean_ambient_run_records_a_pass_for_the_tree_it_ran_on 27s, Ambient.test_a_run_that_moves_the_tree_records_no_verdict 18s, Ambient.t [ran] [tree 626370f034c7] [world 2f1906870a] (2026-11-06T03:41:48Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_ambient.Ambient.test_a_close_reuses_the_ambient_pass_for_the_same_command_and_tree test_ambient.Ambient.test_a_close_reruns_when_the_tree_moved_since_the_pass test_ambient.Ambient.test_a_close_reruns_after_a_red_ambient_run` → exit 0 · Ran 3 tests in 99.2s (3 jobs, 2 at a time; slowest: Ambient.test_a_close_reruns_after_a_red_ambient_run 50s, Ambient.test_a_close_reuses_the_ambient_pass_for_the_same_command_and_tree 45s, Ambient.tes [ran] [tree 626370f034c7] [world 2f1906870a] (2026-11-06T03:43:36Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [48.04s] [ran] [tree 626370f034c7] [world 2f1906870a] (2026-11-06T03:46:01Z)
## Log
- 2026-11-06T02:27:28Z created
- 2026-11-06T02:27:35Z set scope=['plugin/lib/sampo/ambient.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_ambient.py', 'CHANGELOG.md']
- 2026-11-06T02:27:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3270.builder.md
- 2026-11-06T02:28:24Z focused
- 2026-11-06T02:28:25Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3277 [FEATURE M, planned, 4 steps] Moon C-001115: rule keep/neutral/harmful on each edit's replay, at the edit
- T-2644 [PERFORMANCE M, done, 3 steps] fm task finish reuses a criterion's passing run when the same command already ran on this exact tree and world, instead of running …
- T-3273 [FEATURE M, planned, 4 steps] Moon C-001202 (partial): mutation-test any Sampo module: bench guard --mutate --module X --flip --func F flips comparisons/constants…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ambient.py, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
