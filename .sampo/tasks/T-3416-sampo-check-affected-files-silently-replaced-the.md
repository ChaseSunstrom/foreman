---
id: T-3416
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T09:08:54Z
updated: 2026-11-07T00:42:15Z
lane: ~/.claude/foreman/.claude/worktrees/agent-afec3ab52b3885cca
lane_branch: worktree-agent-afec3ab52b3885cca
base: e82c630e4a99732132ef271c31a6f9b466c2aad3
base_tree: bf5e00c5c771552d134d9e2a4a9b417c76bb92ea
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T09:12:37Z
plan0_scope: []
builder_returned: 2026-11-06T09:44:24Z
lane_passed: {"tree": "1d2552de7b729fc34faa5e73e052881985e5aefb", "cmds": ["python3 plugin/tests/run.py test_cli -k test_affected_template_needs", "python3 plugin/tests/run.py test_cli -k test_lane_cannot_change"]}
---
# 'sampo check affected <files>' silently replaced the project's affected-tests template…
## Raw request
> FIX: 'sampo check affected <files>' silently replaced the project's affected-tests template with 'plugin/lib/sampo/louhi.py plugin/tests/test_exam.py' (a lane builder meant 'check --affected'), so every lane's affected check ran louhi.py as a program (exit 126) for ~20 min. Refuse a template with no {tests}/{names} placeholder (hint: did you mean sampo check --affected?), refuse template and gate changes from a lane (project config is the main session's), and log every template change as an event with the old value
## Interpretation
Reading 1: guard the setter (placeholder, lane, log). Reading 2: remove the verb's setter form entirely; ruled out, tests and docs use it.
## Assumptions (confidence)
## Acceptance criteria
- [ ] Template without placeholder refused, change logged — verify with `python3 plugin/tests/run.py test_cli -k test_affected_template_needs`
- [ ] Lane cannot change gates — verify with `python3 plugin/tests/run.py test_cli -k test_lane_cannot_change`
## Non-goals
## Approach (options → choice → why)
1) use what exists: guards in the setter branch (likely outcome: small, works; fails if a lane test can't fake a lane). 2) a separate set verb (fails if callers break). 3) do less: only the placeholder check (likely outcome: lane edits still unlogged). Choice 1 (80%): smallest diff covering all.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests, guards, help
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli -k test_affected_template_needs -k test_lane_cannot_change` → exit 0 · Ran 2 tests in 3.3s (1 jobs, 16 at a time; slowest: Checks 0s) / OK [ran] [tree ee8c1ce9d850] [world 2f1906870a] (2026-11-06T09:13:11Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [23.84s] [ran] [tree ee8c1ce9d850] [world 2f1906870a] (2026-11-06T09:16:47Z)
- (step 1) `python3 plugin/tests/run.py test_cli -k test_affected_template_needs -k test_lane_cannot_change -k per_extension` → exit 0 · Ran 2 tests in 239.6s (2 jobs, 16 at a time; slowest: Checks.test_lane_cannot_change_project_gates 1s, Checks.test_affected_template_needs_a_placeholder_and_is_logged 1s) / OK [ran] [tree 1d2552de7b72] [world 2f1906870a] (2026-11-06T09:35:31Z)
- (step 1) `python3 plugin/tests/run.py test_cli -k test_each_test_extension_gets_its_own_runner` → exit 0 · Ran 1 tests in 348.6s (1 jobs, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 1d2552de7b72] [world 2f1906870a] (2026-11-06T09:41:36Z)
## Log
- 2026-11-06T09:08:54Z created
- 2026-11-06T09:12:25Z planned: it has criteria and steps
- 2026-11-06T09:12:32Z criterion 1 verify: `python3 plugin/tests/run.py test_cli.Checks.test_affected_template_needs_a_placeholder_and_is_logged` → `python3 plugin/tests/run.py test_cli -k test_affected_template_needs`
- 2026-11-06T09:12:32Z criterion 2 verify: `python3 plugin/tests/run.py test_cli.Checks.test_lane_cannot_change_project_gates` → `python3 plugin/tests/run.py test_cli -k test_lane_cannot_change`
- 2026-11-06T09:12:36Z focused
- 2026-11-06T09:12:37Z predicted from its closes: 8 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-05: [costly] T-3219: the standing core yes now passes self-change gate holds made only of footprint, verb-count or hook-speed rows, per the user's 'I sa…
