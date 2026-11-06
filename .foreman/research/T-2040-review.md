[instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I couldn't run the tests here, so the acceptance criteria below rest on reading the code. I didn't open `demo/live.cast`, `live.mp4` or `live.svg`.

## lens: intent
- MEDIUM — site/style.css:~250-270 — The request says "the whole website", but the new entrance, scroll-reveal and stamp animations all target landing-page selectors (`.hero`, `.rules`, `.term`, `.lanes`, `.diagram`, `.facts`, `.steps`). `.fcard` and `.head` may also appear on the feature pages. The 15 `site/pages.py` feature pages get only the `.fcard` hover lift and the footer brand rule. The acceptance criteria also test only `index.html`, so the gap is invisible to them. — Say in the changelog that this pass covers the landing page only and capture a follow-up task for the feature pages, or add the reveal to the feature-page selectors. — confidence medium
- LOW — plugin/tests/test_site_build.py:871-880 — Criterion 2 is about the video's first frame. The test checks the cast and the SVG but never `live.mp4`, the file the site serves. A stale mp4 would still pass. — Assert the mp4 was rendered from the cleaned cast. Option: compare against `ffprobe` duration, or an `ffmpeg` first-frame check when `ffmpeg` is on PATH. Otherwise record in the changelog that the mp4 was checked by hand. — confidence medium

## lens: maintainer
- LOW — demo/record_live.py:99-105 — `--from-cast` re-thins and re-renders an old cast without calling `kept()`. A cast that still holds the trust screen would put it back in the reel. — Filter events here too, and make `kept` work on both frames and events. — confidence high
- LOW — site/stats.py:230 — The `git grep -c "def test_"` loop copies `releases()` at lines 122-123. It counts at `HEAD`, so uncommitted tests are missed. It counts every `def test_`, while `model_tests` counts only `^    def test_`. The page then calls the result "tests in the gate that every release has to pass". — Extract one `test_count(rev)` helper. Rename or reword the claim if the count is not the gate's. — confidence medium
- LOW — site/style.css:~338 — A second `.fcard { transition… }` rule sits apart from the first `.fcard` rule. `.hero` and `.reel` are also split across several rules. — Merge them. — confidence high
- LOW — plugin/tests/test_site_build.py:837 — `Landing` extends `unittest.TestCase`, but `TitleCard` in the same file uses `ForemanTestCase`. — Match the neighbour. — confidence low

## lens: design
- Accessibility reviewer, LOW — site/style.css:~108 (`.hero h1 em`) — In dark mode the 60% `--signal` band sits under light headline text. I estimate about 3.1:1 for the lower 36% of the glyphs. That passes the 3:1 large-text bar only barely. — Drop the mix to about 35%, or set the em text to `--paper` in dark mode. — confidence low (estimate, not measured)
- Accessibility reviewer — `prefers-reduced-motion` is handled well. Every animation sits inside `no-preference`, and `.fcard` is explicitly cleared under `reduce`. The reveals are guarded by `@supports (animation-timeline: view())`, and the focus ring is unchanged.
- Art director — The hero has a point of view: grid-and-glow backdrop, the signal highlight, stamps that slam in. I found no generic tells.
- First-time user — Hover feedback is added on the cards. Keyboard focus has no matching lift, though the focus ring still shows.

## Acceptance criteria
- Site builds, no inline styles, no stale counts: met by code reading, not run. `site/index.html` has no `style=`, no `style=` appears in `site/*.py`, and `build.py` fails the build on an unfilled `{{…}}`. I did not run `test_docs` or `test_design_lint`.
- Demo reel opens on the session, and the recorder drops trust screens: partly met. `kept()` is applied in `write()` and tested, and the cast and SVG are asserted clean. The mp4 is not asserted, and the `--from-cast` path isn't covered.

## Implicit decisions
- The test count is `def test_` occurrences at `HEAD`.
- "5,000 replayed commands" is the cap `fmreplay.MAX`, not a measured count.
- "Tasks" comes from the ledger of the biggest local `foreman-*` project.
- Scroll-driven CSS animation is used with no JS fallback; unsupported browsers see everything in place.
- Hero is two columns from 1080px, and the compact 2x2 poster is shown there.

## Not checked
- Rendered output at widths, full-page screenshots, and print. Elements with view-timeline reveals stay at opacity 0 until scrolled, which may show as blank in full-page captures.
- The `demo/live.cast`, `live.mp4` and `live.svg` media.
- `fm design lint` output.
- Whether `MASTER.md` needs a site line.

**Noticed:**
- site/data/stats.json was regenerated wholesale. The `features/benchmarks` bench cases changed (the `csvlite`/`tokenbucket` cases became `honour` cases, and `tests: null` fields were added). Worth a look that `features/benchmarks.html` still reads right. The committed file had been stale against `stats.py`.
- `site/index.html` `.install` clips the curl command at every width (`site/style.css:122-123`, `.install code`), so "| bash" is hidden behind a horizontal scroll. It is not new, but it is the page's main control.
