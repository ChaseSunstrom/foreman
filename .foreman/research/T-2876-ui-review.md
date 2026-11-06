**Verdict: approve with nits.** The forge palette, the gold titles and borders, and the steel done state read as intended. The main gaps are that the statusline never got the forge, the paper shots can't be trusted, and the heat language is applied unevenly.

I couldn't run `git diff` (no Bash here). I read the changed files and the shots directly, and I computed contrast from the hex values.

## lens: design

**Art director**
- MEDIUM — `plugin/hooks/statusline:150,261,287,290` — The statusline is not re-skinned. It still uses the teal `0x5fd7d7` accent and the `▌` mark, and it has no `⊖`. `pane-glyph.txt` says the glyph is for "the pane and the statusline". Teal chip next to the gold pane head breaks the forge. — Set ACCENT to `0xffc24d`, ACCENT2 to `0x6e9bff` and OK to the forge ok, and use `⊖` for the chip. — high
- MEDIUM — the "Tokens per call" panel in `tui-after-night.png`, and the brand chip — The gold→blue gradient (`accent`→`accent2`) passes through desaturated tan and grey. The bars look muddy and band-like, worse than the clean violet gradient before. — Mix through a warm midpoint (the ember) or use two flat tones. — high
- LOW — Same shot, Time and Changed bars — `ok`→`ok2` (`#6FD8A0`→`#A8D5A2`) is almost flat and pastel. The bars lost the vividness they had before. — Widen the `ok2` gap or leave as is. — medium
- LOW — `smithtui.py:1249` / `tui-after-night.png` header — `⊖` renders touching the chip edge and "SAMPO" with no visible gap, unlike the pane's `⊖ Sampo`. — Check the glyph's advance width in the snapshot font, or pad with an extra space. — medium

**Heat language**
- MEDIUM — Cross-surface inconsistency. Pane done rows cool to steel (`rows.tsx:316,404,510,539`; `register.tsx:1691`). The pane's finished-agent row and `rows.tsx:638` stay green (`C.ok`), and the TUI Activity `✓ read/write/edit` rows stay green (`tui-after-night.png`). "Finished cools to steel" only holds for the step rail and the chips. — Pick one rule for per-action ✓ (steel, with green kept for checks) and apply it in both surfaces. — medium
- LOW — Gold is also used for static things (every panel title, the 1/2/3 step chips, the brand, the token bars). In a closed frame everything is gold, so gold no longer means "running". — Keep titles and step chips on `ink` or `edge`, and keep gold for live state. — medium
- LOW — `steel` `#C8D8EC` is nearly `ink` `#EEF0FA`. Done work reads as plain white text. — A slightly bluer or dimmer steel would set it apart. — low

**Accessibility**
- MEDIUM — `tui-before-paper.png` and `tui-after-paper.png` are pixel-identical to the night shots, so the paper preset was never rendered. Paper contrast can't be judged from the shots. Computed from the hex values, it passes:
  - `ink` on `bg` is very high; `dim`/`steel` `#555B80` on `bg` is 5.8:1.
  - `accent` bronze is 5.5:1; `hot` `#E0461A` is 3.6:1, used only for glyphs.
  - `edge` is 3.4:1; `chip_ok` is 4.7:1.
  — Fix the snapshot harness so the paper background paints, then re-shoot. — high
- LOW — `track` is about 1.4:1 on both themes (night `#2A2C33`; paper `#C9CEDD`). The todo `○` and `─` fail 3:1. This was true before the change too, so it isn't a regression. — Lift `track` to at least 3:1. — medium
- LOW — `kit.ts:14` `C.dim` `#6C7686` is about 4.3:1 on `#060819`. The pane's todo labels (`rows.tsx:161`) fall just under 4.5:1. — Use `muted`. — medium

**cb and riso**
- Both look the same as before apart from the base theme. The cb shot has the deeper `#060819` background, because the ink overlay now sits on forge night, which the brief allows. The riso preset is still built on `classic_paper`.
- LOW — The brand text and mark change for every palette (`smithtui.py:1249`), so they are not exactly as before. — Accept, or keep the old brand under cb and riso. — high
- LOW — `kit.ts:38` overwrites any saved `hot` or `steel` with `accent`/`ok`. — Honour saved keys. — low

