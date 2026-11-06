# Brainstorm — lens: self-modification: every self-change gated by bench and trials, scored afterwards and reverted when it made things worse

- **Bind every self-change to a signed change manifest** — FEATURE — value 5 — effort M — risk low — category: self-change ledger
  Why: T-2272/T-2276/T-2291/T-2281 each change behaviour, but the pack shows no single record linking change → predicted effect → bench/trial result → verdict. Prior ideas ("ledger with verdicts", "prediction before change") are separate; this makes the manifest the unit that every gate, score and revert reads, and unmanifested edits to routers, triggers, rules or thresholds fail `fm check`.
  Done when: a commit touching a self-modifiable surface without a manifest (id, prediction, bench cmd, revert recipe) fails `fm ship` in a test.

- **Generate the revert at change time and test it** — FEATURE — value 5 — effort M — risk med — category: rollback
  Why: "Auto-revert" ideas assume a revert works. A self-change that also migrated learned state (router history, trigger precision) may not revert cleanly. assumption: some self-changes write state that `git revert` doesn't undo.
  Done when: for each manifest, a test applies the change, then the stored revert recipe, and the tree plus state files hash-equal the pre-change snapshot.

- **Score survival by counterfactual, not by calendar** — FEATURE — value 5 — effort L — risk med — category: scoring
  Why: A "day 7 score" mixes the change with the week's workload. Replay the same recorded week of hook inputs and lane outcomes through old and new builds and compare; this uses the user's own stream, which Foreman didn't author.
  Done when: `fm selfchange score ID` prints old-vs-new on an identical replayed input set, and a planted harmful change shows as worse.

- **Split trials into a sealed set the changer cannot read** — SECURITY — value 5 — effort M — risk low — category: anti-gaming
  Why: Standing rule says weakness-finding uses signals Foreman didn't author; the self-fixer that writes the fix and its test can overfit. assumption: trials currently live in the repo the fixer edits.
  Done when: a self-change lane's worktree contains no sealed trial files, and a test shows a lane reading the sealed path is refused by the guard.

- **Reserve a protected core self-changes cannot touch** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: Steer: "keeps the guard intact". Mission 8 #12 requires it; the pack shows the guard changed by the user's own commands (T-2252). Make a path list (guard, hooks, bench, trials, the revert machinery, the manifest checker) that auto-lanes cannot modify, enforced by diff.
  Done when: a self-change diff touching any protected path is rejected with the path named, tested with a planted diff.

- **Score the scorer: plant known-bad changes weekly** — FIX — value 4 — effort M — risk low — category: checker validity
  Why: Questions earlier brainstorms left: "numbers never checked by someone other than the code that produced them". If bench can't flag a planted regression (slower hook, dropped check), its pass means nothing.
  Done when: `fm doctor` reports "canary regressions caught n/n", and a canary that slips through turns it red.

- **Attribute regressions to the change that most plausibly caused them** — FEATURE — value 4 — effort L — risk med — category: bisect
  Why: With several self-changes in a day, a red metric doesn't say which to revert. Merge-order bisect exists for lanes (earlier idea) but not for self-changes against drifted metrics. Revert the smallest suspect set that restores the baseline.
  Done when: with 3 stacked manifests, one planted harmful, `fm selfchange bisect` names it in a test and reverts only it.

- **Treat user corrections as the final verdict on a change** — FEATURE — value 4 — effort M — risk low — category: feedback
  Why: The user's "asked" stream shows corrections ("Plan gate misses an option…"). A correction landing within a window in the area a self-change touched should lower its verdict and open a revert candidate, ahead of any bench number.
  Done when: a recorded correction citing a verb touched by manifest M within 14 days flips M to "contested" in the ledger.

- **Budget self-change per surface, spending by trust earned** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: Routers, triggers and thresholds are low-risk; plan gates and hooks are high. Each surface starts at "propose only", moves to "auto-land" after N held changes, drops back after one revert.
  Done when: a surface with one revert in its window cannot auto-land the next change, shown by test.

- **Wild: Mutation night for the self-improver** — FEATURE — value 4 — effort M — risk low — category: red team
  Why (wild): Break gates, bench and revert on purpose in a throwaway clone and check the improver notices; if it lands a change that a broken gate passed, that gap becomes a task.
  Done when: a nightly run reports mutations caught/total and files a FIX for each survivor.

- **Wild: Run the old build against the new failure** — FEATURE — value 4 — effort M — risk low — category: proof
  Why (wild): A self-fix is only proven if the previous build fails on the replayed signature and the new one passes. Store the pair as the change's receipt.
  Done when: each FIX manifest holds an old-red, new-green replay, and a no-op "fix" is refused.

- **Wild: A one-key undo window with a plain-language receipt** — FEATURE — value 3 — effort S — risk low — category: user control
  Why (wild): The user steers constantly and wants control without reading diffs. After any auto-landed change, one line: "changed X because Y; `fm undo` within 48h".
  Done when: `fm undo` restores the pre-change tree and state in a test, and the notice appears on the next prompt.

- **Quarantine changes that need a fix-of-fix** — FEATURE — value 4 — effort S — risk low — category: churn
  Why: A change followed by a second change in the same area within a short window signals a bad first fix; freeze that class to propose-only.
  Done when: two manifests on one surface within 7 days set the surface to propose-only in a test.

Next question: Which self-modifiable surfaces write learned state (router history, trigger precision, predictions) that a code revert alone can't undo, and who verifies that state after a revert?
Next question: What is the smallest sample of recorded hook inputs and lane outcomes on which an old-vs-new replay can tell a real regression from noise?
