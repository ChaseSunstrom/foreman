# Critique — Mission 8, moonshot (gen 4, #8)

Tasks: T-2918 (done; its live run split out to T-2954, captured). Mission: gen-4/mission-moonshot.md.

## Closed vs planned
- Brief 1, part one: the M-02 slice. T-2918 is closed and merged. `sampo moons regen PATH` (regen.py) deletes one
  module in a throwaway worktree. It asks the model for the module back from its intent only: the briefs that name
  it, its map entry, its tests and the names its importers use. It runs the module's own tests and prints each result.
  Review added safeguards the first build lacked: an isolated test environment, a symlink-safe delete, and "a down
  model moves on". A reply that imports outside the original imports, or does not compile, is refused unrun. It
  lands nothing.
- Brief 1, part one, the run: not done. The Mission's whole point was a result: "2 or more modules round-trip" earns
  "Advanced: M-02 slice". T-2918's third criterion was rewritten mid-close to "the slice run is split out", and the
  result file bench/moonshot/m02-slice-result.json reads `"ran": false`. Its note says the GPU and the remote endpoint
  were busy. The Mission file's own rule said the Advanced line is written only when the slice result is filed. So
  there is no Advanced line, and the floor (advance one extreme or massive moon by a stage) is unmet for gen 4.
  `sampo moons status` still shows M-02 at the kill stage and "0 built".
- Brief 1, part two: the ecology moons. Filed. The catalogue went from 58 to 61 of 100 (xhigh 4 to 5, massive 19 to
  21), and the closing criterion, `sampo moons check` after `rate`, was met. I did not re-read the new blocks for
  wildness. The reviewer's wild score on them is the only judge, and I have not read it.
- Closing a task by moving its hard criterion to a new task is legal under the rules. It is also how an outcome
  slides one generation. Here it moved because the endpoint was busy at 08:10 and the 10k funnel was using it.

## Measures (first readings and due dates)
- Slice round-trip count. Planned measure: modules that regrow and pass every original test, on the 27B first and
  Haiku second. First reading: none. 0 of the 20 sampled leaf modules have been run. Due: when T-2954 runs. It is
  captured, not started.
- Catalogue size, which the Mission shares with self-triggering. Before: 58 moons. Today: 61 moons, and the
  candidates store stands at 10,007 (292 survivors in 280 families), closed by T-2865 in this session by hand.
- Kill-tested extreme or massive moons: 1 of 20 (gen-4 opened at 1 of 18). That means the climb the Mission cited
  (M-18, then kills for M-21 to M-28) did not move. This Mission did not claim it would.

## Outside signals
- None from a user. The Mission's premise, that the user would ask for exactly this step, came from the prediction.
  No steer has confirmed or denied it in the days since. It is not scored here.

## What failed
- The headline did not run. The code that could prove M-02 now exists, and no reading says whether a Sampo module
  can be regrown from its briefs. This is the third time a moon advanced as machinery rather than as a result
  (gen-3 had the kill script, gen-4 has the slice runner). Building the runner is easy to close. The run is the
  claim.
- The failure was foreseeable. Grounding noted the 27B closed 1 of 5 seeds on endpoint errors, and still planned the
  run inside the same close as the build. A run that needs the one scarce GPU should have been its own first task,
  ordered before the build that did not need the GPU.
- The ecology moons were filed in the same close with no stated reading of how wild they are. The measure for a moon
  is its wild score, and the critique cannot quote one.

## What the next Seed should change
- Make T-2954 gen-5's first task, and give it a rule: it holds the GPU lock before any other local job starts, and
  the night's $0 jobs yield to it. Then record the true count, with the failures. A result of 0 of 20 is a finding
  about how well briefs pin code. It is not a reason to drop the moon.
- A Mission whose floor is "advance a stage" gets one criterion that reads the stage in `sampo moons status` after
  the close. No split-out may carry that criterion.
- Count the stage movement in the critique from the catalogue, never from the task title.
