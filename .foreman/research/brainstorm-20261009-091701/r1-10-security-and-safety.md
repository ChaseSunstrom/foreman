# Brainstorm — lens: security and safety

- **Run guarded commands inside an OS sandbox as a second layer** — FEATURE — value 5 — effort L — risk med — category: guard
  Why: the guard is a parser, and users keep finding bypasses (`bash -lc`, `python -c`, brace tricks, download-into-shell, symlink `rm`, T-0275 script files). Each fix is a patch on a language that can't be fully parsed. Assumption: bwrap or Landlock is available on Linux and macOS, with a fallback.
  Done when: a corpus of known parser-evading commands, run in a lane, cannot write outside the lane worktree or reach the network, even when the guard is made to allow them.

- **Detect weakened verification at the done gate** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: Foreman's core claim is "verifies with recorded evidence". Evidence is only worth something if the model can't win by deleting, skipping or loosening tests. One recorded criterion already "ran no tests" because its verify command was malformed. Assumption: no such check exists today.
  Done when: a task diff that adds `skip`/`xfail`, deletes asserts, or narrows a test selector blocks `fm task done` until the user explicitly approves or the change is justified in the brief.

- **Hash-chain the ledger and evidence, and run gates out of the model's reach** — SECURITY — value 5 — effort M — risk med — category: integrity
  Why: evidence, ledger and briefs are plain files the model can edit. `fm trust` exists only because the guard files are protected, and the ledger is not. Assumption: the ledger is an append-only file without chaining.
  Done when: editing or deleting a past ledger or evidence entry makes `fm doctor` fail, and gate results carry a runner-produced digest that the model's own writes can't forge.

- **Taint-track untrusted content and gate actions it triggers** — FEATURE — value 5 — effort L — risk med — category: prompt injection
  Why: Foreman runs unattended (`fm night`, `fm run`, full autonomy) and reads web pages, MCP output, files and the landscape scan. Nothing in the pack separates instructions from the user and instructions embedded in fetched data. Assumption: tool results are not currently labelled by origin.
  Done when: in a replayed session, a command whose arguments came from fetched web text or a downloaded file requires `fm ask`, while the same command typed by the user does not.

- **Track write-then-execute provenance** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: it generalises T-0275 and the "download feeding a shell" fix. The guard should know a file's origin (downloaded, model-written, from the repo) and judge what it runs by that. It also covers the evasion of writing a script in one call and running it in the next.
  Done when: running a script created earlier in the session by a download or a heredoc is judged on its content, and a script containing a guarded action is refused.

- **Fuzz the guard against real bash nightly** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard already has real-bash differential tests and a 5000-command replay, yet users found `bash -lc`, braces and `python -c` gaps by hand. A grammar-based mutation fuzzer in `fm night` would find those first. Assumption: the differential harness can be driven programmatically.
  Done when: `fm night` mutates the replay corpus and reports each case where the guard's predicted effects differ from what real bash does in a scratch directory, filing each as a task.

- **Give each lane a least-privilege capability scope** — FEATURE — value 4 — effort M — risk med — category: lanes
  Why: builders run in worktrees with a brief, but the `jarvis-web/node_modules` symlink case shows scope is judged by path guesses. A scope derived from the brief (paths, commands, network) and enforced by the guard would make confinement explicit. Escalation would go through `fm ask`.
  Done when: a builder lane touching a path outside its declared scope is refused with the scope shown, and an `fm ask` grant widens it for that lane only.

- **Scan all outbound data: sync, share, eval capture, export** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: `fm sync` mirrors briefs into the repo, `fm share` shares lessons across projects, T-0035 plans redacted eval cases, and `fm export` writes AGENTS.md. Each is a way for secrets or private paths to reach a public repo. Assumption: redaction exists for `share` but is not one shared choke point.
  Done when: every outbound writer goes through one scanner, and a planted fake key in a brief is blocked or redacted in all four outputs.

- **Gate dependency changes on supply-chain signals** — FEATURE — value 3 — effort M — risk low — category: supply chain
  Why: `fm deps` only reports versions that are behind. Whenever a lockfile diff adds a package, the gate could check for typosquat distance, package age, install scripts and maintainer changes.
  Done when: adding a package with a postinstall script or a name one edit from a popular package blocks `done` with the reason.

- **Auto-snapshot before risky actions and add `fm undo`** — FEATURE — value 4 — effort M — risk low — category: recovery
  Why: Foreman defaults to bypass mode and blocks by pattern, so anything the guard misses is unrecoverable. Assumption: no snapshot layer exists beyond git.
  Done when: after a guard-allowed destructive edit, `fm undo` restores the tree, including untracked files, to the pre-action state.

- **Plant honeytokens to catch exfiltration (wild)** — FEATURE — value 3 — effort S — risk low — category: detection
  Why: assumption: wild. Fake credentials sit in decoy `.env` and `~/.aws` files. Any command, transcript or outbound request that contains one is blocked, logged and flagged as a successful injection.
  Done when: a command that reads the decoy and sends it anywhere is blocked, and the ledger records which task and which origin led to it.

- **Run a red-team subagent against the guard (wild)** — FEATURE — value 4 — effort L — risk med — category: adversarial agents
  Why: assumption: wild. A sandboxed adversary subagent tries to reach canary actions (write a canary file outside the lane, touch a decoy secret) past the live guard. A separate verifier confirms each success. Only confirmed bypasses become tasks, so the loop closes without unchecked changes.
  Done when: a seeded known bypass is found by the red-team run within its budget and filed as a task with a reproducing command.

- **Preview risky commands in a shadow filesystem (wild)** — FEATURE — value 3 — effort L — risk high — category: guard
  Why: assumption: wild. For commands the guard can't classify, run them in an overlay copy of the tree and diff the result. The user, or `fm ask`, then approves or discards the actual effect rather than a guess about it.
  Done when: an ambiguous command produces a diff of files created, changed and deleted, and nothing in the real tree changes until approved.

- **Require signed approvals for `fm ask` from other devices** — SECURITY — value 3 — effort M — risk med — category: authorization
  Why: with `fm serve`, the desktop app and remote sessions, a grant could come from anywhere. Today it is "their next message decides", and nothing proves the message was typed by the user rather than injected into the session. Assumption: grants are not authenticated beyond the channel.
  Done when: a grant that doesn't carry a valid device signature, or that was written by the model, is rejected.
