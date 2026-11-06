# Brainstorm — lens: simplicity

- **Collapse the 1396 skills into 50 verified cards** — CLEAN — value 5 — effort M — risk low — category: capability
  Why: T-0418 shows a skills update is a manual chore; the card store (small-model cards) already exists, and "one card per model rung" was proposed but not implemented. 1396 skills is a maintenance nightmare and context bloat.
  Done when: `samo skills` lists ≤50 cards; each has a measured lift; `samo doctor` fails if a skill is not a card.

- **Replace MASTER.md with `samo map` + `samo doc <verb>`** — CLEAN — value 5 — effort S — risk low — category: docs
  Why: MASTER.md is already too big to Read in one go; the user's own words show "README and website say only true, current things" is a standing struggle. A generated index + per-verb pages is simpler to keep current.
  Done when: MASTER.md is gone; `samo map` prints a 30-line index; `samo doc decide` prints the decide section.

- **Delete `fm` binary; it's `samo` with a prefix** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: Two binaries confuse users and double the test matrix. The rename to Sampo is done; the alias is a scar.
  Done when: `fm` is a symlink or a one-line script that calls `samo`; no separate test suite for `fm`.

- **One "off" switch that really turns Sampo off** — FEATURE — value 5 — effort S — risk low — category: reliability
  Why: The user's standing rule is "Sampo is the discipline layer," but if they want to test vanilla Claude, they should be able to. A real off switch (not just "reduce injection") is simpler to reason about.
  Done when: `samo off` disables all hooks and injections; `samo on` re-enables; `samo doctor` shows "Sampo is off."

- **One config file per project, not per capability** — CLEAN — value 4 — effort M — risk low — category: simplicity
  Why: The user's steers show a pattern of per-capability config (budgets, pace, round-first, etc.). A single `samo.toml` per project with clear defaults is easier to manage than 10 flags.
  Done when: `samo init` creates one `samo.toml`; all current flags are in it; `samo doctor` validates it.

- **One ledger line per outcome, not per hook event** — CLEAN — value 4 — effort M — risk low — category: observability
  Why: The ledger is growing to 2.4 GB; per-hook-event logging is noisy. One line per outcome (task closed, model called, ward blocked) is simpler to read and cheaper to store.
  Done when: `samo ledger --last 10` shows 10 outcomes, not 100 hook events; ledger size drops by 50%.

- **One error format: "what failed, why, what I can do"** — CLEAN — value 5 — effort S — risk low — category: developer experience
  Why: The user's own words show "fix the cold review's tower rules, hero offset, smear clip, Smith margin" — errors are scattered. A single error format makes debugging simpler.
  Done when: All `samo` errors follow the format; `samo doctor` uses it; tests assert on the format.

- **One "samo init" that sets up everything** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: The user's standing rule is "Sampo is the discipline layer for coding agents," but setup is not one-command. `samo init` should install hooks, create config, and verify.
  Done when: `samo init` in a fresh repo makes Sampo work; `samo doctor` passes.

- **One page of docs: "Sampo in 10 sentences"** — CLEAN — value 4 — effort S — risk low — category: docs
  Why: The user's own words show "README and website say only true, current things" is a burden. A 10-sentence summary is simpler to keep current than a full README.
  Done when: README has a "Sampo in 10 sentences" section; CI checks it against code.

- **One "samo replay" that shows the last task, not a log** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: The user's standing rule is "work in progress is published, not held." A replay of the last task (what was done, what was verified) is simpler than a log.
  Done when: `samo replay` shows the last closed task with its verify commands and results.

- **One "samo what-if" that answers "what if I turned this off?"** — FEATURE — value 3 — effort M — risk med — category: simplicity
  Why: The user's standing rule is "Sampo is the discipline layer," but if they want to test a capability's impact, they should be able to. A what-if mode is simpler than a full A/B test.
  Done when: `samo what-if --off decide` runs the next task without the decide model; `samo replay` shows the difference.

- **wild — One "samo goodbye" that leaves the repo clean** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: The user's standing rule is "Sampo is the discipline layer," but if they want to eject Sampo, they should be able to. A goodbye command that removes all hooks, config, and state is simpler than manual cleanup.
  Done when: `samo goodbye` removes all Sampo artifacts; `git status` is clean; `samo init` can re-install.

- **wild — One "samo ghost" that proves Sampo isn't in the way** — FEATURE — value 4 — effort M — risk med — category: simplicity
  Why: The user's standing rule is "Sampo is the discipline layer," but if they want to prove Sampo isn't slowing them down, they should be able to. A ghost mode that runs Sampo in the background without interfering is simpler than a full benchmark.
  Done when: `samo ghost` runs Sampo in the background; `samo status` shows "ghost mode"; `samo off` exits ghost mode.

- **wild — One "samo teach" that learns from the user's corrections** — FEATURE — value 4 — effort M — risk med — category: capability
  Why: The user's own words show "let the user teach Sampo a new phrase by saying it once, with a confirm" is a standing wish. A teach mode that updates the card store from corrections is simpler than manual card writing.
  Done when: `samo teach` in a session updates the card store from the user's corrections; `samo doctor` shows the new card.

- **wild — One "samo memory" that persists across sessions** — FEATURE — value 4 — effort M — risk med — category: capability
  Why: The user's standing rule is "manage all of that across sessions too, like a consensus thing." A memory that persists across sessions is simpler than a full state ledger.
  Done when: `samo memory` shows the last 10 sessions' outcomes; `samo memory --save` persists them; `samo init` loads them.

Next question: What is the *smallest* set of `samo` verbs that covers 80% of the user's workflow?
Next question: What is the *largest* single file in the Sampo repo that could be generated from other files, and how would that reduce maintenance?
