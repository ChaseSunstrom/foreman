# Brainstorm — lens: blind spots

- **Bind every consent to a channel the model can't write** — SECURITY — value 5 — effort M — risk med — category: consent
  Why: T-2202 had to be asked for: `fm prove` could run a tree's tests on consent the model could forge. The question missed was "which verb executes, spends or publishes, and who can say yes?" The same class holds `fm scout --slow`, the standing-grant publish to main and `fm genesis live`.
  Done when: a test feeds each consent-bearing verb a model-authored flag, env var, file or prompt text that claims consent, and every one refuses and logs why.

- **List standing grants with scope, expiry and last use** — SECURITY — value 4 — effort S — risk low — category: grants
  Why: the genesis publish grant is "standing" and debounced, and approval in one context shouldn't carry to the next. Assumption: grants live in scattered places with no single view.
  Done when: `fm grants` prints each grant with its scope, who gave it, expiry and last use, and `fm doctor` flags any grant with no expiry or one unused for 30 days.

- **Simulate every feedback gate for convergence** — FIX — value 5 — effort M — risk low — category: gate loops
  Why: T-2206, T-2228, T-2229 and T-2231 are four successive repairs to the cold-read gate in `fm genesis put`, which deadlocked on previous-reads, stale quotes and wrapped lines. The question missed was "can this gate loop forever, and does its feedback shrink?"
  Done when: a scripted reader that gives contradictory, stale or unquotable findings makes `put` end in at most N rounds with a named verdict (pass, stuck or needs-user), never a silent deadlock.

- **Anchor each cold-read finding to a content hash** — FEATURE — value 4 — effort M — risk med — category: findings
  Why: T-2228 treats a quote of a changed line as resolved, T-2205 keeps previous-reads on purpose, and T-2229 prints stray quotes. These are ad hoc rules for a missing finding lifecycle.
  Done when: findings are objects with states open, resolved, stale or disputed, tied to the hash of the line quoted, and a rewrite moves them through states in a unit test.

- **Fuzz every prose-parsed file for wrap points** — FIX — value 4 — effort M — risk low — category: parsers
  Why: T-2213 (`step` read only the first line of a wrapped Task: paragraph) and T-2231 (a wrapped paragraph is one logical line) are the same defect found twice. Missions, lineage, the coverage grid and goal files are all read by line-based parsers.
  Done when: a property test re-wraps every fixture at random widths and each parser returns the same result, run over every file kind the tower and `fm goal` read.

- **Refuse comparisons across unequal denominators** — FIX — value 4 — effort S — risk low — category: metrics
  Why: T-2219 shows the scorecard comparing 30/36 against a 1-scenario line shown as 1/36. The question missed was "which number sits beside another measured on a different base?"
  Done when: the scorecard and `fm outcomes` print n/m for each figure and show "not comparable (n=1 vs 36)" instead of a gap whenever the bases differ.

- **Keep a manifest of artifacts each Mission owes** — FEATURE — value 4 — effort M — risk low — category: completeness
  Why: T-2221 had to be asked for: Mission 3's critique file was never filed, and nothing noticed. This is the same class as "knows when it's done".
  Done when: each Mission lists its owed files (critique, receipt, exam line) in a manifest, `fm genesis step` and `check` name any missing one, and deleting a critique makes the Mission not-done.

- **Require a judge's quote in every model verdict that fails something** — CLEAN — value 3 — effort S — risk low — category: judges
  Why: T-2229 exists because a FAIL naming no line hid what the reader said. Assumption: other model-judged gates (drift, sweep, exam grading) can do the same.
  Done when: a lint finds any judge-backed failure path that prints no quote and no judged object, and none remain.

- **Log each "blind" user ask and its missing question** — FEATURE — value 4 — effort M — risk low — category: meta-loop
  Why: the "missed" list holds eight asks, all caught by hand. Assumption: the class question for each was written by a person, not filed automatically.
  Done when: an intake that matches no idea, goal row or open task gets a `blind` tag and a one-line "question that would have caught it", and the next brainstorm's pack reads that file.

- **Run tower tooling on a hostile synthetic tower** — FIX — value 3 — effort M — risk low — category: dogfood
  Why: the tools are exercised mostly on Foreman's own tower, and the findings (T-2213, T-2231) were shape problems that tower happened to expose. Assumption: other users' files wrap, quote and number differently.
  Done when: a fixture tower with odd wraps, Unicode, CRLF and nested lists passes `step`, `check`, `put` and `sweep` in CI.

- **Wild: Hire a consent forger** — SECURITY — value 4 — effort M — risk med — category: red team
  Why: wild. A child whose only task is to get `prove`, publish or a scout commit through without the user's yes, and every success files a T-2202-class bug.
  Done when: the forger runs in CI against stub verbs, and a planted forgeable consent is caught within its budget.

- **Wild: Fuzz the gates with an ugly scribe** — FIX — value 3 — effort M — risk low — category: adversarial
  Why: wild. An agent rewrites tower files with moved quotes, odd wrapping and re-ordered rows to deadlock `put`, then reports the shortest input that does.
  Done when: it finds the known T-2228 and T-2231 deadlocks on a build with those fixes reverted.

- **Wild: Publish a denominator page** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: wild. Every number the pane, site and scorecard show links to its n, its base and what it was compared with.
  Done when: clicking any site figure on the Genesis page opens its base and sample size.

- **Wild: Predict the user's next five asks and score the guesses** — FEATURE — value 3 — effort S — risk low — category: foresight
  Why: wild. A weekly brainstorm seals five predicted asks and later scores them against the real queue, giving a measurable blind-spot rate.
  Done when: a sealed prediction file exists with a hit rate computed from later intakes.

Next question: Which Foreman verbs have a model on both sides (writer and judge) with no user-owned check between them?
Next question: Which numbers or files does Foreman show the user that have never been checked by someone other than the code that produced them?
