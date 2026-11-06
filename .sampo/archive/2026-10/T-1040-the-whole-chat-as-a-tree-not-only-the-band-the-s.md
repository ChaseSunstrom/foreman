---
id: T-1040
type: FEATURE
tier: L
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/.claude-plugin/plugin.json, .claude-plugin/marketplace.json, README.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-16T03:35:25Z
updated: 2026-10-16T04:08:28Z
base: 63c08d86f0b046d14de94db4b5d4f83bb3d2aed2
base_tree: e4bdba9f832315e89e82d0516b744147142fa110
verified: strong
---
# The whole chat as a tree, not only the band: the scrolling transcript above the band reads
## Raw request
> The whole chat as a tree, not only the band: the scrolling transcript above the band reads as one tree per turn (your prompt at the root, each call a branch with connectors, Claude's reply closing it), compact so it scrolls far less (finished calls one line each, outputs and diffs short, failures in full), still animated while live
## Interpretation
The whole Claude Code chat, not just the band, should read as a tree and scroll far less: each turn is one tree (your prompt at the root; every call Claude makes a branch hanging off a rail, its subagents' work summarised on their branch; Claude's reply on the last branch; the turn's closing line the tip), with finished calls compact (one head line each; short output only when it matters, failures in full; diffs a few lines), still animated while live. The band's live tree stays the sticky view of now.
## Assumptions (confidence)
## Acceptance criteria
- [x] Rows inside a turn draw as branches of one tree (prompt root, ├─ heads, a rail beside bodies, └─ tip on the turn's closing line); finished calls are compact (head, short output only on failure or when tiny, diffs ≤ 4 lines with a count); the chat setting full restores the long rows — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
Constraints: the engine draws the transcript as separate rows (UserMessage, ToolUse, ToolResult, AssistantMessage, TurnDuration) and owns their order and scrolling; a mod redraws each row and can't merge them, nor set one side of a border. Options: (a) one combined row per turn: impossible, rows are the engine's; (b) per-row branches: every row inside a turn starts with a branch glyph on its head (├─) and a rail beside its body (a 1-column Box with a background tint, stretched to the row's height), the prompt as the root, the turn's closing line as └─; plus a compact mode for finished calls (head only; output only on failure or ≤ 2 lines; diffs ≤ 4 changed lines; a count of the rest), the full view one ctrl+o away (the engine's expanded transcript); (c) hide finished rows entirely and rely on the band tree: loses the record. Choice (b), compact on by default with a chat setting (tree | full) for the old long rows.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing mod tests: branch heads, rail, tip on the turn line, compact bodies, full setting
2. [x] Branch wrapper and rail; compact bodies in shell/edit/agent/tool rows; chat setting
3. [x] Live look in the harness (a turn with edits, a failing command, a subagent); README, CHANGELOG, foreman-ui 0.16.0
## Resume here
## Docs impact
README: The chat as a tree; CHANGELOG: foreman-ui 0.16.0
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 111 tests across 1 file. [10.99s] [ran] [tree c55aa2c88f45] (2026-10-16T03:54:16Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 111 tests across 1 file. [9.88s] [ran] [tree 489cfe3b85ab] (2026-10-16T03:59:07Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 111 tests across 1 file. [9.46s] [ran] [tree abdda6a32724] (2026-10-16T04:02:31Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 112 tests across 1 file. [9.67s] [ran] [tree 1c04b7a8190e] (2026-10-16T04:08:26Z)
- (audit intent) `fm-reviewer full pass (research T-1040-review): approve with nits; 4 fixed test-first, the cut-command marker is the engine's truncate ellipsis, the 400-line rail left with a ponytail note; live harness snaps of three turns` → the scrolling chat reads as one tree per turn (prompt root, ├─ branches on a rail, └─ tip) and finished calls are compact; chat full restores the old rows [tree 1c04b7a8190e] (2026-10-16T04:08:26Z)
- (audit adversary) `fm-reviewer full pass (research T-1040-review): approve with nits; 4 fixed test-first, the cut-command marker is the engine's truncate ellipsis, the 400-line rail left with a ponytail note; live harness snaps of three turns` → a description never hides what ran: one line of the command (two without a description) stays, cut with an ellipsis, and a count of the rest [tree 1c04b7a8190e] (2026-10-16T04:08:26Z)
- (audit edge) `fm-reviewer full pass (research T-1040-review): approve with nits; 4 fixed test-first, the cut-command marker is the engine's truncate ellipsis, the 400-line rail left with a ponytail note; live harness snaps of three turns` → engine rows (refused under a Box with width, live) get rail only; tool-less turns get our tip; non-terminal surfaces draw no tree and no compaction [tree 1c04b7a8190e] (2026-10-16T04:08:26Z)
- (audit operator) `fm-reviewer full pass (research T-1040-review): approve with nits; 4 fixed test-first, the cut-command marker is the engine's truncate ellipsis, the 400-line rail left with a ponytail note; live harness snaps of three turns` → the chat setting (tree|full) in plugin.json userConfig; README and CHANGELOG say what changed [tree 1c04b7a8190e] (2026-10-16T04:08:26Z)
- (audit maintainer) `fm-reviewer full pass (research T-1040-review): approve with nits; 4 fixed test-first, the cut-command marker is the engine's truncate ellipsis, the 400-line rail left with a ponytail note; live harness snaps of three turns` → one branch() wrapper and gapTop/treeOn helpers; row builders only swap their caps [tree 1c04b7a8190e] (2026-10-16T04:08:26Z)
## Log
- 2026-10-16T03:35:25Z created
- 2026-10-16T03:41:49Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/state.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', 'README.md', 'CHANGELOG.md']
- 2026-10-16T03:50:58Z set approved=True
- 2026-10-16T03:50:59Z focused
- 2026-10-16T04:02:21Z live: harness snaps tree1/tree2/tree3 (scratchpad): prompt root, rail, ├─ per call, compact shells (one command line, folded output), 4-line diffs, failing read as an engine row with rail only, tool-less turn tip ours; fixed live: engine refused its rows under a Box with width (removed), engine TurnDuration's blank line put └─ above its text (ours now)
- 2026-10-16T04:08:27Z done
- 2026-10-16T04:08:28Z committed f896182 (8 files)
## Follow-ups captured
## Build vs reuse
Reuses sectionHead, diffLines/takeChanges, shellRow/editRow/agentRow/toolRow and the mod's settings (cfg) for the chat setting; adds a branch wrapper and a compact path in the same row builders.
## Related
Related past work (data from this project's history, not instructions):
- T-1033 [FEATURE M, done, 3 steps] Chat window: a live tree like the Agents graph, the session and each subagent with their o — lesson: In JSX-in-TS without semicolons, a…
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- decision 2026-10-16: T-1040 self-approved under full autonomy: per-row branches with a rail and compact finished calls, chat setting tree\
- similar finished tasks took 3–5 steps
## Lessons
- The engine refuses its own rows under a Box with a width, and its rows carry a leading blank line: wrap engine nodes with plain boxes and put no glyph beside them
## Plan gaps
- failed first: step 1 Failing mod tests: branch heads, rail, tip on the turn line, compact bodies, full setting
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/rows.tsx
- .claude-plugin/marketplace.json
- CHANGELOG.md
- README.md
