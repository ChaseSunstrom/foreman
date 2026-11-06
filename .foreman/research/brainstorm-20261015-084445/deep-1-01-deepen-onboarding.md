# Brainstorm — lens: deepen: onboarding

- **Make one resumable `fm start` ladder that owns the whole first hour** — FEATURE — value 5 — effort M — risk low — category: onboarding
  Why: the pack lists ~10 separate onboarding verbs (hello, demo, tour, learn, preview, examples, cheat card); newcomers hit 231-line `fm --help` and jargon (evidence A4, A11). One stateful ladder (install → PATH → doctor → demo → first real task → first finish) stores its rung in state, survives `/compact` and new sessions, and each rung's last line names the next command. The other verbs become rungs, not top-level choices.
  Done when: in a clean HOME, `fm start` run five times in a row advances through each rung exactly once, and killing the session mid-rung and rerunning resumes at the same rung.

- **Install as a plain marketplace plugin first, with "full Foreman" as an opt-in upgrade** — FEATURE — value 5 — effort M — risk med — category: distribution
  Why: every rival installs via `/plugin install …` and doesn't rewrite `~/.claude` (B); Foreman's default sets bypassPermissions, outputStyle, autocompact and 20 deny rules (A2). Tier 0 = commands, skills and hooks only, with no settings changes. `fm start` offers each setting change one at a time, with a stated reason, and records consent.
  Done when: a clean-HOME install through the plugin path leaves `settings.json` byte-identical, and `fm start` can apply and revert each wiring item separately.

- **Ship a trust ledger: show every change install made, with a one-line undo each** — SECURITY — value 4 — effort S — risk low — category: trust
  Why: "bypass by default is a large trust ask" and uninstall leaves residue and prints "defaultMode = None" (A2, A10). `fm wiring` lists each touched key/file, why, and the revert command. Uninstall uses the same ledger, so removal is complete by construction.
  Done when: after install then uninstall in a clean HOME, a recursive diff against the pre-install snapshot is empty, and `fm wiring` lists every key install changed.

- **Replace `fm doctor`'s fresh-install failure with a first-run checklist that self-heals** — FIX — value 4 — effort S — risk low — category: onboarding
  Why: a fresh install fails its own doctor on a missing backup and prints 40 lines of passes (A8). Show only non-passing lines, split into "not set up yet" (with a one-key fix) and "broken". Install creates the first backup.
  Done when: `fm doctor` right after a clean install exits 0 with ≤5 lines, and a deliberately broken hook shows up as "broken" with a fix command.

- **Let `fm task done` refuse with one prefilled, copy-ready `fm task finish` line** — FIX — value 4 — effort S — risk low — category: friction
  Why: the 4-bullet refusal hides the one-call shortcut (A9). The refusal computes what's missing (evidence, summary) and prints the complete command with the observed test command filled in.
  Done when: running `fm task done` on a task with unrecorded evidence prints a single `fm task finish …` line that, when pasted, succeeds.

- **Make `fm task new` and `fm capture` one forgiving path with real help** — FIX — value 4 — effort S — risk low — category: friction
  Why: `task new` after `capture` makes a duplicate, and `--help` lists no valid `--type`/`--tier` values or examples (A6). Match near-duplicate captures (offer to promote), list enums, and show 3 real examples from the gallery. Typos suggest the closest value.
  Done when: capturing "fix login timeout" then `fm task new "fix the login timeout"` offers to promote the capture, and `fm task new --help` lists every valid type and tier.

- **Detect the test runner at first `fm check` and write the gate with the user's yes** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: no gates configured means no detection (A7), while the usage data shows test-runner calls dominate (C). Detect from files (pytest.ini, pyproject, package.json, Cargo.toml, go.mod) and from the command history. Whole-suite commands only, which also fixes `fm repeats` suggesting single test modules (C).
  Done when: in a fixture repo with pytest, `fm check` proposes `pytest` as the gate, accepting it persists it, and `fm repeats` never suggests a single-module gate.

