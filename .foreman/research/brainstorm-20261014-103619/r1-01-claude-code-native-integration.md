# Brainstorm — lens: Claude Code native integration

- **Publish a live Artifact cockpit with a two-way ArtifactData channel** — FEATURE — value 5 — effort M — risk med — category: Artifact
  Why: Artifact is unused and offers a shared db, comments to Claude, and "ask Claude" from the page. The user's Frontier 11 cockpit (see/steer/rewind plan and fleet) is exactly this, reachable from the phone with no server. Assumption: the CLI side can write ArtifactData on each task transition.
  Done when: `fm artifact publish` yields a page showing the queue, current step and lanes, and an edit made on the page (reorder, defer) shows up in `fm task list` within one hook cycle.

- **Route Artifact comments into the inbox** — FEATURE — value 4 — effort S — risk low — category: Artifact
  Why: The user's pending items (T-0755 to T-0760) are loose chat messages that get truncated ("also, the …"). A comment on a published task card is a typed, task-anchored capture with no truncation. Assumption: ArtifactComments are readable from the session.
  Done when: a comment on task T-0758's card creates a captured item linked to T-0758, visible in `fm inbox`.

- **Replace tmux send-keys wakeups with Monitor streams** — PERFORMANCE — value 5 — effort M — risk med — category: Monitor
  Why: `fm bus` types into tmux panes, which is fragile, and the user said "make sure it doesn't sit idle". Monitor streams a background command's output as notifications, so idle sessions wake on queue or lane events natively. Assumption: Monitor can run an `fm bus tail` process per session.
  Done when: with tmux absent, a lane finishing wakes the idle main session within 5 s and the ledger records the wake source as Monitor.

- **Add an idle watchdog on ScheduleWakeup** — FIX — value 5 — effort S — risk low — category: idle
  Why: "can you make sure it doesnt sit idle like it is" is a direct complaint. Before any stop with a non-empty runnable queue or an unfinished step, the Stop hook arms ScheduleWakeup (self-paced /loop) so the session resumes without the user.
  Done when: a test with a runnable queue and a Stop event shows a wakeup armed, and a session left alone for 10 min still advances a step.

- **Push to the phone only for decisions and finishes** — FEATURE — value 4 — effort S — risk low — category: PushNotification
  Why: `fm notify` only runs a user shell command. PushNotification gives native phone/desktop push, and the user never wants to be handed commands. Assumption: push is budgeted to avoid spam (asks, blocked, done-of-L).
  Done when: a blocked ask triggers one push containing the question and the default, and routine step completions trigger none.

- **Schedule the overnight work as cloud routines** — FEATURE — value 4 — effort M — risk med — category: RemoteTrigger
  Why: `fm night` and the dream and red-team ideas need an open laptop; /schedule routines run on a cron in the cloud. The first slice is the nightly guard fuzz and the queue groom, which need only a repo clone. Assumption: routines can clone from the user's GitHub remote.
  Done when: `fm night --cloud` registers a routine and the next morning's ledger holds its findings file.

- **Pick model and effort per step through the Agent tool's own parameters** — PERFORMANCE — value 5 — effort S — risk low — category: Agent model
  Why: T-0755 asks "can foreman spawn agents of lower models like haiku/sonnet?". Today only S-tier lanes pass "sonnet" and scout is pinned to haiku. Agent accepts `model` and `effort` per call, so a plan step's tier can carry both. Cost and speed follow directly.
  Done when: each plan step carries model and effort fields, spawns use them, and the ledger shows haiku used for at least one read-only step in a replay.

- **Render reviewer output through ReportFindings** — FEATURE — value 3 — effort S — risk low — category: ReportFindings
  Why: Reviewers write free text that Foreman must parse, and "reproducible findings" is a recent theme. ReportFindings gives typed findings the host UI renders, and a hook can read them for the done-gate.
  Done when: the reviewer agent ends with a ReportFindings call and the done-gate counts its blockers without text parsing.

- **Back resolve-the-blast-radius checks with LSP** — FEATURE — value 4 — effort M — risk low — category: LSP
  Why: Plans guess footprints from co-change history, and the deletion checks (Chesterton fence, "prove unused") use grep. LSP references and definitions give exact callers. Assumption: a language server exists for the project; fall back to grep.
  Done when: before a deletion step, `fm` lists LSP references, and a rename-by-grep miss in a fixture is caught.

- **Fix step-tracking drift with a PostToolUse step-gate** — FIX — value 4 — effort S — risk low — category: hooks
  Why: T-0759: "it will start working on different steps without updating the step". A PreToolUse check compares the edited file to the current step's footprint and injects "advance or declare step N" instead of blocking.
  Done when: an edit outside the current step's footprint produces the nudge, and the ledger records a step switch within one call.

- **Wild: Publish a "return screen" Artifact the user opens after being away** — FEATURE — value 4 — effort M — risk low — category: Artifact — wild
  Why: assumption: a single page of what shipped, what blocked, and one-tap defaults for the pending asks, rewritten on each wake. Covers "return screen" without a terminal.
  Done when: after an unattended run, the page lists finished tasks with proof links and each ask has an Approve button that resolves it.

- **Wild: Make the fleet a SendMessage mesh across machines** — FEATURE — value 4 — effort L — risk high — category: SendMessage — wild
  Why: SendMessage and ListAgents reach cloud and Remote Control sessions on other machines, which gives the federation ideas a native transport with no daemon of our own. Assumption: cross-machine messages are delivered reliably enough for claims.
  Done when: a task queued on machine A is claimed by an idle session on machine B and reported back to A.

- **Wild: Let a /code-review ultra run be the closing gate for L tasks, with its findings imported** — FEATURE — value 3 — effort M — risk med — category: code-review — wild
  Why: Foreman builds its own reviewer lenses; the native multi-agent cloud review is a free independent panel. It is user-triggered and billed, so Foreman can only prompt for it and ingest a result the user pastes or exports. Assumption: findings can be pulled into the ledger by a command.
  Done when: for an L task, the close-out offers one line to run it, and after it runs, its findings appear as criteria in the task.

- **Wild: Use EnterWorktree for the main thread's risky experiments** — FEATURE — value 3 — effort S — risk low — category: worktree — wild
  Why: Spike lanes today spawn agents; moving the main thread into a throwaway worktree keeps its context and discards the tree on ExitWorktree. Assumption: the move preserves the Foreman state paths.
  Done when: a spike task runs in a worktree, exits with discard, and leaves the main tree byte-identical.
