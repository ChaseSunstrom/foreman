**Verdict: approve with nits.** The brief names no audit lens, so I covered intent, adversary, edge, operator and maintainer together. I could only read files, not run them. The golden hash and the tests are unrun from here, so I checked them by reading the code.

## lens: intent
- LOW — plugin/lib/fmraster.py:39-41 — The comment says shared-edge pixels "go to the first triangle drawn", which is not quite true. Each triangle computes depth as `(w0*iz0+w1*iz1+w2*iz2)//area`. Two triangles sharing an edge can floor to depths one unit apart, so the winner is decided by rounding, not by draw order. Only exact ties go to the first triangle. The output is still deterministic for a given input — fix: reword to "ties go to the first drawn; rounding can decide near-ties" — confidence high.

## lens: adversary
- LOW — plugin/lib/fmraster.py:55-59 — `_rgb(3)` returns `b"\0\0\0"`, because `bytes(int)` makes that many zero bytes. So `colour=3` or `background=3` is silently accepted as black. Reproducer: `fmraster.render([], 2, 2, background=3)`. Fix: reject `isinstance(c, int)`, or build the colour with `bytes(tuple(c))` — confidence high.
- LOW — plugin/lib/fmraster.py:105 — `focal`, `ambient` and `light` are not validated. `focal=0` silently becomes `width`, and a negative focal mirrors the scene so every face is culled. A float `focal` gives float maths, which usually fails later with an obscure `TypeError` in `range()`. `ambient=300` raises from `bytes()` mid-render. Fix: check `focal` is a positive int and `0 <= ambient <= 256` at the top of `render()` — confidence medium.

## lens: edge
- MEDIUM — plugin/lib/fmraster.py:103,126-136 — The cost limits don't bound the run time. The 4 MP cap limits the frame, but each triangle scans its whole clamped bounding box in pure Python, about 1 s per MP. Reproducer: 5,000 full-frame triangles at 2000x2000 is over an hour with no way to stop it. The module docstring says "keep frames small", but nothing enforces it, and scene.json will feed arbitrary triangle lists. Fix: add a work budget (the sum of box areas above a cap, e.g. `MAX_PIXELS * 16`) that raises ValueError, or cap the triangle count — confidence high.
- LOW — plugin/lib/fmraster.py:114-115 — A triangle with any vertex at `z < 1` is dropped whole, not clipped. A ground quad that crosses the camera plane vanishes entirely. NEAR=1 on integers only rejects `z <= 0`. The docstring documents this. Clipping would be needed before scene.json can hold large floors or walls — confidence high.
- LOW — plugin/lib/fmraster.py:125 — `ONE//z` is 0 once `z > 2^32`, so far triangles vanish silently. Depth also gets coarse at large z. This is harmless at current scales — confidence medium.

## lens: operator
- Nothing installs or changes defaults, and nothing calls the module yet (grep shows only fmraster.py and its test). The CHANGELOG and MASTER.md edits match the code. Both MASTER.md lines are very long, but that is the existing style.

## lens: maintainer
- LOW — plugin/tests/test_raster.py:229-230 — The comment says `facing(10**6)` is "too far to cover a pixel's centre". It is actually dropped by `area <= 0`, because every vertex floors to the same X and Y. The assertion passes, but it tests the zero-area guard, not far-away coverage. Fix: reword the message — confidence high.
- LOW — plugin/tests/test_raster.py:190 — The `Cube` class sits in `test_raster.py`, which also holds the T-1630 `Img` tests. The acceptance command `test_raster.Cube` still works. A later split into `test_img.py` would be tidier.

## Acceptance criteria
- Two renders of a lit cube are byte-identical PNGs: **met on reading, not run here**. `test_two_renders_are_byte_identical_pngs` compares the two PNG files. It also pins the sha256 of the pixels and checks that the PNG decodes to the same pixels.

## Your questions
- **Fixed-point maths:** correct. The edge functions on the 1/16 grid are exact integers. `w0+w1+w2` equals `area` and the per-column steps `-dx[i]` have the right signs. The bounding box is conservative, so no pixel centre is missed. Shared vertices floor identically, so no cracks. Python ints cannot overflow. The only wraparound-like limit is that `ONE//z` is 0 past about 4.3e9.
- **Depth buffer:** the sentinel 0 with a strict `>` is fine, because the weights are non-negative and the floor is safe.
- **Culling and shading:**
  - Back-face culling uses the sign of the screen-space area, which is consistent.
  - I traced `facing()` by hand. Its normal is (0,0,-100), toward the camera, so it is lit when the light vector is (0,0,-1).
  - `min(256, …)` absorbs the isqrt floor.
  - `cube()` flips each triangle so its normal points outward. `_turn` is a proper rotation, and it is exact for the default half=100.
  - Cubes with other `half` values get floor-distorted faces, which stay deterministic.
- **Top-left rule:** not needed. There is no blending and the edges are inclusive, so nothing is missed or double-written. The result is deterministic. A top-left rule would only matter for blending or for exact-tie symmetry. Keep the current rule and fix the comment.
- **Near plane and cost limits:** see the edge findings above. Dropping triangles is acceptable for now. The missing work or triangle cap is the one real gap.
- **PNG bytes versus zlib builds:** the design is right. The golden hash covers pixels only, which don't depend on the zlib build. The PNG comparison happens within one process, so it can't fail on a zlib difference. Don't pin PNG bytes.
- **API as a base for scene.json (T-1633):** `render(tris, w, h, focal, light, ambient, background)` and `save` are a reasonable base. Integer-only input is a strict contract, and JSON floats raise loudly. T-1633 will need a quantising layer. It will also need a camera or transform layer, because the camera is fixed at the origin looking along +z and only `cube()` can rotate. Near-plane clipping and the work cap should come first.

## Implicit decisions
- Left-handed camera space (x right, y up, z ahead), with clockwise front faces as in Direct3D.
- 1/16-pixel subpixel grid, pixel centres at +8, and inclusive edges (`>= 0`).
- Depth is the interpolated 1/z scaled by 2^32, with 0 meaning nothing drawn. Ties go to the first triangle.
- A single flat directional light with a fixed default (1,2,-3), ambient 64/256, and shade as `c*shade>>8`.
- Rotation only through rational (c, s, d) triples, 3-4-5 by default. PNG output is RGB through `fmimg.save` at zlib level 6.
- The frame cap is 4 MP and the default focal length equals the width.

## Not checked
- I did not run the tests or confirm the golden hash.
- I did not check the `fmimg.save` internals beyond its signature and its atomic rename.
- I did not check MASTER.md drift tooling.

Noticed: add near-plane clipping and a per-render work budget to fmraster before T-1633 feeds it scene.json.
Noticed: `_rgb` accepts a bare int such as `3` as black (plugin/lib/fmraster.py:55).
