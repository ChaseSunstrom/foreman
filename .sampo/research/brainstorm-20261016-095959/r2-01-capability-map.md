# Brainstorm — lens: capability map

- **Read every harness's rule files and commands as one config** — FEATURE — value 4 — effort M — risk low — category: compatibility
  Why: assumption: users arrive with CLAUDE.md, AGENTS.md, GEMINI.md, `.cursorrules`, and custom slash commands and skills. Every rival reads at least some of these. The pack shows `fm agents install` writing rules out, but nothing reading them in for `fm code`.
  Done when: a fixture repo with AGENTS.md, CLAUDE.md and a `.claude/commands/x.md` shows all three in `fm code --show-context`, with conflicts between them listed.

- **Feed LSP diagnostics back after every edit** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: Cline, Zed and OpenHands return compiler or type errors to the model right after a write. T-0788 defers LSP for blast radius, but not as a per-edit feedback loop. This also helps small models most, since the errors are exact.
  Done when: with a fake LSP server that reports one error, an edit through `fm code` returns that error in the tool result and the loop fixes it before `finish`.

- **Add plan mode and approval modes to `fm code`** — FEATURE — value 4 — effort S — risk low — category: permissions
  Why: Claude Code, Codex (suggest, auto-edit, full-auto) and Gemini all ship named approval tiers. The pack has the guard but no user-facing ladder. Assumption: the tiers map onto the existing guard policy.
  Done when: in `--mode plan` every write tool is refused with a message that names the mode, and `--mode auto-edit` still asks before running Bash.

- **Manage background processes as a first-class tool** — FEATURE — value 4 — effort M — risk med — category: tools
  Why: assumption: dev servers, watchers and long test runs block simple loops. Rivals offer start, tail, and kill for background shells. Foreman's gates (`fm doctor`, e2e) are long and benefit from the same.
  Done when: a task starts `python -m http.server` in the background, curls it, reads its log tail, and the process is killed at task close with no leftover pid.

- **Add web fetch and search tools behind a domain allowlist** — FEATURE — value 3 — effort M — risk med — category: tools
  Why: Claude Code, Gemini CLI and Goose all fetch docs. In `fm code` the guard would be the choke point, and the default would be off or offline-safe, which suits the local-first constraint.
  Done when: a fetch to an unlisted domain is refused with the allowlist hint, and a listed one returns text truncated to the token cap.

- **Run as a CI and PR-review action (headless GitHub Action)** — FEATURE — value 4 — effort M — risk low — category: integration
  Why: the user is already building `fm pr --post` and `fm audit run`. Claude Code and Codex both ship a GitHub Action. Combined with the gates, this is the review bot.
  Done when: a workflow YAML in the repo runs `fm code --ci` on a PR from a fixture, posts one review comment through a fake gh, and exits non-zero on a failed gate.

- **Add an auto-commit-per-edit mode with `/undo`** — FEATURE — value 3 — effort S — risk low — category: git
  Why: Aider's most loved feature. Checkpoints are already proposed, but plain git history that a person can read and `git revert` is a different surface. It must respect the user's pending dirty files (T-pending close rule).
  Done when: three edits make three commits tagged `fm:`, `fm code undo` removes only the last, and pre-existing dirty files are untouched.

- **Export and share a session as a redacted transcript** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the pack has replay and a web UI session view, but no portable artifact. Bug reports, model comparisons and eval capture (T-0035) all need one. Redaction matters because Foreman logs commands.
  Done when: `fm code export SESSION` writes a single HTML or JSONL file with secrets from a seeded fixture replaced, and `fm code replay` accepts it.

- **Add image input and screenshot verification** — FEATURE — value 3 — effort M — risk med — category: multimodal
  Why: the pack lists web UI work and the pillar "screenshot every screen". Rivals accept pasted images. Assumption: models without vision get a skip note, not an error.
  Done when: a task attaches a PNG, the vision-capable fixture model gets it as an image part, and a non-vision profile logs "image skipped".

- **Wild: Let the model set its own reasoning budget per slot, measured** — FEATURE — value 3 — effort M — risk med — category: cost
  Why: wild. Claude, o-series and Gemini expose thinking effort. The harness knows which slots (plan, edit, verify) failed before, so it could spend effort only on the slots that history says need it.
  Done when: the ledger shows plan slots at high effort and edit slots at low for a fixture model, with total tokens lower than a fixed-high run on the same brief.

- **Wild: Provide a pocket "fm code" over SSH and phone** — FEATURE — value 3 — effort M — risk med — category: surfaces
  Why: wild. The web UI exists and the work runs overnight. A phone page with approve, deny and "what did it do" over a tunnel would complete the unattended story (assumption: auth uses a one-time token).
  Done when: from a second device on the LAN, a pending approval shows up in under 2 seconds and tapping it releases the blocked step.

- **Wild: Add a cross-model "second opinion" gate before every irreversible action** — SECURITY — value 4 — effort M — risk med — category: safety
  Why: wild. Today the guard is rule-based. A tiny different-vendor model (or a local one) could judge only commands the rules flag as ambiguous, with the rules still winning on any deny.
  Done when: an ambiguous fixture command goes to the judge and is logged with its verdict, a rule-denied command never reaches it, and a judge outage fails closed.

- **Publish a settings layering and managed-policy file** — FEATURE — value 3 — effort S — risk low — category: configuration
  Why: Claude Code has user, project, local and enterprise layers. Foreman has state and settings across modules, and teams adopting it for other CLIs will want one pinned policy (allowed models, spend caps, guard strictness) that users can't loosen.
  Done when: a managed file setting a spend cap overrides a project file that sets a higher one, and `fm settings --explain` names which layer won.
