---
id: T-1016
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: scout
created: 2026-10-16T01:34:32Z
updated: 2026-10-16T01:37:26Z
base: 4c98791f8db9b29c6c14b1a5ff7cd339bb6a233e
base_tree: 93a2a358d353a9c9827ec1e472fa1842a21bd8b0
verified: strong
---
# Stack cards for the deps scout found: scipy, python-audio (librosa, soundfile, demucs), postprocessing; detect lines for playwright-core, vite-plugin-svelte, svelte-check
## Raw request
> Found by fm scout: dependencies in your projects with no stack card: @sveltejs/vite-plugin-svelte, demucs, librosa, playwright-core, postprocessing, scipy, soundfile, svelte-check. Write one card each to the spec in plugin/skills/library/SKILL.md (a writer subagent per batch), then fm lib check
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lib check passes and fm lib finds a card for each of the 8 deps — verify with `fm lib check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] detect lines on playwright and svelte cards; three new cards to the SKILL.md spec
2. [x] fm lib check; fm lib for each dep
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `plugin/bin/fm lib check` → exit 0 · 1081 cards, all well-formed (27 related names have no card yet). [ran] [tree ee11d52fed04] (2026-10-16T01:36:03Z)
- (step 2) `plugin/bin/fm lib show postprocessing` → exit 0 · - [ ] The composer is disposed on teardown. / - [ ] A browser smoke test confirms the canvas renders. [ran] [tree ee11d52fed04] (2026-10-16T01:36:03Z)
- (step 1) `fm lib check` → exit 0 · 1081 cards, all well-formed (27 related names have no card yet). [ran] [tree 5b0764f187ec] (2026-10-16T01:37:23Z)
- (step 2) `fm lib show scipy && fm lib show python-audio && fm lib show postprocessing` → exit 0 · - [ ] The composer is disposed on teardown. / - [ ] A browser smoke test confirms the canvas renders. [ran] [tree 5b0764f187ec] (2026-10-16T01:37:24Z)
- (ac 1) `fm lib check` → exit 0 · 1081 cards, all well-formed (27 related names have no card yet). [ran] [tree 5b0764f187ec] (2026-10-16T01:37:24Z)
- (audit intent) `self` → spot-checked the builder's flagged claims (librosa keyword-only rates since 0.10, SMAAEffect and composer multisampling, scipy.misc removed); all 8 deps now have a card by detect [tree 176dac4a4b4d] (2026-10-16T01:37:24Z)
- (ac 1) `fm lib check` → exit 0 · 1081 cards, all well-formed (27 related names have no card yet). [ran] [tree 176dac4a4b4d] (2026-10-16T01:37:25Z)
- (audit intent) `cards read in full; fm lib check passes in main` → every scout-found dep covered, 3 by detect lines, 5 by new cards [tree 176dac4a4b4d] (2026-10-16T01:37:25Z)
- (audit self) `cards read in full; fm lib check passes in main` → no findings [tree 176dac4a4b4d] (2026-10-16T01:37:25Z)
## Log
- 2026-10-16T01:34:32Z created
- 2026-10-16T01:34:57Z planned from capture
- 2026-10-16T01:34:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1016.builder.md
- 2026-10-16T01:35:06Z focused
- 2026-10-16T01:37:13Z merged worktree-agent-a1a1c7565b48aa2b9 (5 file(s))
- 2026-10-16T01:37:14Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1a1c7565b48aa2b9
- 2026-10-16T01:37:14Z focused
- 2026-10-16T01:37:26Z done
- 2026-10-16T01:37:26Z committed 9941b64 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0933 [FEATURE L, done, 5 steps] Stack library: 400+ on-demand implementation cards (fm lib) plus federated search over installed plugins' skills — lesson: Subagent-wri…
- T-0939 [FEATURE M, done, 3 steps] Pane shows skill use: skills invoked, stack cards read, and this repo's suggested cards — lesson: A mechanical sed over JSX props must …
- research T-0933-review: Changes needed. The code works and the 22 cards I sampled are accurate. Detect signals produce false-positive suggestions, and one manifest regex…
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
## Files touched
- plugin/skills/library/cards/web/playwright.md
- plugin/skills/library/cards/web/svelte.md
- plugin/skills/library/cards/python/scipy.md
- plugin/skills/library/cards/python/python-audio.md
- plugin/skills/library/cards/web/postprocessing.md
- CHANGELOG.md
