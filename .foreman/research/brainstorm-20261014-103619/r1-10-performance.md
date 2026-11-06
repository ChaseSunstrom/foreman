# Brainstorm — lens: performance

- **Wake idle sessions with ScheduleWakeup, not tmux keystrokes** — FEATURE — value 5 — effort M — risk med — category: drive
  Why: T-0758 ("make sure it doesn't sit idle"), and `fm bus` wakes sessions by `send-keys`, which only works inside tmux. Assumption: a self-paced wakeup survives where a pane doesn't.
  Done when: a queued session with no tmux pane resumes the next queued task within the set interval after going idle, shown in the ledger.

- **Fix while the suite is still running** — FEATURE — value 5 — effort M — risk med — category: latency
  Why: Monitor is unused (0 references). Gates run to completion before the builder sees the first red test. Streaming each failure as it happens starts the fix sooner.
  Done when: on a seeded suite with an early failure, the first edit happens before the run exits, and the final gate run still passes.

- **Re-review by continuing the same reviewer** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: SendMessage and ListAgents are unused. A fresh reviewer re-reads the whole diff after every fix round. Assumption: a finished subagent can still be messaged; if not, keep it alive until `fm task finish`.
  Done when: the second review round's token count is under half the first on a measured task, and it still finds a planted regression.

- **Escalate-on-fail model and effort ladder** — PERFORMANCE — value 5 — effort M — risk med — category: cost
  Why: T-0755 asks for haiku/sonnet lanes. The Agent tool takes a per-call `model` and `effort`, but only S-tier lanes pass "sonnet" today. Start mechanical steps on haiku-5-5 at low effort and escalate one rung per failed gate.
  Done when: `fm bench` shows a lower token cost with an equal pass rate on mechanical tasks, and every escalation is logged with the failing gate that caused it.

- **Save one named Workflow for review fan-out** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: Workflow is unusable without the user's words, so ask once through `fm ask` and store the durable opt-in. After that the fan-out is a deterministic script, and the main thread no longer pays tokens to orchestrate it.
  Done when: a stored named workflow runs the reviewer panel with zero main-thread orchestration turns, and revoking the opt-in disables it.

- **Return reviewer findings through ReportFindings** — FEATURE — value 4 — effort S — risk low — category: tokens
  Why: ReportFindings is unused, and reviewer prose is re-read and re-parsed by the main thread. Typed findings are rendered by the host and parsed once. Assumption: a subagent can call it.
  Done when: reviewer output reaches the ledger as structured records with no prose parsing, and the pane lists them.

- **Burst heavy lanes to isolation "remote"** — PERFORMANCE — value 3 — effort L — risk high — category: lanes
  Why: remote isolation is unused. Under local load, lanes and gates queue up behind each other. Assumption: the repo can be reached from the cloud, so gate this on a per-project opt-in and the secrets scan.
  Done when: with local load over the threshold, an opted-in lane runs remotely and merges back with the same gate results as a local run.

- **Spend fast mode only on the critical path** — PERFORMANCE — value 3 — effort S — risk low — category: latency
  Why: fast mode is a toggle and Foreman never touches it. Intake, the done-gate close-out and blocking steps are latency-bound, while background lanes are throughput-bound.
  Done when: time-to-close on a benchmarked task drops with fast mode on only for the critical-path steps, at lower cost than fast mode everywhere.

- **Use `/code-review` levels instead of a custom reviewer on S tasks** — CLEAN — value 3 — effort S — risk med — category: reuse
  Why: Foreman maintains its own reviewer, while the built-in offers low through max levels. Map tier to level and compare catch rates from the existing check track records.
  Done when: for S tasks the built-in at low level matches the custom reviewer's catch rate on the planted-bug set, or the mapping is rejected with the numbers.

- **Navigate by LSP first** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: LSP is unused (0 references), so builders grep and read whole files to find a definition. Add it to the builder/recon agents and run an A/B on read tokens. This is a prompt change, so it adds no hook latency.
  Done when: the A/B shows fewer read tokens per task with LSP-first, with no drop in first-pass rate.

- **Wild: Pre-warm the day from the user's habits with CronCreate** — FEATURE — value 4 — effort M — risk low — category: scheduling — wild
  Why: assumption: the user starts at similar times. A cron fires shortly before then to pre-plan the top queued tasks, refresh `fm map` and warm gate caches, so the first request starts with a plan ready.
  Done when: the first task after a scheduled window skips planning and its time-to-first-edit falls versus baseline.

- **Wild: Show a live flame graph on an Artifact, with comments as steering** — FEATURE — value 3 — effort M — risk med — category: observability — wild
  Why: Artifact and ArtifactComments are unused. Publish where each task's wall-clock and tokens went, and a comment such as "stop spending on recon" becomes a captured queue item. Assumption: an Artifact never carries unredacted ledger content.
  Done when: the page updates during a run, and a comment on it appears as a captured task within a minute.

- **Wild: Run a work-stealing census with ListAgents** — FEATURE — value 3 — effort L — risk high — category: fleet — wild
  Why: assumption: the user runs several local and cloud sessions. An idle session takes an unclaimed queued task from a busy one, using a lease, so no session sits idle while others have a backlog.
  Done when: two sessions on one queue never run the same task, and an idle session picks up a task within the interval.

- **Wild: Ping the phone on a blocking ask and log human latency** — FEATURE — value 3 — effort S — risk low — category: attention — wild
  Why: PushNotification is unused and `fm notify` only runs a shell command. A blocking ask pushes once, the queue parks that task and continues, and a ledger of answer times tunes when to interrupt.
  Done when: a blocking ask produces one push, other tasks keep running while it waits, and the answer latency shows up in the report.
