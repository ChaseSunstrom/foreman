## Verdict
Approve with nits. I found no blocker. I had no Bash tool, so I did not run any test, including `test_scene.Three`.

## lens: adversary (injection)
No finding. Nothing in `SCENE` is a free-form string.
- Every string is a `#rrggbb` colour (`fmscene.py:87`), a NAME-validated identifier (`:94`, ASCII, `fullmatch`), or an enum word.
- So `</script>`, backticks and quotes cannot get in.
- `json.dumps` (`:381`) escapes non-ASCII by default, so U+2028 and U+2029 come out as `\u2028`/`\u2029`.
- NAME must start with a letter, so `__proto__` is refused. `constructor` and `toString` are allowed and harmless, because the module reads materials through `Object.entries` into a `Map`.
- Python `repr` in `_show` escapes control and bidi characters in error text.
- `10**400` is caught by the `OverflowError` branch.

## lens: three.js API (r160+)
All four calls are correct for r155 through r170.
- `WebGLRenderer({canvas, context: gl})` takes a WebGL2 context. From r163 it reads `getContextAttributes().alpha` from the context, so `alpha: true` is honoured.
- `debug.onShaderError(gl, program, vs, fs)` exists and replaces the default `console.error`. `checkShaderErrors` defaults to true.
- `setClearColor(hex, alpha)` is fine. The clear colour is emitted in output sRGB, so there is no seam with the page.
- Colour strings in material and light constructors are read as sRGB and converted to linear from r152. `Euler.set(x,y,z)` keeps XYZ order.
- Three registers its own context-lost and context-restored listeners first, so it restores before the module's `render()` runs.

## lens: survival contract
All nine clauses are met, with these nits.

## Findings
## lens: edge / maintainer
- MEDIUM — `plugin/lib/fmscene.py:23` — "rotation … (X, then Y, then Z)" is ambiguous. Three's XYZ order is the matrix Rx·Ry·Rz, so a vector turns about Z first. A rasteriser that applies X first as a fixed-axis turn would disagree with three on any multi-axis rotation. — Say "matrix = Rx·Ry·Rz (three.js 'XYZ'); mesh transform = T·R·S" — high
- LOW — `fmscene.py:14-29` — Gaps the integer rasteriser (`fmraster.py:3`, camera on +z, `focal` in pixels, flat shading, one light) will have to guess: camera up is +Y and the camera looks down −Z (right-handed, versus fmraster's +z forward). A camera straight above or below the target is not refused. The sphere's height segments are `max(2, segments>>1)` (`:269`) but undocumented. Point-light decay is 2. Vertices geometry gets smooth normals in three but is flat in the rasteriser. — Add one line each to SCHEMA — high
- MEDIUM — `fmscene.py:301-302,371` — After `dispose()` calls `forceContextLoss()`, `getContext("webgl2")` on the same canvas returns the same permanently lost context. A remount (SPA or HMR) then builds a renderer on a dead context and fails or stays stuck. — `if (!gl || gl.isContextLost()) return () => {};`, or document that dispose needs a fresh canvas — medium
- LOW — `fmscene.py:360` — `([e])` reads the oldest IntersectionObserver entry. A queued out-then-in pair would leave the loop asleep on screen. — `entries.at(-1)` (the same flaw is in `templates/scene.html:273`) — medium
- LOW — `fmscene.py:308` — `fail()` stops the loop but keeps the renderer and context until `dispose()`. — Dispose the renderer in `fail` too — medium
- LOW — `MASTER.md:61` — `fm img` is listed there and `fm scene` is not. — Add an entry — high
- LOW — `fmcli.py:6039` — `--to` has a single choice and `args.to` is never read. — Fine if a second target is planned; otherwise drop it — low
- LOW — `plugin/tests/test_scene.py` — Nothing asserts that the compiled output contains no `</` and no non-ASCII. The symlink case of the `samefile` guard is also untested. — Add both tests — medium

## Acceptance criteria
- Camera, light, mesh and material compile to a module with the same camera: met by reading the code. `test_the_module_holds_the_camera_it_was_given` needs no node, but I did not run it.
- Pre-audit: the `console.log` in the test driver is its output channel, so dismiss it. The skip is a `node` guard on 2 of 3 tests and is acceptable. The large files are just where the diff landed.

## --out write path
Sound. `fmcore.write_atomic` (`fmcore.py:809`) uses mkstemp, fsync and `os.replace`, and removes the temp file on error. A symlink at `out` is replaced, not written through. `samefile` blocks overwriting the source, including through a symlink or hardlink. A directory target raises an OSError, which is caught.

## Implicit decisions
- ACES tone mapping with sRGB output.
- Transparent canvas when `background` is null.
- Loop defaults to true.
- 1.5 DPR cap on coarse pointers.
- Parser-level `import fmscene` (same pattern as `fmdesign`).
- Stdout when `--out` is absent.

## Not checked
Real-browser behaviour, `test_help` tiers, performance on a scene near the 16 MB cap, and the T-1633 steps (the brief doesn't include them).

**Noticed:** `plugin/skills/playbooks/references/ui/templates/scene.html:273` has the same stale-entry IntersectionObserver bug.
