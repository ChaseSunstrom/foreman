# Brainstorm — lens: beautiful UI and motion

- **Publish a live Foreman Artifact dashboard** — FEATURE — value 5 — effort M — risk med — category: artifacts
  Why: Artifact is in the tool list with 0 references; the user asks for a cockpit UI (Frontier 11) and a "what Foreman did while you were away" view. A private claude.ai page (queue, step ladder, proof cards, fleet) is viewable from phone or any browser with no local server. Assumption: Artifact publish can be driven from a hook or `fm` child, and the page may carry sanitized data only.
  Done when: `fm artifact publish` returns a URL whose page shows the current task, its steps with evidence state and the queue, and re-running after `fm task step` changes the step state on the page.

- **Make the page's comments and buttons steer the queue** — FEATURE — value 5 — effort M — risk med — category: artifacts
  Why: ArtifactComments and "ask Claude" from the page are unused. A "defer", "reorder", "approve ask" or "this looks wrong" button on a card becomes an `fm` inbox capture, so the phone steers Foreman. This answers the user's complaint that it sits idle. Assumption: comments reach the session through a channel Foreman can read (Monitor or SendMessage).
  Done when: a comment on a queue card in the Artifact appears as a captured inbox item (T-id) within one drive cycle, linked to that card's task.

- **Drive the band from Monitor instead of send-keys** — PERFORMANCE — value 4 — effort M — risk low — category: motion
  Why: `fm bus` wakes idle sessions by typing into tmux panes, which is fragile and invisible. Monitor streams a background command's lines as notifications, so a `fm watch --stream` process can push step changes, guard blocks and ask arrivals with no polling and no hook latency. The band and pane then animate from real events. Assumption: Monitor notifications reach an idle session.
  Done when: a state change made from another session shows in the first session's band within 2 s with no tmux send-keys involved.

- **Ship a motion grammar for step transitions** — FEATURE — value 4 — effort S — risk low — category: motion
  Why: The user reports that the agent starts working on different steps without updating the step in the band (T-0759). Motion should explain state. Define a few durations and easings: a step slides to active, a check draws on evidence, a mismatch pulses amber when the edited files belong to a different step. Respect reduced motion. Assumption: the foreman-ui mod can animate band segments.
  Done when: running `fm task step` produces a captured frame sequence in `fm smoke` showing the transition, and an edit to files outside the active step's footprint sets the amber mismatch state.

- **Render reviewer findings through ReportFindings** — FEATURE — value 4 — effort S — risk low — category: native UI
  Why: ReportFindings gives typed findings rendered by the host UI, but Foreman's reviewer subagents (and the stalled T-0034 audit) return prose. Native cards with severity, file:line and click-through beat a text wall, and the typed shape feeds the eval inbox directly. Assumption: ReportFindings is callable from a subagent or the main thread after review.
  Done when: a reviewer run on a seeded-bug diff displays findings as typed host-rendered items and the same records land in the ledger with file and line.

- **Push only the moments that need the human** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: `fm notify` runs a user shell command; PushNotification is unused. Wire one pattern: an ask, a blocked queue or a finished milestone sends one push with a one-line result and approve/defer wording, and nothing else. Quiet by default, with a daily cap. Assumption: PushNotification works from unattended runs.
  Done when: an overnight run that hits an ask produces exactly one push containing the task id and question, and a run with no ask produces none.

- **Animate a pace-aware idle state** — FIX — value 4 — effort S — risk low — category: states
  Why: "make sure it doesn't sit idle like it is" (T-0758). An idle band is currently just static text. Make idle an explicit state with a reason (waiting on ask, waiting on lane, queue empty, paused) and a slow breathing glyph. Unexplained stillness becomes impossible, and the reason is the one to act on. Assumption: the drive loop can name its wait reason.
  Done when: every state where no tool call has occurred for 60 s shows a named reason in the band and the pane, and a test fails if the state is blank.

- **Open the cockpit as a Claude Docs checklist** — FEATURE — value 3 — effort S — risk med — category: shared docs
  Why: Claude Docs are shared editable docs and unused. A milestone's criteria as an editable doc lets the user tick, reword or strike a criterion on a phone, and Foreman reads the edits as steers (the checked-criteria immutability rule applies). Assumption: docs are readable from the CLI side.
  Done when: striking a criterion in the doc results in that criterion marked dropped in the task with the user's edit cited.

- **Wild: Make the ScheduleWakeup cadence visible as a heartbeat ring** — FEATURE — value 3 — effort S — risk low — category: motion — wild
  Why: /loop self-paced wakeups are unused. Show a thin ring around the band's glyph that fills toward the next scheduled wake, so a sleeping Foreman looks alive and the user can see when it will next act.
  Done when: while a ScheduleWakeup is pending, the band shows a countdown ring that reaches full at wake time and resets.

- **Wild: Turn the Artifact into a time-lapse "night reel"** — FEATURE — value 4 — effort M — risk low — category: delight — wild
  Why: The user runs overnight and release lanes. Compose the ledger into a 20-second scrubbable reel in an Artifact: each task a tile that flies in, ticks its checks, and lands in a "shipped" row, with failures shown as a dim wobble. A morning view people would screenshot. Assumption: the ledger has timestamps per event, as the replay ideas imply.
  Done when: opening the reel after a night run plays one tile per finished task in timestamp order and scrubbing to a tile shows its proof card.

- **Wild: Colour the whole terminal's accent by guard posture** — FEATURE — value 2 — effort S — risk low — category: ambient — wild
  Why: Foreman runs in bypass mode and the user cares about the guard. A subtle statusline accent that shifts from calm teal to amber to red as irreversibility risk rises (pushes, deletes, network) gives peripheral awareness without a prompt.
  Done when: the statusline accent changes within one tool call of a guarded action category appearing and returns to baseline after the task closes.

- **Add a first-class "models" strip to the fleet deck** — FEATURE — value 3 — effort S — risk low — category: fleet
  Why: The user just asked whether Foreman can spawn lower-model agents (T-0755); the Agent tool takes per-call `model` and `effort`. Show each lane as a chip with its model and effort and a cost tick, so the user sees "haiku, low" on scouts and sees the routing working, and can tap a chip to pin it.
  Done when: the pane shows model and effort for every live lane, and pinning a chip changes the next spawn's parameters in the ledger.

- **Show worktree moves as a visible transition** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: EnterWorktree/ExitWorktree move the main thread, and the lane model already uses worktrees. A short slide in the band and a branch label make "where am I working" legible, which addresses step and location confusion.
  Done when: entering a worktree changes the band's location label and shows a transition, and exiting restores it.

- **Wild: Let the user draw on the Artifact queue to reorder** — FEATURE — value 4 — effort M — risk med — category: artifacts — wild
  Why: The user asked for "reordering of operations" and for grouping things into one task or milestone (T-0757). A drag-to-reorder, drag-to-merge board on the page, saved to ArtifactData and applied by the drive loop, makes that spatial instead of a command.
  Done when: dragging one card onto another in the Artifact merges them into one milestone and the queue shows the same grouping after the next sync.
