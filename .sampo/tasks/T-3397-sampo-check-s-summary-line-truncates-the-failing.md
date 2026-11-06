---
id: T-3397
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T07:11:48Z
updated: 2026-11-06T08:04:04Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a591e1ef550c60621
lane_branch: worktree-agent-a591e1ef550c60621
base: 1e1c29e31cc159395ca6ac04cedb714d3fb14c89
base_tree: c52b066e571b19f07ff3d5cc92292ff201c55ec1
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T07:43:36Z
plan0_scope: []
builder_returned: 2026-11-06T08:04:04Z
---
# Sampo check's summary line truncates the failing-class list (~200 chars), so builders…
## Raw request
> FIX: sampo check's summary line truncates the failing-class list (~200 chars), so builders rerun whole suites to learn which classes failed; print every failing class name, one per line (T-3380, T-3181 builders)
## Interpretation
Reading 1: print and ledger every failing class (chosen). Reading 2: only raise the 200-char cut; ruled out, any cap truncates again.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a gate naming 12 failing classes prints all 12 and the ledger carries all 12 — verify with `python3 plugin/tests/run.py test_cli.Checks test_run`
## Non-goals
## Approach (options → choice → why)
1) run.py marker lines parsed by core; likely outcome: lossless names. 2) use what exists: widen the existing [:200] and 5-name caps; fails if a long list outgrows it. 3) do less: parse only the FAILED line; fails if run.py caps it at 5 names. Choice 1 (80%): lossless, no cap to outgrow.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then implement
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.Checks test_run test_left_out` → ✗ exit 1 · Ran 103 tests in 20.0s (50 jobs, 16 at a time; slowest: DiffGates 10s, PerTestJobs 8s, Hang 8s) / FAILED (1 classes: test_cli.Checks) [ran] [tree 4a3dc9a7dd45] [world 2f1906870a] (2026-11-06T07:44:50Z)
- (step 1) `python3 plugin/tests/run.py test_cli.Checks test_run test_left_out` → exit 0 · Ran 107 tests in 7.1s (78 jobs, 16 at a time; slowest: DiffGates 5s, UnknownNames.test_a_red_runs_last_line_names_the_failing_class 4s, CheckSkip 4s) / OK [ran] [tree 167b81dbf85a] [world 2f1906870a] (2026-11-06T07:45:04Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ci_annotations test_cli test_core test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_run test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [18.99s] [ran] [tree 167b81dbf85a] [world 2f1906870a] (2026-11-06T07:45:46Z)
- (step 1) `python3 plugin/tests/run.py test_cli.Checks` → ✗ exit 1 · Ran 14 tests in 52.9s (14 jobs, 16 at a time; slowest: Checks.test_the_suite_gate_deadline_scales_with_load_and_a_timeout_names_both 3s, Checks.test_a_failing_gate_is_not_hidden_by_a_later_passing_one [ran] [tree ed21a3013c62] [world 2f1906870a] (2026-11-06T08:01:55Z)
- (step 1) `python3 plugin/tests/run.py test_cli.Checks.test_a_red_gate_names_its_classes_in_the_finish_refusal_and_the_affected_print` → exit 0 · Ran 1 tests in 11.6s (1 jobs, 16 at a time; slowest: Checks 1s) / OK [ran] [tree dfb13259e8eb] [world 2f1906870a] (2026-11-06T08:02:15Z)
- (step 1) `python3 plugin/tests/run.py test_cli.Checks` → exit 0 · Ran 14 tests in 34.8s (1 jobs, 16 at a time; slowest: Checks 7s) / OK [ran] [tree dfb13259e8eb] [world 2f1906870a] (2026-11-06T08:02:56Z)
- (step 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 91 tests in 46.5s (61 jobs, 16 at a time; slowest: DiffGates 37s, CheckSkip 32s, PerTestJobs.test_a_split_class_runs_as_one_job_per_test_and_a_failure_names_the_test 28s) / OK [ran] [tree dfb13259e8eb] [world 2f1906870a] (2026-11-06T08:03:44Z)
- (step 1) `python3 plugin/tests/run.py test_left_out` → exit 0 · Ran 3 tests in 0.5s (1 jobs, 16 at a time; slowest: LeftOut 0s) / OK [ran] [tree dfb13259e8eb] [world 2f1906870a] (2026-11-06T08:03:45Z)
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 6.3s (5 jobs, 16 at a time; slowest: AffectedPairs.test_only_the_red_first_file_itself_is_left_out 2s, AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 2s, AffectedPai [ran] [tree dfb13259e8eb] [world 2f1906870a] (2026-11-06T08:03:55Z)
## Log
- 2026-11-06T07:11:48Z created
- 2026-11-06T07:43:24Z planned: it has criteria and steps
- 2026-11-06T07:43:35Z focused
- 2026-11-06T07:43:36Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T07:44:29Z criterion 1 verify: `python3 plugin/tests/run.py test_check_failed` → `python3 plugin/tests/run.py test_cli.Checks test_run`
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-2613 [FEATURE M, done, 4 steps] fm exam long grade splits false dones into misses on names the goal never states and real misses — lesson: When an automatic rule repla…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
