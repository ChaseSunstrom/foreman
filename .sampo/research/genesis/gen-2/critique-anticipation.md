# Critique — Mission 6, anticipation (gen 2, #3)

Tasks: T-2554 (done). Mission: gen-2/mission-anticipation.md.

## Closed vs planned
- The one planned brief is closed. The user model reads the user's own asks (T-2554): fmforesight._requests leaves out
  briefs any Genesis Mission's Task paragraph names, and captures dropped as a mistake. fm intake --source genesis
  files the tower's briefs as its own, and the Genesis step's intake line uses it. fmexam.replay_forecast scores the
  cleaned and the raw history on the same held-out asks, side by side.
- Grounded before filing, and not rebuilt: the prediction book and its muting (T-2406), the lane plan for the top
  prediction (T-2407), the foresight flags (CI red, setup change, dead timers).

## Outside signals
- The walk-forward replay on this project's real history, which Foreman didn't choose: on the same 331 held-out user
  asks, type hits were 201 with the cleaned history and 201 with the raw one (the baseline 196 for both), and path
  overlap was 0.118 against 0.113 (baselines 0.116 and 0.113). The bar was "not lower", and it was met.
- CI on main: green on 5e5889a (T-2542, T-2543). Ship bets have held 14 in a row.

## What failed
- The first replay compared the two streams on different held-out sets (331 asks against 388), which made the raw
  stream look 10 points better. Its Mission tower briefs come in easy-to-predict runs of one type. The Mission had
  said "on the same requests". The replay was rebuilt to score both histories on the user's own held-out asks before
  any verdict was taken.
- The gain is small: no type hits gained, a 0.005 path-overlap gain. The cleanup's value is mostly that the model is
  honest about whose habits it learns, not that it predicts much better yet.

## What the next Seed should change
- A backtest compares two variants on the same evaluation set, fixed before either is run. Write the set into the
  Mission's Exam section, as this one did, and check the code against it before reading any number.
- The tower's own work never enters a user model. Any new reader of "the user's requests" uses fmforesight._requests,
  not its own filter.
