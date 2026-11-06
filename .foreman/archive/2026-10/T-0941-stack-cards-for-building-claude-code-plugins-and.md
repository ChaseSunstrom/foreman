---
id: T-0941
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T20:23:54Z
updated: 2026-10-15T20:46:30Z
base: 0505928b772d84fa78373956e6f677ea1756029b
base_tree: 9bf8ae6ab07ace527cc9471b93579c56a58d0d7f
verified: ok
---
# Stack cards for building Claude Code extensions (plugins, hooks, skills, subagents, commands, MCP, output styles, statusline, mods UI, evals, headless, Agent SDK) and for ideation and self-improvement practice
## Raw request
> Stack cards for building Claude Code plugins and mods (hooks, skills, subagents, commands, MCP servers, output styles, statusline, mods UI, marketplaces, plugin evals, Agent SDK) plus brainstorming-method cards, so Foreman can keep improving itself
## Interpretation
The user wants Foreman to be able to improve itself and to build Claude Code plugins and mods well, so the library needs cards on Claude Code's own extension points, grounded in what really works here: Foreman's plugin (plugin/.claude-plugin/plugin.json, hooks/hooks.json, skills, agents, monitors, output styles, statusline) and the foreman-ui mod (mods/foreman-ui, with the engine types in .claude-plugin/types/claude-code/index.d.ts). It also wants cards on brainstorming and improvement practice: ideation lenses, capability maps, premortems, experiment design and self-improvement loops.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lib check passes with a claude-code area of 20+ cards and a practice area of 15+ cards — verify with `fm lib check`
- [x] fm lib search finds them: 'hook PreToolUse' ranks the hooks card first, 'brainstorm' ranks a practice card in the top 3 — verify with `python3 plugin/tests/run.py -k LibraryAreas`
## Non-goals
## Approach (options → choice → why)
Options: (A) two writer subagents, one per area, each told to verify every format detail against the local files (Foreman's plugin and mod are working examples) and the docs, leaving out anything it can't confirm (chosen); (B) port ECC's agent and plugin skills (generic, not grounded in this engine); (C) write them on the main thread (slow, costly context). Area names: claude-code and practice.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Write the cards in two writer subagents, grounded in Foreman's own plugin files and the mod engine's types
2. [x] A LibraryAreas test for the two areas and their search
3. [x] Lint, spot-check five cards against the sources, README count
## Resume here
<!-- auto -->
- 2026-10-15T20:41:52Z step 2/3: A LibraryAreas test for the two areas and their search
- git: foreman/build; 4 uncommitted: README.md, plugin/tests/test_library.py, plugin/skills/library/cards/claude-code/, plugin/skills/library/cards/practice/
- touched since last checkpoint: plugin/tests/test_library.py, plugin/skills/library/cards/practice/brainstorming-lenses.md, plugin/skills/library/cards/practice/capability-mapping.md, plugin/skills/library/cards/practice/approach-comparison.md, plugin/skills/library/cards/practice/premortem.md, plugin/skills/library/cards/practice/five-whys.md, plugin/skills/library/cards/practice/first-principles.md, plugin/skills/library/cards/practice/assumption-mapping.md, plugin/skills/library/cards/claude-code/cc-plugins.md, plugin/skills/library/cards/practice/scope-cutting.md, plugin/skills/library/cards/claude-code/cc-plugin-manifest.md, plugin/skills/library/cards/practice/value-effort-scoring.md, plugin/skills/library/cards/claude-code/cc-marketplaces.md, plugin/skills/library/cards/practice/spikes.md, plugin/skills/library/cards/claude-code/cc-hooks.md
## Docs impact
README.md stack library line: 27 areas including Claude Code extension building and practice
## Verification evidence
- (step 2) `python3 plugin/tests/run.py -k LibraryAreas` → ✗ exit 1 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: LibraryAreas 0s) / FAILED (1 classes) [ran] [tree 513101ee2876] (2026-10-15T20:39:18Z)
- (step 1) `fm lib check` → exit 0 · 1078 cards, all well-formed (27 related names have no card yet). [ran] [tree 2815e0c23b7e] (2026-10-15T20:46:03Z)
- (step 2) `python3 plugin/tests/run.py -k LibraryAreas` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: LibraryAreas 0s) / OK [ran] [tree 2815e0c23b7e] (2026-10-15T20:46:03Z)
- (step 3) `spot-check cc-hooks, cc-plugins, cc-mods-ui, practice/premortem, practice/brainstorming-lenses against plugin/hooks/hooks.json, the mod engine types and fm verbs` → accurate: exit 2 blocks, the hooks wrapper key, onFailure block, stop_hook_active; every fm verb named exists (the writer fixed fm task lesson → fm task finish --lesson) [tree 2815e0c23b7e] (2026-10-15T20:46:03Z)
- (ac 1) `fm lib check` → exit 0 · 1078 cards, all well-formed (27 related names have no card yet). [ran] [tree 2815e0c23b7e] (2026-10-15T20:46:04Z)
- (ac 2) `python3 plugin/tests/run.py -k LibraryAreas` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: LibraryAreas 0s) / OK [ran] [tree 2815e0c23b7e] (2026-10-15T20:46:04Z)
- (ac 1) `fm lib check` → exit 0 · 1078 cards, all well-formed (27 related names have no card yet). [ran] [tree 3577cf87b9b8] (2026-10-15T20:46:17Z)
- (ac 2) `python3 plugin/tests/run.py -k LibraryAreas` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: LibraryAreas 0s) / OK [ran] [tree 3577cf87b9b8] (2026-10-15T20:46:17Z)
- (audit intent) `main-thread spot-check of five cards against Foreman's own plugin, the mod engine types and the fm parser; lint over all 1,078 cards; area and search tests` → ok: 27 claude-code cards grounded in Foreman's working plugin and mod plus the docs; 25 practice cards that name only real fm verbs [tree 3577cf87b9b8] (2026-10-15T20:46:17Z)
- (audit edge) `main-thread spot-check of five cards against Foreman's own plugin, the mod engine types and the fm parser; lint over all 1,078 cards; area and search tests` → ok: a plugin repo outside git now gets its cards (the walk sees .claude-plugin); practice cards have no detect so they never crowd suggestions [tree 3577cf87b9b8] (2026-10-15T20:46:17Z)
- (audit maintainer) `main-thread spot-check of five cards against Foreman's own plugin, the mod engine types and the fm parser; lint over all 1,078 cards; area and search tests` → ok: LibraryAreas pins counts and search ranking [tree 3577cf87b9b8] (2026-10-15T20:46:17Z)
- (audit intent) `main-thread spot-check of five cards against Foreman's own plugin, the mod engine types and the fm parser; lint over all 1,078 cards; area and search tests; security cards read in full` → ok: 27 claude-code cards grounded in Foreman's working plugin and mod plus the docs; 25 practice cards that name only real fm verbs [tree 3577cf87b9b8] (2026-10-15T20:46:28Z)
- (audit adversary) `main-thread spot-check of five cards against Foreman's own plugin, the mod engine types and the fm parser; lint over all 1,078 cards; area and search tests; security cards read in full` → ok: cc-hook-security and cc-settings-permissions are defensive (fail closed with exit 2 or onFailure block, no interpolation of tool_input, no interpreter-wide allow rules, bypass modes only in user settings); no payloads or secrets [tree 3577cf87b9b8] (2026-10-15T20:46:28Z)
- (audit edge) `main-thread spot-check of five cards against Foreman's own plugin, the mod engine types and the fm parser; lint over all 1,078 cards; area and search tests; security cards read in full` → ok: a plugin repo outside git now gets its cards (the walk sees .claude-plugin); practice cards have no detect so they never crowd suggestions [tree 3577cf87b9b8] (2026-10-15T20:46:28Z)
- (audit operator) `main-thread spot-check of five cards against Foreman's own plugin, the mod engine types and the fm parser; lint over all 1,078 cards; area and search tests; security cards read in full` → ok: README lists the two new areas [tree 3577cf87b9b8] (2026-10-15T20:46:28Z)
- (audit maintainer) `main-thread spot-check of five cards against Foreman's own plugin, the mod engine types and the fm parser; lint over all 1,078 cards; area and search tests; security cards read in full` → ok: LibraryAreas pins counts and search ranking [tree 3577cf87b9b8] (2026-10-15T20:46:28Z)
## Log
- 2026-10-15T20:23:54Z created
- 2026-10-15T20:28:38Z planned from capture
- 2026-10-15T20:38:35Z focused
- 2026-10-15T20:41:53Z paused: focus moved to T-0944
- 2026-10-15T20:46:02Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-15T20:46:02Z focused
- 2026-10-15T20:46:02Z scope: fmlib walk now sees dot dirs (.claude-plugin, .devcontainer) so plugin repos outside git get their cards; heavy dot caches skipped
- 2026-10-15T20:46:29Z done
- 2026-10-15T20:46:30Z committed f01441f (31 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0588 [RESEARCH L, done, 3 steps] And maybe a knowledge graph if we dont have it already, and also, better intuition/reasoni — lesson: grounding brainstormers in today'…
- T-0933 [FEATURE L, done, 5 steps] Stack library: 400+ on-demand implementation cards (fm lib) plus federated search over installed plugins' skills — lesson: Subagent-wri…
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
## Lessons
- Writers grounded in local working examples (Foreman's own plugin and mod) produce format-accurate extension cards; telling them to check every fm verb against the parser caught a nonexistent verb before it shipped.
## Plan gaps
- failed first: step 2 A LibraryAreas test for the two areas and their search
## Files touched
- plugin/tests/test_library.py
- plugin/skills/library/cards/practice/brainstorming-lenses.md
- plugin/skills/library/cards/practice/capability-mapping.md
- plugin/skills/library/cards/practice/approach-comparison.md
- plugin/skills/library/cards/practice/premortem.md
- plugin/skills/library/cards/practice/five-whys.md
- plugin/skills/library/cards/practice/first-principles.md
- plugin/skills/library/cards/practice/assumption-mapping.md
- plugin/skills/library/cards/claude-code/cc-plugins.md
- plugin/skills/library/cards/practice/scope-cutting.md
- plugin/skills/library/cards/claude-code/cc-plugin-manifest.md
- plugin/skills/library/cards/practice/value-effort-scoring.md
- plugin/skills/library/cards/claude-code/cc-marketplaces.md
- plugin/skills/library/cards/practice/spikes.md
- plugin/skills/library/cards/claude-code/cc-hooks.md
- plugin/skills/library/cards/practice/kill-criteria.md
- plugin/skills/library/cards/claude-code/cc-hook-payloads.md
- plugin/skills/library/cards/practice/experiment-design.md
- plugin/skills/library/cards/claude-code/cc-hook-security.md
- plugin/skills/library/cards/practice/metrics-and-guardrails.md
- plugin/skills/library/cards/claude-code/cc-hook-performance.md
- plugin/skills/library/cards/practice/red-team-review.md
- plugin/skills/library/cards/claude-code/cc-skills.md
- plugin/skills/library/cards/practice/scientific-debugging.md
- plugin/skills/library/cards/claude-code/cc-skill-descriptions.md
- plugin/skills/library/cards/practice/rubber-ducking.md
- plugin/skills/library/cards/practice/self-improvement-loops.md
- plugin/skills/library/cards/practice/friction-logging.md
- plugin/skills/library/cards/practice/retrospectives.md
- plugin/skills/library/cards/practice/decision-records.md
