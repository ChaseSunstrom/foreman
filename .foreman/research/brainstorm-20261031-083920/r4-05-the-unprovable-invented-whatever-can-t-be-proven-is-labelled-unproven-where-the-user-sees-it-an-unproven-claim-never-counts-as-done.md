# Brainstorm — lens: the unprovable (invented): whatever can't be proven is labelled unproven where the user sees it; an unproven claim never counts as done

- **Make "unproven" a typed state with a closed reason set** — FEATURE — value 5 — effort M — risk low — category: proof state
  Why: the rollup (T-2273) counts typed/inconclusive evidence, but reasons are free text. Prior ideas say "first-class state" without a schema. Reasons would be: no-command-possible, judge-same-house, environment-gap, expired, user-accepted, tool-missing. Each gets a fixed one-line remedy shown beside it.
  Done when: `fm task show` and the rollup print one of the six reason codes for every unproven row, and a row with a free-text-only reason fails `fm check`.

- **Gate goal finish on a ledger of unproven rows, with a user-only waive** — FEATURE — value 5 — effort M — risk med — category: done gate
  Why: the lens says an unproven claim never counts as done; today it is counted and listed, not blocking. Goal finish would refuse while any row is unproven and unwaived. The waive verb joins `USER_ONLY_FM` (T-2252), so the model can't write it. A waive records reason and expiry.
  Done when: `fm goal finish` exits non-zero naming the unproven row IDs, and succeeds after `fm waive T-NNNN --reason … --until …` run by the user; the same call from a session is refused by the guard.

- **Split "done" into proven-done and claimed-done in every count** — FIX — value 5 — effort S — risk low — category: honest counts
  Why: the "done" tallies on the site, status line and exam quotes likely merge the two (assumption: the counters don't split them). A bare "done: 212" overstates. Show "212 done, 171 proven, 41 unproven".
  Done when: every surface that prints a done count (CLI, pane, web UI, site stats) prints the proven/unproven split, checked by one test that greps each renderer's output.

- **Test that every renderer carries the unproven label** — CLEAN — value 4 — effort S — risk low — category: label coverage
  Why: the user wants the label "where the user sees it", and there are many surfaces (CLI, web UI, foreman-ui pane, finish receipt, commit trailer, site/genesis). One omission silently launders a claim. A single fixture task with unproven evidence is rendered through all of them.
  Done when: a test renders the fixture through each surface and fails if the string "unproven" and its reason code are absent from any.

- **Stamp unproven into the commit and the merge message** — FEATURE — value 4 — effort S — risk low — category: provenance
  Why: after a merge, the task record is no longer in view, but `git log` is. Assumption: commits now carry task IDs but not proof status. A trailer `Proof: unproven (judge-same-house)` travels with the code.
  Done when: `fm ship` writes a `Proof:` trailer on the merge commit, and `git log --format=%(trailers:key=Proof)` shows it for a task closed on typed evidence.

- **Decay typed evidence into a visible bet with an age** — FEATURE — value 4 — effort M — risk low — category: proof decay
  Why: the unproven rollup is a snapshot; old typed claims go stale unnoticed. Show the age ("bet, 41 days") and sort the oldest first, so the staleness is the cue to pay the debt.
  Done when: the rollup lists unproven rows ordered by age, with age in days, and a row older than a configurable limit appears in `fm doctor` as a warning.

- **One-command upgrade from unproven to proven** — FEATURE — value 4 — effort M — risk med — category: debt paydown
  Why: labelling without a path to fix it becomes a graveyard. For each reason code, `fm prove --upgrade T-NNNN` tries the matching proof kind (the migration, bench or UI flow already built) and flips the state only if the run records evidence.
  Done when: running the command on a task whose reason is tool-missing-but-now-installed turns it proven with recorded output; on a still-unprovable one it prints the unchanged reason and exits non-zero.

- **Flag a criterion that no command could falsify, at plan time** — FEATURE — value 4 — effort M — risk med — category: plan gate
  Why: the plan gate checks options and risks (T-2269, T-2285) but not whether each criterion has a falsifiable check. "Feels faster" or "reads well" gets caught only at close. Catch it at the plan and let the user choose a check or accept it as unproven then.
  Done when: `fm task new` with a criterion containing no verify command and no `unprovable:` marker is refused, and one with the marker is accepted and shows as unproven from the start.

- **Refuse to quote a number without its proven fraction** — FIX — value 4 — effort S — risk low — category: honest numbers
  Why: the exam scorecard, bench numbers and site stats are quoted bare. The earlier ideas ask for it in general; this is a mechanical check on the docs and site generators: a number from the exam or bench must have its denominator and proven share adjacent.
  Done when: the site build fails if a stats field lacks `proven_of` and `total`, and a doc line quoting an exam score without one fails `fm check`.

- **Wild: Turn each unproven row into a bet the user can place** — FEATURE — value 3 — effort M — risk low — category: delight, wild
  Why: assumption: users skim the list and ignore it. A one-key "I bet this holds / this breaks" on each row records a guess; when later evidence arrives, Foreman scores the user's calibration and shows how often their gut matched.
  Done when: `fm bet T-NNNN holds` records a bet, and a later proof or reopen of that task prints "bet won/lost" and updates a running tally in `fm status`.

- **Wild: Run a nightly lane that tries to prove the oldest unproven claim** — FEATURE — value 4 — effort L — risk med — category: agents, wild
  Why: the standing rules favour unattended work and the free arms; paying down debt overnight needs no user attention. A lane takes the oldest unproven row, attempts the upgrade, and posts only the rows that flipped or definitively can't.
  Done when: after a nightly run, `fm unproven` shows at least one row moved to proven with recorded output, or annotated "tried, cannot be proven: <reason>" with the attempt log.

- **Wild: Show a "debt weather" strip on the status line** — FEATURE — value 3 — effort S — risk low — category: ambient UI, wild
  Why: the user shouldn't have to run a command to feel the unproven share. A compact glyph and count ("proof ▂▃▅ 41 open, 3 stale") on the status line, coloured by age, makes drift visible at a glance.
  Done when: the status line shows the unproven count and the oldest age, and the figure matches `fm unproven --count` in a test.

- **Make the label survive a sub-agent's summary** — FIX — value 4 — effort M — risk med — category: laundering
  Why: assumption: a builder or lane reports "done, tests pass" in prose to the planner, and the unproven qualifier drops out between hops. The lens needs a path from the evidence record to the user's eyes that the model's wording can't edit.
  Done when: a lane's brief and merge report are generated from the evidence record, and a test with a lane that closes on typed evidence shows the planner-facing summary containing the reason code verbatim.

Next question: Which surfaces where the user reads "done" are written by a model's prose rather than rendered from the evidence record, and can any of them be switched to render from the record?

Next question: When the user accepts a claim as unproven, what would make them revisit it, and does anything currently bring it back?
