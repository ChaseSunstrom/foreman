# Brainstorm — lens: setup and configuration

- **Pin trust to the hash of a project's `.foreman/code.toml`** — SECURITY — value 5 — effort M — risk low — category: trust
  Why: assumption: the planned per-project overrides and `CMD {prompt}` runners let a cloned repo ship config that names a command to execute. The guard is the product, so repo-supplied config must not be able to widen it.
  Done when: a fixture repo whose project config defines a runner command is refused with a "trust this config? (hash)" step on first open. Approving it runs the command, and editing the file by one byte asks again.

- **Reject shell-string runner templates and pass the prompt as argv** — SECURITY — value 4 — effort S — risk low — category: runner templates
  Why: the pack shows `CMD {prompt}` templates. Substituting a model- or user-written prompt into a shell string is an injection path. Assumption: templates are split with shlex and run via `sh -c` today.
  Done when: a template containing `sh -c ... {prompt}` fails the config lint with a rewrite hint, and a prompt containing `$(touch X)` run through a valid template never creates X.

- **Derive a project's gates from its own CI files** — FEATURE — value 5 — effort M — risk med — category: project setup
  Why: Foreman's own map lists "gates", and the first request in a new project (nixie) has no verify commands. Reading `.github/workflows`, `Makefile`, `package.json` scripts and `pyproject` lets the setup card propose test/lint/build commands. Evidence: the "probe a project on first open" idea exists, but not its source of truth.
  Done when: on a fixture repo with a workflow running `pytest -q`, `fm code init` proposes exactly that command as the gate, with the file and line it came from, and `--yes` writes it.

- **Keep an install ledger and add `fm code uninstall`/`reset`** — FEATURE — value 4 — effort M — risk low — category: reversibility
  Why: the user already had a ~/.local/bin link fixed by hand, and the planned PATH/shell installer will edit rc files and links. Without a manifest of what was written, nobody trusts the installer.
  Done when: after setup, `fm code uninstall --dry-run` lists every link, rc block and config file Foreman created. Running it for real restores the pre-setup file hashes in a test HOME.

- **Respect read-only and XDG-managed config** — FIX — value 3 — effort S — risk low — category: dotfiles
  Why: assumption: the user runs a hardened Arch setup with dotfile habits, and config may be a symlink into a managed repo. Atomic writes over a symlink or read-only file would break it or silently replace the link.
  Done when: with `config.toml` as a read-only symlink, `fm code config set` writes its change to a state-dir overlay, says so, and `config explain` shows the overlay as the source of the value.

- **Offer config changes as diffs, never apply them** — FEATURE — value 4 — effort M — risk low — category: self-tuning
  Why: this answers "Foreman should figure it out" without silent mutation. After the same silence or startup-tax stall repeats (the nixie run), Foreman proposes "set `startup_budget` to 20s for claude in this project" as a reviewable patch in the inbox.
  Done when: three recorded stalls of one runner produce one pending proposal containing a unified diff, applying it changes the effective config, and ignoring it changes nothing.

- **Switch whole named profiles in one key** — FEATURE — value 3 — effort S — risk low — category: profiles
  Why: the pack has per-intent flags (`--careful`, `--cheap`) and layered config, but no named bundle of runner, caps, motion and local-only settings (for example `overnight`, `offline`, `demo`) that the TUI header shows and switches.
  Done when: `fm code --profile offline` refuses a non-loopback endpoint, and the TUI header shows the active profile and cycles it with one key.

- **Ship conservative default caps and say so at first run** — FIX — value 4 — effort S — risk low — category: safe defaults
  Why: the user wants to leave runs unattended ("full auto", "don't stop"). Assumption: no default spend, time or turn cap applies out of the box, so a first unattended run on a 100k-token-per-call CLI can burn unbounded.
  Done when: a fresh HOME run prints its resolved caps (cost, wall time, turns) once, a run exceeding the time cap stops with a `Next:` line naming the config key, and raising it is one line.

- **Scope gates by sub-package in monorepos and worktrees** — FEATURE — value 3 — effort M — risk med — category: project resolution
  Why: assumption: "the project is the current directory" breaks when the user starts in a package subfolder or a git worktree, and the wrong-directory warning idea doesn't say which root and which gates apply.
  Done when: starting in `pkg/a` of a fixture monorepo resolves the root, names it on the first line, and runs only the gates declared for `pkg/a`.

- **Generate every `FM_CODE_*` env override from the config schema** — CLEAN — value 3 — effort S — risk low — category: config schema
  Why: CI, containers and Claude plugin workers need config without files, and hand-written env names drift. One schema can drive the file keys, the env names, `--print-config` JSON and the docs.
  Done when: each schema key has a working env override, a test sets every one and sees it in `config explain` as source `env`, and the docs page diffs clean against the schema.

- **Wild: Fuzz the config loader with generated configs and corrupted files** — CLEAN — value 3 — effort M — risk low — category: reliability
  Why: assumption: wild but cheap. Generate random valid and mangled configs (truncated, wrong types, duplicate keys, huge values) and assert `fm code`, `doctor` and the TUI never traceback and always fall back to last-good with a line-accurate message.
  Done when: a 1,000-case seeded fuzz run in CI ends with zero tracebacks and every bad file yields a message naming the key and line.

- **Wild: Let `fm code setup` write itself from the user's shell history** — FEATURE — value 3 — effort M — risk med — category: onboarding
  Why: assumption: wild. With an explicit read-only opt-in, scan local history for CLI names the user actually invoked (`codex`, `aider`, `ollama run`) and rank the runner audition by real habits. Nothing leaves the machine and the scanned text is never stored.
  Done when: with a fixture history file and opt-in, setup lists the CLIs found with counts and pre-selects the most used one. Without opt-in the file is never opened, which a test checks with a denied-open stub.

- **Wild: Emit a "why it behaved this way" config receipt on every run** — FEATURE — value 4 — effort S — risk low — category: provenance
  Why: assumption: wild. Each run journal stores the resolved config hash plus the winning source of each non-default key, so "it just isn't doing anything" can be answered as "this run used runner X from project config, cap Y from env". A diff between two runs' receipts shows what changed.
  Done when: `fm code config diff RUN_A RUN_B` prints the keys that differed with their sources, and two runs with identical config print "same".

- **Wild: Hold a "fresh machine" CI job that runs setup from nothing** — CLEAN — value 4 — effort M — risk low — category: first five minutes
  Why: the user hit `fm` missing from PATH and CI broke over an un-set-up HOME. A container with empty HOME, only the claude CLI stub on PATH, and no network config should complete `fm code` → first request in a time budget, ratcheted.
  Done when: the CI job starts with an empty HOME and ends with a closed task in under the budget, and a regression in setup steps fails the job.
