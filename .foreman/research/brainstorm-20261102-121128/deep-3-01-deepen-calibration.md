# Brainstorm — lens: deepen: calibration

- **Reversal ledger for "proven" labels** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: the pack's open question asks which "proven" labels were later reversed and what share had no run record; five calibration ideas circle this without a store. This merges them into one append-only ledger: each proven label, the run record behind it (or "none"), and any later reversal (reopen, revert commit, failed re-verify, user override).
  Done when: `fm outcomes --reversals` prints reversal rate over the last N finished tasks, split by "had a run record" vs "no run record", and a fixture with one reversed task shows in it.

- **Predict-then-run proof commands** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the bets machinery (Brier, base rates) exists but covers closes, tasks and choices. A pass/fail guess before each `fm task prove` run adds many cheap, fast-settling bets, and the settling is immediate rather than a 30-day wait (T-2610).
  Done when: `fm task prove` records a stated probability before execution, and `fm outcomes --judgment` shows a "proof" bet kind with a Brier score.

- **Confidence-gated ceremony** — FEATURE — value 5 — effort M — risk med — category: calibration
  Why: T-1266 (ceremony profile per task kind) is deferred for want of data. The calibration table is that data: where Foreman's predictions are overconfident, require the full prove and cold-read path, and where it is well calibrated, let it skip. This turns a score into behaviour.
  Done when: with a seeded history where "docs" bets have Brier below 0.1 and "refactor" bets above 0.3, `fm next` shows a lighter plan for docs than for refactor and names the reason.

- **Outside-signal contradiction check** — SECURITY — value 4 — effort M — risk low — category: calibration
  Why: the pack asks which gauges Foreman trusts only because it wrote them (timer liveness, bet settlement). The check compares each gauge to a signal Foreman didn't write (systemd's `LastTriggerUSec`, git history, CI status), consistent with the "signals Foreman didn't author" steer.
  Done when: `fm doctor` flags a planted case in which the bet ledger says "settled" but git shows no matching commit, naming both sources.

- **Human override ledger** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: the question "who records that an override isn't proof?" has no owner. Overrides are logged with a reason, and the receipt shows "overridden, not proven". Overrides later reversed count against calibration, and overrides that held count for it.
  Done when: an overridden row's receipt says "override (unproven)", and `fm outcomes` reports override survival next to proof survival.

- **Let the user bet against Foreman** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: there's a shell-checking habit nothing logs. A one-line `fm bet --against T-1234 "will be reopened"` captures the user's own doubt as ground truth Foreman didn't author, and it settles through the existing 30-day window.
  Done when: a user bet appears in `fm outcomes --by harness` as harness "user", with Foreman's Brier shown against it.

- **"Unproven" as a first-class receipt state** — FIX — value 4 — effort S — risk low — category: calibration
  Why: the pack asks how a receipt says "unproven" when a UI check can't run. Calibration needs a third state besides pass and fail: "not run, and why." A reader that treats a missing record as a pass would give a wrong answer, not an error.
  Done when: a UI check run with no display writes `unproven: no display` in the receipt, and the proven-rate denominator excludes it while a separate count shows it.

- **Calibration drift alarm** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: the nightly digest already names the worst Brier bucket once 20 are scored. A rolling-window comparison would catch a model or harness change, such as a Claude upgrade, that makes bets worse, and fire at the first shift instead of at an arbitrary count.
  Done when: seeded bets whose second half is much worse trigger a doctor WARN naming the harness and the date of the change.

- **Settled-bet one-liners in the feed (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The pack's list has three variants of this. Turn it into a streak counter: "Called it: 7 closes held in a row", or "Missed: T-2601 reopened (said 92%)", in the terminal and on the web UI, so the number gets looked at.
  Done when: a settled bet prints one line in the session note, and a miss reads differently from a hit.

- **Calibration court (wild)** — FEATURE — value 3 — effort L — risk med — category: calibration
  Why: wild. A cold Sonnet reads a closed task's evidence blind and gives its own probability that it holds. Foreman's and the court's probabilities are scored against later survival, so the user sees which judge is better calibrated, which is a signal from a different model.
  Done when: `fm outcomes --court` lists tasks where Foreman and the court disagreed by 30+ points and who was right once settled.

- **Forecast the whole queue (wild)** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild. Before a drive, Foreman bets on each queued task: chance of first-time pass, cost, time. After the drive, a report shows predicted vs actual, so the user can decide whether an overnight drive is worth starting.
  Done when: `fm drive --forecast` prints per-task odds and a total expected cost, and the next day's digest compares them with the actual figures.

- **Restore drill with calibration carried over (wild)** — FEATURE — value 3 — effort L — risk med — category: calibration
  Why: wild. The pack asks what must be rebuilt by hand after a host wipe. Calibration history is the thing that's hardest to rebuild. A drill restores the ledgers into a scratch directory, reruns the Brier computation, and checks it matches the live numbers.
  Done when: `fm doctor --restore-drill` reports match or mismatch of the Brier table from an exported bundle.

- **Calibration card in the session start** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: the standing rule says every capability must be reached by a real session path. A two-line card at session start ("closes on refactors: you've overridden 3, 2 reversed") puts the numbers in front of the agent when it decides how careful to be.
  Done when: a session start note contains the card only when 20 or more bets are scored, and a test pins its length.

Next question: Which calibration numbers have actually changed a decision the user made, so that the ledger can be measured by its use and not just by its accuracy?
Next question: What would a bet's settlement look like for work with no later signal (docs, deletions), and does the ledger quietly count those as survived?
