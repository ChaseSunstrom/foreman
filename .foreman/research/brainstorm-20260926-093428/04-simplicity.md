# Brainstorm — lens: simplicity

- **Ship `fm serve` alone first; defer `fm run`**: FEATURE, value 5, effort M, risk low
  Why: the user's verbatim goal is remote control that keeps going forever. `fm run` is a second execution model (its own queue-popping and failure handling) that the goal doesn't require. Add it only if context rot shows up in real use.
  Done when: `fm serve` in a fresh repo, then a feature request typed from claude.ai, ends with a task brief queued and worked, with no `fm run` code shipped.

- **Let systemd be the only supervisor; make tmux optional** — CLEAN — value 4 — effort S — risk med
  Why: assumption: `claude remote-control` may not need a TTY. If it doesn't, the unit runs it directly, with `Restart=on-failure`, `RestartSec` and journald for logs, so there is no tmux session to drift out of sync with the unit. Verify TTY need first. If a TTY is required, keep tmux inside the unit and don't add a second lifecycle.
  Done when: killing the `claude` process makes systemd restart it, and `fm serve status` agrees with `systemctl --user is-active`.

- **Make `fm serve status|stop` thin wrappers over systemctl** — CLEAN — value 4 — effort S — risk low
  Why: the pack says everything must be removable by uninstall and state lives in `~/.claude/foreman/state`. Deriving status from `systemctl --user` plus the existing state avoids a pidfile or registry that can go stale. A single generated unit file, named per repo, is the only new artifact.
  Done when: after `fm serve stop` followed by uninstall, no unit file, symlink or state entry remains, and `fm serve status` never reads a pidfile.

- **Expose only `--name` and an optional `--permission-mode`, with a safe default** — CLEAN — value 3 — effort S — risk low
  Why: `claude remote-control` has many flags (`--spawn`, `--capacity`, `--session-id` and others). Passing them all through creates maintenance surface, and `bypassPermissions` on an unattended server is dangerous. Assumption: the defaults are fine for a single user.
  Done when: `fm serve --help` lists at most two options, and `bypassPermissions` is refused unless it is passed explicitly.

- **Never capture remote-control output in Foreman logs** — SECURITY — value 4 — effort S — risk low
  Why: the pack says secrets must never be logged, and remote-control output likely contains session URLs or tokens (assumption). Leave stdout and stderr to journald and don't tee, parse or copy them. `fm serve attach` or `journalctl` covers debugging.
  Done when: grepping `~/.claude/foreman` after a serve run finds no URL or token text from the server output.

- **Add an idle-and-backoff rule so "forever" doesn't burn tokens** — FIX — value 4 — effort S — risk med
  Why: assumption: the drive keeps Claude working through the queue, so an empty queue or a task that fails repeatedly could loop. Stopping the drive on an empty queue, and after N consecutive failures on the same task, parks the task and surfaces it via `fm ask`. This reuses existing mechanisms with no new daemon.
  Done when: a test with an always-failing task stops after N attempts and posts one `fm ask`, and an empty queue causes no further turns.

- **Reuse the existing full-autonomy and `fm ask` path with no new approval channel** — CLEAN — value 3 — effort S — risk low
  Why: autonomy "full" already collects user-only approvals through the next chat reply. That fits remote control, where the user is already typing in claude.ai. A separate notification mechanism would add complexity, and hooks can't use the network anyway.
  Done when: an approval requested during an unattended run is answered from claude.ai, with no new code path or config key.
