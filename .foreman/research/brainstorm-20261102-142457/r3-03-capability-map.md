# Brainstorm — lens: capability map

Capability map for #12, "Staying lean and safe". The comparison set is Lynis, OpenSSF Scorecard, Falco, bubblewrap and `systemd-analyze security`. The ideas below are what a best-in-class version would add, and none of them repeats the slate.

- **Run every Foreman-initiated git call with a hardened config on untrusted repos** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: assumption: Foreman shells out to `git` in checkouts it didn't write (`fm map`, `fm ship`, lanes, `fm tick`). The pack covers marking a checkout untrusted but not the git-config attack surface itself.
  Done when: a fixture repo whose `.git/config` sets `core.fsmonitor`, `core.hooksPath` and a textconv driver to a canary script runs `fm map` and `fm status` without the canary executing.

- **Pin ambient infrastructure context and block on mismatch** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: assumption: the guard judges command shapes, not where they point. Today's `kubectl delete`, `terraform apply` or `psql -c "DROP"` is safe or fatal depending on `current-context`, `AWS_PROFILE`, workspace or DSN host. Context pinning is not among the listed ideas.
  Done when: with a fake kube context named `prod`, a `kubectl delete` is blocked with a `Next:` line naming the pin command, and the same command passes under the pinned `dev` context.

- **Make privileged fm verbs refuse lane and child callers** — SECURITY — value 4 — effort M — risk med — category: agents
  Why: the pack's grants for `fm ship` and `fm ask`, and the sealed gen-0, assume the agent is not the caller. A lane with Bash can invoke `fm ship`, `fm decide`, or a steer store directly. Existing ideas tag verb use by caller for the census only, not enforcement.
  Done when: a child process spawned by `fm lane` that runs `fm ship` or `fm steer add` exits nonzero naming the verb as human-only, and the same verb from the user's TTY works.

- **Cap spawn depth and debit child spend from the parent's budget** — SECURITY — value 3 — effort S — risk low — category: agents
  Why: budgets are per task and per account; nothing hierarchical is listed. A recursion or fan-out loop (brainstorm, audit, lanes) can burn the account while each child stays under its own cap.
  Done when: a stub agent that tries to spawn a third level is refused, and the parent's receipt shows children's spend summed against its cap.

- **Scan instruction files, skills, steers and pasted asks for hidden Unicode** — SECURITY — value 3 — effort S — risk low — category: injection
  Why: the pack covers injection and the "lint agent instruction files for drift", but invisible tag characters, bidi controls and zero-width characters (Trojan-Source style) aren't named. They survive git review and cold reads.
  Done when: a planted `CLAUDE.md` and a skill file containing U+202E and tag characters each yield a red `fm doctor` row that quotes the codepoints and offsets.

- **Census listeners, tunnels and background services after bypass sessions** — SECURITY — value 3 — effort S — risk low — category: footprint
  Why: the pack has a persistence census and orphan reaping, but no check for sockets left bound to `0.0.0.0` or for `ssh -R`, ngrok or cloudflared tunnels that expose the dev box.
  Done when: a session that leaves `python -m http.server` on `0.0.0.0` and a stub tunnel process gets a close-time warning naming the port and pid, and a loopback-only server doesn't.

- **Ship a safe extractor for every archive Foreman fetches** — SECURITY — value 3 — effort S — risk low — category: supply chain
  Why: the environment note says downloaded archives are untrusted, and Foreman imports packs, cards and rival formats. The pack has "type grafts" but no extraction hardening.
  Done when: fixture archives with `../` paths, absolute symlinks, setuid bits and a 1000:1 compression ratio are each rejected with a named reason, and a clean archive extracts into an empty directory.

- **Guard the browser behind `fm shot` and `fm flow` against SSRF and file reads** — SECURITY — value 3 — effort S — risk low — category: proof tools
  Why: the pack gates the browser sandbox but not where the browser may navigate. A flow can reach `169.254.169.254`, `file://`, or a hostname that rebinds to a private range.
  Done when: a flow targeting the metadata IP, `file:///etc/passwd` or a rebinding fixture aborts with a "blocked navigation" line, and `localhost:<app-port>` still works.

- **Run lanes under a `systemd-run --user` sandbox and print its exposure score** — FEATURE — value 4 — effort M — risk med — category: sandbox
  Why: the pack lists bwrap, Landlock and a learned profile, but not the systemd route. `ProtectHome`, `PrivateTmp`, `IPAddressDeny` and `SystemCallFilter` are already on the host, and `systemd-analyze security` gives a ready-made number. Assumption: the host runs systemd, as the Arch-based environment suggests.
  Done when: a lane started with `--sandbox systemd` can't read a canary in `$HOME` outside its bind-mounted repo, and `fm doctor` prints the unit's exposure score.

- **Add pause, resume and shrink-budget controls per lane in the pane** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: the pane has an Agents graph, and the pack has HALT and freeze, but only all-or-nothing. The thin categories are ui and agents.
  Done when: selecting a lane in the pane and pressing `p` SIGSTOPs its process tree, the graph node shows paused, and `r` resumes it.

- **Show an annotated approval card for guard blocks and `fm ask` grants** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: the pack covers rubber-stamping and safe alternatives, but not explaining the command. An explainshell-style card would highlight the risky token and show the resolved path, flag meanings and blast size.
  Done when: blocking `rm -rf ./build /` renders a card that highlights the stray `/` and shows the safe variant, in both the terminal and the web UI.

- **Wild: Mine installed binaries' man pages for destructive flags and diff them against guard coverage** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: wild. The GTFOBins import covers known abuse; this covers the user's own tools, such as `--force`, `--purge`, `--delete`, `--yes`, `--no-preserve-root`, ranked by how often the user runs each binary.
  Done when: `fm guard coverage` lists the top 20 installed binaries with destructive flags that have no rule or exam item, each with a sample command.

- **Wild: Release secrets only while the human is present, and give unattended lanes decoys** — SECURITY — value 3 — effort M — risk med — category: secrets
  Why: wild. The pack has a keyring, canaries and presence-aware cooling-off. Gating credential release on recent keyboard activity or an unlocked screen would make overnight lanes structurally unable to use real keys.
  Done when: with the screen locked, `fm with-secret` hands a lane a canary value and records "decoy served"; unlocked, it hands the real one.

- **Wild: Tie the ledger signing key to the machine with TPM or `systemd-creds`** — SECURITY — value 2 — effort M — risk med — category: integrity
  Why: wild. Signing keys the agent can't read are listed, but a key that stays on the box lets a copied state dir prove authentic history yet never forge new records on another host. Assumption: a TPM or `systemd-creds` is available.
  Done when: a state dir copied to a scratch host verifies as "history intact, cannot sign" and refuses to append new signed lines.

Next question: Which fm verbs does a lane's Bash tool reach today that a human-only verb list would block, and what breaks if that list is enforced?
Next question: What fraction of the guard's rules key on the command shape alone, versus on the target (host, context, path), and which real incidents hinged on the target?
