# Brainstorm — lens: security and safety

- **Make Foreman's state and grants unwritable from inside a run** — SECURITY — value 5 — effort M — risk med — category: control plane
  Why: assumption: workers run as the same OS user as Foreman, so a hostile skill or injected worker could run `fm task set ID --allow publish`. Env-var caller tags can be spoofed. The pack plans "human-only verbs" and a bwrap cage but not how they are enforced. The user wants full auto and no prompts, so enforcement has to be structural: mount `$FOREMAN_HOME` read-only in the cage, and have mutating verbs check process ancestry (not descended from a run's process group).
  Done when: a test worker spawned by `fm code` that runs `fm task set T --allow publish` or writes to `grants` fails, while the same command from the user's shell succeeds.

- **Attest each child's capabilities from its own init event** — SECURITY — value 4 — effort S — risk low — category: runner trust
  Why: the pack claims claude sessions run "lean, only Foreman's guard" and brainstorm children are "tool-less". Stream-json emits an init event listing tools, MCP servers and plugins, but nothing checks it. A settings-merge change or an upstream default shift would silently void the claim.
  Done when: a fake runner whose init event lists an unexpected tool or MCP server is killed within one event, and a `stalled`-style event names the offending entry.

- **Harden the model-endpoint client** — SECURITY — value 4 — effort S — risk low — category: network
  Why: `models.json` takes any OpenAI-compatible or Anthropic endpoint, and upstream sync also fetches over HTTP. Nothing in the pack covers redirects forwarding `Authorization` cross-host, link-local or metadata addresses (169.254.169.254), or DNS rebinding into LAN. Proposal: one shared client that refuses cross-origin redirects, scopes each key to its host, denies link-local and metadata IPs unless named explicitly, and tags each endpoint loopback, LAN or cloud.
  Done when: a stub server that 302s to a second host never receives the key, and an endpoint resolving to 169.254.169.254 is refused with a named reason.

- **Pin model identity (digest) to grades and privilege** — SECURITY — value 3 — effort S — risk low — category: model trust
  Why: `fm code bench` grades by model name, and "routing by record" is planned. A local Ollama or llama.cpp tag can be silently re-pulled to different weights and keep its old grade. Key bench grades and the privilege tier to (endpoint, name, digest, quant) where the server exposes one.
  Done when: changing a stub server's reported digest drops that model to the ungraded tier and `fm code runners` shows "re-grade needed".

- **Enforce a tighten-only config lattice** — SECURITY — value 4 — effort M — risk med — category: config trust
  Why: planned per-project `.foreman/code.toml`, committed gate packs, runner manifests, stack cards and brief frontmatter all arrive via git. A hostile PR could ship `allow: publish` in a brief or a looser guard overlay. Rule: layers are ordered by trust (managed > user > project > brief). From the project layer and below, only keys that add deny rules, gates or caps are honoured. Loosening keys (allow, grants, runner paths, sandbox off, timeouts raised) are ignored with a printed note.
  Done when: a committed brief with `allow: publish` and a project `code.toml` with a looser cap leave the effective config unchanged, and `fm code config explain` lists both as ignored.

- **Require a differential soundness oracle for every fast path** — SECURITY — value 4 — effort M — risk low — category: guard integrity
  Why: the pack's performance ideas (verdict caching by command shape, a read-only prefilter, a shell fast-path, a resident hook daemon, gate caching by tree hash) each create a bypass risk if the shortcut disagrees with the full guard. Add a CI rule: a shortcut may only return the same verdict as the slow path or a stricter one on the full corpus plus mutations. Any case where it is more permissive fails the build.
  Done when: seeding a deliberately unsound prefilter (treats `git -c core.pager=... log` as read-only) turns CI red naming the command.

- **Watch every runner's control surfaces, not just git** — SECURITY — value 4 — effort M — risk med — category: worker containment
  Why: "Git config/hooks restored" exists for git only. Workers could instead write `.claude/settings.json`, `.mcp.json`, `AGENTS.md`, `.codex/config.toml`, `.gemini/`, `.cursor/rules`, `.vscode/tasks.json` or `.envrc`, which later sessions or the editor execute. Make each runner manifest declare its control files (the registry is the planned 8-line manifest). The harness snapshots them before a step, then treats a changed one as a judged change that is restored and reported unless the task names it.
  Done when: a fake worker that edits `.codex/config.toml` has the edit reverted and a "control file touched" line in the run summary.

- **Keep secrets off argv** — SECURITY — value 3 — effort S — risk low — category: credentials
  Why: CLI runner templates and `models.json` could place API keys in command lines, visible in `/proc/*/cmdline`, `ps` and wrapper logs. The pack has keyring and by-reference ideas but not argv. Spawn through the single launcher, pass keys by env on the child only, and abort if any argv element matches a key shape.
  Done when: a runner template containing `--api-key sk-...` fails to spawn with a message naming the env alternative.

- **Treat a marketplace rename or source change as a new install** — SECURITY — value 3 — effort S — risk low — category: supply chain
  Why: the pack plans "follow marketplace renames and yanks" over `marketplace.json` (about 166 plugins, half third-party, pinned by sha). A rename or a git-subdir change could repoint an already-trusted name to different code. Re-keying trust to (name, source, sha) and re-running quarantine and capability-delta on any change closes this. Add a lookalike-name check against the existing catalog.
  Done when: a fixture catalog that renames `foo` to a new source leaves `foo` untrusted and unrouted until re-adopted, and `fo0` is flagged as a lookalike.

- **Mint a run-scoped, spend-capped API key (wild)** — SECURITY — value 4 — effort M — risk med — category: credentials
  Why: assumption: providers with key-management APIs allow creating a limited key. A leaked or exfiltrated worker key would then die at run end and cost at most the run's cap. Fall back to the broker where unsupported. Opt-in per provider.
  Done when: against a stub key-management API, a run creates a key with the cap, uses it, revokes it on every exit path (including kill), and `fm code why` shows the revocation.

- **Give each model a gullibility score from a planted-injection exam (wild)** — SECURITY — value 4 — effort M — risk low — category: model trust
  Why: bench grades correctness but not obedience to hostile text. Run fixtures where SKILL.md, README and a tool result carry instructions that contradict the request. The score (obeyed / quoted-and-ignored / flagged) becomes a ceiling on privilege (read-only plan, no unattended mode). It is re-run on digest change.
  Done when: a stub model that obeys planted text scores 0 and cannot be selected for `--unattended` runs.

- **Share only hashes of rejected assets, as an opt-in immune feed (wild)** — SECURITY — value 3 — effort M — risk med — category: supply chain
  Why: quarantine and the poison-asset corpus catch bad skills locally, but each install relearns them. A deny-only list of SHA-256s (no content, no paths) can be fetched signed and merged tighten-only. Local rejections are exported only with an explicit setting. Assumption: some distribution channel exists.
  Done when: a hash in the local feed blocks adoption of the matching fixture skill offline, and exporting is off until enabled.

- **Mark every run's outer edge with a canary the worker can't see (wild)** — SECURITY — value 3 — effort M — risk low — category: containment
  Why: the pack has honeytokens and sandboxing but no end-to-end proof that the cage actually holds in the user's real environment (hardened kernel, no user namespaces, and so on). At run start, plant a harmless sentinel file outside the cage and a loopback listener. A probe worker step tries to read, write and connect. A leak downgrades the runner to plan-only and says why.
  Done when: on a host where the cage is deliberately disabled, the probe detects the sentinel read and `fm code` refuses worker steps with a named reason.
