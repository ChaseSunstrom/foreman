# Brainstorm — lens: security and safety

- **Lock down what `fm sync` may import** — SECURITY — value 5 — effort M — risk med
  Why: sync imports `.foreman/` from the repo before every fm command, so a pulled branch could inject queue items or grant-like flags. This is an assumption about the importer's current allowlist.
  Done when: a test repo whose `.foreman/` carries forged core/remote/plugin approvals, oversize files or bad schema imports none of them, and the rejection is logged.

- **Redact secrets before evidence is stored or synced** — SECURITY — value 5 — effort M — risk low
  Why: `fm task evidence --run` records raw command output, and `fm sync` mirrors state into a committed folder. The MUST list says no secrets get committed. Assumption: no scanner exists on either path.
  Done when: output containing a fake AWS key, a `ghp_` token and a `.env` line is stored as `[REDACTED]`, and `fm sync` refuses to export a file that still matches a secret pattern.

- **Make the guard fall back to a verified copy, not fail open** — SECURITY — value 4 — effort M — risk med
  Why: T-0033. A half-applied guard edit made every write fail closed, and recovery needed an unusual command.
  Done when: with a syntax error in the working `fmguard`, hooks load the committed copy after a hash check. If no verified copy exists they still fail closed, and `fm doctor` names the recovery command.

- **Gate persistence vectors under a new `persist` category** — SECURITY — value 4 — effort M — risk med
  Why: MASTER §10 says crontab and shell rc persistence are not gated. `.git/hooks`, `~/.config/systemd/user`, and `~/.claude/settings*` writes are similar. Assumption: `fm serve` writes its own unit only through `fm`, so it stays allowed.
  Done when: `crontab -`, appending to `~/.bashrc`, and writing `.git/hooks/pre-commit` each raise an `fm ask` prompt, while `fm serve install` still works.

- **Pin plugin approvals to the exact content approved** — SECURITY — value 4 — effort M — risk med
  Why: plugin installs need the user's yes, but the pack doesn't say the approval is bound to a version or hash. That leaves a gap between approval and install. Assumption: approvals are keyed by name only.
  Done when: an approval records name, source and content hash, is single-use, and expires. Changing the upstream content after approval makes the install fail with a re-ask.

- **Strip terminal escapes and cap size on injected or displayed text** — SECURITY — value 3 — effort S — risk low
  Why: captured requests, evidence output and reviewer files are rendered by the dashboard and statusline and re-injected by SessionStart and resume. ANSI or OSC sequences and injection text could pass through. Assumption: no sanitizer exists.
  Done when: a captured request containing `\x1b]0;x\x07` and "ignore previous rules" is shown escaped, and hook injections stay length-capped and labelled as data.

- **Add an adversarial guard regression corpus** — SECURITY — value 3 — effort M — risk low
  Why: the guard blocked the agent's own legitimate edits (quoted paths, "claude plugin" strings), and obfuscation beats it. There is no measured false-positive or false-negative baseline.
  Done when: a table-driven test of 60 or more allowed and blocked commands (base64, `$IFS`, heredocs, quoting) runs in CI, and known bypasses are listed as expected-fail so gaps stay visible.

- **Harden the `fm serve` unit and state permissions** — SECURITY — value 3 — effort S — risk low
  Why: Remote Control runs as a long-lived systemd user unit. Assumption: it has no sandbox directives and state files use the default umask.
  Done when: the generated unit sets `NoNewPrivileges`, `PrivateTmp` and `ProtectSystem=strict`. State dirs are mode 0700, and `fm doctor` warns on looser permissions.
