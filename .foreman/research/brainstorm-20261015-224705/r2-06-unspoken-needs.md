# Brainstorm — lens: unspoken needs

- **Let blocked tasks carry a probe that unblocks them** — FEATURE — value 4 — effort S — risk low — category: backlog
  Why: T-0325 (needs libappindicator), T-0418, T-0335/6/7 sit blocked on outside facts. The user's own "when PATH changes" deferral shows they think in triggers. Assumption: blocked tasks today need a human to notice the world changed.
  Done when: a task blocked with `--unblock-when '<cmd>'` flips to ready at the next SessionStart once the command exits 0, and the greeting says which one flipped and why.

- **Replay recorded claude sessions through a cassette shim** — CLEAN — value 4 — effort M — risk low — category: test isolation
  Why: tests reached the paid binary (T-0990 fallback), two tests fake "no claude" with PATH alone, and the harness session was driven by the Stop hook. Assumption: the drive, `fm ideas` and reviewer children can be exercised from recorded `claude -p` streams.
  Done when: a fake `claude` replays a recorded stream-json cassette, and the suite runs with zero real-binary calls. A `--record` mode writes new cassettes, and a test fails if any call misses a cassette.

- **Tell inherited red from new red at close** — FEATURE — value 4 — effort M — risk med — category: gates
  Why: the gate-failure items (tests that predate T-0972, PATH-faking tests) show builders chasing failures they didn't cause. Assumption: the lane's start tree can be snapshotted cheaply.
  Done when: a worktree records which tests were red at branch point. Closing with only those red prints "inherited red, not yours" and files a task for each, while a newly red test still blocks.

- **Mine the repo's unwritten house style into a verified card** — FEATURE — value 4 — effort M — risk low — category: cards
  Why: cards are chosen by language and imports, but nothing captures per-repo conventions such as naming, error handling, test shape or comment density. Assumption: the git history is rich enough to derive them.
  Done when: `fm style` writes ≤15 rules from a git sample, each with ≥90% conformance on held-out files, and the edit-time injector loads the card for that repo.

- **Forget on demand across every store** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: the ledger, lessons, fixes, research notes and git-carried hints all keep text, and the user is moving them through git. Assumption: no single verb removes a leaked secret or client name from all of them.
  Done when: `fm forget "<term>"` previews hits in every store, redacts or deletes them on confirm, lists the git commits that still hold the term, and a re-scan finds zero.

- **Run a compatibility farm against popular plugins** — FEATURE — value 3 — effort M — risk low — category: coexistence
  Why: the user wants Foreman to be "THE plugin", but real installs carry other plugins' hooks and skills. Assumption: no check yet shows double-firing or conflicting matchers.
  Done when: `fm doctor --farm` loads N plugin manifests beside Foreman's and reports overlapping hook matchers and skill triggers. A fixture pair with a known clash is flagged.

- **Add `--dry-run` to every mutating verb** — FEATURE — value 3 — effort M — risk low — category: safety
  Why: the user has been burned by side effects reaching real state (a real session, a paid binary). Assumption: mutating verbs are enumerable from the CLI table.
  Done when: every mutating `fm` verb prints "would write/run/send: …" and changes nothing under `--dry-run`, and a test enumerates the verbs and fails on a stray write.

- **Wild: Turn each Claude Code workaround into a ready-to-file upstream bug** — FEATURE — value 3 — effort M — risk low — category: community
  Why: shims keep appearing for CC quirks (the folder-trust prompt, claude missing from PATH, Stop-hook re-entry), and each one is a bug report nobody wrote. Assumption: the user would file reports if the minimal repro and the text were handed to them.
  Done when: `fm upstream <shim>` emits a standalone script under 50 lines with no Foreman imports, plus a redacted issue body. Nothing is sent without an explicit yes.

- **Wild: Hold a prototype tournament for brainstorm ideas** — FEATURE — value 4 — effort L — risk med — category: prioritisation
  Why: the user called the last catalogue "very simple", and 600+ ideas are ranked only by prose and guessed S/M/L. Assumption: a throwaway Haiku build in a worktree can approximate real effort and test impact.
  Done when: the top 3 ideas each get a discarded worktree prototype, and the digest shows diff size, tests touched and pass/fail beside the guessed effort, with the worktrees removed afterward.

- **Wild: Give every magic number an owner metric** — CLEAN — value 3 — effort M — risk low — category: self-tuning
  Why: timeouts, caps and thresholds are scattered through `plugin/lib` (54 modules), and tuning has been by hand after complaints. Assumption: most can be named and tied to a ledger metric.
  Done when: a constants registry lists each tunable with its rationale and metric. A nightly `fm tune` reports the ones whose measured p95 sits more than 2x from the setting, and a test fails on an unregistered new constant.

- **Wild: Draft a standing-orders sheet from the user's steers and show it at greeting** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the user repeats "fill the dock", "no gaps" and "declutter" across rounds, and the need underneath is not having to say it twice. Assumption: steers can be clustered into a short list the user can approve.
  Done when: the first screen of a session shows ≤7 standing orders with last-upheld dates, and the user can strike one with a single command.

- **Ship JSON Schemas for every Foreman file** — FEATURE — value 2 — effort S — risk low — category: developer experience
  Why: repos can drop their own gates, cards and lenses, and a team will hand-edit `.foreman/` files. Assumption: formats are stable enough to schema.
  Done when: `fm schema` emits one schema per file type and a bad `.foreman/` file shows a squiggle in VS Code. A test validates the fixtures against the schemas.
