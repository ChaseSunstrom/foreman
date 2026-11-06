---
id: T-1018
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: scout
created: 2026-10-16T01:37:40Z
updated: 2026-10-16T01:39:04Z
base: 9941b64397645d64c51e44b9f9111fadc276aa34
base_tree: 176dac4a4b4d4a1c4e47b38ed1f626d3084bd77f
verified: strong
---
# Stack cards: CodeMirror 6 card; tauri-build and tauri-plugin-* on the tauri card; troika-three-text on three-js
## Raw request
> Found by fm scout: dependencies in your projects with no stack card: tauri-build, tauri-plugin-notification, tauri-plugin-single-instance, troika-three-text, @codemirror/autocomplete, @codemirror/commands, @codemirror/language, @codemirror/lint. Write one card each to the spec in plugin/skills/library/SKILL.md (a writer subagent per batch), then fm lib check
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lib check passes; codemirror card exists; tauri and three-js cards detect the scout's deps — verify with `fm lib check && fm lib show codemirror`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] detect lines and the codemirror card
2. [x] fm scout --slow no longer lists these deps
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `fm lib check && fm lib show codemirror` → exit 0 · - [ ] `@codemirror/*` packages resolve to single copies. / - [ ] State logic has tests that need no DOM. [ran] [tree 191711120059] (2026-10-16T01:38:23Z)
- (step 2) `fm lib check` → exit 0 · 1082 cards, all well-formed (27 related names have no card yet). [ran] [tree bdeb1c33c8ac] (2026-10-16T01:39:02Z)
- (ac 1) `fm lib check && fm lib show codemirror` → exit 0 · - [ ] `@codemirror/*` packages resolve to single copies. / - [ ] State logic has tests that need no DOM. [ran] [tree bdeb1c33c8ac] (2026-10-16T01:39:03Z)
- (audit intent) `self` → CodeMirror 6 API names checked (EditorState.create, EditorView, view.dispatch changes, Compartment.reconfigure, StateField, ViewPlugin, keymap.of, linter, autocompletion); the scout's next run no longer lists the batch [tree bdeb1c33c8ac] (2026-10-16T01:39:03Z)
- (ac 1) `fm lib check && fm lib show codemirror` → exit 0 · - [ ] `@codemirror/*` packages resolve to single copies. / - [ ] State logic has tests that need no DOM. [ran] [tree bdeb1c33c8ac] (2026-10-16T01:39:03Z)
- (audit intent) `card written to spec; fm lib check passes; scout moved past the batch` → real-API deps covered, assets left out [tree bdeb1c33c8ac] (2026-10-16T01:39:03Z)
- (audit self) `card written to spec; fm lib check passes; scout moved past the batch` → no findings [tree bdeb1c33c8ac] (2026-10-16T01:39:03Z)
## Log
- 2026-10-16T01:37:40Z created
- 2026-10-16T01:38:01Z planned from capture
- 2026-10-16T01:38:01Z focused
- 2026-10-16T01:39:04Z done
- 2026-10-16T01:39:04Z committed 72bd3fb (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1016 [FEATURE S, done, 2 steps] Stack cards for the deps scout found: scipy, python-audio (librosa, soundfile, demucs), postprocessing; detect lines for playwright-cor…
- T-0933 [FEATURE L, done, 5 steps] Stack library: 400+ on-demand implementation cards (fm lib) plus federated search over installed plugins' skills — lesson: Subagent-wri…
- research T-0933-review: Changes needed. The code works and the 22 cards I sampled are accurate. Detect signals produce false-positive suggestions, and one manifest regex…
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
## Files touched
- plugin/skills/library/cards/web/tauri.md
- plugin/skills/library/cards/web/three-js.md
- plugin/skills/library/cards/web/codemirror.md
- plugin/skills/library/cards/node/eslint.md
- CHANGELOG.md
