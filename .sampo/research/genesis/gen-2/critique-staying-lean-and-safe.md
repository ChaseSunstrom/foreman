# Critique — Mission 3, staying lean and safe (gen 2, #12)

Tasks: T-2532 (done), T-2536 (done), T-2534 (dropped: an exact duplicate), T-2533 and T-2535 (carried: deferred to
2026-12-01, each with a revive condition). Mission: gen-2/mission-staying-lean-and-safe.md.

## Closed vs planned
- Two of five planned briefs are built. Hooks survive a self-edit (T-2532): when plugin/lib fails to import, every hook
  event now runs from the committed library, as the guard's PreToolUse already did, and hooks.log names the event. A
  test breaks fmhooks.py in a committed copy and checks that SessionStart still prints its context. Subtract by
  evidence (T-2536): `fm bench duel --ablate` files one cleanup candidate per hook feature whose off arm changed no pass
  at no more cost. The candidate names the run and says a cut needs every exam kind and the long-horizon tier first.
- Dropped at grounding: brief 3 (T-2534). The exam's plain arm is already Claude with only the guard (FOREMAN_QUIET=1
  plus the bare guard settings, T-0963), so a guard-only arm would duplicate it.
- Carried, deferred to 2026-12-01: brief 2 (T-2533, per-call hook notes in the ratchet) waits because hook notes are
  0.8% of what enters the context and swing with session length, so a 2% band would trip on noise. It revives past 3%,
  or once a per-call rate holds within 10% for a week. Brief 4 (T-2535, which commit made it heavier) waits because the
  ratchet has never tripped at a ship. It revives at the first trip whose cause isn't obvious.
- Found and fixed beside the Mission, in the same lean-and-safe area: the usage-burn advice named a no-op fix against
  the user's own 1M compact window, and the state-size row named fm tidy for exam runs it never prunes (T-2539). The
  Genesis build gate stalled on a dated deferral, now carried and named (T-2541).

## Outside signals
- CI on main: green on 9f28863 (T-2430 and T-2526) and 28d5de3 (T-2524, T-2527, T-2529). Ship bets have held 11 in a
  row. cef5811 (T-2532) was still being watched when this was written.
- fm ship's own test, on the remembered uv python3.12, caught what the local gate on python3 3.14 passed: the exam's
  package kind assumed setuptools (T-2529). One case in 22 ship baselines. Ship's affected-first run stopped it in
  minutes, so no second interpreter was added to fm check (a recorded decision).
- No exam ran: by rule 6 the session arms wait for the end of the run. T-2536 has nothing to act on until the first
  --ablate run.

## What failed
- The Mission was filed before its briefs were grounded. Three of five turned out to be built, or to have no failure
  behind them, and were found only at planning. The file was revised three times through the cold reader. The next
  Mission grounds each brief before filing: is it built, and has the failure happened?
- #12's tier 3-4 share is 25% (one of four built or carried briefs), under gen-0 §3's 70%. The remaining tier 3-4 work
  is in the guard's parser, which the standing safety rules hold for the user (T-1937, T-1928, T-2261, T-2068).
- Subagents were paused by the budget's pace rule throughout, so all grounding ran in the main thread.

## What the next Seed should change
- Ground every brief against the code and the ledger before `fm genesis put` of a Mission. Count a brief whose problem
  has never happened as a deferral with a revive condition, not as work.
- #12 needs its first measured price on injected context: run `fm bench duel --ablate all` in the end-of-run exam, so
  T-2536's candidates and the plain arm's delta decide what Foreman's context buys.
