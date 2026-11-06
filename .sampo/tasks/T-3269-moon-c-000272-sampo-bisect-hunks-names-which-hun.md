---
id: T-3269
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/bisecthunk.py, plugin/lib/fmbisecthunk.py, plugin/lib/sampo/cli.py, plugin/tests/test_bisect_hunks.py, MASTER.md, docs/map/files-lib-2.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:27:24Z
updated: 2026-11-06T04:01:04Z
builder: 2026-11-06T02:27:31Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-a71b68a594cef35d3
lane_branch: worktree-agent-a71b68a594cef35d3
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:23Z
plan0_scope: [plugin/lib/sampo/bisecthunk.py, plugin/lib/sampo/cli.py, plugin/tests/test_bisect_hunks.py, CHANGELOG.md]
builder_returned: 2026-11-06T04:01:04Z
---
# Moon C-000272: sampo bisect --hunks names which hunk of the first bad commit breaks the check
## Raw request
> Moon C-000272: sampo bisect --hunks names which hunk of the first bad commit breaks the check
## Interpretation
Reading 1 (chosen): when a check goes red, sampo bisect already names the first bad commit and its files (cli.py cmd_bisect:5378, first_bad); this adds --hunks, which says which hunk of that commit matters, by reverting each hunk alone in a throwaway worktree and re-running the check (reuses _hunks/_revert_hunk from task prove --hunks, cli.py:2231). Reading 2 (ruled out): a general replay-with-changed-input pipeline stepper, because Sampo has no pipeline-state model and the bisect plus hunk revert is the same what-if for code.
## Assumptions (confidence)
## Acceptance criteria
- [ ] bisect --hunks reverts each hunk of the first bad commit alone in a throwaway worktree and names those after which the check passes (file, line range) — verify with `python3 plugin/tests/run.py test_bisect_hunks`
- [ ] a commit whose bad change spans two hunks of two files names only the culprit hunk, and the user's tree and worktrees list are unchanged afterwards — verify with `python3 plugin/tests/run.py test_bisect_hunks`
- [ ] existing bisect output is unchanged without --hunks — verify with `python3 plugin/tests/run.py test_diagnosis`
## Non-goals
## Approach (options → choice → why)
1. New module bisecthunk.py with culprit_hunks(), lazy-importing cli._hunks/_revert_hunk, plus a --hunks flag in cmd_bisect. Likely outcome: small diff, one cli.py touch, hunk-level answer.
2. Extend task_prove_hunks to take a commit range. Likely outcome: edits the large cli.py function that other lanes touch, merge conflicts.
3. Revert whole files instead of hunks. fails if: a commit's file holds both the culprit and innocent changes, which is the common case.
4. Do less: print git show --stat only. Likely outcome: already what bisect does, no new value.

