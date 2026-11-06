**Verdict: approve with nits.** I found no HIGH or MEDIUM defects. I only read the code; I had no way to run the tests, so I did not run `python3 plugin/tests/run.py Graph`.

## lens: intent
Ok. The scene has a box per task, height from `TIER_HEIGHT`, colours read from `graph.html`'s `--graph-*` tokens, a ground slab per layer, and a key of counts per status. `--out` and `--cells` on any other page are refused, and no page is written.
- LOW — plugin/lib/fmpage.py:604 — `graph_cells` keeps only the newest 1500 tasks and says nothing about it. The page says "N older tasks are not drawn". Here the key's counts quietly sum to at most 1500, and a broken cycle is not mentioned either. — Compute `left = len(tasks) - GRAPH_MAX` and append "N older not drawn" to the key line. — confidence high.

## lens: adversary
Ok. The output holds only fixed status names, integer counts and colours taken from the template. No task title or id reaches the terminal. A tier outside S/M/L falls back to 0.5 through `TIER_HEIGHT.get`.

## lens: edge
- LOW — plugin/lib/fmpage.py:591,595 — `near = far/10000` is compared by `fmscene.validate` (fmscene.py:149) as `far <= 10000*near`. Float rounding can leave `10000*near` one ulp below `far`. That only happens when `far > 1000`, which needs a chain of roughly 120 or more layers. `graph_scene` would then raise ValueError "camera.far", and `graph_page` would print it as a usage error. — Use `near = max(0.1, far/5000)`. — confidence plausible, not reproduced.
- LOW — plugin/lib/fmpage.py:581-582,593-594 — A token in `graph.html` written as uppercase hex or `#rgb` fails the regex. `tokens[s]` then raises KeyError and the user sees a traceback, not a usage error. The test only pins `active` and `bg` (test_showpieces.py:132-133). — Assert every key in `GRAPH_STATUSES + ["floor"]` against the template in the test. — confidence medium.
- LOW — plugin/lib/fmpage.py:734 and plugin/lib/fmcli.py:36 — `--cols` is range-checked only after the layout and scene are built, so `--cols 500` on a big graph does that work first. `--cols N` without `--cells` is silently ignored. — Check the range at the top of the `args.cells` branch, and reject `--cols` unless `--cells` is given. — confidence high.
- The `fmraster.render` pixel budget (fmraster.py:126) turns an oversized render into a ValueError, which the `except ValueError` at fmpage.py:735 catches. That is handled.

## lens: operator
Ok. It is a one-shot user command with no hook or loop. The cost is pure-Python rasterising, bounded by the `WORK` budget in fmraster, so I found nothing to multiply out. The task recorded no timing for a 1500-task graph.
- The MASTER.md and CHANGELOG entries match the code (default `--cols 64`, range 2-400, no page written).
- At 64 columns, a graph hundreds of layers wide draws boxes smaller than a pixel. The key then carries all the information.

## lens: maintainer
- LOW — plugin/lib/fmpage.py:604 — This repeats the sort-and-slice at the top of `graph_html` (fmpage.py:667-670). The two copies can drift. — Share one helper. — confidence medium.
- LOW — plugin/tests/test_showpieces.py:125-144 — No test checks the camera framing. The test only asserts more than 4 distinct colours, so a regression in `dist` or `wide`/`deep` that crops most boxes still passes. The first test also runs only on the 34-task fixture. — Add a test with a 40-layer chain. It should check that `validate` accepts the scene and that the first and last tasks' colours appear in the drawn lines. — confidence high.

## Acceptance criteria
- `fm page graph --cells [--cols N]` prints the scene through `fmscene.cells` with height by tier, colour from the graph's tokens, a ground per layer and a key of status counts: met by the code (fmpage.py:575-613, 727-738). The new `Graph` tests cover it. I did not run them.

## Implicit decisions
- Default `--cols` is 64.
- The camera sits at 35° elevation, 35° field of view, aimed at `[0, 0.4, 0]`, with a framing margin of 1.1.
- The ground is a 0.05-thick slab.
- Escape codes are written even when output is piped, the same as `fm scene cells`.
- A task with an unknown status is drawn as captured.

## Not checked
Whether `fm page graph --cells` renders correctly in a real terminal. How long a 1500-task graph takes to draw. Whether rounding in the `far`/`near` comparison actually fails.

**Noticed:** none
