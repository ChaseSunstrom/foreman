---
id: T-1023
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/.claude-plugin/plugin.json, .claude-plugin/marketplace.json, plugin/lib/fmwatch.py, plugin/lib/ui-demo.json, plugin/tests/test_ui.py, README.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-16T01:45:27Z
updated: 2026-10-16T02:00:17Z
base: 2a28715b6c3b10c825f73683cbbf8afa10309d1d
base_tree: 01b8e4bdd7a2602f09b650e5ea8957d24893b63b
verified: strong
---
# Can you have a graph of sub agents/worktrees/brainstorms?
## Raw request
> can you have a graph of sub agents/worktrees/brainstorms?
## Interpretation
An Agents section in the pane: a Gantt on its own adaptive time axis with one row per subagent (this session's, running and recently finished), per git worktree (a builder's joins its agent's row by the worktree-agent-<id> branch; a lone or stale worktree gets a dim row), and per brainstorm (fm ideas: answers as dots). Bars span start→end/now; braille dots mark tool calls; the right column names it and says running/quiet/done, with ■ stop where it was. Hidden when there is nothing.
## Assumptions (confidence)
## Acceptance criteria
- [x] the pane draws an Agents Gantt for running/finished subagents, worktrees and a brainstorm, hidden when none, still filling the dock — verify with `cd mods/foreman-ui && claude plugin test .`
- [x] fm ui --json lists the project's worktrees with branch, task and agent id — verify with `python3 plugin/tests/run.py test_ui`
## Non-goals
## Approach (options → choice → why)
(a) extend the Activity 'agent' lane into per-agent sub-rows: no room for names, Activity height would change; (b) a separate Agents section with its own axis (chosen: bars fill the width even for 2-minute agents, names fit, appears only with agents); (c) a node graph of tasks/lanes: reads poorly in 74 columns. Data: LiveAgent gains endedAt and call times; finished agents kept for the window; fm ui adds worktrees from git worktree list; brainstorm answer times recorded by the mod as counts rise.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: Agents rows from agents, worktrees and a brainstorm; hidden when none; layout still fills the dock
2. [x] fm ui worktrees (path, branch, task, agent id, created); LiveAgent endedAt and call times; brainstorm answer times
3. [x] render the Agents Gantt (terminal raster + text twin), link builder worktrees to agents, stop button
4. [x] look at it live with a real subagent and a worktree; README, CHANGELOG, foreman-ui 0.12.0
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ui` → ✗ exit 1 · Ran 22 tests in 8.4s (7 classes, 16 at a time; slowest: UiView 8s, UiSkills 1s, SkillRoute 1s) / FAILED (1 classes) [ran] [tree bcc9fed3bf65] (2026-10-16T01:46:12Z)
- (ac 2) `python3 plugin/tests/run.py test_ui test_board_surfaces` → exit 0 · Ran 28 tests in 8.5s (7 classes, 16 at a time; slowest: UiView 8s, BoardSurfaces 2s, UiSkills 1s) / OK [ran] [tree baf790d1c89a] (2026-10-16T01:47:25Z)
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test . && cd ../.. && python3 plugin/tests/run.py test_ui test_board_surfaces` → exit 0 · Ran 28 tests in 8.5s (7 classes, 16 at a time; slowest: UiView 8s, BoardSurfaces 2s, UiSkills 1s) / OK [ran] [tree b1d907a500d2] (2026-10-16T01:51:03Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 96 tests across 1 file. [7.46s] [ran] [tree b1d907a500d2] (2026-10-16T01:51:19Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 96 tests across 1 file. [7.40s] [ran] [tree b1d907a500d2] (2026-10-16T01:51:27Z)
- (step 4) `test -s /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/ui-agents2.png && grep -q 'T-1023' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 2fccac9820f8] (2026-10-16T01:52:06Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 96 tests across 1 file. [7.58s] [ran] [tree 2fccac9820f8] (2026-10-16T01:52:14Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 3 fail / Ran 98 tests across 1 file. [7.81s] [ran] [tree 467b0aaaf836] (2026-10-16T01:55:42Z)
- (ac 2) `python3 plugin/tests/run.py test_ui test_board_surfaces` → exit 0 · Ran 28 tests in 8.8s (7 classes, 16 at a time; slowest: UiView 9s, BoardSurfaces 2s, UiSkills 1s) / OK [ran] [tree 5784ae3e4edb] (2026-10-16T01:56:36Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 98 tests across 1 file. [8.20s] [ran] [tree 5784ae3e4edb] (2026-10-16T01:56:45Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 98 tests across 1 file. [8.57s] [ran] [tree 5784ae3e4edb] (2026-10-16T01:56:54Z)
- (audit intent) `fm-reviewer` → aging-out at render and finished-before-worktree ranking fixed test-first; Agents section reads as the user asked: subagents, worktrees and brainstorms on one Gantt [tree 5784ae3e4edb] (2026-10-16T01:59:52Z)
- (audit edge) `fm-reviewer` → bar-at-now, narrow-dock stop button, detached worktree state, worktree cap order: fixed with tests; pre-load brainstorm stamps left (cosmetic) [tree 5784ae3e4edb] (2026-10-16T01:59:52Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 98 tests across 1 file. [8.28s] [ran] [tree 5784ae3e4edb] (2026-10-16T02:00:10Z)
- (ac 2) `python3 plugin/tests/run.py test_ui` → exit 0 · Ran 22 tests in 8.7s (7 classes, 16 at a time; slowest: UiView 9s, UiSkills 1s, SkillRoute 1s) / OK [ran] [tree 5784ae3e4edb] (2026-10-16T02:00:10Z)
- (audit edge) `fm-reviewer pass (intent, edge) + live render with a real Explore subagent and a leftover worktree` → aging, ranking, narrow dock, bar at now, detached worktrees, newest-first cap [tree 5784ae3e4edb] (2026-10-16T02:00:10Z)
- (audit intent) `fm-reviewer pass (intent, edge) + live render with a real Explore subagent and a leftover worktree` → one Gantt for subagents, worktrees and brainstorms, hidden when none [tree 5784ae3e4edb] (2026-10-16T02:00:10Z)
- (audit edge) `fm-reviewer pass (intent, edge) + live render with a real Explore subagent and a leftover worktree` → aging, ranking, narrow dock, bar at now, detached worktrees, newest-first cap [tree 5784ae3e4edb] (2026-10-16T02:00:16Z)
- (audit intent) `fm-reviewer pass (intent, edge) + live render with a real Explore subagent and a leftover worktree` → one Gantt for subagents, worktrees and brainstorms, hidden when none [tree 5784ae3e4edb] (2026-10-16T02:00:16Z)
## Log
- 2026-10-16T01:45:27Z created
- 2026-10-16T01:45:38Z focused
- 2026-10-16T01:52:06Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/types/index.d.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', 'plugin/lib/fmwatch.py', 'plugin/lib/ui-demo.json', 'plugin/tests/test_ui.py', 'README.md', 'CHANGELOG.md']
- 2026-10-16T01:59:35Z the user's pane went blank after /reload-plugins mid-turn and came back when the session reopened; a probe render of the real fm ui view at 30 sizes, idle and live, passed in the test engine, so not the code
- 2026-10-16T02:00:16Z scope: tests/zz-probe.test.tsx, zz-view.json and zz-view.ts were a throwaway probe for the blank-pane report, moved out to the scratchpad; nothing of them is committed
- 2026-10-16T02:00:16Z done
- 2026-10-16T02:00:17Z committed 5dd2e84 (11 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0137 [FEATURE M, done, 3 steps] Everything in the chat: shell rows with their output formatted inline, folded command groups unfolded, the pane's Output card gone — le…
- playbook Terminal and mod UI (skills/playbooks/references/ui/terminal-ui.md)
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- similar finished tasks took 3–6 steps
## Lessons
- A list kept for a time window must be filtered at every draw, not only when something new arrives: the retention filter ran only on the next agent's spawn, so a quiet session kept finished agents forever.
## Plan gaps
- failed first: step 1 test-first: Agents rows from agents, worktrees and a brainstorm; hidden when none; layout still fil…
## Files touched
- plugin/tests/test_ui.py
- plugin/lib/fmwatch.py
- plugin/lib/ui-demo.json
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- .claude-plugin/marketplace.json
- CHANGELOG.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/tests/zz-probe.test.tsx
- mods/foreman-ui/tests/zz-view.json
- mods/foreman-ui/tests/zz-view.ts
