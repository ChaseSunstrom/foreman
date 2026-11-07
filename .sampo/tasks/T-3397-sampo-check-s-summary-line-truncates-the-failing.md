---
id: T-3397
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/tests/run.py, plugin/tests/test_cli.py]
depends_on: []
source: discovered
created: 2026-11-06T07:11:48Z
updated: 2026-11-06T21:59:29Z
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T07:43:36Z
plan0_scope: []
builder_returned: 2026-11-06T08:04:04Z
base: 89d0d3468a2770da2f90299261ea1f467b4500ce
base_tree: 9b757399c14a04329ce334557e059834a049f1f8
lane_stop: merged 2026-11-06T18:54:00Z
verified: strong
---
# Sampo check's summary line truncates the failing-class list (~200 chars), so builders…
## Raw request
> FIX: sampo check's summary line truncates the failing-class list (~200 chars), so builders rerun whole suites to learn which classes failed; print every failing class name, one per line (T-3380, T-3181 builders)
## Interpretation
Reading 1: print and ledger every failing class (chosen). Reading 2: only raise the 200-char cut; ruled out, any cap truncates again.
## Assumptions (confidence)
## Acceptance criteria
- [x] a gate naming 12 failing classes prints all 12 and the ledger carries all 12 — verify with `python3 plugin/tests/run.py test_cli.Checks test_run`
## Non-goals
## Approach (options → choice → why)
1) run.py marker lines parsed by core; likely outcome: lossless names. 2) use what exists: widen the existing [:200] and 5-name caps; fails if a long list outgrows it. 3) do less: parse only the FAILED line; fails if run.py caps it at 5 names. Choice 1 (80%): lossless, no cap to outgrow.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then implement
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
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
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree f997eb98c8d4] (2026-11-06T19:03:52Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.Checks test_run` → exit 0 · Ran 113 tests in 5.0s (79 jobs, 16 at a time; slowest: Hang 5s, UnknownNames 4s, PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 4s) / OK [ran] [tree f997eb98c8d4] [world 2f1906870a] (2026-11-06T19:04:01Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree f997eb98c8d4] (2026-11-06T19:04:01Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree f997eb98c8d4] (2026-11-06T19:04:01Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree f997eb98c8d4] (2026-11-06T19:04:01Z)
## Log
- 2026-11-06T07:11:48Z created
- 2026-11-06T07:43:24Z planned: it has criteria and steps
- 2026-11-06T07:43:35Z focused
- 2026-11-06T07:43:36Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T07:44:29Z criterion 1 verify: `python3 plugin/tests/run.py test_check_failed` → `python3 plugin/tests/run.py test_cli.Checks test_run`
- 2026-11-06T17:37:55Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a591e1ef550c60621 (branch worktree-agent-a591e1ef550c60621 kept: not merged)
- 2026-11-06T17:37:56Z lane: ~/.claude/foreman.lanes/T-3397 on foreman/T-3397
- 2026-11-06T17:38:36Z focused
- 2026-11-06T18:54:00Z merged foreman/T-3397 in merge train
- 2026-11-06T19:03:52Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/tests/run.py', 'plugin/tests/test_cli.py']
- 2026-11-06T19:03:52Z scope: widened at merge to the reviewed lane's own diff (016e39895), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T19:04:41Z done
- 2026-11-06T19:04:43Z committed 8b61cb108 (1 file)
- 2026-11-06T21:59:29Z lane removed: ~/.claude/foreman.lanes/T-3397; dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-2613 [FEATURE M, done, 4 steps] fm exam long grade splits false dones into misses on names the goal never states and real misses — lesson: When an automatic rule repla…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 test, then implement
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/sampo/core.py
- plugin/tests/run.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
