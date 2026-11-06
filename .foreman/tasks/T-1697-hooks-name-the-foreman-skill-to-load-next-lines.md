---
id: T-1697
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_hooks.py, CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_core.py, plugin/tests/test_context_tax.py, MASTER.md, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/tests/foreman-ui.test.tsx]
depends_on: []
source: user
created: 2026-10-22T22:36:17Z
updated: 2026-10-22T23:12:19Z
base: 9cf17dcdb1e6361a67abed86ecb26cb027d6dbb0
base_tree: 0a4a6fd57da51e288fab548ff61db67b627d0267
plan0_at: 2026-10-22T22:37:17Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_hooks.py, CHANGELOG.md]
verified: strong
---
# Hooks name the Foreman skill to load: Next lines and stage notes say which skill (or playbook) fits, within the prompt budget
## Raw request
> Hooks name the Foreman skill to load: Next lines and stage notes say which skill (or playbook) fits, within the prompt budget
## Interpretation
Every turn the hooks hand Claude the exact fm command, so it never loads the skill describing the step (30 days: 1 of 13 skills used). A SKILL_FOR map from stage and request words to a skill or playbook adds '(skill foreman:X)' to the Next line and to STAGE_REFERENCE for every stage, not only CLEAN/PERFORMANCE/SECURITY, so the Skill tool gets called at the moment it helps.
## Assumptions (confidence)
## Acceptance criteria
- [x] a design request's prompt note and a FIX/FEATURE stage's Next line name the matching foreman: skill; the injected total stays within PROMPT_BUDGET and the T-1258 byte ratchet — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
Options: always-on long skill hints (context tax every turn); a router the model must remember to call; a short skill name on the Next line and stage notes. Choice: the short name, measured against the byte ratchet; the skill body loads only when the model invokes it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] SKILL_FOR map and Next/stage wiring
3. [x] byte ratchet
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_the_skill_that_fits` → ✗ exit 1 · Ran 1 tests in 6.0s (1 classes, 16 at a time; slowest: UserPromptSubmit 5s) / FAILED (1 classes) [ran] [tree 3e1bbfd877ec] (2026-10-22T22:43:10Z)
- (step 2) `python3 plugin/tests/run.py -k test_the_skill_that_fits -k test_stage_and_next_action_follow_the_brief -k test_next_action_is_injected_every_turn` → exit 0 · Ran 3 tests in 3.6s (2 classes, 16 at a time; slowest: UserPromptSubmit 3s, Stages 0s) / OK [ran] [tree efa5aeb7614e] (2026-10-22T22:47:35Z)
- (step 3) `python3 plugin/tests/run.py -p test_context_tax.py` → exit 0 · Ran 1 tests in 5.0s (1 classes, 16 at a time; slowest: ContextTax 5s) / OK [ran] [tree efa5aeb7614e] (2026-10-22T22:47:45Z)
- (step 1) `python3 plugin/tests/run.py -k test_the_skill_that_fits -k test_a_skill_hint_that_does_not_fit -k test_a_ui_request_names -k test_drive_names_the_skill` → ✗ exit 1 · Ran 4 tests in 4.8s (2 classes, 16 at a time; slowest: UserPromptSubmit 4s, Stop 2s) / FAILED (2 classes) [ran] [tree 6385b5a38279] (2026-10-22T22:57:32Z)
- (step 2) `python3 plugin/tests/run.py -k test_the_skill_that_fits -k test_a_skill_hint_that_does_not_fit -k test_a_ui_request_names -k test_drive_names_the_skill -k test_stage_and_next_action_follow_the_brief -k test_next_action_is_injected_every_turn -k test_unchanged_state` → exit 0 · Ran 7 tests in 12.5s (3 classes, 16 at a time; slowest: UserPromptSubmit 12s, Stop 2s, Stages 0s) / OK [ran] [tree 441cbbd93dc3] (2026-10-22T23:00:40Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 133 tests across 3 files. [25.10s] [ran] [tree 441cbbd93dc3] (2026-10-22T23:01:06Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_core test_context_tax` → exit 0 · Ran 271 tests in 115.9s (41 classes, 16 at a time; slowest: Stop 115s, NoTaskGate 88s, PreToolUse 83s) / OK [ran] [tree e88eff9f13e4] (2026-10-22T23:07:49Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.UserPromptSubmit` → exit 0 · Ran 18 tests in 21.9s (1 classes, 16 at a time; slowest: UserPromptSubmit 22s) / OK [ran] [tree e88eff9f13e4] (2026-10-22T23:08:28Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 201 tests in 87.4s (24 classes, 16 at a time; slowest: Stop 87s, NoTaskGate 60s, PreToolUse 52s) / OK [ran] [tree e88eff9f13e4] (2026-10-22T23:09:56Z)
- (audit intent) `fm-reviewer full pass on the lane; three MEDIUMs fixed test-first (a hint with no room waits instead of being lost; the UI note can't cut the Next line; ui_request no longer matches fm ui / foreman-ui / ui test / redesign … app) plus LOWs (imperative wording, fm next skill field and Stop path tests, dead kit.ts strip removed; foreman-ui mod tests 133 pass)` → each stage's Next line or note names the skill or playbook to load (load: Skill foreman:intake …), once a session, so Claude actually calls the Skill tool; fm next always shows it [tree e88eff9f13e4] (2026-10-22T23:09:56Z)
- (audit edge) `fm-reviewer full pass on the lane; three MEDIUMs fixed test-first (a hint with no room waits instead of being lost; the UI note can't cut the Next line; ui_request no longer matches fm ui / foreman-ui / ui test / redesign … app) plus LOWs (imperative wording, fm next skill field and Stop path tests, dead kit.ts strip removed; foreman-ui mod tests 133 pass)` → a hint that doesn't fit waits for a turn with room; the UI note only goes out when it fits and never cuts the Next command; compaction re-arms hints [tree e88eff9f13e4] (2026-10-22T23:09:56Z)
- (audit adversary) `fm-reviewer full pass on the lane; three MEDIUMs fixed test-first (a hint with no room waits instead of being lost; the UI note can't cut the Next line; ui_request no longer matches fm ui / foreman-ui / ui test / redesign … app) plus LOWs (imperative wording, fm next skill field and Stop path tests, dead kit.ts strip removed; foreman-ui mod tests 133 pass)` → the marker key is a sha1 of constant text and the session id is regex-checked, so prompt text can't steer marker paths [tree e88eff9f13e4] (2026-10-22T23:09:56Z)
- (audit operator) `fm-reviewer full pass on the lane; three MEDIUMs fixed test-first (a hint with no room waits instead of being lost; the UI note can't cut the Next line; ui_request no longer matches fm ui / foreman-ui / ui test / redesign … app) plus LOWs (imperative wording, fm next skill field and Stop path tests, dead kit.ts strip removed; foreman-ui mod tests 133 pass)` → SessionStart 818→852 bytes (cap 1000), prompt replay 397→321; no STAGE_REFERENCE callers left; the foreman-ui mod no longer strips a (procedure:…) that no longer exists [tree e88eff9f13e4] (2026-10-22T23:09:56Z)
## Log
- 2026-10-22T22:36:17Z created
- 2026-10-22T22:36:18Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md']
- 2026-10-22T22:36:22Z from T-1692 (skills hardly used; brainstorm-skills-20261022)
- 2026-10-22T22:37:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1697.builder.md
- 2026-10-22T22:37:16Z focused
- 2026-10-22T22:44:36Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md', 'plugin/lib/fmcli.py']
- 2026-10-22T22:44:36Z scope: plugin/lib/fmcli.py cmd_next — fm next names the skill_for hint, since next_action no longer carries the per-step procedure
- 2026-10-22T22:45:46Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md', 'plugin/lib/fmcli.py', 'plugin/tests/test_core.py', 'plugin/tests/test_context_tax.py']
- 2026-10-22T22:45:47Z scope: test_core.py (FIX's procedure moved from next_action to skill_for) and test_context_tax.py (the ratchet's measured line)
- 2026-10-22T22:49:45Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md', 'plugin/lib/fmcli.py', 'plugin/tests/test_core.py', 'plugin/tests/test_context_tax.py', 'MASTER.md']
- 2026-10-22T22:58:59Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md', 'plugin/lib/fmcli.py', 'plugin/tests/test_core.py', 'plugin/tests/test_context_tax.py', 'MASTER.md', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx']
- 2026-10-22T22:58:59Z scope: review LOW — remove the dead (procedure:) strip in foreman-ui humanNext and its fixture
- 2026-10-22T23:05:39Z merged worktree-agent-a7051b97b820d7fdb (10 file(s))
- 2026-10-22T23:05:39Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7051b97b820d7fdb
- 2026-10-22T23:05:42Z focused
- 2026-10-22T23:07:58Z scope: plugin/lib/fmcli.py, plugin/tests/test_core.py, test_context_tax.py, MASTER.md, mods/foreman-ui/hooks/kit.ts and its test (dead procedure strip, review item)
- 2026-10-22T23:12:16Z done
- 2026-10-22T23:12:19Z committed 9778a011 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-1699 [FEATURE M, planned, 3 steps] fm which TASK: route a task in plain words to the Foreman skill, playbooks and fm verbs that fit
- decision 2026-10-22: Skills fix: make the hooks name the skill and rewrite descriptions in task terms before adding skills; keep the 2,000-character listing cap and free…
- similar past tasks were L: consider --tier L
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Lessons
- A hint competing for a fixed byte budget must be all-or-nothing and must not mark itself shown until delivered, or it is lost forever
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcli.py
- plugin/tests/test_core.py
- plugin/tests/test_context_tax.py
- MASTER.md
- CHANGELOG.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
