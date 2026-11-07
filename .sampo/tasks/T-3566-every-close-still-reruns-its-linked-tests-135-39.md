---
id: T-3566
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T01:06:26Z
updated: 2026-11-07T04:15:35Z
lane: ~/.claude/foreman.lanes/T-3566
lane_branch: foreman/T-3566
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T02:45:30Z
plan0_scope: []
---
# Every close still reruns its linked tests (135-399 s each; T-3082 211 s, T-3321 399 s,…
## Raw request
> PERFORMANCE: every close still reruns its linked tests (135-399 s each; T-3082 211 s, T-3321 399 s, T-3484 135 s on 2026-11-06 evening) although the train's gate passed the same code: _cached_pass reads only the newest check_run, and since T-3544 a train's pass is affected-only, so it holds for a close only when the close's linked modules are a subset of the train's affected list; and the per-close background full gates add newer check_runs. Measure with T-3548's miss reason once it lands, then make the close's linked set and the train's affected set agree (or look past newer non-matching runs)
## Interpretation
Reading 1 (chosen): a close after a green train must reuse the train's pass; the misses come from the close selecting tests differently from the train. Ledger 2026-11-07: batch 2 (train 02:10, 181 affected modules) reused 0/6 closes (459 s rerun): every close cmd carried the .tsx runner part (cd mods/foreman-ui && claude plugin test .), which _gates_cover can't parse, and its linked set held tests linked only to the .sampo/ mirror folder (test_fixes, …) because mirror .md files other closes committed count as changed; in batch 1 a lane's sentinel check_run on another code tree (00:23) hid the train's full pass. Reading 2 (ruled out): make the train run every close's full linked set: it would grow the blocking train gate back toward the full suite T-3544 removed.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a close whose linked tests include another runner's (.tsx) test and mirror .md changes reuses a train's affected-only pass on its code tree — verify with `nice -n 10 python3 plugin/tests/run.py test_close_affected`
- [ ] _cached_pass skips a newer run on another code tree and reuses the newest pass on this one; a newer red run on this tree still misses — verify with `nice -n 10 python3 plugin/tests/run.py test_round_f test_verify_strength test_close_affected`
## Non-goals
## Approach (options → choice → why)
1) do less: a train pass holds for any task in its train list, names ignored. Likely outcome: batch-2 in-train closes reuse; fails if: a close not in the train (T-3546) or a sentinel run in between still reruns. 2) use what exists: select as train._affected_gate does (another runner's tests left to their own gate), drop the mirror .md files from affected()'s changed set as core.code_tree and worktree_tree already do, and let _cached_pass skip runs on other code trees to the newest run on this one. Likely outcome: 6/6 batch-2 closes and 10/13 batch-1 closes reuse; fails if: a project's other runner has no gate (the train makes the same assumption). 3) log the full linked names in close_affected and decide later. Likely outcome: better data, no time saved; fails if: nobody reads it. Choice 2 (80%): it fixes the cause for every close, in a train or not, with the selector the train already uses.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests: tsx + mirror close reuses the train pass; a newer other-tree run doesn't hide it  <- CURRENT
2. [x] Fix: _gates_cover selects like train._affected_gate; affected() leaves out mirror .md; _cached_pass looks past other code trees
3. [x] Replay the ledger with the new logic: closes reused before → after, seconds saved
## Resume here
## Docs impact
docs/map/ops-1.md (close gates: how a close's linked tests are counted against a gate pass, T-3566)
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_close_affected` → ✗ exit 1 · Ran 8 tests in 105.6s (8 jobs, 16 at a time; slowest: CloseAffectedReuse.test_no_pass_at_all_says_so 2s, CloseAffectedReuse.test_another_runner_runs_them_once_despite_the_pass 2s, CloseAffectedReuse.t [ran] [tree e14eb3e729e2] [world 2f1906870a] (2026-11-07T02:53:06Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_close_affected test_round_f test_verify_strength test_lane_train test_affected_hubs test_affected_rules test_affected_symbols test_ship` → exit 0 · Ran 160 tests in 148.2s (11 jobs, 16 at a time; slowest: Ship 104s, Train 30s, VerifyStrength 17s) / OK [ran] [tree fde8db4cdf3d] [world 2f1906870a] (2026-11-07T02:57:58Z)
- (step 3) `python3 -I /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3566/replay.py` → exit 0 · 02:20 T-3533   53.9s actual rerun old: False new: True / 02:22 T-3331   72.2s actual rerun old: False new: True [ran] [tree fde8db4cdf3d] [world 2f1906870a] (2026-11-07T02:58:09Z)
- (ac 2) `nice -n 10 python3 plugin/tests/run.py test_round_f test_verify_strength test_close_affected` → exit 0 · Ran 55 tests in 35.5s (55 jobs, 16 at a time; slowest: VerifyStrength.test_a_timed_out_check_kills_its_whole_process_group 5s, CloseAffectedReuse.test_no_pass_at_all_says_so 5s, Repeat.test_timed_out_ [ran] [tree fde8db4cdf3d] [world 2f1906870a] (2026-11-07T02:58:49Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py test_close_affected` → exit 0 · Ran 8 tests in 2.1s (8 jobs, 16 at a time; slowest: CloseAffectedReuse.test_a_train_pass_covers_another_runners_tests_and_the_mirrors_noise 2s, CloseAffectedReuse.test_another_runner_runs_them_once_de [ran] [tree fde8db4cdf3d] [world 2f1906870a] (2026-11-07T02:58:52Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py test_close_affected` → exit 0 · Ran 10 tests in 41.2s (1 jobs, 16 at a time; slowest: CloseAffectedReuse 35s) / OK [ran] [tree 83538f536bc7] [world 2f1906870a] (2026-11-07T03:07:13Z)
## Log
- 2026-11-07T01:06:26Z created
- 2026-11-07T02:45:06Z planned: it has criteria and steps
- 2026-11-07T02:45:10Z lane: ~/.claude/foreman.lanes/T-3566 on foreman/T-3566
- 2026-11-07T02:45:29Z focused
- 2026-11-07T02:45:30Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T02:58:02Z scope: plugin/lib/sampo/cli.py, plugin/lib/sampo/train.py, plugin/tests/test_close_affected.py, docs/map/ops-1.md — the close's reuse selector, shared with the train (suite_gate)
- 2026-11-07T03:06:30Z steer: review — another runner's tests count as covered only when a gate runs that runner (suite_gate over _argv, so this repo's cd-spelled .tsx runner matches its claude plugin test gate); none: a miss 'no gate runs the .tsx tests'
- 2026-11-07T04:15:35Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3544 [PERFORMANCE M, done, 3 steps] Merge trains test only what changed: the gate runs the tests affected by the batch's merged changes (plus the rule tests), the full…
- T-3548 [FIX M, active, 3 steps] A close's reuse of the train's pass (T-3526) never hit: the working tree's code tree…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-11-06: Post-merge suite back on (supersedes the pause): a close runs only its criteria and affected tests, not the full suite, so the post-merge run is the…
- similar finished tasks took 3–5 steps
## Measurements
Closes that reuse the train's pass, ledger replay of 2026-11-07 (scratchpad replay.py; old rule reproduces the actual reuse on every row): batch 2 (train 02:10, 181 affected modules) 0/6 → 6/6, 459.3 s of linked-test reruns saved (393 s net of the ~11 s test_docs.Judgment each code-tree reuse over a changed CHANGELOG runs); batch 1 (train 00:04, full suite) 1/14 → 11/14, 1,587 s saved (1,477 s net); the 3 left (00:10-00:22) sat on an untracked scripts/ file in the main checkout, T-3548's self-check.