- **Produce a public, reproducible "with vs. without Foreman" proof from `fm demo`** — FEATURE — value 5 — effort L — risk med — category: credibility
  Why: the bench has 1 case and 0/3 court cases, so there's no evidence Foreman helps (C). Build `fm demo` on a seeded-bug fixture kit and replay recorded transcripts with no model calls. Add a live mode that runs N real trials both ways, publishing pass rate, tokens and wall time in the README as a table (README opens abstractly, A1).
  Done when: README's first screen has a measured table, and `fm demo --replay` reproduces the same outcome offline in under 60 seconds.

- **Hide the 108-verb surface behind progressive disclosure (`fm help` tiers)** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: `--help` is 231 lines with ticket numbers (A4), 46 verbs were never run by Claude in 11 days (C), and the audit says merge to ~70 (D). Show 8 core verbs by default, with `fm help --all` and `fm help <topic>`. Unlock the next group once the user's usage shows a need. Nothing is deleted, per D's caution.
  Done when: `fm --help` fits in 25 lines with no ticket IDs, `fm help --all` still lists every verb, and a test fails if a verb is undocumented.

- **Wild: Turn the tutorial into a git repo whose history is the lesson, graded by Foreman itself** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: wild. Each commit is a lesson, such as a failing test or a dangerous command the guard blocks. `fm learn` checks out the next commit, and the user's fix is verified through the same evidence flow they will use for real work. Completion closes the tutorial with a real receipt.
  Done when: running `fm learn` through all steps in a clean HOME ends with a recorded passing task and a certificate line in `fm digest`.

- **Wild: Make a stranger test the CI gate: a scripted persona runs the install and first task, and the build fails if friction grows** — FEATURE — value 4 — effort M — risk low — category: quality
  Why: wild. Section A is a one-off audit that will rot. A CI job installs into a clean HOME and runs the `fm start` path with no model calls. It counts commands, output lines, "command not found" hits, and time-to-first-finish, then ratchets each against a committed budget.
  Done when: CI fails if a change adds a "command not found", pushes `fm --help` over its line budget, or doubles time-to-first-finish.

- **Wild: Install by telling Claude "install Foreman", via an agent-readable INSTALL.md that asks consent per step** — FEATURE — value 3 — effort S — risk med — category: distribution
  Why: wild. Rivals use a single command (B), but Claude Code is already open on the user's machine. The agent reads INSTALL.md, explains each wiring item in plain words, asks, applies it, and ends in `fm start`. It composes with the trust ledger, so consent is recorded per item.
  Done when: giving a fresh Claude session only the repo URL results in a working install, and the ledger shows each change with its consent.

- **Preview on the user's own history: `fm preview` replays past sessions to show what Foreman would have caught** — FEATURE — value 4 — effort M — risk low — category: credibility
  Why: abstract promises don't convince, but the user's own repo does (A1, C). Read-only, local, and fully on the owner's machine, it scans recent transcripts for repeated test runs, dangerous commands the guard would have blocked, lost context after compaction, and unverified "done" claims. It ends with a count and a single `fm start` suggestion.
  Done when: on a machine with ≥5 past sessions, `fm preview` prints at least one concrete, line-cited finding without writing outside Foreman's state dir or making network calls.

- **Put `fm` on the shell PATH through a shim that never shadows another `fm`** — FIX — value 4 — effort S — risk low — category: onboarding
  Why: `fm` exists only inside Claude sessions, so README commands say "command not found" in a shell (A3). Install a shim in `~/.local/bin` only if no other `fm` resolves, otherwise offer an alias, and record it in the trust ledger so uninstall removes it.
  Done when: in a fresh shell after install, `command -v fm` resolves to Foreman; with a pre-existing `fm` on PATH, the installer leaves it alone and reports it.
