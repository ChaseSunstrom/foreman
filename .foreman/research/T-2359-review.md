**Verdict: changes needed.** Nothing is wrong with the ratchet's core logic. But the hook p95 leg can turn the sweep red on an unchanged tree, a failure in the lean row crashes the whole sweep, and the `put` wiring has no test.

## lens: intent
- MEDIUM — plugin/lib/fmdoctor.py:34 — `hook_p95` runs `run_bench(20)`. `bench_hooks.py:113` takes index `int(20*0.95)=19`, which is the maximum of 20 samples. The metric is therefore the median of three maxima, with a zero band. Equal true latency compares `cur > start` roughly half the time, so the sweep goes red on an unchanged tree. The AC mandates "no band", so keep that. Instead cut the noise: more runs, such as 30 or more, and compare `cpu_p95` when `bench_hooks.load_per_core() > 1`, as `within()` does. At a minimum, print one decimal at fmgenesis.py:147, because `40.0 -> 40.4` currently renders "hook p95 40 -> 40 ms" as a failure. — confidence: high
- MEDIUM — plugin/lib/fmgenesis.py:145 — The footprint and verb metrics read `p.root/plugin`. The hook p95 comes from `fmdoctor.PLUGIN` = `c.PLUGIN_ROOT`, the copy of fm that is running (`bench_hooks.py:17-19`). If `fm genesis sweep` runs from an installed copy or a different checkout than `p.root`, the generation's own hook changes are never measured. Pass the bench `p.root/plugin` or refuse to judge when the two paths differ. — confidence: medium (it depends on how fm is launched)
- LOW — plugin/lib/fmgenesis.py:149 — `row()` clips `bad` to 8 entries (fmgenesis.py:2943), and `bad + more + less` is one list. On a red sweep with many added verbs, the "removed against added" listing (AC2) is cut off. Cap `bad` separately, or put `less` and `more` ahead of the clip. — confidence: high
- LOW — plugin/lib/fmgenesis.py:145-151 — If the start `hook_p95` is None (bench unavailable at `put`, or the gen-1 fallback), the hook leg is skipped without saying so. The pass detail reads "no metric above its start". Add "hook p95 not judged" to the detail. — confidence: high

## lens: adversary
ok. The archive and tar extraction go into a TemporaryDirectory from git's own output, and git runs with `hooksPath=/dev/null` and `fsmonitor=false`. I found no untrusted-input path.

## lens: edge
- MEDIUM — plugin/lib/fmgenesis.py:2976 — `_lean_row` is not wrapped. `hook_p95` catches only the import. A `CalledProcessError` from `_scratch_project`, a `TimeoutExpired` or `FileNotFoundError` (git or tar) in `_lean_at_seed` (fmgenesis.py:110-122) propagates out of `sweep`. That loses every other row and `sweep.md` is never written. `put` guards the same call; `sweep` should too, turning an exception into a ✗ "lean: could not measure: …" row. — confidence: high
- LOW — plugin/lib/fmgenesis.py:106 — The fallback uses the seed file's current mtime. If the tower is rewritten or re-put, the mtime moves later and the baseline commit moves later with it, hiding growth. `rev-list --before` also depends on commit-date ordering. — Use the seed's first-filed record if one exists. — confidence: low

## lens: operator
- MEDIUM — plugin/lib/fmdoctor.py:33-35 — Each `hook_p95` call runs `run_bench` three times. Each run spawns a scratch project (about 26 fm calls) and all 15 fixtures × 20 runs, while only the 2 non-script PreToolUse fixtures are used. That is about 900 hook subprocesses per call, and it happens on every `put` of a seed and on every sweep rerun. I didn't time it; at roughly 60 ms each it is probably a minute or more. Give `run_bench` an `only=` fixture filter. — confidence: medium on the size, high on the waste

## lens: maintainer
- MEDIUM — plugin/tests/test_genesis.py:199 — The test calls `record_lean` directly ("what put does"). Deleting the `put` hook at fmgenesis.py:53-57 fails no test. Nothing covers `fmdoctor.hook_p95` either (the median of three, excluding `:script` fixtures, and the None case), and no test covers the sweep failing when `_lean` or the bench raises. Add a test that does `put` of `gen-1/seed.md` and then asserts that `_lean_record` is set, plus one for `hook_p95` with `run_bench` mocked. — confidence: high
- LOW — plugin/lib/fmgenesis.py:78 — The `add("…"` regex is applied to old commits' `fmcli.py` as well. If an older tree registered verbs another way, the verb count there is 0 and the current count then reads as growth from 0 to N. I didn't check history. Treat `verbs == 0` at the fallback as "not judged". — confidence: low (lead)

## Acceptance criteria
- AC1 (`put` records footprint, verbs and hook p95; sweep fails on any growth with no band, naming each; equal or lower passes; gen-1 is measured from the seed's commit): partly met.
  - The logic is present, and the test asserts `put`'s `record_lean`, equal-passes, growth naming and the fallback.
  - Not met in practice: the hook leg is noisy, and the gen-1 fallback never judges hook ms.
  - I did not run `python3 plugin/tests/run.py test_genesis`.
- AC2 (the sweep lists what was removed against what was added): met on a pass. On a red sweep it can be truncated (see the LOW above).

## Implicit decisions
- The start record is kept once, at the first `put` of a seed, in `genesis-lean.json` under `p.dir`.
- Verbs are the `add("name"` regex matches in `fmcli.py`.
- Hook p95 is the maximum over PreToolUse fixtures, scripts aside.
- A tree that isn't Foreman's own, or a gen with no start, passes ("not judged").
- The fallback judges footprint and verbs only.
- A rename counts as one removed and one added verb.

## Not checked
I did not run the tests. I did not check the `MASTER.md` hunk, which the diff left out. I did not view the real `fmcli.py` history, and I did not measure the bench.

Noticed: the CHANGELOG and MASTER entries are fine. The bench has no fixture filter, so any caller that wants only a few hooks pays for all 15.
