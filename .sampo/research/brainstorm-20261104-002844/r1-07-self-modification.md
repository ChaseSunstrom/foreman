# Brainstorm — lens: self-modification

- **Resolve state from any worktree** — FIX — value 5 — effort S — risk low — category: reliability
  Why: the pack says evidence and lease commands fail inside the builder worktree the harness puts the agent in. Resolve the state dir through `git rev-parse --git-common-dir`, and fall back to a recorded main-repo path when that fails.
  Done when: `fm evidence` and `fm lease` run from a fresh linked worktree and write to the main repo's ledger, in a test.

- **Run a worktree drill in `fm doctor`** — FIX — value 4 — effort S — risk low — category: observability
  Why: the worktree failure went unseen until a builder hit it, so the same class (a verb that works only in the main checkout) can recur. Doctor creates a scratch worktree and runs every state-touching verb from it.
  Done when: planting a cwd-dependent path in one verb turns the doctor line red and names that verb.

- **Gate every self-edit on the long-tier replays** — SECURITY — value 5 — effort M — risk med — category: self-change safety
  Why: the long tier is stuck at 0/6 true done, and resume needed 2 later fixes, so edits to done-gate or resume code are unverified when they land. Any diff touching those paths must pass the planted-fault scenarios (forced compaction, killed session, usage-limit pause, misleading test) in a scratch home before `fm ship`.
  Done when: a deliberately broken resume patch is refused at ship with the failing scenario named.

- **Turn each false done into a regression scenario** — FEATURE — value 5 — effort M — risk low — category: evals
  Why: 6 false dones have been unchanged since gen 2, which suggests the failures are known but not pinned. Each one is written as a replayable fixture (the goal, the claimed done, the missing evidence) that the free arms run every generation.
  Done when: all 6 are fixtures, each red on today's code, and a fix flips exactly its own fixture.

- **Draft done-gate patches from false-done evidence** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: the gaps have sat for 2 generations with no fix. A tool-less child reads one false-done fixture and proposes a minimal gate-clause patch, which is adopted only if it clears that fixture and doesn't regress the other 5 or the plain-Claude parity runs.
  Done when: at least one proposed patch is adopted and its fixture turns green with the other fixtures unchanged.

- **Roll a self-change back automatically on worse outcomes** — FEATURE — value 4 — effort M — risk med — category: self-change safety
  Why: lean-substance rows already wait on measurements, but nothing reverts a change that proved harmful. Each self-edit records a baseline for false-done rate and resume failures, and a revert task is filed if they worsen over the next N tasks.
  Done when: a simulated regression after a self-edit files a revert task that cites the baseline and the new reading.

- **Keep a self-edit ledger** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: lineage.md marks choices provisional, but there is no per-edit before/after record of the metric the edit was meant to move. One line per self-edit: the path, the metric, the baseline, the later reading and the verdict.
  Done when: `fm genesis check` lists every self-edit of the generation with a metric, and fails if one has none.

- **Write the resume card before compaction** — FIX — value 5 — effort M — risk low — category: resume
  Why: resume is the worst area, with 2 of 6 needing a later fix. A hook writes a machine-checked card (goal, checklist state, lease, next command) before compaction and at each close, and the resumed session must read it back before acting.
  Done when: killing the session at every checkpoint in a drill and resuming restores the same checklist state, in a test.

- **Wild: Hold a gate tournament overnight** — FEATURE — value 4 — effort L — risk med — category: self-improvement (wild)
  Why: assumption: gate wording and thresholds can be mutated cheaply. Variants of the done-gate run against the false-done fixtures in a scratch home, and the survivors are filed as probation branches, never merged unseen.
  Done when: a morning card lists the surviving variants with fixture scores, and none is applied without a task.

- **Wild: Generate a per-goal verifier script** — FEATURE — value 5 — effort L — risk high — category: done detection (wild)
  Why: a vague goal turned into a complete plan has no machine check of "done". At intake Sampo writes a small verifier from the plan's checklist, a cold different-model read attacks it, and the task closes only when that verifier passes against real evidence.
  Done when: a goal with a planted missing clause fails its generated verifier, and the verifier is stored beside the plan.

- **Wild: Fork a probation self** — FEATURE — value 4 — effort L — risk high — category: self-change safety (wild)
  Why: assumption: the standing rule of never blocking on the user lets it work unattended. A sandboxed copy of Sampo tries to improve the weakest long-tier cell, and its patch lands only on an expiring branch that passes the free arms plus the replays.
  Done when: a probation branch exists with its replay scores, auto-expires in 3 days, and never reaches main without `fm ship`.

- **Run an adversarial completer on every close** — FEATURE — value 4 — effort M — risk med — category: done detection
  Why: the false dones suggest the agent's own claim is trusted too much. A cold child gets only the goal and the diff and lists the clauses it thinks are unmet, and a close that cites no counter to its list is held.
  Done when: replaying a known false done makes the child name the missing clause, and the close is held.

- **Pin the self-edit protected core by hash** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: the guard and done-gate sit on the self-modification path. Their hashes are sealed, and drift not tied to a task with a cold read turns doctor red.
  Done when: editing a guard rule outside a task makes `fm doctor` name the file.

- **Wild: Sampo files its own obituary for dead gate clauses** — CLEAN — value 2 — effort S — risk low — category: simplicity (wild)
  Why: assumption: gate clauses accrete as the false dones are fixed. A clause that has not changed a verdict in 30 days is flagged and removed by a self-edit that must pass the replays.
  Done when: a clause with zero verdict changes is proposed for removal, and the replays stay green after it goes.

Next question: Which of the 6 false dones came from the agent misjudging evidence, and which from the plan itself missing a clause?
Next question: Can a self-edit be judged on the fixtures alone, or does it need a real long-horizon run before it is trusted?
