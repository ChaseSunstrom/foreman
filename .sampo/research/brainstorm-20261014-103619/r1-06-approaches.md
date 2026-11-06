# Brainstorm — lens: approaches

- **Run the done-tail on built-in review levels** — FEATURE — value 4 — effort M — risk low — category: reuse
  Why: Foreman maintains its own reviewer subagents, while `/code-review` (low…max), `/simplify` and `/security-review` ship with Claude Code and have 0 references. Approach: reuse over rebuild. Map task tier to level (S→low, L→max) and record the result as evidence. Bench them against Foreman's lenses per project and retire whichever loses. Trade-off: less control over prompts, but fewer home-grown lenses to maintain.
  Done when: `fm task finish` on an L task records a built-in review result as evidence, and `fm bench` reports built-in vs home-grown catch rate.

- **Drive idle sessions with ScheduleWakeup instead of Stop-hook blocking** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: T-0758 ("make sure it doesn't sit idle") and the tmux send-keys bus are workarounds for the same gap. The native self-paced loop wakes the session when the queue has work, with no pane typing. Trade-off: it depends on harness semantics, so keep the Stop-hook path as a fallback.
  Done when: a session with queued tasks and no user input resumes by a scheduled wakeup, with the bus disabled and no send-keys used.

- **Publish a live Artifact cockpit with approvals and comments** — FEATURE — value 5 — effort L — risk med — category: surface
  Why: Artifact (private HTML on claude.ai, a shared db, comments sent to Claude) is unused. Frontier 11 asked for a cockpit the user can steer from. This one is reachable from a phone with no local server. Page content: queue, plan tree, pending asks and per-criterion evidence. The comment box becomes a captured task. Trade-off: it publishes data off-box, so it needs an explicit setting and redaction (assumption: a redaction pass exists, as for `fm recall --ask`).
  Done when: `fm artifact publish` yields a page showing the live queue, and a comment left on it appears as a captured T-id.

- **Stream gates through Monitor and fail fast** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: the full suite (149 test files) runs as one blocking call. Monitor streams a background command's output as notifications. Start gates in the background, react on the first `✗ exit N` line, and keep reading or editing meanwhile. Trade-off: a notification can interleave with a step and needs a step-aware filter.
  Done when: `fm task finish --run` starts verify in the background and the first failing line reaches the session before the suite ends.

- **Replace send-keys with SendMessage/ListAgents** — FIX — value 4 — effort M — risk med — category: bus
  Why: typing into a tmux pane breaks if the user is mid-keystroke or the pane is not tmux. SendMessage reaches local, cloud and remote-control sessions, which also gives the multi-machine path. Trade-off: it needs a version probe and fallback to the old bus.
  Done when: `fm bus send` delivers to an idle session with no tmux pane and to a session on a second machine.

- **Ship named Workflows for audit and release** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: T-0034 (`fm audit run`) wants lens reviewers writing a findings file, and Workflow gives deterministic multi-agent scripts. The constraint is that it needs the user's opt-in. Approach: ship saved named workflows, and intake detects the user's own words ("run the audit") as the opt-in, never launching one silently.
  Done when: saying "run the audit" triggers the saved `foreman-audit` workflow and writes the findings file; with no such phrase, nothing launches.

- **Offload nightly work to cloud routines** — FEATURE — value 3 — effort L — risk high — category: scheduling
  Why: `fm night` needs the laptop on. RemoteTrigger/`/schedule` and Agent isolation "remote" run on a cron elsewhere. Candidates are the release canary, the audit and the dependency scan. Trade-off: the repo and data leave the machine, so it is opt-in per project and read-only.
  Done when: a scheduled routine runs the audit on a project and its findings land in the central ledger without the local machine running.

- **Use EnterWorktree for risky steps and revert with ExitWorktree** — FEATURE — value 3 — effort M — risk low — category: safety
  Why: lanes only get worktrees through Agent isolation. The main thread can now move into one. A one-way-door step gets a worktree, and an ExitWorktree discard becomes a clean per-step revert. The existing task revert is commit-level only. Trade-off: path-dependent state such as the guard's cwd rules must follow.
  Done when: a flagged step runs in a worktree, and a failed verify discards it leaving the main tree byte-identical.

- **Collect reviewer output as ReportFindings** — FEATURE — value 3 — effort S — risk low — category: reviews
  Why: reviewers' prose findings are parsed by Foreman. Typed findings give the host UI rendering and a stable schema, and map directly onto the audit findings file. Trade-off: there is no equivalent on other harnesses, so keep an adapter.
  Done when: a reviewer run produces typed findings that `fm findings` lists with severity, file and line.

- **Send only needs-you events through PushNotification** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: `fm notify` runs a user-configured shell command, which means setup the user never wants to do. Native push covers asks, blocks and done-for-the-night with zero config. Trade-off: it can be noisy, so cap it at one per ask.
  Done when: a blocking ask reaches the phone with no `fm notify` command configured.

- **Edit the plan in a shared Claude Doc** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: plan review is terminal text, and the user cannot edit one node. A shared doc lets the user strike or rewrite a step, and Foreman diffs their edit back into the plan as a steer. Trade-off: it is outward-facing, so confirm before publishing.
  Done when: editing a step in the doc changes the plan step on the next `fm plan show`.

- **Wild: Make every ledger line an Artifact-comment target** — FEATURE — value 3 — effort M — risk med — category: feedback
  Why: assumption: comments are routable back to the session. The user taps "wrong turn" on a decision, and it becomes a veto or lesson candidate with the line attached.
  Done when: a comment on a decision line creates a linked steer task.

- **Wild: Run a skill-doctor and permission-prompt sweep nightly** — CLEAN — value 2 — effort S — risk low — category: hygiene
  Why: Foreman ships 73 skills and fewer-permission-prompts and `/skill-doctor` exist, yet `fm doctor` never calls them. Wild extension: auto-apply the safe fixes in a lane.
  Done when: `fm doctor` reports skill-doctor findings for `plugin/skills/`.

- **Wild: Hold a cloud sibling session that answers while the laptop sleeps** — FEATURE — value 3 — effort L — risk high — category: continuity
  Why: assumption: a remote session can see the queue. It triages new phone messages into briefs and replies by push while the local drive is down.
  Done when: a message sent with the laptop off becomes a captured task by morning.
