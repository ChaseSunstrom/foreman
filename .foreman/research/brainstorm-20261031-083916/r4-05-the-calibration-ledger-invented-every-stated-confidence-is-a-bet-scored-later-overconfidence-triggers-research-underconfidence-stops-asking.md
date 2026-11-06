# Brainstorm — lens: the calibration ledger (invented): every stated confidence is a bet scored later; overconfidence triggers research, underconfidence stops asking

- **Pre-register each confidence in a write-once ledger row** — FEATURE — value 5 — effort M — risk med — category: calibration
  Why: the pack's Mission 5 #8 wants "states confidence", yet earlier ideas only score after the fact. Assumption: confidences today live in prose Foreman can edit. A hook-written, append-only row (claim, number, evidence class, resolver, deadline) is made at the moment of stating.
  Done when: a test that tries to edit or delete a ledger row from a session path is refused, and `fm calibration show` lists the row with its resolver.

- **Print a reliability table per evidence class in `fm doctor`** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the pack has no measure of whether "80% sure" holds 80% of the time. Assumption: 30+ scored rows per bucket exist after a few weeks.
  Done when: `fm doctor` prints stated vs observed per bucket and says "too few" under 10 rows, not a number.

- **Fire the research trigger on bucket overconfidence, not keywords** — FEATURE — value 5 — effort M — risk med — category: research
  Why: the seed row says "unsure → research trigger (3)". Make it data-driven: when a bucket's observed rate trails stated by more than a set gap, the next claim in that bucket needs a research note before the plan gate passes.
  Done when: a fixture ledger with an overconfident bucket makes `fm task focus` refuse an M task that lacks a note, and a calibrated bucket passes.

- **Let a proven-reliable question class stop asking** — FEATURE — value 5 — effort M — risk high — category: autonomy
  Why: the user is repeatedly interrupted by `fm ask`, and the standing steer says to stop only for the irreversible and ambiguous. Record Foreman's guess before each ask and score it against the answer; after a Wilson lower bound clears a threshold on a reversible class, decide and record a one-line undo.
  Done when: a class with 12 of 12 matches stops asking, one miss re-opens asking, and each skip appears in a receipts file.

- **Cap stated confidence by evidence kind** — SECURITY — value 4 — effort S — risk low — category: honesty
  Why: the pack has "Unproven rollup" for done tasks resting on typed or inconclusive evidence. Carry that into confidence: typed evidence caps at 60%, a run command lifts the cap.
  Done when: a claim of 95% on typed evidence is written as 60% with the reason, in a test.

- **Decay confidence when its files change** — FEATURE — value 3 — effort M — risk low — category: staleness
  Why: assumption: claims made at plan time outlive edits to the scope paths. Store the tree hash of the scope with each bet and mark it "stale" after a change.
  Done when: editing a scoped file turns the row's state to stale and the close receipt lists it.

- **Score the scorers: audit who resolves each bet** — SECURITY — value 4 — effort M — risk med — category: integrity
  Why: the open question "which verbs have a model on both sides with no user-owned check" applies here. Reject any bet whose maker and resolver are the same model session, unless a command ran.
  Done when: a bet resolved by its own session without a command is stored as "unscored" and excluded from the table.

- **Price the miss, not just count it** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: a wrong guess on a one-way step costs more than one on a reversible step. Weight each row by the door class and the user's minutes lost, and show cost-weighted Brier.
  Done when: two equal misses with different door classes give different weights in `fm calibration show`.

- **Show one weekly calibration digest with a one-word veto** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: assumption: the user will not read a table, but will read three lines: what got more trusted, what got stricter, what changed. "undo" reverts the last knob move.
  Done when: the digest renders in under 10 lines and `fm calibration undo` restores the prior threshold.

- **Wild: Hold a weekly calibration quiz with a cold Haiku child as bettor** — FEATURE — value 3 — effort M — risk low — category: validation
  Why: wild. The child sees only a closed task's request and bets on its outcome. If it out-forecasts Foreman's own ledger, the ledger's features are leaking nothing useful.
  Done when: a report compares the child's Brier score with Foreman's on the same 20 tasks.

- **Wild: Let racing lanes bet before they run** — FEATURE — value 3 — effort L — risk med — category: races
  Why: wild. Each lane states its odds of passing the frozen verify; payouts scale with surprise, and the router learns which model's odds to trust, which feeds the history-based router (T-2291).
  Done when: a race records every lane's pre-run bet, and the router prints a per-model trust figure.

- **Wild: Publish Foreman's scored forecasts on the site** — FEATURE — value 2 — effort S — risk med — category: trust
  Why: wild. The site follows Genesis on its own (a standing steer); a public Brier curve is a number nobody on the team can quietly flatter.
  Done when: `site/genesis` data includes the curve with its row count and the page shows "n=" beside it.

- **Add a humility thermostat driven by the global trend** — FEATURE — value 3 — effort M — risk high — category: gates
  Why: assumption: gate strictness is fixed today. If the 14-day Brier worsens, tighten the plan gate by one tier; if it improves, loosen. Capped at one step a week, with revert.
  Done when: a simulated worsening ledger raises strictness once, a second worsening in the same week does not, and `fm calibration undo` reverts it.

Next question: Where does a stated confidence first appear in a session today (plan text, ask, receipt), and which of those places can a hook capture without parsing prose?
Next question: Will a ledger of a few dozen bets per month ever have enough rows per bucket to calibrate anything, or must buckets be coarser than the evidence classes above?
