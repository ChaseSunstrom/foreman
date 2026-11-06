# Brainstorm — lens: capability map

- **Merge Foreman's state files with a custom git merge driver** — FIX — value 4 — effort M — risk med — category: lanes
  Why: round 1 shipped lane-merge fixes (T-0812: pre-merge start point lost), so merging lane branches into state files already bites. Assumption: the queue/ledger files are line-oriented text and conflict on textual merges.
  Done when: a test merges two lane branches that each append a ledger entry and edit different tasks, and the merge finishes with no conflict markers and both changes present.

- **Export audit findings and evidence failures as SARIF** — FEATURE — value 3 — effort M — risk low — category: security
  Why: T-0034 (`fm audit run`) is still deferred and findings are only prose. GitHub code scanning and IDEs already read SARIF. Assumption: findings carry file and line.
  Done when: `fm audit --sarif out.sarif` produces a file that validates against the SARIF 2.1.0 schema and keeps rule ids, locations and severities.

- **Lock down the compact-output store (0600, redact on write, size cap)** — SECURITY — value 4 — effort S — risk low — category: security
  Why: round 1 stores full Bash output in `state/outputs`, and Bash output can contain tokens. The only retention rule so far is a 7-day prune, with no permission or redaction rule. Assumption: the directory uses default umask permissions.
  Done when: a test prints a fake secret through compact output, the stored file is mode 0600 and holds the redacted text, and the directory stays under its configured byte cap.

- **Add `fm daemon install` for systemd user and launchd units** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: `fm serve`, `fm night` and `fm bus watch` all need a long-lived process. The installer wires `~/.claude` but supplies no service unit. Assumption: users currently start these by hand or via tmux.
  Done when: `fm daemon install` writes and enables a unit, `fm daemon status` reports it running, and `fm daemon uninstall` removes every file it wrote.

- **Print a stable `fm status --porcelain` and ship tmux and starship segments** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: the statusline wrapper works only inside Claude Code. A one-line machine format would also serve a shell prompt or tmux bar. Assumption: nothing like this exists in the repo.
  Done when: the output is a documented single line (step, queue depth, needs-you flag) that runs in under 30 ms, with golden tests and a tmux snippet in the docs.

- **Ship a devcontainer feature and Codespaces install** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: the installer supports only Linux, macOS and WSL, and remote or cloud lanes need a repeatable setup. Assumption: `install.sh` can run non-interactively with `--no-bypass`.
  Done when: a devcontainer using the feature builds in CI, `fm doctor` passes inside it, and `fm task new` works.

- **Offer a self-hosted ntfy channel for local-first push** — FEATURE — value 3 — effort S — risk low — category: privacy
  Why: round 1's push goes through the model's PushNotification tool, which is a cloud path, and sensitive repos refuse it. A local topic gives those repos a way to reach the phone. Assumption: users can run or reach an ntfy server.
  Done when: with `notify.ntfy_url` set, a drained queue or open ask posts to that URL (verified against a local stub server) and PushNotification is never requested.

- **Add a state quota with hot/cold tiering** — PERFORMANCE — value 3 — effort M — risk med — category: storage
  Why: `fm tidy` already prunes by age (T-0811), but nothing bounds total size across the ledger, finished tasks, outputs and snapshots. Assumption: state grows without limit on long-running projects.
  Done when: `fm tidy --quota 200MB` moves finished tasks older than N days into a compressed archive, `fm task show` and `fm find` still read them, and the total drops below the quota.

- **Give every mutating `fm` verb `--dry-run` that prints the state diff** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: round 1 added `fm task new --redo` and refusal paths. Users and tests cannot preview a transition before committing it. Assumption: only some verbs have a dry-run today.
  Done when: for each verb in an allowlist, `--dry-run` leaves the state hash unchanged and prints the diff that the real run then produces.

- **Add `fm config explain KEY` showing which layer set each value** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: toggles such as compact output ("off until the user says yes"), bypass mode and the mod are spread across the installer, settings and env. Assumption: more than one layer can set the same key.
  Done when: for 5 seeded conflicts across layers, the command names the winning layer, the file and the losing values.

- **Wild: Give each machine a restricted SSH forced-command Foreman shell** — FEATURE — value 3 — effort M — risk med — category: devices — wild
  Why: assumption: a key in `authorized_keys` could expose only capture, status, ask-approve and pause. That would put every device with an SSH client on the same surface with no web UI or cloud.
  Done when: a test key can run `capture`, `status` and `approve`, and any other command exits with a refusal that is recorded in the ledger.

- **Wild: Add a Foreman Lens browser extension for GitHub PR pages** — FEATURE — value 3 — effort L — risk med — category: devices — wild
  Why: assumption: evidence for a branch already exists locally, and reviewers on a PR page can't see it. A localhost-only read call could overlay the task id, criteria and proof state.
  Done when: opening a PR whose branch maps to a task shows its criteria and verdict, and the page makes no request outside localhost.

- **Wild: Run Pocket Foreman in Termux on a phone** — FEATURE — value 2 — effort L — risk high — category: devices — wild
  Why: assumption: the Python-only kernel could run on-device for capture, ask-approve and viewing, syncing through the git-ref store already proposed. That is the one surface not yet covered.
  Done when: on an Android Termux install, `fm capture "x"` writes a task that appears in the desktop queue after sync.
