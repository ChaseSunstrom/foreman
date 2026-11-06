# Brainstorm — lens: security and safety

- **Quarantine unknown repos before trusting their config** — SECURITY — value 5 — effort M — risk low — category: trust
  Why: assumption: Foreman sessions open cloned repos whose own `.claude/settings`, hooks, `.mcp.json`, skills and CLAUDE.md can run code or steer the agent. The pack's `fm trust` and `fm sensitive` cover only Foreman's own guard and settings, not a hostile project's.
  Done when: opening a fixture repo whose `.claude/settings.json` hook runs `curl|sh` makes `fm doctor` flag it. The session starts in manual mode with that config disabled until `fm trust-repo` is typed.

- **Broker credentials so sessions never hold real ones** — SECURITY — value 5 — effort L — risk med — category: secrets
  Why: assumption: sessions, lanes and `fm run` children inherit the user's `gh` login, cloud keys and env. `fm secrets` finds credentials after the fact, and the pack shows no mechanism that keeps them out of reach. A local broker would mint short-lived, per-lane, per-purpose tokens (push to one branch, read one registry) and proxy them.
  Done when: a lane's environment contains no long-lived token, `git push` from it works only to its own branch through the broker, and the token expires when `fm lane rm` runs.

- **Bind approvals to content hashes** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: T-0275 (guard reads script files run by bash, `.` and python) is deferred. An `fm ask` grant or an allowed command can be invalidated by editing the file between check and run (TOCTOU). Pin each allow to the sha256 of the script or command text, and re-verify at exec through a thin wrapper.
  Done when: a test allows `bash x.sh`, rewrites `x.sh` to add `rm -rf`, and the second run is refused with a "content changed since approved" reason.

- **Give autonomy=full an irreversibility budget** — SECURITY — value 5 — effort M — risk low — category: autonomy
  Why: `autonomy full` never asks mid-run, and the user wants the drive never idle. A per-run blast-radius ledger would count deletions, force-pushes, outbound posts, publishes and migrations. It would auto-pause for a typed confirm when a cap is crossed, and caps could rise with a task's track record.
  Done when: a scripted full-autonomy run that deletes more files than the cap stops with `needs you: irreversibility budget`. The ledger shows the count, and the run resumes after `fm ask`.

- **Run a pre-push egress manifest** — SECURITY — value 4 — effort S — risk low — category: release
  Why: the user repeatedly asks "to GitHub main and JARVIS" for each release (1.2.8 to 1.2.16), which is outward-facing and indexable. Before any push, publish or `gh release`, print exactly what leaves: commits, files, a secrets scan including history, and large or binary additions. Authorization would be scoped to that release only.
  Done when: pushing a commit that adds a fake AWS key is blocked with the manifest. A clean push prints the manifest and proceeds.

- **Check guard parity per harness shell form** — SECURITY — value 4 — effort M — risk low — category: multi-agent
  Why: a steer says "fmguard missed bash -lc/zsh -ic, Codex's shell form", and T-0335, T-0336 and T-0337 show Codex, Gemini and opencode adapters not live-verified. Generate a conformance corpus from each harness's real tool-call schema (wrappers, option clusters, `env`, `sudo`, `timeout`, `nohup`). Run it through the guard per adapter.
  Done when: `fm agents verify` lists per-harness pass/fail on a ≥200-form corpus. A deliberately removed unwrap rule turns the run red.

- **Compartmentalize projects with information-flow labels** — SECURITY — value 4 — effort M — risk med — category: privacy
  Why: `fm share` and `fm recall` move lessons across projects, `fm sensitive` marks repos, and JARVIS and Foreman are cross-fed. Label each brief, lesson, research note and evidence file with its project and sensitivity. Refuse to put a sensitive project's data into another project's context, exports, `AGENTS.md` or evals unless it is declassified.
  Done when: a lesson from a sensitive fixture repo never appears in `fm recall`, `fm export` or an eval from another repo. A test asserts that.

