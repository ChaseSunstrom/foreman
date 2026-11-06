**Verdict:** approve with nits. One finding should be fixed before merge (the silent missing-marker case).

## lens: intent
- MEDIUM — site/build.py:458 — A missing `POSTER_MARK` fails silently. `str.replace` does nothing when the marker is absent, so if someone edits the comment in `index.html`, the build succeeds and ships a hero with no poster. Only `test_site_hero` would notice. Fix: `if POSTER_MARK not in page: raise SystemExit("site/index.html lost the poster mark")` before the replace. Add a test that builds with the marker removed and expects a non-zero exit. Confidence: high (proven by the code path).
- LOW — site/index.html:46 — The poster sits after the install box and the "Or from inside Claude Code" line, above the video. The brief calls it "the hero's first paint", but it is below the h1, lede and install box. That is probably right for T-1610's scene to sit over later. Say so in the task log, or move it above the install box if "first paint" is meant literally. Confidence: medium.

## lens: adversary
No finding. A crafted `stats.json` cannot inject markup:
- `head`, `said` and each label go through `esc` (build.py:271-278). `html.escape` quotes by default, so `aria-label` is safe.
- `fmt(v)` is the only unescaped sink, and it is safe for every type `json.load` returns. A string value raises ValueError on the `:g` format. A list or dict raises TypeError in `max`. Numbers, `NaN` and `Infinity` format as plain digits or `nan`/`inf`, and `r` stays numeric.
- LOW hardening: use `esc(fmt(v))` at build.py:281 so safety does not rest on `fmt`'s type behaviour. Confidence: high.

## lens: edge
- LOW — site/style.css:87 — At phone widths the text is too small. The frame scales with width, so at a 320px viewport (svg about 290px, scale about 0.3) the 32px labels render at about 10px and the 28px kicker at about 8.5px. The bump at 560px does not compensate. On Linux without Barlow, the mobile kicker with the date (about 56 characters at 28px plus letter-spacing) can pass 960 and clip. Fix: below 560px use a 2×2 layout and shorten the kicker, or drop the kicker there. Confidence: medium (estimated from glyph widths, not rendered).
- Overlap for large numbers is not an issue today. Stations are 240 units apart. At 46px a comma-formatted 7-digit number is about 145 to 180 wide. Numbers overlap only at 8 or more digits, with the fallback font at 56px. The current totals are 4 digits or fewer.

## lens: operator and maintainer
- The pre-audit "usually changes with" items need no edit. `test_docs` only reads the built pages generically.
- `--muted`, `--grid` and `--axis` are defined. They are in `:root` and both dark blocks at style.css:279-286. The builder's note is wrong, and the poster does not use them.
- MASTER.md and CHANGELOG entries match the change.

## lens: design
- MEDIUM — build.py:274-278 and style.css:81 — The red-to-amber-to-green gradient is a generic traffic-light device and means nothing here. Tasks, evidence, proofs and commits are counts, not states, yet "tasks done" is red and "commits" is green. It is also a red/green pair for colour-blind readers. Fix: use one hue, `--ok` or `--signal`, for the track and stations. Or give the colour a real meaning, such as a muted track that fills toward `--ok` for verified.
- LOW — build.py:281 — Plain circles on a line read as a stock infographic. The site already has a motif: the 45° signal-coloured diamond (`.points li::before`, style.css:165) and the condensed uppercase `.stamp`. Make the stations diamonds or rotated squares sized by area, and set the labels as small-caps `.stamp` text. That ties the hero to the rest of the page and to the "chain" idea.

## Acceptance criteria
- Inline SVG with `role=img`, an aria-label naming the totals, and no external host: met. `test_site_hero` asserts each of these. I did not run it.
- A changed `stats.json` changes the poster: met. The second test builds with changed totals and compares the output.

## Implicit decisions
- Station area is a square-root scale with a 10-unit floor.
- A date from `stats.json["generated"]` is appended to the label.
- The poster's `max-width` is 900px, narrower than the 1120px wrap.
- A fixed 960×290 frame.
- A first-match replace of the marker comment.

## Not checked
Rendered appearance, since there was no screenshot, and I did not run the tests. Real glyph widths. Colour-vision and contrast measurements.

**Noticed:** style.css:233 has a dead fallback `var(--muted, #898781)`. The variable is defined, so the fallback can go.
