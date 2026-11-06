---
id: T-1508
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/skills/directions/SKILL.md, plugin/skills/directions/references/cards.md, plugin/tests/test_docs.py, CHANGELOG.md, MASTER.md, plugin/README.md, plugin/skills/playbooks/references/ui/design-direction.md, plugin/skills/brainstorm/SKILL.md, plugin/skills/next/SKILL.md, plugin/skills/library/SKILL.md, plugin/skills/tidy/SKILL.md, plugin/skills/improve/SKILL.md, plugin/skills/doctor/SKILL.md, plugin/skills/status/SKILL.md, plugin/skills/reflect/SKILL.md, plugin/skills/intake/SKILL.md, plugin/skills/resume/SKILL.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:40Z
updated: 2026-10-22T19:53:04Z
base: 0573c77fe9ea6b4ec40fe83dcd62171c50037137
base_tree: 4dfbcbe9927a40762dd2d70d49d567c71febfaeb
plan0_at: 2026-10-22T19:04:02Z
plan0_scope: [plugin/skills/directions/SKILL.md, plugin/tests/test_docs.py, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 13): a directions skill: six one-screen style direction
## Raw request
> Brainstorm T-1479 round 2 (cluster 13): a directions skill: six one-screen style directions from one sentence; the pick is saved as DESIGN.md with an audacity level (builds on ui/design-direction.md, T-1488)
## Interpretation
A directions skill: from one sentence about a product, Claude proposes six one-screen style directions (drawn from ui/design-direction.md's bank and taste words, each with palette, type pairing, layout idea, motion temperament and signature move), the user (or full autonomy) picks one, and it is saved as DESIGN.md with an audacity level. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] the directions skill exists with its procedure (six directions, the pick, DESIGN.md) and test_docs finds it — verify with `cd plugin/tests && python3 -m unittest test_docs.Skills`
## Non-goals
## Approach (options → choice → why)
Options: generate images (a dependency); chosen: a skill that writes the six as short text cards plus one HTML preview page per direction when asked, saving the pick through the DESIGN.md template.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write plugin/skills/directions/SKILL.md
2. [x] register it where skills are listed
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs 2>&1 | tail -5` → exit 0 · Ran 50 tests in 6.3s (12 classes, 16 at a time; slowest: TaskLifecycle 4s, Site 2s, TaskDocsDrift 2s) / OK [ran] [tree 7a461e69e77d] (2026-10-22T19:05:35Z)
- (step 2) `python3 plugin/tests/run.py test_docs 2>&1 | tail -3` → exit 0 · Ran 51 tests in 1.4s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, Site 1s, TaskDocsDrift 0s) / OK [ran] [tree 3564cdfa4cbc] (2026-10-22T19:14:20Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 51 tests in 1.4s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, Site 1s, TaskDocsDrift 0s) / OK [ran] [tree 3564cdfa4cbc] (2026-10-22T19:14:23Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_docsdrift test_doctor test_library` → exit 0 · Ran 147 tests in 7.1s (39 classes, 16 at a time; slowest: LibSources 7s, LibraryAdmit 2s, Command 2s) / OK [ran] [tree 3564cdfa4cbc] (2026-10-22T19:14:35Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 51 tests in 1.4s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, Site 1s, TaskDocsDrift 0s) / OK [ran] [tree 1d8e17c3aed9] (2026-10-22T19:15:52Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 107 tests in 2.2s (31 classes, 16 at a time; slowest: Command 2s, TaskLifecycle 2s, ViewsRepair 2s) / OK [ran] [tree 11eccb4b3c2c] (2026-10-22T19:21:50Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_docs.Skills` → exit 0 · Ran 8 tests in 0.018s / OK [ran] [tree eb17ce32d1fc] (2026-10-22T19:52:12Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_doctor test_library` → exit 0 · Ran 146 tests in 7.6s (39 classes, 16 at a time; slowest: LibSources 7s, LibraryAdmit 3s, Command 3s) / OK [ran] [tree eb17ce32d1fc] (2026-10-22T19:52:20Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_docs.Skills` → exit 0 · Ran 8 tests in 0.017s / OK [ran] [tree 20d66e81202c] (2026-10-22T19:52:29Z)
- (audit adversary) `self: intent: six distinct directions, a pick, DESIGN.md · adversary: preview pages are written outside the repo and run through fm design lint; no code runs · edge: a second run stops when DESIGN.md exists unless asked; terminal UIs go to terminal-ui.md · operator: skill listing 1,956 of 2,000 chars (descriptions trimmed, cap kept by decision) · maintainer: test_docs checks procedure terms, six cards with every field and measured contrast` → a skill only, no code path; trimmed descriptions keep every trigger phrase; security-sensitive files in range belong to T-1585, T-1505 and T-1503, reviewed there [tree 20d66e81202c] (2026-10-22T19:52:29Z)
- (audit maintainer) `self: intent: six distinct directions, a pick, DESIGN.md · adversary: preview pages are written outside the repo and run through fm design lint; no code runs · edge: a second run stops when DESIGN.md exists unless asked; terminal UIs go to terminal-ui.md · operator: skill listing 1,956 of 2,000 chars (descriptions trimmed, cap kept by decision) · maintainer: test_docs checks procedure terms, six cards with every field and measured contrast` → test_docs, test_doctor and test_library pass [tree 20d66e81202c] (2026-10-22T19:52:29Z)
- (audit self) `self: intent: six distinct directions, a pick, DESIGN.md · adversary: preview pages are written outside the repo and run through fm design lint; no code runs · edge: a second run stops when DESIGN.md exists unless asked; terminal UIs go to terminal-ui.md · operator: skill listing 1,956 of 2,000 chars (descriptions trimmed, cap kept by decision) · maintainer: test_docs checks procedure terms, six cards with every field and measured contrast` → no findings [tree 20d66e81202c] (2026-10-22T19:52:29Z)
## Log
- 2026-10-22T17:36:40Z created
- 2026-10-22T17:55:39Z set scope=['plugin/skills/directions/SKILL.md', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-22T19:03:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1508.builder.md
- 2026-10-22T19:04:00Z focused
- 2026-10-22T19:13:24Z set scope=['plugin/skills/directions/SKILL.md', 'plugin/skills/directions/references/cards.md', 'plugin/tests/test_docs.py', 'CHANGELOG.md', 'MASTER.md', 'plugin/README.md', 'plugin/skills/playbooks/references/ui/design-direction.md']
- 2026-10-22T19:13:26Z scope: + references/cards.md (long material kept out of SKILL.md), MASTER.md and plugin/README.md (where skills are listed, step 2), design-direction.md (a pointer to the skill)
- 2026-10-22T19:19:57Z set scope=['plugin/skills/directions/SKILL.md', 'plugin/skills/directions/references/cards.md', 'plugin/tests/test_docs.py', 'CHANGELOG.md', 'MASTER.md', 'plugin/README.md', 'plugin/skills/playbooks/references/ui/design-direction.md', 'plugin/skills/brainstorm/SKILL.md', 'plugin/skills/next/SKILL.md', 'plugin/skills/library/SKILL.md', 'plugin/skills/tidy/SKILL.md', 'plugin/skills/improve/SKILL.md', 'plugin/skills/doctor/SKILL.md', 'plugin/skills/status/SKILL.md', 'plugin/skills/reflect/SKILL.md', 'plugin/skills/intake/SKILL.md']
- 2026-10-22T19:19:57Z steer: keep the 2,000-char listing cap; trim the longest descriptions' wording to fit directions with ~40 to spare (coordinator's answer to the andon)
- 2026-10-22T19:20:40Z set scope=['plugin/skills/directions/SKILL.md', 'plugin/skills/directions/references/cards.md', 'plugin/tests/test_docs.py', 'CHANGELOG.md', 'MASTER.md', 'plugin/README.md', 'plugin/skills/playbooks/references/ui/design-direction.md', 'plugin/skills/brainstorm/SKILL.md', 'plugin/skills/next/SKILL.md', 'plugin/skills/library/SKILL.md', 'plugin/skills/tidy/SKILL.md', 'plugin/skills/improve/SKILL.md', 'plugin/skills/doctor/SKILL.md', 'plugin/skills/status/SKILL.md', 'plugin/skills/reflect/SKILL.md', 'plugin/skills/intake/SKILL.md', 'plugin/skills/resume/SKILL.md']
- 2026-10-22T19:22:37Z merged worktree-agent-abf94b16434c6662f (16 file(s))
- 2026-10-22T19:22:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abf94b16434c6662f
- 2026-10-22T19:52:11Z focused
- 2026-10-22T19:52:29Z scope: the reference file, MASTER.md, plugin/README.md, design-direction.md pointer and eleven skill descriptions (trimmed for the 2,000-char listing cap, decision recorded); other files came from other tasks' merges
- 2026-10-22T19:53:03Z done
- 2026-10-22T19:53:04Z committed e93bffda (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Design direction before pixels (skills/playbooks/references/ui/design-direction.md)
- T-1498 [FEATURE M, done, 2 steps] Style shelf: twelve original named looks as library cards — lesson: Name taste cards with a prefix (look-) so a single everyday word in…
- T-1488 [FEATURE M, done, 2 steps] UI playbook: design direction before pixels — lesson: A playbook's acceptance check proves headings, not quality: pair every writing ta…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–2 steps
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/README.md, plugin/skills/brainstorm/SKILL.md, plugin/skills/directions/SKILL.md, plugin/skills/directions/references/cards.md, plugin/skills/doctor/SKILL.md, plugin/sk…; re-ground the plan against them before editing
## Why not caught
new skill
## Lessons
- The skill listing budget has ~44 characters left: the next model-invocable skill needs a rule (a per-skill allowance), not another trim
## Files touched
- plugin/tests/test_docs.py
- plugin/skills/directions/references/cards.md
- plugin/skills/directions/SKILL.md
- ANDON.md
- MASTER.md
- plugin/README.md
- plugin/skills/playbooks/references/ui/design-direction.md
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/doctor/SKILL.md
- plugin/skills/improve/SKILL.md
- plugin/skills/intake/SKILL.md
- plugin/skills/library/SKILL.md
- plugin/skills/next/SKILL.md
- plugin/skills/reflect/SKILL.md
- plugin/skills/status/SKILL.md
- plugin/skills/tidy/SKILL.md
- plugin/skills/resume/SKILL.md
- CHANGELOG.md
- README.md
- plugin/commands/settings.md
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmrelease.py
- plugin/lib/fmsettings.py
- plugin/lib/fmsmoke.py
- plugin/lib/smoke_web.cjs
- plugin/skills/playbooks/ratchet.json
- plugin/skills/playbooks/references/clean/code-simplifier.md
