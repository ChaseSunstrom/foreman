---
id: T-3427
type: FIX
tier: M
status: dropped
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-11-06T10:32:54Z
updated: 2026-11-06T19:12:20Z
trigger: baseline
trigger_key: a288bcd4419dc8e3
baseline: true
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_check_paths.CheckSkip.test_a_committed_test_file_is_shared_and_still_runs, test_check_paths.CheckSkip.test_a_look_alike_tests_folder_proves_nothing_about_the_gates_own, test_check_paths.CheckSkip.test_a_pass_with_tests_left_out_isnt_reused_once_they_count_again, test_check_paths.CheckSkip.test_a_red_test_in_this_tasks_scope_still_runs, test_check_paths.CheckSkip.test_an_inherited_skip_list_skips_nothing, test_check_paths.CheckSkip.test_another_tasks_red_first_test_is_skipped_and_named …. Captured by sampo check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T10:32:54Z created
- 2026-11-06T19:12:20Z dropped: green on HEAD 016e39895+: python3 plugin/tests/run.py test_check_paths ran 11 tests OK (CheckSkip 4 s); a load-time flake, covered by T-3436's load-robust classes
## Follow-ups captured
