# Brainstorm — lens: reliability

- **Wake sessions through SendMessage, with send-keys as the fallback** — FIX — value 4 — effort M — risk med — category: orchestration
  Why: `fm bus` wakes idle sessions by typing into a tmux pane. That fails when the pane is mid-typing, the session isn't in tmux, or it's on another machine. SendMessage and ListAgents reach local, cloud and Remote Control sessions, and the pack shows 0 uses of either.
  Done when: a test wakes a session that has no tmux pane through SendMessage, and a session in tmux still wakes via send-keys when SendMessage is unavailable.

- **Hold a per-step ScheduleWakeup heartbeat so the drive can't sit idle** — FEATURE — value 5 — effort M — risk med — category: liveness
  Why: T-0758 ("make sure it doesn't sit idle like it is") is the user's own complaint, and ScheduleWakeup is unused. Each step arms a wakeup that fires if the ledger hasn't advanced, then re-enters `fm drive`. A clean done or an explicit block disarms it.
  Done when: a test session that stops after step 2 of 4 without blocking resumes at step 3 on its own, with a ledger event naming the wakeup as the cause.

- **Block edits that belong to a later step while the pointer is behind** — FIX — value 4 — effort M — risk med — category: step sync
  Why: T-0759 reports work starting on other steps without updating the step in the plan. PreToolUse maps the edited path to the plan's declared footprint. If it belongs to step N+1 and the pointer is on N, it returns a deny whose text carries the exact `fm task step` command to run.
  Done when: editing a file owned by step 3 while on step 2 is denied with the fix command, and the same edit passes after the pointer moves.

- **Stream long gates through Monitor instead of blocking** — FEATURE — value 4 — effort M — risk low — category: gates
  Why: Monitor turns a background command's output into notifications, and Foreman uses it 0 times. The full suite and `fm smoke` become non-blocking, a first red line interrupts the builder early, and a hung gate shows up as silence instead of a wedged turn.
  Done when: a failing gate's first `✗` line reaches the session as a notification before the command exits, and a gate with no output for N seconds raises a stall event.

- **Reconcile background agents on resume with ListAgents** — FIX — value 4 — effort S — risk low — category: resume
  Why: Agent calls are background by default, and Foreman resumes at the exact step after `/compact`. A lane that finished or died during the gap can be re-spawned or double-counted. Resume lists live agents and matches them to the lanes in STATE.
  Done when: after a simulated compact with one lane still running and one dead, resume adopts the first and respawns only the second.

- **Make reviewers return typed findings through ReportFindings** — FEATURE — value 3 — effort M — risk med — category: review
  Why: Reviewer verdicts are parsed from prose today (precision tracking and "reproducible findings" already exist in the commits). The host-typed ReportFindings payload removes the parse step and renders in the UI. Assumption: the tool is callable from subagents.
  Done when: a reviewer run produces a findings record that `fm` ingests without regex, and a malformed prose-only reply is flagged as a reviewer failure.

- **Spawn with per-call model and effort, and fall back on failure** — FEATURE — value 4 — effort S — risk low — category: delegation
  Why: T-0755 asks for lower-model agents, and the Agent tool accepts `model` and `effort` per call. Add a spawn wrapper with a fallback chain (haiku → sonnet → inherit) that triggers on a limit or model-unavailable error and logs which tier produced the result.
  Done when: a forced model-unavailable error on a haiku spawn retries on sonnet, the ledger records both attempts, and the S-tier lane still returns a result.

- **Push to the phone when a run stalls or needs the user** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: `fm notify` runs a user-configured shell command, which is a silent no-op if misconfigured. PushNotification is built in and needs no config. Fire it on blocked, stalled-past-heartbeat and night-run-died events, with a dedupe window.
  Done when: a blocked task triggers exactly one push per window, and the same event with PushNotification unavailable falls back to `fm notify`.

- **Publish a heartbeat Artifact that survives the terminal** — FEATURE — value 3 — effort M — risk med — category: observability
  Why: Artifact has a shared db and comments that reach Claude, with 0 references. Foreman writes queue, step pointer and last-pulse time into ArtifactData, so a crashed terminal or sleeping laptop still leaves a page showing when it last moved. Assumption: an artifact can be updated from the CLI side without a prompt. Per the harness rules, publishing sends content to an external service, so it must be opt-in and redacted.
  Done when: with the setting on, the page's last-pulse time advances each step, and with it off no artifact call is made.

- **Wild: Let artifact comments steer the queue** — FEATURE — value 3 — effort M — risk high — category: remote control
  Why: ArtifactComments are sent to Claude. A comment like "defer T-0034" or "stop after this step" typed from a phone becomes a captured inbox item that goes through Foreman's normal intake and guard. A comment can never run a command directly. Assumption: this is wild.
  Done when: a comment saying "pause" results in `fm pause` through intake, and a comment containing a shell command is captured as text only.

- **Wild: Fail over to an `isolation: "remote"` lane when the local host dies** — FEATURE — value 3 — effort L — risk high — category: resilience
  Why: The local machine can sleep, hit a usage limit or lose the network mid-queue. A cloud lane runs one self-contained S/M task from a pushed branch, and the result returns as a patch for the normal gate. This is wild and assumes cloud isolation can reach the repo.
  Done when: a task marked remote-eligible runs in a cloud agent, and its diff is gated locally before merge.

- **Wild: Run a canary cron that deliberately wedges a throwaway session** — FIX — value 3 — effort M — risk low — category: self-test
  Why: Reliability claims for the heartbeat, wake and resume paths are untested against real failures. A CronCreate job sets up a fixture session, stalls it, and expects the heartbeat or bus to revive it within a deadline. If it doesn't, it pushes an alert. Assumption: session crons only live while the session is open, so this runs in the night/serve process.
  Done when: breaking the wake path in a test build makes the canary report failure within one cycle.

- **Wild: Add a "pulse" step in `fm doctor` that races all liveness paths** — CLEAN — value 2 — effort S — risk low — category: diagnostics
  Why: Liveness now has several redundant paths (heartbeat wake, SendMessage, send-keys, push). `fm doctor` fires each at a dummy session and prints which ones work on this machine, so a degraded path is visible before an unattended run.
  Done when: `fm doctor` lists each wake path as ok or failed, and disabling tmux flips only the send-keys row.
