# Brainstorm — lens: simplicity

- **Break ties toward the smaller tower** — FEATURE — value 4 — effort S — risk low — category: selection
  Why: the pack says a rewrite stays only if it closes more scenarios than its parent. Nothing rewards a rewrite that closes the same number with fewer lines or rules, so the spec only ever grows. Assumption: gen docs have a countable size.
  Done when: given two fixtures with equal closure, the selector keeps the one with fewer lines and logs "tie, smaller won" in lineage.

- **Use git history as the lineage** — CLEAN — value 4 — effort M — risk med — category: storage
  Why: lineage.md, status per generation and rewind are all separate custom code (T-2078). One commit per generation on a tower branch makes `git log` the lineage, `git revert` the rewind and `git diff gen-a gen-b` the diff. Assumption: tower storage can be a git repo or orphan branch.
  Done when: after three generations `git log --oneline` on the tower shows one line per generation, and `fm genesis status` reads only from it.

- **Trace every rule to a scenario that needs it** — FEATURE — value 4 — effort M — risk low — category: pruning
  Why: gen-0 §2 lists many MUSTs, NEVERs and sections. A self-written spec will have rules that no exam scenario exercises. Assumption: scenarios can be tagged with rule ids.
  Done when: `fm genesis status` lists rules with zero exercising scenarios, and the sweep either deletes each one or files it in not-yet.md.

- **Replace the knobs with one effort dial** — FEATURE — value 4 — effort S — risk low — category: settings
  Why: budget, wall-clock, scenario count, generation cap, held-out size and the plain-arm switch are all separate settings. A user typing "make this great" wants one choice. Assumption: the existing settings can be derived from a small table.
  Done when: `fm genesis --effort low|normal|high` is the only flag needed, and the table mapping it to the underlying limits is a single readable block.

- **Publish at generation close, not on every put** — CLEAN — value 3 — effort S — risk low — category: site
  Why: T-2080, T-2087, T-2088 and T-2090 show the live site cost four tasks, including a debounce for bursts. Publishing once per closed generation removes the debounce and the burst problem. Assumption: users care about generation-level freshness, not per-put.
  Done when: ten `put`s in one generation cause zero publishes, and generation close causes exactly one.

- **Answer "should Genesis start?" with one predicate** — CLEAN — value 4 — effort S — risk low — category: auto-start
  Why: the loop, scout and the routing line in the protected rules/foreman.md would each carry their own start logic. One `fm genesis due` returning yes or no plus a one-line reason gives all three a single call, and gives the user's yes a single thing to approve.
  Done when: loop and scout contain no start heuristics of their own, and `fm genesis due` has a table-driven test.

- **Cap stages by test, not by taste** — CLEAN — value 3 — effort S — risk low — category: complexity budget
  Why: the tower already has Seed, missions, critique, selection, drift, sweep, grid and ledger. A test that fails when the stage count or the genesis module's line count passes a stated ceiling forces any new stage to replace an old one. Assumption: the ceiling is set from today's size.
  Done when: adding a ninth stage fails the test until one is removed or the ceiling is raised in a reviewed edit.

- **Give every failure one of three sentences** — FEATURE — value 3 — effort S — risk low — category: errors
  Why: a stranger repo will hit missing toolchains, empty queues, exhausted budgets and failed children. The user needs only to know whether to wait, answer or give up. Assumption: every failure maps cleanly to one of those three.
  Done when: each Genesis exit prints exactly one line starting "Waiting:", "Need you:" or "Stopped:", and a test confirms that for every failure fixture.

- **Check the tower reads in three sentences** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: the user wants every doc readable in full on the page. If a tool-less child can't summarize a tower in three sentences, a person can't either. Assumption: child summaries are cheap enough to run per generation.
  Done when: `fm genesis status` includes a three-sentence summary from a tool-less child reading only the files, and flags the generation when the child's summary contradicts the recorded next step.

- **Wild: Genesis with no stored state** — FEATURE — value 3 — effort L — risk high — category: architecture
  Why: wild. Every run recomputes the current tower from the repo, gen-0, the exam and the ledger, with no hidden state and no resume logic. Assumption: runs are cheap enough, or cached, to rebuild.
  Done when: deleting everything except gen-0, the exam and not-yet.md and running `fm genesis` reproduces the same status.

- **Wild: a 30-line reference tower** — CLEAN — value 3 — effort M — risk low — category: testing
  Why: wild. A deliberately naive shell or Python reference that does init → write → exam → keep-better → stop is the oracle for the real orchestrator. They must agree on selection outcomes for fixtures, so complexity must pay for itself.
  Done when: a test runs both on three fixtures, and a disagreement fails unless the real one's reason is recorded.

- **Wild: one sentence per run** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: wild. Each run ends with a single plain sentence (for example "Closed 4 of 9 gaps in 38 minutes for $2.10; the next thing is the empty grid cell for deploys") and nothing else by default, with everything else behind `--full`. Assumption: users prefer the short form.
  Done when: default output is one line, and a test confirms the details are only shown with `--full`.

Next question: Which Genesis stage has never changed a selection outcome on any tower so far, and could it be deleted?
Next question: What would the user still be able to do if `fm genesis` had only two commands, `run` and `undo`?
