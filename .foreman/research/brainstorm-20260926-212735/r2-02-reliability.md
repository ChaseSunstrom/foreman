# Brainstorm — lens: reliability

- **Stamp state with a schema version and add `fm doctor --fsck`** — FIX — value 4 — effort M — risk low
  Why: state is briefs, queue, inbox, and log, all written across many plugin versions and read by hooks at ~30 ms. Nothing in the pack checks for drift or corruption, and a bad frontmatter field can break every hook.
  Done when: a fixture state dir with an orphaned queue entry, a brief with bad frontmatter, and an older schema version is reported by `fsck`. `--repair` fixes it (migrating the old version), and a newer-schema state read by an older plugin degrades to read-only with one warning.

- **Add a Stop-hook circuit breaker for the drive loop** — FIX — value 5 — effort S — risk low
  Why: the Stop hook nudges questions and drives the queue, and the user has already burned 20% of weekly usage in one session. Assumption: no cap exists on consecutive Stop blocks that make no progress.
  Done when: a test simulating N Stop blocks with no new evidence, step, or task change makes the hook allow the stop and write a "stalled: needs decision" inbox item. A run with progress is never cut off.

- **Give the active task a session-ownership lease with heartbeat** — FIX — value 4 — effort M — risk med
  Why: `fm run` headless sessions, an interactive session, and resumed sessions can all touch the single active task. Atomic writes don't say who owns the task, and the pack has no owner field.
  Done when: a second session's mutating `fm` call on a task leased by a live owner is refused with the owner's id. After the heartbeat times out, it takes over and the log records the takeover.

- **Run a resume preflight that checks the brief against the tree** — FEATURE — value 4 — effort S — risk low
  Why: resumed and `fm run` sessions get the brief and resume note as-is. Scope globs, verify-command binaries, and referenced files may be stale, and the pack has no drift check.
  Done when: resuming a task whose scope file was renamed, or whose HEAD moved past the recorded base, produces a one-line "drift: …" in the resume note. Resuming an unchanged task adds nothing.

- **Validate hook payload shapes and record schema drift** — FIX — value 3 — effort S — risk low
  Why: hooks depend on Claude Code's payload fields (tool names, exit codes, `stop_hook_active`). Assumption: a missing or renamed field currently degrades silently, so evidence auto-recording or the guard could quietly stop working.
  Done when: a payload with an unknown or missing required field is logged once to a drift file, the hook still fails open, and `fm doctor` lists the affected hook and field.

- **Build a guard bypass corpus as a table-driven test** — SECURITY — value 4 — effort M — risk low
  Why: the PreToolUse guard blocks dangerous commands and protected paths. Assumption: it is tested on direct forms only, not `bash -c`, `env`/`sudo` prefixes, `../` traversal, symlinked paths, or quoting tricks.
  Done when: a corpus file of at least 60 blocked and allowed commands passes, includes each of those bypass forms, and a new false positive or false negative is added as one line.

- **Add an install/uninstall residue check to `fm doctor`** — CLEAN — value 2 — effort S — risk low
  Why: the constraint says Foreman is removable by uninstall, and hooks and statusline are wired into settings.
  Done when: a test simulating uninstall leaves no Foreman entries in settings, and `doctor` flags any hook that points to a missing plugin path.
