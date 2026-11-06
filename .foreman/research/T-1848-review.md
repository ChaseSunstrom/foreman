**Verdict: changes needed.** The geometry is correct. One regression in the CLI error path should be fixed before this lands. I ran nothing; everything below is from reading the code.

## lens: intent
- none. The acceptance criteria are covered: the blob is closed, deterministic per seed and bounded by `--grid`, and it passes `fm scene check`.

## lens: adversary
- none. No untrusted input reaches a sink. The ints are range-checked, and `--out` goes through `write_atomic`.

## lens: edge
- MEDIUM — `plugin/lib/fmscene.py:1264,1275,1289` (check at 1316) — Making FILE optional breaks the error path of `shader`, `soak` and `check`. The new "needs FILE" check at 1316 sits after the code that reads `args.path`. Before the change, argparse rejected a missing FILE with exit 2 and a usage line. Now `fm scene check` hits `args.path.lower()` at 1275 and raises AttributeError. `fm scene shader` passes None to `shader_paths` at 1264, and `fm scene soak` passes it to `os.path.abspath` at 1289. The handlers catch only OSError, ValueError and the like, so each ends in a traceback instead of the clean `fm: scene: X needs FILE`, exit 2. Fix: put the `if not args.path` check straight after the metaballs branch, before the shader branch, or move the metaballs branch to the top and the check right under it. Confidence: high (confirmed by reading).
- LOW — `plugin/lib/fmscene.py:1307,1252` — `fm scene metaballs blob.json --out blob.json` is refused with a cut-off message, `--out blob.json is `, because `_write_out` is called with `what=""`. Any FILE given to metaballs is otherwise silently ignored. Fix: refuse a FILE in the metaballs branch (`if args.path: ... "metaballs takes no FILE"`) and drop the `what` argument. Confidence: high.

Verified safe:
- **Divide by zero:** `vertex()` is only ever called on one inside corner (val > 1) and one outside corner (val ≤ 1), so `val[b]-val[a]` is never 0. The field adds 1e-12 to d², so it has no zero divisor either.
- **Box growth:** it terminates. Every term starts with `half - m ≥ r > 0` and shrinks as `half` grows. `half - max|c|` is a true lower bound on the distance from a ball to any box face, so the box faces stay under 0.9 and the surface never reaches them.

## lens: operator
- none. The runtime at grid 48 with 12 balls is a few seconds of pure Python for a single use, and the output is well under `MAX_FILE`. The docs match the code, except for the unchecked vertex count below.

## lens: maintainer
- MEDIUM — `plugin/tests/test_scene.py:753` — The test meant to guard the "others still need FILE" change only asserts a nonzero return code, and `check=False` means a traceback (exit 1) passes it. It cannot catch the regression above. Fix: assert `returncode == 2` and "needs FILE" in stderr, for `check`, `shader` and `soak`. Confidence: high.

## Acceptance criteria
- Metaballs prints a scene.json that `fm scene check` accepts: **met** (CLI round-trip test, and `validate()` is called inside `metaballs`).
- One closed blob mesh with faces facing out: **met by reading.** The orientation rule is right in all three cases, which I derived by hand with `n·u = det`:
  - 1 in: reverse when `det ≤ 0`.
  - 3 in: reverse when `det > 0`.
  - 2 in, quad `[pr, ps, qs, qr]`: reverse when `det(p,q,r,s) < 0`.
  - TETS is the six-tetrahedra split around the 0→7 diagonal, which fits together across neighbouring cubes.
- Deterministic per seed: **met** (a private `random.Random(seed)`).
- Bounded by `--grid`: **met**, the range is 8 to 48 and out-of-range values raise ValueError.

## Implicit decisions
- The surface is the field value 1, with a corner at exactly 1 counted as outside.
- Ball positions are uniform in ±0.8 and radii in 0.35 to 0.6.
- The surface is interpolated linearly in the field value.
- The spin is 12 s about +Y, around the origin and not the blob's centre.
- The camera is placed from the box size, the floor sits 0.02 under the lowest vertex, and the lights are fixed.
- The scene is written with `indent=2`.

## Not checked
- The doc's "about 16,000 vertices at 48". My rough estimate is a few thousand, so it may be overstated. Measure it.
- A coarse grid (8) with many balls could miss a small isolated ball. If every ball were missed, `min()` at line 1230 would raise a cryptic ValueError. I could not trigger it by hand.
- Rendering.

Noticed: the same `args.path`-before-validation pattern would hit any future action that reads `args.path` ahead of the FILE check.
