# Brainstorm — lens: capability map

- **Publish a live Artifact cockpit with a round trip** — FEATURE — value 5 — effort M — risk med — category: surfaces
  Why: Frontier 11 asks for a cockpit; the user wants to steer without being handed commands, and Artifact (private HTML pages with ArtifactData and ArtifactComments) has 0 references today. Assumption: the CLI side can read and write ArtifactData while the page is open.
  Done when: `fm artifact` publishes a page showing the queue, current step and evidence, and a comment typed on the page appears as a captured T-id within one drive tick.

- **Replace idle polling with Monitor-fed wakes** — FEATURE — value 5 — effort M — risk low — category: liveness
  Why: T-0758 says "make sure it doesn't sit idle". Today the bus types into tmux panes, while Monitor streams a background command's output as notifications. Assumption: a stream from fm bus, long gates and lane completion can drive Monitor.
  Done when: with a lane running in the background, the main thread wakes within 5 seconds of the lane's completion event, with no send-keys, shown by a replayed event log.

- **Self-pace the drive with ScheduleWakeup and session crons** — FEATURE — value 4 — effort S — risk low — category: liveness
  Why: Both are unused. When the queue is blocked only on a background lane or a cooldown, the drive should schedule its own resume and not stop.
  Done when: a test with a slow fake lane shows the drive scheduling a wakeup, resuming at the exact step, and never ending a turn with queued work and no pending wake.

- **Route model and effort per call from a learned tier table** — FEATURE — value 5 — effort M — risk med — category: cost
  Why: T-0755 asks "can foreman spawn agents of lower models?". The Agent tool takes per-call `model` and `effort`, but only S-tier lanes pass "sonnet" and effort is never set. A table of step type to (model, effort) could be seeded from bench pass rates.
  Done when: `fm plan` prints a model and effort per lane, a haiku lane runs a read-only step, and the ledger records the choice and its outcome.

- **Make reviewers return typed ReportFindings** — FEATURE — value 4 — effort M — risk low — category: review
  Why: Reviewers return prose today, while T-0034 (`fm audit`) wants structured findings. The host UI renders ReportFindings natively and Foreman can parse them.
  Done when: a reviewer run produces findings with file, line, severity and a reproducer field, and `fm task finish` blocks on an open blocker finding.

- **Wrap the built-in /code-review, /simplify and /security-review as tiered done-gate lenses** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: Foreman's own reviewers duplicate commands the host already maintains and improves. The level (low to max) could scale with task tier, with /skill-doctor run on skill edits. Assumption: these are callable from a Foreman-driven turn.
  Done when: an L task close runs /code-review at a higher level than an S task, and each run is recorded as evidence with its level.

- **Move cloud-safe routines to RemoteTrigger and /schedule** — FEATURE — value 4 — effort M — risk med — category: unattended
  Why: `fm night` needs the machine awake. Cloud routines on a cron could run a Claude Code version canary, a nightly doc and gate audit, or a stale-queue groom. Local-only state is the open problem. Assumption: routines can read a synced repo.
  Done when: one scheduled cloud routine runs with the laptop off and its findings arrive as captured tasks.

- **Replace tmux send-keys with SendMessage and ListAgents** — FEATURE — value 4 — effort M — risk med — category: fleet
  Why: Typing into panes breaks when no tmux pane exists and cannot reach other machines. Native messaging reaches local, cloud and Remote Control sessions, which also serves T-0335 and the idea of fleets across machines.
  Done when: `fm bus` wakes a session that is not in tmux, and ListAgents output appears in the fleet pane.

- **Push-notify on needs-you moments with a deadline default** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: `fm notify` runs a user shell command, which the user must configure. PushNotification reaches the phone with no setup. Assumption: PushNotification can be called from a Stop or Notification hook path via the model.
  Done when: a blocked-on-user event pushes one message naming the task, the question and the default that will be taken at the deadline.

- **Back blast sketches and hallucination checks with LSP** — FEATURE — value 4 — effort M — risk low — category: code intelligence
  Why: Foreman uses grep and `fm map`, while LSP gives real definitions and references. Plan footprints, symbol-existence checks on new calls, and safe renames all follow from it.
  Done when: a plan's footprint lists callers found through LSP references, and a diff calling a nonexistent method is flagged before verification.

- **Wild: Make the plan a Claude Doc the user edits like tracked changes** — FEATURE — value 3 — effort M — risk med — category: collaboration — wild
  Why: assumption: shared editable docs let the user reorder steps or strike a criterion from a phone, and Foreman reads the diff as a steer (T-0757 asks for reordering).
  Done when: striking a step in the doc causes the next drive tick to skip it and note the steer in the ledger.

- **Wild: Ship a saved named Workflow the user can invoke with one word** — FEATURE — value 3 — effort M — risk med — category: orchestration — wild
  Why: Workflow cannot be launched without the user's words, but a saved, named workflow they ask for is allowed. A "fm-verify" workflow would run reviewer fan-out, a negative twin and a mutation probe as deterministic steps.
  Done when: the user says the workflow's name once and it runs the fixed steps, returning one structured verdict.

- **Wild: Gate L tasks by running them in a cloud "remote" worktree race** — FEATURE — value 3 — effort L — risk high — category: parallelism — wild
  Why: Agent isolation "remote" is unused. A hard task could race a local lane against a cloud lane while the laptop sleeps, and the gate winner merges. Assumption: cloud lanes can reach the repo.
  Done when: one task runs both lanes, the gates pick a winner, and the loser's diff is archived.

- **Wild: Turn the Artifact page into a phone approval deck** — FEATURE — value 4 — effort M — risk med — category: surfaces — wild
  Why: The ask queue blocks unattended runs. A swipeable deck of pending asks on a private page, answered through ArtifactData, would clear blocks from anywhere. Assumption: the page can write answers that the CLI polls.
  Done when: tapping Approve on the page unblocks a waiting task and records a content-bound grant in the ledger.
