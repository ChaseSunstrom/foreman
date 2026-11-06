# Why long goals false-done (T-2556)

Source: fm exam long l001 and l002, foreman arm (2026-10-31). Each goal's hidden checks were rerun on the session's kept tree the grader's way (hidden test files laid over a copy), keeping each failure's first error line. Raw output below.

## Classes (31 failed checks over 12 goals)
- Out of the goal's reach, 17: the check demands an interface the goal text never states. Missing attributes: fmlong.KILL_T ×5 (T-2262), fmwatch._shown (T-1674). JSON keys: 'problems' ×4 (T-2093), 'read' ×2. A return shape: 'Result object is not subscriptable' ×3 (T-2279). An exact viewBox '0 0 64 64' (T-2041). An installed binding's API: tree_sitter_language_pack.get_parser (T-2240, environment).
- Planned but not built, or built incomplete, 9: T-2020 compiled 104 patterns lazily where its checks need 150+, and module-level patterns remain (×3); T-1665 leaves sensitive projects in the export; T-2181 legacy-file reads (×3); T-2093 a full grid reported not ok (×1); T-2211 one child scenario rejected (×1).
- Built but different, 5: T-2031's closed-keys file holds a path the check forbids; T-2225's required-languages rule reads every language as required (×2); T-2240 rule headers and precision keys (×2).

## What it means
- The largest class is the exam's keys, not Foreman: l001's goals state no new names, and l002's 'The checks use these new names' hint still leaves JSON keys and return shapes unstated. Foreman never rewrites its own exam's keys. This goes to the final report for the user, and any re-keying is done by the tool-less child author (--author child).
- The next class is real: the session claimed done with a stated requirement unmet (T-2020's Done when, T-1665's sensitive projects). T-2557 targets it: before a goal session claims done, each line of the goal's Done-when list and each stated requirement is checked against the tree, or named missing.
- Plain scored 1 of 6 true and 5 false dones on l002, consistent with the reach class dominating both arms.

