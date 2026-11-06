# Brainstorm — lens: the unprovable (invented): whatever can't be proven is labelled unproven where the user sees it; an unproven claim never counts as done

- **Make "unproven" a closing state that blocks `done`** — FEATURE — value 5 — effort M — risk med — category: task state
  Why: T-2273 counts and lists unproven tasks, but the pack shows "done" still being granted. Assumption: a done task can still rest on typed or inconclusive evidence.
  Done when: `fm task finish` on a task whose only evidence is typed ends in state `unproven`, not `done`, and a goal's finish check lists it as an open row.

- **Add a claim ledger that grades every claim in the final answer** — FEATURE — value 5 — effort M — risk med — category: claims
  Why: assumption: the closing prose can assert things (speed, "all callers updated") that no evidence row covers; the rollup only counts tasks, not sentences.
  Done when: a finish on a planted answer with one uncovered claim prints that claim line tagged `UNPROVEN: no evidence row`.

- **Stamp each evidence line with who could have lied** — FEATURE — value 4 — effort S — risk low — category: evidence
  Why: the questions left ask which verbs have a model on both sides with no user-owned check. Witness classes (ran command / model-judged / typed / user-owned check) make that visible.
  Done when: every evidence line in `fm task show` carries one of four witness tags, and a test fails on an untagged line.

- **Carry the unproven label through every renderer** — FIX — value 4 — effort M — risk low — category: consistency
  Why: the rollup is promised "on every surface" (terminal, web UI, site, commit, finish receipt). Assumption: at least one renderer still drops it.
  Done when: a test seeds one unproven task and greps CLI, web UI JSON, site data and receipt output, and all show the label.

- **Gate quoted numbers on their proven fraction** — FIX — value 4 — effort S — risk low — category: numbers
  Why: the questions left ask which numbers were never checked by anyone but their producer. Exam, bench and site stats appear bare.
  Done when: `fm exam scorecard` and the site stats print "N of M proven" beside each figure, and a figure with no producing command prints "unproven".

- **Add a user-only "accept as unproven" verb with a reason and expiry** — FEATURE — value 4 — effort S — risk low — category: user control
  Why: the guard already reserves `fm mandate set` for the user (T-2252). Some things truly can't be proven, and a recorded, dated acceptance beats a silent pass.
  Done when: the model cannot run the verb (guard refuses), the user can, and the task shows "accepted unproven: <reason>, expires <date>" in the rollup.

- **Decay typed evidence into a visible bet with an age** — FEATURE — value 3 — effort M — risk low — category: proof decay
  Why: assumption: old typed claims are trusted as much as new ones. Age shown beside the label tells the user what to re-check first.
  Done when: the rollup lists unproven items oldest first with an age column, and one command re-runs a proof to upgrade it.

- **Offer a one-command upgrade from unproven to proven** — FEATURE — value 4 — effort M — risk med — category: proof upgrade
  Why: labelling without a path forward becomes noise. Assumption: each unproven reason maps to a missing proof kind (shot, bench, migration, docs run).
  Done when: each rollup row prints the exact `fm …` command that would prove it, and running it moves the row out of the rollup.

- **Flag a criterion that no command could falsify, at plan time** — FEATURE — value 4 — effort M — risk med — category: plan gate
  Why: T-2269-style plan gates check content by tier but not testability. Declaring "unprovable on purpose" up front prevents late surprise.
  Done when: a plan with the criterion "feels fast" is refused until it gets a measurable check or an explicit unprovable tag.

- **Test that the rollup itself doesn't undercount** — FIX — value 4 — effort S — risk low — category: self-check
  Why: the rollup determines UI changes by "no visual check", which is a heuristic; the rollup is itself a number nobody else verified.
  Done when: a fixture repo with five planted unproven tasks (typed, inconclusive, UI-no-shot, perf-no-bench, docs-no-run) yields a count of exactly five.

- **Wild: Hold a nightly "unproven court"** — FEATURE — value 3 — effort M — risk med — category: unproven queue
  Why: wild. Each night the oldest unproven claim becomes a task, and a cold different-house model tries to prove or refute it; only the diff is posted.
  Done when: the next morning's report lists one claim as proven, refuted or still unproven, with the command that decided it.

- **Wild: Publish an "unproven ledger" beside the exam scores on the site** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: wild. The site's stats already refresh daily (T-2326); showing Foreman's own unproven fraction makes honesty the brand.
  Done when: the Genesis page shows the unproven count, its age histogram and the last refresh time, from generated data.

- **Wild: Let a green wobble until a saboteur fails to break it** — FEATURE — value 3 — effort L — risk med — category: mutation
  Why: wild. A saboteur lane mutates the fix; a proof that stays green under mutation is flagged "could not have failed" and counts as unproven.
  Done when: a planted vacuous test is reported as unproven with the mutation that survived.

- **Wild: Show a confidence-weather strip on the status line** — FEATURE — value 2 — effort S — risk low — category: status line
  Why: wild. One glyph run (proven / bet / unproven share) in the pane so the user feels the repo's proof level without opening a report.
  Done when: the status line renders the three shares and updates after a task closes.

Next question: What does the user do with a rollup row today — does any session path read it, or is it a list nobody is made to act on?
Next question: Which of Foreman's own claims in the README and site (hook latency, held rate) have no producing command at all?
