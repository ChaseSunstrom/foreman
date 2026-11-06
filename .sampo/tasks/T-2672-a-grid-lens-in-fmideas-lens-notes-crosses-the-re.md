---
id: T-2672
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T21:30:41Z
updated: 2026-11-02T21:41:01Z
builder_model: sonnet
base: 525eb957f7a83d340ffcaddd783bef503030a831
base_tree: 3f668e7c8b003d3c85ac119426453cb60e2015f4
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T21:31:29Z
plan0_scope: []
lane_stop: merged 2026-11-02T21:38:24Z
verified: strong
unproven: [docs]
---
# a grid lens in fmideas.LENS_NOTES: cross the request's surfaces with its actors and failure modes, one idea per cell; selectable with --lens grid; the brainstorm skill names it for exhaustive requests
## Raw request
> FEATURE: a grid lens in fmideas.LENS_NOTES crosses the request's surfaces with its actors and failure modes and asks for one idea per cell; fm ideas --lens grid selects it and the brainstorm skill names it for exhaustive requests
> CONTEXT: Genesis gen-3 Mission 6 (#2 exhaustive thinking), gen-3/mission-exhaustive-thinking.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] LENS_NOTES has a grid note asking for one idea per surface × actor × failure-mode cell, fm ideas --lens grid sends it, and the skill names it — verify with `python3 plugin/tests/run.py test_ideas test_brainstorm_skill`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: the grid note and its selection
2. [x] the note in LENS_NOTES and the skill line
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_ideas test_brainstorm_skill` → exit 0 · Ran 29 tests in 21.0s (6 classes, 16 at a time; slowest: Ideas 20s, BoardIdeas 4s, DegradeOnPace 2s) / OK [ran] [tree bd3e42b5e419] [world 2f1906870a] (2026-11-02T21:32:52Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_surfaces test_brainstorm_skill test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_extras test_followups test_guard test_guard_cases test_hooks test_ideas test_ideation test_incident test_judgment test_lib_hostile test_lib_source_kill test_library test_nudges test_onwrite test_playbook_use test_plugin_parity test_plugins test_release test_replan test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste test_taste_ledger test_tidy test_tool_queue test_ui test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [23.43s] [ran] [tree bd3e42b5e419] [world 2f1906870a] (2026-11-02T21:36:12Z)
- (step 1) `python3 plugin/tests/run.py test_ideas test_brainstorm_skill` → exit 0 · Ran 30 tests in 12.4s (7 classes, 16 at a time; slowest: Ideas 12s, BoardIdeas 2s, DegradeOnPace 1s) / OK [ran] [tree 25470459a4ab] [world 2f1906870a] (2026-11-02T21:38:45Z)
- (step 2) `python3 plugin/tests/run.py test_ideas test_brainstorm_skill` → exit 0 · Ran 30 tests in 12.4s (7 classes, 16 at a time; slowest: Ideas 12s, BoardIdeas 2s, DegradeOnPace 1s) / OK [ran] [tree 25470459a4ab] [world 2f1906870a] (2026-11-02T21:38:58Z)
- (step 3) `python3 plugin/tests/run.py test_ideas test_brainstorm_skill` → exit 0 · Ran 30 tests in 12.0s (7 classes, 16 at a time; slowest: Ideas 12s, BoardIdeas 2s, DegradeOnPace 1s) / OK [ran] [tree 25470459a4ab] [world 2f1906870a] (2026-11-02T21:39:11Z)
- (ac 1) `python3 plugin/tests/run.py test_ideas test_brainstorm_skill` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T21:39:11Z [ran] [tree 25470459a4ab] [world 2f1906870a] (2026-11-02T21:39:13Z)
- (audit edge) `self: reviewed the builder diff: one fixed note in LENS_NOTES, picked up by name in lens_prompt, and one skill sentence; nothing reads outside text` → whether a real model fills one idea per cell is measured on Mission 7's brainstorm, as Mission 6's Done when says [tree 25470459a4ab] (2026-11-02T21:39:13Z)
- (audit self) `self: reviewed the builder diff: one fixed note in LENS_NOTES, picked up by name in lens_prompt, and one skill sentence; nothing reads outside text` → no findings [tree 25470459a4ab] (2026-11-02T21:39:13Z)
## Log
- 2026-11-02T21:30:41Z created
- 2026-11-02T21:31:12Z planned from capture
- 2026-11-02T21:31:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2672.builder.md
- 2026-11-02T21:31:28Z focused
- 2026-11-02T21:31:29Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T21:38:24Z merged worktree-agent-a95ab72596c06b85b (4 file(s))
- 2026-11-02T21:38:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a95ab72596c06b85b
- 2026-11-02T21:38:25Z focused
- 2026-11-02T21:40:59Z done
- 2026-11-02T21:41:01Z committed b38c5388 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- research brainstorm-20261102-m6: 398 ideas in 44 clusters, each grounded in the code: 54 built, 2 false-premise, 156 new, 186 partial. 24 clusters marked build.
- decision 2026-11-02: Recommendation: Mission 6 builds three gaps where Foreman drops part of a request's space silently (a grid lens, a count on every cut list, a canary…
## Files touched
- plugin/tests/test_ideas.py
- plugin/tests/test_brainstorm_skill.py
- plugin/lib/fmideas.py
- plugin/skills/brainstorm/SKILL.md
- CHANGELOG.md
