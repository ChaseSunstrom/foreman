---
id: T-2659
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/skills/brainstorm/SKILL.md, plugin/tests/test_brainstorm_skill.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T19:56:57Z
updated: 2026-11-02T19:59:48Z
base: 845127d3471ba31a5fd899f6f00759725af014b9
base_tree: 5784b1bc50837b208f620666a8b88eba70883cb7
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T19:56:59Z
plan0_scope: [plugin/skills/brainstorm/SKILL.md, plugin/tests/test_skills.py, CHANGELOG.md]
verified: strong
---
# The brainstorm skill's grounding step asks for MASTER.md first, three phrasings per idea and the verbs' own help strings before 'new', and says a grounding pass is spot-checked: 3 of 4 slate items from brainstorm-20261102 marked new or partial were already built
## Raw request
> The brainstorm skill's grounding step asks for MASTER.md first, three phrasings per idea and the verbs' own help strings before 'new', and says a grounding pass is spot-checked: 3 of 4 slate items from brainstorm-20261102 marked new or partial were already built
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the brainstorm skill's step 4 names MASTER.md first, three phrasings and the argparse help strings, and a spot check of grounded 'new' items before any is built — verify with `python3 plugin/tests/run.py test_brainstorm_skill`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] edit step 4
## Resume here
<!-- auto -->
- 2026-11-02T19:58:21Z steps 1/1 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, plugin/skills/brainstorm/SKILL.md, MOONSHOT.md, plugin/tests/test_brainstorm_skill.py
- touched since last checkpoint: plugin/tests/test_brainstorm_skill.py, plugin/skills/brainstorm/SKILL.md
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_brainstorm_skill` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Grounding 0s) / FAILED (1 classes: test_brainstorm_skill.Grounding) [ran] [tree d7a22faad09c] [world 2f1906870a] (2026-11-02T19:57:13Z)
- (ac 1) `python3 plugin/tests/run.py test_brainstorm_skill` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Grounding 0s) / OK [ran] [tree 3e6249e0b6bc] [world 2f1906870a] (2026-11-02T19:57:35Z)
- (step 1) `python3 plugin/tests/run.py test_brainstorm_skill test_docs` → exit 0 · Ran 104 tests in 10.5s (25 classes, 16 at a time; slowest: Fences 10s, DocsProof 4s, TaskLifecycle 3s) / OK [ran] [tree 3e6249e0b6bc] [world 2f1906870a] (2026-11-02T19:57:35Z)
- (audit self) `self: one paragraph of the skill's step 4; the test pins its four requirements` → no findings [tree 3e6249e0b6bc] (2026-11-02T19:57:35Z)
## Log
- 2026-11-02T19:56:57Z created
- 2026-11-02T19:56:58Z focused
- 2026-11-02T19:56:59Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T19:57:12Z set scope=['plugin/skills/brainstorm/SKILL.md', 'plugin/tests/test_brainstorm_skill.py', 'CHANGELOG.md']
- 2026-11-02T19:57:12Z criterion 1 verify: `python3 plugin/tests/run.py test_skills test_docs` → `python3 plugin/tests/run.py test_brainstorm_skill`
- 2026-11-02T19:59:45Z done
- 2026-11-02T19:59:48Z committed 6148fe2a (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2076 [FEATURE M, done, 2 steps] Brainstorms learn from what they missed: asks no idea predicted feed a blind-spots lens, and each run leaves questions for the next — l…
- research brainstorm-20261102: 552 ideas in 59 clusters, each grounded in the code: 104 built, 197 new, 249 partial, 2 premise-false. 24 clusters marked build.
- research brainstorm-pass-5: Source: research/brainstorm-20261004-033458 (simplicity: what to cut, merge or make automatic; bold bets: what would make Foreman indispensab…
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_board_surfaces.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_cost.py, plugin/test…
## Why not caught
the skill asked for 'a grep or read per cluster', which a recon satisfied with one phrasing in one file
## Lessons
- A grounding rule that allows one grep produces confident 'new' marks: ask for the system map first and several phrasings, then spot-check
## Plan gaps
- failed first: step 1 edit step 4
## Files touched
- plugin/tests/test_brainstorm_skill.py
- plugin/skills/brainstorm/SKILL.md
- CHANGELOG.md
