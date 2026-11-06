# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Ablate one goal mechanism at a time on the planted-fault tier** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: long tier is 0/6 true done and 6 false dones haven't moved since gen 2, so it is unknown which of lease, evidence, checkpoint or done-gate earns its keep. Run each long-tier fault with each mechanism switched off in turn.
  Done when: a table of mechanism × fault shows, for each mechanism, which faults change outcome when it is removed, and names any mechanism with zero changes.

- **Plan so no step outlives a context window** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: resume is the worst area (2 of 6 needed a later fix). The inverse fix is to make resume rare: cut the plan into tracer steps sized to finish inside one window, each leaving a green, committed state.
  Done when: on a long-tier scenario the count of mid-step resumes falls to 0 and every step's commit passes its own check.

- **Ladder the discipline prompt: 0, 30 lines, full verbs** — PERFORMANCE — value 4 — effort S — risk low — category: simplicity
  Why: assumption: much of the goal-finish lift comes from a short instruction like "list the clauses, run a check for each, don't say done until all pass". Run three arms on the same scenarios and find the knee.
  Done when: the exam prints the true-done rate for three arms, and the cheapest arm within 10% of the full arm is named.

- **Engage goal machinery only above a predicted horizon** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: assumption: short tasks are already handled by the host, and clause-ledger overhead there is pure tax. Gate the heavy path on predicted step count, using the existing task size and cost forecast.
  Done when: a goal under N steps starts with no clause ledger or lease writes, and the short tier's true-done rate does not drop.

- **Cite the false done behind every done-gate clause** — CLEAN — value 4 — effort S — risk low — category: provenance
  Why: the six false dones are known but not tied to the gates. A gate clause with no live justifying scenario is a candidate for deletion.
  Done when: `fm doctor` lists each done-gate clause with its scenario id, and flags any clause with none.

- **Test fixes on a host-release day** — SECURITY — value 3 — effort M — risk low — category: host drift
  Why: Foreman stops being needed the day the host does this natively. On each new host CLI version, auto-run the six-false-done corpus with Foreman disabled.
  Done when: a nightly record shows, per host version, how many of the 6 corpus cases the plain host passes, and a jump above 0 files a task.

- **Count nudges the user or model ignores on the goal path** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: assumption: a goal-path nudge that is overridden or ignored with no later regret is the cheapest obsolescence signal not authored by Foreman. Log shown, followed and ignored, and whether a false done followed.
  Done when: a per-nudge table shows shown/followed/ignored counts over 14 days, with zero-catch nudges listed first.

- **Use per-model gate necessity** — PERFORMANCE — value 4 — effort M — risk med — category: model drift
  Why: a stronger model may never produce some false dones. Key each goal gate's catch record by model, and demote a gate for a model where it has caught 0 across N goals.
  Done when: the same goal on two models runs different gate sets, and each demotion cites its per-model catch count.

- **Publish the false-done corpus as an upstream benchmark** — FEATURE — value 3 — effort M — risk low — category: ecosystem — wild
  Why: the success metric of a discipline layer is the host fixing it. A redacted corpus of the 6+ false dones, which Foreman should eventually fail to beat the bare host on, makes that visible.
  Done when: a standalone folder runs against any agent CLI with no Foreman and prints a pass count.

- **Run a blind pair review on real goals** — FEATURE — value 4 — effort M — risk med — category: trust — wild
  Why: the user's trust is the real test and it is unmeasured. For one real goal a week, produce Foreman-on and Foreman-off results in worktrees and ask the user to pick, unlabelled.
  Done when: a ledger holds the user's blind picks and prints the share that chose Foreman, per goal kind.

- **Uninstall Foreman mid-goal and finish with the plain host** — FEATURE — value 4 — effort M — risk med — category: portability — wild
  Why: if a goal cannot survive Foreman's removal, Foreman is a lock-in rather than a discipline. Kill Foreman at step k and have a plain session finish from `GOAL.md` and git alone.
  Done when: the scenario finishes with all clauses proven and no Foreman state read, and the drill reports what it needed.

- **Make `done` a status vector, not a boolean** — FEATURE — value 3 — effort M — risk med — category: delight — wild
  Why: assumption: the false dones come from a single claimed word. If the agent can only emit a per-clause vector (proven, unproven, unmeasured), the user decides when it is done.
  Done when: the final message of a long-tier goal contains the vector, the word "done" appears only when all clauses are proven, and false-done count on the 6 scenarios is 0.

- **Report the goal tax per goal** — PERFORMANCE — value 3 — effort S — risk low — category: overhead
  Why: assumption: the cost of leases, hooks and evidence calls is unmeasured against what they catch. Print minutes and tokens spent on Foreman's goal path next to catches per goal.
  Done when: each closed goal prints "tax X min / Y tokens, caught Z", and a goal with Z=0 across 10 goals files a lean task.

Next question: which goal kinds does the bare host already finish reliably enough that Foreman should stay out of them?
Next question: if the host shipped a native goal feature next month, which three Foreman behaviours would the user still miss?
