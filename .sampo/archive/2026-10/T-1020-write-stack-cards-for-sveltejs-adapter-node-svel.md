---
id: T-1020
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: scout
created: 2026-10-16T01:39:19Z
updated: 2026-10-16T01:40:11Z
base: 72bd3fba0c180444b057aa47280be31b5555c458
base_tree: bdeb1c33c8ac3940cdb5c00d35a0613a6f0f533d
verified: strong
---
# Stack cards: SvelteKit adapters, Vite plugins, VS Code extension tooling and xterm.js detected
## Raw request
> Found by fm scout: dependencies in your projects with no stack card: @sveltejs/adapter-node, @sveltejs/adapter-static, @vitejs/plugin-react, @vscode/test-electron, @vscode/vsce, @xterm/addon-fit, @xterm/headless, @xterm/xterm. Write one card each to the spec in plugin/skills/library/SKILL.md (a writer subagent per batch), then fm lib check
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lib check passes; each of the 8 deps matches a card's detect — verify with `fm lib check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] detect lines (and a card where none fits)
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `fm lib check && fm lib show vscode-extension && fm lib show xterm` → exit 0 · - [ ] Large output is flow-controlled. / - [ ] Terminal and pty are disposed together. [ran] [tree d18ae4414090] (2026-10-16T01:40:09Z)
- (ac 1) `fm lib check` → exit 0 · 1084 cards, all well-formed (27 related names have no card yet). [ran] [tree d18ae4414090] (2026-10-16T01:40:09Z)
- (audit intent) `self` → API names kept to ones I'm sure of (vsce ls/package, test-electron/test-cli, context.subscriptions, engines.vscode; Terminal.open/write(cb)/onData/onResize, FitAddon.fit, headless buffer.translateToString); all 8 deps match a card [tree d18ae4414090] (2026-10-16T01:40:09Z)
- (ac 1) `fm lib check` → exit 0 · 1084 cards, all well-formed (27 related names have no card yet). [ran] [tree d18ae4414090] (2026-10-16T01:40:10Z)
- (audit intent) `two cards to spec, two detect lines; fm lib check passes` → no invented flags [tree d18ae4414090] (2026-10-16T01:40:10Z)
- (audit self) `two cards to spec, two detect lines; fm lib check passes` → no findings [tree d18ae4414090] (2026-10-16T01:40:10Z)
## Log
- 2026-10-16T01:39:19Z created
- 2026-10-16T01:39:24Z planned from capture
- 2026-10-16T01:39:24Z focused
- 2026-10-16T01:40:11Z done
- 2026-10-16T01:40:11Z committed 1900549 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1016 [FEATURE S, done, 2 steps] Stack cards for the deps scout found: scipy, python-audio (librosa, soundfile, demucs), postprocessing; detect lines for playwright-cor…
- T-1018 [FEATURE S, done, 2 steps] Stack cards: CodeMirror 6 card; tauri-build and tauri-plugin-* on the tauri card; troika-three-text on three-js
- T-1019 [FEATURE S, dropped, 0 steps] Write stack cards for @eslint/js, @fontsource-variable/inter, @fontsource-variable/jetbrains-mono, @lezer/common, @leze…
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
- similar finished tasks took 2–2 steps
## Files touched
- plugin/skills/library/cards/node/vite.md
- plugin/skills/library/cards/web/sveltekit.md
- plugin/skills/library/cards/node/vscode-extension.md
- plugin/skills/library/cards/web/xterm.md
- CHANGELOG.md
