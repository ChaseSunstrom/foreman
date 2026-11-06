**Verdict:** changes needed. I could not run anything here (read and search tools only), so the test results below come from reading the code. No pow or normalize appears in any shader, so there is no NaN risk from those.

## lens: adversary / edge (GLSL, icon checker, browser test)
- MEDIUM — shader-halftone.md:32-33 — `uIntensity=0` is not plain. Tone is 0, so r=0 and `smoothstep(-aa, aa, d)` returns 0.5 at d=0. Each cell centre gets a roughly pixel-sized speck of up to 50% ink, which is a faint dot grid. The card says "0 = plain `uPaper`" in three places. — Fix: `dotInk *= step(1e-4, uIntensity);` (or early-return `uPaper`). — CONFIRMED (arithmetic)
- MEDIUM — svg-icon-system.md:62-68 — The checker crashes on common unit values. The `box` dict evaluates `f("width")` for every element, so root `width="1em"` (the card says "Sized in em") or `width="100%"` raises `ValueError`. `rstrip("px")` only strips characters. Repro: `check('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="1em" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"/>')`. — Fix: parse in a try/except and report a problem, and build `box` only for the matching tag. — CONFIRMED
- MEDIUM — svg-icon-system.md:37,42-72 — `pytest -q test_icons.py` collects nothing, because the file defines only `check` and no `test_*` function. It exits 5 ("no tests ran"). — Fix: add a `test_icons()` that loops over the icon files and asserts `check(svg) == []`. — CONFIRMED
- LOW — svg-icon-system.md:51 — `ET.fromstring` on project SVGs. Entity expansion is only safe with expat 2.4.1 or newer, so a billion-laughs SVG could exhaust memory on an older Python. — Fix: return an error if `<!DOCTYPE` or `<!ENTITY` appears before parsing. — PLAUSIBLE
- LOW — svg-icon-system.md:66-69 — The "2-22 live area" check covers only rect, circle and line. The `path` element is the common case and goes unchecked. — Fix: say so in the card, or parse path bounds.
- MEDIUM — shader-grain-gradient.md:34, shader-paper-fibre.md:40 — The sin-hash is fed raw pixel coordinates (up to about 3840x2160, so `dot` is about 2.2e5). On GPUs with weak `sin` range reduction this gives streaks or patterns. In grain-gradient the grain is the look. — Fix: use an integer hash (`uvec2`, valid in ES 3.00) or a sin-free hash. — PLAUSIBLE
- LOW — shader-contour-lines.md:33 — `fwidth` is an L1 norm, so diagonal lines render up to 1.41x wider, against the "1-2 px on steep and flat alike" claim. Also `/fwidth(h)` is 0/0 at `uCount=0`. — Fix: `max(length(vec2(dFdx(h), dFdy(h))), 1e-4)`.
- LOW — shader-ink-diffusion.md:50 — "wrap only nudges the warp" is false. 600 s x 0.02 is 12 noise cells, so the stain outline jumps. — Fix: say it jumps (as the contour card does), or drift on a circle.
- LOW — shader-ink-diffusion.md:52,71 — Radius is 0.5*`uSpread` frame heights (plus or minus 0.3 of warp). A 16:9 half-diagonal is 1.02, so 1.3 does not fill the frame. The probe "pixel at `uOrigin` (ink colour)" is wrong, since the centre is pale at about 22% ink. — Fix: correct both lines.
- LOW — test_library.py:742-747 — `subprocess.run` timeout kills only the parent browser, so GPU and renderer children can outlive it. Any crash or timeout becomes a skip, which hides a broken environment. — Fix: `start_new_session=True` and `os.killpg` on timeout.
- LOW — light-and-material.md:19-22 — The Rim rig lists lights at 1.0-1.5 "relative to the key", but it has no key. The Overcast key at 0.3-0.5 has no stated reference against the hemisphere light. The albedo, metalness and roughness numbers are otherwise sensible: key:fill 2:1-4:1 is correct, and the clamped gold is flagged as such.

Checked and fine:
- The halftone (200π) and grain (400π) wraps are exact multiples of all their periods.
- The Bayer matrix is correct.
- Dither-fade `uProgress` 0 and 1 give one flat colour.
- `uIntensity=0` is plain in all other shaders (aurora, contour, dither, grain, ink, paper, caustics), with ±1/255 dither where used.
- The reduced-motion stills are honest.
- `BG_VS` supplies a y-up `vUv`.

## lens: maintainer (tests)
- MEDIUM — test_library.py:688-716 — No test asserts that `uIntensity=0` gives a flat result. It only checks that the name is declared, which is how the halftone bug got through. — Fix: in the headless page, draw each shader at `uIntensity=0`, `readPixels`, and assert every pixel is within 1/255 of the paper or floor colour. — CONFIRMED

## Acceptance criteria
- Ten cards exist with their fields, and every block is an ES 3.00 skeleton: met by reading. `out vec4`, `void main` and `precision` are present, and the section lists match. I did not run `test_library.ShaderLooks`.

## Implicit decisions
- Dither is ±0.5/255, applied only in some shaders.
- Only the sin-hash noise is used.
- Python's expat parser, not defusedxml.
- Chromium via SwiftShader, with skip-on-failure.
- A card-embedded checker with a fixed 1.5 stroke.

## Not checked
- Actual rendering and GPU behaviour.
- Whether `fmlib.lint` accepts the new cards.
- The `shader-performance` card contents.

Noticed: none
