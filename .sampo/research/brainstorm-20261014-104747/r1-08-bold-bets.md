# Brainstorm — lens: bold bets

- **Publish a live Foreman Cockpit as an Artifact** — FEATURE — value 5 — effort M — risk med — category: native UI
  Why: Artifact is unused (0 refs) and the user asked for a Cockpit UI (Frontier 11); the foreman-ui mod only works inside one terminal. Assumption: Artifact pages can be updated from the CLI side via ArtifactData.
  Done when: `fm cockpit publish` creates a private page showing the plan tree, current step, fleet and queue, and a task status change appears on the page within 10s of `fm task finish`.

- **Take steering comments from the Artifact into the queue** — FEATURE — value 4 — effort M — risk med — category: native UI
  Why: ArtifactComments are sent to Claude and the user wants to steer without typing commands. Assumption: comments arrive as a readable event the session can act on.
  Done when: a comment "move T-0758 first" on the cockpit page reorders the queue and the page shows the new order.

- **Replace tmux send-keys wakeups with ScheduleWakeup and Monitor** — FIX — value 5 — effort M — risk med — category: idle handling
  Why: the user said "make sure it doesnt sit idle" (T-0758); fm bus wakes sessions by typing into tmux panes, which breaks without tmux. Assumption: Monitor can stream `fm bus` or queue events as notifications.
  Done when: an idle session with a queued task resumes without tmux, and `fm doctor` reports wake via native primitives.

- **Route every lane to the cheapest sufficient model and effort** — FEATURE — value 5 — effort M — risk low — category: cost routing
  Why: T-0755 asks for lower-model agents; only scout and S-tier lanes pick a model today, and per-call `model` and `effort` are available. Assumption: Foreman's tier and task type are enough to pick them.
  Done when: `fm plan` shows model and effort per step, and a bench over 20 replayed tasks shows lower token cost with no drop in pass rate.

- **Block step drift with a PreToolUse step-sync check** — FIX — value 4 — effort S — risk low — category: discipline
  Why: T-0759 says it starts working on other steps without updating the step in the plan. Assumption: the edited files can be matched to a step's declared scope.
  Done when: an edit outside the active step's scope gets a one-line nudge naming the step, and a test covers it.

- **Send PushNotification when a task needs the user or the queue drains** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: PushNotification has 0 refs, and fm notify only runs a user shell command; autonomous night runs have no way to reach a phone. Assumption: PushNotification is callable from the main session.
  Done when: a blocked task or a finished queue sends one push with the task ID and the question, with a rate limit of one per task.

- **Feed ReportFindings from the reviewer subagent** — FEATURE — value 3 — effort S — risk low — category: review
  Why: the reviewer writes its own formats while the host UI renders typed findings, and T-0034 (deferred audit) wants a structured findings file. Assumption: ReportFindings can be called from a subagent.
  Done when: reviewer output shows as host-rendered findings and is stored as the T-0034 findings file.

- **Run a nightly Foreman routine in the cloud via RemoteTrigger** — FEATURE — value 4 — effort L — risk high — category: scheduling
  Why: fm night exists but needs a live machine; routines run on a cron in the cloud. Assumption: a cloud run can open a PR without local secrets.
  Done when: a scheduled routine pushes a branch with one pre-planned L task's results and the morning `fm status` lists it.

- **Use LSP for blast-radius and the edit-time sentinel** — FEATURE — value 4 — effort M — risk low — category: code intelligence
  Why: T-0214 (edit-time test sentinel) links tests to files by naming only; LSP references give real callers. Assumption: LSP is available in the sessions that need it.
  Done when: after editing a function, `fm` lists tests that reference it through LSP references, including one the name-based map misses.

- **Wild: Make Foreman a fleet across machines with SendMessage and ListAgents** — FEATURE — value 4 — effort L — risk high — category: multi-machine — wild
  Why: SendMessage reaches Remote Control sessions on other machines; Foreman's queue is single-host. Assumption: sessions can address each other by ID.
  Done when: a task queued on the laptop runs on the desktop, and its evidence appears in the laptop's ledger.

- **Wild: Spawn a "red team" subagent that tries to forge a pass before close-out** — FEATURE — value 4 — effort M — risk med — category: verification — wild
  Why: forge-a-pass briefs and negative twins exist as a prompt idea, but nothing runs as an isolated adversary in a worktree with a different model. Assumption: a different model catches different gaps.
  Done when: on a seeded task with a weak test, the adversary finds a passing-but-wrong change and close-out is blocked.

- **Wild: Turn the day's ledger into a spoken or written morning briefing Artifact** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: the user returns to overnight work and must read the queue; an Artifact with a checklist, diffs and "approve all" shows it at a glance. Assumption: ArtifactData can carry approval flags back.
  Done when: opening the page shows what shipped, what blocked and one-click approvals that `fm` reads on the next session.

- **Wild: Let Foreman rewrite its own hook latency budget by running /loop self-paced bench cycles** — PERFORMANCE — value 3 — effort M — risk med — category: self-improvement — wild
  Why: bench_hooks.py gates latency by hand, and the flywheel (Frontier 12) wants overnight self-tuning. Assumption: a ScheduleWakeup loop can run benches without interrupting work.
  Done when: a loop run records hook p95 per event over 5 cycles and files a task for any event that regressed.

- **Trim the bypass-mode surface by adopting fewer-permission-prompts output** — SECURITY — value 3 — effort S — risk med — category: permissions
  Why: Foreman relies on bypass mode plus its own guard; fewer-permission-prompts proposes narrow allowlists from real history. Assumption: its output can be read by Foreman.
  Done when: `fm doctor` offers a minimal allowlist built from the last 30 days and states which guard checks it would leave unchanged.
