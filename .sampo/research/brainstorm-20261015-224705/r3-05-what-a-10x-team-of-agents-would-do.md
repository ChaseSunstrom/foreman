# Brainstorm — lens: what a 10x team of agents would do

- **Staff the repo with standing seats** — FEATURE — value 5 — effort M — risk med — category: agents
  Why: assumption: every reviewer, lens and subagent today starts cold and forgets. A real team keeps QA, docs, security and release owners who build up notes. First version: `.foreman/seats/<name>/charter.md` and `notebook.md`, plus path-glob triggers. `fm seat run` builds a `claude -p` child from the charter, the notebook and the closed task's diff, then appends a dated finding. The seat files travel in git like the other shared brain files.
  Done when: closing a task that touches a seat's glob appends a notebook entry, and the next run's prompt contains it (stubbed `claude` in the test).

- **Run a bounded RFC round and show only unresolved objections** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: assumption: plan review currently shows the whole plan. Pre-mortem and plan-auction ideas exist, but none of them filters what the user sees. Before an L plan, two objector children each get one round. The plan is amended or the objection is marked unanswered. The review screen lists only the unanswered ones.
  Done when: an L plan with a planted flaw shows one unresolved objection, and a clean plan shows a single "no objections" line.

- **Reproduce feedback before it becomes a task** — FEATURE — value 4 — effort M — risk med — category: support
  Why: T-0317 "There's new bug feedback" sits deferred, and issues→tasks only creates tasks without proving anything. A support seat takes each feedback item into a throwaway worktree and tries to write a failing test. The item is labelled `reproduced` (with the test path) or `unreproduced` (with what was tried).
  Done when: a feedback fixture with a known bug yields a red test path, and a vague one yields an `unreproduced` label with a transcript.

- **Enforce architecture fitness functions mined from the import graph** — FEATURE — value 4 — effort M — risk low — category: architecture
  Why: `fm map` already knows imports and layout (1472 files). Nothing stops a new edit from adding a layering violation. `fm arch init` writes layer rules from the current graph, treating existing violations as a ratcheted baseline. A PostToolUse check flags any new forbidden edge.
  Done when: an edit adding an import across a mined boundary is flagged, and the baseline violations stay silent.

- **Walk the README in a clean room, for any project** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: the user wants Foreman to work on any project. Newcomer-facing docs rot silently. `fm walk` clones into an empty temp directory, then an agent follows the README or CONTRIBUTING to install and run. It writes a friction report quoting the first failing step.
  Done when: a fixture repo with a wrong install line yields a report naming that line, and a correct one yields "walked clean".

- **Give dependent lanes generated stubs so they run in parallel** — FEATURE — value 3 — effort M — risk med — category: fleet
  Why: assumption: contract commits and critical-path ordering exist, but a lane that needs another lane's API still waits. Generate a stub module from the declared signature so lane B starts at once. A swap check then stays red until lane A's real symbol matches the stub.
  Done when: lane B's tests run against the stub while A is unfinished, and the swap check fails on a signature mismatch.

- **Merge or split subagents by overlap in observed work** — CLEAN — value 3 — effort M — risk low — category: simplicity
  Why: the pack mentions 73 skills and many agents, and "hide skills the model never uses" only prunes. Compare tool and file footprints per agent from the ledger. Propose merging pairs that overlap heavily and splitting ones whose runs fall into two clusters.
  Done when: `fm roster` lists at least one overlap pair with its numbers on the existing ledger, and prints nothing if none qualify.

- **Record dissent and score it later** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: assumption: reviewer findings the user or builder overrules are dropped today. Store each overruled objection with its files. If a later red gate, revert or fix-after-edit hits the same files, log "dissent vindicated" and weight that seat's next objections higher.
  Done when: an overruled finding is stored, and a later fix on the same file adds a vindication entry visible in `fm digest`.

- **Wild: Drill the bus factor on every seat** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: wild. Seat notebooks only matter if a stranger can use them. Weekly, a fresh cheap agent gets only the notebook and answers five questions the seat answered last week. A low match means the notebook is thin and the seat gets a "rewrite notes" task.
  Done when: a notebook with key facts deleted scores lower on the drill than the intact one.

- **Wild: Run a simplification skunkworks with differential traces** — FEATURE — value 4 — effort L — risk med — category: simplicity
  Why: wild. Nobody asked for it, but the user keeps steering toward "less clutter." Idle time, in a sandbox clone: pick a module, record its test inputs and outputs, have a child rewrite it shorter, and run the original suite plus the recorded traces. Only rewrites that match every trace and delete more than N lines get surfaced.
  Done when: a seeded verbose module comes back as a shorter diff with identical traces, and a rewrite that changes a trace is discarded.

- **Wild: Open a seat library with probation** — FEATURE — value 3 — effort L — risk high — category: ecosystem
  Why: wild. Teams can import a seat charter from a pack, just as they hire someone. A new seat runs in observe-only probation on the replay corpus, and promotion needs a measured catch rate. Imported charters are untrusted text, so they're read, not run.
  Done when: an imported charter on probation writes findings but cannot block a close, and `fm seat promote` is refused until a replay score exists.

- **Wild: Spawn a sprint-review seat that demos instead of reports** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: wild. At the end of a day or a batch, a seat picks the three most user-visible closes and produces a runnable demo script plus one screenshot or recording each (the demo harness already exists). The idle pane shows a link, so the user sees outcomes rather than prose.
  Done when: a day with a UI-touching close produces a `demo/` entry with a script that runs and an image, and a day with only internal changes says so in one line.
