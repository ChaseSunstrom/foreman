# Brainstorm — lens: reliability

- **Make every tower step resumable and idempotent** — FEATURE — value 5 — effort M — risk med — category: orchestrator
  Why: the tower is many long steps (Seed, ≤8 Missions, critique, selection, drift, sweep), and the pack shows only storage (`init/put/status`), not an orchestrator. A crash or usage cap midway currently leaves a half-written generation. Assumption: steps are not yet checkpointed.
  Done when: killing `fm genesis run` with SIGKILL at each step boundary and rerunning finishes with the same files as an uninterrupted run, and no step runs twice (asserted by a step journal).

- **Single-owner lock with stale-lock takeover** — FIX — value 4 — effort S — risk low — category: concurrency
  Why: the site-publish debounce, `fm loop`, `fm scout` auto-start and a manual `fm genesis` can all write the same tower. Assumption: no tower-level lock exists.
  Done when: two concurrent `fm genesis run` calls in one project yield one runner and one clean "already running (pid, since)" refusal, and a lock whose pid is dead is taken over with a logged note.

- **Hard budget and wall-clock fuse per generation and per tower** — SECURITY — value 5 — effort M — risk low — category: limits
  Why: "runs forever" and "burns a week of usage on one project" are the inversion failures, and auto-start from an empty queue makes them unattended. The current $35 budget line shows budgets exist but are not tied to the tower.
  Done when: with a $1 cap and a stub child that always spends, the tower stops at the cap, writes `halted: budget` in status and resumes only with an explicit raise.

- **Auto-start with cooldown, ceiling and opt-in** — SECURITY — value 4 — effort M — risk med — category: auto-start
  Why: gap map #13 wants Genesis to start when the queue runs dry, but the routing line is protected core. A queue that is dry because of a failure, not completion, would trigger a loop of runs. Assumption: the trigger is a dry-queue check in loop/scout.
  Done when: a dry queue starts at most one tower per N days per project, never starts without `genesis auto on`, and the second trigger inside the cooldown logs "skipped: cooldown".

- **Freeze the exam, the oracle and gen-0 behind content hashes during a generation** — SECURITY — value 5 — effort S — risk low — category: integrity
  Why: inversion risk is "rewrites its own rules toward easier exams" and overfitting the held-out third. Gen-0 is read-only already, but exam keys and the selection rule are not shown as pinned.
  Done when: editing any exam scenario, key or selection rule mid-generation makes selection refuse with a hash mismatch, and the tower's status shows the hashes.

- **Rerun-for-variance before a rewrite can win selection** — FEATURE — value 4 — effort M — risk med — category: selection
  Why: "a rewrite stays only if it closes more exam scenarios than its parent" is a bare count, and model-driven scenarios are noisy. Cost shows up in the economics lens, but a flaky win corrupts lineage.
  Done when: a rewrite must beat its parent in a majority of k runs (k configurable), a ±1 flake no longer flips lineage in a replay of recorded scores, and ties keep the parent.

- **Quarantine held-out scenarios from every writer** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: Seed, Missions and critique children read the tower, and the held-out third could leak through the exam directory or a "what failed" summary. Assumption: the leak path is untested.
  Done when: a canary string planted in a held-out scenario never appears in any prompt sent to a Seed, Mission or critique child (checked by a prompt-log grep in a test).

- **Drift check as a blocking gate with a MUST/NEVER coverage table** — FEATURE — value 5 — effort M — risk med — category: drift
  Why: the exam is "self-written gen-0 covers every MUST, NEVER and section of the hand-written one". Making that an enumerated table means a missing NEVER fails loudly, not by an `fm second` impression.
  Done when: `fm genesis drift` prints one row per MUST/NEVER/section of the hand-written gen-0 with covered/missing, and any missing NEVER stops the generation.

- **Not-yet ledger with attempt counts, distinct approaches and a retire rule** — FEATURE — value 4 — effort S — risk low — category: ledger
  Why: the user's standing rule is ≥2 different approaches, then a ledger retried every generation. Without counts and approach fingerprints, it will retry the same thing or never stop. The user also said to kill only for proven harm or an exact duplicate.
  Done when: each ledger entry records blocker, attempts and approach hash; a retry that repeats a prior hash is rejected; an entry leaves only on success, proven harm or exact duplicate.

- **Atomic tower writes with a self-check on open** — FIX — value 3 — effort S — risk low — category: storage
  Why: tower archaeology depends on files alone. A torn `lineage.md` or a gen with no Seed misleads the next session. The earlier `write_atomic` bare-filename bug shows these paths are fragile.
  Done when: `fm genesis status` validates that every generation has the required files and a parseable lineage, reports the first problem, and all writes go through `write_atomic` (test with an injected crash).

- **Replayable tower: re-run selection from the journal with no model calls** *(wild)* — FEATURE — value 3 — effort M — risk low — category: replay
  Why: assumption: if every child output and exam score is journaled, selection, drift and sweep become pure functions. A bug report could ship a tower and get a deterministic reproduction.
  Done when: `fm genesis replay <tower>` reproduces every selection decision byte-for-byte with the network disabled.

- **Chaos mode: inject failures into the tower on a fixture project** *(wild)* — FEATURE — value 3 — effort M — risk low — category: testing
  Why: the planted-gap exam shows the "closes gaps" path, not the failure path. Randomly killing children, truncating outputs, returning empty Seeds and expiring usage on a generated project would prove the recovery paths.
  Done when: a seeded chaos run of 20 injected faults ends with the tower either completed or cleanly halted, never with corrupt files or a stuck lock.

- **Dead-man's switch: a tower that has stopped progressing says so on the site and in the next session** *(wild)* — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the site page is kept live automatically, so a silently stalled tower would look healthy. Assumption: no heartbeat exists.
  Done when: a tower with no step progress for X hours shows a "stalled since…" banner on the site and in the session-start note, and clears when progress resumes.

- **Self-change canary: any edit Genesis makes to its own templates must pass a frozen mini-exam first** — SECURITY — value 4 — effort M — risk med — category: self-modification
  Why: the self-modification lens needs a measured, reversible change. A template edit that lowers the frozen exam score is reverted automatically and logged.
  Done when: a deliberately bad template edit is auto-reverted with a lineage entry, and a good one is kept with before/after scores.

Next question: What does Genesis do when the user's own corrections in history contradict each other or the hand-written gen-0, and who wins?
Next question: Which tower step is the most expensive to repeat after a crash, and is it worth checkpointing inside the step?
