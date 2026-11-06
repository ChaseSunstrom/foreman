# Brainstorm — lens: user value

- **Ship a native plugin-marketplace install with zero config rewrite** — FEATURE — value 5 — effort M — risk med — category: adoption
  Why: Section B shows every popular rival installs with one marketplace/npx command and only adds commands; Foreman clones into ~/.claude, sets bypassPermissions, installs third-party plugins and 20 deny rules. Newcomer finding A2. Assumption: the plugin dir layout can be published as a marketplace entry without install.sh.
  Done when: in a clean HOME, `/plugin install foreman@<marketplace>` yields working hooks and skills, and `~/.claude/settings.json` has no permissions.defaultMode change.

- **Add `fm hello`, a 60-second guided first task on a throwaway fixture** — FEATURE — value 5 — effort M — risk low — category: onboarding
  Why: A1, A5, A6, A9: README is abstract, `fm init` prints a slug, `task new` makes duplicates, `task finish` is buried. Nothing shows a before/after.
  Done when: in a clean HOME, `fm hello` runs capture → plan → fix → `task finish` on a bundled toy repo and prints a before/after in under 90 seconds with no model calls.

- **Put `fm` on the user's shell PATH at install** — FIX — value 5 — effort S — risk low — category: install
  Why: A3: "command not found" in a normal shell while README says "run fm …" everywhere.
  Done when: after install, a fresh login shell resolves `fm --version`, and uninstall removes the shim.

- **Make a fresh install pass its own `fm doctor` and end with one line** — FIX — value 4 — effort S — risk low — category: first-run
  Why: A8: new install fails doctor on a missing backup and prints 40 passes. Pairs with the existing "one line, green or first failing fix" idea but targets the fresh-install state specifically.
  Done when: `fm doctor` right after a clean install exits 0 and prints at most 3 lines.

- **Offer a Foreman "lite" posture chosen at install: ask, don't assume bypass** — FEATURE — value 5 — effort M — risk med — category: trust
  Why: A2 calls bypass-by-default a large trust ask; rivals add hook profiles (minimal/standard/strict) after conflict complaints. Install prints one choice with plain consequences and the default keeps the user's current permission mode.
  Done when: the installer shows a three-option prompt (lite/standard/strict), lite changes no permission mode, outputStyle, or statusline, and the choice is recorded and shown by `fm status`.

- **Ship a published proof page: Foreman vs. bare Claude Code on a public task set** — FEATURE — value 5 — effort L — risk med — category: proof of value
  Why: C: the bench has 1 case and 3 court cases at 0/3; no evidence Foreman helps, while rivals have 100k+ stars. Assumption: a dozen real fix-commit cases from open-source repos can be replayed headlessly within budget.
  Done when: README links a page with ≥12 cases, N runs each, with pass rate and token cost for with/without Foreman, reproducible by one command.

- **Detect the test runner and offer it as the gate on first `fm check`** — FEATURE — value 4 — effort S — risk low — category: first-run
  Why: A7: with no gates configured nothing is detected; C shows `fm repeats` suggests single test modules as gates, which is bad advice.
  Done when: in a repo with pytest or unittest and no gates, `fm check` proposes the whole-suite command and one yes records it; `fm repeats` never proposes a single module.

- **Make `fm task new` smart about duplicates and self-describing** — FIX — value 4 — effort S — risk low — category: ergonomics
  Why: A6: a capture followed by `task new` makes a duplicate; `--help` lists no valid --type/--tier values or example.
  Done when: `task new` with a title matching an open capture links it and says so; `--help` lists valid values and one example.

- **Import an existing repo's conventions into injected standards (`fm adopt` standards)** — FEATURE — value 4 — effort M — risk low — category: conventions
  Why: B lists agent-os conventions extraction as a gap; Foreman has map but no standards file. Assumption: conventions can be derived from sibling code plus CLAUDE.md without model calls.
  Done when: `fm adopt` writes a ≤600-char conventions card from a sample repo, and SessionStart injects it.

- **Wild: Give Foreman a "tell me what you'd have done differently" receipt vs. plain Claude** — FEATURE — value 4 — effort L — risk med — category: proof — wild
  Why: A user's real question is "what did Foreman add here?" C shows no answer exists. At close, replay the diff against the ledger and list the gates that fired, catches, and seconds added.
  Done when: `fm task finish` prints a ≤5-line "what Foreman added" block counting actual blocks, evidence demands and seconds, from the ledger.

- **Wild: Turn the README into a self-running demo (`fm demo` plays a recorded session)** — FEATURE — value 3 — effort M — risk low — category: onboarding — wild
  Why: A1: abstract first screen. A recorded, offline terminal cast of a messy request becoming a verified task shows value without trust or model cost.
  Done when: `fm demo` replays a bundled 45-second transcript with no network, and README embeds the same cast above the fold.

- **Wild: A "pause Foreman" one-word escape that hides it for a single task** — FEATURE — value 4 — effort S — risk low — category: trust — wild
  Why: Footprint (C, D) and newcomer jargon suggest users sometimes just want plain Claude. `fm off` for one task/session lowers friction and builds trust.
  Done when: `fm off` disables non-safety gates for the current session, `fm status` shows "off", and the guard stays on.

- **Hide the 108-verb surface behind a ten-verb `fm help` and a pointed `--help`** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: A4 and D: `fm --help` is 231 lines with ticket numbers; `fm help` is better but unlinked.
  Done when: `fm --help` prints ≤25 lines naming the core verbs and `fm help --all`; no ticket numbers appear in user-facing output.

- **Make uninstall leave nothing behind and restore prior settings exactly** — FIX — value 3 — effort S — risk low — category: trust
  Why: A10: residue dirs, plugin cache, stray projects/ dir, and "defaultMode = None" printed. A reversible install is part of a safe trial.
  Done when: install then uninstall in a clean HOME leaves a byte-identical `~/.claude` tree.
