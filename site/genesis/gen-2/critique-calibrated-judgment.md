# Critique — Mission 2, calibrated judgment (gen 2, #8)

Tasks: T-2496, T-2497, T-2498, T-2499, T-2500 (all done). Mission: gen-2/mission-calibrated-judgment.md.

## Closed vs planned
- All five planned briefs are closed. Ship bets (T-2496): `fm ship --chance N` books a bet that CI's blocking jobs
  pass, and `fm ci-watch` settles it. The base-rate note (T-2497): a Choice 20+ points from its type and tier's base
  rate is named at `fm task set`, `fm focus` and `fm next`. The interim read (T-2498): bets on tasks closed 7+ days
  ago, "held so far", never scored, with a reliability chart on the Judgment page. Settling with no session (T-2499):
  the night tick runs the ledger's maintenance, and `fm digest` names the kind whose Brier trails its base rate. Each
  bet carries its harness (T-2500): `fm outcomes --judgment --by harness`.
- Re-scoped on the way: T-2498 reads its reliability bins from the existing kinds table instead of adding a duplicate
  key. T-2500 adopted the rival read's `--by harness` wording and rejected a query-time join to sessions.

## Outside signals
- Ship bets are the first bets scored by a signal Foreman didn't author, within hours. Four were booked this
  generation: 85% on 0a89e375, 75% on fcf9848c, 85% on ff9d1be6 and 85% on 6a2e8fc7. CI's blocking jobs passed on
  all four (4 ci_verdict events), so 4 of 4 held at stated 75–85%. That leans under-confident, like T-2338's 75%
  against a 96% base rate. Four is far too few to say so.
- The ledger holds 77 bets, 5 scored, 72 pending. The interim read is empty (no task with a pending bet closed 7+
  days ago yet: bets began 2026-10-31). The trails clause needs 20 scored, so it says nothing yet.
- `--by harness` reads all 77 as unknown: every row predates the field.
- The night tick runs hourly (systemd timer, "0 order(s) fired, 0 captured" at 18:00 CST). It logs a night_tick
  event only when something happened, so how often it settled bets can't be read from the ledger.

## What failed
- The scored ship bets don't show where a user looks. KINDS has no "ship", so `--judgment`'s bucket table skips the 4
  settled ship bets while counting them in "scored 5" (filed as T-2519).
- Harness coverage stops at fm code, the exam and Claude Code. A codex, gemini or opencode session's bets read
  unknown: their hook environment doesn't reach the shell that runs `fm focus`.
- The tick's maintenance leaves no trace of what it settled. A night with due bets and a night with none look alike
  in the ledger.

## What the next Seed should change
- Show ship bets in the buckets (T-2519), and keep booking `--chance` on every ship. That's the only fast outside
  signal, and 20 scored ship bets is the first point a ship Brier means anything.
- Have the tick log what maintenance settled (n outcome rows written), so "bets settle with no session" is measured
  instead of assumed.
- Find a marker for the other agents' sessions, or record the harness at the hook that sees the session start, before
  their bets accumulate as unknown.
