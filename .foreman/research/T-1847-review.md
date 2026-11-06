**Verdict: changes needed.** The math and the three.js conventions check out. The faults are in hostile-input handling and in what the notes leave unnamed.

**Verified correct (by reading the code against three.js; I had no shell and ran nothing):**
- `_mat4mul` is column-major `a*b`.
- `_decompose` matches `Matrix4.decompose` and `Euler.setFromRotationMatrix` XYZ, including the 0.9999999 gimbal branch and the sign flip for a mirrored matrix.
- The camera looks along `-world[8:11]`, and `zoom` narrows the fov as `2*atan(tan(fov/2)/zoom)`.
- A missing index becomes triples of consecutive vertices, and an index array is sliced into faces.
- The light mapping is right, and the camera path's target name `camera` is reserved.

## lens: adversary
- MEDIUM — plugin/lib/fmscene.py:799,770,764 — The file's `type` and `uuid` go raw into the notes, which `print` writes to the terminal at 1176–1181. `validate` goes through `_show` to avoid exactly this. Failing input: a child `{"type":"\u001b]0;pwned\u0007"}` or `"\u001b[2J"`. Fix: use `_show(t)` in all three messages, and cap the number of notes. — high
- MEDIUM — plugin/lib/fmscene.py:768,734 — Every mesh that references the same BufferGeometry gets its own copy of the vertex list, and nothing caps the total. Failing input: a 1 MB doc with one 50k-float geometry and 5,000 Mesh children pointing at its uuid. That is about 80M vertex lists, so memory blows up. `MAX_FILE` bounds the file size, not the amplification. Fix: count total vertices and raise `ValueError` past about 1M, the size the comment at line 46 says fits. — high

## lens: edge
- MEDIUM — plugin/lib/fmscene.py:1173 — `cmd_scene` catches only `OSError` and `ValueError`, so the cases below crash with a traceback. Fix: wrap the `from_three` call and re-raise `TypeError`, `AttributeError` and `ArithmeticError` as `ValueError`.
  - `"color": null` raises `TypeError` in `_hex` at 746.
  - `"fov": "50"` raises `TypeError` at 793.
  - `{"type": [1]}` raises `TypeError` at 775 (unhashable).
  - A geometry `{"type": null}` raises `AttributeError` at 719.
  - A matrix entry of `10**400` raises `OverflowError` in the `sqrt` at 681.
  - A camera matrix with a zero third column raises `ZeroDivisionError` in `_unit` at 788.
- LOW — plugin/lib/fmscene.py:783 — `validate` raises where a note would do. The first failing input is a DirectionalLight whose world position is the origin. The same applies to roughness above 1, sphere `widthSegments` above 256, and a fov under 1 after `zoom`. Any of these aborts the whole import with a message about a scene.json path. Fix: skip or clamp the value and add a note.

## lens: intent
- MEDIUM — plugin/lib/fmscene.py:762-800 — `visible: false` is never read, though `Object3D.toJSON` writes it. A hidden mesh, light or camera is imported and drawn. Fix: skip the object and its subtree, and note it.
- MEDIUM — plugin/lib/fmscene.py:746-757,684,711,787-797 — The acceptance criterion says what it can't carry is named, but these drops are silent:
  - A material's `side`, `opacity`, `transparent`, `wireframe` and `flatShading` are dropped. A MeshBasic or MeshPhong material becomes a lit Standard one; the test at test_scene.py:570 does exactly this and gets no note.
  - Shear is lost, although the docstring says so.
  - Camera roll is lost, because the up vector is fixed at +Y.
  - A light's `target`, `distance` and `decay` are dropped, as are fog and the root's `animations`.
  - A name like `Cube.001` or `Box 1` fails `NAME` and is renamed `meshN` with no note.
  Fix: add a note for each.
- LOW — plugin/lib/fmscene.py:795 — `far` is clamped to `near*10000` with no note. three's default camera (near 0.1, far 2000) always becomes far 1000. Fix: add a note when the clamp bites.

## lens: operator
- Cost is bounded by the 16 MB file cap apart from the amplification finding above. There is no hook, loop or schedule. The MASTER.md and CHANGELOG entries match the code.

## lens: maintainer
- LOW — plugin/lib/fmscene.py:1168-1172 — The `--out` check, the `samefile` check and `write_atomic` repeat the block at 1214-1218. Fix: factor out one helper.
- LOW — plugin/tests/test_scene.py:599-665 — No test covers a mirrored matrix, `zoom`, the fourth directional light, a rotated camera, `visible`, or any hostile input. Line 654 only asserts a nonzero exit code. Fix: add one test for each.

**Acceptance criteria:**
- The three.js scene becomes a scene.json that `fm scene check` accepts: met. The tests cover this path.
- What it can't carry is named: partly met, because several drops are silent (intent lens).

**Implicit decisions:**
- Only the first camera is used.
- A mesh keeps only the first of several materials.
- Without a camera, the default is fov 50 at [0,0,5].
- The camera target sits as far off as the camera is from the origin, with a minimum of 1.
- A straight-down camera is tilted by 0.06 degrees.
- Sphere `widthSegments` becomes `segments`.
- Rotation and position values are rounded to 6 decimals.

**Not checked:** I did not read the CHANGELOG and MASTER.md text in full. I did not read the scene-3d.md hunk. I did not run the tests.

**Noticed:** `_decompose(world)[0]` for lights at plugin/lib/fmscene.py:782 is just `world[12:15]` with rounding. It does needless work and can raise on overflow.
