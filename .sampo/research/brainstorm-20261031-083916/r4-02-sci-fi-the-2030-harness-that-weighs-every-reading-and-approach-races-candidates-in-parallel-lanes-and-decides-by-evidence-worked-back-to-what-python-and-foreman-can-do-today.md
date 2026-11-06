# Brainstorm — lens: sci-fi: the 2030 harness that weighs every reading and approach, races candidates in parallel lanes and decides by evidence, worked back to what Python and Foreman can do today

- **Differential-fuzz the finalists** — FEATURE — value 4 — effort M — risk med — category: race
  Why: assumption: when two lanes both pass the tests, the existing ideas (cross-examination, mutation grading) still leave the choice resting on the tests the lanes wrote themselves. A stdlib random-input driver can run both candidates on the same generated inputs, and each input where they differ becomes a new test or a question for the user.
  Done when: given two fixture candidates that agree on the tests but differ on one input, `fm lane race` prints that input and refuses to pick silently.

- **Pick by minimax regret across readings** — FEATURE — value 4 — effort M — risk low — category: judgment
  Why: the request asks for readings and approaches to be weighed. Today the plan gate checks that the readings exist. Nothing scores each finalist against every reading, so the winner is the one that is least wrong under the worst reading, not the one that fits the first reading best.
  Done when: a fixture task with two readings produces a readings × finalists table, and the chosen row is the one with the lowest worst-case miss.

- **Seed lanes with structural constraints** — FEATURE — value 3 — effort S — risk low — category: race
  Why: assumption: lanes started from the same prompt converge on near-identical diffs. Handing each lane a different constraint ("smallest diff", "no new file", "reuse an existing helper", "no new dependency") forces real alternatives and gives "use what exists" and "do less" a lane each.
  Done when: `fm lane race` on a fixture produces lanes whose diffs differ in files touched, and the brief for each states its constraint.

- **Choose the next experiment by information gain** — FEATURE — value 4 — effort M — risk med — category: stuck ladder
  Why: T-2271's ladder races the runner-up and then falls back to a hypothesis table. The table could hold a prior per hypothesis, update it after each run, and propose the experiment expected to split the remaining mass most evenly.
  Done when: a fixture with 3 hypotheses and a planted cause is solved in fewer experiments than listing them in written order.

- **Run lanes on diff-reachable tests only** — PERFORMANCE — value 4 — effort M — risk med — category: lane cost
  Why: parallel racing multiplies suite time. Selecting tests by import and co-change reachability from each lane's diff (`fm graph blast` already holds the graph) cuts that cost, and the full suite runs once at the winner.
  Done when: a 3-lane race on a fixture runs fewer tests than 3 full suites, and a deliberately missed coupling is caught by the winner's full run.

- **Order the verify ladder by failures per second** — PERFORMANCE — value 3 — effort M — risk low — category: gates
  Why: `fm check` and the gates run in a fixed order. History in the ledger can rank checks by how often each fails divided by its runtime, so a bad lane dies on its first cheap, likely failure.
  Done when: a replay of 20 recorded red runs reaches the first failure faster than the fixed order.

- **Report how fragile the pick is** — FEATURE — value 3 — effort S — risk low — category: judgment
  Why: assumption: the chosen race winner is shown as a verdict with no sense of margin. Re-scoring under ±25% on each rubric weight and printing "flips if cost weight doubles" tells the user whether the evidence was decisive.
  Done when: a close-margin fixture prints a flip condition, and a clear-margin one prints "stable under all perturbations".

- **Stop a deliberation when the lead has stopped moving** — FEATURE — value 3 — effort S — risk low — category: depth control
  Why: depth should scale with risk (S tasks shouldn't pay L costs). A rule of "leader unchanged for k rounds, or the budget for the tier is spent" makes that automatic and logs which one ended the race.
  Done when: a fixture race ends early under the stable-lead rule and records the reason.

- **Stop benchmark races with a sequential test** — PERFORMANCE — value 2 — effort S — risk low — category: perf proof
  Why: T-2288's `--bench` timing uses medians over a fixed run count. A sequential probability ratio test over interleaved runs stops as soon as the difference is real, or declares a tie.
  Done when: a fixture with a planted 30% speedup stops in fewer runs than the fixed count, and an identical pair ends as "tie".

- **Wild: Propagate confidence through a claim graph** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: wild. Assumptions, readings, research notes and criteria become nodes. When a leaf is falsified, by a failed probe or a changed file, every dependent claim's stated confidence drops and the receipt names the chain. `fm graph` and the confidence ledger already exist to host it.
  Done when: falsifying one assumption in a fixture lowers the confidence of two dependent criteria and the close receipt lists the chain.

- **Wild: Re-run the winner in a perturbed mirror universe** — FEATURE — value 3 — effort M — risk med — category: robustness
  Why: wild. Before merge, the winning diff is re-verified in a throwaway copy with one thing shifted (another Python minor, shuffled test order, a different `PYTHONHASHSEED`, a 3-hour clock skew). A winner that only holds in one universe is marked fragile.
  Done when: a fixture winner that depends on dict order fails the mirror run and is flagged before merge.

- **Wild: Draw the deliberation as a funnel** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. Readings → approaches → lanes → winner is drawn as a narrowing funnel in the web UI. Each cut shows the one piece of evidence that ended that branch, and the user can click a cut to ask "why not this one?".
  Done when: the web UI renders a finished race with each eliminated branch labelled by its killing evidence, and a no-race task shows a single-stage funnel with an honest empty state.

- **Wild: Hold the verdict until the finalists vote blind** — FEATURE — value 3 — effort M — risk med — category: judgment
  Why: wild. Each finalist lane, after the race, is shown all diffs with the authors scrubbed and ranks them. A winner that its own author ranks first and no other lane ranks above third is flagged as self-favoured.
  Done when: a fixture where the author-favoured diff loses the blind vote prints a self-favour warning.

Answer to an earlier question: the race winner is the clearest writer-and-judge pair with no user-owned check, because the lane that wrote a candidate usually wrote the tests it was judged on; the differential-fuzz and blind-vote ideas above address that.

Next question: which wrong picks in the finished-task history would a minimax-regret or blind-vote rule have caught, and is that history big enough to tell?
Next question: what is the smallest race cost (tokens, minutes) at which the user would accept evidence-picked designs over first-instinct ones, and does the ledger show it?
