# Brainstorm — lens: self-modification: a planner whose stated confidence and chosen approach are scored against what happened, so its gates and races retune themselves, measured and reversible

- **Keep a calibration ledger of stated confidence vs. outcome** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: T-2290 records predictions of minutes and attempts, but the stated confidence on assumptions and Approach choices (Mission 5 #8) isn't scored. The ledger would score each confidence against first-time pass, reopen or revert, and print a reliability table per tier.
  Done when: `fm calibration` prints, per tier, stated-confidence buckets against the observed hold rate, built from at least 20 closed tasks.

- **Version every gate threshold as a knob with one-command revert** — FEATURE — value 5 — effort M — risk low — category: reversibility
  Why: T-2269 hardcodes "3+ options" and "2+ readings", and the Lean ratchet hardcodes its margin. Self-tuning needs values in `knobs.json` with history, an evidence link per change, and `fm tune revert ID`. Without that, every retune is irreversible.
  Done when: changing a knob writes a dated entry, and `fm tune revert` restores the old value and the gate behaves as before (tested).

- **Log gate refusals and what happened next** — FIX — value 4 — effort S — risk low — category: gate telemetry
  Why: T-2285 (a gate rejecting an option that starts with a flag) was found by the user, not by Foreman. A refusal followed by a one-edit pass that changes only formatting is a false positive and should file a FIX automatically. This is the Mission 8 #7 signal-to-fix loop applied to Foreman's own gates.
  Done when: a seeded false refusal produces one FIX task naming the gate, and a refusal followed by a real plan change does not.

- **Run candidate gates in shadow before enforcing** — FEATURE — value 4 — effort M — risk med — category: gate tuning
  Why: tightening a gate blind risks the stalls the dropped `_next_runnable` item worried about. Shadow mode records "would have blocked" per task and compares it with later reopens and reverts. A gate enforces only if it would have caught at least one real miss and no more than N% of clean passes.
  Done when: `fm tune shadow GATE` reports would-block count against outcomes over the last N tasks, and the gate stays off until promoted.

- **Score the race trigger and the runner-up** — FEATURE — value 4 — effort S — risk low — category: races
  Why: T-2271 fires after 3 failed runs. Nobody knows whether the runner-up ever wins, or whether racing earlier would have cost less. The race ledger records winner, cost and the failure count at firing. After 10 races it suggests 2 or 4 as the trigger.
  Done when: `fm triggers` shows race win rate for the runner-up and cost per race, and a threshold suggestion appears after 10 races.

- **Score research triggers on whether the research changed the plan** — FEATURE — value 3 — effort S — risk low — category: judgment
  Why: "unsure → research" has no cost check. If a research note never alters the Approach choice, the unsure threshold is too jumpy. If a spike-less low-confidence assumption later fails, it's too lax.
  Done when: each research note records "changed choice yes/no", and `fm calibration` shows the change rate per tier.

- **Check blast-radius neighbours against where the task actually failed** — FEATURE — value 3 — effort M — risk low — category: blast radius
  Why: T-2277 writes co-change neighbours into Risks. Whether the later red tests or reverts landed in those neighbours isn't scored. Neighbours that never hit get ranked lower, which shortens the Risks text.
  Done when: the plan's Risks list shows hit-rate per neighbour source (co-change, past FIX), and sources under 10% are dropped by default.

- **Tune tier assignment from actual effort** — FIX — value 3 — effort S — risk low — category: tiering
  Why: every gate hangs off S/M/L, and a task misfiled as S skips the readings and race gates. Compare the tier set at creation with active minutes and attempts at close, and propose reclassification rules for the creator.
  Done when: `fm tier audit` lists the misfiled share per type and proposes one rule change with evidence.

- **Use only outcome signals Foreman didn't author when tuning** — SECURITY — value 4 — effort S — risk low — category: anti-gaming
  Why: the steers require signals Foreman didn't author (outcome survival, cold reads). A tuner that optimises "gate passes" would game itself. Tuner inputs would be whitelisted to reverts, reopens, and red-after-merge. A self-reported metric would be rejected with a message.
  Done when: a tuning proposal citing a self-reported metric is refused by `fm tune`, and the whitelist is shown in `fm doctor`.

- **Auto-revert a knob when its measured metric worsens** — FEATURE — value 4 — effort M — risk med — category: safety net
  Why: every retune carries a prediction ("reopen rate should fall"). After N tasks the knob is scored. If the metric is worse, it reverts and records the reason. That keeps self-modification honest. Assumption: N around 15 closed tasks is enough signal.
  Done when: a seeded bad knob reverts itself after N tasks with a visible ledger line.

- **Wild: Backtest the planner against its own history** — FEATURE — value 4 — effort L — risk low — category: replay
  Why: wild. Replay the plan gate and race rules of today against the last 200 closed tasks. Report what each rule would have changed, so a new rule has a score before it ships.
  Done when: `fm tune backtest KNOBSET` prints would-have-caught and would-have-blocked counts for a past window.

- **Wild: Run a nightly knob-mutation tournament** — FEATURE — value 3 — effort L — risk med — category: evolution
  Why: wild. Each night the planner mutates one knob, backtests it on history, and proposes the winner as a PR-style task for the user to accept. It never applies one itself.
  Done when: a nightly run files at most one proposal with its backtest diff, and none is applied without the user's accept.

- **Wild: Publish the planner's Brier score on the site** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: wild. The Genesis site already follows the tower. A public calibration curve (stated confidence against reality) would keep the claims honest and meet the "show the number and the claim beside each other" idea.
  Done when: the site's stats include a calibration chart refreshed by the daily publish.

- **Wild: Add a humility thermostat** — FEATURE — value 3 — effort M — risk med — category: adaptive ceremony
  Why: wild. When rolling calibration worsens, ceremony rises automatically: more readings, earlier races, more research. When it recovers, ceremony relaxes. This is the profile-per-task-kind idea (T-1266) driven by the planner's own track record.
  Done when: a simulated run of bad outcomes raises the tier requirements, and good outcomes lower them, each change logged and revertible.

Next question: which of the planner's gates has never been wrong in a way someone other than Foreman noticed, and how would we know?
Next question: how many closed tasks does Foreman need before a tuning signal is distinguishable from noise, given this repo's task volume?
