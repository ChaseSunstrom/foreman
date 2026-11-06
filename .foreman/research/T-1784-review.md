## lens: intent, adversary, edge, operator, maintainer

**Verdict: changes needed.** The default `fm scene sketchbook` crashes, and the fallback does not hide the canvas. Both are one-line fixes. I read the code and ran nothing.

**Findings**

- HIGH — `plugin/lib/fmscene.py:1681-1682` — The default path crashes. `out = args.out or "sketchbook.html"` is a bare name, so `fmcore.write_atomic` gets `os.path.dirname("") == ""`. Then `os.makedirs("", exist_ok=True)` (`fmcore.py:927`) raises `FileNotFoundError`. The same happens for `--out sketchbook.html`. `_write_out` (`fmscene.py:1596`) already carries a comment about this exact case and uses `os.path.abspath`. The only test passes an absolute `self.tmp` path, so it never sees this. The write is also outside any `OSError` handler. Fix: `out = os.path.abspath(args.out or "sketchbook.html")`, catch `OSError` as `_write_out` callers do, and add a test that runs from a temp cwd with no `--out`. Confidence: high.

- MEDIUM — `plugin/lib/fmscene.py:1262` (CSS) and `:1273` (JS) — With no WebGL2, or a shader that won't compile, `fail()` sets `canvas.hidden = true`, but `.sketch canvas{display:block}` overrides the browser's `[hidden]{display:none}`. A blank 320x200 canvas stays next to the text fallback. That breaks the "text fallback" half of the request. Fix: add `.sketch [hidden]{display:none}` to `SKETCH_CSS`. Confidence: high (author CSS beats UA `[hidden]`). The test only greps the page for strings, so it never sees this.

- MEDIUM — `plugin/lib/fmscene.py:299` — Reduced motion draws `draw(2.0)`, but the cards define their own stills. Each card's "Reduced motion" section says `uTime = 0.0`. The dither-fade card says `uProgress = 1.0`, the end state, while the sweep gives about 0.61 at t=2. The ink-diffusion card says `uSpread = 1.0` but its preset is 0.6. The still the page shows is not the still the card promises. Fix: draw the still at t=0, with sweep uniforms at 1, or document that the thumbnail still is its own. Confidence: medium.

- LOW — `plugin/lib/fmscene.py:1676` — The sketchbook branch now runs before the `_READS` check (the merge resolution). So `fm scene sketchbook --balls 5` or `fm scene sketchbook FILE` silently ignores the flag or file, where every other action refuses with exit 2. Fix: run the `_READS` loop first, and reject `args.path` as the neighbouring branch does. Confidence: high.

- LOW — `plugin/tests/test_scene_verify.py:531-543` — The "still under reduced motion" and "fallback" criteria are checked only by `assertIn("prefers-reduced-motion")` on the page text. Nothing runs the JS. That is why the two defects above got through. Fix: extend the CSS check and the bare-name test. A real WebGL run would need a browser, so it can't be done here.

**Acceptance criteria**
- Each Sketch line sets each declared uniform except `uRes` and `uTime`, with the right component count: met. `test_every_card_presets_each_declared_uniform` checks all 8 cards. Uniforms of other types (`int`, `sampler`, `mat`) are never counted, so a card declaring one would pass silently.
- Sketchbook page has a canvas, source and fallback per card: met, by count in the test.
- Page draws still under reduced motion: partly met. The code draws once, but at t=2.0 rather than the card's own still.
- Text fallback without WebGL2: not met visually (the blank canvas stays); the text is present.

**Merge resolution**
- `fmcli.py` action choices contain both the new `sketchbook` and the older `lookbook` and `gallery`: fine.
- `site/pages.py`: the `shaders` page entry is well formed and `test_docs` is relaxed to match. I found no conflict damage.
- `cmd_scene`: only the ordering problem above.
- The `pane_replay`, `golden.ts`, `replay.test.tsx` and `test_ui_replay.py` hunks are T-1670 content from the merge, not this task.

**Implicit decisions**
- Dark and light colours are baked into the page CSS.
- The thumbnail is fixed at 320x200 with no device-pixel-ratio scaling.
- Presets are space-separated `uName=v1,v2` on the last backtick span of the line, with `sweep` for a float.
- The default output file is `./sketchbook.html`.
- A card containing `</script` is skipped silently.

**Not checked:** CHANGELOG and MASTER wording, running the page in a real browser, and the `site/` build output.

**Noticed:** `plugin/lib/fmcore.py:925` — `write_atomic` fails on a bare filename (`dirname == ""`); fixing it there would cover every caller.
