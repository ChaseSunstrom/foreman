---
id: T-1700
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/ui-design, plugin/tests/test_docs.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T22:36:34Z
updated: 2026-10-23T01:42:03Z
base: b5d277bca44524fdce64f8427485a6c64cb22746
base_tree: 42a2c5f3b9163840da27c7b6955a7396c34bb28f
plan0_at: 2026-10-22T23:19:48Z
plan0_scope: [plugin/skills/ui-design, plugin/tests/test_docs.py, CHANGELOG.md]
group: skills and routing
verified: strong
---
# foreman:ui-design skill: one job-shaped entry to distinctive UI work: direction, tokens, type and colour, motion, 3D scenes and visual QA
## Raw request
> foreman:ui-design skill: one job-shaped entry to distinctive UI work: direction, tokens, type and colour, motion, 3D scenes and visual QA
## Interpretation
The design capability (playbooks ui/*, fm design palette/extract/contrast/lint, fm scene, fm motion, fm looks, fm img, the directions skill) is large but nearly unused: nothing says when to use it. One model-invocable skill whose description fires on UI, page, component, animation, 3D or 'make it look good' requests walks the work: pick a direction, tokens, build, motion, check contrast and lint, screenshot.
## Assumptions (confidence)
## Acceptance criteria
- [x] the skill routes to the ui playbooks and fm design / fm scene / fm motion / fm looks / directions, every reference it names exists, and it fits the listing budget — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
Options: a stub skill per UI playbook (budget); a separate design plugin (duplicates); one job skill routing to the existing pieces. Choice: one job skill under 100 lines.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing doc test
2. [x] SKILL.md routing to playbooks and verbs
3. [x] budget fit
## Resume here
## Docs impact
plugin/README.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_docs 2>&1 | tail -15` → ✗ exit 1 · Ran 64 tests in 25.1s (15 classes, 16 at a time; slowest: Fences 18s, TaskLifecycle 7s, Site 3s) / FAILED (1 classes) [ran] [tree a7a8999afe77] (2026-10-22T23:21:33Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → ✗ exit 1 · Ran 64 tests in 19.3s (15 classes, 16 at a time; slowest: Fences 19s, TaskLifecycle 11s, Site 4s) / FAILED (1 classes) [ran] [tree a7a8999afe77] (2026-10-22T23:21:58Z)
- (step 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 64 tests in 11.5s (15 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 3s, Site 2s) / OK [ran] [tree 626f220af97d] (2026-10-22T23:24:19Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 64 tests in 10.9s (15 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 3s, Site 2s) / OK [ran] [tree 626f220af97d] (2026-10-22T23:24:31Z)
- (ac 1) `python3 plugin/tests/run.py test_docs 2>&1 | grep -E "ranks|ties|^OK|FAIL:" | head` → exit 0 · OK [ran] [tree b186c21f6e37] (2026-10-22T23:35:47Z)
- (ac 1) `python3 plugin/tests/run.py test_docs 2>&1 | grep -E "AssertionError|^OK|FAIL:" | head` → exit 0 · OK [ran] [tree f3053cd85083] (2026-10-22T23:36:28Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_hooks test_core test_doctor` → exit 0 · Ran 393 tests in 145.3s (74 classes, 16 at a time; slowest: Stop 145s, NoTaskGate 120s, PreToolUse 113s) / OK [ran] [tree 819de4d74896] (2026-10-23T01:27:15Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_hooks test_core test_doctor` → exit 0 · Ran 393 tests in 48.8s (74 classes, 16 at a time; slowest: Stop 49s, NoTaskGate 36s, PreToolUse 28s) / OK [ran] [tree 099cc9ad6fc3] (2026-10-23T01:38:27Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 65 tests in 8.7s (15 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 099cc9ad6fc3] (2026-10-23T01:38:43Z)
- (audit intent) `fm-reviewer pass (shared with T-1701); fixed: ui-design trigger requests (T-1704 eval), palette prints to stdout (redirect) and extract writes DESIGN.md, tidy/doctor user-only in MASTER/README, _UI catches animation/3D/WebGL/three.js/motion and the ui hint loads the skill` → one job skill routes UI, animation and 3D work through direction, tokens, build, motion, 3D scene and checks, naming only real playbooks and verbs (a test checks each) [tree 099cc9ad6fc3] (2026-10-23T01:38:43Z)
- (audit edge) `fm-reviewer pass (shared with T-1701); fixed: ui-design trigger requests (T-1704 eval), palette prints to stdout (redirect) and extract writes DESIGN.md, tidy/doctor user-only in MASTER/README, _UI catches animation/3D/WebGL/three.js/motion and the ui hint loads the skill` → 'fm motion check' doesn't trigger the UI hint; 'motion sensor' or '3D printer' may (one extra hint per session) [tree 099cc9ad6fc3] (2026-10-23T01:38:43Z)
- (audit maintainer) `fm-reviewer pass (shared with T-1701); fixed: ui-design trigger requests (T-1704 eval), palette prints to stdout (redirect) and extract writes DESIGN.md, tidy/doctor user-only in MASTER/README, _UI catches animation/3D/WebGL/three.js/motion and the ui hint loads the skill` → the verb test catches a renamed subcommand (proved with fm img dif) [tree 099cc9ad6fc3] (2026-10-23T01:38:43Z)
- (audit operator) `fm-reviewer pass (shared with T-1701); fixed: ui-design trigger requests (T-1704 eval), palette prints to stdout (redirect) and extract writes DESIGN.md, tidy/doctor user-only in MASTER/README, _UI catches animation/3D/WebGL/three.js/motion and the ui hint loads the skill` → listing at 1,837 of 2,200 after ui-design; hint wording 'load: Skill foreman:ui-design, or for a small change fm playbooks show ui/INDEX' [tree 099cc9ad6fc3] (2026-10-23T01:38:43Z)
## Log
- 2026-10-22T22:36:34Z created
- 2026-10-22T22:36:35Z set scope=['plugin/skills/ui-design', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-22T22:36:36Z from T-1692 (skills hardly used; brainstorm-skills-20261022)
- 2026-10-22T23:19:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1700.builder.md
- 2026-10-22T23:19:48Z focused
- 2026-10-23T01:37:27Z merged worktree-agent-affe43a7d7479b467 (8 file(s))
- 2026-10-23T01:37:28Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-affe43a7d7479b467
- 2026-10-23T01:37:37Z focused
- 2026-10-23T01:38:34Z scope: fmcore.py (SKILL_FOR/_UI), test_hooks.py, MASTER.md, plugin/README.md, the trigger fixture — review items
- 2026-10-23T01:42:03Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook UI playbooks (skills/playbooks/references/ui/INDEX.md)
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- research mission-20261022-172631: Request: I also know there arent a lot of skills with foreman? and they are also hardly used? why? super improve!!!
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/skills/ui-design/SKILL.md, plugin/tests/test_docs.py; re-ground the plan against them before editing
## Lessons
- A skill that names verbs and paths needs a test that resolves each one, or it rots the first time a verb is renamed
## Plan gaps
- failed first: step 1 failing doc test
## Files touched
- plugin/tests/test_docs.py
- plugin/skills/ui-design/SKILL.md
- plugin/lib/fmcore.py
- plugin/tests/test_hooks.py
- MASTER.md
- plugin/README.md
- CHANGELOG.md
- plugin/evals/playbooks/verify/tdd-workflow.json
- plugin/lib/fmcli.py
- plugin/lib/fmplaybooks.py
- plugin/skills/playbooks/SKILL.md
- plugin/tests/fixtures/skill_triggers.json
- plugin/tests/test_playbook_evals.py
- plugin/lib/fmcost.py
- plugin/lib/fmhooks.py
- plugin/tests/test_cost.py
- plugin/tests/test_drive_side.py
