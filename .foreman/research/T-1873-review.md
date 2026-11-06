## Verdict
Approve with nits. The feature works as described, and the refactor of `cmd_scene` into `_builtin` keeps the existing behaviour. One MEDIUM finding: the time-budget test doesn't time the scenes the gallery actually draws.

## lens: intent
- MEDIUM — plugin/tests/test_scene.py:219-227 — The request's "each renders small under a time budget" is checked only on `SAMPLES` and `metaballs(5,16,0)`. The gallery draws `_builtin` scenes from real data. A sample lookbook has 1 look and a sample terrain has 2 rows by 5 columns. The real ones are up to 8 looks and 10 rows by 40 columns, which is about 20x the triangles. A slow `_frame` on real data passes the test, and the CLI test at :229 has no budget at all. Fix: time `fmscene.gallery()` (or the real-size `terrain`, `lookbook` and `bench` builders) against a budget, in addition to the samples. — confidence high
- LOW — plugin/lib/fmscene.py:128-131 — `churn` can wait up to 60 s on git (fmscene.py:1302) with no overall budget for `gallery`. A caption such as `a sample: 0 looks: 1 to 12 hang`, from `lookbook` raising on an empty look folder, is a confusing reason. Fix: catch the empty case in `_builtin` and say "no look cards". — confidence medium
- LOW — plugin/lib/fmscene.py:113-116 — An empty guard record doesn't raise, so `airlock` draws a bare gate captioned "0 held in 0 categories" and never falls back to `SAMPLES["airlock"]`. The CHANGELOG says a sample is used "when there's none yet". Fix: raise ValueError when `held` is empty and `through == 0`. — confidence high
- LOW — plugin/lib/fmscene.py:130-131 — The PNG carries no labels. The "1. metaballs: …" captions exist only on stdout and in `--json`, so the sheet loses them when shared. Fix: say so in the help text, or write a sidecar `.txt`. — confidence medium

## lens: adversary
Nothing found. `--out` goes through `fmimg.save`, which uses mkstemp and `os.replace`, so a symlink is replaced and never written through. A directory or missing path raises OSError, which is caught. Captions interpolate only fixed strings plus `str(e)`, where `e` holds a path from the user's own cwd or state, as the other showpieces do.

## lens: edge
Nothing found. The no-git, no-project and no-bench cases fall back to samples through OSError or ValueError. `git` missing raises FileNotFoundError, which is an OSError, so it is caught. An unusual error type from corrupt state (for example KeyError) would still abort the whole sheet, but I found no reproducer. See Noticed.

## lens: operator
Nothing found. The CHANGELOG, MASTER.md, scene-3d.md and `--help` text agree with the code. Cost per call: one `git log --since=90.days --numstat`, one ledger read, one global-events read, and five software renders at 160x100. Nothing runs from a hook or a loop.

## lens: maintainer
- LOW — plugin/tests/test_scene.py:224 — The test hard-codes `metaballs(5, 16, 0)`, duplicating the namespace in `gallery()` (fmscene.py:124). If one changes, the other won't follow. Fix: expose the gallery's defaults as a constant, or time `_builtin("metaballs", ns)`. — confidence medium
- The error-path assertions (:241-244) check the exact `(2, True, False)` of return code, message and no traceback. This fixes the earlier "returncode != 0" nit.

## Acceptance criteria
- `fm scene gallery` writes one sheet and a caption per built-in: met. The test checks the PNG header, 480x200, 5 caption lines in order, and `--json`.
- Each built-in draws small under a time budget: partly met. The budget test covers the samples and a 16-grid blob, not the real-data scenes (see MEDIUM).

## Implicit decisions
- Five built-ins in a fixed order, 3 columns, 160x100 tiles, sheet background (17,17,17).
- Unturned view (turn 0) for every tile.
- Blob drawn at grid 16 instead of 32.
- Real-data defaults are terrain 90 days, airlock 30 days, lookbook 8 looks.
- Captions go to stdout and `--json` only, never onto the PNG.
- A sample is used only when the builder raises OSError or ValueError.
- `gallery` requires `--out` and takes no FILE.
- The 60 s churn timeout is inherited.

## Not checked
I did not run the tests and did not view the rendered PNG.

**Noticed:** `gallery()` catches only OSError and ValueError per tile (fmscene.py:128), so one corrupt look card or ledger entry that raises KeyError or TypeError takes down the whole index. A per-tile `except Exception` falling back to the sample would make the index robust.
