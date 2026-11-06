## Verdict
Changes needed. One acceptance criterion is not met (cb, riso and custom palettes "render exactly as before"). I read the code and did not run the test suites.

## lens: intent
- MEDIUM — `mods/foreman-ui/hooks/register.tsx:1156,1208` — The band progress meter went from `C.ok` to `C.accent` for every palette (diff lines 82-92). Under cb, riso and a custom palette the band bar now draws in a different colour. `palette-baseline.test.tsx` compares only `C` key values, so it cannot see which key a surface uses. — Use `C.hot` and add a render test of the band under cb, riso and custom. (Or keep `C.ok` when the palette lacks hot.) — high
- MEDIUM — `plugin/lib/sampo/smithtui.py:1837-1843` — `theme=night|paper` with `palette=cb|riso` now lays the ink over the forge base (bg `#060819`), not the old base. `tui-baseline.json` pins the palette dicts, not (preset, palette) renders, yet the CHANGELOG says cb and riso look exactly as before. — Pin those renders, or build the ink on `classic` / `classic_paper`. — medium

## lens: adversary
- No findings. Config values still pass through `_style_error`, `_faint` and the `customColors` hex whitelist.

## lens: edge
- MEDIUM — `plugin/lib/sampo/smithtui.py:96-97` (also `_track` ~900, `_tokens` ~1003) — `hot`, `steel` and `chip_steel` are copies of accent and ok taken when the theme is built. A saved `[colors] accent` or `ok` override on classic, signal, riso or cb no longer recolours running or done nodes, links or chips. A classic `ok` override also makes `_track` take the `steel != ok` branch, and an accent override changes the `_tokens` gradient top. — In `_apply`, mirror an `accent` or `ok` override into `hot` / `steel` / `chip_steel` when the user didn't set them. Add a test. — medium
- LOW — `plugin/lib/sampo/smithtui.py:107-109` — `classic_paper` is not a preset, so a saved `paper` user cannot get the old light look back. — Add a preset or say so in the CHANGELOG. — medium
- LOW — `plugin/tests/test_code_tui.py` (class Forge) — The 256-colour and 8-colour hot-vs-steel checks cover night only. At 8 colours on paper, hot and accent both map to red. — Add paper cases. — medium

## lens: operator
- MEDIUM — `plugin/hooks/statusline:152-153` — On a light terminal `DIM 0x9097bc` is about 2.9:1 contrast on white. `TRACK 0x2a2c33` is now the foreground of the unfilled `─`, which nearly vanishes on dark terminals. The statusline has no light-terminal handling, and only WARN is pinned by a test. — Lift DIM and TRACK, or switch on `COLORFGBG`. Pin the constants. — medium
- LOW — `plugin/hooks/statusline:169-171` — `heat()` was green to amber to red and now ends in pink, with a lime WARN. That is a visible change for anyone who reads the colour as a severity. — State it in the CHANGELOG or keep red as the top step. — medium

## lens: maintainer
- LOW — `plugin/tests/test_code_tui.py` (class Forge) — The "no Foreman" mod scan is a line regex. It can be fooled by `//` inside strings and by multi-line template literals. The banner test only greps the source. — Scan rendered output instead. — low

## Acceptance criteria
- Pane glow and cool, plus the ⊖/⊘ glyph: met (`kit.ts` `paneMark`).
- cb, riso and custom render as before: **not met** (band meter, and night with cb/riso in the TUI).
- Banner, and every preset, palette and motion value still loading: met. night, paper, signal, riso, mono and the new classic all load.
- 256-colour fallback distinguishes running from done: met on night, not pinned on paper. NO_COLOR is fine.
- One token source pinned by tests: met.
- No user-visible "Foreman": met, with the scan weakness above.
- Renders equal to the baseline fixtures: not verifiable. The fixtures pin dicts and `C`, not surfaces.

## Implicit decisions
- The ink overlays sit on the forge night/paper base.
- `hot` and `steel` fall back to accent and ok at theme-build time.
- The band bar uses the accent colour, and the closed sweep stays `C.ok` while its row is `C.steel`.
- `signal` is classic plus the CB night ink, and `riso` is classic_paper plus the RISO paper ink.
- The statusline uses fixed truecolor constants.

## Not checked
The design lens, token.json equality, the golden fixtures, and a run of either test suite.

Noticed: the statusline has no light-terminal path at all, which is worth its own task.
