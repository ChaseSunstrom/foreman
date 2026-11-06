## Verdict
Changes needed. One MEDIUM bug (an uncaught timeout aborts the whole bench) and one MEDIUM comparison flaw. The rest are LOW. I read the code and did not run it, because this role is read-only.

## Findings

## lens: edge
- MEDIUM — plugin/lib/fmcodebench.py:100 — The seed's own check, `subprocess.run(..., timeout=120)`, is not guarded. A graded model that edits `calc.add` into a loop that never ends makes the check raise `TimeoutExpired`. That aborts the run with a traceback, and the earlier seeds' results are lost because the jsonl is only written at the end (:172). The same applies to `git()` at :83 (30 s limit, missing git raises `FileNotFoundError`). Reproducer: serve a fake that edits `a - b` to `while True: pass`, then run `fm code bench --model fake --seeds operator`. Fix: catch `TimeoutExpired` and `OSError` around the check and report `closed=False, reason="verify timeout"`. Consider appending a record per seed. — high
- MEDIUM — plugin/lib/fmcodebench.py:166 — `previous` is matched on (model, worker, seed_set) only. A `--seeds operator` run is compared with the last full run. A 1/1 subset shows "last time 0.40" against a different seed mix, and the stored record has no seed names to tell them apart. Fix: store the counted seed names in the record and match `previous` on them too. — high
- LOW — plugin/lib/fmcodebench.py:92,112 — The `communicate()` stderr is thrown away (`out, _`). If `fm code` crashes with a traceback or has no events, the reason is a bare "verify failed" with no cause. Fix: keep the last stderr line in the reason when `ended` is empty. — high

## lens: intent
- LOW — plugin/lib/fmcodebench.py:156,79 — A worker run skips the danger seed, so its score is out of 4, not the "five seeded tasks" README.md:296 states. Its CLI also runs with the real HOME (:78), so it can write outside the temp dirs, which criterion 3 forbids. The README and CHANGELOG don't say either. Fix: add one sentence to the README and print a "worker runs use your real home" note. — high
- LOW — plugin/lib/fmcodebench.py:198 — `--model X --worker Y` runs the model and silently ignores the worker. Fix: reject the combination with exit 2. — high

## lens: maintainer
- LOW — plugin/tests/test_code_bench.py — Three branches have no test: the `canary touched` reason (:112), a worker skipping the danger seed (:156), and a check that times out. The check-timeout case is where the MEDIUM bug above sits. Fix: add these three cases. — high
- LOW — README.md:296, plugin/lib/fmcode.py:3 — The documented `--json` fields leave out `ts` and `skipped`. README.md:296 doesn't mention `--seed-timeout` or `--max-steps`, and the `fmcode.py` usage docstring doesn't list `bench`. Fix: add them. — medium

## lens: adversary and operator
No other findings. `FOREMAN_INHIBITED` only disables systemd-inhibit (fmserve.py:710), so it does not weaken the guard. The canary and the HOME override for a model run hold. `kill_group` kills the whole process group (fmcore.py:430). Tests are restored before the check. I found no bypass.

## Acceptance criteria
1. Met. Tests cover the good-fake and bad-fake cases (test_code_bench.py:331-352). I did not run them.
2. Met. The check is re-run after `fm code` returns and the tests are restored first (fmcodebench.py:99-100). The bad fake gets "verify failed", and the good fake outscores it.
3. Met for model runs. Each seed gets a temp repo, home and `FOREMAN_HOME`, and the canary is checked. For worker runs the canary seed is skipped and the real HOME is used, which only partly meets it (see LOW above).
4. Mostly met. There is a per-seed timeout and the line carries seed set, model or worker, Foreman version and score. A bad line is skipped on read. A hung seed is reported 'timeout', but a hung check is not (MEDIUM above). The `--json` fields are only partly documented.

## Implicit decisions
- The score excludes skipped seeds from the denominator.
- Defaults are a 600 s seed limit, a 120 s check limit and 40 steps.
- The verify command is split with `shlex` and run without a shell.
- Records are written once per run, at the end.
- Without `--model` or `--worker`, the default model is resolved with `fmmodels.resolve(None)`.
- `previous` means the last run of the same model or worker and seed set.

## Not checked
I did not run the tests. I did not read the `fm code` loop internals (the guard's behaviour on `rm -rf ~`) or the `fmcli` parser beyond the diff. I did not read the CHANGELOG, MASTER or README hunks beyond the diff.

**Noticed:** `fmcode.py` and `fmcodebench.py` both resolve the `models.json` location separately. A shared `models_path` helper might be worth its own task.
