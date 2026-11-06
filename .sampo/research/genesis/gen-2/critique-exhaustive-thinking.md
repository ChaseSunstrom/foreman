# Critique — Mission 5, exhaustive thinking (gen 2, #2)

Tasks: T-2546 (done, its nudge not shipped by its own backtest), T-2547 (done). T-2544 and T-2545 carried (deferred to
2026-12-01, each with a revival condition). Mission: gen-2/mission-exhaustive-thinking.md.

## Closed vs planned
- Grounded Missions (T-2547): fm genesis put refuses a Mission file whose intake block has more briefs than grounding
  lines, each naming the code it rests on. It runs before the cold read, so an ungrounded Mission costs no model call.
- Already built, at birth (T-2546): the matcher was built and backtested on real history before anything printed: 46
  tasks dropped as already built against 400 done as new work, each matched only against MASTER.md clauses of earlier
  tasks. No threshold met the bar (a third of the built drops at under 1 in 10 of new work). The best setting caught
  4 of 46 while flagging 31 of 400. By the plan's rule, fm capture prints nothing new. The matcher and fm recall
  --backtest-built stay as the yardstick a better matcher has to beat (research covered-backtest).
- Carried: T-2544 (model-substitution checks on deliberation children) revives at the first answer recorded on a
  model other than the one asked. T-2545 (voiding races scored on a flaky verify) revives once races run here.

## Outside signals
- The backtest's outcome labels came from the record, not from this Mission: which tasks were later dropped as built
  and which were done as new work. It said no, and the brief honoured that.
- CI on main: green on a0ba95a (T-2536 to T-2541). Ship bets have held 13 in a row.

## What failed
- The Mission's main bet failed: word overlap between a request's title and MASTER.md's long clauses is too blunt to
  spot work that already exists. Built-drop titles are often review notes worded unlike the clause they duplicate.
- Two helper names in this Mission's code were silently shadowed by later definitions of the same name in their
  modules (_grounded in fmgenesis, _TID in fmrecall). Tests caught both before landing.

## What the next Seed should change
- A heuristic that gates or nudges ships only behind a backtest on real outcomes, with its bar stated before the run.
  T-2546 is the pattern: the bar was in the Mission, and the result decided.
- Try the model layer's embeddings against covered-backtest's rows. That is the first use of the model layer with an
  exam already waiting for it.
