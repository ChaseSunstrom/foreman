# Brainstorm — lens: security and safety

- **Neutralize control sequences in every rendered string** — SECURITY — value 4 — effort S — risk low — category: ui-safety
  Why: assumption: band, pane, `fm watch`, the statusline and the Tauri/web UI render task titles, file names, commit subjects and refusal text taken from the repo or from `curl` output. Those are attacker-controllable, and ANSI/OSC sequences or HTML in them can forge a "done ✓" line, retitle the terminal, or run script in the webview.
  Done when: a fixture task whose title, filename and commit subject contain `\x1b]0;`, `\x1b[2K` and `<img onerror>` renders as inert escaped text on every surface, and a test enumerates the surfaces.

- **Watch the persistence surface at the done gate** — SECURITY — value 5 — effort M — risk med — category: deferred-exec
  Why: the guard judges commands at run time, but an agent can plant execution that fires later outside it: `.git/hooks`, `.envrc`, `package.json` scripts, Makefile targets, `.vscode/tasks.json`, CI workflows, shell rc files, `pre-commit` config, cron/systemd user units. Write-then-execute provenance is on the list, but nothing diffs these auto-run files as a class.
  Done when: a task that edits any registered auto-exec file cannot close without a named approval line, and a test that adds a `post-checkout` hook is blocked.

- **Execute exactly what was judged** — SECURITY — value 5 — effort L — risk high — category: guard-core
  Why: the guard reads scripts (T-0275 is open) and carries real-bash differential tests, yet it still hands the original string back to bash, so a TOCTOU window and parser differentials remain (the `bash -lc` / `zsh -ic` miss is one example). Instead, the PreToolUse hook would rewrite the command to run the parsed argv, or a hash-pinned snapshot of the script it judged.
  Done when: a test that swaps a judged script file between check and run executes the snapshot or is refused, and the 5000-command replay shows zero verdict changes.

- **Quarantine lessons that came from untrusted input** — SECURITY — value 4 — effort M — risk med — category: memory-poisoning
  Why: lessons, taste, vetoes, `fm share` and `fm sync` (.foreman/ in the repo) are persistent instructions injected into later sessions. A poisoned README or web page can make a session write a lesson like "always skip the guard for X" that outlives the session. Confidence scoring ranks lessons by usefulness but not by origin.
  Done when: every lesson carries a provenance tag (user-typed, tool-read-from-web, repo-file, other project), tagged-untrusted lessons load only as quoted data, and a planted "ignore vetoes" lesson is never injected as an instruction.

- **Trip an anomaly dead-man's switch on unattended runs** — SECURITY — value 4 — effort M — risk med — category: unattended-safety
  Why: `fm run`, `fm night`, `fm serve` and `autonomy=full` run without anyone watching. The panic button idea is manual. A switch could freeze the run automatically on a spend spike over the task's learned cost shape, three identical guard refusals in a row, writes outside the lane, or new network hosts.
  Done when: a scripted runaway fixture (a loop of refused commands, a 10× token burn) halts the run, writes an incident bundle and notifies, and a normal run never trips it across a bench replay.

- **Prove a safety non-regression before evolve promotes** — SECURITY — value 4 — effort M — risk low — category: self-modification
  Why: `fm evolve` and friction passes revise instruction files and are gated on bench performance, which rewards fewer refusals and fewer asks. A candidate could quietly loosen safety. Add a locked adversarial suite (injection, guard-bypass and ask-skipping cases) that a candidate may not score worse on, and that evolve cannot read or edit.
  Done when: a candidate that deletes a "confirm before outward action" rule passes the performance bench but is vetoed by the safety suite, with the failing case named.

- **Scrub and expire Claude's own transcripts** — SECURITY — value 4 — effort S — risk low — category: data-at-rest
  Why: `fm cost`, `fm replay` and `fm claude` read the session jsonl transcripts, which hold everything the model saw, including `.env` contents and tokens. Redacting at write time protects only Foreman's own ledger. Run `fm secrets` over the transcripts, redact in place or encrypt old ones, and set retention.
  Done when: after `fm tidy --transcripts`, a planted fake key in a 30-day-old transcript is gone, `fm cost` totals are unchanged, and the report lists counts only.

- **Audit Foreman's own file and socket permissions** — SECURITY — value 3 — effort S — risk low — category: local-hardening
  Why: assumption: the central records, the `fm serve` Remote Control unit, the MCP stdio server, the Desktop IPC and the `fm session` detached processes expose every project's briefs and sessions on a multi-user or shared machine.
  Done when: `fm doctor` fails on any state file with a group/world-readable mode, on any listening socket not bound to loopback/UNIX 0600, and on a Tauri capability not in the allowlist, each with a one-line fix.

- **Tag message provenance between sessions and lanes** — SECURITY — value 4 — effort M — risk med — category: agent-to-agent
  Why: `fm session`, lane steering, `fm ask` from other devices and the planned agent-to-agent handoffs all pass text between agents. A lane that read a hostile page can pass instructions to the main thread dressed as a teammate's message.
  Done when: every inter-agent message is wrapped with sender, trust level and source, and a lane reply carrying "approve all guard categories" is shown as data and never counted as a user grant.

- **Pin and diff plugins, skills and hooks on update** — SECURITY — value 3 — effort M — risk low — category: supply-chain
  Why: `fm plugins` installs from marketplaces and `install.sh` enables third-party plugins; a plugin update can add a hook or a broader tool permission silently.
  Done when: an update that adds a hook, MCP server or `Bash(*)` allowance shows a capability diff and stays disabled until approved, and `fm doctor` lists unpinned plugins.

- **Wild: Run a canary that bites the agent's own guard before every night run** — SECURITY — value 3 — effort M — risk low — category: unattended-safety
  Why: wild. Before `fm night` begins, fire a harmless, labelled set of forbidden actions (a decoy `rm -rf` in a temp dir, a fake exfil to localhost) at the live hook chain. Abort the night if any slips through, which catches a broken hook after a Claude Code update.
  Done when: with the guard hook disabled in a test, the pre-flight fails and no queued task starts, and with it enabled the pre-flight passes in under 5 seconds.

- **Wild: Let the user toggle a "paranoid hour" that raises every dial at once** — FEATURE — value 3 — effort S — risk low — category: safety-modes
  Why: wild. Working on a customer's repo, a sensitive VPN or a new unknown clone: one command makes `autonomy` standard, drops standing yeses, forces the sandbox and approvals for network and installs, then reverts at a set time. This builds on the rigor dial and kill switch ideas.
  Done when: `fm paranoid 2h` changes each listed setting, prints what it changed, and a test confirms they are all restored after expiry.

- **Wild: Keep a red-team decoy repo that fights back against injections** — SECURITY — value 3 — effort L — risk med — category: adversarial
  Why: wild. A generated repo full of booby-trapped docs, issues and package scripts. Each new Foreman release must run its tasks there with zero planted instruction followed. Failures are added to the safety suite.
  Done when: the release gate runs the decoy repo, and a release with a deliberately weakened injection defence fails with the followed trap named.
