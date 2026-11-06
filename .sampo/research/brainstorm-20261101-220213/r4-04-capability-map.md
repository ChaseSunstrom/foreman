# Brainstorm — lens: capability map

**Capability map (lean and safe).** Reference points are Claude Code's permission rules and sandbox, Codex's sandbox policies, gVisor/bubblewrap/firejail, OPA/Cedar, Socket.dev and `npm audit`, Little Snitch/OpenSnitch, gitleaks, Lakera, and Simon Willison's "lethal trifecta". The pack already covers a lot: hook budgets, context attribution, honeytokens, `fm halt`, Landlock, egress ledger, SBOM and shim ideas. These are the gaps it does not show.

Earlier question I can answer: only checks with no network and no secrets belong in the default proof set. Anything needing a vendor account should print a fixed label ("unverifiable here") that only the user can waive.

- **Wrap hookless agents in a guarded shell** — SECURITY — value 5 — effort M — risk med — category: other agents
  Why: T-0335/T-0337 show Codex/Gemini/opencode lack equivalent hooks, so the guard's "stop commands in bypass mode" promise stops at `claude`. Assumption: they honour `$SHELL` or a PATH shim.
  Done when: `fm shell-wrap codex` makes `rm -rf ~` run through it return the same deny verdict as the Claude Code hook, in a test.

- **Flag the lethal trifecta at session start** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the pack covers commands and MCP pins but no check of dangerous combinations. Private-data access plus untrusted content plus an outbound channel (web fetch, MCP, `gh`) is the real exfiltration path.
  Done when: a fixture config with a web-fetch MCP and an open `.env` read prints one `trifecta: 3/3` line in `fm doctor`. A config with only two legs prints none.

- **Enforce an install cooldown** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: the pack has an SBOM and a dependency diff on ship, but nothing about new package versions. A release under N days old (default 7) is the cheapest filter against hijacked packages. Assumption: the guard already sees `pip/npm/cargo install`.
  Done when: `npm i foo@<version published 1 day ago>` is denied with a "pin the older version" hint. An older version passes.

- **Allowlist egress per lane** — SECURITY — value 4 — effort M — risk med — category: network
  Why: the egress ledger only logs Foreman's own model calls, not what an agent's shell reaches. Assumption: unprivileged `unshare -n` plus a filtering proxy works on the user's hardened kernel.
  Done when: a lane with allowlist `pypi.org` fails `curl example.com` and passes `pip download`. Both attempts appear in the ledger.

- **Meter prompt-cache stability** — PERFORMANCE — value 4 — effort M — risk low — category: context
  Why: 387k context per reply across 5735 replies and a ~2k-char SessionStart note ×89 suggest cache prefixes break often. The pack proposes a byte-stable goal card but nothing measures it.
  Done when: `fm doctor` shows the share of replies whose injected prefix hash matched the previous turn. A test that injects a timestamp turns it red.

- **Prune permissions that were never used** — SECURITY — value 3 — effort S — risk low — category: least privilege
  Why: the pack lints permission rules, but nothing compares them to what ran. Android-style "granted vs used" would shrink the allowlist from evidence.
  Done when: `fm perms --unused 30d` lists allow rules with zero matching tool calls in the event log and prints a removal diff, which it never applies itself.

- **Break retry storms** — FEATURE — value 3 — effort S — risk low — category: reliability
  Why: edit oscillation and stall by yield decay are covered, but identical failing shell commands burning tokens are not. Assumption: the hook log has command hashes.
  Done when: the fourth identical failing command in a lane is denied with "same command failed 3×; change something or ask", and a test shows this.

- **Emit SARIF from `fm check`** — FEATURE — value 3 — effort S — risk low — category: CI
  Why: lean regressions, guard-corpus failures and docs drift already exist as checks, but only as terminal text. SARIF puts them in GitHub code scanning on the existing CI.
  Done when: `fm check --sarif out.sarif` validates against the SARIF 2.1 schema, and a seeded lean regression appears as a result.

- **Publish a guard changelog as a verdict diff** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: guard-corpus replay is proposed per rule change, but nothing tells the user in plain words what a release loosened or tightened.
  Done when: the release step prints "newly allowed: N, newly denied: M" over the corpus, with examples. A loosening without a steer reference fails ship.

- **Run a platform matrix for hooks and the guard** — FIX — value 3 — effort M — risk med — category: portability
  Why: the Desktop app and "headless/server" are listed surfaces. Assumption: path quoting, shell tokenizing and `fcntl` locks differ on macOS, Windows or musl, and the pack shows only Arch runs.
  Done when: CI runs the guard corpus and the hook bench on macOS and Windows runners and the results are green or filed as tasks.

- **Roll back a bypass-mode session with a copy-on-write snapshot** (wild) — SAFETY: SECURITY — value 4 — effort L — risk high — category: recovery
  Why: wild. The pack logs writes outside the repo, but a btrfs/overlayfs snapshot taken at bypass-session start would undo everything, including the home directory and package installs.
  Done when: `fm rewind` restores a scratch directory after a session that wrote outside the repo, tested on a loopback btrfs image.

- **Downgrade bypass when the screen locks** (wild) — SECURITY — value 3 — effort S — risk low — category: presence
  Why: wild. A bypass session unattended while the user sleeps is the risky case. logind's `LockedHint` is a free presence signal that is stricter than any timer.
  Done when: with the session locked, a destructive-class command is parked for the morning bundle instead of run. Unlocking restores bypass.

- **Define an `agents.deny` file honoured by every agent** (wild) — SECURITY — value 3 — effort M — risk med — category: cross-agent
  Why: wild. Like `robots.txt` for repos: one file naming never-touch paths. Foreman's guard enforces it, and AGENTS.md carries one line asking other agents to respect it.
  Done when: editing a listed path is denied on Claude Code and via the shell wrapper, and the doc names which agents honour it.

Next question: which of the six surfaces (Desktop, site, MCP, headless) has no deny-class test at all, and what is the cheapest probe that proves the guard fires there?
Next question: what do users pay in milliseconds and tokens when the guard is working perfectly, versus when it is blocking nothing? Nothing in the pack separates the two.
