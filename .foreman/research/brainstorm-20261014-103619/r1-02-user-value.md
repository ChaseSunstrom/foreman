# Brainstorm — lens: user value

- **Publish the queue as a live Artifact the user can comment on** — FEATURE — value 5 — effort M — risk med — category: Artifact
  Why: Artifact is unavailable to Foreman today (0 references). It gives a private page with a shared db, comments sent back to Claude, and "ask Claude". The user keeps relaying requests by chat, and the capture backlog (T-0755 to T-0760) is mostly half-sentences typed on the move. Assumption: ArtifactData can be written from the CLI side without a human click.
  Done when: running `fm artifact sync` creates a page listing the active task, step, queue and blocked asks, and a comment typed on a queue card appears as a captured T-id within one drive cycle.

- **Replace tmux send-keys wakes with SendMessage and ListAgents** — FIX — value 4 — effort M — risk med — category: Reliability
  Why: `fm bus` types into tmux panes, which breaks when the pane is mid-edit, scrolled, or running outside tmux. The user's complaint "make sure it doesn't sit idle like it is" is a wake that never landed. Assumption: SendMessage reaches idle local sessions.
  Done when: an idle session in a non-tmux terminal wakes on a queued task via `fm bus`, with send-keys kept only as a labelled fallback.

- **Keep the session busy with Monitor and ScheduleWakeup instead of ending turns** — FEATURE — value 5 — effort M — risk med — category: Idle
  Why: the user said "can you make sure it doesnt sit idle". A Stop with a non-empty queue should arm a Monitor on running gates and lanes, or a ScheduleWakeup, rather than stop and wait for a nudge. Assumption: Monitor notifications re-enter the turn loop.
  Done when: with two queued tasks and a 3-minute background gate, the session starts the next task on gate completion with no user input, and the ledger shows the wake source.

- **Derive the current step from tool activity** — FIX — value 4 — effort M — risk low — category: Step tracking
  Why: T-0759: it "will start working on different steps without updating the step". PostToolUse already sees the edited paths. Match them against each step's declared footprint and advance the step, or flag a mismatch, automatically.
  Done when: editing a file that belongs to step 3 while step 2 is marked current moves the current step to 3, or warns once, and the statusline shows the corrected step.

- **Own the Agent call: a model and effort table enforced in PreToolUse** — FEATURE — value 5 — effort S — risk low — category: Delegation
  Why: T-0755 asks "can foreman spawn agents of lower models? haiku/sonnet". Only S-tier lanes pass `model`. The Agent tool accepts per-call `model` and `effort`. Rewrite or reject calls that omit them, using a small role→(model, effort) table, and log the choice. Assumption: PreToolUse can edit Agent input.
  Done when: a recon spawn with no model runs as haiku at low effort, and the ledger records model and effort per spawn.

- **Adopt ReportFindings as the reviewers' output channel** — FEATURE — value 4 — effort M — risk low — category: Review
  Why: reviewers currently write prose that Foreman parses, and T-0034 (fm audit) is deferred for lack of a structured file. Typed findings render in the host UI and can feed the queue directly.
  Done when: a reviewer run produces ReportFindings entries, `fm task finish` reads them as blockers or notes, and a high finding without a repro is rejected.

- **Move risky FIX and L tasks into EnterWorktree and merge back on done** — FEATURE — value 4 — effort M — risk med — category: Isolation
  Why: lanes use worktrees, but the main thread edits the user's live tree. The user also edits by hand and `fm` has no separate-tree story for them. Moving the main thread into a worktree lets the user keep working. Assumption: ExitWorktree can merge or keep the branch.
  Done when: an L task runs in a worktree, the user's tree stays unchanged during the run, and done merges it only after the gates pass.

- **Push to the phone only when a decision is waiting, with a one-line default** — FEATURE — value 4 — effort S — risk low — category: Notifications
  Why: `fm notify` runs a shell command the user must set up, and PushNotification is unused. A push for an ask, a block, or a night-run finish should carry the default and its expiry. Assumption: push is permitted from a hook or the main thread.
  Done when: a blocked ask sends one push including the default and deadline, and quiet-hours suppress everything else.

- **Save the review fan-out as a named Workflow after a one-time user grant** — FEATURE — value 3 — effort M — risk med — category: Workflow
  Why: Workflow gives deterministic multi-agent scripts but can't be launched without the user's words, and Foreman's lens fan-out is currently model-improvised. Foreman can ask once, in one sentence, to save `foreman-review`, then call it by name. Assumption: saved workflows persist across sessions.
  Done when: after the user's single approval, `fm review` runs the saved workflow for later tasks without asking, and the run lists every lens.

- **Wild: Preview a speculative L task as an Artifact from a cloud lane overnight** — FEATURE — value 4 — effort L — risk high — category: Cloud
  Why: the Agent tool supports isolation "remote". A cloud lane could build the top queued L task while the machine sleeps and publish a before/after Artifact with an approve comment. Assumption: the remote lane can reach the repo and the gates. wild
  Done when: from a phone, one comment on the Artifact promotes the cloud branch into a local queue item with its evidence attached.

- **Wild: Make a Claude Docs "priorities" page where editing a line reorders the queue** — FEATURE — value 3 — effort M — risk med — category: Steering
  Why: the user steers by chat and re-sequencing ("reordering of operations… put them into one task", T-0757) is awkward in chat. A shared doc whose lines map to T-ids would make drag-and-edit the control surface. Assumption: Claude Docs is readable from the CLI. wild
  Done when: moving a line in the doc changes `fm queue` order within a minute, and the ledger notes who reordered.

- **Wild: Ask Claude from a queue card on the Artifact to explain "why is this waiting?"** — FEATURE — value 3 — effort S — risk low — category: Explainability
  Why: the user keeps finding Foreman idle or off-step and has to ask in chat. A card-level "ask Claude" answered from the ledger and live state turns each queue stall into a one-tap explanation. Assumption: page-level asks route to the active session. wild
  Done when: tapping "why waiting?" on a blocked card returns the blocker, the owner, and the next unblocking action in under 30 seconds.

- **Map task tier to a /code-review level and run it before done** — FEATURE — value 3 — effort S — risk low — category: Review
  Why: built-in /code-review spans low to max, while Foreman's reviewer is a custom sonnet agent with fixed depth. S tasks use low, M uses medium, L uses high, and Foreman tells the user once when an `ultra` review is worth their own trigger, since it can't launch one. Assumption: skills can be invoked from a lane.
  Done when: the close-out of an M task records the review level run and its findings count, and an L release prints the one-line `/code-review ultra` suggestion.
