# Brainstorm — lens: user value

- **Track multi-task goals with a spend cap and a stop rule** — FEATURE — value 5 — effort M — risk med
  Why: the user's ask ("fully featured", "recurse, then implement all ideas") is a goal spanning dozens of tasks, but the state model has only tasks, a queue and an inbox. Nothing says when enough is enough, and the user worries about token burn. Mechanism: a `goal` record (intent text, child task ids, token budget from `fm cost`, exit criteria). Children link to it, `fm run` and the Stop-hook drive check it, and SessionStart shows one line ("goal 7/12 done, 60% of budget").
  Done when: with a 10k-token budget, `fm run` stops queueing a goal's children once the budget is spent and prints a one-line rollup.

- **Batch every pending yes/no into one decision sheet** — FEATURE — value 5 — effort M — risk low
  Why: the user only answers yes/no prompts, and approvals (merges, standing approvals, undo, assumptions, plugin installs) arrive scattered across the session. Mechanism: pending consents go into one state file, and a boundary hook (task done, run end) renders them as a numbered list. Each entry has a consequence line, cost, reversibility and a recommended default, so one reply like "yes to all but 3" resolves everything.
  Done when: three queued approvals produce one prompt, and one reply resolves all three.

- **Grade each finished task by how strongly it was verified** — FEATURE — value 4 — effort S — risk low
  Why: gates and audits exist, but the user can't tell which "done" tasks deserve a second look. Mechanism: at `fm task done`, compute an A–D grade from signals already in the brief (red→green proof, criteria with verify commands, audit tier, a `--affected` versus full run, scope-drift result). Put it in the outcome report and the digest.
  Done when: a FIX task with red→green and a full run grades A, and a CLEAN task with no tests grades D with a stated reason.

- **Start plans from the nearest successful past brief** — PERFORMANCE — value 4 — effort M — risk med
  Why: recall writes a "Related" section, but each task is still planned from scratch, which costs tokens on repetitive work (add a command, add a hook check). Mechanism: at focus, if a past done task has BM25 similarity above a threshold and the same type/tier, copy its steps and criteria as a marked draft skeleton with paths and names generalized. The planner edits the skeleton instead of writing a new plan.
  Done when: on a replayed near-duplicate request, the planning turn's output tokens drop measurably versus baseline (logged by `fm cost`), and the tests still pass.

- **Ping the user when unattended work finishes or blocks** — FEATURE — value 4 — effort S — risk low
  Why: the user never runs commands, and `fm run` and the drive loop work unattended, so they must poll to learn anything. Assumption: a desktop session with `notify-send` or a terminal bell is available. Mechanism: an opt-in `notify` setting; `fm run` end, Stop when blocked, and goal completion each emit one line through a local notifier, with a silent fallback to a `state/last-event` file that the statusline shows.
  Done when: finishing a headless run triggers exactly one notification with the outcome line, and a missing notifier does not error.

- **Show step-duration ETAs on the statusline** — FEATURE — value 3 — effort S — risk low
  Why: the statusline shows current state but not how long is left, and the ledger already holds step timings. Mechanism: keep per-type, per-tier median step durations from recorded logs and show "step 3/6 · ~8 min left". Turn it amber when a step passes 3× its median, which reuses the thrash signal without an extra prompt.
  Done when: the statusline shows an ETA after at least 5 comparable tasks, and nothing is shown before then.

- **Preview risky actions as a dry-run yes/no** — FEATURE — value 3 — effort M — risk med
  Why: the guard blocks dangerous commands, but blocking gives the user no way to see what would happen. Mechanism: for a blocked bulk delete, migration or rewrite, a guard hook variant runs a safe preview (`git clean -n`, a `--dry-run` flag, or a file-list count) and asks one yes/no with the concrete effect ("removes 41 files"). Approval is single-use.
  Done when: a blocked `rm -r` shows the file count in the prompt, and "yes" allows exactly that one command.
