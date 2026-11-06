---
id: T-1780
type: FIX
tier: S
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T11:40:02Z
updated: 2026-10-23T11:57:40Z
base: 5594486cfd6d35e8512a3f6238da702796b17189
base_tree: ad7a791e7a2b73d4dd331dd8eb3a805a9b33f1dc
plan0_at: 2026-10-23T11:56:07Z
plan0_scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
verified: strong
---
# FIX: foreman-ui pane: an options change (motion, chat, …) re-applies the palette without t
## Raw request
> FIX: foreman-ui pane: an options change (motion, chat, …) re-applies the palette without the saved one (T-1717), so the saved colours vanish until fm ui's view next refreshes, which can be long when idle
## Interpretation
applyOptions repaints with setPalette(cfg.palette) and no saved palette, so any options change drops T-1717's saved colours until fm ui's view refreshes; the pane must keep the last palette_custom it was given and pass it on every repaint.
## Assumptions (confidence)
## Acceptance criteria
- [x] a saved palette survives an options change on the next poll, and an explicit palette still wins — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] keep fm ui's palette_custom and pass it on every repaint, test first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 146 tests across 4 files. [11.55s] [ran] [tree 9bd76f438bd8] (2026-10-23T11:56:24Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 146 tests across 4 files. [11.45s] [ran] [tree 7d3f06b5435f] (2026-10-23T11:56:40Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 146 tests across 4 files. [11.48s] [ran] [tree 7d3f06b5435f] (2026-10-23T11:56:53Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 146 tests across 4 files. [11.55s] [ran] [tree 7d3f06b5435f] (2026-10-23T11:57:11Z)
- (audit edge) `self: the pane keeps fm ui's last palette_custom in one module variable, set where the view arrives and used by every repaint (refresh and applyOptions); cleared by a view that has none, as before` → an options change with no new view keeps the saved colours; palette cb or riso still wins; a view without palette_custom clears them as T-1717 did; the poll before the first view has none to keep [tree 7d3f06b5435f] (2026-10-23T11:57:11Z)
- (audit self) `self: the pane keeps fm ui's last palette_custom in one module variable, set where the view arrives and used by every repaint (refresh and applyOptions); cleared by a view that has none, as before` → no findings [tree 7d3f06b5435f] (2026-10-23T11:57:11Z)
## Log
- 2026-10-23T11:40:02Z created
- 2026-10-23T11:41:18Z set tier=S, scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'CHANGELOG.md']
- 2026-10-23T11:56:06Z focused
- 2026-10-23T11:57:38Z done
- 2026-10-23T11:57:40Z committed 796529b7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1574-review: Verdict: changes needed.** One MEDIUM bypass of the guard (in code from T-1496, which the new command calls through) and one MEDIUM test gap. I c…
- T-1717 [FEATURE M, done, 1 steps] Foreman-ui pane: load a custom palette (the JSON fm design tokens --to pane prints) over k — lesson: A key allowlist in TypeScript want…
- research wave2-plan-ab508671842de9f2d: === T-1069 [stale: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts…
- decision 2026-10-21: Accept foreman-ui's supply entry after T-1434 named its hooks module
- similar past tasks were M: consider --tier M
- the similar finished task took 1 steps
## Regression test
foreman-ui.test.tsx: 'a saved palette survives an options change on the next poll (T-1780)': a motion change with fm ui's view unchanged keeps the saved err colour; cb still wins.
## Why not caught
T-1717's tests changed the palette through fm ui's view only, never an option while a saved palette was showing
## Lessons
- State a repaint needs must live where every repaint can read it, not only on the path that first received it
## Plan gaps
- failed first: step 1 keep fm ui's palette_custom and pass it on every repaint, test first
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
- mods/foreman-ui/hooks/register.tsx
