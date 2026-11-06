---
id: T-2766
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/reverify.py, plugin/lib/sampo/graph.py, plugin/lib/sampo/ideas.py, plugin/lib/sampo/split.py, plugin/lib/sampo/release.py, plugin/lib/sampo/stack.py, plugin/bin/*, plugin/tests/test_rename_*.py, plugin/tests/test_docs.py, plugin/tests/test_secrets.py]
depends_on: []
source: user
created: 2026-11-03T04:16:26Z
updated: 2026-11-03T15:03:32Z
builder_model: sonnet
base: bea1f96e9ccab952692552a980a9d363e22fae24
base_tree: 0a945a8c2cbc82d189242c112b49f5e06bf59d64
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-03T04:16:59Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/reverify.py, plugin/lib/sampo/graph.py, plugin/lib/sampo/ideas.py, plugin/lib/sampo/split.py, plugin/lib/sampo/release.py, plugin/lib/sampo/stack.py, plugin/bin/*, plugin/tests/test_rename_*.py, plugin/tests/test_docs.py, plugin/tests/test_secrets.py]
lane_stop: merged 2026-11-03T04:51:27Z
verified: strong
---
# sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as their old verbs; fm prints one now-sampo line a day on a TTY; SAMPO_X and FOREMAN_X mirror each other; Sampo-Task is written and both trailers are read
## Raw request
> sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as their old verbs; fm prints one now-sampo line a day on a TTY; SAMPO_X and FOREMAN_X mirror each other; Sampo-Task is written and both trailers are read
## Interpretation
Reading 1 (chosen): SAMPO.md's alias rule for the CLI, environment and trailer, done the way T-2742's logged step-2 plan says. (a) `sampo` (plugin/bin/sampo sets SAMPO_PROG) is the same CLI. The new verbs map silently onto the old ones in the CLI's ALIASES/_alias table (plugin/lib/sampo/cli.py ~8353): smith→code, rune→genesis, louhi→exam, ward→guard, moons→genesis moonshot, and underworld→a new genesis action that prints the tower's not-yet.md. A new name never prints '(ran `fm …`)'. The parser's prog and its messages ('usage: fm …', 'fm help lists them') say whatever was typed (sampo or fm). (b) fm says '… now sampo …' as one stderr line at most once a day, only when stderr is a TTY, never under sampo, never to scripts; the stamp lives in the state dir. (c) One env mirror at sampo.core import covers every FOREMAN_* read: SAMPO_X overrides FOREMAN_X, and FOREMAN_X fills SAMPO_X when it is unset. (d) The trailer readers accept (?:Sampo|Foreman)-Task: reverify.py:42 (%(trailers:key=…) takes both keys), graph.py:68, ideas.py:636, cli.py:1136/5294/5351/5357 (git --grep needs -E), split.py:120. The writers say Sampo-Task: cli.py:2182 (finish --commit; skip when either trailer is already in the message), release.py:189/696, stack.py:80. test_secrets:84 asserts Sampo-Task. Reading 2 (ruled out): rename the verbs outright in the parser. That breaks fm genesis/exam/guard/code for scripts and the user's habits, which SAMPO.md forbids.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo runs the six new verbs silently, the parser names what was typed, fm and every old verb still work, and fm says once a day on a TTY that it is now sampo — verify with `python3 plugin/tests/run.py test_rename_cli`
- [x] SAMPO_* is read with FOREMAN_* as its fallback (SAMPO wins), and both the Sampo-Task and Foreman-Task trailers name a task's commits — verify with `python3 plugin/tests/run.py test_rename_env`
- [x] nothing else breaks: the rename suites and the CLI's own tests stay green — verify with `python3 plugin/tests/run.py test_rename_aliases test_rename_scan test_docs test_cli test_secrets test_graph test_split`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: extend the CLI's ALIASES/_alias table with a silent flag for the new names, plus one prog lookup from SAMPO_PROG or argv[0]; mirror env in sampo.core at import; switch the trailer regexes. Likely outcome: about 60 lines across 8 files, and the parked red tests go green. Fails if: a verb reads FOREMAN_X before sampo.core is imported (the hook and bin entry points); then the mirror moves into the entry points too.
2. Register each new verb as a full argparse subparser that copies the old one. Fails if: it doubles every verb's help and tests, and drifts from the original.
3. Do less: only the sampo entry point and silent aliases, leaving env and trailers for later. Fails if: SAMPO.md's acceptance names SAMPO_* and Sampo-Task, and test_rename_env stays red.
Choice 1 (85%).
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, MASTER.md, site/pages.py, plugin/lib/fmcli.py, site/build.py; past FIXes T-1239, T-1371, T-1569, T-1714, T-2266.
## Execution prompt
## Steps
1. [x] move the parked red tests (test_rename_cli.py, test_rename_env.py) into plugin/tests and see them fail
2. [x] the verb map and the parser's prog, the daily fm line
3. [x] the env mirror at core import, the trailer readers and writers; drop test_docs' SAMPO_OLD/SAMPO_NEW map
## Resume here
<!-- auto -->
- 2026-11-03T04:41:11Z step 1/3: move the parked red tests (test_rename_cli.py, test_rename_env.py) into plugin/tests and see them fail
- git: worktree-agent-a543507836f2996bc; 1 uncommitted: ANDON.md
- touched since last checkpoint: plugin/lib/sampo/rune.py, plugin/tests/test_rename_cli.py, plugin/bin/sampo, plugin/lib/sampo/py.py, ANDON.md, plugin/lib/sampo/core.py, plugin/lib/sampo/graph.py, plugin/lib/sampo/ideas.py, plugin/lib/sampo/split.py, plugin/lib/sampo/stack.py, plugin/lib/sampo/reverify.py, plugin/tests/test_docs.py, plugin/tests/test_secrets.py, plugin/lib/sampo/release.py, plugin/lib/sampo/cli.py
## Docs impact
none: SAMPO.md and the CHANGELOG entry (T-2742 step 8) cover the names
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_rename_cli test_rename_env` → ✗ exit 1 · Ran 9 tests in 2.4s (2 classes, 16 at a time; slowest: RenameCli 2s, RenameEnv 1s) / FAILED (2 classes: test_rename_cli.RenameCli, test_rename_env.RenameEnv) [ran] [tree f185698830f4] [world 2f1906870a] (2026-11-03T04:17:35Z)
- (step 2) `python3 plugin/tests/run.py test_rename_cli` → exit 0 · Ran 7 tests in 6.5s (1 classes, 16 at a time; slowest: RenameCli 5s) / OK [ran] [tree 07f52f19787b] [world 2f1906870a] (2026-11-03T04:26:02Z)
- (ac 3) `python3 plugin/tests/run.py test_rename_aliases test_rename_scan test_docs test_cli test_secrets test_graph test_split 2>&1 | tail -40` → ✗ exit 1 · FAILED (1 classes: test_rename_aliases.RenameAliases) / ✗ exit 1 (94.0 s; last 24 of 24 lines) [ran] [tree a6e4c8d6f4bf] [world 2f1906870a] (2026-11-03T04:30:14Z)
- (step 3) `python3 plugin/tests/run.py test_rename_env test_secrets test_graph test_split test_docs test_cli test_rename_scan` → exit 0 · Ran 288 tests in 57.1s (82 classes, 16 at a time; slowest: TaskLifecycle 56s, CaptureAndIntake 27s, StateViews 27s) / OK [ran] [tree a6e4c8d6f4bf] [world 2f1906870a] (2026-11-03T04:31:29Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit_run test_bench test_bench_family test_board_verbs test_budget test_bus test_check_paths test_ci_watch test_claude test_clean_helpers test_cli test_code test_code_bench test_code_envelope test_code_fakes test_code_hardening test_code_worker test_core test_crash_hygiene test_deliberation test_design_tokens test_docs test_docsdrift test_doctor test_draft test_ecosystem test_evidence_quality test_evolve test_exam test_find test_fmpy test_genesis test_goal test_graph test_guard test_guard_diff test_guard_exec_vectors test_hooks test_ideas test_ideation test_intent test_judge_home test_judgment test_knowledge test_long test_model_probe test_motion_verify test_night test_oracle test_outside test_parallel test_pass4 test_perf_cost test_plugin_parity test_plugins test_pr_train test_prove test_reaper test_relate test_release test_rename_cli test_rename_env test_replan test_request test_research test_research_rigor test_retired_models test_runner_lint test_runtime test_scaffold test_second test_secrets test_serve test_session test_session_care test_session_fixes test_settings_extras test_setup test_ship test_smoke test_smoke_profiles test_split test_stack test_steer test_supply_delta test_until_conditions test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [51.04s] [ran] [tree 06e389d3bda7] [world 2f1906870a] (2026-11-03T04:40:57Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_cli` → exit 0 · Ran 7 tests in 4.6s (1 classes, 16 at a time; slowest: RenameCli 4s) / OK [ran] [tree 43ad4698efa7] [world 2f1906870a] (2026-11-03T05:49:42Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_env` → exit 0 · Ran 3 tests in 1.6s (1 classes, 16 at a time; slowest: RenameEnv 1s) / OK [ran] [tree 43ad4698efa7] [world 2f1906870a] (2026-11-03T05:49:42Z)
- (ac 3) `python3 plugin/tests/run.py test_rename_aliases test_rename_scan test_docs test_cli test_secrets test_graph test_split` → exit 0 · Ran 293 tests in 48.5s (82 classes, 16 at a time; slowest: TaskLifecycle 48s, CaptureAndIntake 26s, StateViews 23s) / OK [ran] [tree 43ad4698efa7] [world 2f1906870a] (2026-11-03T05:49:42Z)
- (step 1) `python3 plugin/tests/run.py test_rename_cli test_rename_env` → exit 0 · Ran 10 tests in 4.2s (2 classes, 16 at a time; slowest: RenameCli 4s, RenameEnv 1s) / OK [ran] [tree 43ad4698efa7] [world 2f1906870a] (2026-11-03T05:49:42Z)
- (audit intent) `self: read the merged diff and the andon's decision; SAMPO_X mirrors into FOREMAN_X and is popped` → sampo's verbs run as the old ones, SAMPO_* wins over FOREMAN_*, Sampo-Task is written and both trailers are read [tree 43ad4698efa7] (2026-11-03T05:49:42Z)
- (audit edge) `self: read the merged diff and the andon's decision; SAMPO_X mirrors into FOREMAN_X and is popped` → a child given its own FOREMAN_X never inherits a stale SAMPO_X (popped); the now-sampo line prints once a day on a TTY only [tree 43ad4698efa7] (2026-11-03T05:49:42Z)
- (audit adversary) `self: read the merged diff and the andon's decision; SAMPO_X mirrors into FOREMAN_X and is popped` → SAMPO_HOME is popped after the mirror so the guard reads one name; the literal SAMPO_HOME/state still matches the guard's scan [tree 43ad4698efa7] (2026-11-03T05:49:42Z)
- `python3 plugin/tests/run.py test_rename_aliases test_rename_scan test_rename_cli test_rename_env test_docs test_cli` → exit 0 · Ran 271 tests in 31.8s (70 classes, 16 at a time; slowest: TaskLifecycle 31s, CaptureAndIntake 15s, StateViews 14s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:58:12Z)
- (audit intent) `self: read the merged diff and the andon's decision; SAMPO_X mirrors into FOREMAN_X and is popped` → sampo's verbs run as the old ones, SAMPO_* wins over FOREMAN_*, Sampo-Task is written and both trailers are read [tree 1b964dd8dbe8] (2026-11-03T14:58:12Z)
- (audit edge) `self: read the merged diff and the andon's decision; SAMPO_X mirrors into FOREMAN_X and is popped` → a child given its own FOREMAN_X never inherits a stale SAMPO_X (popped); the now-sampo line prints once a day on a TTY only [tree 1b964dd8dbe8] (2026-11-03T14:58:12Z)
- (audit adversary) `self: read the merged diff and the andon's decision; SAMPO_X mirrors into FOREMAN_X and is popped` → SAMPO_HOME is popped after the mirror so the guard reads one name; the literal SAMPO_HOME/state still matches the guard's scan [tree 1b964dd8dbe8] (2026-11-03T14:58:12Z)
## Log
- 2026-11-03T04:16:26Z created
- 2026-11-03T04:16:41Z set approved=True
- 2026-11-03T04:16:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2766.builder.md
- 2026-11-03T04:16:56Z focused
- 2026-11-03T04:16:59Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-03T04:51:27Z merged worktree-agent-a543507836f2996bc (15 file(s))
- 2026-11-03T04:53:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a543507836f2996bc
- 2026-11-03T05:48:37Z focused
- 2026-11-03T05:48:38Z scope: files outside the scope since focus came from other lanes' merge commits, not this task's edits
- 2026-11-03T05:59:44Z paused: focus moved to T-2767
- 2026-11-03T14:57:37Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T14:57:37Z focused
- 2026-11-03T15:03:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2748 [CLEAN M, active, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py…
- T-2745 [SECURITY M, done, 3 steps] Ward knows Sampo: the guard treats sampo (and plugin/bin/sampo) exactly as fm, sampo* modules as fm* ones, SAMPO_STATE, SAMPO_HOME and…
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit_run.py, plugin/tests/test_bench.py, plugin/tests/test_bench_family.py, plugin/tests/test_board_verbs.py, plugin/tests/test_budget.py…
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/bin/sampo, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/graph.py, plugin/lib/sampo/ideas.py, plugin/lib/sampo/release.py, plugin/lib/sampo/reverify.py, plugin/lib/sampo/…; re-ground the plan against them before editing
## Lessons
- Mirror one way and pop the source so one name is read
## Plan gaps
- failed first: step 1 move the parked red tests (test_rename_cli.py, test_rename_env.py) into plugin/tests and see them f…
## Files touched
- plugin/tests/test_rename_cli.py
- plugin/tests/test_rename_env.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/rune.py
- plugin/bin/sampo
- plugin/lib/sampo/py.py
- plugin/lib/sampo/core.py
- ANDON.md
- plugin/lib/sampo/graph.py
- plugin/lib/sampo/ideas.py
- plugin/lib/sampo/split.py
- plugin/lib/sampo/release.py
- plugin/lib/sampo/stack.py
- plugin/lib/sampo/reverify.py
- plugin/tests/test_docs.py
- plugin/tests/test_secrets.py
