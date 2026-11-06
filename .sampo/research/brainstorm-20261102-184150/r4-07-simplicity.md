# Brainstorm — lens: simplicity

- **Fold the Exam into the Done-when line** — CLEAN — value 4 — effort S — risk low — category: briefs
  Why: the carried gap adds a second section (Exam: outcome plus live reading) beside Done-when. The pack already has Done-when as one testable check. Assumption: a Done-when command that prints one number can serve as both the live reading and the outcome measure.
  Done when: `fm genesis check` rejects a brief with a separate Exam block, and a brief whose Done-when command prints no number fails with a message naming what to add.

- **Exempt S-sized FIXes from the Exam requirement** — CLEAN — value 4 — effort S — risk low — category: ceremony
  Why: the recent tasks (T-2731, T-2735, T-2738) are small fixes whose red-first test already is the outcome. Demanding an outcome measure for each adds ceremony with no new signal. Assumption: S FIXes make up most of the filed briefs.
  Done when: a FIX/S brief with no Exam passes filing, an L FEATURE without one is refused, and a test pins both cases.

- **Allow one dissent per Mission, the one with the most lens disagreement** — CLEAN — value 3 — effort S — risk low — category: dissent
  Why: "dissents scored against outcomes" is a carried gap, and scoring many dissents needs many readings. One pick is cheaper to score and to read. Assumption: the strongest disagreement is the most informative to score.
  Done when: a Mission file with two dissent sections fails `fm genesis check`, and the kept one names the lenses that disagreed.

- **Hand-run every new gap rule once before automating it** — CLEAN — value 3 — effort S — risk low — category: process
  Why: the pack lists dozens of automated checks for gaps, several of which have already been dropped as vacuous or duplicate. A rule run by hand on one real brief shows whether its output is readable. Assumption: a hand run costs less than a drop and refile.
  Done when: a rule's task Done-when must quote one real brief's hand-run output, and `fm task finish` refuses without it.

- **Add a sunset test to each new Exam field** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: the standing lean rule says growth with no measurement waits. If the live reading never differs between the parent commit and the fix, the field adds nothing. Assumption: briefs record both readings cheaply.
  Done when: after 10 briefs close, `fm outcomes` prints one line, "Exam live reading differed on N of 10", and a field with N=0 files a removal task.

- **Make the Mission page a single list: briefs, then one "Left out" line** — CLEAN — value 4 — effort M — risk low — category: legibility
  Why: the grid, banner, slip, register and manifest ideas each add an artifact. The user's actual asks are "file the Mission with its briefs". Assumption: the grid is scaffolding for the planner, not something the user reads.
  Done when: a Mission file is at most 1 screen of briefs plus one left-out line, and the grid is kept only in the child's output and never written to disk.

- **Skip canaries on "already built" claims** — PERFORMANCE — value 2 — effort S — risk low — category: grounding
  Why: a false "not built" wastes a brief, but a false "built" costs only a missed idea, and the user can re-ask. Canary effort belongs on negative claims. Assumption: asymmetric costs, shown by the drops in the pack.
  Done when: the canary runs only for briefs whose text says "not built" or "missing", and a test shows a positive-claim brief files with zero canary calls.

- **Pin the Exam format for gen 4 and add nothing for two Missions** — CLEAN — value 3 — effort S — risk low — category: restraint
  Why: Missions keep adding fields (receipts, manifests, hashes, versions), and the lean rule says growth needs measurement. Assumption: two Missions are enough to see whether the current format is used.
  Done when: a test fails if the Exam template differs from its gen-4 hash before the gen-5 seed exists.

- **Use the user's one close-time answer as the dissent score (wild)** — FEATURE — value 3 — effort S — risk med — category: dissent
  Why: automatic dissent scoring needs outcomes that may not exist yet, but the user reads the close card anyway. One keystroke ("a dissent was right: y/n/none") costs seconds. Assumption: the user will answer it.
  Done when: the Mission close card asks one question, the answer is stored with the dissent, and a skipped answer is recorded as "unscored", never as a miss.

- **Try the Mission with no grid at all and compare left-outs (wild)** — PERFORMANCE — value 3 — effort M — risk low — category: experiment
  Why: nothing in the pack shows the grid finds more gaps than a plain "what did you leave out?" question. Assumption: it might not.
  Done when: one Mission is run both ways on the same request, and the two left-out lists are recorded side by side with the extra items named, one line each.

- **Print the exhaustiveness claim as a number, or nothing (wild)** — CLEAN — value 2 — effort S — risk low — category: honesty
  Why: "covers the whole space" is the request's own word, but a prose claim can't be wrong. A number can: "7 of 9 cells examined, 2 left out". Assumption: the grid has a countable cell set.
  Done when: the Mission page's first line holds "N of M" and a test rejects the words "exhaustive" or "complete" without it.

- **Delete a dead lens from the next Mission's fan-out (wild)** — CLEAN — value 2 — effort S — risk low — category: lean
  Why: the pack has no `lens_rates` use yet (T-0829 deferred), and every lens costs a child call. Assumption: some lenses return almost no new ideas.
  Done when: the Mission records ideas-per-lens, and a lens with 0 accepted briefs in two Missions is dropped from the default list with the reason recorded.

Next question: which of the carried gaps does the user actually read on a finished Mission page, and which are only for cold readers?
Next question: if the Exam were removed from every brief for one Mission, would any later correction have been caught only by it?
