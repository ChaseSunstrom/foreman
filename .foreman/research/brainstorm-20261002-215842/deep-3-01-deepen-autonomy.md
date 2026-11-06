# Brainstorm — lens: deepen: autonomy

- **Replay user yeses as scoped standing grants** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: every protected-core edit needs a yes (one per task) and a plugin update needs its own; the decision-log idea is only a record. Grants make it a rule: "yes to edits under `hooks/` for this queue, expires at queue end", keyed by path glob, action class and expiry.
  Done when: after approving a protected-core edit with "for this queue", a second task's edit to the same glob runs with no prompt, and `fm grants` lists it with its expiry.

- **Add a queue preflight that batches every predictable yes** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: combines "batch yeses at session start" with "ask once for the whole queue". Foreman reads the queued briefs, predicts which will touch the protected core, run risky commands or need a plugin update, and presents one approval card.
  Done when: starting drive on a 5-task queue shows one card listing predicted gated actions; approving it means no prompts on those actions, and unpredicted ones still prompt.

- **Park blocked tasks and keep driving** — FEATURE — value 5 — effort M — risk low — category: autonomy
  Why: T-0176 showed drive stopping with queue work left, and any pending yes stalls the session for hours. A task that needs a yes should go to a "waiting on you" lane while Foreman moves to the next independent task.
  Done when: with task A blocked on an approval, drive finishes B and C, then shows A in the digest as "needs your yes".

- **Write a morning digest with a one-keypress review** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: the overnight idea in the list is a bare digest. Make it a pane card: finished, parked, decisions Foreman made on the user's behalf, and gate/time stats. Each line gets approve, revert or promote-to-rule.
  Done when: after an unattended run the first prompt shows a digest, and "revert" on a line restores the task's pre-change snapshot.

- **Add a reliability budget for autonomous decisions** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the "reliability budget for yeses" idea only counts prompts. Add a per-queue budget of irreversible actions, wall-clock hours and tokens; when it's exhausted Foreman parks work and digests instead of stopping dead.
  Done when: setting `budget.hours=2` makes drive stop starting tasks after 2 h, write a digest, and say which limit it hit.

- **Replace the session-wide drive loop with a self-healing watchdog** — FIX — value 4 — effort M — risk med — category: watchdog
  Why: the drive stop bug, the 2 h backstop and T-0087 (hook failure circuit breaker) point to the same need: detect a stalled or looping session and recover without the user. The watchdog should diagnose, then re-prompt, compact or skip the task.
  Done when: a simulated stall (turn ends with queue work left) is detected within one Stop event and the next task starts, with a log line saying why.

- **Escalate by risk class, not by every edit** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: T-0078/T-0079 and "every protected-core edit needs a yes" show prompts are triggered by location, not danger. Classify actions (reversible within a git snapshot vs. outward-facing) so only the irreversible ones ask. Builds on T-0086 snapshots.
  Done when: a snapshot-covered protected-core edit auto-proceeds with a rollback handle, while `git push --force` still asks.

- **Wild: let Foreman pre-argue its own yes requests with a devil's-advocate subagent** — FEATURE — value 3 — effort M — risk med — category: autonomy wild
  Why: assumption: the user would rather not be asked at all. A cheap Haiku reviewer checks the proposed action against standing grants and the brief; only a disagreement reaches the user.
  Done when: an in-scope action is cleared by the reviewer with no prompt, and a deliberately out-of-scope action is escalated with the reviewer's objection shown.

- **Wild: add a "ghost shift" that works the inbox on a timer while the user is away** — FEATURE — value 4 — effort L — risk high — category: autonomy wild
  Why: T-0077 (an env var marking orchestrator-driven sessions) is the missing piece for headless runs. A scheduled session picks up the inbox, works on a throwaway branch, and leaves a digest and a diff, never touching main.
  Done when: a scheduled run processes one inbox item on a branch, leaves main untouched and queues a digest.

- **Wild: add a "trust dial" slider in the pane from hands-on to hands-off** — FEATURE — value 3 — effort S — risk low — category: autonomy wild
  Why: it replaces the "just do it" mode that hides Foreman with something visible. One control sets grant breadth, budget, review depth and verbosity together, and reacts to a bad outcome by dropping a notch.
  Done when: moving the dial changes the active grants and budget shown in `fm ui --json`, and a failed audit lowers it one step.
