# Brainstorm — lens: reliability

- **Claim tasks with a lease and a single-writer lock** — FIX — value 5 — effort M — risk med
  Why: assumption: `fm serve` (drive hook) and `fm run` can both touch the queue in ~/.claude/foreman/state, and a crash mid-task leaves it "in progress" forever.
  Done when: killing `fm run` with SIGKILL mid-task leaves the task requeued (attempt count +1) after lease expiry, and a second worker started concurrently exits with a clear "already running" message.

- **Add a supervisor with restart backoff and a crash-loop breaker** — FEATURE — value 5 — effort M — risk low
  Why: the plan relies on a systemd user unit plus tmux for months of uptime; remote-control disconnects, auth expiry and OOM are normal at that scale. assumption: `Restart=` alone would hammer the API on a persistent failure.
  Done when: killing the tmux session or `claude` process restarts it within N seconds, and 5 failures in 10 minutes stops the unit and writes a visible "failed" status.

- **Enforce per-task watchdogs and attempt caps in `fm run`** — FEATURE — value 5 — effort M — risk low
  Why: a fresh `claude -p` per task can hang, loop, or burn spend without finishing. assumption: no timeout or retry cap is planned yet.
  Done when: a stub `claude` that sleeps forever is killed at the configured timeout, the task is marked failed after max attempts, and the queue moves on.

- **Park blocked tasks and continue instead of stalling** — FEATURE — value 4 — effort M — risk med
  Why: `fm ask` depends on the user's next chat reply, but `fm run` has no chat, so an approval-needing task could block the queue for days. assumption: approvals are not yet persisted with an owner or expiry.
  Done when: a task needing approval is marked `blocked`, the worker proceeds to the next task, and answering the ask later un-parks it.

- **Detect usage limits and auth expiry, then pause with backoff** — FEATURE — value 4 — effort M — risk med
  Why: unattended months will hit rate limits, plan caps and login expiry. assumption: `claude -p` exits with distinguishable errors or messages for these cases.
  Done when: a simulated limit or auth-failure output pauses the worker with exponential backoff (no retries counted as task failures) and `fm serve status` shows the reason.

- **Ship `fm serve status` and `fm doctor` with a heartbeat** — FEATURE — value 4 — effort S — risk low
  Why: nobody watches a headless server, so silent death is the main failure. assumption: `loginctl enable-linger` may need to be checked, since user units die at logout without it.
  Done when: status reports last heartbeat age, current task, last error and linger state, and exits non-zero when the heartbeat is stale.

- **Bound and redact logs, and make uninstall remove everything** — SECURITY — value 4 — effort S — risk low
  Why: the rules say secrets are never logged and everything is removable by uninstall. Months of `claude` output otherwise grow unbounded and may capture tokens.
  Done when: logs rotate at a size cap, a seeded fake token never appears in them, and uninstall removes the unit, tmux session, logs and state.

- **Isolate each unattended task in a branch or worktree and default to a non-bypass permission mode** — SECURITY — value 4 — effort M — risk med
  Why: autonomy full with no human watching means a bad task can damage the repo. assumption: `bypassPermissions` is tempting for headless use; `--spawn worktree` is available.
  Done when: each task runs on its own branch or worktree, and a failed task can be discarded with one command without touching main.
