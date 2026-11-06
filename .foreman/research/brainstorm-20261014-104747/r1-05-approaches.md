# Brainstorm — lens: approaches

- **Route every Agent call by tier, model and effort** — FEATURE — value 5 — effort M — risk low — category: orchestration
  Why: T-0755 asks for lower-model agents. Only S-tier lanes pass "sonnet" today, and the per-call `model` and `effort` parameters are unused.
  Done when: `fm plan` prints a model and effort for each step, and a test shows an S step dispatched as haiku/low and an L step as opus/high.

- **Replace tmux send-keys with Monitor and ScheduleWakeup so sessions never idle** — FIX — value 5 — effort M — risk med — category: autonomy
  Why: T-0758 ("make sure it doesn't sit idle"). The bus types into a tmux pane, which is brittle. Monitor can stream queue and lane events as notifications, and ScheduleWakeup can self-pace the drive.
  Done when: with a queued task and an idle session, the session resumes within 30s with no send-keys call. A test covers it.

- **Bind steps to edits automatically** — FIX — value 4 — effort S — risk low — category: plan integrity
  Why: T-0759 reports work starting on other steps without the step being updated. A PreToolUse hook could map the edited file to the step that declared it, mark that step in progress, and warn on a mismatch.
  Done when: an edit to a file owned by step 3 while step 2 is active flips the state or blocks with a message. The hook stays under the `bench_hooks.py` budget.

- **Use ReportFindings as the reviewer's output channel** — FEATURE — value 4 — effort M — risk low — category: review
  Why: reviewer findings are likely prose that Foreman reparses. Typed findings render in the host UI and reach `fm` already structured, which supports T-0034 and reproducible findings.
  Done when: a review run yields typed findings that `fm task finish` ingests without regex, and a malformed finding fails a test.

- **Publish the Cockpit as an Artifact with a shared database** — FEATURE — value 4 — effort L — risk med — category: UI
  Why: Frontier 11 wants a pane to see and steer from. An Artifact is a private claude.ai page. ArtifactData could carry plan, fleet and queue state, and ArtifactComments could carry steering back. This reaches the user without foreman-ui being installed.
  Done when: `fm cockpit publish` creates the page, a comment on a step arrives as a captured request, and a test fakes the data path.
  Assumption: the CLI side can write ArtifactData non-interactively.

- **Send PushNotification only for needs-you events** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: `fm notify` runs a user shell command, so setup is manual and the user never wants to be handed commands. Push is native and works away from the desk. It should fire only when blocked, on a failed gate, or at release-ready.
  Done when: a blocked task fires exactly one push, repeat blocks are deduplicated, and routine progress fires none.

- **Run the night queue and the eval flywheel as cloud routines** — FEATURE — value 4 — effort L — risk high — category: scheduling
  Why: Frontier 12 wants overnight improvement, and `fm night` currently needs the machine awake. RemoteTrigger with /schedule, or Agent isolation "remote", would run it without the laptop. The risk is that secrets and local state must stay out of the cloud.
  Done when: a scheduled routine runs the eval inbox and lands a branch. A redaction check proves no local-only files are sent.

- **Derive linked tests from LSP references** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: T-0214, the edit-time test sentinel, depends on `fm map` test links, which are filename heuristics. LSP references give true call-graph links, and the same data could scope reviewer diffs.
  Done when: editing a function runs the tests that reference it by symbol, and a test shows a test with a mismatched filename still gets picked.

- **Make the review gate a native /code-review level ladder (doing less)** — CLEAN — value 3 — effort S — risk med — category: simplification
  Why: Foreman keeps its own reviewer, while built-in /code-review has low…max levels and ultra. The trade-off is that you lose custom evidence rules. A hybrid keeps Foreman's checks and uses the native level for L tasks.
  Done when: `fm doctor` reports review level per tier, and at least one tier uses the native review with its findings recorded.

- **Wild: Run competing attempts in worktrees and let verification pick the winner** — FEATURE — value 4 — effort L — risk med — category: orchestration — wild
  Why: assumption: background worktree Agents are cheap. For hard FIX tasks, run 2–3 approaches in parallel with different models, run the same criteria on each, and merge only the passing one that has the smallest diff.
  Done when: `fm try --approaches 3` produces three worktrees, scores them with the task's verify, and merges exactly one.

- **Wild: Add a phone approval surface for guard asks** — FEATURE — value 3 — effort L — risk high — category: devices — wild
  Why: assumption: PermissionRequest can wait on an external answer. A guard block would show as an Artifact button or push action, and the answer would flow back through ArtifactData. The user approves from their phone with no terminal. Approvals would need to be pinned to the exact command hash.
  Done when: a blocked command is approved from the page, runs once, and the same command is refused again afterwards.

- **Wild: Escalate through model tiers on verify failure** — PERFORMANCE — value 4 — effort M — risk low — category: cost — wild
  Why: assumption: haiku passes a measurable share of S steps. Start every step on the cheapest model, and on a failed check retry one tier up with the failure attached. Per-model pass rates feed back into the router, so the table learns.
  Done when: a seeded failing step escalates from haiku to sonnet exactly once, and the ledger shows tokens saved against an all-sonnet baseline.

- **Replace the tmux bus with SendMessage and ListAgents** — CLEAN — value 3 — effort M — risk med — category: orchestration
  Why: the bus types into panes, which breaks when a pane is busy, absent or on another machine. SendMessage reaches local, cloud and Remote Control sessions. Keep tmux as the fallback.
  Done when: a message to a session on another machine arrives through SendMessage, and the tmux path is used only when SendMessage fails.
