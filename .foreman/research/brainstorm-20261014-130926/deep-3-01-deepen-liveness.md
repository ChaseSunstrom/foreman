# Brainstorm — lens: deepen: liveness

- **Unify arming proof into one liveness ledger** — FEATURE — value 5 — effort M — risk low — category: liveness
  Why: the existing list has ~8 near-duplicate "prove armed / receipt / canary" ideas, and round 1 notes the monitor's arming is unverified. Merge them: every wake path (monitor, tmux, bus piggyback, drive nudge) writes `sent`, `seen`, `acted` rows to a single `state/liveness.jsonl`; `fm doctor` and `fm status` read it.
  Done when: a test sends a wake through each path and `fm liveness` shows three timestamps per wake, with unacked rows flagged after N seconds.

- **Degrade wakes along a ladder, automatically** — FEATURE — value 5 — effort M — risk med — category: liveness
  Why: the wake already prefers the monitor and falls back to tmux, but the fallback is static. Use the ledger so a path that missed its ack is demoted: monitor, then tmux, then piggyback on the next hook output, then a push notification, then park the task as "needs you".
  Done when: a fake monitor that never acks causes the next wake to use tmux, then piggyback, and a test asserts the demotion order and that one wake never delivers twice.

- **Stamp each wake with an idempotency key** — FIX — value 4 — effort S — risk low — category: delivery
  Why: with several wake paths and fallbacks, a message can arrive twice (monitor plus tmux) and make the model repeat work. assumption: duplicates aren't deduped today.
  Done when: sending the same wake via two paths yields exactly one model-visible message, shown in a test transcript.

- **Detect a stalled session from the outside** — FEATURE — value 4 — effort M — risk med — category: watchdog
  Why: the Stop hook handles drive-on-stop, but a hung tool call or a rate-limit wait never reaches Stop. A tiny sidecar compares last-hook-activity time against the queue state and an active task, and nudges, notifies, or just records a "stalled since" mark.
  Done when: a session with an active task and no hook events for the threshold produces a stall record and a single notification, with no false positive while a long Bash call is running.

- **Make the stall threshold learn from history** — FEATURE — value 3 — effort S — risk low — category: watchdog
  Why: a fixed idle timeout either spams during long builds or misses real hangs. Per-tier p95 gaps between hook events are already derivable from the session logs. assumption: the logs are retained long enough.
  Done when: the watchdog's threshold for an L task differs from an S task, and the two values appear in `fm doctor`.

- **Handoff a wedged session to a fresh one with the step pointer** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: Foreman already resumes at the exact step after `/compact`, so the same pointer could seed a replacement session when a stall persists past the nudges. Distinct from the deferred crash-recovery item because it triggers on a stall, with no crash needed.
  Done when: a simulated dead session leads to a new `claude -p --resume`-style child that picks up at the recorded step and the old one is marked superseded.

- **Reap orphans on every session start** — CLEAN — value 3 — effort S — risk low — category: hygiene
  Why: watchers, lane processes and tmux wake helpers can outlive their sessions, and the ledger knows which sessions are alive. Sweep at SessionStart and in `fm tidy`.
  Done when: after killing a session's parent, the next SessionStart removes its watcher and `fm doctor` shows zero orphans.

- **Add a one-line liveness verdict to the SessionStart greeting** — FEATURE — value 3 — effort S — risk low — category: visibility
  Why: the user can't tell whether the monitor armed, which is the known gap. The greeting says "wakes: monitor armed (ack 2s)" or "wakes: tmux only" so a silent fallback is visible at once.
  Done when: a new session's first context contains exactly one liveness line matching the ledger state.

- **Replay the liveness ledger in a time-travel view** — FEATURE — value 2 — effort M — risk low — category: visibility
  Why: when something went idle overnight, the user wants to see when and why. `fm page` already renders self-contained HTML, so add a timeline of wakes, acks, demotions and stalls.
  Done when: `fm page --liveness` outputs a page whose timeline matches the ledger rows for a seeded fixture.

- **Wild: Run a chaos monkey for liveness in CI** — FEATURE — value 4 — effort L — risk low — category: testing
  Why: wild. Spawn a throwaway session in a fixture repo, randomly kill the watcher, drop acks, delay hooks, and fill the context, then assert the queue still drains or escalates. It goes beyond the nightly wedge canary by randomizing the failure and recording a seed for replay.
  Done when: a seeded run with a killed watcher ends with a recorded escalation, and re-running the same seed reproduces it.

- **Wild: Let sessions heartbeat to each other as a peer mesh** — FEATURE — value 3 — effort L — risk high — category: fleet
  Why: wild. Lanes and the planner session watch each other's heartbeats, so any live peer can restart or notify about a dead one. This removes the single sidecar as a point of failure, and it also sets up the deferred fleet registry work.
  Done when: killing one lane makes another lane's ledger record "peer dead" and trigger exactly one takeover proposal.

- **Wild: Turn the queue's idle time into a spoken or haptic heartbeat** — FEATURE — value 2 — effort M — risk low — category: ambient
  Why: wild. A long unattended run emits a quiet periodic "alive, step 4 of 9" line to the phone through the existing push channel, or a status-line glyph that pulses. Silence then becomes meaningful, because the user knows a missing pulse means a stall.
  Done when: with the option on, a running task emits a heartbeat at the set interval, and it stops with the task.

- **Gate the push on liveness confidence** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: round 1 added a push when an ask is open or the queue drains, but if the monitor isn't armed the user may never learn the session is waiting. Use ledger confidence to decide: push earlier when delivery is unproven, stay quiet when acks are healthy.
  Done when: with no acks in the ledger the push fires at the short threshold, and with fresh acks it fires at the long one, in tests.

- **Check liveness in the install and release gate** — CLEAN — value 3 — effort S — risk low — category: release
  Why: arming is only verified in new sessions, so the install gate can't catch a monitor that stops arming after a Claude Code update. Run a headless canary in `fm doctor --live`, and make the release checklist (T-0431) require it.
  Done when: `fm doctor --live` starts a throwaway session, observes the monitor's first event, and exits nonzero if it doesn't arrive within the timeout.
