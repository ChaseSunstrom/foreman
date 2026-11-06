# Mission 2 — calibrated judgment (gen 3, #8)

Task: T-2610 (brief 1), T-2611 (brief 2).

Parent: gen-3/seed.md row 2 → gen-0.md #8: "Calibrated judgment. It knows what it doesn't know: it states
confidence, researches when unsure, and stops for me only when something is irreversible and ambiguous. Everything
else it decides and records." gen-0's goal, MUSTs and NEVERs are quoted in the seed and apply here unchanged.

## Capability
Confidence read from a fair ruler. Grounded before filing: stated bets and their ledger (T-2338), ship bets settled by
CI (T-2496), the base-rate note on a plan's Choice (T-2497), the interim read (T-2498), settling with no session and
the trails clause (T-2499, T-2520), the harness on each bet (T-2500), ship bets in the buckets (T-2519) and the
survival rate over finished windows only (T-2584) are built.
What it lacks: every other read of the record is censored. A miss counts the day it lands; a hold counts only once its
30-day window ends. `fm outcomes` today: "Survival (30 days): of 1720 closes, 111 finished the window: 5 lost (5%)",
yet the track record shown at every `fm focus` reads "FEATURE M: … 21 of 43 held" (49%), and the ledger reads
"choice 80–94%: n 4, held 0 (0%), gap +84" from four bets whose windows can't close before 2026-11-30. The research
bar check reads the same rows. A Foreman that learns from this ruler learns it is far worse than it is.
The second lack: ship bets are under-confident ("ship 80–94%: n 21, held 21 (100%), gap -15"; the digest's trails
line names ship), but the record never shows where the number is typed: every ship this generation stated 85 by
habit.

## Grounding
- Brief 1: fmoutcomes.track (`r["settled"] += o["fate"] != "held" or bool(o.get("window_done"))`) counts a miss at
  once and a hold after the window; fmoutcomes.tables, brier, _trails and bar_rows take every scored task and choice
  row, open window or not; fmoutcomes.base_rate pools every close, so an open-window close counts as held. Only
  survival_lines (T-2584) counts finished windows.
- Brief 2: fmoutcomes.ship_bet already stores each ship bet's base (the held share of earlier settled ship bets);
  fmoutcomes.base_note is the plan-time pattern (a note when the stated number sits 20+ points from the record);
  `fm ship --chance` prints nothing about the record.

## Gaps this Mission targets (coverage: #8)
- verify × CLI and judge × ledger: every calibration read compares like with like, and the stated number meets its
  record where it is typed.
- Not in this Mission: a harness marker for codex, gemini and opencode sessions (gen-2's critique). Of 119 bets, 42
  read claude-code and 77 read unknown, and all 77 predate the field (T-2500); none came from another agent, so it
  is carried until one of them books a bet. Also not here: a new exam kind (the ledger itself is the measure; see
  Exam).

## Ideas (grounded; no new brainstorm this Mission)
The area's 40 open cells already hold brainstormed ideas, and this read of the live ledger found a measured defect
that outranks them (recorded with fm decide --kind costly).
### One window for every read
A close, a task bet or a choice bet counts only once its 30-day window has finished: the track record, the ledger's
buckets, both Briers, the trails clause, the bar check and the base rate. A miss inside an open window is shown as
"N lost in open windows, not scored yet". Prior art: survival analysis's fixed follow-up window; clinical trials
read an outcome only for patients followed the full period. Better by: one rule, applied where T-2584 applied it to
the survival line, now everywhere the record is read.
### The record where the number is typed
`fm ship --chance N` prints one line when N sits 15+ points from the held share of 20+ settled ship bets ("ship bets
here: 21 of 21 held; 85 sits 15 under the record"). Prior art: the plan's base-rate note (T-2497). Better by: the
outside signal reaches the next bet, not only the weekly digest.

## Approaches
1. One helper (`ripe(rows, outs)`) that keeps a task or choice row only when its task's window_done, used by
   ledger_data, maintain's bar check and the trails clause; track and base_rate filter on window_done directly; an
   "open windows" line lists early misses. Likely outcome: FEATURE M reads near 95% held, the choice bucket reads
   "too few", and the bar check waits for real rows. Fails if: too few finished windows make every table empty (the
   "too few" line already handles it, and finished windows grow by about 50 a day).
2. use what exists: keep the reads, and print the interim read (T-2498) beside them as the honest number. Fails if:
   the biased numbers still drive the bar check and the focus line.
3. do less: stop settling task and choice bets before their window ends. Fails if: a revert inside the window is
   evidence that should be recorded at once; grade rows are write-once, so the existing early grades stay.

Choice: 1 (85%): one filter at read time, so grade rows stay write-once and nothing already written moves.

## Exam
#8's exam kind stays clean (a clean repo must be left alone). This Mission adds no exam kind; the exam harness
cannot produce a month of closes, so the measure is the live ledger, read before and after: the track record's
FEATURE M row (21 of 43 held, today), the choice bucket (n 4, gap +84, today) and whether the research bar check sees
open-window rows. Unit checks: a close with a miss inside an open window is left out of the track record, the
buckets, the Briers, the bar check and the base rate, and is named in the open-windows line; a close whose window
finished counts both ways; a ship chance 15+ points from 20+ settled ship bets prints the note, and one within 15 or
with under 20 prints none.

## Long-horizon goal (end of run)
The track record at `fm focus` and the ledger's buckets read within 5 points of the finished-window survival rate.

## Lean
One read-time filter and one line at ship. No new verb, no hook cost, no rewritten rows.

## Tier share
Brief 1 is tier 3 (judgment from a fair ruler); brief 2 is tier 2.

## Done when
The track record, the ledger's buckets, both Briers, the trails clause, the bar check and the base rate count a close
or a task or choice bet only once its window finished, with early misses named apart; `fm ship --chance` names the
ship record when the chance sits 15+ points from it; the unit checks above pass; the live ledger read is recorded
before and after in the critique; MASTER.md (fmoutcomes), CHANGELOG and the planning reference's calibration section (intake/references/planning.md) say
it.
No site page: the Judgment page reads ledger_data, so it shows the fixed numbers with no change of its own.

## Briefs (fm intake)
```
FIX: calibration reads compare like with like: fmoutcomes.track, tables, brier, the trails clause, the bar check (bar_rows) and base_rate count a close or a task or choice bet only once its 30-day window finished (window_done), as survival_lines does since T-2584; misses inside open windows are named apart ("N lost in open windows, not scored yet"); MASTER, CHANGELOG and intake/references/planning.md say it
FEATURE: fm ship --chance N names the ship record in one line when N sits 15+ points from the held share of 20+ settled ship bets, like the plan's base-rate note (T-2497); CHANGELOG and release/ship-to-main.md say it
```