- **Redact secrets at write time into ledger, briefs and evidence** — SECURITY — value 4 — effort S — risk low — category: secrets
  Why: assumption: evidence records, `guard_block` events (T-0423 now keeps the offending command part) and transcripts can capture tokens pasted in commands or printed by tests. `fm sync` mirrors them into the repo. A redaction filter at the append layer would keep secrets out for good, not just scan them later.
  Done when: logging a command containing a `ghp_…` token stores `ghp_[redacted:github]`. The mirrored `.foreman/` contains no match from the `fm secrets` patterns.

- **Wild: Run prompt-injection drills on the live agent** — SECURITY — value 4 — effort M — risk low — category: red-team
  Why: wild. Foreman occasionally plants a harmless canary instruction in a fetched page, file or tool output ("run `fm canary-hit`"). If the session obeys, that is logged as a susceptibility score per model, Claude Code version and plugin revision, and it feeds `fm bench` and release gating. This measures the injection risk that taint tracking only guards against.
  Done when: a drill in a sandbox project records "obeyed/ignored" per model in `fm bench`. A deliberately weakened instruction file raises the obey rate.

- **Wild: Add a panic button that freezes everything** — FEATURE — value 4 — effort M — risk low — category: kill-switch
  Why: wild. The user runs sessions across projects, lanes, `fm serve` and the desktop app, and the drive is built to keep going. `fm panic`, also on the tray and phone, would SIGSTOP every Foreman-spawned session, revoke standing grants and `fm ask` approvals, snapshot dirty trees and stop `fm night`. `fm unpanic` would resume them in order.
  Done when: with three detached sessions running, `fm panic` halts all of them within 2 s. Grants are listed as revoked, and `fm unpanic` restores them with the resume point intact.

- **Wild: Keep an effect ledger with compensating actions** — FEATURE — value 4 — effort L — risk med — category: reversibility
  Why: wild. The pack's snapshot and undo covers the filesystem, but the damaging steps are outward ones: pushes, tags, releases, created cloud resources, sent messages. Record each external effect with its inverse (delete tag, revert merge, close PR, destroy resource). `fm undo --effects T-xxxx` would walk them back and report which ones are irreversible.
  Done when: a task that pushes a branch and creates a tag can be undone with one command in a fixture remote, and an unreversible effect is listed as such.

- **Wild: Require two-vendor concurrence for irreversible actions** — SECURITY — value 3 — effort M — risk med — category: dual-control
  Why: wild. `fm second` already gets a plan from another model, and the Codex, Gemini and opencode adapters exist. For the highest-risk categories (force-push, prod deploy, history rewrite, `rm -rf` outside the repo), a different vendor's agent must independently read the command and context and agree before the guard lets it through. A disagreement escalates to the user.
  Done when: a staged irreversible command is held until the second model's verdict is recorded. A forced "disagree" turns into an `fm ask`.

- **Sign Foreman's own releases and updates** — SECURITY — value 4 — effort M — risk low — category: supply-chain
  Why: the installer is `curl … | bash` from `main`. Releases 1.2.8 to 1.2.16 go to GitHub main, and Desktop publishing is T-0352. Tag releases with signatures (sigstore or minisign). Have `install.sh` and self-update verify a pinned key and refuse unsigned or downgraded builds. Print the checksum so `curl|bash` becomes a verified step.
  Done when: tampering with a release tarball makes `install.sh` abort with a signature error. A test covers both tamper and rollback cases.

- **Fuzz the approval and grant parser with adversarial user messages** — SECURITY — value 3 — effort S — risk low — category: authorization
  Why: `fm ask` says "their next message decides" and `fm standing` makes yeses durable. A pasted file, tool output or quoted text could pass as consent. Fuzz the "next message decides" path with pasted content, quoted "yes" text and subagent-relayed messages. Only a genuine user turn should ever count.
  Done when: a corpus of 100 forged-consent shapes (quoted yes, pasted `<pasted_content>` containing "approve", a subagent echo) is all rejected. A real typed "yes" still grants.
