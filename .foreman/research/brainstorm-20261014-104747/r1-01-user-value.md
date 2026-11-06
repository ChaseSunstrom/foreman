# Brainstorm — lens: user value

- **Route each plan step to the cheapest capable model and effort** — FEATURE — value 5 — effort M — risk med — category: orchestration
  Why: T-0755 asks for haiku/sonnet agents. Today only the scout is pinned to haiku and S-tier lanes pass "sonnet". The Agent tool takes per-call `model` and `effort`, which Foreman doesn't set.
  Done when: `fm task plan` stores model and effort per step, the spawned Agent call carries them, and a test fixture shows an S step on haiku/low and an L step on opus/high.

- **Replace tmux send-keys wakeups with ScheduleWakeup and Monitor** — FIX — value 5 — effort M — risk med — category: autonomy
  Why: T-0758 reports the session sitting idle. `fm bus` types into a tmux pane, which breaks without tmux and when the pane is focused elsewhere.
  Done when: a session with queued tasks resumes by itself after a quiet period in a no-tmux test, and the wake is logged.

- **Block edits that belong to a step other than the current one** — FIX — value 4 — effort S — risk low — category: discipline
  Why: T-0759 says Claude starts working on later steps without updating the step in the record, which breaks exact-step resume after `/compact`.
  Done when: an Edit touching files linked only to step N+1 while step N is current either advances the step or is refused with a message, covered by a hook test.

- **Push to the phone when a run needs the user or finishes** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: `fm notify` only runs a user shell command, and PushNotification is unused. The user never wants to be handed commands, and `fm night` runs unattended.
  Done when: a blocked task or finished night run triggers one PushNotification with the task id and one-line reason, rate-limited, with `fm notify` as the fallback.

- **Publish a live run Artifact that feeds comments back as captured tasks** — FEATURE — value 4 — effort L — risk med — category: cockpit
  Why: Frontier 11 asks for a live pane to see and steer from. Artifact with ArtifactData and ArtifactComments gives a private page on claude.ai that works from any device. Assumption: ArtifactComments can be read from the CLI side as described.
  Done when: `fm artifact` publishes the queue, current step and evidence, and a comment on the page appears as a captured task within one poll.

- **Render reviewer output through ReportFindings** — FEATURE — value 3 — effort S — risk low — category: review
  Why: Reviewer subagents write prose or custom files, and the host UI renders typed findings natively. T-0034's structured findings file could be this instead.
  Done when: a close-out review produces ReportFindings entries with file, line and severity, and `fm task finish` reads them to gate on high-severity items.

- **Stream gates with Monitor and stop at the first failure** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: the full suite and bench gates run to completion before Claude sees a failure. Monitor streams a background command's output as notifications.
  Done when: a seeded failing test aborts the gate run within seconds of the failure line, and the failing output reaches the model without waiting for the rest.

- **Run `fm night` as a cloud routine when the laptop is closed** — FEATURE — value 4 — effort L — risk high — category: autonomy
  Why: RemoteTrigger, `/schedule` and Agent isolation "remote" are unused, and `fm night` only works on a live machine. Assumption: the repo is on GitHub, as Foreman's is. High risk because central task records live locally.
  Done when: a scheduled cloud run takes one queued S task, pushes a branch with evidence in the PR body, and `fm` imports the result on next session start.

- **Map close-out review depth to the built-in `/code-review`, `/simplify` and `/security-review`** — FEATURE — value 3 — effort S — risk low — category: review
  Why: Foreman has its own reviewer subagent but doesn't use the built-ins, which have low to max levels and ultra cloud review. Size, tier and security-touching paths could pick the level.
  Done when: a task touching guard code gets `/security-review` evidence recorded and an S docs task gets none, shown in the close-out record.

- **Check LSP references before editing a shared symbol** — FEATURE — value 3 — effort M — risk med — category: safety
  Why: LSP has 0 references. `fm map` links tests to sources by name, which misses callers. T-0214's edit-time sentinel would pick better tests from real references.
  Done when: editing a function with callers in other files adds those files' linked tests to the step's verify list, shown in a fixture repo test.

- **Wild: dispatch tasks to sessions on other machines** — FEATURE — value 3 — effort L — risk high — category: fleet
  Why: wild. SendMessage and ListAgents can reach Remote Control sessions elsewhere. A desktop and a laptop could share one queue, with the idle one claiming the next S task.
  Done when: `fm fleet` lists sessions on two machines and a task sent to the second one finishes there, with evidence returned to the central record.

- **Wild: learn the model and effort routing from first-time-pass history** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: wild. T-0217 and the bench already record per-task pass outcomes. Combined with per-call `model` and `effort`, Foreman could find the cheapest setting that still passes per task type.
  Done when: after N recorded runs `fm cost` shows a recommended model and effort per task type with pass rate, and the router uses it only past a stated sample size.

- **Wild: a self-paced `/loop` babysitter for open PRs and CI** — FEATURE — value 3 — effort M — risk low — category: autonomy
  Why: wild. After a release to GitHub main, the session ends and nobody watches CI. ScheduleWakeup could poll and fix or capture a task on failure, then stop itself.
  Done when: after a push, a wake fires, reads CI status, captures a FIX task on a red run, and cancels the loop on green.

- **Isolate risky tasks in the main thread with EnterWorktree** — FEATURE — value 3 — effort M — risk med — category: safety
  Why: lanes use worktrees only through Agent isolation. A guard or installer change in the main thread has no cheap rollback. T-0751's task revert shows the need.
  Done when: a task tagged risky enters a worktree at start, merges only after verification passes, and exits cleanly on revert, covered by an end-to-end test.

- **Run `/skill-doctor` on Foreman's 73 skills in `fm doctor`** — CLEAN — value 2 — effort S — risk low — category: maintenance
  Why: the pack shows 73 skill files and a doctor check that already fails on self-docs, so skill drift is likely. The built-in is unused.
  Done when: `fm doctor` reports skill-doctor findings, and a seeded broken skill description turns the check red.
