---
id: T-0938
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T20:08:35Z
updated: 2026-10-15T20:35:49Z
base: d3b3bc24083a3762e6cc96f56aebf33032a159d0
base_tree: a7e936a0632d1a867e52ad9f102052b52d1cb37c
verified: ok
---
# Pane stays put: volatile cards hold their height and linger instead of popping in and out
## Raw request
> UI: the pane jumps up and down when panels come and go; keep the layout stable (reserved slots, eased collapse)
## Interpretation
In the foreman-ui pane, cards that come and go with live activity (Now, Subagents, Background shells, the asks card, the failing-gates card) mount and unmount, and their lists grow and shrink, as tool calls start and end. Everything below them then moves up and down several times a second. Done means the pane's vertical layout holds still during a turn: a volatile card keeps its space for a hold window, then gives it back gradually.
## Assumptions (confidence)
## Acceptance criteria
- [x] A card that shrinks or empties keeps its tallest recent height for a hold window, then eases down a row at a time; cards below don't jump — verify with `claude plugin test mods/foreman-ui`
- [x] Now, Subagents and Shells linger dimmed for the hold window after their last item ends instead of vanishing — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Options: A) sticky height plus linger: a small helper in hooks/register.tsx (module-level Map key → {rows, at}) gives each volatile card minHeight = the most rows it drew within HOLD_MS (8 s, in hooks/state.ts). After the hold, it steps down one row per second. A card whose list empties keeps rendering dimmed ('idle · last: <verb> <target> · Ns ago') until its hold ends. B) merge Now, Subagents and Shells into one fixed-height Live card that is always present: stable, but it wastes rows when idle and loses the headings. C) move volatile cards to the bottom: stable, but the user asked for the important things on top. D) animate height changes: the engine has no layout transitions, so it would mean per-frame rerenders.
Chosen: A. It keeps the order and headings and is a small diff. The hold applies under every Motion setting, because it is about stability, not animation.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing mod tests: a shrinking list keeps its height inside the hold, a finished call lingers
2. [x] A stable(key, rows) helper with hold and step-down; apply to Now, Subagents, Shells, asks, gates
3. [x] Re-record the pane shot and check by eye
## Resume here
## Docs impact
README.md pane description: the Now line says live cards hold their place
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 2 fail / Ran 82 tests across 1 file. [6.46s] [ran] [tree ea1f42f77e1f] (2026-10-15T20:22:08Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 83 tests across 1 file. [8.40s] [ran] [tree d636c2e66b93] (2026-10-15T20:25:03Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 83 tests across 1 file. [8.35s] [ran] [tree 20970513ad58] (2026-10-15T20:32:39Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 83 tests across 1 file. [8.36s] [ran] [tree 20970513ad58] (2026-10-15T20:32:49Z)
- (step 3) `mods/foreman-ui/tools/shot.py snaps every 3 s through a two-call haiku turn (scratchpad ui-1..8.png)` → Now held its rows between the calls with 'idle · last: … · Ns ago', then left about 8 s after the last call; Plan and later cards did not move [tree 20970513ad58] (2026-10-15T20:35:17Z)
- `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 1 test across 1 file. [0.18s] (start tree + this task's tests) [ran] [tree 20970513ad58] (2026-10-15T20:35:27Z)
- `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 83 tests across 1 file. [8.30s] [ran] [tree 20970513ad58] (2026-10-15T20:35:27Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 83 tests across 1 file. [8.32s] [ran] [tree 9bf8ae6ab07a] (2026-10-15T20:35:48Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 83 tests across 1 file. [8.32s] [ran] [tree 9bf8ae6ab07a] (2026-10-15T20:35:48Z)
- (audit intent) `main-thread review of the 127-line diff (stable/settle helpers, per-card minHeight, idle lingers, tick redraw while held) plus a live tmux shot sequence` → ok: Now held between calls and lingered dimmed, seen live at 3 s intervals [tree 9bf8ae6ab07a] (2026-10-15T20:35:48Z)
- (audit edge) `main-thread review of the 127-line diff (stable/settle helpers, per-card minHeight, idle lingers, tick redraw while held) plus a live tmux shot sequence` → ok with a known limit: an emptied card's last 4 rows leave in one step when its hold ends; asks height is an estimate (a floor) [tree 9bf8ae6ab07a] (2026-10-15T20:35:48Z)
- (audit operator) `main-thread review of the 127-line diff (stable/settle helpers, per-card minHeight, idle lingers, tick redraw while held) plus a live tmux shot sequence` → ok: no setting needed; applies under every Motion setting [tree 9bf8ae6ab07a] (2026-10-15T20:35:48Z)
- (audit maintainer) `main-thread review of the 127-line diff (stable/settle helpers, per-card minHeight, idle lingers, tick redraw while held) plus a live tmux shot sequence` → ok: HOLD_MS/STEP_MS in state.ts, helpers exported and unit-tested [tree 9bf8ae6ab07a] (2026-10-15T20:35:48Z)
## Log
- 2026-10-15T20:08:35Z created
- 2026-10-15T20:17:07Z planned from capture
- 2026-10-15T20:17:19Z criterion 1 verify: `cd mods/foreman-ui && bun test` → `claude plugin test mods/foreman-ui`
- 2026-10-15T20:17:19Z criterion 2 verify: `cd mods/foreman-ui && bun test` → `claude plugin test mods/foreman-ui`
- 2026-10-15T20:18:30Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0938.builder.md
- 2026-10-15T20:19:15Z focused
- 2026-10-15T20:32:28Z merged worktree-agent-a4ab92edb7a6bde69 (3 file(s))
- 2026-10-15T20:32:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4ab92edb7a6bde69
- 2026-10-15T20:32:29Z focused
- 2026-10-15T20:35:49Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- research T-0909-review: Verdict: changes needed.** The 14-day bars are wrong on this repo today, and the pane order does not match the third acceptance criterion. I coul…
- playbook Terminal and mod UI (skills/playbooks/references/ui/terminal-ui.md)
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
- similar past tasks were L: consider --tier L
- the similar finished task took 6 steps
## Why not caught
none: layout motion only shows in a live pane over time; the new hold tests drive the clock through it
## Lessons
- Layout stability is a time property: test it by driving the clock through the hold, and confirm with a live shot sequence, not one frame.
## Plan gaps
- failed first: step 1 Failing mod tests: a shrinking list keeps its height inside the hold, a finished call lingers
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/hooks/register.tsx
- README.md
