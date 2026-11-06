---
id: T-3369
type: CLEAN
tier: S
status: planned
priority: normal
scope: [install.sh, INSTALL.md, MASTER.md, README.md, site/stats.py, plugin/tests/test_install.py]
depends_on: []
source: followup
created: 2026-11-06T06:03:46Z
updated: 2026-11-06T06:48:28Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a185619b5690dd96e
lane_branch: worktree-agent-a185619b5690dd96e
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T06:19:47Z
plan0_scope: [install.sh, INSTALL.md, MASTER.md, README.md, site/stats.py, plugin/tests/test_install.py]
builder_returned: 2026-11-06T06:48:28Z
---
# Install and docs read SAMPO_* first: install.sh reads only FOREMAN_* (install.sh:19-26) while the code already reads SAMPO_* (core.py:68); docs name FOREMAN_HOME x40, REPO x8, DESKTOP_REPO x6, QUIET x2, NO_BACKGROUND x1 (INSTALL.md, MASTER.md, README.md, install.sh, site/stats.py): say SAMPO_* with FOREMAN_* as the old alias
## Raw request
> Install and docs read SAMPO_* first: install.sh reads only FOREMAN_* (install.sh:19-26) while the code already reads SAMPO_* (core.py:68); docs name FOREMAN_HOME x40, REPO x8, DESKTOP_REPO x6, QUIET x2, NO_BACKGROUND x1 (INSTALL.md, MASTER.md, README.md, install.sh, site/stats.py): say SAMPO_* with FOREMAN_* as the old alias
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] install.sh honours SAMPO_HOME (FOREMAN_HOME still works) and the docs name SAMPO_* first — verify with `python3 plugin/tests/run.py test_install test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] install.sh reads both; docs
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_install test_docs` → ✗ exit 1 · Ran 125 tests in 222.1s (33 jobs, 16 at a time; slowest: Fences 10s, DocsProof 3s, TaskLifecycle 2s) / FAILED (1 classes: test_install.InstallEnv) (ran] (tree 93960d94a860] (world 2f1906870a] (2026-11-06T06:24:31Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_install.py` → exit 0 · Ran 4 tests in 0.265s / OK (ran] (tree 33ba073618ac] (world 2f1906870a] (2026-11-06T06:31:07Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_board_surfaces test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_install test_left_out test_map test_mcp test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 124 (timed out after 893.646s) · timed out after 893.646s (ran] (tree bb5b8e2935b9] (world 2f1906870a] (2026-11-06T06:46:04Z)
## Log
- 2026-11-06T06:03:46Z created
- 2026-11-06T06:19:46Z focused
- 2026-11-06T06:19:47Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T06:25:40Z focused
- 2026-11-06T06:30:56Z focused
- 2026-11-06T06:42:25Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint.py, plugin/tests/test_docs.py, plugin/tests/test_fmpy.p…
