# Brainstorm — lens: adoption and onboarding

- **Wire per project by default, not into `~/.claude`** — FEATURE — value 5 — effort M — risk med — category: install
  Why: the clean-HOME run shows the default install rewrites global settings (bypass mode, outputStyle, autocompact, statusline wrapper, 20 deny rules). Rivals "add commands, they don't rewrite `~/.claude`". Assumption: Claude Code reads project-local `.claude/settings.local.json` and hooks, so the same wiring can live in the repo and be gitignored. The hooks are already meant to be inert outside Foreman projects, so project-local wiring is the same behaviour with a smaller footprint.
  Done when: after a default install in a clean HOME, `diff -r` of `~/.claude` before and after shows only the plugin cache, and `fm init` in a repo is what enables hooks and guard there.

- **Prove Claude still starts after wiring, and ship a file-based off switch** — FIX — value 4 — effort S — risk low — category: install safety
  Why: a newcomer whose `claude` breaks after install blames Foreman and leaves. Assumption: some non-model `claude` invocation parses settings (the doctor's version probe may already do this). Today the only panic switch is `fm`, which can itself be the broken thing.
  Done when: the installer launches `claude` once with no model call, reverts its own wiring on failure and says so, and `touch ~/.claude/foreman/OFF` makes every hook exit 0 immediately.

- **Compose with the user's statusline and output style instead of replacing them** — FIX — value 4 — effort S — risk low — category: install
  Why: the install sets a statusline wrapper and outputStyle `foreman`, which overrides whatever the user already had.
  Done when: with a pre-existing statusline command, the rendered output equals the original plus one Foreman segment, and turning the segment off gives byte-identical output.

- **Merge the proposed onboarding verbs into one resumable `fm start` ladder** — CLEAN — value 4 — effort M — risk low — category: onboarding
  Why: the idea pile has hello, demo, tour, learn, spar and examples as separate verbs, while the audit says the surface should shrink from 108 verbs. Assumption: these can share one seeded-bug fixture.
  Done when: one command walks capture → plan → fix → evidence → finish on a fixture, remembers the rung after quitting, and no other onboarding verb is added.

- **Give every refusal a "tell the user" plain sentence for the model to relay** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: hook denials are read by the model, so the newcomer sees the model's paraphrase of jargon like "brief", "scope" and "drive" (finding A11). Done-gate and guard messages can carry one 15-word gloss line the model is told to pass on once.
  Done when: every refusal code has a gloss, a lint rejects glosses containing glossary-banned words, and a scripted refusal shows the gloss in the transcript.

- **Split the docs by audience with enforced word budgets** — CLEAN — value 4 — effort S — risk low — category: docs
  Why: MASTER.md is 18k words, and the README's first screen is abstract. Assumption: nobody reads MASTER.md to start.
  Done when: there are three documents (newcomer ≤ 400 words, operator, contributor), CI fails when one exceeds its budget, and the README's first screen has an example request and a result.

- **Show a per-client capability matrix (CLI, IDE extensions, desktop, web) in `fm doctor`** — FEATURE — value 3 — effort M — risk low — category: surfaces
  Why: Claude Code runs in IDEs, the desktop app and the web, but the band, mod and statusline are terminal-only and the install assumes `~/.claude`. Assumption: the client can be detected from the environment at SessionStart.
  Done when: SessionStart records the client kind, and `fm doctor` prints which Foreman features are active on that client and which are not.

- **Ratchet newcomer-path cost in CI** — CLEAN — value 3 — effort S — risk low — category: onboarding
  Why: the clean-HOME walkthrough already exists as a no-model gate. Extending it to count commands, output lines and seconds from install to the first closed task turns "feels heavy" into a number.
  Done when: CI fails if the install-to-first-finish path gains commands or lines over a committed budget.

- **Offer `fm init` automatically in the user's second repo with the same posture** — FEATURE — value 3 — effort S — risk low — category: adoption
  Why: assumption: the user-level posture choice is stored, so the second project needs no questions. A one-line offer on the first session in a new repo avoids a second onboarding.
  Done when: in an uninitialised repo, the first SessionStart offers a single-keystroke init that reuses the stored posture and creates no files until accepted.

- **Wild: make the tutorial a git repo whose history is the lesson** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: assumption: a newcomer who can `git log` and check out step N learns by doing. The same repo serves as the fixture for tests and the demo.
  Done when: the tutorial repo's commits pass tests in order, and `fm start` can check out any step.

- **Wild: a portable "Foreman passport" file for dotfiles** — FEATURE — value 3 — effort S — risk low — category: portability
  Why: one small file (posture, glossary level, vetoes, no secrets) lets a new machine or friend reproduce the setup. This contrasts with the heavy rewrite of `~/.claude`.
  Done when: `fm passport export` and `import` on a clean HOME reproduce the same posture with a printed diff, and no secrets are in the file.

- **Wild: publish a nightly "time to first task" badge from the clean-HOME run** — FEATURE — value 2 — effort M — risk low — category: proof
  Why: the first-run experience becomes a public, falsifiable number, and regressions show up as a visible trend. Assumption: the run stays no-model.
  Done when: a scheduled job records seconds, command count and failed checks, and the README badge updates from that record.