**Verdict:** The forge reads, but fix the statusline, the green-versus-steel rule for done rows, the muddy gradients and the paper shots before calling it done.

## Acceptance criteria
- Forge palette and mark: met in the TUI and the pane.
- Statusline: not met.
- cb, riso and saved palettes unchanged: met, except the brand text.
- `classic` preset: met (`smithtui.py:109`).
- Contrast: met from the hex values; not verifiable from the shots.

## Implicit decisions
- Brand renamed to "SAMPO CODE".
- Bar and track stay neutral grey `#2A2C33` against the navy.
- `classic` is night only, with no light variant.
- `hot` is used only for step glyphs and links, not for text.

## Not checked
No running-state shot was provided, so the glowing `hot` state, its animation and the `⊘` frames were not seen. The pane's colour, which the shots don't carry, was not checked. The statusline diff itself was not seen.

**Noticed:** `ok2` `#4E9F1D` on paper is about 2.9:1, under 3:1 for graphics (`smithtui.py:47`, and the same value in `classic_paper`).

**Verdict:** changes needed. Three of the four first-pass MEDIUMs are fully fixed; the statusline re-skin is only partly done.

I read the shots and the code. I computed contrast by hand and did not render any new shot.

## Verification of the four
1. **Statusline: mostly fixed.** `plugin/hooks/statusline:152-154` now uses the forge colours and the `⊖ ` mark. The heat language did not carry over: the step bar at `:267` still runs blue to green (`mix(ACCENT2, OK, t)`) instead of steel for done and ember for current. I rate that LOW because it never shares a screen with the pane band.
2. **Tokens chart: fixed.** `smithtui.py:1003` heats gold to ember. The night shot reads cleanly. cb and riso keep their old purple-to-pink and blue-to-gold gradients, matching the before shots.
3. **Steel on finished marks: fixed for the rows named.**
   - TUI Activity ✓ (`smithtui.py:1073`) is steel.
   - Pane finished marks (`rows.tsx:442`, `:638`) are steel.
   - The DONE chip (`:1102`) is steel.
   - Other finished work still shows green; see the first finding below.
4. **Paper shots: fixed.** `tui-after-paper.png` renders the paper theme. PASS chip contrast is about 4.7:1, steel `#555B80` on the paper background is about 5.7:1, and the gold accent `#7A5A26` is about 5.5:1.

cb and riso differ from before only in the base theme and the brand mark. `preset_theme` (`:1841`) strips `hot` and `steel` under an ink, and `kit.ts:38` falls back to `ok` and `accent`.

## lens: design
- MEDIUM — `smithtui.py:1043` — finished Time bars are still green (`ok` to `ok2`) beside the steel track and steel ✓ rows. Same class of miss as first-pass finding 3, and it is visible in the night shot. — colour done bars `steel` when the palette defines it; keep the old gradient otherwise. — high
- MEDIUM — `smithtui.py:1743-1745` — the projects-deck mini track (`_card_track`) uses green for done stations; the main track uses steel. — use `steel` for done and `hot` for the current station, falling back for palettes without them. — medium; this screen has no shot
- MEDIUM — `smithtui.py:41` (night `track`) and `:46` (paper `track`) — the unfinished track colour is about 1.3:1 on night (`#2A2C33` on `#060819`) and 1.37:1 on paper, against the 3:1 graphics target. It was about 1.7:1 on the old night. Todo `○` nodes and `─` links (`NODE`/`LINK`, `:132-133`), and the todo step segments in `kit.ts:145`, are near-invisible while a run is in progress. The shots show only finished runs, so I could not confirm this visually. — draw todo marks with `edge` (`#5C6390`, about 3.2:1 on night) and keep `track` as a fill only. — medium
- LOW — `plugin/hooks/statusline:153` — the empty bar track (`0x2A2C33`) has the same 1.3:1 problem on a dark terminal. The statusline hardcodes a dark palette, so gold and `DIM` fall below 3:1 on a light terminal.
- LOW — `smithtui.py:44`, `:48` — on paper, `steel` equals `dim` (`#555B80`), so finished marks look the same as labels.
- LOW — paper `key` hints (`warn` `#5F6A0A` on bar `#D6DBEA`) are about 4.3:1, just under 4.5:1. The old paper was about 4.0:1, so this is not a regression.
- LOW — the night bar and track `#2A2C33` is a neutral grey inside a navy theme.
- LOW — the live Time bar (`:1048`) and the tokens chart use gold, not `hot`.
- LOW — the pane shots show only an idle pane, so steel, ember and the `⊘` strike are not visually confirmed.

