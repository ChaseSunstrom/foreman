## Verdict
**Changes needed.** Two acceptance criteria are not met: no bar check runs at finish, and Foreman's own evidence can still move a bar. I read the code but did not run the tests, because I had no Bash tool.

## lens: intent
- HIGH — plugin/lib/fmoutcomes.py:578 (and plugin/lib/fmcli.py:779-799) — AC2 says the bar check runs at each `fm task finish`, but nothing calls `adjust_bars` or `settle` there. Grep shows their only callers are `cmd_calibration` (lines 576-578). A bar rises only if someone runs `fm calibration`, and the tests only ever invoke that verb. Fix: call `settle` and `adjust_bars` (inside try/except) from the close path next to `record_close`, and add a test through `fm task finish`.
- HIGH — plugin/lib/fmoutcomes.py:503-509 — AC1 says only fm outcomes' re-fixes and reverts may raise a bar, and race results, assumption marks and reversed decisions never do. `adjust_bars` loops over every kind in `table`. Race rows raise the race bar, and assumption, decision, choice and task rows raise the research bar. `test_a_bar_only_rises…` (test_outcomes.py:576) pins a race-only raise. Task and choice rows also score "missed" on a failed first finish (line 373), which is Foreman's own check. Fix: filter the rows passed to `adjust_bars` and the trial Brier to task and choice rows whose verdict came from survival (`o["survival"]`), and make the race bar read a different signal or not move.
- MEDIUM — plugin/lib/fmoutcomes.py:580-586 — AC2 wants "what each bar cost (races and research it triggered)", and `fm calibration` prints no such line. Fix: count race and research events since the last raise, or drop the clause from the AC.
- LOW — nothing reads the bars. Grep finds no consumer of `bars()`, `routed()` or `routes()` outside the report, so the 70 and 55 defaults change no behaviour. Fix: wire a consumer or say so in the docs.

## lens: adversary
- MEDIUM — plugin/lib/fmoutcomes.py:337-356, plugin/lib/fmcli.py:3195 — `fm task set` on a task that has `plan0_at` records bets even after its first finish or its close. Run `fm task set T confidence=95` after a clean finish, or add "(90%)" to an assumption after verifying it, and the hindsight bet is written and scored at once. Fix: skip `record_stated` for bets when the task has a finish event or is done, or mark the row `late`.
- MEDIUM — plugin/lib/fmoutcomes.py:383 — a decision that reverses another is scored against itself. Example: `fm decide "Drop Redis for sessions" --reverses "Redis for sessions" --confidence 80`. Its key contains the reverses words, and the `decision` event has the same-second `ts` as the bet, so `ts >= r.ts` holds and the new bet is "missed" immediately. Fix: skip events whose `data.decision.lower()[:80]` equals the row's key.
- Write-once held on every path I tried. After focus, `fm task set` refuses edit and clear, and `bet()` dedupes on (task, kind, key). Editing the brief text can't change an existing row.

## lens: edge
- MEDIUM — plugin/lib/fmoutcomes.py:509 — one close writes both a task row and a choice row with the same verdict. Each kind has its own 20-row threshold, so about ten closes can raise the research bar twice, 70 to 90, on the same evidence. Fix: dedupe by task, or count one row per task toward the 20.
- MEDIUM — plugin/lib/fmoutcomes.py:531-532 — the raise is written to meta and `decisions.md` under the lock, then `fmtrials.add` runs afterwards. If the add fails (lock timeout 2), the bar has risen with no trial, and `calibration_seen` blocks a retry. Fix: register the trial before the meta write, or record a pending-trial marker.
- LOW — plugin/lib/fmoutcomes.py:310 and 383 — `key` is cut to 80 characters, so a `--reverses` phrase longer than 80 never matches. Two decisions that share a long prefix also collide. Re-stating a decision with a new `--confidence` is silently dropped, because `bet()` returns None and fm still prints "Decision recorded".
- LOW — plugin/lib/fmoutcomes.py:435 — `bars()` clamps a hand-set bar above 90 down to 90, and the next meta write persists that. Never lowering a bar is the invariant, so leave values above 90 alone.

## lens: operator
- MEDIUM — plugin/lib/fmoutcomes.py:342-345 — `record_stated` calls `outcomes(p)`, `_first_finish` (a 50,000-event tail) and `_tree` (a git subprocess) before checking whether the brief states any number. 0 of 2332 briefs set a confidence, so this is almost always wasted work. It runs at every first focus, where `track_line` already ran `outcomes` once, and again on every `fm task set` after focus (fmcli.py:3195). `outcomes()` loads every brief including the archive and runs `git log`. Fix: parse the percentages first and return if there are none, and compute the base rate lazily.
- LOW — plugin/lib/fmoutcomes.py:318-320 — `bet()` reads the whole ledger twice per bet, under the lock. `scored()` is called about three times per `fm calibration` or `fm digest`, each repeating `_first_finish` and `load_briefs`. The file is about 14 lines per task and is never trimmed. Fix: read the ledger once in `record_stated`, and pass `first` and `verdicts` through.
- LOW — plugin/lib/fmcli.py:3972 and plugin/lib/fmlanes.py:462 — `bet()` is unguarded here. A lock timeout raises after the decision or race was already written. Fix: wrap it in try/except.

## lens: maintainer
- LOW — `routed()` (fmoutcomes.py:485) has no caller and is exercised only by tests. Delete it or wire it.
- LOW — the class name `CalibrationLedger` appears in both test_outcomes.py:442 and test_planning.py:125, so `-k CalibrationLedger` is ambiguous across files.

## Acceptance criteria
- **AC1: not met.** Rows, write-once and `fm decide --confidence` work, but Foreman's own signals (race picks, assumption marks, reversed decisions, a failed first finish) can raise bars.
- **AC2: not met.** Buckets, both Briers, "too few", and the rule that bars never lower are present, and digest and cost read the ledger. There is no finish-time check and no per-bar cost line.

## Implicit decisions
- Bar defaults 70 and 55, a gap of 15, a step of 10 and a cap of 90.
- Buckets 0–59, 60–79, 80–94 and 95–100.
- The `_CHOICE_PCT` and `_PCT` regexes parse the stated numbers.
- A decision with no reversal in 30 days counts as "held".
- All non-race kinds feed the research bar.
- Race bets are written only for side A.

## Not checked
I did not run the tests. I also did not check the UI, the docs edits, or `fmcost` beyond the grep.

Noticed: the base rate counts "smoke failed after" as a miss, but the survival score does not, so the Brier comparison is slightly biased.
