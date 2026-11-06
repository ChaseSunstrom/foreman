# Brainstorm — lens: deepen: calibration

- **Gate every "none" behind a canary recall check** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: the exam shows finders caught 0 of 108 planted defects, yet a quiet scan reads as "clean". Mission 3 is graded on the exam's `none` kind, where saying "nothing here" correctly is the point. Merges the many "plant canaries first" ideas into one rule.
  Done when: `fm scout` on a repo with no findings prints "clean (canary recall 4/5 on this stack)" or "unverified: canary recall below floor", and a test with a deliberately blind finder gets "unverified".

- **Build a mutation-based canary planter per language** — FEATURE — value 5 — effort L — risk med — category: calibration
  Why: planting needs real defects, not comments. Applying small mutations (off-by-one, dropped null check, swapped comparison, removed `await`) in a scratch worktree gives bugs whose location is known, and the repo's own tests tell you whether each is detectable. Exam covers python, js, ts, ruby, rust and c, so one mutator table per language.
  Done when: `fm calibrate plant --n 10` on a fixture repo in each of the 6 languages writes a hidden key of file:line:kind, and the key never sits in the worktree the finders can read.

- **Score precision against a decoy set, not just recall** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: recall alone rewards a finder that flags everything. Mixing known-false lookalikes (code that resembles a bug but is guarded) into the scratch copy exposes false-positive rates, which matter for the `none` kind.
  Done when: calibration output shows recall and precision per finder, and a finder that flags every line scores precision under 0.2 in a test.

- **Keep a per-kind trust table that gates ranking weight** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the user asked for ranking by value, but a ranker with uncalibrated inputs is false precision. Combine canary recall, decoy precision and `fm outcomes` 30-day survival into one weight per finding kind and stack; mute kinds that score near zero.
  Done when: `fm findings` shows a trust column per kind, and a kind whose survival is 0 across 10 or more findings ranks below the cutoff in a test.

- **Make "proved" a graded claim: failing test strength score** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: the pipeline proves each finding with a failing test, but a test can fail for the wrong reason. Check that the test fails on the original, passes on the fix, and fails again when the fix is mutated back in; record the failure message matches the claimed bug.
  Done when: a finding whose test fails with an import error is marked "unproven", and a test suite exercises both the pass and the reject path.

- **Predict, then prove: log the finder's confidence and score it** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: each finding gets a stated probability that it's real. After the repro runs, the Brier score per finder accumulates, so confidence becomes a measured quantity.
  Done when: `fm findings --calibration` prints a reliability table (stated vs observed per bucket) after at least 20 resolved findings.

- **Predict each night's yield and score the forecast** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: `fm night` queues `fm run --fit --max 2`; a forecast like "expect 2 real findings, $0.40" scored against the morning result tells the user whether to trust the shift, and sizes the budget (a question earlier brainstorms left).
  Done when: the morning summary line states predicted vs actual findings and cost, and the ledger holds the error for 7 consecutive nights.

- **Wild: Build a never-seen bug corpus from package version pairs** — FEATURE — value 5 — effort L — risk med — category: calibration
  Why: wild. Pairing a package's buggy release with its fix commit, via the changelog or a linked issue, gives real bugs with real fixes that postdate training data. That is a held-out exam the user does not author, and it answers "who audits the hidden keys".
  Done when: `fm calibrate corpus --ecosystem pypi --n 20` produces 20 buggy-checkout/test pairs where the fix's test fails before and passes after.

- **Wild: Run a silence quiz before trusting a quiet repo** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild. Hand the hunter a repo known to be clean (a pinned, heavily tested release) and a twin with one planted bug, unlabeled, and require it to separate them. Grades the `none` kind head-on and costs one extra run.
  Done when: the quiz reports "separated twin from clean" or "failed", and a blind finder fails it in a test.

- **Wild: Stake credibility on each finding with a bet ledger** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild. Each probe starts with a balance and stakes some of it per finding; confirmed findings pay out, refuted ones burn it, and a broke probe is paused until recalibrated. It turns calibration into a self-throttling economy that needs no human tuning.
  Done when: a probe that makes 5 refuted findings in a row drops below the stake floor and stops queueing tasks in a test.

- **Wild: Slip decoy findings into the review card** — FEATURE — value 3 — effort S — risk med — category: calibration
  Why: wild. Mixing 1 known-false finding into every 10 the user sees measures whether the user, or the ranker, rubber-stamps. If the decoy is accepted, the approval signal is discounted.
  Done when: the card marks a decoy accepted as "approval discounted" and the ledger records the rubber-stamp rate per week.

- **Detect calibration drift when the model or repo changes** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: a recall number from last month says little after a model swap or a big refactor. Store the canary score with model id and repo hash, and re-run when either shifts.
  Done when: changing the configured model makes the next scan print "calibration stale" and rerun the canaries before reporting.

- **Check that exam deltas predict survival** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the pack asks whether a passing exam predicts 30-day survival. Join exam scores by scenario kind to `fm outcomes` and flag kinds with near-zero correlation as measuring nothing.
  Done when: `fm exam --validity` prints a correlation per kind with sample counts and marks kinds under 10 samples "insufficient".

Next question: Where do the canaries' hidden keys live so a finder with file access can never read them, and who checks that a mutation actually breaks behavior rather than being a no-op?
Next question: What recall floor makes a "clean" claim trustworthy, and what is it per language when the planted bugs are easy ones the real defects are not?
