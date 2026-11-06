# Brainstorm — lens: capability map

- **Publish a live Artifact cockpit** — FEATURE — value 5 — effort M — risk med — category: Artifact
  Why: Artifact (private HTML pages with shared db, comments to Claude, "ask Claude") has 0 references; the user's Frontier 11 "Cockpit UI" asks for one live pane to see, steer and rewind the plan. An Artifact makes it reachable from a phone and shareable without the foreman-ui mod. Assumption: Artifact data can be written from the CLI side as the pack says.
  Done when: `fm cockpit publish` creates an Artifact showing the active task, steps with evidence, and queue, and a step edited from the page's comment box appears in `fm task show` within one minute.

- **Wake idle sessions with Monitor and ScheduleWakeup, not tmux send-keys** — FIX — value 5 — effort M — risk med — category: idle handling
  Why: T-0758 "make sure it doesn't sit idle"; the bus types into tmux panes (fragile, needs tmux). Monitor streams a background command's output as notifications, and ScheduleWakeup is self-paced. Assumption: a Monitor on `fm queue watch` can re-trigger the model when new work lands.
  Done when: with no tmux, a queued task added while the session is idle starts within 30s, shown by a test that records the start time.

- **Route work by model and effort per call** — FEATURE — value 5 — effort M — risk low — category: model routing
  Why: T-0755 asks for lower-model agents. The Agent tool takes per-call `model` and `effort`, and subagent frontmatter can set effort. Foreman only passes "sonnet" for S-tier lanes. A routing table maps task tier and step kind (read, grep, edit, review, plan) to model and effort, and `fm doctor` reports spend against it.
  Done when: `fm route show` prints the table, and a recorded L-task run shows haiku for scouting steps, sonnet for edits, and opus at high effort for the plan review.

- **Pin the active step to the host UI with a step-sync guard** — FIX — value 4 — effort S — risk low — category: step tracking
  Why: T-0759 reports it starts other steps without updating the step indicator. PreToolUse already sees every edit. Compare the file or tool target to the active step's declared files and, on mismatch, warn or auto-advance.
  Done when: a test that edits a file belonging to step 3 while step 2 is active yields a step-mismatch notice, and the indicator updates after the fix.

- **Emit review findings through ReportFindings** — FEATURE — value 4 — effort S — risk low — category: review UX
  Why: ReportFindings (typed findings rendered by the host UI) has 0 references, while the reviewer subagent returns prose that Foreman parses. T-0034 (`fm audit run`) wants a structured findings file. Reuse one schema for both.
  Done when: a reviewer run renders findings in the host UI and `fm task finish` blocks on any unresolved high-severity finding from the same payload.

- **Use LSP for the plan-time blast radius** — FEATURE — value 4 — effort M — risk low — category: code intelligence
  Why: LSP (definitions and references) is unused, and `fm map` links tests to sources by filename convention (test_x.py→fmx.py). Real references give an exact list of the tests and callers a step touches. This also feeds T-0214, the edit-time test sentinel. Assumption: an LSP server is available for Python.
  Done when: for a function rename, `fm plan impact <symbol>` lists callers and tests found via references, including ones the filename map misses.

- **Send PushNotification when it needs a human or finishes a milestone** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: `fm notify` runs a user shell command, so each user must wire up their own. PushNotification is native. Fire it only for blocked-on-user states and queue-empty, rate-limited.
  Done when: a blocked task triggers one push (and not a second within the debounce window), shown by a test with a stubbed push tool.

- **Schedule a nightly cloud routine with RemoteTrigger** — FEATURE — value 4 — effort M — risk med — category: scheduling
  Why: `fm night` runs only on the local machine, and Frontier 12 wants overnight proven improvements. A /schedule routine can run the flywheel, the eval inbox and audits when the laptop is closed, then put results in the queue. Assumption: the repo is reachable from the cloud, and the user opts in once.
  Done when: `fm night --cloud` registers one routine and the next morning `fm status` lists its findings.

- **Run read-only lens reviewers as remote-isolated agents** — FEATURE — value 3 — effort M — risk med — category: parallelism
  Why: the Agent tool's isolation "remote" is unused, and worktree lanes consume local CPU and disk. T-0034's headless lens reviewers fit remote isolation because they only read. Assumption: the code can be shipped to the cloud without breaking the privacy settings.
  Done when: `fm audit run --remote` returns lens findings with the local load unchanged, and refuses when the repo is flagged private-local.

- **Wild: Turn the repo into a Claude Docs "war room" for multi-session handoff** — FEATURE — value 3 — effort M — risk med — category: collaboration — wild
  Why: Claude Docs (shared editable docs) is unused. A live doc holds the plan, decisions and open questions. The user edits it in plain language and Foreman reads the diffs as steering, so a person can steer from a browser without a terminal.
  Done when: editing a step's text in the doc changes the plan on the next turn, and the change is logged as a user steer.

- **Wild: Ask Claude on a page — a clickable "why did Foreman do this" trace** — FEATURE — value 3 — effort M — risk low — category: explainability — wild
  Why: the Artifact page's "ask Claude" capability could make each timeline entry (blocked command, decision, verified claim) clickable, answered from the recorded evidence in the task log. It reuses `fm decide` records. Assumption: ArtifactComments reach the session.
  Done when: clicking a blocked-command entry returns the guard rule and the task step that triggered it.

- **Wild: Cross-machine fleet via SendMessage and ListAgents** — FEATURE — value 3 — effort L — risk high — category: fleet — wild
  Why: SendMessage and ListAgents reach other local sessions, cloud sessions and Remote Control sessions on other machines. The user already runs Foreman on JARVIS plus a local box, with releases going to both. The fleet could hand the queue's S tasks to whichever machine is idle.
  Done when: with two machines up, a queued S task is claimed by the idle machine and its result is visible from the other via `fm fleet`.

- **Wild: Self-repairing permissions via fewer-permission-prompts and skill-doctor in the flywheel** — FEATURE — value 3 — effort S — risk low — category: self-maintenance — wild
  Why: /skill-doctor and fewer-permission-prompts exist in the host but Foreman's 73 skills and its guard allowlist are tuned by hand. The overnight run could run both, test the proposed changes on the replay bench and queue passing ones as tasks.
  Done when: `fm night` outputs a skill-doctor report and a proposed allowlist diff, each linked to a task, with none applied unless the bench passes.

- **Delegate /code-review and /security-review levels by task risk** — FEATURE — value 3 — effort S — risk low — category: review
  Why: the built-in /code-review levels (low to max) and /security-review exist, while Foreman has its own reviewer subagent with one depth. Map the L-tier and the guard-touching diffs (T-0275) to a higher level and S-tier to low. Ultra is user-triggered only, so Foreman only suggests it.
  Done when: finishing an L task that touches guard code runs the security review and records its result as evidence, and S tasks record a low-level run.
