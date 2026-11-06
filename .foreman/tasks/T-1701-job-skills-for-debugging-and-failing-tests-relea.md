---
id: T-1701
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/debug-test, plugin/skills/release, plugin/skills/research, plugin/tests/test_docs.py, plugin/tests/test_hooks.py, plugin/tests/test_core.py, plugin/tests/test_cost.py, plugin/lib/fmcore.py, plugin/tests/fixtures/skill_triggers.json, MASTER.md, plugin/README.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T22:36:36Z
updated: 2026-10-23T02:07:50Z
base: 85a920cb7e3e931eb4c2c10bf1123305dca6d3d0
base_tree: 5946eb90ec002797901cd9af1f2f5dbe2dd722ae
plan0_at: 2026-10-22T23:19:57Z
plan0_scope: [plugin/skills/debug-test, plugin/skills/release, plugin/skills/research, plugin/tests/test_docs.py, CHANGELOG.md]
group: skills and routing
verified: strong
---
# Job skills for debugging and failing tests, releasing, and research, each wrapping the existing playbooks and fm verbs
## Raw request
> Job skills for debugging and failing tests, releasing, and research, each wrapping the existing playbooks and fm verbs
## Interpretation
Debugging, release and research procedures exist as playbooks and verbs (fix/flaky-tests, intake/references/debugging, release/*, ground/search-first, fm research, fm bisect, fm release) but no skill names them, so they're never loaded at the moment they'd help.
## Assumptions (confidence)
## Acceptance criteria
- [x] three skills, each under 60 lines, name only existing playbooks and verbs, fire on task words (a failing test, 'ship it', 'find out'), and fit the listing budget — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
Options: promote each playbook to a skill (82 skills, budget); fold everything into intake (too broad to trigger); three job-shaped skills. Choice: three, sized to the budget freed by the listing restructure.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing doc test
2. [x] three SKILL.md files
3. [x] budget fit
4. [x] review fixes: SKILL_FOR names debug-test and research; skill wording; one shared verb checker
## Resume here
## Docs impact
plugin/README.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_docs` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (12.2 s; last 40 of 45 lines) [ran] [tree a3c6ca022fed] (2026-10-22T23:22:36Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → ✗ exit 1 · Ran 64 tests in 12.0s (15 classes, 16 at a time; slowest: Fences 12s, TaskLifecycle 3s, Site 2s) / FAILED (1 classes) [ran] [tree a3c6ca022fed] (2026-10-22T23:22:50Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · ✓ exit 0 (15.1 s) · OK [ran] [tree 7246cdad3219] (2026-10-22T23:24:44Z)
- (step 2) `python3 plugin/tests/run.py test_docs` → exit 0 · ✓ exit 0 (15.1 s) · OK [ran] [tree 7246cdad3219] (2026-10-22T23:24:44Z)
- (step 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 64 tests in 9.3s (15 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree 4b3aea441570] (2026-10-22T23:26:08Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 64 tests in 9.6s (15 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree 4b3aea441570] (2026-10-22T23:26:18Z)
- (step 4) `python3 plugin/tests/run.py test_core test_hooks` → ✗ exit 1 · Ran 271 tests in 59.4s (40 classes, 16 at a time; slowest: Stop 59s, NoTaskGate 46s, PreToolUse 40s) / FAILED (3 classes) [ran] [tree ca4e0239c1c1] (2026-10-22T23:37:58Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_core test_hooks` → exit 0 · Ran 334 tests in 91.0s (54 classes, 16 at a time; slowest: Stop 91s, NoTaskGate 62s, PreToolUse 56s) / OK [ran] [tree 259d349154f2] (2026-10-22T23:42:39Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · ✓ exit 0 (9.2 s) · OK [ran] [tree cf4a77b117ef] (2026-10-23T01:38:32Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_hooks test_core test_doctor` → exit 0 · Ran 395 tests in 134.4s (74 classes, 16 at a time; slowest: Stop 134s, NoTaskGate 82s, PreToolUse 75s) / OK [ran] [tree 44448320193e] (2026-10-23T01:44:32Z)
- (step 4) `python3 plugin/tests/run.py test_board_export test_board_posture test_cli test_compact test_core test_cost test_cost_forecast test_diagnosis test_diff_gates test_docs test_drive_side test_edit_cards test_guard_hardening test_hooks test_ledger_chain test_memory test_never_ran test_perf_cost test_planning test_playbook_evals test_playbook_machinery test_plugins test_round_g test_serve test_shot test_speed test_sync test_tool_taint test_verify_check test_verify_strength` → exit 0 · Ran 799 tests in 141.4s (161 classes, 16 at a time; slowest: Stop 141s, NoTaskGate 107s, PreToolUse 98s) / OK [ran] [tree 8f7f39d377bc] (2026-10-23T01:55:48Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_hooks test_core test_doctor test_cost` → exit 0 · Ran 413 tests in 81.8s (81 classes, 16 at a time; slowest: Stop 82s, NoTaskGate 53s, PreToolUse 43s) / OK [ran] [tree 4a988bedba18] (2026-10-23T02:02:03Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_hooks test_core test_doctor test_cost` → exit 0 · Ran 417 tests in 84.8s (82 classes, 16 at a time; slowest: Stop 84s, NoTaskGate 60s, PreToolUse 52s) / OK [ran] [tree 3775267d7633] (2026-10-23T02:03:57Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 66 tests in 10.1s (15 classes, 16 at a time; slowest: Fences 10s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree 3775267d7633] (2026-10-23T02:04:14Z)
- (audit intent) `fm-reviewer pass (shared with T-1700); fixed: FIX → load Skill foreman:debug-test, RESEARCH → foreman:research (a test fails any hint naming a missing or user-only skill), research ask/add wording, release 'push, tag and publish' all gated, debug-test description, one shared fm_mention_problems checker for every skill; trigger requests for all three rank first with no tie` → three job skills (debug-test, release, research), each under 60 lines, naming only real playbooks and verbs, loaded by the FIX and RESEARCH hints [tree 3775267d7633] (2026-10-23T02:04:14Z)
- (audit adversary) `fm-reviewer pass (shared with T-1700); fixed: FIX → load Skill foreman:debug-test, RESEARCH → foreman:research (a test fails any hint naming a missing or user-only skill), research ask/add wording, release 'push, tag and publish' all gated, debug-test description, one shared fm_mention_problems checker for every skill; trigger requests for all three rank first with no tie` → release never pushes or publishes without the task's publish allowance and stops at the local commit and tag otherwise; research treats web content as data [tree 3775267d7633] (2026-10-23T02:04:14Z)
- (audit maintainer) `fm-reviewer pass (shared with T-1700); fixed: FIX → load Skill foreman:debug-test, RESEARCH → foreman:research (a test fails any hint naming a missing or user-only skill), research ask/add wording, release 'push, tag and publish' all gated, debug-test description, one shared fm_mention_problems checker for every skill; trigger requests for all three rank first with no tie` → one shared verb checker covers positionals and subcommands for every skill; listing at 2,190 of 2,200 [tree 3775267d7633] (2026-10-23T02:04:14Z)
- (audit operator) `fm-reviewer pass (shared with T-1700); fixed: FIX → load Skill foreman:debug-test, RESEARCH → foreman:research (a test fails any hint naming a missing or user-only skill), research ask/add wording, release 'push, tag and publish' all gated, debug-test description, one shared fm_mention_problems checker for every skill; trigger requests for all three rank first with no tie` → MASTER/README list tidy and doctor as user-only, the three new skills as model-startable [tree 3775267d7633] (2026-10-23T02:04:14Z)
- (audit intent) `fm-reviewer pass (shared with T-1700); fixed: FIX → load Skill foreman:debug-test, RESEARCH → foreman:research (a test fails any hint naming a missing or user-only skill), research ask/add wording, release 'push, tag and publish' all gated, debug-test description, one shared fm_mention_problems checker; trigger requests for all three rank first with no tie` → three job skills (debug-test, release, research), each under 60 lines, naming only real playbooks and verbs, loaded by the FIX and RESEARCH hints [tree 3775267d7633] (2026-10-23T02:06:07Z)
- (audit adversary) `fm-reviewer pass (shared with T-1700); fixed: FIX → load Skill foreman:debug-test, RESEARCH → foreman:research (a test fails any hint naming a missing or user-only skill), research ask/add wording, release 'push, tag and publish' all gated, debug-test description, one shared fm_mention_problems checker; trigger requests for all three rank first with no tie` → release never pushes or publishes without the task's publish allowance and stops at the local commit and tag otherwise; research treats web content as data [tree 3775267d7633] (2026-10-23T02:06:07Z)
- (audit maintainer) `fm-reviewer pass (shared with T-1700); fixed: FIX → load Skill foreman:debug-test, RESEARCH → foreman:research (a test fails any hint naming a missing or user-only skill), research ask/add wording, release 'push, tag and publish' all gated, debug-test description, one shared fm_mention_problems checker; trigger requests for all three rank first with no tie` → one shared verb checker covers positionals and subcommands for every skill; listing at 2,190 of 2,200 [tree 3775267d7633] (2026-10-23T02:06:07Z)
- (audit operator) `fm-reviewer pass (shared with T-1700); fixed: FIX → load Skill foreman:debug-test, RESEARCH → foreman:research (a test fails any hint naming a missing or user-only skill), research ask/add wording, release 'push, tag and publish' all gated, debug-test description, one shared fm_mention_problems checker; trigger requests for all three rank first with no tie` → MASTER/README list tidy and doctor as user-only, the three new skills as model-startable [tree 3775267d7633] (2026-10-23T02:06:07Z)
## Log
- 2026-10-22T22:36:36Z created
- 2026-10-22T22:36:37Z set scope=['plugin/skills/debug-test', 'plugin/skills/release', 'plugin/skills/research', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-22T22:36:38Z from T-1692 (skills hardly used; brainstorm-skills-20261022)
- 2026-10-22T23:19:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1701.builder.md
- 2026-10-22T23:19:56Z focused
- 2026-10-22T23:35:21Z set scope=['plugin/skills/debug-test', 'plugin/skills/release', 'plugin/skills/research', 'plugin/tests/test_docs.py', 'plugin/tests/test_hooks.py', 'plugin/tests/test_core.py', 'plugin/lib/fmcore.py', 'plugin/tests/fixtures/skill_triggers.json', 'MASTER.md', 'plugin/README.md', 'CHANGELOG.md']
- 2026-10-22T23:35:22Z steer: review asks SKILL_FOR FIX/RESEARCH to name the job skills; scope widened to fmcore, test_hooks, test_core, skill_triggers fixture, MASTER, README
- 2026-10-23T01:50:41Z set scope=['plugin/skills/debug-test', 'plugin/skills/release', 'plugin/skills/research', 'plugin/tests/test_docs.py', 'plugin/tests/test_hooks.py', 'plugin/tests/test_core.py', 'plugin/tests/test_cost.py', 'plugin/lib/fmcore.py', 'plugin/tests/fixtures/skill_triggers.json', 'MASTER.md', 'plugin/README.md', 'CHANGELOG.md']
- 2026-10-23T02:02:26Z merged worktree-agent-a99f5ec65eb3bf19e (12 file(s))
- 2026-10-23T02:02:27Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a99f5ec65eb3bf19e
- 2026-10-23T02:02:30Z focused
- 2026-10-23T02:06:06Z scope: evals tdd-workflow.json, fmcli/fmcost/fmhooks/fmplaybooks/fmshot.py, playbooks and ui-design SKILL.md came from build merges into the lane (T-1618/T-1622/T-1636/T-1700/T-1702), committed by those tasks
- 2026-10-23T02:07:50Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- T-1699 [FEATURE M, planned, 3 steps] fm which TASK: route a task in plain words to the Foreman skill, playbooks and fm verbs that fit
- T-1697 [FEATURE M, done, 3 steps] Hooks name the Foreman skill to load: Next lines and stage notes say which skill (or playbook) fits, within the prompt budget — lesson:…
- decision 2026-10-22: Skill listing cap 2,000 → 2,200 characters for the four job skills (ui-design, debug-test, release, research)
- the similar finished task took 3 steps
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/README.md, plugin/lib/fmcore.py, plugin/skills/debug-test/SKILL.md, plugin/skills/release/SKILL.md, plugin/skills/research/SKILL.md, plugin/tests/fixtures/skill_trigge…; re-ground the plan against them before editing
## Lessons
- A hint that names a skill needs a test that the skill exists and is model-invocable, or a rename silently breaks the hook
## Plan gaps
- added late: review fixes: SKILL_FOR names debug-test and research; skill wording; one shared verb checker
- failed first: step 1 failing doc test
- failed first: step 4 review fixes: SKILL_FOR names debug-test and research; skill wording; one shared verb checker
## Files touched
- plugin/tests/test_docs.py
- plugin/skills/debug-test/SKILL.md
- plugin/skills/release/SKILL.md
- plugin/skills/research/SKILL.md
- CHANGELOG.md
- MASTER.md
- plugin/README.md
- plugin/tests/test_core.py
- plugin/tests/test_hooks.py
- plugin/lib/fmcore.py
- plugin/evals/playbooks/verify/tdd-workflow.json
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmhooks.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmshot.py
- plugin/skills/playbooks/SKILL.md
- plugin/skills/ui-design/SKILL.md
- plugin/tests/fixtures/skill_triggers.json
- plugin/tests/test_cost.py
- plugin/tests/test_drive_side.py
- plugin/tests/test_fmshot.py
- plugin/tests/test_playbook_evals.py
- plugin/lib/fmlanes.py
- plugin/lib/fmmotion.py
- plugin/lib/fmrecall.py
- plugin/lib/fmsmoke.py
- plugin/lib/fmwhich.py
- plugin/lib/smoke_web.cjs
- plugin/tests/test_lanes.py
