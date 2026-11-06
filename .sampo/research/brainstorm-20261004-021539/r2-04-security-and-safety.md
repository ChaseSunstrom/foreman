# Brainstorm — lens: security and safety

- **Quarantine instruction-bearing text from untrusted sources before it reaches lessons** — SECURITY — value 4 — effort M — risk med — category: memory poisoning
  Why: assumption: research notes and recalled lessons feed the always-on context, and the pack covers marking fetched text as untrusted but not what happens when that text is distilled into a lesson. A web page's injected "always run X" could persist across sessions.
  Done when: a lesson derived from a fetched page containing an imperative line is stored with a `source=web` taint and is not recalled as a rule until the user confirms it with `fm lesson trust ID`. A test injects such a page and asserts that recall output omits the rule.

- **Lock verify commands and test files once a brief is approved** — SECURITY — value 5 — effort M — risk med — category: evidence integrity
  Why: pass 2 found proof tools that could record a pass with nothing proven, and steered criteria edits happened mid-task. Nothing stops the model from weakening a criterion's verify command or editing the tests that gate it.
  Done when: editing a criterion's verify line or a file named by it after approval is recorded as a "goalpost move" event and shown in `fm pr` and the audit lens input. A test that weakens a verify mid-task shows the event.

- **Run child processes with a scrubbed environment** — SECURITY — value 4 — effort S — risk low — category: secrets
  Why: assumption: verify commands, gates and children inherit the full shell env, including API keys and cloud tokens. This is separate from the listed no-network jail and write-time scrubbing.
  Done when: a verify command that prints `env` shows only an allowlisted set (PATH, HOME, LANG, project vars). A test with a planted `FAKE_TOKEN` shows it absent from the output, and an opt-in `--env NAME` passes it through.

- **Firewall outbound research queries and fetch URLs** — SECURITY — value 4 — effort M — risk low — category: exfiltration
  Why: `fmresearch` sends model-composed queries and URLs to the web, and a query can carry repo code, secrets or internal hostnames. The pack's privacy checks cover exports, not live egress.
  Done when: a research query containing a planted secret pattern or an internal path is refused or redacted before the request, and the host and byte count of every request lands in an egress ledger. A test covers both.

- **Snapshot automatically before any user-approved destructive command** — SECURITY — value 4 — effort M — risk low — category: reversibility
  Why: the guard blocks risky shell with user-granted approvals, but an approved `git reset --hard` or `rm -rf` has no undo. The pack shows a crash already destroyed state with no recovery path.
  Done when: approving and running a destructive command first writes a dangling snapshot ref (`git stash create` plus untracked files), and `fm undo-grant` restores it. A test deletes a file under an approval and restores it.

- **Check newly added dependencies for slopsquatting** — SECURITY — value 4 — effort M — risk med — category: supply chain
  Why: assumption: the model can add hallucinated or typosquatted package names to manifests or install commands. The pack covers dependency release watching, not vetting a name at the moment it is added.
  Done when: a new manifest entry or `pip/npm install X` that isn't in the lockfile triggers a note with the name's near-miss against popular packages and whether the registry knows it. The registry lookup needs the user's yes. A test with `reqeusts` produces the note.

- **Add an injection drill set to `fm bench`** — SECURITY — value 4 — effort M — risk low — category: prompt injection
  Why: fetched pages, diffs and repo files all reach the reviewer and research children. Bench ablations measure quality but nothing measures obedience to planted instructions.
  Done when: bench cases with planted instructions in a page, a diff comment and a README run through research and review, and passing means no tool action or approval change and a flag raised. A seeded vulnerable prompt fails the case.

- **Preview the blast radius in every guard block** — SECURITY — value 3 — effort M — risk low — category: guard UX
  Why: blocks currently say what category was hit, not how much is at stake. Globs and `git clean` expand to unknown counts, which makes approvals blind.
  Done when: a blocked `rm -r build/*` or `git clean -fd` shows the expanded count and paths (via read-only dry-run forms) alongside the reason. A test asserts the count in the message.

- **Wild: Issue approvals as spend-down capability leases** — SECURITY — value 4 — effort M — risk med — category: permissions
  Why: assumption: grants are durable until re-verified. A lease holds N uses, a path scope and a TTL, and shows in the pane as remaining charge, so a "yes" given once cannot quietly become standing authority.
  Done when: a grant of 2 uses allows 2 matching commands and blocks the third with "lease spent", and the pane card shows the remaining uses. Wild.

- **Wild: Open untrusted repos in a read-only quarantine mode with a capability card** — SECURITY — value 4 — effort L — risk med — category: repo trust
  Why: a freshly cloned repo can carry `.claude/settings.json` hooks, MCP configs, skills and an AGENTS.md written to steer the agent. This extends the foreign-skill capability card to the whole repo.
  Done when: the first session in an unseen repo lists the hooks, MCP servers and instruction files it found, and edits stay blocked until `fm trust` is given. A fixture repo with a malicious hook shows the card. Wild.

- **Wild: Pause the drive on behavioural drift from a per-task-type baseline** — SECURITY — value 3 — effort L — risk med — category: autonomy safety
  Why: assumption: full-autonomy and drive modes can run unattended for long stretches. Spend, edits outside the brief's files, new network hosts or a burst of guard blocks are signals the guard's rules don't see in aggregate.
  Done when: a replayed drive log with a spend spike and off-brief edits trips a pause with the named signals, and a normal log doesn't. Wild.
