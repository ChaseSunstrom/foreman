---
id: T-1090
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/.claude-plugin/plugin.json, .claude-plugin/marketplace.json, README.md, CHANGELOG.md, plugin/lib/ui-demo.json, plugin/tests/test_batch_edit.py]
depends_on: []
source: user
created: 2026-10-16T04:20:28Z
updated: 2026-10-16T04:54:04Z
base: 158bf06cd3c615174447cd55a0e24f3e81f386bd
base_tree: 1bcdd3c216b74a762bab543dd01589c14cc34bf6
verified: strong
---
# Also for the tree UI, theres no bar/gap seperating the this session from the chat UI, and
## Raw request
> Also for the tree UI, theres no bar/gap seperating the this session from the chat UI, and I want the stuff for the SESSION/EACH SUB AGENT THING to hold a FEW inline chat stuff, obviously shrinking the more subagents etc. not MY CHAT, so the this session has a few inlined/sumarrized things for what YOURE doing, and each subagent has its own as WELL, worktrees etc. nott just thte SINGULAR chat UI stuff, etc.
## Interpretation
The live tree above the prompt should carry each node's own story, not just its tool calls: under 'this session' a few lines of what Claude is saying it is doing (its latest narration, summarised), and under each subagent (and a builder in its worktree) its own latest lines, so the person can follow every agent without scrolling the main chat. Fewer lines per node as nodes multiply. A divider separates the tree from the chat above it.
## Assumptions (confidence)
## Acceptance criteria
- [x] the band tree shows a divider above it, the session's and each subagent's latest narration under their nodes (fewer lines with more agents), and a builder's worktree on its node — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
Where the words come from: (a) the transcript rows (AssistantMessage) carry only the main session's text; (b) turn.step, the engine's streaming model-request event, carries every text chunk with the subagent's agentId (absent on main): a pass-through tap that accumulates per agent and keeps each node's last 3 lines; (c) reading session.messages on every frame: expensive. Choice (b): one async generator hook that forwards every chunk unchanged. Drawing: liveTree gains said lines per node (a quote mark in the node's colour, light text) inside the existing row budget: narration keeps one line per node before calls shrink, a second line when there is room; the agent row names its worktree when it has one. A fading rule tops the sticky tree.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: liveTree draws said lines per node within its row budget; the turn.step tap keeps each agent's last lines and forwards chunks unchanged; a tree-rule divider tops the band tree
2. [x] turn.step tap (state.said), summarise in kit, liveTree narration rows, divider
3. [x] Live look in the harness with two subagents; README, CHANGELOG, foreman-ui 0.17.0
## Resume here
T-1090: awaiting fm-reviewer; tests green; docs/0.17.0 written
<!-- auto -->
- 2026-10-16T04:50:09Z step 1/3: Failing tests: liveTree draws said lines per node within its row budget; the turn.step tap keeps each agent's last lines and forwards chunks unchanged; a tree-rule divider tops the band tree
- git: foreman/build; 9 uncommitted: .claude-plugin/marketplace.json, CHANGELOG.md, README.md, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/tests/foreman-ui.test.tsx
- touched since last checkpoint: CHANGELOG.md
## Docs impact
README live tree paragraph; CHANGELOG foreman-ui 0.17.0 and T-1097 line
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 1 test across 1 file. [0.42s] [ran] [tree c8df26ed65ce] (2026-10-16T04:33:02Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 115 tests across 1 file. [11.41s] [ran] [tree d1794cf20aea] (2026-10-16T04:35:08Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 115 tests across 1 file. [10.04s] [ran] [tree 154a373f8ca5] (2026-10-16T04:48:36Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 116 tests across 1 file. [17.91s] [ran] [tree 6cbdbc72a573] (2026-10-16T04:52:54Z)
- (audit intent) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → the session and each subagent show their own latest words under their node, fewer as agents multiply; a builder names its worktree; a rule tops the sticky tree [tree 6cbdbc72a573] (2026-10-16T04:52:54Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → model text reaches the screen only through clean() (escapes, controls, bidi stripped); the tap never alters or holds a chunk [tree 6cbdbc72a573] (2026-10-16T04:52:54Z)
- (audit edge) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → abort/error settles the line; 40-node cap keeps this session; long one-line steps stop accumulating at 400 chars [tree 6cbdbc72a573] (2026-10-16T04:52:54Z)
- (audit operator) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → no extra fm ui refreshes while streaming; README live-tree paragraph and CHANGELOG; foreman-ui 0.17.0 [tree 6cbdbc72a573] (2026-10-16T04:52:54Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → one pass-through turn.step hook, narration() in kit, said in state, liveTree budget extended with kn/ka [tree 6cbdbc72a573] (2026-10-16T04:52:54Z)
- `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 116 tests across 1 file. [18.10s] [ran] [tree 6cbdbc72a573] (2026-10-16T04:53:27Z)
- (audit intent) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → the session and each subagent show their own latest words under their node, fewer as agents multiply; a builder names its worktree; a rule tops the sticky tree [tree 6cbdbc72a573] (2026-10-16T04:53:27Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → model text reaches the screen only through clean() (escapes, controls, bidi stripped); the tap never alters or holds a chunk [tree 6cbdbc72a573] (2026-10-16T04:53:27Z)
- (audit edge) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → abort/error settles the line; 40-node cap keeps this session; long one-line steps stop accumulating at 400 chars [tree 6cbdbc72a573] (2026-10-16T04:53:27Z)
- (audit operator) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → no extra fm ui refreshes while streaming; README live-tree paragraph and CHANGELOG; foreman-ui 0.17.0 [tree 6cbdbc72a573] (2026-10-16T04:53:27Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → one pass-through turn.step hook, narration() in kit, said in state, liveTree budget extended with kn/ka [tree 6cbdbc72a573] (2026-10-16T04:53:27Z)
- `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 116 tests across 1 file. [11.22s] [ran] [tree 6cbdbc72a573] (2026-10-16T04:54:02Z)
- (audit intent) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → the session and each subagent show their own latest words under their node, fewer as agents multiply; a builder names its worktree; a rule tops the sticky tree [tree 6cbdbc72a573] (2026-10-16T04:54:02Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → model text reaches the screen only through clean() (escapes, controls, bidi stripped); the tap never alters or holds a chunk [tree 6cbdbc72a573] (2026-10-16T04:54:02Z)
- (audit edge) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → abort/error settles the line; 40-node cap keeps this session; long one-line steps stop accumulating at 400 chars [tree 6cbdbc72a573] (2026-10-16T04:54:02Z)
- (audit operator) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → no extra fm ui refreshes while streaming; README live-tree paragraph and CHANGELOG; foreman-ui 0.17.0 [tree 6cbdbc72a573] (2026-10-16T04:54:02Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-1090-review): 8 findings fixed test-first (cost on the stream path, per-chunk refresh, eviction, abort, names); live harness snap shows each node's narration; adversary ok (narration runs clean())` → one pass-through turn.step hook, narration() in kit, said in state, liveTree budget extended with kn/ka [tree 6cbdbc72a573] (2026-10-16T04:54:02Z)
## Log
- 2026-10-16T04:20:28Z created
- 2026-10-16T04:21:11Z steer: (screenshot of the band tree with 4 fm-recon subagents) like all of these subagents I want their stuff under them, instead of the singular chatUI above everything — each node (this session, each subagent, worktrees) holds a few lines of its own narration/messages, summarised, shrinking as nodes grow; a divider between the chat and the tree
- 2026-10-16T04:32:09Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/state.ts', 'mods/foreman-ui/types/index.d.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', 'README.md', 'CHANGELOG.md']
- 2026-10-16T04:32:10Z focused
- 2026-10-16T04:37:44Z paused: focus moved to T-1097
- 2026-10-16T04:48:36Z live: harness snap narr4 — the band tree under this session shows '› I'm about to wait 40 seconds…' and '› ok' over its calls; fm ui had been crashing in that folder (T-1097, fixed), which is why earlier snaps showed no band
- 2026-10-16T04:50:02Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T04:50:02Z focused
- 2026-10-16T04:50:03Z scope: CHANGELOG line for T-1097 (its commit left the changelog to this one)
- 2026-10-16T04:50:09Z paused: focus moved to T-1089
- 2026-10-16T04:50:24Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T04:50:24Z focused
- 2026-10-16T04:50:44Z scope: plugin/lib/ui-demo.json — the T-1097 loop line had a trailing space and sat on the brace line (review)
- 2026-10-16T04:52:35Z scope: plugin/tests/test_batch_edit.py is T-1089's red test, parked during this close and restored after, unchanged
- 2026-10-16T04:53:02Z scope: plugin/tests/test_batch_edit.py is T-1089's red test, parked during this close and restored after, unchanged; plugin/lib/ui-demo.json tidied per the review
- 2026-10-16T04:53:50Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/state.ts', 'mods/foreman-ui/types/index.d.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', 'README.md', 'CHANGELOG.md', 'plugin/lib/ui-demo.json', 'plugin/tests/test_batch_edit.py']
- 2026-10-16T04:54:03Z done
- 2026-10-16T04:54:04Z committed 30a4572 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-1033 [FEATURE M, done, 3 steps] Chat window: a live tree like the Agents graph, the session and each subagent with their o — lesson: In JSX-in-TS without semicolons, a…
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- decision 2026-10-06: [costly] fm ask grants stay Claude-Code-only on Codex/Gemini/opencode until T-0336 verifies live whether their prompt hooks fire for agent-written s…
## Lessons
- A hook on a model stream must do bounded work per chunk and never await before the first chunk; repaint from the frame clock, not by marking the view dirty
## Plan gaps
- failed first: step 1 Failing tests: liveTree draws said lines per node within its row budget; the turn.step tap keeps ea…
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/rows.tsx
- .claude-plugin/marketplace.json
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
- plugin/lib/ui-demo.json
- plugin/tests/test_batch_edit.py
