**Verdict:** changes needed. There are no blockers. The doctor behaviour doesn't match what the user asked for, and one enforcement hole could leave a steer rule unchecked.

## lens: intent
- MEDIUM — plugin/lib/fmdoctor.py:416-139 (`check_steers`) — The user asked that `fm doctor` in a tower project "fails on a standing rule … with no check or whose check fails". It only WARNs, and it runs no checks unless `--full`, so a failing check never shows in a plain `fm doctor`. The CHANGELOG says "warns", but the user never agreed to that weaker behaviour. — Mark an unbuilt rule explicitly, for example `[check: pending T-2158]`, so the doctor can FAIL on a rule with no check and no pending marker. Otherwise get the user's yes to WARN — confidence 80%
- MEDIUM — plugin/lib/fmcore.py:3225 (`STEER`) — Enforcement is keyed on the free-text `--cites` wording `user steer` or `the user's steer`. `--cites "steer 2026-10-30 #2"`, `"user's message"` or `"user  steer"` (two spaces) make `steer_checks` return `[]`, so the rule escapes the check. Repro: `fm decide "r" --cites "user message"`, then `steer_checks(p)` returns nothing. — Have `fm decide` warn when `--cites` mentions user/steer/message but doesn't match `STEER`. Better, add an explicit `--steer` flag — 70%

## lens: adversary
- MEDIUM — plugin/lib/fmcore.py:3217-3222, 3253 — Any later row can silence an unchecked steer rule. Repro: `fm decide "rule one: no check" --cites "user steer"`, then `fm decide "drop" --reverses "rule one"`. The first row is now settled and `steer_checks` returns `[]`. A short `--revisited rule` (4 or more characters, whole word) settles every earlier steer row containing that word. The session being policed writes both rows. — A `--reverses` or `--revisited` that settles a steer-cited row must itself cite a user steer, or sweep must list it as "settled by non-steer row" — 75%
- LOW — plugin/lib/fmcore.py:3110 — `subprocess.run(..., timeout=900)` kills only the direct child. After a timeout, `run.py`'s class workers are orphaned. — Use `start_new_session=True` and `killpg` on timeout — 60%
- LOW — The allowlist runs `fm genesis check` and `fm exam scorecard`, which are not tied to the rule they back. `--check "fm genesis check"` satisfies any steer rule. This is by design, but note it as a ceiling in a `ponytail:` comment — 60%

## lens: edge
- LOW — plugin/lib/fmcore.py:3110-3114 — A failing check reports only `exit N`; stderr is dropped. The sweep or doctor row can't say why it failed. — Append `fit(plain(stderr.splitlines()[-1]), 80)` — 70%

## lens: operator
- MEDIUM — plugin/lib/fmcore.py:3246 and plugin/lib/fmgenesis.py:1524 — Each sweep, and each `doctor --full`, runs about 7 distinct test sets one after another. They include `test_ship.Ship`, `test_setup.InstallScript` and `test_genesis.GenesisLive`, which build git repos. The worst case is 7 × 900 s with no output. No wall-clock measurement is recorded. — Record the time of `fm doctor --full`. Consider a cache keyed on tree hash, or a lower timeout — 60%
- Consequence: the Foreman tower's sweep stays red, and so does `step()`, until T-2158, T-2160 and T-2161 land. This matches the user's request.

## lens: maintainer
- LOW — plugin/tests/test_judgment.py — Nothing covers the `argv[0] == "fm"` branch (the `bin/fm` path), the `OSError` or `TimeoutExpired` branch, or the dedupe in `ran`. Deleting the `bin/fm` mapping would pass every test. — Add a test that a `fm genesis check` rule runs and reports an exit code — 80%
- LOW — plugin/lib/fmcore.py:3252 and plugin/lib/fmdoctor.py:133 — `import subprocess` and `import fmgenesis` sit inside function bodies with no stated reason. Earlier reviews flagged this pattern. — Add a one-line comment, for example "keeps the guard path light" — 50%

## Acceptance criteria
1. Met. `check_argv` uses shlex with no shell, the allowlist is enforced at decide time, and `test_judgment.SteerChecks` covers off-list commands and a hand-forged row.
2. Partly met. Sweep is met (`GenesisSweep` test). Doctor only warns (see the intent finding).
3. Not verifiable from the code. `decisions.md` has 9 `[check:]` tags (lines 261-269), consistent with the claim. The run output of `fm doctor --full -v` wasn't seen.

## Implicit decisions
- Doctor WARNs rather than FAILs.
- Steer rules are recognised by the wording of `--cites`.
- Checks run serially, with a 900 s timeout each, and results are deduplicated per command string.
- Dotted test ids such as `test_x.Class.method` are allowed.
- `--check` on a rule that isn't steer-cited is stored but never run.
- Settling reuses the existing `--revisited` and `--reverses` word match.

## Not checked
- I did not run the tests or `fm doctor --full`.
- I did not read the MASTER.md diff, which was left out of the diff file.
- I did not check whether the genesis SKILL.md change needs a matching README edit.

**Noticed:** none
