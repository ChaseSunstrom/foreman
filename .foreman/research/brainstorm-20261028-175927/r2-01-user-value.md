# Brainstorm — lens: user value

- **Chart round-over-round improvement on a fixed corpus** — FEATURE — value 5 — effort L — risk med — category: measurement
  Why: the request is "improve past everything shipped", but nothing shows whether round 5 beat round 4; T-1231 (beat Claude Code on the duel) and T-0866 are both deferred for lack of cases. Assumption: `fm duel` can run a pinned case set against an old tag.
  Done when: `fm round bench` runs the same 20 cases at the last two round tags and prints pass-rate, cost and time per tag with the delta.

- **Give each task a ship ladder: closed, on main, live** — FEATURE — value 4 — effort M — risk low — category: shipping
  Why: the user repeatedly sends "Push T-1785, T-1830..T-1834… to main" and "Push foreman/build to main so the site publishes", so closed-local is not the state they care about.
  Done when: `fm status` shows each task as closed, on-main or live-on-site, and one `fm ship` command moves every closed-but-not-on-main task up one rung after the gate passes.

- **Verify review findings against the code before filing** — FIX — value 4 — effort S — risk low — category: review quality
  Why: all five "dropped" items are false positives where the code already did it (`set_panic` already atomic, `fm drill` already in the suite, lights already fixed in T-1847, FILE check already at the top of `cmd_scene`). Each cost the user a triage decision.
  Done when: a finding with no quoted line that `grep` finds at the named path is rejected before it becomes a task, and a test feeds one fabricated finding to prove it.

- **Turn review severity into test-first fix tasks automatically** — FEATURE — value 4 — effort M — risk low — category: review loop
  Why: the user's steers ("3 MEDIUM… fixing test-first") show a manual routine: MEDIUM and above become tasks with a failing test first, and LOWs get batched.
  Done when: closing a review files one test-first task per MEDIUM+ finding and one batched cleanup task for the LOWs, each carrying the finding's quoted line.

- **Measure orchestrator idle time and fill it** — PERFORMANCE — value 4 — effort M — risk med — category: lanes
  Why: pillar 1 says never idle while a gate, build or review runs, yet there is no measurement of seconds spent waiting with no lane working. Assumption: lane start and stop events are in the journal.
  Done when: the round report prints idle seconds, and a test with two independent tasks and one slow gate shows the second lane starting during the gate.

- **Split a stalled lane into two tasks and keep its partial diff** — FEATURE — value 4 — effort M — risk med — category: lanes
  Why: the user split T-1803 by hand into T-1833 (routing) and T-1834 (use) lanes; a lane that stops making progress could offer that same split.
  Done when: a lane flagged stalled can run `fm task split`, which creates two child tasks, each starting from the preserved worktree, and the parent closes as split.

- **Reopen the closed task whose commit turned main red** — FIX — value 4 — effort M — risk low — category: CI
  Why: the user asked that the session-start CI line stop pointing at a closed task and say what to do ("fix it first" was wrong). The fix is to link the red run to the owning task and reopen it with the failing line.
  Done when: a red CI run on main is matched to the task that owns the breaking commit, the session line reads "T-xxxx closed, reopened, failing: <first failing line>", and the task is back in the queue.

- **Rerun only what failed last time with `fm test --last-red`** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: CI's 20-minute cap hid a hanging test class until run.py learned to name it, and the suite is flaky under parallel load (browser, bench, fake git). Rerunning the last failure set is the cheap first step. Assumption: run.py records per-class results.
  Done when: `fm test --last-red` runs only the classes that failed or hung in the previous run, naming any hang with its stack.

- **Run Desktop without the tray and say how to get it back** — FIX — value 2 — effort S — risk low — category: desktop
  Why: T-0325 has been blocked on `libappindicator-gtk3`; a blocked FEATURE shouldn't leave Desktop with no signal at all.
  Done when: Desktop starts without the library, shows window-title state and notifications, and `fm doctor` prints the exact `pacman` line to restore the tray.

- **Wild: Rehearse the round and show the user-only list first** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: pillar 7 puts what only the user can do (the blocked T-0325, T-0335, T-0352, T-0418) in the final report, after the user could have acted in parallel. A dry-run from the queue and journal could produce it up front. Assumption: blocked items carry their unblock condition.
  Done when: the first message of a forever round lists every item that will need the user, each with the exact command or step, before any lane starts.

- **Wild: Keep a pre-gated integration branch of everything proved but unpushed** — FEATURE — value 4 — effort L — risk med — category: shipping
  Why: pushes land in batches (T-1785, T-1830..T-1834, T-1839, T-1803), so batch conflicts and a red main are only discovered at push time.
  Done when: `fm ship --preview` shows a branch merging all proved tasks with its own gate result, and the push to main is a fast-forward of that branch.

- **Wild: Turn every stalled or killed lane into a stall-classifier fixture** — CLEAN — value 3 — effort M — risk low — category: reliability
  Why: stalls, hung test classes and usage-limit waits are each fixed one at a time (run.py hang naming, the watchdog for headless runs). Assumption: lane transcripts are kept long enough to snapshot.
  Done when: a killed or stalled lane writes a redacted fixture that the stall-classifier tests replay, and the suite fails if the classifier calls it healthy.

- **Raise a lesson's confidence only when recall preceded a first-time pass** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: T-0217 is deferred, and T-1865 shows that unmeasured matching is unsafe. This gives lessons a measured value and lets unused ones decay.
  Done when: each lesson shows recalled, passed-first-time and wrong counts in `fm lessons`, and one with a 0% pass rate over ten recalls stops being injected.
