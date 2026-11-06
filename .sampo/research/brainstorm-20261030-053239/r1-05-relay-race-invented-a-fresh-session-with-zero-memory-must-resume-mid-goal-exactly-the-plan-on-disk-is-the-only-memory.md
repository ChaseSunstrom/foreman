# Brainstorm — lens: relay race (invented): a fresh session with zero memory must resume mid-goal exactly; the plan on disk is the only memory

- **Write a baton file per goal** — FEATURE — value 5 — effort M — risk low — category: goal ledger
  Why: the gap map lists "a goal ledger" and "a goal carried across days"; today only a task's "Resume here" survives compaction.
  Done when: in a project with an open goal, a fresh session that sees only the SessionStart injection (under 2 KB) names the same next action as `fm goal next`.
  The baton holds the goal in the user's words (quoted as data), the contents list, task ids, the next action, the last verified fact, and the decisions made.

- **Grade the relay with a kill-and-resume exam** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: the exam has no scenario for "carries the plan over days, across crashes". Assumption: `fm exam` can kill a session at a chosen point.
  Done when: a G-relay scenario kills the session at 3 seeded points, a cold session resumes from disk alone, and the grade counts redone steps (must be 0) and whether the goal finishes.

- **Compute a typed done-vs-stopped verdict** — FEATURE — value 5 — effort M — risk low — category: verdict
  Why: the gap map names it. Today the Stop hook sees DRIVE_MAX, a no-progress stop and "done" as different mechanisms with no shared answer.
  Done when: `fm goal verdict` returns FINISHED, or STOPPED with a reason (usage-limit, crash, drive-cap, no-progress, contract-bound, model-said-done). Fixtures cover all six, and "model said done" with an unmet criterion returns STOPPED.
  The verdict is derived from ledger events and criteria evidence, never from the model's words.

- **Log intent before each step and reconcile on resume** — FIX — value 4 — effort M — risk med — category: crash safety
  Why: a kill between an action and its recorded result leaves a resume that either repeats the action or skips it. Assumption: steps are mostly idempotent or checkable from the tree.
  Done when: a test kills between the intent line and the result line of a commit step. Resume inspects the tree, finds the commit exists, records the result, and does not commit again.

- **Re-prove "done" items on resume** — FEATURE — value 4 — effort M — risk low — category: drift
  Why: days pass between sessions, and the user or other tools may revert or break earlier work. `task finish` checks fresh evidence only at the moment of closing.
  Done when: after a commit that breaks a finished task's verify command is added, the next resume reopens that task, shows the failing criterion, and lowers the goal's progress.

- **Tie the contents list to its sources** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: the gap map's "grounded contents lists, not model boilerplate".
  Done when: every contents item carries a source tag (repo `path:line`, a user quote, or `assumed`). `fm goal check` fails an untagged item, and only sourced items count toward "finished" unless the item is accepted through `fm decide`.

- **Make the progress denominator honest** — FEATURE — value 4 — effort S — risk low — category: scope integrity
  Why: a "finished" verdict can be gamed by shrinking the list. Progress should read like "14/31 verified, 3 added, 1 dropped".
  Done when: removing a contents item without a `fm decide` event with a reason makes `fm goal check` fail, and the pane and status line show added and dropped counts.

- **Render every surface from one goal object** — CLEAN — value 4 — effort M — risk low — category: surfaces
  Why: the Missions' rule is "ships on every surface". Separate renderers drift apart.
  Done when: `fm goal render --for claude|fmcode|mcp|agents|pane|site` all read one JSON. A test asserts all six name the same next action and progress, and the MCP `goal_status` tool stays read-only.

- **Reconcile the plan with hand edits** — FEATURE — value 4 — effort M — risk med — category: drift
  Why: the user edits the repo between sessions, and a plan that ignores that redoes finished work or fights the user.
  Done when: after the user hand-implements a contents item, `fm goal reconcile` maps the changed files to that item, runs its verify command, and marks it "satisfied by user" with evidence instead of queueing a task.

- **Audit "finished" with a cold reviewer** — FEATURE — value 4 — effort M — risk med — category: verdict
  Why: "knows when it's actually done" is the capability's last clause, and a reviewer pass per task already catches what the author missed.
  Done when: before FINISHED, a tool-less child gets only the goal text and the repo summary, not the plan, and lists missing capabilities. Any item it names that is not in the contents list goes to `fm decide` and blocks the verdict until resolved.

- **Relaunch at the usage-limit reset** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: a usage-limit stop is the most common "stopped, not done" case. `fm run` and `fm serve` exist. Assumption: a reset time can be read or estimated, and the relaunch is covered by an existing grant.
  Done when: on a limit stop, Foreman writes the baton and schedules a headless resume at the reset time. A test with a fake clock shows it fires once and skips itself if the goal is already FINISHED.

- **Wild: write a letter to the future session** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: a first-hour plan can be scored against the final result.
  Done when: the first session of a goal writes a "what I expect the finish to look like" note, and on FINISHED `fm goal retro` diffs it against the final contents list, reporting items that were added late and items that were never needed. The result feeds the next grounded-contents prior.

- **Wild: run a shadow cold-resumer** — FEATURE — value 4 — effort L — risk med — category: observability
  Why: the baton can only be tested by someone who lacks the author's memory. Assumption: a cheap tool-less child can do this each night.
  Done when: a nightly child gets only the baton and answers "what is the next action and why". A mismatch with `fm goal next` is filed as a baton defect, and the pane shows a "baton readable by a stranger: yes/no" line.

- **Wild: write an epitaph for an abandoned goal** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: goals that stop for good are the ones users forget, and silence reads as a bug.
  Done when: `fm goal drop` (or 30 idle days, after a nudge) writes a plain page covering what shipped, what didn't and why, with one command, `fm goal revive`, that restores the baton and reopens the open tasks.

- **Wild: keep a goal diary on the site and pane** — FEATURE — value 2 — effort M — risk low — category: observability
  Why: Genesis already publishes a live tower page. A goal's day-by-day history is a natural sibling.
  Done when: the site page lists each session's start state, end state and verdict as a timeline built from the ledger, with no free-text model claims shown unquoted.

Next question: How does a goal behave when two sessions or lanes work on it at once, and who owns the baton's write lock?
Next question: When the user's own words change mid-goal (a steer or a drop), what rewrites the contents list, and how does a later session know which version it is carrying out?
