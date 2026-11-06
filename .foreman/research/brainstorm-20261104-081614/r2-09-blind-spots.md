# Brainstorm — lens: blind spots

- **Mine co-change companions for every diff** — FEATURE — value 5 — effort M — risk low — category: change impact
  Why: T-2960 (site test must name `--planner`), the shim plus MASTER bullet asks for `sampo.smallcards` and `sampo.regen`, and the Domain wording fix are all files a change implied that nobody listed. Question missed: "what always changes alongside this?" Project-agnostic: learn from each repo's git history and closed briefs, with no weights needed at first.
  Done when: replaying 20 past commits that later drew a follow-up fix, the companion list names the missed file in at least half of them.

- **Turn each late ask into a standing class lint** — FEATURE — value 5 — effort M — risk low — category: blind spots
  Why: the pack's "missed asks" are instances of classes: serial calls, doc drift, literal paths, silent cuts, nulls, missing shims. Each class is checked once, then never again. Tag each ask by class and store the class question as a check that `sampo doctor` runs on the whole repo.
  Done when: a seeded violation of each of 5 classes in a scratch repo is reported by name, and a new late ask adds a class row.

- **Meter endpoint slot use** — PERFORMANCE — value 4 — effort S — risk low — category: observability
  Why: the kill stage (T-2953) and tier stage (T-2959) both judged one batch at a time while the endpoint serves 2. Question: "which model-call loop has fewer calls in flight than slots?" Log in-flight against slots per profile and flag a stage that sat under half for over 5 minutes.
  Done when: a serial loop over an endpoint with 2 slots prints "1 of 2 slots used" in `sampo doctor`, and the parallel version doesn't.

- **Canonicalise old names in the corpus** — FIX — value 4 — effort S — risk low — category: training data
  Why: 1,767 briefs predate the rename, so they say `fm`, Foreman and `~/.claude/foreman`. A decider trained on them will propose dead verbs. Map aliases to canonical names at export and drop rows whose verbs no longer exist.
  Done when: the exported table has zero tokens from the alias list outside a quoted-history field, and a verify-command head never suggests a missing verb.

- **Relocate model state with the home** — FIX — value 4 — effort S — risk med — category: migration
  Why: T-2967 showed `sampo migrate` turns the old home into a symlink and literal-path code breaks. Model registry entries, manifests and adapter paths are the next literal-path users. Store them relative to the home and resolve through realpath.
  Done when: after a scratch `sampo migrate` and `--undo`, every registered model resolves and loads, and the test fails if one stores an absolute path.

- **Run the ship gate without a GPU or endpoint** — FIX — value 4 — effort M — risk low — category: reliability
  Why: ship's scratch-tree suite already failed on unrelated site tests, and the standing rule is that Sampo works without claude on PATH. Model code must pass the full suite against a recorded-response fake endpoint, with no Ollama running.
  Done when: the suite is green on a machine with Ollama stopped and the network blocked, and a model test that dials out fails.

- **Probe each model's quirks at install** — FEATURE — value 4 — effort M — risk low — category: serving
  Why: `think:false` did not reach Ollama, and gemma4 kept reasoning until it ran out of budget. Send a canary prompt per profile that checks reasoning off, JSON obedience, context really honoured and stop behaviour, and store a quirks row.
  Done when: a profile that ignores reasoning-off is marked "quirk: reasons" before first use, and Smith raises its budget or refuses the slot.

- **Show training rows that can't be reproduced** — CLEAN — value 3 — effort S — risk low — category: data integrity
  Why: unrated nulls crashed the site build, and the sensitive-path exclusion needed real paths. Add a dry-run exporter that reports row counts dropped per reason, such as null, excluded, alias and truncated, so no filter is silent.
  Done when: export prints a drop table summing to input minus output, and a row with a null field is counted rather than crashing.

- **Review shipped surfaces after a model-facing change** — FEATURE — value 3 — effort M — risk low — category: docs and UI
  Why: T-2964's cold review found layout and contrast misses after shipping. When a model slot's UI card or the Code page changes, render at 390, 768 and 1440 and run the cold review before the close.
  Done when: a seeded overflow on the model card at 390px fails the close with a screenshot path.

- **Wild: Fuzz the rename as a distribution shift** — FEATURE — value 3 — effort M — risk low — category: robustness (wild)
  Why: Foreman to Sampo changed every noun the deciders see. Treat before and after the rename as a natural split, train on one side, test on the other, and use the gap as a genericity score for projects with different vocabularies.
  Done when: the scorecard prints a pre/post-rename accuracy gap, and an adoption card fails above a set threshold.

- **Wild: Pre-mortem head that predicts the next three asks** — FEATURE — value 4 — effort L — risk med — category: foresight (wild)
  Why: the user's late asks follow closes in a pattern (docs, shim, tests, site). Train on close-to-next-ask sequences across the 13 projects and file the likely follow-ups as drafts, named as predictions, when a task closes.
  Done when: on held-out projects, at least 30% of drafted follow-ups match a task the user later filed.

- **Wild: Dual-environment twin run** — SECURITY — value 3 — effort S — risk low — category: aliases (wild)
  Why: T-2967 and the mirrored-env pop show old and new names diverge in guards. Run every model path under `SAMPO_*`, `FOREMAN_*` and both set, and compare the Ward verdicts and model choices.
  Done when: a seeded divergence, such as the guard refusing one name only, fails the twin run with the differing keys listed.

Next question: Which model decision is made from text a repo or tool wrote rather than the user, and can that text change the outcome without a ledger trace?
Next question: What would a user who never read MASTER.md need to see in order to know which slot is model-driven and how to turn it off?
