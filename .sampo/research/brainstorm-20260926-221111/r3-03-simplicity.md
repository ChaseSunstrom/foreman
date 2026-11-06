# Brainstorm — lens: simplicity

- **Report every unmet done-requirement in one pass** — FEATURE — value 4 — effort S — risk low
  Why: `fm task done` checks evidence, audits, docs, lesson, red→green, scope drift, behaviour lock, perf numbers. If it stops at the first failure, each retry costs a turn and tokens. Assumption: it currently reports the first failure.
  Done when: a brief missing three requirements gets one `fm task done` call that lists all three with their fix commands, and a test asserts the list is complete.

- **Add `fm task done --fix` for mechanical gaps** — FEATURE — value 3 — effort M — risk med
  Why: some unmet gates need no judgement: refreshing a stale self-audit, recording Files touched, writing the Docs impact "none" line when no docs changed. Assumption: these are currently done by hand.
  Done when: on a fixture with only mechanical gaps, `--fix` completes the task in one call. On a fixture with a judgement gap (missing lesson), it does not complete and names that gap.

- **Compute a mechanical simplicity delta at done** — FEATURE — value 4 — effort M — risk low
  Why: the "net-complexity line" on FEATURE tasks is self-reported prose. A stdlib `ast` diff can report lines added minus removed, new public symbols, new files, and symbols the change left unreferenced (orphans).
  Done when: a fixture diff that removes the last caller of a helper makes done print "orphaned: helper", and a CLEAN task with net-positive complexity gets a warning.

- **Flag non-functional churn in the diff** — CLEAN — value 3 — effort S — risk low
  Why: scope drift only checks files, not hunks. Whitespace-only, import-reorder and rename-only hunks inflate audit and review reads. Assumption: no hunk-level classifier exists yet.
  Done when: a diff with a reformatted, otherwise untouched function prints "churn: N lines in FILE not tied to a step". A test covers whitespace-only, import-only and real hunks.

- **Keep a gate-yield ledger and demote gates that never catch anything** — CLEAN — value 4 — effort M — risk med
  Why: Foreman has many gates and none records whether it changed an outcome. Existing pruning covers commands, notes and lessons, not gates. Yield means the gate blocked and the block led to a real fix.
  Done when: `fm doctor` lists per-gate fires and fixes-after-fire. A gate with zero fixes over 30 finished tasks is proposed for demotion to a warning, and demotion needs one yes.

- **Add one-call task abandon and restart** — FEATURE — value 3 — effort S — risk med
  Why: the state machine is strict (one active task, focus gates, done gates). The pack shows no escape hatch for a wrong plan or a request the user withdrew. Assumption: none exists. Without one, the model improvises multi-command state surgery.
  Done when: `fm task drop ID --to inbox|cancelled` restores the focus checkpoint and clears the active task. The request text goes back to the inbox or is archived, and the fuzz invariants still hold.

- **Distill lessons into a bounded per-project handbook** — CLEAN — value 3 — effort M — risk low
  Why: lessons are required for every M/L task, so recall keeps accumulating overlapping entries. Hit counts and retirement thin them but never merge. Merging lessons that share a scope glob into one line keeps SessionStart and recall injections small.
  Done when: `fm tidy` merges lessons with overlapping scope into a handbook of ≤10 lines per project. Each line keeps its source lesson IDs, and recall on a fixture returns the handbook line, not the duplicates.

- **Lint plan shape at focus** — CLEAN — value 2 — effort S — risk low
  Why: `fm focus` checks that a brief is planned for its tier, not whether the plan is simple. Steps beyond a tier cap or without an observable result each need their own evidence later.
  Done when: focusing an S brief with 5 steps, or a step with no verifiable outcome, prints one note suggesting a split or a tier change. It never blocks.
