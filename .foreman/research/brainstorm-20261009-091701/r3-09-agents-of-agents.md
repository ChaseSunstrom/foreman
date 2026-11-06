# Brainstorm — lens: agents of agents

- **Govern recursive delegation with a lineage tree** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: the user asked for "super recursive" agents, but the pack shows budget cascades and caps only per child. Assumption: nothing yet limits depth, fan-out or total spend across a tree of agents spawning agents. Every agent gets a lineage id, depth and fan-out limit, and a share of the parent's budget. Cycles are detected by task hash. One `fm tree` kill stops a whole subtree.
  Done when: a test agent told to spawn recursively stops at the configured depth, `fm tree` shows the lineage with spend per node, and killing a node ends its descendants.

- **Coalesce identical questions across the agent tree** — PERFORMANCE — value 4 — effort M — risk low — category: dedupe
  Why: assumption: parallel lanes, reviewers and scouts re-ask the same questions ("what calls X?", "does the gate pass on main?") and pay for it each time. An in-flight and completed question memo is keyed by (question hash, tree hash). A second asker waits for the first answer or reads it.
  Done when: two lanes asking the same recon question trigger one scout run, and the ledger records one run and one reuse.

- **Settle reviewer disagreements with an experiment agent** — FEATURE — value 5 — effort M — risk low — category: arbitration
  Why: `fm second` debate rebuts reviews with more argument. Assumption: many disagreements are empirical. When two lenses conflict ("this breaks X" vs "it doesn't"), a fresh agent writes a runnable test or repro that decides it. The result is recorded as evidence.
  Done when: a seeded conflicting-review fixture produces a failing or passing test file, and the verdict cites it instead of an opinion.

- **Shard "done" into context-blind claim checkers** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: the user wants "checks the product the way its user uses it", and the done-gate is checked by the same context that built the work. A claim-splitter turns the done summary into atomic claims. Each goes to a fresh agent that sees only the claim, the diff and the repo, not the brief's narrative. Any claim without independent evidence blocks done.
  Done when: a seeded task whose summary overclaims one behaviour is blocked on exactly that claim.

- **Staff reviewer panels for decorrelated errors** — FEATURE — value 4 — effort M — risk low — category: ensembles
  Why: existing ideas weight reviewers by precision, but three lenses on the same model tend to miss the same thing. Assumption: the ledger holds enough past verdicts to measure which lens, model or harness pairs miss different bugs. A panel composer picks the set with the least overlap in misses for the diff's risk profile.
  Done when: on replayed bench cases, the composed panel catches at least as many seeded defects as the default panel.

- **Add an integrator agent that owns the seams between lanes** — FEATURE — value 5 — effort L — risk med — category: integration
  Why: the merge train and the DAG across lanes prove each lane alone, and lane merges have already been a pain point (T-0280 couldn't land during T-0278). After parallel lanes finish, an integrator writes and runs contract tests at the interfaces they share. It must pass before the merge train advances.
  Done when: two lanes that each pass alone but disagree on a signature are caught by a seam test before merge.

- **Make every sub-agent state a confidence and score it** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: assumption: builder and reviewer reports are taken at face value. Each report ends with a numeric chance that it is right, scored later against the gate and sentinel outcome. Low-calibration agents get extra checking, and high-calibration ones get less.
  Done when: `fm digest` shows a calibration curve per role, and a routing rule changes based on it in a test.

- **Run a librarian agent that builds per-lane context packs** — FEATURE — value 4 — effort M — risk low — category: context
  Why: builder briefs have needed repeated hand-tuning (T-0399, T-0428). A librarian assembles each lane's pack from `fm outline`, `fm why`, `fm impact` and recall. It then learns from which files the lane actually opened or missed.
  Done when: a lane's first-hour file reads outside the pack drop measurably on replayed tasks.

- **Wild: Fork a lane at a decision point** — FEATURE — value 4 — effort L — risk high — category: forking
  Why: wild. Races today start from scratch. Instead, when a builder hits a real design fork, the orchestrator snapshots its worktree and context and spawns N children, one per option. The gate picks the survivor and the others are discarded with a note.
  Done when: one fork produces two worktrees that share a prefix, one merges, and the other's note is recorded.

- **Wild: Leave teaching notes from hard tasks for cheaper models** — FEATURE — value 4 — effort M — risk med — category: distillation
  Why: wild. After a strong-model agent solves an L task, it writes a short "how this repo bites" note keyed by file area. Weaker or cheaper agents load it for matching tasks. Bench measures whether it lifts their pass rate, and unhelpful notes are dropped.
  Done when: a bench run shows the cheap model's pass rate on matched tasks with notes beats without.

- **Wild: Hold an orchestration policy tournament on replayed queues** — FEATURE — value 4 — effort L — risk med — category: meta-orchestration
  Why: wild. Policies such as lane count, when to race, when to escalate and when to ask differ in outcome, and nobody tests them. A simulator replays the ledger of real queues under candidate policies with a cost model. The winner is proposed as a setting, and the user approves it.
  Done when: two policies replay on the same recorded queue and produce a comparable table of time, spend and idle minutes.

- **Run a standing "chief of staff" that answers sub-agents' blockers by escalation tier** — FEATURE — value 3 — effort M — risk med — category: escalation
  Why: assumption: children block on questions the system already knows. Each question goes through vetoes, then decisions, then recall, then the taste model, and reaches the user only if all of those fail. The path taken is logged.
  Done when: a seeded blocker covered by an existing decision resolves without a user ask, and the ledger names the tier that answered.
