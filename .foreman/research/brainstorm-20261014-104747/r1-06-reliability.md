# Brainstorm — lens: reliability

- **Replace tmux send-keys wakeups with a native idle watchdog** — FIX — value 5 — effort M — risk med — category: liveness
  Why: T-0758 ("make sure it doesn't sit idle like it is"). `fm bus` types into tmux panes, which breaks when there is no tmux, the pane moved, or the session is mid-prompt. ScheduleWakeup and CronCreate are unused (0 references). Assumption: they can be called from a Foreman skill or hook-injected instruction while the queue is non-empty.
  Done when: with tmux absent, a session that stops with queued work and no `needs you` flag is resumed within N minutes, and a test asserts the wake was scheduled via ScheduleWakeup. send-keys stays as the fallback.

- **Block step drift in PreToolUse** — FIX — value 5 — effort M — risk med — category: state integrity
  Why: T-0759 reports that Foreman works on other steps without updating the current step. Resume-at-exact-step depends on that pointer being true. Assumption: each step records the files or commands it expects.
  Done when: an edit outside the current step's declared scope either auto-advances the step with an evidence note or is refused with a message. A test replays a drift transcript and the pointer ends correct.

- **Stream gates through Monitor with a hang detector** — FEATURE — value 4 — effort M — risk low — category: gates
  Why: full gates (`fm doctor`, roundtrip, bench) run as blocking commands, and a hung one stalls the session silently. Monitor is unused. Assumption: gate output has a steady cadence.
  Done when: a gate that prints nothing for the stall threshold is flagged and killed, the task records "✗ stalled", and the session is not blocked while it runs.

- **Push to the phone when blocked or finished** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: `fm notify` only runs a user shell command, and the user never wants to be handed commands. PushNotification is unused. A needs-you state that nobody sees is a reliability failure.
  Done when: a task entering blocked or needs-you, or the queue draining, sends one PushNotification. Repeats are rate-limited, and a test stubs the tool call.

- **Catch hook-schema drift with a nightly canary** — FIX — value 4 — effort M — risk low — category: compatibility
  Why: Foreman uses 14 hook events and has 1.2.x releases and `claude plugin eval`, but nothing tests the next Claude Code release. Assumption: a cloud routine (RemoteTrigger or /schedule) can run `roundtrip.py` against the newest `claude`.
  Done when: a routine runs the roundtrip and `bench_hooks.py` on the latest Claude Code daily, and a failure files a captured task naming the broken event.

- **Run reviewer findings through ReportFindings** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: the verification work (typed claims, reproducible findings) parses reviewer prose, and `fm audit run` (T-0034) is deferred. ReportFindings gives typed findings the host renders. Assumption: its schema carries severity, file, line and a repro.
  Done when: the reviewer subagent emits ReportFindings. `fm task finish` reads them instead of parsing text, and a malformed prose-only review fails the gate.

- **Fsck and journal the central task store** — FIX — value 4 — effort M — risk med — category: state integrity
  Why: many writers touch the central record (hooks, lanes, `fm bus`, children), and hooks are latency-gated. Assumption: the store is files with no write-ahead log.
  Done when: `fm doctor` runs a store fsck. Killing a writer mid-update at a random point never loses an acknowledged task, and a test does this 100 times.

- **Reap orphaned worktree lanes using ListAgents** — FIX — value 3 — effort M — risk low — category: lanes
  Why: lanes use Agent isolation "worktree" and S-tier lanes pass model "sonnet". A crashed lane leaves a dirty worktree and a task stuck "in lane". ListAgents is unused. Assumption: it exposes liveness for local agents.
  Done when: a lane whose agent is gone for more than N minutes has its worktree diff saved as a patch, the task returned to the queue, and the worktree removed.

- **Verify rename and removal claims with LSP** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: a step like "remove X" or "rename X" is currently checked by grep or tests. LSP references are unused, and a missed caller passes if tests don't cover it.
  Done when: a claim typed rename/remove is accepted only when LSP finds zero remaining references. A fixture with a dynamic caller proves it is refused.

- **Chaos-test resume** — FEATURE — value 4 — effort M — risk low — category: resilience — wild
  Why: resume at the exact step after `/compact` is the core promise, yet the e2e covers only the happy path. Assumption: a seeded fault injector fits the existing test layout.
  Done when: `fm chaos` runs the roundtrip while killing hooks, truncating a state file, and compacting at random steps. Every run either resumes at the right step or fails loudly, over 50 seeds.

- **Run a dead-man's-switch routine in the cloud** — FEATURE — value 4 — effort M — risk med — category: liveness — wild
  Why: if the machine sleeps or the session dies, nothing local can notice. RemoteTrigger and PushNotification are unused. Assumption: a cloud routine can read a heartbeat the machine publishes, and the user opts in to what is sent.
  Done when: a routine pushes a notification if no heartbeat arrives for N minutes while the queue is non-empty, and stays silent when the queue is empty.

- **Publish a flight-recorder Artifact** — FEATURE — value 3 — effort L — risk med — category: observability — wild
  Why: plan, step pointer, evidence and the last decisions live in files that only `fm` reads. Artifact offers a live private page with comments sent to Claude. Assumption: nothing sensitive is published without a setting, and secrets are redacted first.
  Done when: one page shows the live step, recent evidence and blocked items, and a comment on it becomes a captured task.

- **Shadow-replay hook decisions in a second session** — SECURITY — value 3 — effort L — risk med — category: determinism — wild
  Why: the guard blocks dangerous commands in bypass mode, and a guard that decides differently on the same input is a hazard (see the heredoc and pipe-to-bash disputes). Assumption: guard decisions are logged with their inputs.
  Done when: a nightly replay feeds the last 1,000 logged commands to the current guard, and any decision that differs from the logged one is reported with the diff.

- **Recover after a failed Stop via TaskCompleted** — FIX — value 3 — effort S — risk low — category: close-out
  Why: Gemini's AfterAgent deny discards the answer (T-0337). Claude Code's TaskCompleted hook is already used, but a denied close-out can loop or lose the final answer. Assumption: there is no deny-count cap today.
  Done when: after N consecutive denials the close-out is accepted with a recorded "unverified" flag, and the final answer is delivered intact.
