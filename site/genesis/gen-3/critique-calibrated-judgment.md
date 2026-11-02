# Critique — Mission 2, calibrated judgment (gen 3, #8)

Tasks: T-2610 (done), T-2611 (done). Mission: gen-3/mission-calibrated-judgment.md.

## Closed vs planned
- Both planned briefs are closed. One window for every read (T-2610): scored() holds a task or choice bet's grade back
  as `early` while its task's 30-day window is open, so the buckets, both Briers, routes, the trails clause, the bar
  check and the trial grader skip it with no change of their own; track and base_rate gate on window_done. Grade rows
  are still written at once.
- The record where the number is typed (T-2611): `fm ship --chance N` prints one line after the bet when N sits 15+
  points from the held share of 20+ settled ship bets.
- Re-scoped on the way, both inside T-2610: the interim read had the mirror bias (it dropped early losses, so "held
  so far" could only read high) and now counts them as not held so far; a Brier trial on the research bar, due 30
  days after the move, would have found no settled bets and proposed a revert, so it now waits until its due date
  plus 30 days.

## Outside signals
- The live ledger, before and after T-2610: the track record's FEATURE M row went from "21 of 43 held" to "21 of 22
  held"; FIX M from "5 of 12" to "5 of 6"; the choice bucket's "n 4, held 0 (0%), gap +84" became "5 task or choice
  bet(s) missed inside a 30-day window still open: scored when it ends". The research bar stayed at 70 throughout.
- Ship bets: 23 scored, all held, at stated 75–85% ("ship 80–94%: n 22, held 22 (100%), gap -15"). T-2611's line
  would have fired on every ship this generation. Its effect on the next stated numbers can only be read on the ships
  after it.
- CI passed on the generation's ship (1d5ea2b); the full gate passed on both tasks (5704 and 5708 tests).

## What failed
- The Mission's grounding missed the interim read and the trial grader, both readers of the same rows. The review
  pass found the trial grader; the interim read was found while tracing scored()'s callers. A Mission that changes a
  shared read should list every caller of that read in its Grounding.
- The plan had no brainstorm: the area's open cells already held ideas, and the measured defect outranked them
  (recorded with fm decide --kind costly). Nothing was lost on this Mission, but the open cells were left unread.
- Two tests encoded the biased behavior (the digest's "1 of 20 scored" and a trial test that passed only when seeded
  rows fell in the same second as the trial). The first full gate caught both.

## What the next Seed should change
- When a Mission changes a shared read, its Grounding names every caller of that read, found with grep, before
  filing.
- A time-windowed signal has one rule: a reading counts only once its window has finished. A new read of outcomes is
  tested with a close still inside its window.
