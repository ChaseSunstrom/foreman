# Brainstorm — lens: self-modification: a planner whose stated confidence and chosen approach are scored against what happened, so its gates and races retune themselves, measured and reversible

- **Write a prediction row at plan accept, score it at close** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: T-2290 already predicts minutes/attempts at focus; the plan gate's confidence, chosen approach and "options" have no scored counterpart. Earlier ideas ask for a ledger but none ties a single record (confidence, approach, race trigger, predicted tier) to the same task's close.
  Done when: closing a task appends one JSON row with predicted vs actual (tier, attempts, reopen, race winner) and `fm calibration` prints a per-bucket hit rate from ≥5 fixture rows.

- **Turn every gate threshold into a named knob with a shadow mode** — FEATURE — value 5 — effort M — risk med — category: self-tuning
  Why: T-2269 tier checks (3+ options, 2+ readings), T-2271 "3 failed runs", and the blast-radius trigger are hard-coded numbers. Without a knob registry they can't be tuned or reverted. Shadow mode logs "would have refused" without enforcing.
  Done when: `fm knobs` lists each gate threshold with its default, current value and shadow-fire count, and a test shows a shadow knob logs but never blocks.

- **Propose a knob change only from outcomes Foreman didn't author** — FEATURE — value 5 — effort M — risk med — category: self-tuning
  Why: standing rule says weakness-finding uses signals Foreman didn't author (reverts, reopens, red-after-merge, cold reads by another model). A tuner fed by its own gate verdicts would game itself.
  Done when: `fm knobs propose` cites only reverts, reopens, post-merge red and user edits as evidence, and a test fails if a proposal's evidence field names a Foreman-authored verdict.

- **Auto-revert a knob when its metric worsens over a window** — FEATURE — value 4 — effort M — risk med — category: safety
  Why: "measured and reversible" is the lens. Each change stores the prior value, the metric, and a window (N closed tasks); a worse metric restores the old value and records why.
  Done when: a fixture where the metric worsens after a change reverts the knob in one `fm knobs sweep` run and writes a reason line; a better metric keeps it.

- **Score the race trigger: did the runner-up ever win?** — FEATURE — value 4 — effort S — risk low — category: races
  Why: T-2271 races the runner-up after 3 failed runs, with no record of whether racing paid. Winner, cost and time of each race, plus the first approach's eventual fate, would show whether to race earlier or never.
  Done when: `fm lane race` results append to a race ledger, and `fm knobs` shows runner-up win rate and tokens spent per tier.

- **Make the user's plan edits the training signal** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: the pack asks which plan edit the user makes most after accepting one. Diffing the accepted plan against the plan at close (rows added, options changed, tier raised) is a signal the planner didn't author and the user did.
  Done when: closing a task stores an edit-class summary, and `fm knobs propose` can cite "tier raised after accept in 4 of 6 M tasks".

- **Cap stated confidence by evidence kind and learn the cap** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: Mission 7 distinguishes typed/inconclusive from run evidence. A confidence statement resting on typed evidence should be capped, and the cap should be fitted from how often each kind was later reopened.
  Done when: a plan whose only evidence is typed cannot record confidence above its fitted cap, and a test shows the cap moving after fixture reopens.

- **Backtest a proposed gate on finished tasks before enabling it** — FEATURE — value 4 — effort L — risk med — category: safety
  Why: T-2285 shows a gate miscounting options that start with a flag. Replaying a candidate gate over the closed tasks' plans shows refusals on plans that held up fine, catching false positives before they cost the user.
  Done when: `fm knobs backtest KNOB=VALUE` prints how many past plans it would have refused and how many of those later failed, using at least 20 stored plans.

- **Quarantine the tuner with a hard change budget** — SECURITY — value 3 — effort S — risk low — category: guardrail
  Why: a self-modifying planner must not move the user's steer-derived rules or gen-0 fences. Only listed knobs may change, at most one per day, never anything a steer or the standing intent defines.
  Done when: a test shows the tuner refuses a knob tagged `steer` and a second change within the budget window, and `fm doctor` flags a knob changed outside the tuner.

- **Show the user one weekly tuning digest with one-word veto** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: changes the user never sees violate "decides and records". A short digest of knob moves, their evidence and a `fm knobs undo ID` line keeps it legible.
  Done when: the digest lists every change in the window with evidence and undo command, and undo restores the prior value in a test.

- **Wild: Hold a nightly "plan tournament" on the repo's own history** — FEATURE — value 4 — effort L — risk med — category: backtest
  Why: wild. Roll back to old commits, let the planner re-plan with current knobs, and compare against what the shipped change needed (files touched, tier, blast neighbours). Free arms only, per the testing-cadence steer.
  Done when: a run prints per-knob agreement with real history for ≥10 commits and writes no session tokens.

- **Wild: Let two knob sets race on live tasks (A/B planner)** — FEATURE — value 3 — effort L — risk high — category: experiment
  Why: wild. Route alternate S/M tasks through candidate vs current thresholds, compare reopen and attempt rates, and promote only if the gap exceeds noise over a stated minimum n.
  Done when: `fm knobs ab` reports n per arm and refuses promotion below the minimum sample, shown by a fixture test.

- **Wild: Pre-register a surprise score for every plan** — FEATURE — value 3 — effort M — risk low — category: humility
  Why: wild. The planner writes "I expect approach 1 to pass in ≤2 attempts" before work; a high surprise rate raises race depth automatically (a humility thermostat) and the surprise rate is shown beside the exam number.
  Done when: closing computes surprise per task, and a fixture with 5 surprises raises the race-depth knob within its allowed range.

- **Wild: Publish the planner's calibration curve on the site** — FEATURE — value 2 — effort S — risk low — category: transparency
  Why: wild. The site already refreshes stats daily (T-2326); a reliability plot of stated confidence vs outcome, with the denominator beside it, makes the claim checkable by anyone.
  Done when: the daily publish writes a calibration data file and the page renders it with n per bucket.

Next question: Which outcome signals does Foreman have today that it didn't author and that arrive within days, not weeks, so a knob's metric window can be short enough to learn from?
Next question: When two knobs interact (the option-count gate and the race trigger), how does the tuner attribute a better or worse outcome to one of them?
