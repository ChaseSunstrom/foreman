**Verdict:** approve with nits. I found no defects in the feature itself. The data sources, validation, name handling and layout all hold up. I did not run the suite, because I was read-only.

## lens: intent
No findings. `airlock` returns a validated scene with a box per held category named after it and a `through` box. Heights come from `log1p` scaled to the largest count (`fmscene.py:1336,1342`). Outside a project it exits 2 with a message (`fmscene.py:1406-1415`). The CHANGELOG matches the behaviour. The 30-day default is documented in the help, the CHANGELOG and the code.

## lens: adversary
No findings. Category text reaches mesh names only through `re.fullmatch(r"[a-z][a-z0-9-]{0,40}")` and the gate-name check (`fmscene.py:1335`). Anything else becomes the literal `other`. The `what` string carries only numbers, so no ledger text reaches the terminal. `--out` goes through the existing `_write_out`.

## lens: edge
No findings.
- The data sources are correct. `fmhooks.py:1784-1792` writes `guard_block` with `data.category` to the ledger and `project: p.slug` to the global event log. `fmhooks.py:2736-2737` writes `tool` and `tool_fail` with the same slug. A worktree resolves to the main project's slug through `find_project`, so the two sides agree.
- The worst case is 14 categories plus `other`, which is 15 boxes. The last row sits at x≈-7.2, inside the 20-wide floor.
- The camera does not look through the `through` box.
- `global_events` reads at most 200,000 lines per file. `state/events.jsonl` has 6,257, so truncation is theoretical.
- With nothing held and no calls the command still draws a gate and a 0.1-high `through` box. That differs from terrain, which raises on an empty window, but it is defensible.

## lens: operator
No findings. It is a one-shot read of the ledger and the global event log. It adds no hook, loop or schedule and installs nothing. The CHANGELOG, MASTER.md, help text and playbook agree with the code.

## lens: maintainer
- LOW — `plugin/tests/test_scene.py:794,797` — This repeats the earlier nit on T-1848. Both error-path assertions are `assertNotEqual(..., 0)` with `check=False`. A traceback (exit 1) passes them, so they would not notice a crash replacing the refusal. Trigger: `guard_counts` raising `TypeError` for `--days 0`. Fix: assert `returncode == 2` and that stderr contains `1 to 3650` and `not in a Foreman project`.
- LOW — `plugin/lib/fmscene.py:1367` — The code hand-rolls `time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(...))`. `fmcore.iso(epoch)` at `fmcore.py:74` already does this. Fix: `since = fmcore.iso(time.time() - days * 86400)`, which also removes the `import time`.

## Acceptance criteria
- `fm scene airlock` prints a scene that `fm scene check` accepts, with a box per held category, a `through` box, log-scaled heights, and an error outside a project: met by the code. `test_scene.py:761-797` covers each part (the box names, `validate`, the heights and the `check` round-trip). The error cases are asserted loosely (see the maintainer finding). I did not run `python3 plugin/tests/run.py Airlock`.

## Implicit decisions
- The window is 30 days by default, and `--days` is limited to 1–3650, as for terrain.
- A category that is not a valid mesh name, or that collides with a gate name, is folded into `other`, and a missing category also becomes `other`.
- "Through" counts `tool` plus `tool_fail` events, not blocked calls.
- Zero counts get no box. An empty record still draws the gate.
- At most six colours, cycled.
- `--days` is silently ignored by metaballs.

## Not checked
The rendered look, because I viewed no screenshot or `fm scene cells` output. The test run. The CHANGELOG and MASTER.md prose beyond the airlock lines.

**Noticed:** `fm scene metaballs --days N` accepts and ignores `--days` without a note (`fmscene.py:1394-1395`).
