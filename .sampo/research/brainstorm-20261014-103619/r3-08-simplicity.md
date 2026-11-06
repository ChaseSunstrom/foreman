# Brainstorm — lens: simplicity

- **Vendor a minimal Foreman kernel in the repo for cloud and remote sessions** — FEATURE — value 5 — effort L — risk med — category: portability
  Why: the installer wires `~/.claude`, but `isolation: "remote"`, RemoteTrigger routines and Remote Control sessions run on machines with no such wiring. Assumption: those machines only see the repo.
  Done when: a fresh clone with `.foreman/` and `.claude/settings.json` enforces the guard, step pointer and done-gate in a `claude -p` run on a machine with no `~/.claude/foreman`.

- **Put an expiry on every shim for Claude Code behaviour** — CLEAN — value 4 — effort M — risk low — category: native overlap
  Why: tmux `send-keys` wakes, the foreman-ui bundle patch and the custom reviewer plumbing all work around Claude Code gaps that the unused-features list says are closing. Nothing records when a shim becomes deletable.
  Done when: each shim declares `until: CC <version>` plus a probe command. `fm doctor` lists shims whose probe now passes, and a test fails if a shim has no declaration.

- **Cap the `fm` CLI's output tokens per command, with golden tests** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: the user says they never want to be handed commands, so the CLI is read by the model on every call. Assumption: several commands print human-formatted tables the model re-reads each time.
  Done when: a test measures each command's default output on fixtures, fails above its budget, and `--pretty` restores the human layout.

- **Say what a task did in the user's few words, and lint for jargon** — CLEAN — value 4 — effort M — risk low — category: vocabulary
  Why: lane, band, pane, brief, ledger, veto, lesson, milestone and decision are all nouns the user would have to learn. Their own requests use "step", "task", "idle" and "milestone". Assumption: the core list is under 15 words.
  Done when: user-facing strings (close-outs, refusals, band text) are checked against a core-vocabulary file. Terms outside it need a one-line gloss at first use, or the lint fails.

- **Split core decisions from IO** — CLEAN — value 4 — effort L — risk med — category: architecture
  Why: guard, classification and gate selection are all being asked for replay, fuzzing and caching, and those only work cheaply if the decision code has no side effects. 48 lib files with tests mapped to each suggest the seam is reachable.
  Done when: an import lint shows the decision modules (guard parse, classify, plan gating) import no `subprocess`, `os.environ` or file-write helpers, and a replay test runs them from a recorded input alone.

- **Mark every state file as source or derived** — CLEAN — value 3 — effort S — risk low — category: state
  Why: after the recent bugs (a parser that misread results, STATE drifting from the step pointer), "which file can I safely rebuild?" has no written answer.
  Done when: each state path carries a tag in one registry. `fm clean --derived` deletes only derived files, and a test proves the next command rebuilds them byte-for-byte.

- **Forbid migrations by making the state schema expand-only** — CLEAN — value 3 — effort M — risk low — category: state
  Why: Foreman ships a release every few days (1.2.17 to 1.2.27) across projects at different versions. A rename or removal means a migration, and a migration means a skew bug.
  Done when: a test compares the current schema against the last release's and fails on a removed or retyped field. Readers tolerate unknown fields, and an old-version reader opens new state.

- **Register every write path and outbound call, and fail the doctor on strays** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: the user is asking for more integrations (Artifacts, push, cloud routines, SendMessage). Each adds a place data can leave or land. Assumption: no single list of Foreman's write targets and network calls exists yet.
  Done when: `fm data` prints every path written and every host contacted. A static scan fails `fm doctor` if code writes or connects somewhere not in the registry.

- **Detect duplicated knowledge in the lib** — CLEAN — value 3 — effort S — risk low — category: maintainability
  Why: the same fact lives in several places (the `exit N` / `✗ exit N` parser bug existed because parsing was spread out, and T-0750 fixed it by consolidating into one parser). Assumption: other duplicated regexes, thresholds and lists remain.
  Done when: a scan lists regexes, numeric thresholds and string lists that appear in two or more `plugin/lib` files, and the first report's top five are merged into single definitions.

- **Wild: Add `fm eject`, which leaves a project with plain markdown and no Foreman** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: assumption: a user can only adopt a heavy discipline layer fully if leaving is cheap. It also forces the state to stay human-readable.
  Done when: `fm eject` writes tasks, decisions and lessons to `docs/foreman-export/*.md`, removes hooks and settings entries for that project, and a Claude Code session in the project afterwards shows no Foreman hook output.

- **Wild: Shrink MASTER.md by ablating sentences against a cold-reader quiz** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: MASTER.md documents every file and part, and `fm doctor` already checks that it names every command. Length is policed only by "everything must be named".
  Done when: a job drops each sentence in turn and re-scores a cold agent on a fixed question set. Sentences whose removal doesn't lower the score are proposed for deletion in one diff, and the quiz score stays equal after applying it.

- **Wild: Lint everything the user reads for reading level** — FEATURE — value 2 — effort S — risk low — category: user value
  Why: close-outs, refusals and band text are the product's face. Assumption: they drift toward dense, internal phrasing as features land.
  Done when: a test scores a sample of generated user-facing strings against a target grade level and fails above it. The worst offenders from the first run are rewritten.
