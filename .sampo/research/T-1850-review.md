**Verdict: approve with nits.** `bench()` matches the data shape of the records. I found no crash from real `fm code bench` output. The three real defects are LOW and only bite hand-edited or corrupt `code-bench.jsonl`, or give a weak test.

## lens: intent
- LOW — plugin/lib/fmscene.py:1365 — Every record in the last 12 shares one axis: no model, worker, `variant` or `seed_set` is shown, and mesh names are window indexes (`operator-3`), not run ids. A run with a different model or variant looks like a regression with no way to tell. — Say so in the CHANGELOG or help, or filter `history()` to the latest record's (model, worker, variant). — medium
- LOW — plugin/lib/fmscene.py:1380 — `--days`, `--balls` and the like are silently ignored by `bench`. This matches the other showpieces, so it is not new. — none needed. — low

## lens: adversary: ok
- Seed names are cleaned to `[A-Za-z0-9_-]` (:1373), so the terminal and the module's object literal get no control characters or `__proto__`. `float()` error text uses repr, which escapes control characters.

## lens: edge
- LOW — plugin/lib/fmscene.py:1365 — Only `ValueError` is caught at :1453, but a bad `results` or `seconds` can raise other errors. Triggers:
  - `"seconds": [1]` or `{}` raises TypeError.
  - `"seconds": 1e999` or `Infinity` is a float inf, and `h` becomes NaN. `validate` rejects it with ValueError, so it exits 2 with a message.
  - `"seconds": 10**400` raises OverflowError, an uncaught traceback.
  - `"results": 5`, or a non-dict entry such as `["x"]`, raises TypeError or AttributeError. `history()` only checks for `"score"`.
  - Fix: either skip bad cells, or catch `(TypeError, AttributeError, ArithmeticError)` in cmd_scene and re-raise as ValueError, as T-1847 did. — high
- Name rules held up under checking:
  - Names are at most 48 + `-NNN`, and `_k` fallbacks end in `_digits` while firsts end in `-digits`, so the fallback can't collide the way terrain's did. They can't reach `floor` or `camera`, and `"s"+base` covers a leading digit, hyphen or underscore, or an empty seed.
- Camera framing is fine at both ends:
  - 1 run and 1 seed puts the camera at about [1.6, 4.6, 6.2] and 5.2 wide.
  - 12 runs and about 8 seeds is about 19 by 14 with the camera 22 away; the field of view covers it.
  - `far`/`near` is 2000, under the 10,000 cap.
  - If every run is all-skipped except one, empty columns still take width. That is cosmetic.
- No cap on box count, though real records stay small. — low

## lens: operator
- Cost is negligible: one JSONL read and at most 12 × seeds boxes.
- The docs match the code. The `scene-3d.md` edit also trims the metaballs line, dropping `(--grid 8-48)` (unrelated to bench, probably done for budget). — LOW, scene-3d.md:127.

## lens: maintainer
- LOW — plugin/tests/test_scene.py:167 — The no-runs path asserts only `returncode != 0` with `check=False`, so a traceback (exit 1) passes. This is the same nit as T-1848 and T-1849. — Assert `(returncode, "no fm code bench results" in stderr) == (2, True)`. — high
- LOW — plugin/tests/test_scene.py:142 — No test covers a malformed `seconds`, a collision between cleaned names such as `a b` and `a-b` (the `_k` loop at :1376), or a non-alphabetic seed (`"s"+base`). — Add one assert each. — medium
- Test arithmetic checks out. 2.1 and 0.1 follow from log1p, `runs * 10` gives 12 operator boxes, and the skipped case would be named `rm-rf-3`.
- No bench-specific duplication of an existing helper.

## Acceptance criteria
- `fm scene bench` prints a scene that `fm scene check` accepts: met. `validate` runs inside `bench()`, and the CLI test runs `check` on the output.
- A box per run and seed, green or red by `closed`: met (:1380).
- Heights are log-scaled seconds: met (:1379).
- Errors with no runs: met (:1367). `history()` returns `[]` for a missing file.

## Implicit decisions
- Skipped seeds get no box and no axis slot.
- Seed axis order is alphabetical, not run order.
- The 12-run window is a hard-coded constant.
- Runs from every model, worker and variant share one window.
- `seconds` of 0 or below clamps to a 0.1 stub box.

## Not checked
- Rendered output, since I ran nothing.
- The `fm code bench` writer beyond the record shape.

Noticed: none
