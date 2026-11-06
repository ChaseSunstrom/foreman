**Verdict:** approve with nits. I found no defect I can trigger, only one LOW test gap.

## lens: intent / adversary / edge / operator / maintainer / design

- LOW — plugin/tests/test_site_build.py:214-221 and site/site.js:25,69-88 — Nothing tests that the new JS motion stays behind the reduced-motion early return. The count-up and pointer-glow code sits after `return` at site.js:25, and the only motion test (line 214) reads CSS only. If a later edit moves either block above that return, reduced-motion readers get the count-up and the glow, and the suite stays green. Fix: add a test that finds `performance.now` and `pointermove` in site.js only after the `if (still` return, or move the new code into a function called after the guard. Confidence: high that the gap exists. I have not seen anyone move the code.

## Acceptance criteria

- **Stylesheet, script and icon URLs carry the content hash on every built page: met.**
  - `layout()` (site/build.py:300, 301, 306, 323, 332) hashes the icon link, both header and footer logo images, the stylesheet and the script.
  - The landing page is rewritten at build.py:505-514. It raises if any of the four tags is missing, and `replace()` has no count, so both `<img>` tags are hashed.
  - The only pages built outside `layout()` are the landing page and the `gallery/` pages, which are copied as-is and link no stylesheet or script.
  - The test checks all four tags on the landing page, the features index, the benchmarks page and a story page.
  - I did not run it.
- **Every animation stays inside `prefers-reduced-motion: no-preference`: met.**
  - `@keyframes drift` and `.hero::before { animation }` are at style.css:269-270, inside the media block at line 257.
  - `.fcard:hover` with the glow is at line 272, also inside it.
  - The count-up and pointer glow in JS run only after the early return at site.js:21-26, which fires on reduced motion or without IntersectionObserver.
  - The existing test at test_site_build.py:214 covers the CSS side.

## Checked and dismissed

- **Count-up flash:** `.proof` is invisible during the first 0.28 s (`rise` with fill `both`, style.css:263,267). The first frame that sets "0" is therefore never seen as a flash from the full number to zero.
- **Stalled frames:** the 1700 ms timeout (site.js:79) sets the final text in a hidden tab. A late `tick` then sees `k=1` and writes the same text.
- **Layout shift while counting:** `.proof dd` uses `tabular-nums` (style.css:85).
- **`nowrap` on `.sketch code`:** the longest shader name is `shader-grain-gradient`, 21 characters at 0.8em, so it fits the 250 px minimum card width.
- **`.fcard:hover` specificity:** it beats `.fcard`'s `background` shorthand at line 359, and no dark-mode rule overrides it.
- **Pre-audit items:** the CHANGELOG entry was added at the top of Unreleased. MASTER.md describes `site.js` and `style.css` generically and needs no edit.

## Implicit decisions

- 8-hex-character SHA-256 prefix as `?v=`.
- A query string rather than hashed file names.
- The build hashes `site/*` source files at import time.
- The count-up lasts 1.2 s after a 300 ms delay, with a cubic ease-out.
- The 1700 ms fallback timer is fixed.
- The hero drift cycle is 16 s, infinite, alternating.
- The glow uses the accent colour at 14% opacity with a 240 px radius.
- The glow shows on hover only, not on keyboard focus.

## Not checked

- I ran nothing: no tests, no build, no screenshots.
- **Hero drift cost:** `--drift` is a registered property, so the gradient repaints on the main thread every frame, forever, behind a `mask-image`. This is an unmeasured lead, not a finding. Before and after CPU or paint numbers are needed.
- **Old browsers:** where `@property` is unsupported, such as Firefox before 128, the drift would step discretely instead of gliding.

Noticed: the MASTER.md `site/` row doesn't say CSS, JS and icon URLs carry content hashes; worth a docs line.
