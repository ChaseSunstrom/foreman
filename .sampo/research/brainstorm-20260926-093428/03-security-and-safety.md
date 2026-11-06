# Brainstorm — lens: security and safety

- **Default to a scoped permission mode, never bypassPermissions** — SECURITY — value 5 — effort S — risk low
  Why: `--permission-mode` accepts bypassPermissions, and `fm serve` plans autonomy full with no one watching. Anyone who gets into the claude.ai session can run arbitrary commands as the user. Assumption: the server holds SSH keys and deploy creds.
  Done when: `fm serve` with no flags starts with acceptEdits or dontAsk plus an allowlist. Bypass needs an explicit `--i-understand` flag, and `fm serve status` prints the active mode.

- **Add a hard kill switch and budget guard** — SAFETY — value 5 — effort M — risk low
  Why: "forever" plus a Stop-hook drive can loop indefinitely. Nothing in the pack caps turns, wall-clock time, or spend.
  Done when: a `STOP` sentinel file under ~/.claude/foreman/state halts drive and `fm run` within one turn. Configurable max tasks per hour and per day pause the queue and log why. A test simulates a runaway queue and confirms it halts.

- **Confine the blast radius with worktrees and branch rules** — SAFETY — value 4 — effort M — risk med
  Why: `--spawn worktree` exists. Unattended runs can otherwise push, force-push, or reset the user's working tree.
  Done when: `fm run` and `fm serve` work on a `foreman/*` branch or worktree. A PreToolUse hook denies `git push --force`, pushes to main, and `rm -rf` outside the repo. A test for each denial passes.

- **Lock down state, unit, and tmux permissions** — SECURITY — value 4 — effort S — risk low
  Why: secrets must never be logged, and the state dir and tmux socket are otherwise readable by other local users. Assumption: the server is shared or has other services.
  Done when: state dir is 0700, files 0600, the tmux socket sits in a private dir, and the unit file holds no secrets (it uses an `EnvironmentFile` with 0600). A test greps the logs and unit for token-shaped strings and finds none.

- **Treat queued and repo content as untrusted in headless runs** — SECURITY — value 4 — effort M — risk med
  Why: `fm run` feeds task briefs into fresh `claude -p` sessions with no human present. Injected text in issues, READMEs, or fetched pages can steer a full-autonomy agent. Assumption: briefs can include external text.
  Done when: `fm run` wraps external content in data-tagged blocks, restricts tools per task type (no network or secrets access by default), and a fixture with an injected "curl … | sh" instruction is not executed.

- **Prevent duplicate or orphaned servers with locking and an audit log** — SAFETY — value 3 — effort M — risk low
  Why: systemd restart plus tmux can leave two `claude remote-control` processes on one repo. That means concurrent writers and confusing state.
  Done when: a per-repo flock ensures one server and one worker. `fm serve stop` and uninstall remove the unit, tmux session, and lock. An append-only audit log (no secrets) records each task start, end, tool denials, and who approved what.

- **Make `fm ask` approvals unforgeable and non-blocking** — SECURITY — value 3 — effort M — risk med
  Why: approvals are answered by the user's next chat reply, and headless `fm run` has no chat. An agent or injected text could self-answer.
  Done when: in headless mode, `fm ask` parks the task as "blocked-on-user" and continues with other tasks. Only replies arriving through the remote-control user channel resolve it, and a test confirms tool output cannot resolve a pending ask.
