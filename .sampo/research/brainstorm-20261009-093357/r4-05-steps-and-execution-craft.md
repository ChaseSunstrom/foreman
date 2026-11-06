# Brainstorm — lens: steps and execution craft

- **Make every step produce a handoff stub** — FEATURE — value 4 — effort M — risk low — category: step execution
  Why: resume after `/compact` is a core promise, yet the pack shows only "resume at the exact step". Steps lack a uniform artifact saying what is done, what is half-touched and what the next command is. Existing ideas cover reconciling a half-done step and replaying the last green command, not writing the stub as each step's exit contract.
  Done when: closing any step via `fm task step done` fails without a stub (touched files, open assumptions, next command), and a resume test in a fresh session reads only the stub and reaches the next action.

- **Lint steps for single-observable granularity at plan time** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: assumption: plans contain steps like "implement X and update docs" that hide failures. Existing ideas calibrate step size from history; none lint the step text itself.
  Done when: `fm task plan` warns on any step with multiple verbs/outcomes or no observable, and a test fixture with a compound step is flagged while an atomic one passes.

- **Run a pre-edit "blast sketch" for each step** — FEATURE — value 3 — effort M — risk low — category: execution
  Why: guard and sentinel work happens after edits; the step starts without naming files and tests it expects to touch. Complements footprint forecasting by making it per-step and checked at step end.
  Done when: each step records an expected file set, and step close reports files edited outside it, with a test showing an out-of-set edit is surfaced.

- **Detect step-skipping and reorder at execution** — FIX — value 3 — effort S — risk low — category: discipline
  Why: assumption: the model sometimes does step 4's work during step 2 and then marks steps done in bulk. The pack shows per-step discipline but no check on ordering or bulk closure.
  Done when: closing 2+ steps within one tool turn, or closing a step with no diff or command activity in the ledger since the previous step, is flagged, verified by a ledger-fixture test.

- **Keep a per-step "tried" ledger that blocks identical retries** — FEATURE — value 4 — effort M — risk low — category: retries
  Why: three failed attempts block with diagnosis, but nothing stops attempt 2 repeating attempt 1 in different words. Differs from forced diverse retries on gate failure by working at step level from recorded commands and edits.
  Done when: a second attempt whose command and edited hunks match a prior failed attempt (normalized) is refused with the earlier attempt's result, shown by a test.

- **Give every step a cheap undo point and a "step diff" view** — FEATURE — value 3 — effort M — risk med — category: recovery
  Why: assumption: reverting one bad step currently means manual git work. Related checkpoint-commit ideas exist; this adds the reviewable per-step diff and one-command rollback of only that step in a dirty tree using stash-like snapshots.
  Done when: `fm task step undo N` restores the tree to the pre-step snapshot without touching later unrelated edits, tested on a three-step fixture.

- **Add a mid-step "am I still on the task" tripwire based on the brief's nouns** — FEATURE — value 3 — effort M — risk med — category: focus
  Why: Foreman's core pitch is staying on the current task. Drift detection exists at the diff/brief level; this checks live tool calls (files, commands) against the step's declared nouns and nudges before the work is done.
  Done when: editing a file with no overlap to the step text or brief footprint triggers a one-line nudge, and a replay of a known-drift transcript fires it at least once.

- **Wild: Make the executor narrate its next move in the ledger before acting, then grade the narration** — FEATURE — value 3 — effort M — risk med — category: reasoning
  Why: wild; predictions per step are proposed, but a cheap one-line intent-before-action record at tool-call level lets a post-hoc grader find the first action that diverged from stated intent.
  Done when: a replay tool prints the first tool call whose intent and effect mismatch, on a seeded bad transcript.

- **Wild: Let a step run in "dry-run script" form first** — FEATURE — value 3 — effort L — risk med — category: execution
  Why: wild; the builder writes the sequence of commands and edits as a script plan, a cheap checker reviews it, then it executes. This turns step execution into plan-check-run for risky steps only.
  Done when: steps tagged risky produce a reviewable command list before any write, and a rejected list stops execution.

- **Wild: A "second pair of hands" that does the boring half of each step in parallel** — FEATURE — value 3 — effort L — risk high — category: parallel
  Why: wild; while the main thread implements, a Haiku scout drafts the test scaffold, changelog line or fixture for that same step from the brief.
  Done when: for a sample step, a scout draft arrives and is accepted or discarded by the main thread, recorded in the ledger with the time saved.

- **Reconcile steps against the brief at the halfway mark** — FEATURE — value 3 — effort S — risk low — category: plan fidelity
  Why: the "re-read the brief after the third step" idea exists generally; this makes it a deterministic gate at step N/2 that lists criteria with no step touching them.
  Done when: closing the middle step prints uncovered criteria, tested on a plan that omits one.

- **Classify each stall by type and switch the move** — FEATURE — value 4 — effort M — risk low — category: unsticking
  Why: stuck ladders and classifiers exist as ideas for debugging; execution stalls are different (waiting, unclear spec, flaky env, wrong approach). Each needs a different first response.
  Done when: a ledger of a stalled step is labeled with one of four stall types and the matching suggested move is printed, checked on four fixtures.

- **Require a "done looks like" command output snippet in each step before starting** — FEATURE — value 3 — effort S — risk low — category: verification
  Why: reduces vacuous step closure; narrower than the contract-compiler ideas, applying to steps rather than criteria.
  Done when: starting a step without an expected-output snippet is refused for M/L tasks, and closing compares actual output with it.
