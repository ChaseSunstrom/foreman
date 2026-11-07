---
id: T-3537
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-06T21:55:03Z
updated: 2026-11-07T00:57:30Z
group: guard refuses legitimate lane and task work
lane: ~/.claude/foreman.lanes/T-3537
lane_branch: foreman/T-3537
base: 0033ea2768da24cb7879a2565e24269492ab3948
base_tree: 34ab8cd74598a0eb1439b89a358cf751cedf32f0
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-07T00:38:45Z
plan0_scope: []
---
# The Ward refused merging the build branch into a lane from inside that lane 5 times…
## Raw request
> FIX: the Ward refused merging the build branch into a lane from inside that lane 5 times today, the very step its own lane lesson recommends, and its hint (sampo lane merge ID) is for the main repo: treat a cd into a lane worktree followed by that merge as lane-local, with a FORMS row in test_guard_diff
## Interpretation
Reading 1 (chosen): a git merge of the main checkout's branch (foreman/build) run in a lane worktree's root (<repo>.lanes/<ID>, or <repo>/.claude/worktrees/<name>, a linked worktree of that repo) only updates that lane's checkout, so the guard lets it through; a merge in the main checkout, a merge of any other branch (a lane into build), extra operands or value-taking flags keep their refusal. Reading 2 (ruled out): exempt every git tree write under a lane folder: too wide, a checkout or reset of an arbitrary ref there is not the lesson's step, and the parent asked not to loosen beyond the build-branch merge. Found while grounding: the brief refusals are this rule (a nested worktree root is strictly under the unbriefed project root); the core ones on foreman.lanes come from a separate cwd misread (a later for V in $(…) loop makes the guard judge earlier commands from the session cwd), captured separately.
## Assumptions (confidence)
## Acceptance criteria
- [ ] cd into a lane worktree then git merge foreman/build passes; the same merge in the main checkout, a merge of a lane branch, and a cd that may be skipped stay refused — verify with `nice -n 10 python3 plugin/tests/run.py test_guard_diff.LaneMerge`
- [ ] FORMS rows with a lane merge before a payload still refuse the payload — verify with `nice -n 10 python3 plugin/tests/run.py test_guard_diff`
## Non-goals
## Approach (options → choice → why)
1) use what exists: the cwd walk already resolves where the merge runs; add one predicate on top that drops the brief/core finding for a build-branch merge whose every cwd is a lane worktree root: likely outcome: small diff, fails if: the walk's cwds include the main checkout (then it stays refused, the safe side). 2) exempt any tree write whose target is a worktree root from brief: fails if: a reset --hard/checkout of an arbitrary ref in a lane counts too (broader than asked). 3) rewrite the cwd walk so a later for-substitution keeps the head cd: likely outcome: fixes the foreman.lanes misread too, fails if: it opens a bypass in a security-critical parser (separate task). 4) do less: only change the hint to name a lane-local way: fails if: builders still can't do the lesson's step; the refusal stays wrong. Choice 1 (85%): narrowest change matching the lesson's step; the branch is read from the lane's own .git link to the common dir HEAD, so no hardcoded name, and another repo's lanes work the same.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests: lane-local merge allowed, main/lane-into-build merges refused; FORMS rows  <- CURRENT
2. [x] Guard: let a build-branch merge in a lane worktree root through
3. [x] Run targeted guard suites green
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_guard_diff.LaneMerge` → ✗ exit 1 · Ran 4 tests in 1.4s (1 jobs, 16 at a time; slowest: LaneMerge 0s) / FAILED (1 classes: test_guard_diff.LaneMerge) [ran] [tree c2f726c5ec75] [world 2f1906870a] (2026-11-07T00:44:20Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_guard_diff.LaneMerge test_guard.MergeHint` → exit 0 · Ran 5 tests in 18.9s (2 jobs, 16 at a time; slowest: LaneMerge 1s, MergeHint 1s) / OK [ran] [tree 291488a71c56] [world 2f1906870a] (2026-11-07T00:46:32Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_guard_diff test_guard_sampo test_guard` → exit 0 · Ran 346 tests in 40.8s (126 jobs, 16 at a time; slowest: Mutation 27s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 12s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 291488a71c56] [world 2f1906870a] (2026-11-07T00:47:18Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_guard_diff test_guard_sampo test_guard` → exit 0 · Ran 347 tests in 18.1s (118 jobs, 16 at a time; slowest: Mutation 18s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 11s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree f60dd1536d36] [world 2f1906870a] (2026-11-07T00:54:29Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_guard_diff test_guard_sampo test_guard` → exit 0 · Ran 347 tests in 16.3s (126 jobs, 16 at a time; slowest: Mutation 16s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 8s, GuardAgainstBash.test_every_form_that_runs_a_dangerou [ran] [tree 85e8241ae79b] [world 2f1906870a] (2026-11-07T00:57:22Z)
## Log
- 2026-11-06T21:55:03Z created
- 2026-11-07T00:33:10Z planned: it has criteria and steps
- 2026-11-07T00:33:22Z criterion 1 verify: `nice -n 10 python3 plugin/tests/run.py test_guard_lane_merge` → `nice -n 10 python3 plugin/tests/run.py test_guard_diff.LaneMerge`
- 2026-11-07T00:36:26Z lane: ~/.claude/foreman.lanes/T-3537 on foreman/T-3537
- 2026-11-07T00:38:44Z focused
- 2026-11-07T00:38:45Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-07T00:47:25Z steer: folded T-3553 (merge hint inside a non-lane worktree names the cd, not sampo lane merge) into this lane; discovered T-3560 (for V in $(…) cwd misread) captured
- 2026-11-07T00:54:10Z steer: security review FIX FIRST: lane exemption also needs no GIT_* name settable on the line (bare), depth 0; hint path shlex-quoted; merge note keyed on the git subcommand; red on the pre-review guard: 5 failures (4 env rows, hint)
- 2026-11-07T00:57:30Z steer: re-review FIX FIRST: lane exemption needs git typed bare as the command word (no wrapper or assignment prefix: env ${a}_DIR=…, env "G""IT_…", env -C, LC_ALL=C); rows red on 3b06e06e2 (4 failures), green now
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-3406 [FIX M, done, 1 steps] Sampo lane train can never pass in this repo: its gates run in a scratch worktree, where… — lesson: none: a reviewed builder lane; its less…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 1–9 steps
