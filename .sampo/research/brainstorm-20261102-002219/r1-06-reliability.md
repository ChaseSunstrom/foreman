# Brainstorm — lens: reliability

Answers to earlier questions, from the reliability lens: the pack doesn't show whether cell probes run off Claude Code. I treat that as unknown, and every idea below that checks a cell has to say which harness it ran on. Also, the "ideas so far" list is mostly about Anticipation, so I stay on #4's own failure modes: crash, compaction, drift and a false "done".

- **Reconcile baton, ledger and repo on every resume** — FIX — value 5 — effort M — risk med — category: resume
  Why: the pack lists "Baton, ledger and repo disagree after a kill" as a blind-spot class, and #4 promises to carry a plan across crashes. Assumption: resume trusts the baton without checking the repo.
  Done when: a test kills a session after a commit but before the baton write, and the next resume reports the commit as done and does not redo it.

- **Replay kill-at-every-boundary on the goal state** — FIX — value 5 — effort M — risk low — category: crash safety
  Why: the pack asks for "kill hooks at every write boundary" for state generally, but nothing is specific to goal and plan files. Assumption: the goal ledger writes are multi-step and not atomic.
  Done when: a harness kills the goal writer at each write step, and every outcome resumes to a valid goal state with no lost or duplicated item.

- **Make "finished" a computed verdict, not a stored flag** — FIX — value 5 — effort M — risk med — category: done detection
  Why: #4 must know when it is "actually done rather than merely stopped". Assumption: a goal can be closed while a contents row is still unproven or open.
  Done when: `fm goal finish` refuses while any plan row is open, unproven or unreferenced by a closed task, and names each blocking row.

- **Rehydrate the plan after compaction and hash-check it** — FIX — value 4 — effort S — risk low — category: compaction
  Why: the pack's context management section says context is summarized mid-task. Assumption: the plan the model sees after compaction can differ from the plan file.
  Done when: a post-compaction hook prints the plan hash, and a test with a tampered plan file reports a mismatch.

- **Detect a silently stalled goal** — FEATURE — value 4 — effort M — risk low — category: liveness
  Why: the pack asks for a heartbeat so silence means "alive", and for beat checks on unattended jobs. Assumption: a multi-day goal has no signal when no lane has advanced it for days.
  Done when: a goal with no task closed in N days appears in `fm doctor` and the next session note with its last action and its blocker.

- **Probe each filled cell by re-running its cited behaviour** — FEATURE — value 5 — effort M — risk med — category: coverage
  Why: the standing rule says a cell counts only if it is real, and the pack repeats "re-run, not just resolve". Assumption: the sweep today only checks that the cited file exists.
  Done when: the sweep fails a planted cell whose cited path exists but whose behaviour is gone, and records the harness each probe ran on.

- **Tag each probe with the harness it ran on** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: this answers the open question about non-Claude harnesses. Assumption: some cells silently depend on Claude Code hooks.
  Done when: the coverage report shows a harness column, and any cell checked only on Claude Code is flagged.

- **Run the plan-versus-diff check when a goal closes** — FEATURE — value 4 — effort M — risk med — category: done detection
  Why: the pack's ideas mention "diff the plan against the diff at finish", but #4 doesn't show it. Assumption: a plan item can be marked done with no matching change.
  Done when: finishing a goal lists each plan item with the commit or evidence that closed it, and fails on an item with none.

- **Make cell filling resumable and idempotent** — FIX — value 4 — effort S — risk low — category: batch safety
  Why: filling 58 cells across writers and cold reads will be interrupted. Assumption: a half-written coverage.md is possible.
  Done when: killing the fill mid-run and rerunning gives the same file as one clean run, and diffing two runs is empty.

- **Check the goal against a fresh-clone replay** — FEATURE — value 4 — effort L — risk med — category: done detection
  Why: "actually done" needs the real path, per pillar 5. Assumption: a goal's tests can pass in a working tree carrying stray state.
  Done when: `fm goal finish --clean` runs the goal's verify commands on a fresh clone and reports any that differ from the working tree result.

- **Wild: Run a chaos day on a live goal** — FEATURE — value 3 — effort M — risk med — category: chaos
  Why: wild. Assumption: the real failures come in combination: a kill during compaction, then a usage-limit pause.
  Done when: a scripted run does forced compaction, a kill and a pause on one goal, and it still reaches the same final state as an undisturbed run.

- **Wild: Plant a decoy open item and see who notices** — FEATURE — value 3 — effort S — risk low — category: done detection
  Why: wild. Assumption: finish checks may miss an item the plan never listed.
  Done when: a nightly canary goal with one hidden unfinished item is never reported finished.

- **Wild: Keep a shadow ledger rebuilt from git and compare** — FEATURE — value 4 — effort M — risk med — category: crash safety
  Why: wild. Assumption: the goal state can be derived from commits and task closes alone, so any divergence from the stored state shows a bug.
  Done when: the rebuilt ledger matches the stored one on a replayed recorded goal, and a planted divergence is reported.

- **Cap the cost of an interrupted goal** — SECURITY — value 3 — effort S — risk low — category: budget
  Why: the pack's rule says to wait out limits and keep going, which could loop. Assumption: a resume loop on a failing step has no ceiling.
  Done when: a step that fails three resumes in a row parks with a reason and stops spending.

Next question: Which of the goal's recovery paths have never actually run after a real kill, only in tests?
Next question: Does any cell's probe pass only because it reads a file the same session just wrote?