## Acceptance criteria
- Four first-pass fixes: 1 partly met, 2 met, 3 partly met (Time bars and the deck track still green), 4 met.
- Contrast at or above 4.5:1 for text: met, apart from the LOW paper hint above.
- Contrast at or above 3:1 for graphics: not met for the track.
- cb, riso and classic unchanged: met, by the shots and the code.

**Verdict line:** yes, three MEDIUMs remain: green finished Time bars, the green deck mini track, and the 1.3:1 unfinished track.

**Noticed:** none

Items 1 and 2 are fixed and item 3 is fixed with one gap. Nothing above LOW remains, and I found one LOW. I checked the code, the five shots and the contrast figures. I ran no tests.

**1. Finished Time bars: fixed.**
- `smithtui.py:1043-1044` makes a done phase `steel` whenever `steel != ok`, and otherwise falls back to the old ok→ok2 gradient.
- The night shot (`tui-after-night.png`) shows flat pale-steel bars for plan through checks. The paper shot (`tui-after-paper.png`) shows slate #555B80 bars.
- cb (`tui-after-night-cb.png`) keeps its blue gradient. riso and classic keep their green and teal gradients, so they are unchanged.

**2. Projects-deck mini track: fixed.**
- `smithtui.py:1744` and `smithtui.py:1746` use steel for done stations and links, hot for the current station, and todo for the rest.
- The empty-track case at `smithtui.py:1740` also uses todo.
- None of the shots shows the deck, so this is confirmed from the code only.

**3. Unfinished track marks: fixed.**
- The `todo` style is defined at `smithtui.py:97`, with night #5C6390 at line 43 and paper #7C819F at line 48.
- NODE and LINK use it at `smithtui.py:133-134`.
- The pane uses it at `kit.ts:22` and `kit.ts:146`.
- By my hand calculation the contrast is about 3.4:1 on night (#060819) and about 3.3:1 on paper (#EEF0F6). `test_code_tui.py:338-340` pins 3:1 on both grounds.
- The stepper's unfinished circles and links are clearly visible in the night and paper shots.
- Palettes without a `todo` key (classic, signal, riso, the inks) fall back to `track`, so they are unchanged. In the cb night shot, which has no todo marks, nothing shifted from the pre-change look.

The rest holds up:
- **Ink overlay:** `preset_theme` (`smithtui.py:1841-1843`) builds cb and riso on the classic ground, pinned at `test_code_tui.py:350-354`.
- **Saved accent and ok:** `_apply` (`smithtui.py:4455-4463`) mirrors them into hot and steel only where those two stood in for accent and ok. It also sets the `chip_steel` background.
- **Colour roles:** the DONE chip and status text use steel and the PASS chips stay green, matching the heat rule.

## lens: design
- LOW — `mods/foreman-ui/hooks/kit.ts:39` — The pane falls back to the old look whenever a saved palette has any key at all, even an unrelated one like `dim`. The saved palette then loses the forge's heat colours and `C.todo` falls back to the faint `C.track` (the 1.3:1 problem again). The Python `_apply` is narrower and only mirrors when the user actually saved `accent` or `ok`, so the two surfaces disagree. — Fix: use `hot: mine.hot ?? mine.accent ?? C.hot`, `steel: mine.steel ?? mine.ok ?? C.steel`, `todo: mine.todo ?? C.todo`, applied only to the saved-palette case. Keep the current fallback for cb and riso. — confidence medium

**Not checked:** the projects-deck card (no shot), the statusline DIM and TRACK values (0x8088a8 and 0x6c7398), the pane band meter, and the pane's own rendering.

**Verdict:** nothing above LOW remains.

**Noticed:** none
