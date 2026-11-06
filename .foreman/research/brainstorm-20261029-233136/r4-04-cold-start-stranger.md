# Brainstorm — lens: cold-start stranger

- **Read the dirty tree as the unspoken request** — FEATURE — value 5 — effort S — risk low — category: intent
  Why: assumption: when the user types nothing in a stranger repo, the branch name, uncommitted diff, stash, last-touched files and TODOs added this week are the only evidence of what they're doing, and the pack's ideas read none of them.
  Done when: on a fixture with a half-finished diff on branch `fix-pagination`, the self-written gen-0 names pagination as the first Mission and cites the diff.

- **Vet discovered gate commands before their first run** — SECURITY — value 5 — effort M — risk low — category: trust
  Why: "discover the gates by running them" executes a stranger's Makefile, `postinstall`, `conftest.py` and git hooks. Nothing in the pack reads those first.
  Done when: a fixture whose `package.json` postinstall curls a URL gets that script shown and skipped, and a one-word yes is needed to run it.

- **Quarantine a tower the machine didn't write** — SECURITY — value 4 — effort S — risk low — category: provenance
  Why: assumption: a cloned repo can ship its own committed gen-0, `not-yet.md`, or a standing-grant file. Resuming it would import another author's MUSTs and grants.
  Done when: a fixture with a committed tower is opened read-only as evidence, nothing in it resumes or publishes, and `status` says "foreign tower".

- **Bootstrap from zero in a throwaway clone and file each break as a gap** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: the pack covers a README-only reader and a smoke tour of the running product. It doesn't cover a fresh clone followed step by step, where setup failures are the first thing a real newcomer hits.
  Done when: on a fixture with a stale `README` install step, the run logs the failing command and its output as a coverage-grid entry.

- **Quiz the recon with a tool-less reader** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: "scale recon to repo size" sets a reading budget but never checks that the recon understood the repo. Generated questions (entry point, how to test, what the data model is) give an answer key.
  Done when: a reader given only the recon summary answers 8 of 8 generated questions on a fixture. A summary that fails 3 or more triggers one deeper recon pass.

- **Build a danger map from reverts and hotfixes** — FEATURE — value 4 — effort S — risk low — category: caution
  Why: the pack mints exam scenarios from fix and revert commits. A stranger's first edits also need to know which files have burned people, as a guard hint and not only as tests.
  Done when: a fixture file reverted 3 times shows a caution note and requires its test before edit, and an untouched file does not.

- **Separate the user's code from inherited code by blame** — FEATURE — value 3 — effort S — risk low — category: attribution
  Why: assumption: in a stranger repo the user may be one contributor in fifty. Their history applies to their own files, and for the rest Genesis should follow the repo's conventions.
  Done when: gen-0 style rules cite blame share, and a file with under 10% user lines gets the repo-wide convention.

- **Learn commit and PR house style from history** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: assumption: Genesis's first commits and PR text will read as foreign unless it samples the last 50 merged messages (prefix, tense, ticket ids, length).
  Done when: a generated commit on a fixture using `feat(scope):` matches that pattern, and the pattern is shown in the postcard.

- **Mine absence statistics for soft NEVERs** — FEATURE — value 3 — effort M — risk med — category: conventions
  Why: tagging inferred rules by source is covered. What's missing is deriving them from what never appears (no new dependency in 3 years, no file over 400 lines, no `print`). Each is stored with its prevalence and flagged "soft".
  Done when: a fixture with zero `TODO`s over 200 commits yields a soft rule with "0/214 files", and one counterexample is tolerated while three retire it.

- **Deliver the question card with no terminal** — FEATURE — value 2 — effort S — risk low — category: devices
  Why: assumption: the one skippable question can't render under SSH batch, CI or a scheduled auto-start.
  Done when: with no TTY the card is written to a file and a notification, and the run proceeds on defaults after a timeout.

- **Wild: Measure what memory buys by ablation** — FEATURE — value 4 — effort M — risk low — category: evaluation
  Why: wild. The user's lens asks what the cold start "gets wrong without memory". Run gen-0 on the same repo with the user's history hidden and with it shown, then grade both on the same held-out exam and report the delta.
  Done when: one report shows the closed-scenario gap and the three MUSTs that only the history run wrote.

- **Wild: Cold-start roulette on fresh open-source repos** — FEATURE — value 4 — effort L — risk med — category: generalization
  Why: wild. Ten fixed stranger fixtures can be overfit by Genesis's own templates. Each week, clone one unseen small permissively licensed repo in a sandbox with the network used only for the clone, run the cold start, and score it.
  Done when: a weekly entry in the exam log scores gen-0 coverage on a repo never used before.

- **Wild: Write a library card on the fly for an unknown stack** — FEATURE — value 3 — effort L — risk med — category: unfamiliar stacks
  Why: wild. The card list in the map has python, tailwind and a few others. For a stack with no card, a child writes one from the repo's lockfile and docs, and it counts only if its hello-world snippet builds.
  Done when: on a fixture in a language with no card, a generated card exists, its snippet compiles, and gen-0 cites it.

- **Report the share of the repo recon couldn't explain** — FEATURE — value 3 — effort S — risk low — category: confidence
  Why: assumption: abstaining when the kind is unclear is covered, but not a number for how much of the tree has no attributed purpose. That number tells the user whether to trust a one-line "make this great".
  Done when: the postcard shows "explained: 84% of files", and under 60% the run asks before the tower starts.

Next question: What does Genesis do when the stranger repo's own gates are red or absent at the start, so there is no baseline to close gaps against?
Next question: Which of the user's history signals are safe to carry into a repo owned by someone else, and who decides at the moment of the first run?
