# Brainstorm — lens: user value

- **Make the service survive logout and reboot** — FEATURE — value 5 — effort M — risk med
  Why: the goal is "don't need Claude Code open" on a headless server. User units die at logout unless linger is on. Assumption: `loginctl enable-linger` works without root here.
  Done when: after logging out of SSH and rebooting, `fm serve status` shows the session running and reachable from claude.ai. If linger can't be enabled, `fm serve` says so instead of failing silently.

- **Supervise with backoff and resume** — FEATURE — value 5 — effort M — risk med
  Why: months of unattended use guarantees crashes, network drops and auth expiry. Assumption: `claude remote-control -c` resumes the last session.
  Done when: killing the `claude` process makes systemd restart it with exponential backoff and resume. After N rapid failures it stops and records the reason, which `fm serve status` prints.

- **Keep the queue moving past blocked approvals** — FEATURE — value 5 — effort M — risk low
  Why: autonomy "full" means Claude never asks mid-run, and `fm ask` collects the questions. A task waiting on the user must not stall the queue.
  Done when: with one task blocked on `fm ask`, the drive continues with the next unblocked task. The pending question is shown in `fm serve status` and at the top of the next chat reply. Answering it unblocks the task.

- **Give `fm run` per-task limits and a circuit breaker** — FEATURE — value 4 — effort M — risk med
  Why: a fresh `claude -p` per task fixes context rot. A stuck or looping task would still burn hours or budget unattended.
  Done when: each task has a wall-clock timeout and an optional turn or spend cap. A task that exceeds it is marked failed with its log path. Three consecutive failures pause the worker and record why.

- **Pause on usage limits and resume automatically** — FEATURE — value 4 — effort M — risk low
  Why: assumption: long unattended runs hit rate or usage limits. Without handling, the worker either spins on errors or dies.
  Done when: a simulated limit error puts the worker in a "waiting until <time>" state shown by `fm serve status`. It resumes without user action and never marks the task failed because of the limit.

- **Show a "while you were away" digest** — FEATURE — value 4 — effort S — risk low
  Why: a user who dips into remote control from a phone needs a quick view. They need to know which tasks finished, which failed, what is blocked, and the latest commits.
  Done when: `fm serve status` and a `/foreman` chat command print a digest under 15 lines covering the period since the last check-in.

- **Default to safe permissions and isolated worktrees** — SECURITY — value 4 — effort S — risk low
  Why: an unattended agent on a server shouldn't get `bypassPermissions` or push rights by default. `--spawn worktree` and `--permission-mode` already exist.
  Done when: `fm serve` defaults to `acceptEdits` with worktree spawn and no push. `bypassPermissions` needs an explicit flag and prints a warning. Test: a default run cannot push.

- **Bound logs and redact secrets** — CLEAN — value 3 — effort S — risk low
  Why: months of output will fill the disk. The rules also say secrets must never be logged, and uninstall must remove everything.
  Done when: logs rotate at a fixed size cap, and a test with a fake token in the environment finds it absent from logs. `fm uninstall` removes the unit, tmux session, logs and lingering state, verified by a listing.
