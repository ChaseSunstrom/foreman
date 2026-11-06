---
id: T-1081
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/tests/foreman-ui.test.tsx]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T09:31:59Z
base: ece5a0f319d336c6f5ba9493cdcacd263ae29c6a
base_tree: 83bcad738d72efeff4175392ea54f8c025481b16
plan0_at: 2026-10-16T09:21:02Z
plan0_scope: [mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/tests/foreman-ui.test.tsx]
verified: strong
---
# Colourblind palette and a time scrubber for the pane (catalogue C9 skips, now built)
## Raw request
> FEATURE: Colourblind palette and a time scrubber for the pane (catalogue C9 skips, now built)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
Two pane options: palette 'cb' (colourblind-safe ok/err pair, with every error state also carrying a glyph), and a time scrubber key that steps the pane back through history entries ('as of …') with a live key returning to now.
## Assumptions (confidence)
## Acceptance criteria
- [x] the option `palette: 'cb'` swaps ok/err colours, and the error state still carries a glyph — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
- [x] the scrubber shows the earlier event, and the live key restores now — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
PALETTES in kit.ts chosen by cfg.palette. The scrubber is an index into the history the pane already keeps, with key handling in register.tsx and the option declared in plugin.json. Options considered: a full replay mode (heavy), or OS-level colour filters (not ours).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in `foreman-ui.test.tsx`: with `options.palette 'cb'` the rendered ok/err colours differ from the default, and every err row has a glyph. After the scrubber key the pane shows the previous history entry's id. The live key restores the latest.
2. [x] Add `PALETTES` and `cfg.palette` in `kit.ts` and `state.ts`.
3. [x] Add the key handling and "as of" rendering in `register.tsx`, and declare the option in `.claude-plugin/plugin.json`.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 2 fail / Ran 123 tests across 2 files. [19.53s] [ran] [tree e1713c922a7b] (2026-10-16T09:22:01Z)
- (step 1) `~/.local/bin/claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 123 tests across 2 files. [15.33s] [ran] [tree d6f02c0499c1] (2026-10-16T09:23:40Z)
- (step 2) `~/.local/bin/claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 123 tests across 2 files. [16.74s] [ran] [tree d6f02c0499c1] (2026-10-16T09:23:59Z)
- (step 3) `~/.local/bin/claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 123 tests across 2 files. [15.47s] [ran] [tree d6f02c0499c1] (2026-10-16T09:24:16Z)
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 123 tests across 2 files. [12.47s] [ran] [tree e57430dd8e03] (2026-10-16T09:30:07Z)
- (step 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 123 tests across 2 files. [12.83s] [ran] [tree b8ff976f9660] (2026-10-16T09:30:44Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 123 tests across 2 files. [14.09s] [ran] [tree ba3a4797054f] (2026-10-16T09:30:59Z)
- (ac 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 123 tests across 2 files. [14.09s] [ran] [tree ba3a4797054f] (2026-10-16T09:30:59Z)
- (audit intent) `self review of the branch: setPalette rewrites C.ok/C.err, read at render time; TYPE_COLOR had captured C.err at load so FIX chips stayed red under cb → typeColor reads C.err live; the background-task status line already reads C at render and carries ✓/✗/■; scrubber tested back and live` → colourblind-safe pane and a look back in time [tree ba3a4797054f] (2026-10-16T09:30:59Z)
- (audit edge) `self review of the branch: setPalette rewrites C.ok/C.err, read at render time; TYPE_COLOR had captured C.err at load so FIX chips stayed red under cb → typeColor reads C.err live; the background-task status line already reads C at render and carries ✓/✗/■; scrubber tested back and live` → errors keep a glyph, not colour alone [tree ba3a4797054f] (2026-10-16T09:30:59Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:01:29Z set scope=['mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/hooks/state.ts', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/.claude-plugin/plugin.json', 'mods/foreman-ui/tests/foreman-ui.test.tsx']
- 2026-10-16T05:01:29Z set tier=M
- 2026-10-16T09:20:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1081.builder.md
- 2026-10-16T09:21:02Z focused
- 2026-10-16T09:29:48Z merged worktree-agent-abc1993b281a04e60 (5 file(s))
- 2026-10-16T09:29:52Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abc1993b281a04e60
- 2026-10-16T09:29:53Z focused
- 2026-10-16T09:30:44Z scope: CHANGELOG.md, MASTER.md — docs; mods/foreman-ui/hooks/kit.ts — FIX chips follow the palette
- 2026-10-16T09:31:57Z done
- 2026-10-16T09:31:59Z committed 4717db9 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
## Preflight
Changed in scope since this was planned (2026-10-16): mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/state.ts, mods/foreman-ui/tests/foreman-ui.test.tsx; re-ground the plan against them before editing
## Lessons
- A palette switch must reach every colour read at load time, not only the ones read at render
## Plan gaps
- failed first: step 1 Failing tests in `foreman-ui.test.tsx`: with `options.palette 'cb'` the rendered ok/err colours dif…
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/.claude-plugin/plugin.json
- CHANGELOG.md
- MASTER.md
