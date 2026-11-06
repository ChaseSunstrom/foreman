# Brainstorm — lens: self-modification: a planner whose stated confidence and chosen approach are scored against what happened, so its gates and races retune themselves, measured and reversible

- **Tune from a frozen replay set, not live tasks** — FEATURE — value 5 — effort M — risk low — category: tuning
  Why: assumption: earlier ideas list backtests and holdouts separately; none makes a frozen, versioned set of finished tasks (plan, outcome, reopen cause) the only thing a knob change is judged on, with a held-out slice the tuner never reads.
  Done when: `fm tune propose` refuses any change whose score wasn't computed on the frozen set's held-out slice, and a test shows editing the set invalidates earlier proposals.

- **Make every knob a registry row with owner, metric, counter-metric and revert** — CLEAN — value 4 — effort M — risk low — category: knobs
  Why: pack shows thresholds hard-coded across plan gate (T-2269), race trigger (T-2271), blast Risks (T-2277); "Version every gate threshold" is listed but no registry schema is.
  Done when: `fm knobs` lists each threshold with value, metric, counter-metric, last change and a one-command `fm knobs revert NAME`; a test fails if a gate constant exists outside the registry.

- **Run a candidate gate in shadow for N tasks before it can refuse** — FEATURE — value 4 — effort M — risk low — category: shadow
  Why: T-2285 shows the plan gate misfired on a flag-leading option; a shadow mode would have logged it as "would refuse" before blocking the user.
  Done when: a new knob value logs would-refuse vs actual outcome per task for N tasks, and promotion is refused until the shadow false-refuse rate is under a set bound.

- **Auto-revert on a counter-metric breach** — SAFETY→FIX — value 4 — effort S — risk med — category: guardrails
  Why: assumption: a tuner that only optimises one number will game it; the steers already ban metric-gaming (cold-read rule).
  Done when: a test moves a knob so first-pass rate rises but user plan-edits double, and the next `fm doctor` reverts it and records why.

- **Treat the user's plan edits and steers as the only unforgeable label** — FEATURE — value 5 — effort M — risk med — category: signal
  Why: standing rule asks for signals Foreman didn't author; "What earlier brainstorms missed" lists asks the user had to make, each a labelled miss.
  Done when: every user edit after plan accept is stored as (gate, row, kind) in a file the model can't write, and the tuner's input query reads only that and outcome survival.

- **Give each tuning change a budget and a cooling-off** — SECURITY — value 3 — effort S — risk low — category: safety
  Why: assumption: an unbounded self-tuner can drift the whole ceremony level in a night.
  Done when: no more than K knob changes per week are accepted, a reverted knob can't be retried for D days, and a test shows the K+1th is queued, not applied.

- **Score the chosen approach against its runner-up on close** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: T-2271 races the runner-up only when stuck; no record exists of whether the unchosen option would have won on tasks that closed cleanly.
  Done when: for a sample of closed M tasks a background lane builds the runner-up, and `fm triggers` shows a runner-up-win rate per tier.

- **Show the user one weekly tuning digest with one-word veto** — FEATURE — value 4 — effort S — risk low — category: transparency
  Why: standing rules put the user in charge of steers; a self-changing planner needs a legible, reversible surface.
  Done when: a digest lists each change, its evidence and `veto NAME`; vetoing reverts and adds a tabu entry that blocks that value.

- **Wild: Hold a nightly knob tournament on the repo's own history** — FEATURE — value 4 — effort L — risk med — category: tuning
  Why: wild; replaying finished tasks through two gate settings and keeping the better one gives tuning evidence with zero live risk.
  Done when: a nightly run prints for each knob pair the replay score, and only a pair beating the incumbent on the held-out slice becomes a proposal.

- **Wild: Pin a self-model card the tuner cannot edit** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: wild; a short user-signed file of things that never tune (the guard, the irreversible-door table, the steer checks) keeps self-modification inside a fence.
  Done when: `fm tune` exits non-zero on any proposal touching a card-listed item, and the card's hash is checked by `fm doctor`.

- **Wild: Pit two knob sets against each other on live tasks** — FEATURE — value 3 — effort L — risk high — category: A/B
  Why: wild; alternating S-tier tasks between planner settings yields real outcomes, but only safe on reversible work.
  Done when: tasks tagged S are assigned by hash to A or B, the split is recorded, and a report gives per-arm first-pass and reopen rates with intervals.

- **Detect Goodhart: flag a knob whose metric improves while the outcome survival falls** — FEATURE — value 4 — effort M — risk low — category: integrity
  Why: assumption: the tuner's metric is Foreman-authored, so it needs an independent check; the standing rule demands outcomes Foreman didn't author.
  Done when: a synthetic fixture where plan-gate pass rate rises and 7-day revert rate rises too makes `fm doctor` print a Goodhart warning naming the knob.

- **Explain a retune as a plan the user could have written** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: users accept changes phrased as their own rules ("you edited Risks 6 times; Risks is now required at M").
  Done when: each proposal text cites at least three of the user's own edits or steers by id.

Next question: Which outcome signal does the tuner read that the planner itself can influence, and what separates the two?
Next question: What is the smallest number of closed tasks per tier at which a knob change is better than noise?
