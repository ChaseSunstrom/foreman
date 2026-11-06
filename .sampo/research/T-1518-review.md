**Verdict:** approve with nits. I found nothing in `--repeat` that forges or weakens evidence. The canary has two real weaknesses. I had no shell, so I could not run the tests, and every reproducer below is by reading the code.

## lens: adversary
No forging path found.
- Each of the N runs goes through the same `c.run_command`, with the same `bash -c`, process group and redaction.
- `--repeat` with a typed result, with `--expect-fail`, or outside 1–50 is refused before anything is recorded (`fmcli.py:559-562`).
- The first failing run's code and output are kept, so a mixed set cannot record `exit 0`.
- The `[ran]` mark is set only when `args.run is not None`.
- Timeout kills the process group (`fmcore.py:513-519`) and the total is bounded.

## lens: edge
- MEDIUM — `plugin/lib/fmrelease.py:200-210` — Any failure that passes on one rerun is labelled "load flap" and gets no inbox capture, and the headline says "0 failing". The load figure is printed but never checked. A real intermittent regression, or a sentinel whose first run warms a cache, reads as a flap at load 0.1. The stub in the new test fails once at any load and is accepted. — Call it a flap only if the recorded load was high (for example at least the CPU count). Otherwise keep it as a failure and capture it, or capture flaps as low priority. — high
- MEDIUM — `plugin/lib/fmrelease.py:201-202` — The rerun is serial and has no time bound. Each `one()` can take 1800 s, so K projects that time out in the pool cost another K×1800 s, one after another. Timeouts and `couldn't run` failures are also not load flaps. — Rerun only real nonzero exits, or give the reruns a total time budget. — high
- LOW — `plugin/lib/fmcli.py:2054-2063` — With a tiny positive `--timeout` (for example 1e-6), `left <= 0` can break before any run starts. Then `code` is unbound (UnboundLocalError), and `statistics.median([])` would fail too. PLAUSIBLE, not reproduced. — Add `if not times: return 124, "timed out before the first run", ""`. — medium
- LOW — `plugin/lib/fmcli.py:2059,2066-2070` — A timed-out run reports `timed out after {left}s`, the remaining time, not the user's `--timeout` (`fmcore.py:519`). The timed-out run is also counted in median, min and max. When only 1 run completed, it prints "±0.000s (0%)", which looks like zero noise. — Leave timed-out runs out of the statistics, and print "spread n/a" when fewer than 2 runs completed. — high
- LOW — `plugin/lib/fmrelease.py:226-227` — A flap-only canary sends a notification reading "0 project(s) failing: , 1 load flap(s): x", with a stray comma. — Build the message from parts. — high

## lens: maintainer
- LOW — `plugin/lib/fmcore.py:3365` — The diff turned `_BUILTINS = {` into `_BUILTINS ={`. — Restore the space. — high

## lens: intent
- LOW — `plugin/lib/fmcli.py:520-535` — The "before/after view" only echoes the hand-typed Measurements section. Nothing links it to the `--repeat` medians. "receipt" is also already the name of the finish receipt and the UI playbook's evidence receipt. — Say so in the help text, or fill Measurements from the repeat evidence. — medium

## Acceptance criteria
- `--repeat 5` records median and spread: met. `fmcli.py:2046-2071` computes them correctly. N=2 gives MAD = (b−a)/2. N=1 skips timing entirely.
- The canary marks a load flap: met, but the classification is weak (the first MEDIUM finding above).
- A UI task's receipt lists files in reading order: met. I found no crash for deleted files or files outside the repo. `tour` lists git paths only, and deleted files get `(deleted)`. `tour` reads each changed file and runs a regex over the others, so a very large task slows `receipt` the same way it slows `fm tour`.
- `test_verify_strength.Repeat` passing: not verifiable here.

## Implicit decisions
- All N runs execute after a failure; the failing run's output is the one shown.
- `--repeat 1` records no timing.
- A flap is never counted green and is never captured.
- `--timeout` is now a total across the runs.
- The reading-order groups are code, styles, components, entry points, tests, then docs.

## Not checked
Whether `test_docs` requires MASTER.md or CHANGELOG entries for `fm task receipt` and `--repeat`. How `fmguard` treats `--rep` abbreviations (`--repeat` was already in `_FM_VALUED`).

**Noticed:** `fmrelease.py:177` — `subprocess.run(..., text=True)` has no `errors=`, so undecodable sentinel output raises in a pool thread and aborts the whole canary.
