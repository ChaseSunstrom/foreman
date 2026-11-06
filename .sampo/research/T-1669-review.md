**Verdict:** approve with nits. I read the code but didn't run the tests; I haven't confirmed that `python3 plugin/tests/run.py test_drill test_design_gates` passes.

## lens: intent
- MEDIUM — plugin/lib/fmdesign.py:306 and :2017 — A would-block is keyed on `digest`, a hash of every UI file, so any edit to any UI file while one must still fails counts as a new would-block. The test's `change()` edits only a CSS comment. Ten unrelated saves promote the gate to blocking, so `n` counts edits, not distinct false-positive opportunities. — Key on `[gate, failing]` plus a hash of only the files the failing must names, or say in the docs that an edit is the unit. — medium
- LOW — plugin/lib/fmdrill.py:694-695 — A `skipped` fault (unreadable as root) counts as a pass and `ok` is true, though nothing was planted. It's still named in the report. — Fail, or mark the report "N planted of M", when any fault was skipped. — medium

## lens: adversary
- LOW — plugin/lib/fmdesign.py:313-319 — Any caller, including the model, can run `fm design check --wrong GATE` to demote a blocking trial gate. There is no human check or guard category. Editing DESIGN.md already bypasses the gate, so the added risk is small. — Say in MASTER that the mark is a self-report, or gate `--wrong` behind `fm ask`. — medium
- LOW — plugin/lib/fmhooks.py:748 and plugin/lib/fmcli.py:1215 — Every `PermissionError` with a filename is now called a "state error" and skips the circuit breaker. That includes an unreadable `transcript_path` or a non-executable tool, and the message says "fm fsck lists it" when it doesn't. A hook that always fails then never pauses. — Limit it to paths under `c.state_dir()`. — medium

## lens: edge
- LOW — plugin/lib/fmdesign.py:299-319 — The read-modify-append of `design-trials.jsonl` isn't under `c.lock(p.dir)`. Two concurrent checks both append the same key, so `n` and `w` double-count. — Wrap `trial()` in the project lock. — medium
- LOW — plugin/lib/fmdesign.py:293-297 — Outside a project, `--wrong GATE` is silently dropped with exit 0 plus a note, so it looks as if it was marked. — Return the `ValueError` when `wrong` is set and `p` is None. — high
- LOW — plugin/lib/fmdesign.py:1995 — A trial gate acting as blocking doesn't get a11y's blocking strictness (`mode == "blocking"`), so "no pair checked" passes. — Pass `mode in ("blocking", "trial")`. — medium

## lens: operator
- LOW — MASTER.md (the `fm fsck` line) — The inserted "state JSON files … (T-1669)" clause splits "(the last 64 KB, read twice before it's called torn)" from the journal clause it belongs to, so the sentence now misreads. — Move the new clause after the journal clause. — high
- LOW — plugin/lib/fmfixes.py:137, plugin/lib/fmserve.py:552, 957, 977 and plugin/lib/fmhooks.py:2038 — These plain `open(..., "a")` appends weren't moved to `append_line`, so the "journals no longer glue" claim isn't complete. If they are journals, switch them. — low

## lens: maintainer
- MEDIUM — plugin/tests/test_drill.py:1005-1040 — Every drill test asserts a pass, so nothing shows the drill fails. `_verdict`'s "missed" branch, a crash, the exit-1 path and the kept home are all untested, and a detector that always says "found" would stay green. Only `crash()` is unit-tested. — Add a test that monkeypatches `fsck` (or plants an undetectable fault) and asserts exit 1, `ok` false, and the home still existing. — high
- LOW — plugin/lib/fmdesign.py:304 vs 327 — The local `blocks` in `trial()` shadows the module function `blocks()`. — Rename the local to `hits`. — high

## lens: design
Not applicable. The only UI-file edit is a non-visual `append_line` swap at plugin/lib/fmcodetui.py:2651.

## Acceptance criteria
- A seeded compound-fault day passes in a temp home, names each fault and replays a seed: met. `test_a_drill_passes…`, `test_every_kind_at_once…` and `test_a_seed_replays…` cover it. Replay is tested only as plan equality, not as equal verdicts.
- A trial gate promotes and demotes by its overridden rate: met. `test_ten_would_blocks_block_and_a_wrong_one_demotes` covers it.
- Test run: not verifiable from the code.

## Implicit decisions
- Promotion needs 10 would-blocks at under 10% marked wrong, judged over the last 20.
- A new would-block means a changed digest of all UI files.
- `design-trials.jsonl` is read as its last 2000 lines.
- Corrupt `meta.json` exits 4 and is never read as `{}`.
- Only state files under 1 MB, at the top of `state/` or of a project, are judged for corrupt JSON.
- The default seed is the clock modulo 10^6.
- The drill strips `FOREMAN_*` and `GIT_*` from the environment and keeps the rest.
- `sha1` is used as a key only, not for security.

## Not checked
Test execution, the real runtime of the drill (about 16 subprocesses per run), and the remaining non-`append_line` writers.

**Noticed:** `fm drill` has no scheduled or CI run, so the detectors it exercises could regress unseen; consider a task to run it from `fm check`.
