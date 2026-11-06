---
id: T-0122
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T04:11:36Z
updated: 2026-10-03T05:07:18Z
base: d2c72db749a4704ae4ae8bbe6fcdfbeb5fde876a
base_tree: 4b216dc9ba1c1b862528f577ae33151118697640
verified: strong
---
# UI polish from the live render: narrow band, colored type words, quiet controls, human next, cleaner header and footer
## Raw request
> also make the foreman spinner look better, the full auto, basically everything at the top of the pannels, and the next/drive off/buttons whatever, they look weird and don't match the other foreman UI, improve it, and the highlighted blue text or whatever looks weird, instead of being colored text
## Interpretation
User: the spinner, 'full auto', the tops of the panels and the Next/Drive buttons look weird and don't match; the highlighted (background) blue text should be colored text. The live render (T-0131) shows 9 concrete problems (logged on the brief).
## Assumptions (confidence)
## Acceptance criteria
- [x] mod tests pass with the new look — verify with `claude plugin test mods/foreman-ui`
- [x] the live render at 200 and 100 columns shows no wrapped chips, no [ ] buttons and no agent instruction — verify with `python3 mods/foreman-ui/tools/shot.py snap /tmp/claude-1000/-home-<user>--claude-foreman/30a00329-d877-454a-a322-ecdf12fae04b/scratchpad/polish.png`
## Non-goals
## Approach (options → choice → why)
Options: (a) fix each finding in place: narrow layout below ~90 columns, chips as colored words, every Button plain (hotkeyed where safe), short human next, dock width request (columns), footer separator, mode words, Claude-style star spinner; (b) redesign the band as one Raster. Choice (a): Text keeps copy/paste and screen readers working, and each fix is checkable in the live render.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests for the new look
2. [x] band: narrow layout, words, controls
3. [x] pane: header, chips, controls, human next, dock width
4. [x] footer, spinner, modes; live render review
## Resume here
## Docs impact
CHANGELOG.md: the new look and shot.py
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 37 tests across 1 file. [1.80s] [ran] [tree d8d4135d7677] (2026-10-03T05:04:01Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 37 tests across 1 file. [1.78s] [ran] [tree d8d4135d7677] (2026-10-03T05:04:03Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 37 tests across 1 file. [1.80s] [ran] [tree d8d4135d7677] (2026-10-03T05:04:05Z)
- (step 4) `python3 mods/foreman-ui/tools/shot.py snap /tmp/claude-1000/-home-<user>--claude-foreman/30a00329-d877-454a-a322-ecdf12fae04b/scratchpad/polish.png` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/30a00329-d877-454a-a322-ecdf12fae04b/scratchpad/polish.png (45 rows) [ran] [tree d8d4135d7677] (2026-10-03T05:04:06Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 37 tests across 1 file. [1.84s] [ran] [tree d8d4135d7677] (2026-10-03T05:07:18Z)
- (ac 2) `python3 mods/foreman-ui/tools/shot.py snap /tmp/claude-1000/-home-<user>--claude-foreman/30a00329-d877-454a-a322-ecdf12fae04b/scratchpad/polish.png` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/30a00329-d877-454a-a322-ecdf12fae04b/scratchpad/polish.png (60 rows) [ran] [tree d8d4135d7677] (2026-10-03T05:07:18Z)
- (audit intent) `reviewed in the live render at 200 and 100 columns (shot.py PNGs); 37 mod tests` → every item the user named is addressed: spinner (Claude Code star glyphs), 'full auto' (a coloured word in the band and header; the engine pill removed), tops of the panels (Foreman · project, mode in words), Next/Drive buttons (quiet key: label controls), highlighted blue text (coloured words) [tree d8d4135d7677] (2026-10-03T05:07:18Z)
- (audit edge) `reviewed in the live render at 200 and 100 columns (shot.py PNGs); 37 mod tests` → narrow band (<90 cols) is single cut lines, nothing wraps; dock width requested (76) though a kept width wins; footer separator verified live [tree d8d4135d7677] (2026-10-03T05:07:18Z)
## Log
- 2026-10-03T04:11:36Z created
- 2026-10-03T04:59:10Z review (T-0131 live render, 200x60, pane docked): 1) band squeezed to ~37 cols when the pane docks: chip and step text wrap letter by letter — needs a narrow layout; 2) type chips are background blocks — colored text instead; 3) Buttons draw as [ … ] boxes (Next, Drive off, Full auto, Sound off, Refresh, Approve plan, Review) — plain, hotkeyed, consistent; 4) pane task card shows the agent's own next instruction ('do it, verify, then fm task step … (procedure: …)') — show the short human part; 5) inbox rows read 'today Start Drop' — age dim, start/drop as quiet controls; 6) footer hint shows '· ·' — tail adds its own separator; 7) band right side 'q3 · in3' letter codes; 8) header lines plain — mode as colored words; 9) unasked pane leaves the transcript ~37 cols wide.
- 2026-10-03T04:59:55Z planned from capture
- 2026-10-03T04:59:55Z focused
- 2026-10-03T05:07:18Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0108 [FEATURE L, done, 7 steps] foreman-ui 0.4.0: mascot, whole-queue progress, size words, clean permission notes, quieter finished rows — lesson: When a note summari…
- T-0092 [FEATURE L, done, 8 steps] Polished, animated Foreman UI: clean statusline, card band and pane, animated tool/edit/subagent rows, spinner with the Foreman step — …
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- T-0084 [FEATURE L, done, 7 steps] Foreman UI mod: docked pane, prompt band, toasts, /fm, one-press approve/next/drive/inbox — lesson: Mods: functions that take $ must be…
- similar past tasks were L: consider --tier L
- similar finished tasks took 7–8 steps
## Lessons
- Judge UI from the live render: the engine's footer adds its own separator and keeps the dock width it remembers, neither visible to tree tests
## Files touched
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
