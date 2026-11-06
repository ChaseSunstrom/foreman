# Brainstorm — lens: deepen: dissent

- **Settle dissents in a ledger, not a vote** — FEATURE — value 5 — effort M — risk low — category: dissent
  Why: the carried gap is "dissents scored against outcomes"; the pack's ideas each pick a signal but none gives one store. Grow them into `dissents.jsonl`, one line per dissent: id, claim, author lens and model, wake predicate, reversal cost, status (pending / vindicated / overruled / unmeasurable). Every scoring idea becomes a reader of that file.
  Done when: `fm dissent list` shows every gen-4 Mission dissent with a status, and a test shows a dissent moves from pending to a verdict only when its outcome record exists.

- **Wake a dissent from its predicate** — FEATURE — value 5 — effort M — risk med — category: dissent
  Why: it combines "runnable predicate", "sleeping task" and "hold as pending measurement". The dissent is written as `if <observable> by <date>`, e.g. the close is reopened, or the same test is edited within 14 days. `fm next` evaluates it from git and the ledger, with no model call.
  Done when: a fixture dissent with predicate "task T-x reopened within 14 days" flips to vindicated in `fm next` after a reopen line is appended, and stays pending otherwise.

- **Require every dissent to name its loser-pays measure** — CLEAN — value 4 — effort S — risk low — category: dissent
  Why: the asked gap is that every brief's Exam names an outcome measure; extend it to the dissent. Assumption: many dissents are vague opinions, so a dissent with no measure and no date fails `fm genesis check` as vacuous, like a templated coverage cell.
  Done when: a dissent lacking measure or date fails the check with the line quoted, and a well-formed one passes.

- **Score the dissenter lens by calibration, not hits** — FEATURE — value 4 — effort M — risk low — category: dissent
  Why: it takes up "rank by correlation" and "model family and score echo". Per lens and model, it records dissents raised, vindicated and overruled, and the base rate of the thing being dissented. A lens that dissents and is right 5% of the time is noise; one right 60% is signal. This feeds `lens_rates`, which the T-0829 lens scaling needs.
  Done when: `fm outcomes --dissent` prints per-lens raised / vindicated / base-rate, with a floor of N scored before any rate shows (as the MUTE_MIN floor does).

- **Re-raise as the cheap vindication** — FEATURE — value 3 — effort S — risk low — category: dissent
  Why: it takes up "settle by whether the next Seed re-raises it". A dissent that an independent later cold read repeats without seeing it is evidence. It is an early signal before the 14-day outcome exists, labelled provisional in lineage.md like the other early selection signals.
  Done when: a seed-time check matches new dissents to prior ones by quoted clause and marks the earlier one "re-raised", with the match shown.

- **Run the hindsight child on closed dissents** — FEATURE — value 4 — effort M — risk med — category: dissent
  Why: it combines "hand a hindsight child the ledger 14 days later" and "replay the overruled dissent". A tool-less child reads the dissent, the diff and what happened next, and rules vindicated / not / can't tell, quoting the evidence. It is a different model from the author, the signal Foreman didn't write, per the standing rule.
  Done when: the child's verdict on 5 seeded dissents with known outcomes matches the known answer on at least 4, and a "can't tell" is allowed.

- **Make the Mission page show the dissent beside the claim it contradicts** — FEATURE — value 3 — effort S — risk low — category: dissent
  Why: it takes up the two-pan scale. Assumption: the user reads the grid cell first (an earlier question), so the dissent sits in that cell, with a day counter and reversal cost; the scale tips on the verdict.
  Done when: the site/genesis page renders a pending dissent with its counter, and the rendering changes when the status changes.

- **Show unanimity as a warning when the lenses never dissented** — FEATURE — value 3 — effort S — risk low — category: dissent
  Why: the pack lists "audit unanimity as a signal". Zero dissents across lenses on a large Mission is itself suspect, and the Mission's report says "no dissent raised: N lenses agreed", with a comparison against the typical rate.
  Done when: a Mission with 0 dissents across at least 4 lenses prints the unanimity line, and one with dissents doesn't.

- **Charge the dissent's reversal cost up front** — FEATURE — value 3 — effort S — risk low — category: dissent
  Why: it combines "show the cost to reverse" with the shadow patch. Each dissent carries S/M/L to undo the majority path. An expensive-to-reverse path with an open dissent is flagged by `fm next` before it is built.
  Done when: a task built on a Mission path with an open L-cost dissent shows a warning at `fm task new`.

- **Hunch box: one-line doubts that become dissents (wild)** — FEATURE — value 3 — effort S — risk low — category: dissent — wild
  Why: the user's words are mostly terse asks. Assumption: they hold doubts they don't write. `fm hunch "…"` stores a doubt, and the next Mission must answer it as a dissent with a predicate, or say why not.
  Done when: a stored hunch appears in the next Mission's dissent section with its status.

- **Opposite-day Mission with a shadow patch (wild)** — FEATURE — value 4 — effort L — risk med — category: dissent — wild
  Why: it fuses "opposite-day Mission" with "unapplied shadow patch". Once per generation, a lane builds the rejected alternative to a worktree, never merged, and the exam runs both. The cold exam, not argument, shows whether the dissent was right.
  Done when: a gen-4 run produces a shadow branch plus a scorecard of both versions on the same held-out scenarios.

- **Give the dissenter a stake the user can cash (wild)** — FEATURE — value 2 — effort M — risk low — category: dissent — wild
  Why: it takes up "points stake". Each lens gets a bankroll; it stakes points on each dissent, and the pool grows or shrinks on the verdict. Low-bankroll lenses get fewer dissent slots, a natural version of lens scaling.
  Done when: `fm outcomes --dissent` prints each lens's balance, and a seeded vindication raises it by the staked amount.

- **Pool the dissents, as M-12 pools forecasters (wild)** — FEATURE — value 3 — effort M — risk med — category: dissent — wild
  Why: moonshot M-12 asks whether a log-weighted pool beats the best forecaster, and its result exists. Assumption: if pooling won there, weight dissents by lens calibration and surface the pooled probability that the majority path fails.
  Done when: the Mission prints one pooled "chance this path fails" number, and a backtest on past closes shows its Brier score against a flat prior.

Next question: Which past Missions' dissents can be reconstructed from the record at all, and is there enough history to calibrate any lens before gen 5?
Next question: When a dissent is vindicated, who pays: does the builder get a task, the Seed a rewrite, or the user a notice?
