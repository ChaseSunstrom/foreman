# Brainstorm — lens: capability map

Capability map: reference tools are Taskmaster, Kiro, Spec Kit, Linear, Shape Up, Terraform plan/apply and Temporal. The "ideas so far" list already covers most of what those do, so these are gaps it doesn't show. Each of 5, 7, 8 and 9 builds on an existing idea and adds something new.

- **Check name and namespace availability at plan time** — FEATURE — value 3 — effort S — risk low — category: launch
  Why: assumption: a goal that ships a package or tool hits a taken name late, and the pack shows no row for it.
  Done when: a goal that names a product gets a row listing availability on PyPI, npm, crates.io, GitHub and a domain check, and a fixture with a taken name turns the row red.

- **Verify a repo hygiene and launch-asset pack** — FEATURE — value 3 — effort M — risk low — category: templates
  Why: assumption: the existing product-type templates cover day-2 operations. Nothing covers LICENSE, SECURITY.md, CONTRIBUTING, issue templates, a dependency-update config, a demo cast and screenshots that match the current build.
  Done when: a finished fixture goal is red until each file exists and the screenshot's build hash matches HEAD.

- **Give "done" a quorum with a disagreement matrix** — FEATURE — value 5 — effort M — risk med — category: done-detection
  Why: the pack proposes the oracle, a cold read and a second-harness read as separate gates. Nothing composes them or reports where they disagree, and "knows when it's done" is the core ask.
  Done when: finish needs a declared quorum (for example oracle plus cold read plus one user tap), and a planted case where one voter dissents prints which voter and why, and does not close.

- **Plan cutover and parallel-run rows when the goal replaces something the user uses** — FEATURE — value 4 — effort M — risk med — category: migration
  Why: the pack covers deleting what a goal replaced, but not importing the user's existing data, mapping their habits, running old and new side by side, or setting a rollback window. Assumption: replacing existing tooling is a common goal shape.
  Done when: a replace-X goal gets rows for inventory, import with a count check, a parallel-run period and a dated rollback, and finish refuses while the import count mismatches.

- **Fit the finish-date band to the user's real working cadence** — FEATURE — value 3 — effort S — risk low — category: forecasting
  Why: the pack proposes an honest date band and asks about nights, weekends and long gaps, but never says the band should be built from the user's session history.
  Done when: the band is computed from the last 60 days of session timestamps. A fixture user who works only weekends gets a band that skips weekdays.

- **Cut a salvage release at each wave boundary** — FEATURE — value 4 — effort M — risk low — category: ordering
  Why: "any stopping day leaves something runnable" is proposed as an ordering rule. Nothing creates the artifact: a tag plus a generated known-limitations file listing the rows not done.
  Done when: closing a wave writes a tagged build and a KNOWN-GAPS file. Deleting every later row leaves a build that runs and a file that names what is missing.

- **Measure plan recall with a cross-check by a second planner** — FEATURE — value 3 — effort S — risk low — category: plan quality
  Why: the pack has capture-recapture and a rival decomposition as separate ideas. Nothing reports a single number to the user, such as "two independent plans overlap 71%, so about N rows are probably missing".
  Done when: the goal card shows an overlap-based completeness estimate, and a seeded plan with 5 rows removed shows lower overlap.

- **Compare plan steps with this user's past rows that went stale or got cut** — FEATURE — value 3 — effort M — risk low — category: user model
  Why: the pack has a warning about the row this user historically stalls on. This goes further by checking each new row against the user's own cut and stale history by row type.
  Done when: a row type the user cut twice before is flagged at plan time with the two prior task ids.

- **Rank a goal's rows by the first week of use** — FEATURE — value 3 — effort S — risk low — category: ordering
  Why: assumption: rows are ordered by dependency and risk. Nothing orders them by what the user would touch on day one, so the earliest useful cut can be wrong.
  Done when: one-tap "I'd use this first" answers reorder the rows, and the order is stored.

- **Run the plan through three counterfactual worlds** — FEATURE — value 3 — effort M — risk low — category: robustness — wild
  Why: wild: scenario planning (budget halved, a key dependency yanked, priorities shifted) and not a single pre-mortem. The plan reports which rows survive each world.
  Done when: each world produces a short survivor list, and a plan with one single-point-of-failure row names it.

- **Reconstruct the goal from the finished product** — FEATURE — value 3 — effort S — risk low — category: done-detection — wild
  Why: wild: a tool-less child sees only the finished README and CLI help and writes the goal it thinks was asked. Distance from the user's words measures scope drift.
  Done when: finish prints a two-sentence "what a stranger thinks this is" next to the user's sentence, flagged when a judge finds them far apart.

- **Pre-empt the product's likely first three bug reports** — FEATURE — value 3 — effort M — risk low — category: forecasting — wild
  Why: wild: forecast the first user complaints from rivals' public issue trackers and file a guard or test row for each before launch.
  Done when: finish lists three predicted reports, each with a test or an explicit "accepted risk", and none is blank.

- **Show a replayable proof of the user's own acceptance sentence** — FEATURE — value 4 — effort M — risk med — category: done-detection
  Why: the pack proposes tracing phrases and recording acceptance walks separately. Nothing stores the user's own sentence as the first oracle line, run first and never edited without a logged reason.
  Done when: the first oracle probe is the user's verbatim sentence expressed as a command, and editing it writes a reason line in the oracle edit log.

- **Fail a goal that lacks a no-install start** — FEATURE — value 2 — effort S — risk low — category: delivery
  Why: assumption: finished tools often require a long setup. Nothing checks that a goal's first-run path works from a bare clone in one command.
  Done when: a clean-clone run succeeds in one documented command, or the row stays red.

Next question: Which of these rows would the user have been surprised to find missing at their last finished goal, and is that list already in the dropped and reopened ledgers?
Next question: When a goal is "done" by quorum but the user reopens it within a week, which voter should have caught it, and is that recorded anywhere?
