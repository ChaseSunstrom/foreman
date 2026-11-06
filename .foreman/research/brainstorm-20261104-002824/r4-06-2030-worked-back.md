# Brainstorm — lens: 2030 worked back

- **Graduate stable predictions into plain recipes** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: assumption: by 2030 most repeat asks (ship landed commits, bump, re-prove) should need no model. The pack has "Detect periodic asks" and "Mine event→ask rules" but no path for a prediction to stop being a prediction.
  Done when: a row that was accepted unedited 5 times is shown as a proposed recipe. After the user accepts it, `fm anticipate` mutes that row and the recipe fires with zero model calls (test: ledger fixture, token counter at 0).

- **Seal replayable state→outcome cases as a private model bench** — FEATURE — value 5 — effort M — risk low — category: models
  Why: the local-model steer plus the T-2886/T-2887 model-bench asks. Models will turn over before 2030, and "Freeze monthly predictor vintages" scores old predictors, not new models on old states. Store the input bundle (ledger-tail hash, HEAD, pack) and the outcome so any future model can re-predict 2026.
  Done when: `sampo anticipate bench --model X` re-predicts the last N sealed cases from stored bundles and prints hit rate against the recency baseline, with exit 2 if a bundle can't be rebuilt.

- **Keep one surface-use ledger that grounding, drafting and the Exam all read** — CLEAN — value 4 — effort S — risk low — category: grounding
  Why: the carried gap "grounding checks the surface is in use" is currently several separate checks (drafts, Exam, canary). One append-only file of "surface touched, by whom, when" ends the three-way drift.
  Done when: grep shows the brief Exam, the draft gate and the grounding step all read the same file. A surface unused for 30 days blocks a draft with the reason printed.

- **Give each predictor rule a measured half-life** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: assumption: rules decay at different speeds (a ritual lasts years, a project-specific follow-up lasts weeks). Re-validating every rule at one interval wastes tokens or misses decay.
  Done when: `fm anticipate rules` prints each rule's days-above-baseline and the next recheck date derived from it. A fixture rule that stops beating the baseline is rechecked sooner than a stable one.

- **Draft renewals for everything that expires, 7 days early** — FEATURE — value 4 — effort S — risk low — category: obligations
  Why: the pack has grants, leases, review-by dates, quota windows, caps and EOL dates, each as its own warning. Nothing drafts the *action* (renew, rotate, reopen) on spec in a lane before the date.
  Done when: a grant set to expire in 6 days produces a dormant draft brief naming the renewal command. The brief is withdrawn when the grant is renewed (test with a fake clock).

- **Replay each Exam on the parent commit and on a fake-empty world at filing** — FIX — value 4 — effort S — risk low — category: Exam
  Why: the carried gap "every brief's Exam reads live state" needs a guard that the reading can differ. The pack has "outcome measure must read differently on the parent commit" only as an idea. This extends it to speculative drafts, where nobody reviewed the measure.
  Done when: filing a draft whose Exam reads the same on parent and on an empty fixture is refused with "vacuous Exam".

- **Run a canary on a draft's nouns before the user sees it** — FEATURE — value 3 — effort S — risk low — category: canaries
  Why: canaries currently sit near the idea claim. A drafted ask inherits the same "already built" failure (see the many "premise already met" drops), so the canary should run at draft time and print the three nearest existing things.
  Done when: a draft whose title nouns match a shipped verb is filed with a "nearest existing" line, or suppressed above a similarity threshold. The test uses a draft of an existing verb.

- **Score drafts by edit distance to what the user finally typed, per field** — PERFORMANCE — value 4 — effort M — risk low — category: user-model
  Why: "Learn which draft fields the user rewrites" is listed, but it is a lesson, not a headline number. The 2030 target is that the distance falls toward zero. It also feeds the per-kind trust promotion.
  Done when: `fm anticipate score` shows median per-field distance for the last 30 days, split by task kind. A planted rewrite in the fixture raises its field's number.

- **Reserve an exploration slot for the grid cell the user never touches** — FEATURE — value 3 — effort S — risk med — category: anticipation
  Why: assumption: a predictor trained on the user's history narrows what Sampo offers. The pack has induced-demand holdouts but no deliberate widening, and the coverage grid already names empty cells.
  Done when: one draft per week is chosen from an untouched grid cell, tagged "exploration", and counted separately from hit rate.

- **Wild: Hold a dojo where the user guesses what Sampo will predict** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. The pack models the user, but not the user's model of Sampo. A 2-minute quiz of 5 sealed predictions shows where the user's trust is miscalibrated (over-trusting rubber-stamp, or under-trusting).
  Done when: `fm dojo` shows 5 sealed predictions, records the user's guesses and prints agreement. The result changes which row types need a second reader.

- **Wild: Have a cold child play the user in 2030 and write its five complaints** — FEATURE — value 3 — effort S — risk low — category: foresight
  Why: wild. Given only today's trends (ledger growth, model churn, host-native features), a tool-less child writes the complaints a 2030 user would have. Each complaint becomes a canary item or a filed bet. It is the cheapest form of working backward.
  Done when: a dated file of 5 complaints exists per generation, each one linked to a filed task or a recorded "n/a" with a reason.

- **Wild: Run a season league of every model on the sealed cases** — FEATURE — value 3 — effort M — risk low — category: models
  Why: wild. This builds on the sealed-case bench. Each local model, small and 27B, and each frontier model plays a quarterly season. The site's Models section shows the table, so the swap decision is visible to the user rather than buried in the ledger.
  Done when: a season table is generated from the bench with no hand editing. It includes cost per hit and appears on the site Models section.

- **Make the predictor deletable on purpose** — CLEAN — value 4 — effort S — risk low — category: lean
  Why: the lean steers. If graduation turns most rows into recipes, the predictor should be able to retire itself. A single `fm anticipate off` state must leave every graduated recipe working.
  Done when: with the predictor off, graduated recipes still fire and `fm doctor` reports "predictor off by choice" as a non-red line.

Next question: which of the user's repeat asks in the last 90 days would have passed a zero-token recipe, and what share of all asks is that?
Next question: when a new local model beats the sealed-case baseline, who decides to switch the model, and what does a switch cost the user in the morning's first hour?
