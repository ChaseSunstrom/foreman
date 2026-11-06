# Brainstorm — lens: 2030 worked back

- **Run a state broker so lanes never touch state by path** — FIX — value 5 — effort M — risk med — category: worktree
  Why: evidence and lease commands fail inside the builder worktree, and many ideas so far patch path resolution one verb at a time. In 2030 every goal runs across worktrees, containers and hosts, so the fix is to stop resolving paths. One local socket per repo takes evidence, lease and journal calls. Assumption: the current failure is a path or cwd resolution bug.
  Done when: a builder in a fresh worktree, in a container with no shared filesystem, can run `fm evidence` and `fm lease` and the records land in the main ledger.

- **Tombstone every clause removal** — SECURITY — value 5 — effort S — risk low — category: false-done
  Why: 6 false dones are unchanged since gen 2. One cheap way to get a false done is for the plan itself to shrink. Assumption: some of the 6 involved a dropped or reworded clause, which should be checked.
  Done when: removing or weakening a goal clause without a recorded reason and an origin (user or agent) makes `fm task finish` refuse, and a test that deletes a clause fails.

- **Count only user-origin clauses toward done** — FEATURE — value 4 — effort S — risk low — category: false-done
  Why: it follows from the tombstone idea. Clauses the agent adds while planning are useful for work but must not be able to define done by themselves. Assumption: clause records have no origin field yet.
  Done when: the done report shows "user clauses N/N, agent clauses M/M", and done is blocked if a user clause is unmet even when all agent clauses pass.

- **Retrieve the nearest closed goal's clause list to complete a vague plan** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the request is "a vague goal becomes a complete plan." The closed-task ledger already holds hundreds of finished goals with their Done-when lines. By 2030 the plan library is the product. The zero-token step is a TF-IDF lookup of the nearest three closed goals, then a diff of their clauses against the new plan.
  Done when: for a vague goal the planner prints "closed goals like this also had: <clauses>", and the long tier shows fewer missing-clause misses than a run without it.

- **Harvest the user's real closed goals into the long-horizon tier automatically** — FEATURE — value 5 — effort M — risk med — category: exam
  Why: the long tier has 6 scenarios and scores 0/6, which is too few to guide anything. The ledger already has the rolled-back commit and the change that followed, so each finished goal can become a replay scenario. By 2030 the exam is bigger than anything a person could write. Assumption: enough closed goals have a clean base commit.
  Done when: `fm exam long` lists at least 20 scenarios with provenance "harvested from T-id", and one harvested scenario runs end to end in a scratch clone.

- **Measure resume as time to the first correct action** — PERFORMANCE — value 4 — effort M — risk low — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix), and the metric is binary. A cold session after kill or compaction should be scored on tokens and tool calls until its first action that advances an open clause, which exposes slow and wrong resumes alike.
  Done when: the drill prints the resume cost for kill, compaction and usage-limit pause, and the ratchet fails when any exceeds the recorded bar.

- **Bill spend per clause and flag the outliers** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: multi-day goals drift in cost long before they drift in correctness. A clause using three times the median is usually mis-scoped or looping. Assumption: the cost ledger can be joined to task and step ids.
  Done when: the goal view shows dollars per clause, and a planted looping clause gets flagged within one tick.

- **Export a goal as a portable bundle another harness can resume** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: Sampo says it is not Claude-specific, and by 2030 a goal will outlive a model, a host and possibly the user's laptop. The bundle holds the charter, clauses, evidence, journal and base commit. Assumption: the existing goal-file ideas have not been built yet.
  Done when: `fm goal export` followed by `fm goal import` in a clean clone under a different agent CLI finishes the next open clause.

- **Run a model-swap continuity test mid-goal** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: models will change every few months while a goal lasts weeks. Swapping the model after the first checkpoint and comparing clause outcomes against a no-swap run shows how much of the goal state lives in the ledger and how much only in the model's head.
  Done when: a long-tier variant swaps the model mid-run and reports clause pass parity, with a pass or fail against a stated threshold.

- **Wild: Leave a will for the unattended goal** — FEATURE — value 3 — effort M — risk low — category: unattended
  Why: wild. If the user is silent for N days, or a hard cap only they can raise is hit, the goal moves itself to a safe parked state. It leaves a letter that says what is done, what is unproven, and the single action that restarts it. Today a silent stall looks the same as slow progress.
  Done when: after a simulated 3-day silence the goal sits in `parked` with a letter file, and one named command resumes it.

- **Wild: Write a letter from the 2030 maintainer at goal start** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: wild. A cold child gets only the goal and the repo and writes the future post-mortem of why this goal failed. Each cause becomes a candidate clause or a planted fault for the long tier. It makes the missing-clause question concrete.
  Done when: the plan carries at least 3 "pre-mortem" clauses, and at least one is later confirmed or refuted by evidence.

- **Wild: Run a goal séance after compaction** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: wild. After each compaction a cold child that has seen only the charter and the resume card says what it believes is done and what is next. The ledger then grades it, and a mismatch means the card lost something. Assumption: the resume card exists or will.
  Done when: each compaction records an agree or disagree line against the ledger, and a deliberately truncated card is caught.

- **Wild: Bet on a done-date and sweep stalls** — FEATURE — value 2 — effort M — risk low — category: forecasting
  Why: wild. The planner seals a done-date forecast with its error bar before the first edit. When clause movement falls behind the forecast the goal flags itself, and the later score calibrates the next forecast. Assumption: none of the existing forecast ideas are tied to goals.
  Done when: every goal stores a sealed forecast, and closing a goal prints forecast versus actual days.

Next question: which of the 6 false dones came from the plan shrinking rather than the check being wrong?
Next question: can the broker's records be replayed to rebuild the ledger, so the broker doesn't become a single point of loss?
