# Brainstorm — lens: steps and execution craft

- **Gate each step on a pre-declared observable** — FEATURE — value 5 — effort M — risk low — category: execution
  Why: execute.md has per-step discipline, but the pack shows only task-level verify commands (criteria). Prior ideas cover pre/postconditions as a compiled graph, but not a lightweight per-step "you will see X" line checked at step close. Assumption: steps today are prose without machine-checkable exit signals.
  Done when: `fm task step done` refuses to close a step that lacks an observable line or whose recorded command output doesn't match it, and a test covers both.

- **Checkpoint commits per step with a step-scoped revert** — FEATURE — value 4 — effort M — risk low — category: execution
  Why: resume restores "the exact step" after /compact, but there is no evidence of per-step git anchoring. Assumption: steps share one working tree state. Ties to the "keep every step green" and "retry from a clean baseline" ideas but adds the primitive they both need.
  Done when: finishing step N creates a ref `fm/T-xxxx/step-N`, and `fm task step undo N` restores the tree to that ref while leaving later briefs and ledger entries intact (test shows file content returns).

- **Insert a read-the-neighbours step before every edit of unfamiliar code** — FEATURE — value 4 — effort S — risk low — category: craft
  Why: user steer "match surrounding code" style complaints plus hallucinated-API ideas exist, but none make the pre-edit look a recorded step. Assumption: builders sometimes edit after reading only the target file.
  Done when: the ledger shows, per edited file, a prior read of at least one sibling file or test; `fm task done` warns when absent.

- **Make the smallest-diff rehearsal a step type** — FEATURE — value 3 — effort S — risk low — category: craft
  Why: the pack's drift ideas compare the diff after the fact. Assumption: a builder can state "files I will touch, lines about" before editing, cheaply, as step 0.
  Done when: each step records a declared footprint, and the step close reports actual vs declared with a nonzero exit only when the diff exceeds it by a configured factor.

- **Run a step's verify in the background while the next step reads** — PERFORMANCE — value 3 — effort M — risk med — category: throughput
  Why: the pack has lane-level speculation, but within one thread gates block serially (slow-gate signals in T-0424). Assumption: most step verifies are independent of the next step's read-only phase.
  Done when: `fm bench` shows lower wall-clock on a replayed 6-step task with identical verdicts, and a failure in the background verify surfaces before the next edit.

- **Name the step's exit move before starting: continue, split, or escalate** — FEATURE — value 3 — effort S — risk low — category: execution
  Why: the "stuck ladder" and "trip on step size" ideas react after trouble; none pre-commit the response. Assumption: the 3-failures-then-block rule is the only current branch.
  Done when: a step can store an `on_fail` field and drive reads it to pick the next action, with a test where a failing step auto-splits rather than retrying.

- **Replay the last green step's command as the first act on resume** — FIX — value 4 — effort S — risk low — category: resume
  Why: resume lands at the exact step after /compact, but the pack shows "reconcile a half-done step" only as an idea. Assumption: the working tree may have drifted (user edits, lane merges) since the step closed.
  Done when: resume runs the previous step's recorded verify, and a seeded drift in a test produces a "baseline moved" notice before any edit.

- **Wild: Keep a typed "hands" journal so any step can be re-executed by a cheaper model** — FEATURE — value 3 — effort L — risk med — category: execution
  Why: wild. Assumption: recording each step as commands plus edits (not prose) lets a Haiku-class agent replay mechanical steps while the main thread only handles judgement steps.
  Done when: a recorded step replays on a clean checkout via `fm task step replay` and produces an identical tree hash.

- **Wild: Pit a "step sprinter" against a "step cautious" on the same step and keep the cleaner diff** — FEATURE — value 3 — effort M — risk med — category: execution
  Why: wild. Races exist at task level; this is step-level and cheap. Assumption: small S steps are fast enough to race.
  Done when: for a flagged step two worktrees run and the one with passing verify and smaller diff is merged, logged with both diffs.

- **Wild: Show a metronome of steps in the statusline that speeds up with stalls** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The band lacks a sense of per-step tempo. Assumption: median step durations from the ledger are available.
  Done when: the statusline shows step N/M plus a marker that changes when the current step exceeds 2x its historical median.

- **Record the "why this order" line between consecutive steps** — FEATURE — value 3 — effort S — risk low — category: craft
  Why: ordering ideas (riskiest-first, uncertainty per cost) exist but nothing preserves the rationale for later audit. Assumption: plans lose their sequencing reasoning at compaction.
  Done when: `fm task show` prints an order note per step boundary, and resume includes it in the restored context.

- **Fail a step if it left debug scaffolding behind** — CLEAN — value 3 — effort S — risk low — category: craft
  Why: cleanup requests never got done (user steer). Assumption: print statements, temp files and commented code commonly survive steps.
  Done when: step close scans the step's diff for added prints, TODO-tmp markers and untracked temp files, and blocks until each is removed or justified.

- **Time-box exploration steps and force a written finding at expiry** — FEATURE — value 3 — effort S — risk low — category: execution
  Why: thrashing and sunk-cost ideas exist; a per-step timer with a mandatory "what I learned" line is the missing primitive. Assumption: read-only exploration steps can run long without output.
  Done when: an exploration step past its box refuses further reads until `fm task note` records a finding, verified by a test.
