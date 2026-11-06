# Brainstorm — lens: simplicity

- **Retire the tmux send-keys bus for native wakes** — CLEAN — value 4 — effort M — risk med — category: orchestration
  Why: fm bus types into tmux panes to wake idle sessions, which depends on tmux and on pane names. T-0758 ("doesn't sit idle") shows idling still happens. ScheduleWakeup, Monitor and SendMessage/ListAgents do this natively. Assumption: they work in bypass-mode sessions.
  Done when: with tmux not installed, an idle session with queued tasks resumes via ScheduleWakeup, and `fm doctor` passes.

- **Add a built-in overlap audit to fm doctor** — FEATURE — value 4 — effort M — risk low — category: maintenance
  Why: delta reads were built, then dropped once measurement showed Claude Code already returns a stub. `fm doctor` can list each Foreman feature next to the CC built-in that may duplicate it, such as /code-review, ReportFindings, LSP, PushNotification, worktrees and Monitor. Each entry gets a keep or retire verdict backed by a measurement.
  Done when: `fm doctor --overlap` prints a table of at least 8 rows, each with a feature, a built-in and a verdict. A row with no measurement is marked "unmeasured".

- **Collapse model routing into one tier table** — CLEAN — value 4 — effort S — risk low — category: routing
  Why: T-0755 asks for lower-model agents. Today scout=haiku, four agents are sonnet, the builder inherits, and S lanes hardcode "sonnet". The Agent tool takes per-call `model` and `effort`. One table (S→haiku or sonnet, M→sonnet, L→inherit, with effort) read by every spawn site replaces the scattered special cases.
  Done when: grepping `plugin/` for hardcoded model strings finds only the table file, and a test asserts that each tier spawns with the table's model.

- **Use ReportFindings instead of the custom findings format** — CLEAN — value 3 — effort M — risk med — category: review
  Why: the reviewer and T-0034 (`fm audit`) each invent a structured findings file. ReportFindings is typed and the host UI renders it. Assumption: a subagent can call it.
  Done when: reviewer output renders as host findings, and the custom findings parser and its tests are deleted.

- **Drive step state from PostToolUse, not model bookkeeping** — FIX — value 5 — effort M — risk med — category: reliability
  Why: T-0759 reports work starting on other steps without the step being updated. Hooks can infer the active step from edited files and test runs and advance it themselves. That removes an instruction the model keeps forgetting.
  Done when: in a replayed transcript where the model never calls the step update, the recorded step matches the work done, and the step-update instruction is removed from the prompt.

- **Replace the worktree lane plumbing with EnterWorktree and isolation** — CLEAN — value 3 — effort M — risk med — category: lanes
  Why: Foreman already uses Agent isolation "worktree", and the main thread can now EnterWorktree/ExitWorktree. Any lane code that creates, cleans up or tracks worktrees by hand is redundant. Assumption: such code exists.
  Done when: no `git worktree add` remains in `plugin/lib`, and the lane e2e passes.

- **Close out the blocked and deferred backlog** — CLEAN — value 3 — effort S — risk low — category: backlog
  Why: 15 open items are deferred or blocked (T-0325, T-0335 to T-0337, T-0352, T-0418, T-0431, among others). Many have waited for external conditions or are superseded. A sweep that proposes drop, merge or revive for each one shrinks the surface.
  Done when: every deferred or blocked item older than the cutoff has a recorded drop, merge or revive decision, and the open count falls to at most half.

- **Replace the notify shell command with PushNotification** — CLEAN — value 3 — effort S — risk low — category: notifications
  Why: fm notify runs a user-written shell command, which means configuration and a guard surface. PushNotification reaches phone and desktop with no setup. The shell command can remain as a fallback.
  Done when: a finished overnight run produces a push with no notify command configured.

- **Delete hooks that never fire usefully (wild)** — PERFORMANCE — value 4 — effort M — risk med — category: hooks
  Why: 14 hook events are latency-gated by bench_hooks.py, and every hook is a process spawn. Mine 30 days of logs for hooks that never block, rewrite or add context. Retire them or merge them into one dispatcher. wild
  Done when: a report ranks each hook by blocks and context actually used, at least one low-value hook is removed, and bench_hooks p95 improves.

- **Run fm night as a cloud routine (wild)** — FEATURE — value 4 — effort L — risk med — category: scheduling
  Why: fm night depends on the machine staying on and a session staying alive. /schedule with RemoteTrigger, or CronCreate for local runs, hands the overnight work to a native scheduler. wild
  Done when: a scheduled routine runs the queue unattended and writes the results back to the central record.

- **Show the cockpit as an Artifact, not Desktop (wild)** — FEATURE — value 4 — effort L — risk med — category: UI
  Why: Desktop has three blocked items (T-0325 tray, T-0352 publish, T-0418 mod update), and Frontier 11 asks for a live cockpit pane. A private Artifact page can show the plan tree and queue, take comments sent to Claude (ArtifactComments), and work from a phone. This could replace the Desktop and mod maintenance burden. Assumption: Artifact can read state through ArtifactData. wild
  Done when: a page shows the live plan tree, and a comment on a task shows up as a captured request.

- **Resolve fm ask approvals through Artifact comments or SendMessage (wild)** — FEATURE — value 3 — effort M — risk high — category: approvals
  Why: T-0335 (fm ask grants on other CLIs) is blocked. Routing approvals through a native channel means one path for all hosts, though it widens the guard surface. Pins are tied to a content hash (T-0036), and that must stay. wild
  Done when: a pin approval is accepted only through the single channel and only at the matching hash, and a replayed stale approval is refused.

- **Replace the home-grown test linking with LSP references** — CLEAN — value 3 — effort M — risk med — category: code intelligence
  Why: T-0214 (edit-time test sentinel) relies on `fm map` test→src links, which are filename heuristics (test_agents.py→fmagents.py). LSP references give real call links and make the sentinel precise.
  Done when: editing a function runs the tests that reference it by LSP, and the heuristic linker is used only as a fallback.
