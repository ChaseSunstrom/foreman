# Brainstorm — lens: bold bets

- **Publish the cockpit as a live Artifact** — FEATURE — value 5 — effort M — risk med — category: native surface
  Why: Artifact (private claude.ai pages with ArtifactData and ArtifactComments) has 0 references. Foreman's web UI, foreman-ui pane and desktop app are all local-only. The user asked to "see, steer and rewind" (Frontier 11). A private page showing queue, plan tree, evidence and proofs is reachable from a phone.
  Done when: `fm artifact publish` creates or updates one page showing the queue, the active task's steps and the last 10 close-outs. A second call changes only the changed sections, and a test with a stubbed publisher checks the redacted payload.

- **Turn Artifact comments and buttons into queue input** — FEATURE — value 5 — effort M — risk med — category: steering
  Why: The user's captured tasks (T-0755..T-0760) are mostly mid-run steers typed into the terminal. ArtifactComments sends comments to Claude, and ArtifactData lets the CLI read page-side writes. A "defer", "drop", "do next" or "ask" button on each queue card can become `fm task` calls through the existing guard. Assumption: ArtifactData is readable from a hook or CLI.
  Done when: a fixture ArtifactData record `{task: T-0755, action: "next"}` is consumed once by `fm inbox poll`, reorders the queue and is marked applied in the ledger. A replayed record changes nothing.

- **Replace tmux send-keys wake-ups with SendMessage/ListAgents** — FIX — value 4 — effort M — risk med — category: orchestration
  Why: fm bus wakes idle sessions by typing into their tmux pane. This is fragile and only works inside tmux. It is also the likely cause of T-0758 ("doesn't sit idle like it is"). SendMessage targets local, cloud and Remote Control sessions without a terminal. Assumption: SendMessage can wake an idle session.
  Done when: with tmux absent, `fm bus wake <session>` delivers through SendMessage, and the existing bus tests pass. send-keys stays as a fallback, labelled in `fm doctor`.

- **Run the drive loop on Monitor and ScheduleWakeup instead of polling** — PERFORMANCE — value 4 — effort M — risk low — category: idle/autonomy
  Why: Foreman's gates, lane runs and `fm night` wait on background commands. The user complains it "sits idle" (T-0758). Monitor streams a background command's output as notifications, so a finished gate or lane wakes the session. ScheduleWakeup covers timed waits such as flake reruns and usage-limit resets, with no custom daemon.
  Done when: a test drive with a 30-second background gate resumes within 2 seconds of the gate's exit, with no polling calls in the transcript. A usage-limit wait is scheduled with one wakeup call.

- **Pick the model and effort per call from a measured table** — PERFORMANCE — value 5 — effort M — risk low — category: cost/speed
  Why: The Agent tool accepts `model` and `effort` per call. Foreman fixes scout=haiku, S-tier lanes=sonnet and builders inherit. T-0755 asks "can foreman spawn agents of lower models? like 5.5 haiku/sonnet?" Foreman already has bench, per-model lesions and a budget-fit queue. `fm route` returns `{model, effort}` per role and tier from bench pass rates and cost, and the brief template tells the orchestrator to pass them.
  Done when: `fm route builder S` prints a model and effort with the bench numbers behind them. A bench run with routed models passes at least as often as the inherit baseline on the S-tier cases, at lower token cost.

- **Emit review findings through ReportFindings** — FEATURE — value 4 — effort S — risk low — category: native review
  Why: ReportFindings renders typed findings in the host UI. Foreman's reviewer subagent returns prose, and `fm audit` (T-0034) is deferred. Reviewer output mapped to typed findings (severity, file, line, reproducer) gets native rendering and feeds the reviewer-precision tracking Foreman already has. Assumption: the subagent can call the tool.
  Done when: a reviewer run on a seeded-bug fixture yields at least one ReportFindings call whose file and line match the seeded bug. `fm review` stores the same findings in the ledger.

