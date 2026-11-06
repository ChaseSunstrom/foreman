# Brainstorm — lens: steps and execution craft

- **Reconcile a half-done step on resume** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: resume restores "the exact step", but a step interrupted by `/compact`, a crash or a quota stop leaves a half-edited tree. Nothing in the pack says how that state is judged. Each step would carry its postconditions and an idempotent flag. On resume Foreman diffs the worktree against them and picks continue, redo or roll back to the step baseline.
  Done when: a test kills a session mid-step (edit made, test not yet run) and `fm resume` reports which postconditions already hold and takes the matching action.

- **Track the failure frontier, not just the failure count** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: "3 failed attempts → block" counts attempts, so a run whose error moved from import to build to test 4 of 9 is blocked like a spin. Normalize each failure to a fingerprint and the depth it reached in the pipeline. Deeper means progress and an identical fingerprint means spinning. The block fires on spinning and extends on progress.
  Done when: replaying two recorded attempt sequences, one advancing and one repeating, gives "continue" for the first and "block with diagnosis" for the second.

- **Promote the probe that worked into the verify** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: the exploratory command that first showed the bug or the fix is usually the best check, and it is lost in the transcript while the criterion gets a hand-written verify. Capture exploratory commands per task, and at `fm task prove` offer the one that went red→green as the criterion's verify.
  Done when: `fm task prove` lists the candidate probes from the step log and a chosen one is stored as a criterion verify that runs and fails on the pre-fix tree.

- **Attribute every diff hunk to a step and spin off orphans** — FEATURE — value 4 — effort M — risk low — category: scope
  Why: scope-drift and plan-vs-diff checks exist at the brief or step level. Hunk-level provenance would be recorded at edit time. Hunks tied to no step are the drive-by edits, and they get captured as a task or reverted before done.
  Done when: finishing a task whose diff contains an unplanned hunk lists that hunk as an orphan and blocks done until it is captured or reverted.

- **Keep every step green** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: CLEAN and migration plans often cut steps that only pass together, so a mid-task failure has no safe stopping point. Planning would check that the gate stays green after each step and re-cut using expand/migrate/contract (parallel change). Steps that can't be green are flagged with a reason.
  Done when: a CLEAN L plan with a rename-everything step is rejected with a suggested expand/contract split, and the gate runs at each step boundary.

- **Retry from a clean step baseline** — FEATURE — value 3 — effort S — risk low — category: retries
  Why: a failed attempt leaves partial edits that bias the next one, so attempt 2 patches attempt 1's mess. Snapshot the tree at step start, reset to it on retry, and keep the failed diff as a note. Assumption: lanes already give a worktree to snapshot against.
  Done when: after a failed attempt the next one starts from a tree identical to the step-start hash, and the failed diff is attached to the step.

- **Detect foreign rewrites after every edit** — FIX — value 3 — effort S — risk low — category: edit integrity
  Why: formatters, hooks and codegen can rewrite a file right after Claude writes it, and the agent then reasons about content that is no longer on disk. Hash the written content and compare on the next read or at step end. Warn when something else changed the file, naming the likely actor.
  Done when: a test with a format-on-save hook that alters an edit gets a "file changed after write by something else" note.

- **Script the repetition** — FEATURE — value 3 — effort M — risk med — category: execution
  Why: a step that needs the same change at 20 sites is error-prone by hand. Past a threshold, Foreman would write a throwaway transform script, show its dry-run diff, apply it and delete it, with the dry-run recorded as evidence. Codemod campaigns exist, but only as a campaign type, not as in-step craft.
  Done when: a step with 15 or more matching sites is done through a script, and the evidence shows the dry-run diff matches the applied diff.

- **Trip on step size, not only on time** — FEATURE — value 3 — effort S — risk low — category: pacing
  Why: the existing re-frame trigger fires on effort past the estimate. A step that planned for about 20 lines and is now at 300 usually hides a missing split. Each step would declare an expected footprint, and 3x triggers a stop-and-resplit prompt.
  Done when: a step whose diff exceeds 3x its declared footprint pauses with "re-split or justify", and the answer is recorded.

- **Declare safe interrupt points per step** — FEATURE — value 3 — effort M — risk med — category: steering
  Why: user steers and compactions land wherever the model happens to be. Steps would mark the moments when the tree is coherent. Steers are captured immediately but applied at the next safe point, and compaction waits for one unless context is critical.
  Done when: a steer sent mid-edit is queued, acknowledged, and applied only after the step's next safe point is logged.

- **Wild: Pass the baton** — FEATURE — value 3 — effort M — risk med — category: collaboration
  Why: wild; the user often wants to fix one thing by hand mid-task. `fm baton` would mark the step "user driving" and silence Foreman's edits. `fm baton back` would read the user's diff, check it against the step's postconditions and carry on.
  Done when: after a hand edit and `fm baton back`, the step shows the user's hunks as user-authored and the remaining postconditions are rechecked.

- **Wild: Mise en place before step 1** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: wild; plans fail late on things knowable early, like a verify command that errors, a missing tool, or an unanswered question. Before the first edit, run every command the plan names to confirm it executes, check that every named file exists, and batch all missing items into one ask.
  Done when: a plan containing a mistyped verify command is stopped before step 1, with that command named in a single batched list.

- **Wild: Sample a shadow executor** — FEATURE — value 3 — effort L — risk med — category: self-improvement
  Why: wild; on a random 1 in 20 steps, a stronger model gets the same step baseline and brief in a throwaway worktree. The two action traces and diffs are compared, and large divergences become labelled examples of where the cheaper executor is weak, feeding model routing.
  Done when: `fm friction` shows a table of sampled steps with divergence scores per agent type.

- **Wild: Hand-written postcondition haiku** — FEATURE — value 1 — effort S — risk low — category: delight
  Why: wild; each step closes with a one-line, plain-words statement of what is now true, written before the evidence and checked after. A mismatch is shown as "what I said / what I found". It makes the claim-versus-evidence gap visible on every step, and people will screenshot the funny ones.
  Done when: the pane shows each step's "now true" line, with a mismatch badge when verification disagrees.
