# Brainstorm — lens: steps and execution craft

- **Compile the plan into a step graph with pre/postconditions** — FEATURE — value 5 — effort L — risk med — category: planning
  Why: Steps today are prose in the brief; resume works "at the exact step" but nothing checks a step's entry or exit state. (Related to "Compile plans into programs", so go further: each step carries a runnable precondition, a postcondition, and a declared file footprint, and the drive refuses to start step N+1 until N's postcondition passes.)
  Done when: a test plan with a deliberately failing postcondition halts the drive at that step, and `fm task` shows the failing step and check.

- **Commit to a falsifiable prediction before each step** — FEATURE — value 4 — effort M — risk low — category: reasoning
  Why: assumption: execute.md has per-step discipline but no stated expectation. The builder writes "I expect test X to fail with Y / diff touches ≤ N files" before acting; a mismatch is logged as a surprise and forces a re-read of the plan rather than pushing on.
  Done when: a step whose observed result contradicts its recorded prediction produces a ledger "surprise" event and the next step is blocked until it is acknowledged.

- **Re-plan at checkpoints, not only on failure** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the pack shows "3 failed attempts → block", i.e. replanning is failure-triggered. A cheap mid-task pass compares remaining steps against what was learned (new files found, assumptions falsified) and edits the remaining steps with a recorded reason.
  Done when: after a step that falsifies an assumption, `fm task steps` shows revised downstream steps with a "replanned because" line.

- **Order steps by information value (riskiest first)** — FEATURE — value 4 — effort M — risk low — category: sequencing
  Why: assumption: plans are sequenced in natural build order. Put the step that could invalidate the approach (spike on the unknown API, the hardest integration) first, so a doomed approach dies at minute five instead of hour two. Pairs with the brief's 3+ approach options.
  Done when: for an L plan, the step tagged "highest uncertainty" is sequenced first, or the plan states why not.

- **Keep a per-step working set, and flush it at boundaries** — FEATURE — value 3 — effort M — risk low — category: context
  Why: compaction resumes at the step, but the step's discoveries (files read, dead ends tried, current hypothesis) live only in the transcript. Write a small "step notes" file the step owns, carried into the next step and into the handoff.
  Done when: after a forced `/compact` mid-step, the resumed session cites the prior dead end from step notes and doesn't retry it.

- **Run a "stuck ladder" instead of a flat 3-attempt block** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: today three failures lead to a block with a diagnosis. A ladder escalates in kind: (1) re-read the error and the brief, (2) the fm-debugger hypotheses, (3) shrink the repro, (4) a scout checks whether the assumption is true, (5) a second opinion on the approach, (6) then block. Each rung must differ from the last.
  Done when: a task failing repeatedly shows distinct rung types in the ledger, and no two consecutive attempts share the same rung and approach hash.

- **Add a definition-of-done rehearsal at plan time** — FEATURE — value 3 — effort S — risk low — category: verification
  Why: criteria with verify commands exist, but nothing executes them before the work to confirm the red state. Run each verify at plan approval and record red/green/error, so a criterion that is already green or that errors is fixed before building.
  Done when: planning a task with an already-passing verify produces a visible "criterion already green" warning.

- **Add a "smallest next step" mode for bogged-down tasks** — FEATURE — value 3 — effort S — risk low — category: execution
  Why: assumption: long M/L steps swallow hours. Detect a step that has exceeded its estimate or touched more than its declared footprint, and offer an automatic split into sub-steps, each with its own check.
  Done when: a step that overruns its declared footprint triggers a split proposal with at least two checked sub-steps.

- **Write a "why not" line for every rejected approach and test it later** — FEATURE — value 3 — effort S — risk low — category: reasoning
  Why: briefs list 3+ options, but rejections aren't structured. Record the rejection reason as a checkable claim, and when a step hits trouble, resurface the rejected option whose reason has since been falsified.
  Done when: a rejected approach whose reason is marked invalidated is shown at the next replan.

- **Wild: Run the plan as a rehearsal on a throwaway copy first** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: wild. A cheap, fast model executes the whole plan in a disposable worktree to expose missing steps, hidden dependencies and ordering mistakes, then reports a "plan diff" before the real builder starts. Cost: some tokens, benefit: the real run starts with a corrected plan.
  Done when: a rehearsal run outputs a list of steps that failed or were missing, and the final plan includes the corrections.

- **Wild: Give each step a "pair" voice that interrupts at the moment of a risky choice** — FEATURE — value 3 — effort M — risk med — category: thinking
  Why: wild. Rather than reviewing after, a tiny tool-less critic sees each diff hunk as written and may raise a one-line flag ("this swallows the error", "this changes the public signature") that the builder must answer before continuing. Catch the mistake while it's cheap.
  Done when: a seeded swallowed-exception edit raises a flag before the step completes and the builder's reply is recorded.

- **Wild: Keep a "breadcrumb trail" so any step can be reverted and replayed with a different choice** — FEATURE — value 3 — effort L — risk med — category: execution
  Why: wild. Each step ends in a tagged checkpoint (commit plus step notes). `fm task rewind N --choose B` restores the state at step N, swaps in the alternative approach and re-runs only the downstream steps.
  Done when: rewinding to a mid-plan step restores the tree to that checkpoint and the replay uses the new choice.

- **Verify each step by a different method than the one that built it** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: a builder who writes the code and the test shares the same blind spots. Require that a step's check differ in kind (a runtime probe instead of a unit test, a read of the output instead of the exit code) from the one the builder authored.
  Done when: a step whose only evidence is a test written in the same step is flagged "same-author evidence" at done.

- **Compare the diff to the step's plan, not just the brief** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: scope-drift detection exists against the brief, but a finer grain would catch extra edits per step. Each step's changed files are diffed against its declared footprint, and the unplanned ones are listed with a one-line justification required.
  Done when: an edit to a file outside a step's footprint produces a prompt for a justification recorded in the ledger.
