---
id: T-2843
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T21:19:48Z
updated: 2026-11-03T22:12:59Z
base_note: Calibration: this plan states Choice 75% where FIX M closes (124) held on the first finish 95% of the time: 20 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-03T21:39:50Z
rival_split: true
builder_model: haiku
base: 998fdc5ab002649497c2dce476c36c4efea04286
base_tree: b8e26785e3c46646f8542b191ef71f994e4d9381
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-03T21:40:26Z
plan0_scope: []
lane_stop: merged 2026-11-03T22:05:47Z
verified: strong
---
# Inside a builder lane, bare 'fm lib check' (and other fm verbs reading plugin files)…
## Raw request
> FIX: inside a builder lane, bare 'fm lib check' (and other fm verbs reading plugin files) runs the main install via ~/.local/bin/fm, so a lane's check lints the main tree's cards and can pass without seeing the lane's own; lane briefs should name 'python3 plugin/bin/fm' or fm should prefer the worktree's plugin when run inside a lane (T-2799's builder)
## Interpretation
Reading 1: a builder runs in a lane worktree (.claude/worktrees/agent-*), but 'fm' on PATH resolves ~/.local/bin/fm to the main checkout's plugin/bin/fm, so PLUGIN_ROOT is the main tree: fm lib check lints the main cards (a vacuous pass), and fm check playbooks ratchet wrote ratchet.json into the main checkout (T-2778's builder). Fix: an fm launched inside a lane runs that lane's own plugin. Reading 2: only document 'python3 plugin/bin/fm' in lane briefs; ruled out as the whole fix because builders and hooks type bare fm by habit and the write hazard stays.
## Assumptions (confidence)
## Acceptance criteria
- [x] run from inside a lane worktree, the main install's fm re-runs the lane's own plugin/bin/fm (PLUGIN_ROOT is the lane), once; outside a lane nothing changes — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
1) bin/fm re-execs the lane's own plugin/bin/fm when the cwd is inside a git worktree of this same repo that has one and it isn't the running file (an env marker stops loops), saying once on stderr which root runs. Likely outcome: bare fm in a lane checks and writes the lane. Fails if: a lane's broken fm can't run at all; then fm in that folder fails too, which is where the broken code is anyway.
2) Lane briefs say 'python3 plugin/bin/fm' for every fm call. Likely outcome: the briefed calls are right. Fails if: a builder types bare fm from habit (it did).
3) fm warns when the cwd is a lane and PLUGIN_ROOT isn't the lane's. Likely outcome: visible. Fails if: the write already happened by the time anyone reads it.
4) Use what exists: py.reexec already re-runs bin/fm under another interpreter with an env marker; the lane re-exec copies that shape. Likely outcome: a dozen lines beside it. Fails if: reexec's marker semantics differ (it marks a Python child, not a root); use a separate marker.
5) Do less: only add the brief line (2). Likely outcome: fewer stray writes. Fails if: any bare fm in a lane still lints and writes main.

