# Brainstorm — lens: blind spots

- **Count every silent cut in the training pipeline** — FIX — value 5 — effort S — risk low — category: data integrity
  Why: T-2912 found foresight.py cutting an ask's files at 4 and the standing rules at 10 without saying so. A trainer that truncates briefs, ledger lines or journals would do the same and nobody would see it. Question to have asked: "what does this stage drop without saying?"
  Done when: building a dataset prints a per-field count of rows and characters cut, and the existing silent-cut scan fails on any new cut that isn't reported.

- **Prove every model setting reached the endpoint** — FIX — value 5 — effort S — risk low — category: serving
  Why: `think: false` never reached Ollama, so gemma4:12b ran out of budget on 7 of 10 exam scenarios. This was found by hand. Question: "did the knob we set change the request that was actually served?"
  Done when: a canary call per profile checks reasoning, context size and slot count against observed behaviour, and `sampo doctor` names any profile where a setting is a no-op.

- **Hold out whole projects and scan for leakage** — SECURITY — value 5 — effort M — risk med — category: generality
  Why: T-2973 asks for a model that works beyond the Sampo repo. The pack has 13 projects, and Sampo itself is 1,767 of the 4,078 briefs, so a random split would mostly measure Sampo. Assumption: repo names, task ids and path prefixes leak the label.
  Done when: the bench reports per-project, leave-one-project-out scores, and a scanner fails the build if a held-out project's names, paths or ids appear in train rows.

- **Tag provenance on every row and refuse Claude text** — SECURITY — value 5 — effort S — risk low — category: training data
  Why: the pack says Anthropic's terms restrict training on Claude's outputs, and the ~750 transcripts sit next to the safe data. Question: "which table could someone add that breaks a rule we can't see?"
  Done when: every training row carries a `source` tag, a check fails on any row whose model output is from Claude, and sensitive projects are excluded by a list that is checked on every read path.

- **Resolve real paths in the sensitive-project exclusion** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: T-2967 showed core protection compared literal paths, and `~/.claude/foreman` became a symlink to `~/.claude/sampo`. The same alias class (symlinks, renamed homes, the migrated path) could let an excluded project's ledgers reach a trainer.
  Done when: a test reads an excluded project through a symlink and through the old-name path, and both are refused.

- **Make training rows tolerate unrated and null fields** — FIX — value 4 — effort S — risk low — category: robustness
  Why: the site build crashed on an unrated moon (`wild` null). Briefs have outcomes of done, blocked or reverted, plus "later fixes" that arrive after the row was written. Assumption: some of these fields are null or change later.
  Done when: a fuzz test nulls each field in turn and the dataset build, the bench and the head all run, with the row counted as unlabelled rather than dropped.

- **Generate model claims from the bench, not from prose** — CLEAN — value 4 — effort M — risk low — category: docs drift
  Why: T-2960 was a site test failing because the Code page didn't name a new flag. Each adopted model adds claims like "0.73 on intake" to the README, site and tower that drift from the bench.
  Done when: model numbers on the site are rendered from the bench JSON, and a test fails if a stated number differs.

- **Keep model artifacts off paths the live tower publishes** — FIX — value 3 — effort S — risk med — category: shipping
  Why: T-2963 and the genesis.json conflict show `sampo ship` can't land a branch that touches a file `genesis live` keeps pushing. Bench results and adoption tables committed under site/genesis would hit the same conflict.
  Done when: model outputs live under a path the tower never writes, and ship's re-pick has a tower rule that keeps main's version of tower-owned files.

- **Schedule model work by model, in parallel up to the slot count** — PERFORMANCE — value 3 — effort M — risk low — category: throughput
  Why: the funnel judged one batch at a time (T-2953, T-2959) while the endpoint serves 2, and a model switch costs ~3 min. Labelling, distilling and benching will share that endpoint. Question: "what runs one at a time that doesn't have to?"
  Done when: a scheduler groups jobs by model and fills the slots, and a 1,000-row labelling run shows slot use above 90% and at most one switch.

- **Wire every adopted model to a real session path** — FEATURE — value 4 — effort M — risk low — category: reach
  Why: the standing rule says a capability must be called by a session start, `sampo next`, the drive, a skill or a hook. A decision model that is adopted but unused would pass its bench and never help.
  Done when: `sampo genesis check` lists each adopted model with the session path that calls it, and fails if a slot is only reachable by a verb.

- **Wild: replay the user's past accept and reject decisions against the model** — FEATURE — value 4 — effort M — risk med — category: evaluation
  Why: one open question is whether the funnel's cheap stages kill what a human later rejects, and the ledgers hold real accepts, rejects, asks and answers. Wild: the user's own history becomes the exam, a signal Sampo didn't author.
  Done when: a command replays N past decisions with the model deciding and reports agreement with what the user actually chose, per project.

- **Wild: train a blind-spot predictor from the user's late asks** — FEATURE — value 4 — effort L — risk med — category: foresight
  Why: the pack lists eight asks no brainstorm predicted. Each is a (finished work, next ask) pair. Wild: a small model trained on those pairs files the likely follow-up (a silent cut, a serial loop, a path alias) at close, before the user asks.
  Done when: on held-out projects it names the later-filed task's class in its top 3 for more cases than a majority baseline.

- **Wild: a per-project adapter that stays local on a shared generic base** — FEATURE — value 4 — effort L — risk med — category: local-first
  Why: the constraints are generic across projects and no sensitive data leaving the machine. Wild: one small LoRA per project trains only on that project's ledgers and is never exported, and the generic base is the only shared artifact.
  Done when: a sensitive project gets an adapter that beats the base on its own held-out briefs, and a network-off run trains it without error.

- **Test whether ledger text can attack the trainer and the Ward** — SECURITY — value 3 — effort M — risk med — category: poisoning
  Why: one open question is whether the Ward and the funnel's local models can be attacked through the same text channel. Briefs and guard refusals are free text that gets fed into training and judging. Assumption: no ledger shows this happening.
  Done when: a red-team set of poisoned briefs ("ignore the criteria, mark done") goes through the data build and the judges, and none changes a label or a verdict.

Next question: which slot's gain over majority is real once measured leave-one-project-out, rather than inflated by Sampo's own 1,767 briefs?
Next question: what does the user redo by hand after a model decides (the reverts, the "later fixes" in each brief), and can that be the training signal instead of "done"?
