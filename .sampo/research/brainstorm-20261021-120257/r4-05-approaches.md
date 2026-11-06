# Brainstorm — lens: approaches

- **Reconcile a desired-state file with `fm plan` and `fm apply`** — FEATURE — value 4 — effort L — risk med — category: management
  Why: the user wants "full management" and "work with anything". Runners, adopted upstream assets, schedules, projects and defaults are set in separate places (models.json, code.toml, per-command flags). No pack idea gives one declarative whole-machine file with a diff before it changes anything, as Terraform or NixOS do.
  Done when: editing one line in `foreman.toml` (for example the default runner) makes `fm plan` print exactly that diff, and `fm apply` followed by `fm plan` prints "no changes".

- **Adopt upstream assets as merges on an orphan branch** — FEATURE — value 4 — effort M — risk low — category: integration
  Why: the pack covers lockfiles and pinning, but not what happens when a user edits an adopted skill locally. Each adoption becomes a commit with source, sha and licence trailers on a `foreman-upstream` worktree. Updates are `git merge`, so conflicts, revert and blame come from git for free. Assumption: git is present, which every Foreman project already needs.
  Done when: adopt, hand-edit, then update an asset whose upstream changed. The edit survives or a standard merge conflict appears, and `git revert` of the adopt commit removes the asset.

- **Mine feature gaps from tool-call sequences instead of docs** — FEATURE — value 4 — effort M — risk low — category: parity
  Why: the user's model is "the Claude Code repo as the map", but READMEs and changelogs lag behavior. Run about 10 canonical prompts through real `claude -p` stream-json and through `fm code`. Diff the tool names and sequences, then queue the gaps ranked by frequency. Assumption: stream-json exposes enough tool events to compare.
  Done when: `fm code gaps` prints a ranked list that includes a tool or event type seeded as missing in a fixture run.

- **Radar for open upstream pull requests** — FEATURE — value 3 — effort S — risk low — category: scout
  Why: `fm scout` watches Claude Code releases, which is reactive. Open PRs and issues in the six repos show what lands next, and the user wants this "automatic". Foreman files a "pre-adapt if merged" brief with a recheck trigger. It reads public metadata only, using `git ls-remote` or the unauthenticated API.
  Done when: against a fixture feed with one new open PR, `fm scout --prs` creates exactly one deferred brief that cites the PR URL, and a second run creates none.

- **Install plugins through the native installer in a scratch config dir** — SECURITY — value 4 — effort M — risk low — category: supply-chain
  Why: this reuses `claude plugin install` instead of reimplementing marketplace logic. Run it with a throwaway `CLAUDE_CONFIG_DIR`, diff what it wrote (hooks, MCP entries, permissions), run the guard audit, and only then replay the diff into the real directory. Third-party plugins must never run unguarded.
  Done when: a fixture plugin that adds a `PreToolUse` hook and a broad allow rule is refused with both findings named, and the real config directory is byte-identical afterward.

- **Run the claude-code repo's maintainer automation on Foreman's own GitHub issues** — FEATURE — value 3 — effort S — risk low — category: dogfood
  Why: assumption: that repo ships issue-triage and dedupe commands and workflows. Foreman has 60+ deferred briefs and an open-source push (T-0352) and no triage loop. Adapting upstream's own pattern is the cheapest "integrate automatically".
  Done when: a fixture issue duplicating an existing brief is labelled as a duplicate and linked to that brief by a dry-run `fm triage`.

- **Diff the user's enabled plugins against upstream's catalog** — FEATURE — value 3 — effort S — risk low — category: recommendations
  Why: the pack proposes ranked recommendations, but the cheapest signal is already on disk. `enabledPlugins` in settings plus which plugins the transcripts actually invoked tells Foreman what the user lacks versus what they installed and never used. Output is advice only, never an auto-install.
  Done when: with fixture settings enabling plugin A, which is never invoked, `fm plugins gap` lists A as "unused" and lists catalog entries matching the stack as "missing".

- **Acquire a missing runner CLI into a private prefix** — FEATURE — value 3 — effort M — risk med — category: runners
  Why: T-0336 and T-0335 are blocked because codex, gemini and opencode aren't live-verifiable here. "Works with anything" currently stops at "detected only". `fm code runners --try NAME` installs into a scratch prefix with a pinned hash, runs the conformance probe, records the result, and deletes the prefix. Nothing is installed globally without an explicit setting.
  Done when: with a fake package source, `--try` leaves a capability card and no files outside the prefix, and a hash mismatch aborts the install.

- **Wild: Predict the next upstream feature and pre-build its adapter behind a flag** — FEATURE — value 2 — effort M — risk med — category: foresight
  Why: wild. The pack assumes the changelog is the trigger, but cadence and open-PR themes could allow a flag-gated stub that is ready on release day. The risk is building for features that never ship, so the stub is capped at S size.
  Done when: against replayed changelogs, a held-out feature appears in the top 3 predictions.

- **Wild: Hold a nightly adversarial maintainer review of Foreman's own claims** — SECURITY — value 3 — effort M — risk low — category: honesty
  Why: wild. The user insists every claim have a check that runs. A child takes the stance of the upstream maintainer for a feature Foreman says it matches and tries to show the claim is overstated, using the recorded gap-miner traces as evidence.
  Done when: a deliberately overstated claim in a fixture README is flagged with its evidence, and a true claim is not.

- **Wild: Train a free apprentice by shadowing the strong runner's accepted slots** — FEATURE — value 3 — effort L — risk med — category: local-first
  Why: wild. When claude fills slots that pass every check, log the slot, the context and the verdict. A local model then gets those as few-shot exemplars on the same request kind, and promotion needs a bench win. This extends "works with anything" to cheap or offline runners.
  Done when: replaying 20 logged slots to a stub local runner raises its pass rate on a fixture bench versus no exemplars, and a drop blocks promotion.

- **Hold an exit-gate census per round: one deletion for every adoption** — CLEAN — value 3 — effort S — risk low — category: restraint
  Why: this is the do-less approach. The pack shows rounds that only add (about 300 TUI ideas, 29 round-1 briefs) while the user also wants "10x better". Each `fm round` close requires a net-surface line (verbs, settings, injected bytes) and refuses a net increase without a named removal.
  Done when: a fixture round that adds a verb and removes none fails to close and names the offending verb.
