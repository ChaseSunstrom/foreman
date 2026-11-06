---
id: T-1033
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, README.md, CHANGELOG.md, mods/foreman-ui/.claude-plugin/plugin.json, .claude-plugin/marketplace.json]
depends_on: []
source: user
created: 2026-10-16T02:54:05Z
updated: 2026-10-16T03:23:33Z
base: 7afe459eae71efd28d67f01df73a2ea6428f3865
base_tree: aa1461d237cf7162c731f1f93b516d80b3546ae6
verified: strong
---
# Chat window: a live tree like the Agents graph, the session and each subagent with their o
## Raw request
> Chat window: a live tree like the Agents graph, the session and each subagent with their own commands and changes under them and a one-line summary of what each is doing, animated, all in one place so the chat doesn't have to scroll; the band above the prompt stays put while the chat scrolls
## Interpretation
One place that shows everything happening now, so the person doesn't chase it up the scrolling chat: a live tree pinned above the prompt (Claude Code's band, which stays put while the chat scrolls): this session at the root with its task and step and a one-line summary of what it is doing, its latest calls under it with how each went, then a branch per running subagent with its own latest calls and what it is on, animated while work runs. It is the 'more than the right pane' view (T-1027 merged in): with the pane docked it is the band's whole job, with no repeat of the pane.
## Assumptions (confidence)
## Acceptance criteria
- [x] With work running, the band draws a tree: the session root (task, step, current call), its latest calls with marks, and a branch per running subagent with its own latest calls; connectors join them; it fits maxRows — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
- [x] With the pane docked the band shows the tree (not hidden); idle it shrinks to one summary line — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
Options: (a) a second pane: a tab in the same dock, never on screen with the first; (b) restructure the transcript itself: the engine owns its rows and order, a mod can only redraw each one; (c) the AbovePrompt band as a live tree (root: session/task/step/now, its last 3 calls; a branch per running subagent with its last 2 calls and its current call; ✓/✗/spinner per call; a comet on the root's rule while live; capped to the band's maxRows, oldest calls dropping first; idle: one summary line of the last turn). Choice (c). LiveAgent grows a short recent-calls list; the session's own calls come from the ticks it already keeps. With the pane closed the band keeps its card and the tree goes under it when there's room.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing mod tests: band tree with root, calls, agent branches, connectors, row cap; docked pane keeps it; idle line
2. [x] Per-agent recent calls in LiveAgent; tree builder (pure, in kit/rows) and the band render
3. [x] Live look in the harness with two subagents; README, CHANGELOG, foreman-ui 0.15.0
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 2 fail / Ran 107 tests across 1 file. [8.95s] [ran] [tree 1ed6f26bd3b6] (2026-10-16T03:13:17Z)
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 107 tests across 1 file. [8.88s] [ran] [tree bd4f736d68c1] (2026-10-16T03:15:17Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 107 tests across 1 file. [9.05s] [ran] [tree bd4f736d68c1] (2026-10-16T03:15:27Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 107 tests across 1 file. [8.82s] [ran] [tree 48c97c64b9b6] (2026-10-16T03:17:00Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 108 tests across 1 file. [9.09s] [ran] [tree 66d68c1277d3] (2026-10-16T03:21:17Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 108 tests across 1 file. [9.09s] [ran] [tree 66d68c1277d3] (2026-10-16T03:23:32Z)
- (ac 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 108 tests across 1 file. [9.09s] [ran] [tree 66d68c1277d3] (2026-10-16T03:23:32Z)
- (audit intent) `one fm-reviewer pass; all findings fixed test-first (idle summary line, card-aware row budget, ✗ for a thrown call, task cut not dropped, feed reset per session, clean text); two bugs of my own caught by the new tests (slice(-0) returning everything, a line starting with '(' parsed as a call); live in the 200x55 harness with the pane closed and docked (tree1-3.png)` → the session root, its latest calls and a branch per subagent with its own calls, spinners then ✓/✗ with times, on screen above the prompt while the chat scrolls; seen live in both layouts [tree 66d68c1277d3] (2026-10-16T03:23:32Z)
- (audit edge) `one fm-reviewer pass; all findings fixed test-first (idle summary line, card-aware row budget, ✗ for a thrown call, task cut not dropped, feed reset per session, clean text); two bugs of my own caught by the new tests (slice(-0) returning everything, a line starting with '(' parsed as a call); live in the 200x55 harness with the pane closed and docked (tree1-3.png)` → fits maxRows (agents keep a call, older session calls go, agents fold into a count); a thrown call is ✗; idle shrinks to one line; a new session starts empty [tree 66d68c1277d3] (2026-10-16T03:23:32Z)
- (audit operator) `one fm-reviewer pass; all findings fixed test-first (idle summary line, card-aware row budget, ✗ for a thrown call, task cut not dropped, feed reset per session, clean text); two bugs of my own caught by the new tests (slice(-0) returning everything, a line starting with '(' parsed as a call); live in the 200x55 harness with the pane closed and docked (tree1-3.png)` → foreman-ui 0.15.0 in plugin.json and marketplace.json; README and CHANGELOG; no new settings [tree 66d68c1277d3] (2026-10-16T03:23:32Z)
- (audit maintainer) `one fm-reviewer pass; all findings fixed test-first (idle summary line, card-aware row budget, ✗ for a thrown call, task cut not dropped, feed reset per session, clean text); two bugs of my own caught by the new tests (slice(-0) returning everything, a line starting with '(' parsed as a call); live in the 200x55 harness with the pane closed and docked (tree1-3.png)` → TREE_MS in state.ts; liveTree pure over feed and agents; tests for the tree, its budget, idle line and thrown calls [tree 66d68c1277d3] (2026-10-16T03:23:32Z)
- (audit adversary) `one fm-reviewer pass; all findings fixed test-first (idle summary line, card-aware row budget, ✗ for a thrown call, task cut not dropped, feed reset per session, clean text); two bugs of my own caught by the new tests (slice(-0) returning everything, a line starting with '(' parsed as a call); live in the 200x55 harness with the pane closed and docked (tree1-3.png)` → text through clean(); nothing runs from the tree; no new inputs [tree 66d68c1277d3] (2026-10-16T03:23:32Z)
## Log
- 2026-10-16T02:54:05Z created
- 2026-10-16T03:12:08Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/state.ts', 'mods/foreman-ui/types/index.d.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'README.md', 'CHANGELOG.md', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json']
- 2026-10-16T03:12:08Z focused
- 2026-10-16T03:23:33Z done
- 2026-10-16T03:23:33Z committed fc9c6af (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- decision 2026-10-06: [costly] fm ask grants stay Claude-Code-only on Codex/Gemini/opencode until T-0336 verifies live whether their prompt hooks fire for agent-written s…
## Lessons
- In JSX-in-TS without semicolons, a statement that starts with '(' continues the line before it: name the value first (const shown = …) instead of starting a line with a parenthesised expression.
## Plan gaps
- failed first: step 1 Failing mod tests: band tree with root, calls, agent branches, connectors, row cap; docked pane kee…
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/hooks/rows.tsx
- CHANGELOG.md
- README.md
- .claude-plugin/marketplace.json
- mods/foreman-ui/.claude-plugin/plugin.json
