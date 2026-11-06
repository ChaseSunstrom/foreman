---
id: T-1039
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, README.md, CHANGELOG.md, mods/foreman-ui/.claude-plugin/plugin.json, .claude-plugin/marketplace.json]
depends_on: []
source: user
created: 2026-10-16T03:29:52Z
updated: 2026-10-16T03:39:42Z
base: fc9c6af91ad056b43bb9587f687fda59a255cb7d
base_tree: 07b0e3fba2f5bcd83abf9e2e6f6a56f991d1f524
verified: strong
---
# Band tree polish (screenshot 22:28): sticky, fixed height while work runs so the chat neve
## Raw request
> Band tree polish (screenshot 22:28): sticky, fixed height while work runs so the chat never shifts, room under it; a tree like the pane's Agents graph (each node's time bar in one column); no duplicate status lines above it (the spinner line repeats the root)
## Interpretation
In the user's screenshot the tree sits flush at the bottom, grows a row at a time (so the chat jumps), repeats what the lines above it already say (the Foreman spinner line names the task, step and time again), and reads as a plain list. Make it sticky: a fixed height for the whole turn with a blank row under it; make it look like the pane's Agents graph (each node's time bar in one aligned column on a shared axis); and drop the duplicate spinner line while the tree is on screen.
## Assumptions (confidence)
## Acceptance criteria
- [x] While work runs the band tree keeps one height all turn (padded, a blank row under it), each node has a time bar in one aligned column, and the Foreman spinner line is not drawn while the tree is — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
Options: (a) pad the tree to the band's maxRows: tall and mostly empty; (b) a fixed height for the turn: the most rows the tree has needed this turn (at least 5, at most maxRows - 1), padded, plus a blank row; it never shrinks mid-turn; (c) let the engine scroll the band: still moves. Choice (b). Bars: ganttCells over [turn start, now] (calls: start→end; agents: their calls as dots; root: all session calls), gw = a quarter of the width, in one column like the pane. The Spinner row renders nothing while the band tree is live (the root line carries the same facts).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing mod tests: fixed height across redraws as calls arrive; bars in one column; spinner silent while the tree shows
2. [x] Sticky height, gantt bars, spinner suppression
3. [x] Live look in the harness; CHANGELOG, foreman-ui 0.15.1
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 1 fail / Ran 109 tests across 1 file. [9.07s] [ran] [tree 03157d9187b1] (2026-10-16T03:31:13Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 109 tests across 1 file. [9.22s] [ran] [tree bb2e58b52bd0] (2026-10-16T03:32:36Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 109 tests across 1 file. [9.13s] [ran] [tree ba7d1ea07f4d] (2026-10-16T03:34:04Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 109 tests across 1 file. [9.12s] [ran] [tree 076c94af3895] (2026-10-16T03:37:35Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 109 tests across 1 file. [9.33s] [ran] [tree 076c94af3895] (2026-10-16T03:39:40Z)
- (audit intent) `one fm-reviewer pass; the HIGH (bars not in one column) and MEDIUM (spinner blanked without a tree) fixed test-first, the test tightened; live in the 200x55 harness (sticky2/3: bars per node, blank rows under the tree, no spinner line)` → one height all turn with blank rows under it, a time bar per node in one column, the duplicate spinner line gone while the tree shows; seen live [tree 076c94af3895] (2026-10-16T03:39:40Z)
- (audit edge) `one fm-reviewer pass; the HIGH (bars not in one column) and MEDIUM (spinner blanked without a tree) fixed test-first, the test tightened; live in the 200x55 harness (sticky2/3: bars per node, blank rows under the tree, no spinner line)` → the spinner returns when the band can't draw the tree or the engine has a message; idle shrinks to one line; height resets each turn [tree 076c94af3895] (2026-10-16T03:39:40Z)
- (audit operator) `one fm-reviewer pass; the HIGH (bars not in one column) and MEDIUM (spinner blanked without a tree) fixed test-first, the test tightened; live in the 200x55 harness (sticky2/3: bars per node, blank rows under the tree, no spinner line)` → foreman-ui 0.15.1 in plugin.json and marketplace.json; README and CHANGELOG [tree 076c94af3895] (2026-10-16T03:39:40Z)
- (audit maintainer) `one fm-reviewer pass; the HIGH (bars not in one column) and MEDIUM (spinner blanked without a tree) fixed test-first, the test tightened; live in the 200x55 harness (sticky2/3: bars per node, blank rows under the tree, no spinner line)` → fixed right cell (RW) documented; treeDrawn set where the tree is drawn [tree 076c94af3895] (2026-10-16T03:39:40Z)
- (audit adversary) `one fm-reviewer pass; the HIGH (bars not in one column) and MEDIUM (spinner blanked without a tree) fixed test-first, the test tightened; live in the 200x55 harness (sticky2/3: bars per node, blank rows under the tree, no spinner line)` → no new inputs; text through clean() [tree 076c94af3895] (2026-10-16T03:39:40Z)
## Log
- 2026-10-16T03:29:52Z created
- 2026-10-16T03:30:15Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/state.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'README.md', 'CHANGELOG.md', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json']
- 2026-10-16T03:30:15Z focused
- 2026-10-16T03:39:41Z done
- 2026-10-16T03:39:42Z committed 38d75dc (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- research T-1026-review: MEDIUM** `mods/foreman-ui/hooks/register.tsx:1736-1742` — the Agents bars do not stay in one column when a stop button shows. [stale: mods/forema…
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
## Lessons
- Right-anchored columns line up only if every row's trailing cell has the same fixed width; size the cell, not the bar.
## Plan gaps
- failed first: step 1 Failing mod tests: fixed height across redraws as calls arrive; bars in one column; spinner silent …
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/rows.tsx
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
- README.md
- .claude-plugin/marketplace.json
- mods/foreman-ui/.claude-plugin/plugin.json
