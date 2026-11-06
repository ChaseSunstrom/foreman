# Brainstorm — lens: simplicity

- **Unify inbox, queue, batch and task into one item lifecycle** — CLEAN — value 4 — effort L — risk med — category: data model
  Why: the command list has capture, intake, batch, task, queue and relate for what is really one thing at different stages. Blocked and deferred items carry only free-text reasons (T-0325 sudo, T-0335..T-0337 live harnesses, T-0034 deferred). Proposal: one item type with a stage (raw, planned, active, done) and a typed `waiting_on` (user, time, external, item, tool) that drive and relate can act on.
  Done when: the old commands remain as aliases, a migration test converts a copy of real state with no loss, and `fm queue` lists a `waiting_on: tool` item with the missing tool named.

- **Define the task lifecycle as one transition table with property tests** — FIX — value 4 — effort M — risk low — category: correctness
  Why: recent bugs are all state transitions that disagreed with each other. The band stuck on step 1/5 while evidence existed (T-0406). A "no active task" refusal that didn't name the queued task (T-0409). Lane merge blocked by a dirty main checkout (T-0402). Proposal: a single table of legal (state, event) → state, with the UI, guard and drive reading it and a randomized event-sequence test.
  Done when: a generated test runs 10k random event sequences with zero illegal states, and deleting a table row makes it fail.

- **Rewrite a refused command into its allowed form** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: `fm focus T-0278 …; sed -i …` was refused twice in a row (T-0404), and the brief gate refuses `fm task new … --focus && <edit>`. The fix was a better message. The simpler fix is for the hook to split or reorder and return the corrected command itself, only where the rewrite is provably equivalent and gains no extra privilege.
  Done when: the replay corpus shows the focus-then-edit case passing in one tool call, and a rewrite that would widen privilege is still refused.

- **Enforce the guard with a PATH-shimmed shell on every harness** — SECURITY — value 4 — effort L — risk med — category: adapters
  Why: each adapter re-implements hook wiring. `bash -lc`/`zsh -ic` slipped past on Codex, Gemini's Stop hook can't be wired (T-0337), and T-0335/T-0336 are blocked on live verification. Proposal: one `sh` shim that runs the guard and then execs the real shell, so Codex, Gemini and opencode share one enforcement point instead of three.
  Done when: the real-bash differential suite passes through the shim under all three harnesses, and a blocked command is refused identically in each.

- **Keep central state in a git ref instead of a private store** — FEATURE — value 4 — effort L — risk med — category: sync
  Why: `fm sync` mirrors state into `.foreman/` as an opt-in side channel, and the multi-machine ideas on the list each need their own transport. Proposal: briefs, decisions and the ledger live under `refs/foreman/*` in the repo, so git gives history, merge, push and pull across machines with no new server.
  Done when: two clones with divergent ledgers run `git fetch` and `fm doctor` and end with a merged ledger and no lost events.

- **Ship a feature as a thin slice and unlock the rest only on use** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: assumption: about 20 of the 70-plus commands are rarely used (`fm usage` exists to show this). Several open FEATURE L items (T-0034, T-0035) are deferred as big builds. Proposal: split each L feature into a minimal slice plus follow-ups, and block the follow-ups until `fm usage` shows the slice was used N times.
  Done when: a seeded L brief produces a slice task and a locked follow-up, and the follow-up unlocks only after logged use.

- **Generate the skills from the CLI definitions** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: `plugin/skills/` has 72 entries and `plugin/lib/` has 35 modules. Hand-kept skill text and command help drift apart, and `fm docs` already reports markdown drift. Proposal: each skill's command reference is rendered from the same definition as `fm help`, with only the judgment prose handwritten.
  Done when: changing a flag in the CLI definition changes the skill text after a build, and a check fails if a skill's flags are out of sync.

- **Add `fm try`: a session that leaves no trace** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: the installer edits `~/.claude`, which is a heavy commitment just to evaluate Foreman. Proposal: `fm try` launches Claude Code with Foreman loaded for that one session only (plugin dir plus temporary settings), writing state to a temp project.
  Done when: before and after snapshots of `~/.claude` are byte-identical after a try session, and the guard still blocks a dangerous command inside it.

- **Fold the separate toggles into one settings file** — CLEAN — value 3 — effort M — risk low — category: config
  Why: autonomy, sensitive, trust, standing, budget, sync, share and notify are each their own command with their own storage. Proposal: one commented, diffable settings file with `fm set KEY VALUE`, where the old commands are thin aliases.
  Done when: `fm set autonomy full` and `fm autonomy full` give identical state, and `fm doctor` prints the whole configuration from the one file.

- **Make a markdown project page the database (wild)** — FEATURE — value 4 — effort L — risk med — category: data model
  Why: wild. Assumption: the user would rather edit a checklist by hand than learn the queue commands. Proposal: a hand-editable `PROJECT.md` of checklist lines where Foreman parses and normalises edits, and everything richer (plans, evidence) hangs off each line's ID.
  Done when: ticking, reordering or adding a line by hand is reflected in `fm queue`, and `fm` edits round-trip without clobbering the user's prose.

- **Hold weekly delete-golf (wild)** — CLEAN — value 3 — effort M — risk low — category: subtraction
  Why: wild. The user said cleanup requests "never got done", and deferred T-0166 still leaves code in `register.tsx`. Proposal: a scheduled lane gets one target (a module or a command) and is scored on lines removed while `fm bench` and `fm doctor` stay green. The best green result lands as a PR for review.
  Done when: one run produces a PR with a net line deletion and a bench-green report, and a deletion that turns bench red is rejected automatically.

- **Require a tweet-length close-out a cold reader can check (wild)** — FEATURE — value 3 — effort S — risk low — category: done gate
  Why: wild. Long briefs and ledger entries hide what a task actually did. Proposal: `fm task done` requires a ≤280-character summary, and a cheap cold agent that sees only that summary plus the file list must name the main file changed. A mismatch blocks the close.
  Done when: a task whose summary names a file the diff never touched is refused, and an accurate summary passes.
