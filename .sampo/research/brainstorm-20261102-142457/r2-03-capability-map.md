# Brainstorm — lens: capability map

- **Run an obfuscation-transform exam against the guard** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: assumption: the guard matches literal command shapes. Bashfuscator-style encodings (base64 to `sh`, `$'\x72m'`, `${IFS}` splitting, `eval`, here-docs, backticks) are the standard bypass class, and nothing in the pack names a corpus of them.
  Done when: a generated corpus of at least 200 obfuscated variants of 10 blocked commands runs in `fm exam`, and the guard blocks all of them or lists each miss by transform name.

- **Differential-parse the guard against a real shell parser** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the pack has "count the commands the guard couldn't parse", but not a comparison with the shell's own parse. Parser disagreement, where the guard sees one command and bash runs another, is where bypasses live. Compare against `shfmt`'s AST or `bash -n`.
  Done when: a nightly check feeds generated and fuzzed command lines to the guard's tokenizer and to the reference parser, and a disagreement list (empty or not) is written to the ledger.

- **Resolve realpath before protected-path rules** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: assumption: path rules match strings. A symlink, `..`, a hardlink or a bind mount to `$HOME` or `.ssh` defeats a string match, and "Protect named paths from every agent" is on the list.
  Done when: a test creates `ln -s ~/.ssh ./x` and `rm -rf ./x/` is blocked, while the same command on a real temp dir is allowed.

- **Scrub every child's environment to an allowlist** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: Foreman spawns tool-less `claude -p` children, lanes, provers and hooks. Without an allowlist, each inherits every key in the user's shell. Related ideas cover egress, not what the child can read.
  Done when: a canary variable `FM_CANARY_SECRET` set in the parent is absent from `env` inside a brainstorm child, a prover and a lane, and an `fm doctor` row passes.

- **Bind each threat-model row to a test** — SECURITY — value 3 — effort M — risk low — category: docs
  Why: "Publish what Foreman is bad at" and "map MASTER.md clauses to tests" exist, but not a STRIDE-style `THREAT.md` (assets, actors, trust boundaries). Each row would cite the guard test or exam item that covers it, or say "accepted, not covered".
  Done when: `fm check` fails when a threat row has neither a resolvable test id nor an `accepted:` reason.

- **Add `fm forget <repo|path|term>`** — FEATURE — value 3 — effort M — risk med — category: privacy
  Why: lessons, captures, evidence, ledgers, caches and the user model all keep data about a repo. "Scrub a pasted secret" handles one string but not removing a whole project or topic. Assumption: users will eventually want to drop a client repo.
  Done when: after `fm forget <repo>`, a grep of the state dir for the repo's path and a distinctive planted token finds nothing, and the hash chain still verifies via a recorded tombstone.

- **Flag secrets in command arguments** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: tokens typed on a command line (`curl -H "Authorization: [REDACTED]"`, `--password=`) end up in `ps`, shell history, transcripts and the ledger. "Scan allowed outbound text" covers a different surface.
  Done when: the guard warns on a literal token in argv, suggests an env var or a file, and the ledger line stores the redacted form.

- **Ship a typed safe-ops tool server in place of raw bash for risky verbs** — FEATURE — value 4 — effort L — risk med — category: guard
  Why: assumption: blocking and rewriting bash is a losing game. Typed intents (`delete_path`, `git_reset`, `move`) let Foreman enforce trash, snapshot and scope by construction. `trash-cli` and Claude Code's own tool permissions are the references, and "Neutralize the call instead of blocking it" only gestures at this.
  Done when: in a session steered to the tool, a `delete_path` on a directory goes to a TTL trash with a restore command, and the same session's raw `rm -r` is still guarded.

- **Verify the install works with a read-only plugin directory** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: assumption: a hardened or read-only install directory (this host runs a hardened kernel) can't write `__pycache__`, so every hook pays a full compile. `bench_hooks.py` exists, but no read-only arm.
  Done when: `bench_hooks.py --readonly-dir` runs and `fm doctor` warns when hook p95 with an unwritable bytecode cache exceeds the cached p95 by more than a stated margin.

- **Emit a devcontainer or rootless-podman profile from the sandbox profile** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: bubblewrap/Landlock isolation is on the list, but the same boundary can't be reused by an IDE, CI or a remote host. A generated `devcontainer.json` would carry the guard's mounts and egress rules to any surface.
  Done when: `fm sandbox export devcontainer` writes a file, and a smoke test runs a blocked-path write inside the container and sees it denied.

- **Mint a one-use scoped push credential per `fm ship` grant** — SECURITY — value 4 — effort M — risk med — category: privacy — wild
  Why: the standing rule says each push uses a grant "spent on use", but today that is a ledger flag. A short-lived fine-grained token or per-push deploy key would make the grant physical, so a second push fails at GitHub, not in Foreman.
  Done when: a second `git push` after a shipped grant is rejected by the remote, and the token's expiry shows in `fm grants`.

- **Take a btrfs/snapper/ZFS snapshot at bypass start and offer one-command rollback** — FEATURE — value 4 — effort M — risk low — category: safety — wild
  Why: the pack lists overlay, trash and snapshot ideas, but not borrowing the host's own snapshot tool (snapper, btrfs, ZFS, restic). Assumption: the user's Arch machine may have one.
  Done when: starting a bypass session on a snapshot-capable host records a snapshot id, and `fm undo-session` prints the exact restore command, verified in a loopback btrfs test.

- **Require a FIDO2 key touch for the irreversible command class** — SECURITY — value 3 — effort M — risk med — category: devices — wild
  Why: "cooling-off period" and "scoped one-shot allow" exist, but both are software only. A hardware touch (`ssh-sk`/`pam_u2f`) is something a prompt-injected agent cannot satisfy, even in bypass mode.
  Done when: with the setting on, a force-push in bypass mode blocks until a key touch, and with the setting off, behaviour is unchanged.

- **Lint hook-path modules for heavy top-level imports** — PERFORMANCE — value 2 — effort S — risk low — category: performance
  Why: "Budget each verb's cold-start time and import cost" measures the problem. A static check in `fm check` would stop a new top-level `import` of a heavy module in `plugin/lib` hook paths before it lands.
  Done when: adding `import json5` at the top of a hook-path file fails the lint, and the same import inside a function passes.

Next question: Which guard bypass classes would a stranger find in under an hour, and which of them would the current exam never have predicted?
Next question: Which credential or secret can a Foreman-spawned process reach today that the user would be surprised it can read?
