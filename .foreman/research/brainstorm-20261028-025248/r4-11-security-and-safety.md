# Brainstorm — lens: security and safety

- **Refuse `fm answer` and `fm defer` from inside a model run** — SECURITY — value 5 — effort S — risk low — category: approval integrity
  Why: a blocked item is resolved by a command anyone can run. Nothing in the pack says a run can't call `fm answer` on its own needs-you card, which would let the model approve its own blocked prompt (assumption: the verb is reachable from a run's shell).
  Done when: `fm answer` run with a live run's session marker exits non-zero, writes nothing, and journals the attempt.

- **Resolve symlinks before every write check** — SECURITY — value 4 — effort S — risk low — category: path confinement
  Why: write guards that match path text can be bypassed by a repo symlink pointing at `~/.ssh` or a dotfile (assumption: the guard checks the path as written).
  Done when: an edit and a shell redirect into a repo symlink whose target is outside the repo are both refused, and the refusal names the resolved target.

- **Neutralise repo-controlled git config that runs code before any lane touches git** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: a cloned repo's `.git/config` can set `core.hooksPath`, `core.fsmonitor` or filter and diff drivers that git executes on ordinary commands. The pack's fsmonitor and `cat-file` performance ideas would run git more often, so the exposure grows (assumption: lanes run git in the user's clone).
  Done when: a fixture repo with `core.fsmonitor` set to an executable marker file runs `fm check` and the marker is not created.

- **Bind each approval to its targets' inode and hash, and refuse if they change before the run** — SECURITY — value 4 — effort M — risk med — category: time-of-check safety
  Why: the user approves a command, then the file it names can be swapped by a symlink or rewrite before execution. Approval checks the text only (assumption: approvals are recorded per command string).
  Done when: approve `rm build/out.log`, replace the file with a symlink before the run starts, and the run refuses with a message naming the changed target.

- **Render approval cards with the full decoded command and strip terminal control sequences** — SECURITY — value 4 — effort S — risk low — category: approval honesty
  Why: the pack truncates titles and renders model text in the pane. Cursor-movement and OSC escapes can hide or rewrite part of a command on screen, so the user approves text they didn't see (assumption: approval cards print raw strings).
  Done when: a command containing `\x1b[` cursor moves shows its raw form on the card, and a command longer than the card shows an explicit "expand" marker instead of an ellipsis.

- **Escalate after two rephrased attempts at one refused intent** — SECURITY — value 4 — effort S — risk low — category: refusal handling
  Why: the pack explains refusals with a safe alternative, which gives a model a path to retry with a synonym. Refusal-driven rewording is a bypass pattern (assumption: retries are not counted per intent).
  Done when: three spellings of one refused intent in one run stop the run and file a needs-you card showing all three attempts.

- **Skip package lifecycle scripts in lanes unless the manifest allowlists them** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: lanes install dependencies, and `postinstall` scripts run with the user's full access. The pack pins versions but says nothing about which install scripts run (assumption: lanes run installs with default settings).
  Done when: an install in a lane with a package whose `postinstall` writes a marker file, and no allowlist entry, leaves no marker and the receipt lists the skipped script.

- **Publish only projects marked public, with identifiers stripped** — SECURITY — value 4 — effort S — risk med — category: publication safety
  Why: the site and the public transparency log publish run receipts, and receipts quote the user's own words and project names. Nothing in the pack filters personal identifiers or private projects before publish (assumption: publication takes the full receipt).
  Done when: a run in a project not marked public produces no site or log entry, and an email-shaped string in a receipt is replaced with `[redacted]` before publish.

- **Make the journal and receipts append-only at the OS level** — SECURITY — value 3 — effort S — risk low — category: tamper evidence
  Why: the pack treats the journal as the source of truth for every surface, but a run can truncate or rewrite it. An append-only attribute stops that without a new format (assumption: the filesystem supports `chattr +a`).
  Done when: a run's attempt to truncate the journal fails with EPERM, and an append still succeeds.

- **Wild: shadow-deny mode that runs with network off and lists what each run would have reached** — SECURITY — value 3 — effort M — risk low — category: egress review
  Why: wild. Denying egress by default is in the ideas so far, but nobody can tell which hosts a real task needs. A shadow list would let the user grant hosts from evidence rather than guess (assumption: denied connection attempts can be logged).
  Done when: a run in shadow-deny mode that calls an unlisted host finishes, and its receipt names that host under "would have reached."

- **Wild: a monthly phishing drill on the approval card** — SECURITY — value 3 — effort M — risk low — category: approval fatigue
  Why: wild. Approval fatigue is the quiet failure of any guard; a seeded fake approval, opt-in and disclosed, measures whether the user reads the card (assumption: the user will opt in and the drill is labelled in the journal).
  Done when: a seeded fake approval that the user accepts is journaled as a drill, and the next receipt shows the user's hit rate for the last three drills.
