# Brainstorm — lens: the calibration ledger (invented): every stated confidence is a bet scored later; overconfidence triggers research, underconfidence stops asking

- **Stamp every confidence with its evidence class at the moment it's stated** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: the pack's "Calibrated judgment" ask and prior ideas ("Record the confidence number with the evidence that moved it") stop at recording; a class (ran-it, read-it, recalled-it, guessed) is what lets the ledger be bucketed and scored. Assumption: confidence is currently free prose in Approach/Risks.
  Done when: `fm task set ID --confidence 0.7 --basis ran` is stored in an append-only file, and a plan with a confidence and no basis is refused for M/L tasks.

- **Score the ledger per bucket and print a reliability table in fm doctor** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: earlier ideas propose a Brier score and a curve; nothing says where the user sees the result. Doctor already names missing checks (steer rule). Assumption: closed tasks give a binary outcome (held vs reopened/reverted/re-fixed).
  Done when: `fm doctor` prints rows like "0.8–0.9: 14 bets, 9 held" and warns when a bucket is off by more than 20 points with at least 10 bets.

- **Let overconfidence in a bucket fire the research trigger automatically** — FEATURE — value 5 — effort M — risk med — category: research
  Why: the seed row says "unsure → research trigger (3)", but a keyword is a weak trigger. If a bucket has historically held 55% when stated at 90%, the next 90% claim in that bucket should require a research note first. Assumption: T-2269's plan gate can read the ledger.
  Done when: with a seeded ledger showing the 0.9 bucket held 55%, a new M task claiming 0.9 on a low-evidence basis is refused at focus with "research note or spike first", and a ledger-clean one passes.

- **Let a proven-reliable question class stop asking** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the lens's underconfidence half: every stop-and-ask is logged with the user's answer, and when the answer matched Foreman's own guess N times in a row (Wilson lower bound), it decides and records instead. Assumption: stops are classified into question classes.
  Done when: after 8 matched answers in one class, the ninth stop becomes a recorded decision with a one-line undo, and one mismatch re-enables asking.

- **Score the guess you didn't send: record Foreman's prediction of the user's answer before every ask** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: without a guess logged before the question, underconfidence can't be measured. Assumption: `fm ask` can write a row first.
  Done when: each `fm ask` row carries a guess and, after the answer, a hit/miss field; `fm triggers`-style output shows the hit rate per class.

- **Separate who scored the bet from who made it** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: the open question "which numbers has no one but the producing code checked?" and the standing rule on signals Foreman didn't author. Outcomes should come from reopen records, reverts, CI, and cold reads, never from the builder's own close note.
  Done when: the ledger file is written only by a hook or CLI path the model can't call directly (guard test), and resolution source is a required field.

- **Decay confidence when the files it rests on change** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: a claim made before a file changed shouldn't carry its old number. Assumption: each bet records the scope paths and tree hash.
  Done when: editing a scoped file after a 0.9 claim marks it "stale" in `fm task show`, and close requires a refreshed bet.

- **Price each miss: weight bets by cost of being wrong, not just count** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: a wrong 0.9 on a doc tweak and on a migration are not equal; the "irreversible plus ambiguous" stop rule needs a loss term. Assumption: door type is already classified.
  Done when: the table shows an expected-loss column and research is triggered by loss, not only by gap size.

- **Show the recalibrated number beside the stated one in the plan** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user reads "confidence 0.9 (history says ~0.6 for ran-less claims)" and knows when to look closer. Assumption: ledger has at least 10 bets per bucket.
  Done when: the plan and finish receipt print both numbers, hidden when data is under 10 bets.

- **Wild: Hold a weekly calibration quiz where a cold Haiku child bets on past tasks' outcomes** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild; seeds the ledger from history so the buckets fill in days, not months. Child sees the plan and diff, not the outcome; scored against real reopens.
  Done when: running it on 20 closed tasks writes 20 scored bets tagged "backtest" that never mix with live buckets.

- **Wild: Publish a public forecast page of Foreman's own scored bets** — FEATURE — value 3 — effort S — risk low — category: site
  Why: wild; the site already follows Genesis (standing rule), and a scored curve is the honest version of the held-rate scorecard in T-0867.
  Done when: `site/genesis` data includes the reliability table and the page renders it with the bet counts.

- **Wild: Let lanes bet before racing and pay out the winner's surprise** — FEATURE — value 3 — effort M — risk med — category: races
  Why: wild; extends T-2271's runner-up race. Each lane states its pass chance first, and a winner who had a low prior marks the first-instinct plan as a miss for the planner's own ledger.
  Done when: a race writes pre-registered numbers per lane and a surprise score, and the planner bucket updates from it.

- **Wild: A humility thermostat that tightens or loosens gates from the global Brier trend** — FEATURE — value 3 — effort L — risk high — category: tuning
  Why: wild; when recent bets run overconfident, plan-gate thresholds tighten one notch, and when well-calibrated they relax, with a hard change budget and one-command revert.
  Done when: in shadow mode it logs the proposed knob moves for 2 weeks without enforcing, and a revert restores the prior values.

Next question: Which stated confidences today live only in prose, and what share of closed tasks have a machine-readable outcome to score them against?
Next question: When the user overrides a calibrated decision, is that a miss for the ledger or a changed mind, and who classifies it?
