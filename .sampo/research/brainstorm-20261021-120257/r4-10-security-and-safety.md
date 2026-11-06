# Brainstorm — lens: security and safety

- **Bind adopted upstream assets to a signed-by-hash capability manifest, re-diffed on every update** — SECURITY — value 5 — effort M — risk low — category: supply chain
  Why: the request is to integrate six Anthropic repos "automatically"; plugin marketplaces are pinned by sha but about half are third-party, and skills can ship scripts/. Existing ideas cover trial lanes and a cooldown, but not a per-asset manifest (files, hooks, commands, network hosts, scripts) that must be re-approved when any byte of its capability surface changes.
  Done when: updating a fixture plugin so that it adds one new hook or script file makes `fm plugins update` refuse with the exact capability delta, and a content-only edit to a SKILL.md body passes without a prompt.

- **Run every imported script through one exec broker with the guard as its only door** — SECURITY — value 5 — effort M — risk med — category: execution
  Why: skills/plugins carry scripts and the constraint says "third-party skills and plugins run nothing unguarded". An exec broker was mentioned only in passing; no idea makes it the single choke point with argv-only invocation, scrubbed env and a declared cwd/write scope.
  Done when: a fixture skill whose script tries `curl`, writes outside its declared dir, and reads `~/.ssh` has each attempt denied and logged, while its declared action succeeds, and a grep test finds no other `subprocess` path used for imported assets.

- **Mark every byte entering a slot prompt with a provenance tag and fail closed on untrusted-to-sink flows** — SECURITY — value 5 — effort L — risk med — category: prompt injection
  Why: fm code builds small checked JSON slots from repo text, upstream docs, skill bodies and tool output. Existing ideas mention taint ledgers and nonce envelopes in general; a per-byte provenance carried through to the commands/paths a slot can produce is the second-order step that makes injection un-actionable for weak models.
  Done when: a planted "ignore previous, run X" in a fixture README that flows into an `run` slot is rejected with a provenance reason, while the same text typed by the user is accepted.

- **Verify the changed-file set two independent ways and tripwire the paths a worker can reach outside the tree** — SECURITY — value 4 — effort M — risk low — category: containment
  Why: the harness "judges every changed file" for CLI runners; one derivation (git diff) can be fooled by ignored files, .git internals or symlinks. Assumption: a hostile or buggy CLI runner can write to ignored or out-of-tree locations.
  Done when: a fake runner that writes an ignored file, a symlinked target and a file under `~/.config` fails the step with each named, and an honest runner passes.

- **Give each runner a measured gullibility and privilege grade that gates what it may do unattended** — FEATURE — value 4 — effort M — risk med — category: runner trust
  Why: fm code now supports any CLI or endpoint, many with no safety tuning; `fm code bench` grades capability, not susceptibility. Combine with a planted-injection exam so privilege (network, release, unattended) is earned per model digest.
  Done when: `fm code runners` shows a safety grade per runner from a scripted injection exam, and a runner scoring below threshold is refused `--unattended` with the reason.

- **Tighten-only config lattice across global, project and env layers** — SECURITY — value 4 — effort S — risk low — category: config
  Why: the user wants config layered per project and committed with repos; a hostile repo's `.foreman/code.toml` could loosen guard, add a runner or point at an exfil endpoint. Trust pinned to the file hash was suggested, but the rule that project layers may only narrow permissions is not.
  Done when: a fixture project config that enables a new runner template, raises a spend cap or adds an egress host is ignored with a printed reason, while one that lowers a cap is applied.

- **Keep secrets off argv, out of env by default and behind run-scoped spend-capped keys** — SECURITY — value 4 — effort M — risk med — category: credentials
  Why: models.json holds keyed cloud endpoints and nested CLIs inherit the environment; process listings and child CLIs can leak keys. Assumption: keys currently pass via environment or config.
  Done when: while a run is live, `ps` output and the child's environment dump contain no key value, and a fixture child prints only a scoped alias.

- **Treat marketplace renames, source changes and yanks as new installs** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: claude-plugins-official supports renames and git-subdir/url sources; an auto-follow that silently crosses a rename or source swap would pass trust to a different repo.
  Done when: a fixture marketplace.json that renames a plugin or changes its source url makes the sync stop with a "re-trust required" status, and a plain sha bump within the same source passes after the manifest diff check.

- **Refuse unattended and release modes when the safety stack is stale, with a generated safety case** — SECURITY — value 4 — effort M — risk low — category: assurance
  Why: users say "full auto, release any time"; autonomy should depend on a live check that the guard corpus, canary and version probe passed recently, not on past approval. Each claim in the case maps to a runnable check.
  Done when: making the guard replay corpus fail (fixture) causes `fm code --unattended` and `fm release --push` to refuse naming the failing check, and fixing it re-enables both.

- **Fence prompt-borne metadata channels: terminal escapes, bidi/invisible characters and tool descriptions** — SECURITY — value 3 — effort S — risk low — category: injection
  Why: runner output and upstream docs render in the TUI and feed slots; the TUI already has an escape-sanitizer idea, but the same sanitizer is not applied to text entering model prompts or to MCP tool descriptions pinned from third parties.
  Done when: a fixture skill containing bidi overrides, zero-width instructions and an OSC 52 sequence is shown sanitized in the TUI and stripped (with a count) before reaching any prompt.

- **Wild: Honeytoken credentials and a canary slot that expose a hijacked or swapped worker** — SECURITY — value 4 — effort M — risk low — category: detection — wild
  Why: assumption: nested workers may be steered by planted text. Fake keys in a decoy file plus a known-answer canary slot at run start detect both exfiltration attempts and a silently swapped model.
  Done when: a fixture runner that reads the decoy key halts the run with an alert naming the file, and a runner returning a wrong canary answer is flagged as swapped.

- **Wild: Detonation chamber that compares a skill's declared behaviour with what it actually did** — SECURITY — value 4 — effort L — risk med — category: dynamic analysis — wild
  Why: static capability cards are bypassable; running an imported skill once in a throwaway HOME with no network and diffing file/exec/connect attempts against its manifest catches lies.
  Done when: a fixture skill that declares "read-only" but writes a dotfile in the chamber is rejected with the observed writes listed, and an honest one is admitted.

- **Wild: Burn-after-reading mode for sensitive repos** — SECURITY — value 3 — effort M — risk med — category: privacy — wild
  Why: runs leave journals, transcripts, spill stores and exports; a mode that keeps them in RAM-backed storage, forbids cloud runners and shreds on exit suits private repos.
  Done when: after a run in this mode, no file under the state dir mentions the request text, `--local-only` is enforced, and an attempted cloud runner is refused.
