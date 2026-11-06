# Brainstorm — lens: setup and configuration

- **Make `fm code` own the setup contract as one resolved-config object** — FEATURE — value 5 — effort M — risk low — category: config
  Why: the pack shows the runner registry (T-1328), `models.json`, worker flags, and per-project needs all planned separately; assumption: they currently resolve in different places (the dropped "two call sites of models.json" note hints at it).
  Done when: `fm code config show --json` prints one object (runner, model, worker, theme, motion, project root) and every field carries its source (flag, env, project, global, default); a test asserts `fm code` consumes only that object.

- **Add a first-run self-install that fixes PATH and shell** — FIX — value 5 — effort S — risk med — category: install
  Why: the user hit "`fm` wasn't a command in their shell (only inside Claude Code)", fixed by hand with a `~/.local/bin` link.
  Done when: in a clean HOME with a plugin-only install, `fm setup` creates the link (or prints the exact line for the user's shell rc), and a fresh `bash -lc 'command -v fm'` succeeds; it never edits an rc file without a printed diff and a yes.

- **Refuse a second Foreman when the worker is Claude Code with the plugin loaded** — FIX — value 5 — effort M — risk med — category: duplicates
  Why: the request says "no duplicate Foreman when it runs Claude Code as a worker"; the nested session loads 66k–133k tokens of plugins and hooks (T-1327 plans the removal, not the detection).
  Done when: a worker launched by `fm code` carries a lineage env marker; the plugin's session hooks see it and become no-ops except guard and leases; a test counts zero Foreman context lines in the nested session's first prompt.

- **Probe a project on first open and write its setup card** — FEATURE — value 4 — effort M — risk low — category: project config
  Why: the nixie run "just isn't doing anything" in a project Foreman had never been told about; assumption: gates, test command and branch rules are not yet detected for an unfamiliar repo before a run.
  Done when: running `fm code` in a new repo writes `.foreman/code.toml` with detected test/build gates, default branch and runner, shows it for one-key accept, and a run in a fixture repo uses those gates.

- **Preflight "can this run work here?" before the first model call** — FEATURE — value 5 — effort M — risk low — category: preflight
  Why: the silent planner ran minutes before the user saw anything; the root causes (wrong cwd, orphans, heavy startup tax, no model) were all knowable in seconds.
  Done when: `fm code` runs a sub-3-second preflight that lists runner reachable, startup token tax, working dir, git state and lock conflicts, and a fixture with a missing binary stops with a single "Next:" line.

- **Make config schema-versioned with migration and a typed editor in the TUI** — CLEAN — value 3 — effort M — risk low — category: config
  Why: `models.json` plus new config lines plus the theme and extension settings are accumulating; assumption: no version field exists yet.
  Done when: an old-format `models.json` loads, migrates with a backup, and `fm code config set runner.default codex` validates against the schema and rejects an unknown key with the nearest valid one.

- **Detect which Foreman is live across plugin, pip/pyz and dev checkout** — FIX — value 4 — effort M — risk low — category: duplicates
  Why: the user installs Foreman as a Claude plugin and also runs a repo checkout (the `~/.local/bin` link); two versions can disagree on guard rules.
  Done when: `fm doctor` lists every Foreman found on PATH and in plugin caches with versions, flags a mismatch, and names the one that wins.

- **Keep secrets out of config by reference** — SECURITY — value 4 — effort S — risk low — category: secrets
  Why: cloud keys sit beside local endpoints in `models.json`; assumption: keys may be written inline.
  Done when: config accepts `key_env: NAME` or a keychain/`pass` reference, `fm code config show` masks values, and a test fails if a literal key is found in a file that is not mode 0600.

- **Wild: Let a pasted error or complaint configure the setup** — FEATURE — value 3 — effort M — risk med — category: self-repair
  Why: assumption: wild; the user said "how come … isn't recognized" and wants Foreman to work it out. Pasting "fm: command not found" or "it isn't doing anything" maps to the matching fix.
  Done when: feeding five recorded user phrases to `fm code why --from-text` produces the correct diagnostic and proposed fix for each, none applied without confirmation.

- **Wild: Offer a config time machine** — FEATURE — value 3 — effort S — risk low — category: config
  Why: assumption: wild; every config write keeps a snapshot, so "it worked yesterday" is answerable.
  Done when: `fm code config history` lists the last 20 changes with diffs and `fm code config restore N` reverts; a test breaks the config and recovers it.

- **Wild: Generate a setup that matches the machine's idle resources** — FEATURE — value 2 — effort M — risk low — category: runners
  Why: assumption: wild; check RAM/GPU/Ollama models and propose a local default (and a context-size cap) when no cloud key or CLI exists.
  Done when: on a fixture with an Ollama stub listing two models, first launch picks the one that fits the declared RAM and says why.

- **Wild: Keep a project-local `fm code` shim that travels with the repo** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: assumption: wild; a committed `./fm` wrapper bootstraps the pinned Foreman for contributors who have no plugin, killing "not a command" for good.
  Done when: in a clean container with only Python, `./fm code --help` runs, verifies the pinned hash, and refuses on mismatch.

- **Set a per-runner startup budget in config and enforce it** — PERFORMANCE — value 4 — effort S — risk low — category: runners
  Why: 66k–133k input tokens per nested call is the observed cost; a configured ceiling turns it into a visible refusal rather than a silent crawl.
  Done when: `runner.claude.max_startup_tokens=20000` makes a launch above it stop with the measured number and the lean-profile fix.

- **Document config from the registry, and fail CI on drift** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: the pack already plans generated keymap and theme docs; the same applies to config keys, so docs and `config explain` cannot disagree.
  Done when: `fm code config docs` regenerates the page and a CI check fails when a key lacks a description or example.
