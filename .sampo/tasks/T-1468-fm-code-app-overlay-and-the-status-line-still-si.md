---
id: T-1468
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: [T-1302]
source: discovered
created: 2026-10-22T15:52:37Z
updated: 2026-10-22T16:52:53Z
base: 510eee3f2c294a30a038211bf9283b4fb7752322
base_tree: c581526c021e27f8ac2ad61ab7e875e6a6d5ce38
plan0_at: 2026-10-22T16:28:55Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# fm code app: overlay and status line measured in columns
## Raw request
> fm code app: _overlay and the status line still size text with len() (fmcodetui ~890, width = sum(len(t) ...)), so a wide glyph there overflows; use width() as T-1431 did for the track and box titles
## Interpretation
After T-1431, fmcodetui's _overlay and the status line still size text with len() (~890: width = sum(len(t) …)), so a wide glyph there overflows its line.
## Assumptions (confidence)
## Acceptance criteria
- [x] an overlay and a status line holding wide glyphs stay within the screen width — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_overlay_and_status_measure_columns`
## Non-goals
## Approach (options → choice → why)
Replace those len() measures with the module's width() helper, as T-1431 did; truncate with the same column-aware fit.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] width() in _overlay and the status line
## Resume here
<!-- auto -->
- 2026-10-22T16:28:59Z step 1/2: failing test
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_overlay_and_status_measure_columns` → ✗ exit 1 · Ran 1 test in 0.077s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 0d8e9d5f7783] (2026-10-22T16:51:43Z)
- `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_overlay_and_status_measure_columns` → ✗ exit 1 · Ran 1 test in 0.003s / FAILED (errors=1) [ran] [tree 0d8e9d5f7783] (2026-10-22T16:51:43Z)
- `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_overlay_and_status_measure_columns` → ✗ exit 1 · Ran 1 test in 0.030s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree e31b97d7b7ae] (2026-10-22T16:52:02Z)
- `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_overlay_and_status_measure_columns` → exit 0 · Ran 1 test in 0.005s / OK [ran] [tree e31b97d7b7ae] (2026-10-22T16:52:02Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui.Width` → exit 0 · Ran 6 tests in 0.079s / OK [ran] [tree e31b97d7b7ae] (2026-10-22T16:52:15Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.Width` → exit 0 · Ran 6 tests in 0.129s / OK [ran] [tree e31b97d7b7ae] (2026-10-22T16:52:16Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_overlay_and_status_measure_columns` → exit 0 · Ran 1 test in 0.003s / OK [ran] [tree e31b97d7b7ae] (2026-10-22T16:52:17Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_overlay_and_status_measure_columns` → exit 0 · Ran 1 test in 0.002s / OK [ran] [tree a4b6094c29a0] (2026-10-22T16:52:30Z)
- (audit edge) `self: four len()→width()/pad() swaps (_focus_line, the selected log row, _welcome chips, status hints); the _welcome locals renamed (pad→left, width→used) so the module helpers aren't shadowed; Canvas.put already clips by columns, so the visible bug was over-padding plus fit's ellipsis; test_code_tui green` → an ASCII line pads exactly as before (width == len); a combining accent fills no column, so pad gives it one more space than ljust did — correct [tree a4b6094c29a0] (2026-10-22T16:52:30Z)
- (audit self) `self: four len()→width()/pad() swaps (_focus_line, the selected log row, _welcome chips, status hints); the _welcome locals renamed (pad→left, width→used) so the module helpers aren't shadowed; Canvas.put already clips by columns, so the visible bug was over-padding plus fit's ellipsis; test_code_tui green` → no findings [tree a4b6094c29a0] (2026-10-22T16:52:30Z)
## Log
- 2026-10-22T15:52:37Z created
- 2026-10-22T16:00:05Z planned from capture
- 2026-10-22T16:00:25Z set depends_on=['T-1302']
- 2026-10-22T16:00:33Z blocked: waits for T-1302's lane to merge (both edit fmcodetui.py) and for the full gate run to free the checkout; unblock after
- 2026-10-22T16:10:05Z set status=planned
- 2026-10-22T16:28:54Z focused
- 2026-10-22T16:29:00Z paused: focus moved to T-1405
- 2026-10-22T16:37:07Z blocked: waits for T-1316's lane (both edit fmcodetui.py)
- 2026-10-22T16:44:53Z set status=planned
- 2026-10-22T16:48:36Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-22T16:48:36Z focused
- 2026-10-22T16:48:46Z steer: grounded: Canvas.put already clips by columns, so nothing leaves the screen; the visible bug is padding by len(): a focused or selected log line holding wide glyphs is padded past its width and cut with a stray ellipsis. Fix _focus_line, the selected row, _welcome and the status hints with width()/pad()
- 2026-10-22T16:52:29Z scope: CHANGELOG.md also carries T-1472's uncommitted line; it lands in this commit
- 2026-10-22T16:52:50Z done
- 2026-10-22T16:52:53Z committed 6abed44d (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1431 [FIX S, done, 2 steps] fm code app: labels and box titles measured in columns
- research T-1026-review: MEDIUM** `mods/foreman-ui/hooks/register.tsx:1736-1742` — the Agents bars do not stay in one column when a stop button shows. [stale: mods/forema…
- T-1301 [FIX M, done, 2 steps] fm code tui measures text by display width: fit, tail and wrap cut wide (CJK, emoji) text to its columns, with the ellipsis, and padded col…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- similar finished tasks took 2–2 steps
## Why not caught
T-1431 swept cutting, not padding; no test selected a wide row
## Lessons
- Padding by len() is the same bug as cutting by len(): every ljust/len near terminal text should go through width().
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
