**Verdict: approve with nits.** Both acceptance criteria are met and the stubbed-replay tests cover them. One MEDIUM finding is a silent way to pass the gate. I read the code but did not run the tests.

## lens: adversary
- MEDIUM — plugin/lib/fmreplay.py:357,503 — The gate trusts a green `guard_corpus` ledger record, and the record stores neither the corpus path nor any minimum size. `cases_path()` honours `FOREMAN_GUARD_CASES`. An unattended agent can run `printf '{"id":"a","cmd":"ls","cwd":"","should":"allow","why":"t"}\n' > /tmp/c; FOREMAN_GUARD_CASES=/tmp/c fm replay --cases`. That records `cases=1, drifted=0, broken=0`, `safety_gate` then returns None, and nothing is logged as a waiver. `test_the_replay_records_its_result` (test_safety_gate.py:401-409) shows exactly this and asserts the gate passes. Fix: add the corpus path (or the case count) to the record and have `safety_gate` count only a replay of the committed `plugin/tests/fixtures/guard_cases.jsonl`. Alternatively, skip `record()` when the env override is set. — confidence high
- LOW — plugin/lib/fmcode.py:1628-1629, plugin/lib/fmreplay.py:493 — An unattended agent can `export FOREMAN_CODE_ATTENDED=1` or pass `--stale-ok x`, so the gate is a logged speed bump rather than a barrier. Both routes leave a ledger event (`safety_warned` or `safety_waiver`), and the new `safety_warned` event closes the silent route. `--stale-ok` is also what the acceptance criteria asked for. Fix if you want a hard barrier: have `fm doctor` or `fm next` surface recent `safety_waiver` and `safety_warned` events. — confidence medium
- LOW — plugin/lib/fmreplay.py:485-487 — `age_days` goes negative for a future-dated or clock-skewed `guard_corpus` event, and a negative age passes the gate. Fix: treat `age < 0` as stale or invalid. — confidence low

## lens: edge
- LOW — plugin/lib/fmrelease.py:317 — `--stale-ok` without `--push` is accepted and ignored, so no waiver is logged. Fix: say so, or reject the flag without `--push`. — confidence high
- LOW — plugin/lib/fmcodebench.py:88 — Bench seeds waive the gate with a hardcoded reason. The waiver goes into a throwaway Foreman home, so it never appears on the real ledger. `fm code bench` also returns at fmcode.py:1599, before the gate, so bench is effectively ungated. Probably intended, so note it in the changelog. — confidence medium

## lens: maintainer
- LOW — plugin/lib/fmcode.py:1631 — The code rewrites `"fm code refuses: "` to `"refused: "` by string replace. This depends on the message format in `enforce`, and the blank-waiver error passes through unrewritten. Fix: raise a `CodeError` from `enforce`'s caller using a structured reason. — confidence high
- LOW — plugin/tests/test_safety_gate.py — No test covers `--resume` or `--task` being gated, a blank `--stale-ok` on release, or the tty-attended branch (fmcode.py:1629). — confidence high

## lens: intent / operator
No findings.
- Docs: the changelog is accurate and `guard_corpus`, `safety_warned` and `safety_waiver` are new ledger kinds.
- Refresh: `fm night` refreshes only Foreman's own repo (fmnight.py:58). Other installs refuse every 7 days until someone runs `fm replay --cases`, and the message names that command.

## Acceptance criteria
- Red or 8-day-old replay refuses both verbs, naming the check, date and refresh command; a fresh green replay lets both run: **met**. See fmreplay.py:455-496, `SafetyGate` and `ReleaseGate`.
- `--stale-ok REASON` runs and logs the waiver: **met**. See fmreplay.py:489-492 and `test_waiver_is_logged`.
- Follow-up: **met**. fmcodetui.py:1677 sets `FOREMAN_CODE_ATTENDED=1` and fmreplay.py:493-495 logs `safety_warned`. Both are tested (`test_the_apps_runs_are_attended` and `test_an_attended_run_only_warns`).

## Implicit decisions
- 7-day staleness limit and a 90-day ledger window.
- Newest record wins, and a red one masks an older green one.
- `fm code --dry-plan` is ungated, but `--resume` and `--task` are gated.
- A tty on stdin and stdout counts as attended.
- `fm release --push` has no attended mode.
- The replay verifies only the guard corpus, not the canary.
- The record goes to Foreman's project, falling back to the cwd project.

## Not checked
I did not run the test suite. I did not check the rendering of the TUI's note event or the nested-worker environment inheritance of `FOREMAN_CODE_ATTENDED`.

**Noticed:** the `FOREMAN_GUARD_CASES` override lets any replay be recorded as green (the MEDIUM finding above). `fm code bench` is not covered by the new gate.