- **Use LSP for blast radius and safe renames** — FEATURE — value 4 — effort M — risk low — category: code intelligence
  Why: LSP (definitions and references) has 0 references. The map's tests→src links are filename heuristics. Real references would make the edit-time test sentinel (T-0214) precise and improve the pre-edit blast sketch. Assumption: an LSP server is configured for the project's language.
  Done when: on a fixture project, `fm impact app.py:handler` lists the callers found through LSP references, and the sentinel runs only the tests covering them. It falls back to the filename heuristic when no LSP is available.

- **Schedule overnight work as cloud routines with RemoteTrigger** — FEATURE — value 4 — effort L — risk med — category: unattended
  Why: `fm night` needs the user's machine awake. RemoteTrigger and `/schedule` run cloud routines on a cron. Overnight audits, upstream-drift watches, Claude Code release adaptation and the dependency-release scan don't need local state, and they can post findings back as queue captures. Assumption: routines can reach the repo.
  Done when: `fm routine add claude-release-watch` registers one cloud routine. Its next run's result arrives as a captured task with a source tag, with no local process running.

- **Add PushNotification to blocked, done and ask moments** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: `fm notify` runs a user-configured shell command, so the user must set it up. PushNotification reaches the phone natively. Wire it to ask, blocked and night-finished events behind a quiet-hours setting and a once-per-event dedupe.
  Done when: a blocked event produces one push, a repeat within the dedupe window produces none, and quiet hours suppress the push while keeping the ledger entry.

- **Wild: Make the main thread an "orchestrator of orchestrators" via remote isolation** — FEATURE — value 5 — effort L — risk high — category: fleet (wild)
  Why: The user steered toward "orchestration of orchestrators". The Agent tool supports isolation "remote" in the cloud and the worktree option locally. A lane can then be a cloud session that runs its own Foreman scope on a queue slice, reporting back by SendMessage. Assumption: remote sessions can load the Foreman plugin.
  Done when: `fm lane --remote T-0123` starts a cloud lane, which returns a diff and an evidence receipt. The receipt passes the same done-gate locally before merge.

- **Wild: Keep a living Claude Docs "project bible" the user edits in prose** — FEATURE — value 3 — effort M — risk med — category: shared doc (wild)
  Why: Claude Docs are shared editable documents. A doc holding vetoes, standing preferences, decisions and the current milestone lets the user change Foreman's rules by editing text. They have steered by chat repeatedly and want it to "just know". Foreman diffs the doc on session start and proposes rule changes with the quote that justifies each.
  Done when: editing one veto line in the doc produces, at the next session start, a proposed rule diff naming that line. Accepting it updates the vetoes file, and an unchanged doc produces no output.

- **Wild: Self-pace the whole queue with `/loop` and a "heartbeat" artifact** — FEATURE — value 3 — effort M — risk med — category: autonomy (wild)
  Why: ScheduleWakeup powers self-paced loops. Foreman could run an unattended pace loop that wakes at the user's chosen cadence and re-reads usage pace. It continues the queue or sleeps until the limit resets, and it updates an Artifact heartbeat saying "working on T-0xxx, step 3/5, next check 14:20". That also answers the idle complaint visibly.
  Done when: a simulated 3-hour run with one usage-limit pause shows wakeups at the scheduled times. The heartbeat page's last-updated time never lags the ledger by more than one wake interval.

- **Wild: Let Foreman file its own CC feature-adoption tasks from release notes** — FEATURE — value 4 — effort M — risk low — category: self-evolution (wild)
  Why: The unused-tool list in this pack was found by hand. Foreman already has a "turn Claude Code releases into adaptation tasks" idea in the pile but no capability inventory. A nightly diff of the tool list and hook events against a checked-in inventory file (used, unused, rejected-with-reason) captures a task for each new, unrecorded capability.
  Done when: adding a fake new tool to a fixture tool list creates exactly one captured task. A tool marked "rejected: reason" creates none.
