# Brainstorm — lens: bold bets

- **Auto-split L tasks into a dependency DAG of S/M children** — FEATURE — value 5 — effort L — risk med
  Why: the pack says one plan per task and no splitting. `fm run` already exists, so children could each get a fresh, small-context session.
  Done when: `fm split T` on an L brief writes ≥2 child briefs with `depends_on`, `fm focus` refuses a child whose dependency is not done, and `fm run` executes them in order.

- **Add a per-task token budget ledger with stage attribution** — PERFORMANCE — value 5 — effort M — risk low
  Why: the user says one session burned 20% of the weekly usage. `fm cost` gives totals per task but not per stage (plan, execute, audit, brainstorm).
  Mechanism: tag transcript spans by stage, set a budget by tier, and let the Stop hook emit one ≤400-char note at 70% ("audit reads are 40% of spend; use `fm audit prep` slices").
  Done when: `fm cost T --by-stage` prints per-stage tokens, and a task over 70% of budget produces exactly one note.

- **Detect thrash and stalls from a PostToolUse ring buffer** — FEATURE — value 4 — effort M — risk low
  Why: nothing currently notices the same file edited 5×, the same test failing with different errors, or a step running at 5× its estimate.
  Mechanism: keep a tiny per-task counter file and replace the next prompt with "stop: state a hypothesis, run the cheapest probe."
  Done when: a synthetic sequence of 5 edits to one file plus 3 failing runs triggers the note once, and hook p50 stays ≈30 ms.

- **Generalize red→green to hunk-level mutation checks for every type** — FEATURE — value 4 — effort L — risk med
  Why: verification is exit-code only, and red→green exists only for FIX. Assumption: temp-worktree revert is cheap enough for M/L tasks.
  Mechanism: for each changed hunk, revert it in a temp worktree and run the linked tests (`fm impact`). A hunk whose reversion leaves the tests green is flagged "untested" before `done`.
  Done when: a task with a deliberately untested hunk is blocked at `fm task done` with that hunk named.

- **Write a "tried and ruled out" handoff digest automatically** — FEATURE — value 4 — effort S — risk low
  Why: `fm run` and resumed sessions get only the brief and resume note, so dead ends get re-explored.
  Mechanism: PostToolUseFailure, reverted edits, and `fm decide` entries feed a ≤600-char "ruled out" section, written at PreCompact and Stop and injected at SessionStart and `fm run`.
  Done when: a resumed session's opening facts include the ruled-out list, and a replayed dead end is not retried in an eval case.

- **Compile skills into state-keyed cards loaded by section** — PERFORMANCE — value 4 — effort M — risk med
  Why: skills are long markdown, and the 40 playbooks are read whole.
  Mechanism: `fm card <skill> <state>` returns only the ≤300-char section relevant to the current step. Measure the token delta per skill load.
  Done when: average tokens per skill load fall ≥50% with no drop in the eval pass rate.

- **Warm baselines at focus (perf, size, test timing) and gate regressions** — FEATURE — value 3 — effort M — risk med
  Why: there are no perf or size baselines, and PERF tasks can't prove improvement.
  Mechanism: on `fm focus`, snapshot timings and artifact sizes in the background. `fm check` diffs them and fails PERF tasks with no measurable win.
  Done when: a PERF task cannot be closed without a recorded before/after delta.

- **Generate a weekly static HTML digest of work, cost, and lessons** — FEATURE — value 3 — effort S — risk low
  Why: single-user CLI, terminal-only dashboard, and the user never runs commands.
  Mechanism: `fm digest` writes a static file that `fm serve` also exposes, covering tasks done, cost by stage, lessons, and ruled-out paths.
  Done when: `fm digest --week` produces an HTML file whose numbers match `fm cost`.