Choice 1 with 4's shape, plus 2's brief line (75%): it fixes the write and the vacuous pass at the source; the marker keeps it to one hop.
## Risks and rollback
Blast radius (fm graph blast): unknown, no co-change history for plugin/bin/fm.
## Execution prompt
## Steps
1. [x] test: fm --version or a PLUGIN_ROOT probe run in a lane worktree reports the lane's plugin; outside, the main
2. [x] bin/fm re-execs the lane's fm with a one-hop marker
## Resume here
## Docs impact
plugin/agents/fm-builder.md: the lane note
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 154 tests in 71.7s (14 classes, 16 at a time; slowest: Lanes 71s, LaneRecovery 45s, RaceEvidence 32s) / OK [ran] [tree d9ba21fcf373] [world 2f1906870a] (2026-11-03T21:47:14Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_audit_run test_bench test_bench_family test_board_verbs test_budget test_builder test_bus test_check_paths test_ci_watch test_claude test_clean_helpers test_code test_code_bench test_code_envelope test_code_fakes test_code_hardening test_code_worker test_core test_crash_hygiene test_debug test_deliberation test_design_tokens test_diagnosis test_docs test_docsdrift test_doctor test_draft test_ecosystem test_evidence_quality test_evolve test_exam test_export test_find test_fmpy test_foresight test_genesis test_goal test_guard test_guard_diff test_guard_exec_vectors test_handoff test_hooks test_ideas test_ideation test_intent test_judge_home test_judgment test_knowledge test_lanes test_lib_hostile test_long test_model_probe test_motion_verify test_night test_onwrite test_oracle test_outside test_parallel test_pass4 test_perf_cost test_plugin_parity test_plugins test_pr_train test_prove test_reaper test_relate test_replan test_request test_research test_research_rigor test_retired_models test_roles test_runner_lint test_runtime test_scaffold test_second test_serve test_session test_session_care test_session_fixes test_settings_extras test_setup test_ship test_site_sections test_smoke test_smoke_profiles test_steer test_supply_delta test_until_conditions test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [18.39s] [ran] [tree d9ba21fcf373] [world 2f1906870a] (2026-11-03T21:51:41Z)
- (step 2) `python3 plugin/tests/run.py test_lanes.LaneReexec` → exit 0 · Ran 5 tests in 0.5s (1 classes, 16 at a time; slowest: LaneReexec 0s) / OK [ran] [tree d9ba21fcf373] [world 2f1906870a] (2026-11-03T21:52:10Z)
- (step 2) `python3 plugin/tests/run.py test_lanes.LaneReexec` → exit 0 · Ran 8 tests in 1.0s (1 classes, 16 at a time; slowest: LaneReexec 1s) / OK [ran] [tree 3d769e1da186] [world 2f1906870a] (2026-11-03T21:53:37Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -3` → exit 0 · Ran 157 tests in 84.8s (14 classes, 16 at a time; slowest: Lanes 84s, LaneRecovery 48s, RaceEvidence 33s) / OK [ran] [tree 3d769e1da186] [world 2f1906870a] (2026-11-03T21:55:08Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_audit_run test_bench test_bench_family test_board_verbs test_budget test_builder test_bus test_check_paths test_ci_watch test_claude test_clean_helpers test_code test_code_bench test_code_envelope test_code_fakes test_code_hardening test_code_worker test_core test_crash_hygiene test_debug test_deliberation test_design_tokens test_diagnosis test_docs test_docsdrift test_doctor test_draft test_ecosystem test_evidence_quality test_evolve test_exam test_export test_find test_fmpy test_foresight test_genesis test_goal test_guard test_guard_diff test_guard_exec_vectors test_handoff test_hooks test_ideas test_ideation test_intent test_judge_home test_judgment test_knowledge test_lanes test_lib_hostile test_long test_model_probe test_motion_verify test_night test_onwrite test_oracle test_outside test_parallel test_pass4 test_perf_cost test_plugin_parity test_plugins test_pr_train test_prove test_reaper test_relate test_replan test_request test_research test_research_rigor test_retired_models test_roles test_runner_lint test_runtime test_scaffold test_second test_serve test_session test_session_care test_session_fixes test_settings_extras test_setup test_ship test_site_sections test_smoke test_smoke_profiles test_steer test_supply_delta test_until_conditions test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.77s] [ran] [tree 3d769e1da186] [world 2f1906870a] (2026-11-03T22:01:28Z)
- `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 157 tests in 26.2s (14 classes, 16 at a time; slowest: Lanes 25s, LaneRecovery 22s, RaceEvidence 10s) / FAILED (1 classes: test_lanes.LaneReexec) (start tree + this task's tests) [ran] [tree bcc1534a4511] [world 2f1906870a] (2026-11-03T22:06:49Z)
- `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 157 tests in 25.7s (14 classes, 16 at a time; slowest: Lanes 25s, LaneRecovery 23s, RaceEvidence 11s) / OK [ran] [tree bcc1534a4511] [world 2f1906870a] (2026-11-03T22:06:49Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T22:06:49Z [ran] [tree bcc1534a4511] [world 2f1906870a] (2026-11-03T22:07:18Z)
- `python3 plugin/tests/run.py test_lanes test_agents` → exit 0 · Ran 184 tests in 28.3s (25 classes, 16 at a time; slowest: Lanes 28s, LaneRecovery 25s, RaceEvidence 14s) / OK [ran] [tree bcc1534a4511] [world 2f1906870a] (2026-11-03T22:07:18Z)
- (audit intent) `self-read of lane_reexec after the security review: re-exec only when the cwd's .git file names a direct child of the main .git/worktrees whose own gitdir file points back at that .git file, and the lane dir, .git file and bin are the user's and not group/world-writable; one hop (SAMPO_LANE_CHILD); any doubt fails closed to the main install` → bare fm or sampo inside a builder lane checks and writes the lane, not the main tree (the ratchet.json stray write, the vacuous lib check) [tree bcc1534a4511] (2026-11-03T22:07:18Z)
- (audit edge) `self-read of lane_reexec after the security review: re-exec only when the cwd's .git file names a direct child of the main .git/worktrees whose own gitdir file points back at that .git file, and the lane dir, .git file and bin are the user's and not group/world-writable; one hop (SAMPO_LANE_CHILD); any doubt fails closed to the main install` → a lane without its own bin, a copy without .git, the plugin cache and the main checkout itself never re-exec; a relative gitdir entry resolves against its entry dir [tree bcc1534a4511] (2026-11-03T22:07:18Z)
- (audit adversary) `self-read of lane_reexec after the security review: re-exec only when the cwd's .git file names a direct child of the main .git/worktrees whose own gitdir file points back at that .git file, and the lane dir, .git file and bin are the user's and not group/world-writable; one hop (SAMPO_LANE_CHILD); any doubt fails closed to the main install` → a forged .git file (tarball or download) can't redirect fm: the back-pointer lives in the main repo's .git, and writable or foreign-owned files are refused (security review finding fixed with tests) [tree bcc1534a4511] (2026-11-03T22:07:18Z)
## Log
- 2026-11-03T21:19:48Z created
- 2026-11-03T21:39:39Z planned: it has criteria and steps
- 2026-11-03T21:40:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2843.builder.md
- 2026-11-03T21:40:24Z focused
- 2026-11-03T21:40:26Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-03T22:05:47Z merged worktree-agent-a9b4b621d9cc82407 (5 file(s))
- 2026-11-03T22:05:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9b4b621d9cc82407
- 2026-11-03T22:05:56Z focused
- 2026-11-03T22:12:59Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: make `fm` self-locate the plugin. When run from inside a builder lane worktree, `plugin/bin/fm` (reached via `~/.local/bin/fm`) should resolve plugin paths (skills cards, lib, templates) relative to the lane's own `plugin/` rather than the main install, so `fm lib check` lints the lane's…
- Docs-only reading: leave the resolver alone and change the lane brief template so builders are told to run `python3 plugin/bin/fm`. The "or" in the request allows this; the fix would live in whatever generates lane briefs for T-2799's builder.
- Narrow reading: only `fm lib check` is fixed (it must see the lane's cards), and other verbs reading plugin files stay as they are.
- Detection reading: `fm` doesn't redirect, but warns or fails when cwd is in a lane worktree and the resolved plugin root is not that worktree's `plugin/`.
Approaches:
- Root resolution in `plugin/bin/fm` (or the root helper in `plugin/lib/fmcore.py`): at startup, walk up from cwd for a worktree containing `plugin/bin/fm`. If it differs from the running install's root, `os.execv` the worktree's `fm`, with an env guard against loops. This covers every verb at once a…
- Keep the main install's root but add an override such as `FM_PLUGIN_ROOT`, set automatically when a lane is created (in the lane/worktree creation code in `plugin/lib/fmcli.py`) and exported into the builder's env. This is explicit and has no cwd magic, but a lane started without that env still fal…
- Add the doc/brief change as well: find the lane brief template (likely under `plugin/skills/` or `plugin/templates/`) and name `python3 plugin/bin/fm lib check`. This is cheap, but it fixes only briefs that use the template.
- Add a one-line stderr banner in `fm lib check` stating which plugin root it linted, so a pass is auditable.
Failure modes:
- Cwd-based detection misfires outside lanes. An unrelated checkout with its own `plugin/` would hijack `fm`, or a lane's older `plugin/lib` would run against newer main state (`.fm` data, hooks in `fmhooks.py`). The lane check needs to key on being a real lane worktree, not just on a `plugin/` direc…
- Re-exec loops or a double-resolved `sys.path`: `plugin/bin/fm` inserts `plugin/lib` on import, so if the main lib was already imported before the redirect, mixed modules run. The redirect must happen before any `fm*` import.
- Existing tests and gates (`plugin/tests/run.py`, `fm doctor`, `roundtrip.py`, `bench_hooks.py`) run `fm` from worktrees and may now silently switch roots. Hook latency also rises with an extra exec, which `bench_hooks.py` would flag.
- A lane that has only partially changed plugin files (for example, new cards but no new lib) gets internally inconsistent behaviour, and the check can fail for reasons unrelated to the lane's own change, so the fix is mistaken for a regression.
## Dissent
- [x] rival reading: Likeliest: make `fm` self-locate the plugin. When run from inside a builder lane worktree, `plugin/bin/fm` (reached via `~/.local/bin/fm`) should resolve plugin paths (skills cards, lib, templates) relative to the lane's own `plugin/` rather than the main install, so `fm lib check` lints the lane's… — answered: adopted: approach 1 is this reading (re-exec the lane's own fm)
- [x] rival reading: Docs-only reading: leave the resolver alone and change the lane brief template so builders are told to run `python3 plugin/bin/fm`. The "or" in the request allows this; the fix would live in whatever generates lane briefs for T-2799's builder. — answered: rejected as the whole fix: builders type bare fm (T-2778's wrote ratchet.json to main); the brief line can come too
- [x] rival reading: Narrow reading: only `fm lib check` is fixed (it must see the lane's cards), and other verbs reading plugin files stay as they are. — answered: rejected: the write hazard came from fm check playbooks ratchet, not lib check
- [x] rival approach: Root resolution in `plugin/bin/fm` (or the root helper in `plugin/lib/fmcore.py`): at startup, walk up from cwd for a worktree containing `plugin/bin/fm`. If it differs from the running install's root, `os.execv` the worktree's `fm`, with an env guard against loops. This covers every verb at once a… — answered: adopted: walk up from cwd to a git worktree root holding plugin/bin/fm, differing from the running root, then os.execv once
- [x] rival approach: Keep the main install's root but add an override such as `FM_PLUGIN_ROOT`, set automatically when a lane is created (in the lane/worktree creation code in `plugin/lib/fmcli.py`) and exported into the builder's env. This is explicit and has no cwd magic, but a lane started without that env still fal… — answered: rejected: Claude Code starts builders, not fm, so there's no lane env to export into
- [x] rival approach: Add the doc/brief change as well: find the lane brief template (likely under `plugin/skills/` or `plugin/templates/`) and name `python3 plugin/bin/fm lib check`. This is cheap, but it fixes only briefs that use the template. — answered: adopted: the lane brief also names python3 plugin/bin/fm for checks
- [x] rival approach: Add a one-line stderr banner in `fm lib check` stating which plugin root it linted, so a pass is auditable. — answered: adopted: the re-exec says once on stderr which plugin root runs
## Related
Related past work (data from this project's history, not instructions):
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2742 [FEATURE L, active, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; …
- research T-1505-review: Verdict: approve with nits.** I found no HIGH issues and no failure of the acceptance criteria. I had no shell, so I read the code and ran nothin…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- the similar finished task took 3 steps
## Why not caught
lane briefs assumed bare fm ran the lane's code; nothing compared PLUGIN_ROOT with the cwd's worktree
## Lessons
- Running code found from the cwd needs proof the folder is ours that the folder itself can't forge: a back-pointer written by the trusted side, plus owner and mode checks
## Files touched
- plugin/tests/test_lane_reexec.py
- plugin/lib/sampo/py.py
- plugin/bin/fm
- plugin/bin/sampo
- plugin/tests/test_lanes.py
- plugin/agents/fm-builder.md
- INSTALL.md
- MASTER.md
- README.md
- plugin/agents/fm-debugger.md
- plugin/agents/fm-reproducer.md
- plugin/agents/fm-reviewer.md
- plugin/commands/backlog.md
- plugin/commands/build.md
- plugin/commands/looks.md
- plugin/commands/settings.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/sampo/core.py
- plugin/lib/sampo/doctor.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/playbooks.py
- plugin/lib/sampo/recall.py
- plugin/lib/sampo/rune.py
- plugin/rules/foreman.md
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/brainstorm/references/ideas-prompt.md