Choice 1 (85%): isolates new logic in its own module and reuses the proven hunk revert. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] failing test first: temp repo, 3-commit history, one commit with two hunks, only one breaks the check  <- CURRENT
2. [x] new module plugin/lib/sampo/bisecthunk.py: culprit_hunks(root, sha, cmd, timeout) reusing cli._hunks/_revert_hunk via lazy import
3. [x] add --hunks flag to the bisect parser and print the culprit hunks in cmd_bisect (small edit)
4. [x] CHANGELOG line, run the two test modules
## Resume here
<!-- auto -->
- 2026-11-06T03:38:35Z step 1/4: failing test first: temp repo, 3-commit history, one commit with two hunks, only one breaks the check
- git: worktree-agent-a71b68a594cef35d3; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_bisect_hunks` → ✗ exit 1 · Ran 4 tests in 2.5s (1 jobs, 16 at a time; slowest: Hunks 1s) / FAILED (1 classes: test_bisect_hunks.Hunks) [ran] [tree 41ddc0b340e6] [world 2f1906870a] (2026-11-06T02:30:06Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_bisect_hunks` → exit 0 · Ran 4 tests in 8.8s (4 jobs, 16 at a time; slowest: Hunks.test_the_hunk_whose_revert_passes_is_named 7s, Hunks.test_no_single_hunk_is_named_when_two_are_needed 5s, Hunks.test_the_user_tree_and_worktre [ran] [tree e64dd289f686] [world 2f1906870a] (2026-11-06T02:33:12Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 14 tests in 32.9s (8 jobs, 16 at a time; slowest: Refuted 30s, NewWork 13s, WhyNotCaught 13s) / OK [ran] [tree e64dd289f686] [world 2f1906870a] (2026-11-06T02:33:47Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_bisect_hunks` → exit 0 · Ran 4 tests in 5.0s (4 jobs, 16 at a time; slowest: Hunks.test_the_hunk_whose_revert_passes_is_named 4s, Hunks.test_no_single_hunk_is_named_when_two_are_needed 3s, Hunks.test_the_user_tree_and_worktre [ran] [tree 14a2cc57d075] [world 2f1906870a] (2026-11-06T02:34:34Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_bisect_hunks test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [65.88s] [ran] [tree 14a2cc57d075] [world 2f1906870a] (2026-11-06T02:46:33Z)
- (step 1) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_bisect_hunks` → ✗ exit 1 · Ran 9 tests in 65.3s (9 jobs, 2 at a time; slowest: Hunks.test_the_hunk_whose_revert_passes_is_named 21s, Hunks.test_no_single_hunk_is_named_when_two_are_needed 20s, Hunks.test_the_json_carries_the_ou [ran] [tree 3e180f7a4da9] [world 2f1906870a] (2026-11-06T03:43:13Z)
- (step 2) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_bisect_hunks` → exit 0 · Ran 9 tests in 46.5s (9 jobs, 2 at a time; slowest: Hunks.test_the_hunk_whose_revert_passes_is_named 14s, Hunks.test_no_single_hunk_is_named_when_two_are_needed 14s, Hunks.test_without_the_flag_the_ou [ran] [tree 59da663aba18] [world 2f1906870a] (2026-11-06T03:46:43Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 14 tests in 118.5s (14 jobs, 2 at a time; slowest: NewWork 33s, Refuted.test_the_rarest_shared_scope_ranks_first_and_the_scan_is_bounded 23s, Fingerprint 21s) / OK [ran] [tree 59da663aba18] [world 2f1906870a] (2026-11-06T03:48:48Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_bisect_hunks test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [91.05s] [ran] [tree 59da663aba18] [world 2f1906870a] (2026-11-06T04:00:32Z)
- (step 4) `sampo check --affected --evidence T-3269` → exit 0 · ✓ affected tests only (37): python3 plugin/tests/run.py test_ambient test_bisect_hunks test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_docs test_docsdrift test_d [ran] [tree 59da663aba18] [world 2f1906870a] (2026-11-06T04:00:33Z)
## Log
- 2026-11-06T02:27:24Z created
- 2026-11-06T02:27:30Z set scope=['plugin/lib/sampo/bisecthunk.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_bisect_hunks.py', 'CHANGELOG.md']
- 2026-11-06T02:27:31Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3269.builder.md
- 2026-11-06T02:28:22Z focused
- 2026-11-06T02:28:23Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:32:12Z set scope=['plugin/lib/sampo/bisecthunk.py', 'plugin/lib/fmbisecthunk.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_bisect_hunks.py', 'MASTER.md', 'docs/map/files-lib-2.md', 'CHANGELOG.md']
- 2026-11-06T02:32:13Z scope widened: the brief's standing rules need the fm shim (fmbisecthunk.py), a MASTER.md bullet and a docs/map line for the new module
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2918 [FEATURE M, done, 4 steps] M-02 slice: sampo regen PATH deletes one of Sampo's own modules in a throwaway worktree and regrows it on the local 27B from its intent…
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