```
=== l001 T-1665: fm home export and import: a redacted state tarball with a hash manifest, checked on import into an empty home (T-1665)
fm home: an allowlist both ways, grants 
  FAIL test_a_sensitive_project_is_left_out: AssertionError: 'sensitive' not found in 'Wrote /tmp/tmp_bi9slss/home.tar.gz: 6 file(s) from 1 project(s), redacted; grants, commands, ledgers and sessions stay here. Review it before you share it.\n'
  pass test_invisible_characters_inside_marks_dont_save_them
=== l001 T-1674: fm ui --json: every string of the view shown plain, paths kept (T-1674)
  FAIL test_every_string_of_the_view_is_shown_plain_but_paths: AttributeError: module 'fmwatch' has no attribute '_shown'
  pass test_no_string_holds_a_control_character
=== l001 T-2031: Fast active-task scan reads a small closed-keys file instead of the 700 KB brief index: PreToolUse 39 -> 36 ms (T-2031)
  FAIL test_brief_index_the_fast_scan_reads_only_the_closed_keys: AssertionError: '/tmp/tmpj84dh4a2/fhome/state/projects/app-32283b/tasks/T-0001-t0.md' unexpectedly found in ['/tmp/tmpj84dh4a2/fhome/state/projects/app-32283b/briefs-closed.json', '/tmp/tmpj84dh4a2/fh
=== l001 T-2181: fm genesis check flags a tower file whose current text has no cold-read pass on record (T-2181)
fm genesis check read: grow and confirm keep a read lineage.md's
  pass test_a_grow_keeps_a_put_lineage_read_and_never_blesses_a_hand_edit
  FAIL test_a_sectioned_legacy_file_needs_a_pass_for_every_section: AssertionError: Lists differ: ['coverage.md: its current text has no col[101 chars].md'] != []
  FAIL test_a_sectioned_legacy_file_read_whole_counts: AssertionError: Lists differ: ['coverage.md: its current text has no col[101 chars].md'] != []
  FAIL test_legacy_file_is_clean_only_with_a_ledger_pass_just_before_its_mtime: AssertionError: Lists differ: ['coverage.md: its current text has no col[76 chars].md'] != []
  pass test_owned_files_and_gen0_are_exempt
=== l001 T-2225: Scorecard: a capability passes only with a graded result in every exam language; a narrowed run reads partial (T-2225)
Scorecard: required languages are the spe
  FAIL test_a_capability_graded_in_only_some_languages_is_partial_and_names_the_rest: AssertionError: Tuples differ: ('partial', 3, ['python', 'js', 'ts', 'ruby', 'rust', 'c']) != ('partial', 3, ['python'])
  FAIL test_a_python_only_spec_passes_on_python_and_odd_ids_never_crash: AssertionError: Tuples differ: ('partial', 3, ['python', 'js', 'ts', 'ruby',[58 chars]yet') != ('pass', 3, ['python'], '')
  pass test_draft_genesis_graded_in_every_language_passes
  FAIL test_a_grow_keeps_a_put_lineage_read_and_never_blesses_a_hand_edit: KeyError: 'read'
  FAIL test_a_sectioned_legacy_file_needs_a_pass_for_every_section: KeyError: 'read'
=== l001 T-2262: Long exam: foreman and plain session arms with planted kill, pause, compaction and misleading-test faults (T-2262)
Long exam review nits: validated goal ids, --
  FAIL test_a_kill_that_never_fires_is_logged_unfired_with_no_resume: AttributeError: module 'fmlong' has no attribute 'KILL_T'
  FAIL test_a_pause_whose_reply_has_no_marker_is_unfired_and_not_resumed: AttributeError: module 'fmlong' has no attribute 'KILL_T'
  FAIL test_a_resume_that_fails_after_a_kill_gets_one_fresh_turn_and_the_kill_cost_is_unknown: AttributeError: module 'fmlong' has no attribute 'KILL_T'
  FAIL test_a_tampered_run_json_id_is_refused_and_nothing_outside_the_run_is_touched: AttributeError: module 'fmlong' has no attribute 'KILL_T'
  FAIL test_all_faults_together_and_a_rerun_starts_clean: AttributeError: module 'fmlong' has no attribute 'KILL_T'
=== l002 T-2020: Hook modules compile their regexes on first use: PreToolUse 57 -> 44 ms, Notification 95 -> 85 ms (T-2020)

The checks use these new names: fmcore.lazy

Done wh
  FAIL test_lazy_a_pattern_compiles_on_first_use_and_keeps_its_methods: AssertionError: <built-in method search of re.Pattern object at 0x63f675fb00f0> is not <built-in method search of re.Pattern object at 0x63f675fb00f0>
  FAIL test_lazy_every_deferred_pattern_still_compiles: AssertionError: 104 not greater than 150
  FAIL test_lazy_importing_the_hook_modules_compiles_no_module_level_pattern: AssertionError: "['fmguard.py:342', 'fmguard.py:446', 'fm[1665 chars]41']" != '[]'
=== l002 T-2041: New logo: hard hat with a check, in the README and site (T-2041)

Done when:
- the mark is a small self contained square svg the readme shows
  FAIL test_the_mark_is_a_small_self_contained_square_svg_the_readme_shows: AssertionError: '0 0 32 32' != '0 0 64 64'
=== l002 T-2093: fm genesis check: coverage grid + not-yet ledger, exit 1 on any gap (T-2093)

Done when:
- a full grid and a tried ledger pass
- a grid without rows and punctua
  FAIL test_a_full_grid_and_a_tried_ledger_pass: AssertionError: 1 != 0 : {'ok': False, 'generation': 1, 'capabilities': 2, 'coverage': {'rows': 3, 'cells': 192, 'filled': 192}, 'not_yet': {'items': 1}, 'gaps': [{'kind': 'empty', 'where': 'not-yet: 
  FAIL test_a_grid_without_rows_and_punctuated_paths: KeyError: 'problems'
  FAIL test_an_empty_field_never_borrows_the_next_line_and_tries_must_differ: KeyError: 'problems'
  FAIL test_empty_ungrounded_and_unknown_cells_are_flagged: KeyError: 'problems'
  FAIL test_every_capability_needs_its_row: KeyError: 'problems'
=== l002 T-2211: Child authors write untested, clean, docs and flaky exam scenarios too, each its own validated reply shape (a new function with its test held back or kept, a fa
  pass test_a_new_function_is_exported_and_declared_where_the_language_needs_it
  FAIL test_children_author_untested_docs_flaky_and_clean_scenarios: AssertionError: Lists differ: [{'id': 'untested-python-2d9e79', 'why': "[245 chars]rs"}] != []
=== l002 T-2240: fm find --ladder tree-sitter rung: Foreman's .scm rules over an optional binding, capability-miss when absent (T-2240)

The checks use these new names: fmfind._
  FAIL test_a_binding_that_raises_is_a_note_not_a_crash: AssertionError: False is not true : ["tree-sitter rung: python: AttributeError: module 'tree_sitter_language_pack' has no attribute 'get_parser'", "tree-sitter rung: javascript: AttributeError: module
  pass test_absent_binding_is_one_capability_miss_and_a_note
  pass test_absent_language_pack_is_the_same_miss
  FAIL test_findings_join_the_scan_with_a_learned_precision_key: AssertionError: False is not true
  FAIL test_rule_headers_name_kind_and_message: AssertionError: [] is not true : []
=== l002 T-2279: fm doctor times each check: ms on Result, three slowest under -v and in --json (T-2279)
fm doctor timing: bench charged to hook latency, briefs and views timed,
  FAIL test_a_slow_bench_is_charged_to_hook_latency: TypeError: 'Result' object is not subscriptable
  FAIL test_a_slow_check_tops_the_slowest_list: TypeError: 'Result' object is not subscriptable
  pass test_json_and_verbose_carry_the_timings
  FAIL test_unmeasured_rows_are_none_and_briefs_and_views_are_timed: TypeError: 'Result' object is not subscriptable
```
