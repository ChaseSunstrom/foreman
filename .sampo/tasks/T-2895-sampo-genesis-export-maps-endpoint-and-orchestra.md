---
id: T-2895
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/rune.py, plugin/lib/sampo/models.py, site/build.py, site/genesis/genesis.js, plugin/tests/test_genesis.py, plugin/tests/test_site_build.py, plugin/tests/genesis_page.js]
depends_on: []
source: discovered
created: 2026-11-04T04:53:03Z
updated: 2026-11-06T10:20:52Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a88d1c43d130a83c5
lane_branch: worktree-agent-a88d1c43d130a83c5
base: 9d9fa0fbb24df1b029200903120bfec2db40d1de
base_tree: 99dd50385e0908d624cbfe75a56d634f010a38bb
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T09:34:04Z
plan0_scope: [plugin/lib/sampo/rune.py, site/build.py, site/genesis/genesis.js, plugin/tests/test_genesis.py, plugin/tests/test_site_build.py]
builder_returned: 2026-11-06T10:20:52Z
---
# sampo genesis export writes each model as its role in the data (from its profile, not its name), so the site pages drop their 'jarvis' word swaps and a repo named jarvis stays itself
## Raw request
> FIX: sampo genesis export maps endpoint and orchestrator names to roles in the data itself, telling a profile name from a repo of the same name, so the pages need no word swap
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] rune.export replaces each model field (a profile name such as jarvis-nothink) with its role from the profile (own or loopback large model: 'a large local model', loopback small: 'a local model', cloud: its family) and the orchestrator with 'the agent', field by field, never by a word match; a repo or project field named jarvis is kept; site/build.py's and genesis.js's jarvis regex swaps are removed and the pages read the same — verify with `python3 plugin/tests/run.py test_genesis test_site_build`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests: an export with a jarvis-nothink model field and a 'jarvis (1,853)' repo field: the first becomes its role, the second stays; the pages need no swap  <- CURRENT
2. [x] the role map in export, the swaps removed from build.py:573 and genesis.js:89
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisExport.test_export_writes_each_model_as_its_role_from_its_profile_and_keeps_a_repo_of_the_same_name` → ✗ exit 1 · Ran 1 tests in 60.4s (1 jobs, 16 at a time; slowest: GenesisExport 1s) / FAILED (1 classes: test_genesis.GenesisExport) [ran] [tree 14a3f2926951] [world 2f1906870a] (2026-11-06T09:35:30Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisExport.test_export_writes_each_model_as_its_role_from_its_profile_and_keeps_a_repo_of_the_same_name 2>&1 | tail -15` → exit 0 · Ran 1 tests in 168.5s (1 jobs, 16 at a time; slowest: GenesisExport 0s) / OK [ran] [tree 84931be1328a] [world 2f1906870a] (2026-11-06T09:41:41Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisExport test_site_build` → exit 0 · Ran 39 tests in 374.6s (14 jobs, 16 at a time; slowest: CardsPage 16s, GenesisExport 12s, Landing 11s) / OK [ran] [tree 84931be1328a] [world 2f1906870a] (2026-11-06T09:42:40Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_code_hardening test_code_worker test_ctx_variant test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1181 tests in 338.1s (303 jobs, 16 at a time; slowest: Ship 30s, CardsPage 14s, ProofBeforePresentation 14s) / FAILED (1 classes: test_site_sections.Built) [ran] [tree 84931be1328a] [world 2f1906870a] (2026-11-06T09:49:19Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisExport test_models` → exit 0 · Ran 100 tests in 11.1s (16 jobs, 16 at a time; slowest: GenesisExport 8s, Bench 3s, RunRoute 1s) / OK [ran] [tree 86cf1cf8d8d0] [world 2f1906870a] (2026-11-06T10:04:25Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_code_hardening test_code_worker test_ctx_variant test_design_gates test_design_lint test_design_sprint test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 1181 tests in 274.5s (364 jobs, 16 at a time; slowest: GenerationReview 15s, CardsPage 13s, CityBrowser 13s) / FAILED (1 classes: test_steer.Page) [ran] [tree 86cf1cf8d8d0] [world 2f1906870a] (2026-11-06T10:09:11Z)
## Log
- 2026-11-04T04:53:03Z created
- 2026-11-05T03:32:31Z planned from capture
- 2026-11-05T03:32:31Z set approved=True
- 2026-11-05T03:32:31Z set scope=['plugin/lib/sampo/rune.py', 'site/build.py', 'site/genesis/genesis.js', 'plugin/tests/test_genesis.py', 'plugin/tests/test_site_build.py']
- 2026-11-05T03:32:31Z blocked: approved; waits for a builder slot
- 2026-11-06T03:53:11Z unblocked
- 2026-11-06T09:34:02Z focused
- 2026-11-06T09:34:04Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T09:35:55Z set scope=['plugin/lib/sampo/rune.py', 'plugin/lib/sampo/models.py', 'site/build.py', 'site/genesis/genesis.js', 'plugin/tests/test_genesis.py', 'plugin/tests/test_site_build.py', 'plugin/tests/genesis_page.js']
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2889 [FEATURE S, dropped, 0 steps] Treat the orchestrator as a generic, swappable role. "Jarvis" is only the name of an LLM…
- T-2779 [CLEAN M, done, 5 steps] Hook notes and library messages say Sampo (T-2742 step 5a): every user-visible 'Foreman' string in plugin/lib/sampo/*.py, plugin/hooks/co…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint.py, plugin/tests/test_docs.py, plugin/tests/test_fmpy.p…
## Preflight
Changed in scope since this was planned (2026-11-04): plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py, plugin/tests/test_site_build.py, site/build.py, site/genesis/genesis.js; re-ground the plan against them before editing
