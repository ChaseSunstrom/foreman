# Brainstorm — lens: simplicity

- **Derive the goal baton from the ledger** — CLEAN — value 4 — effort M — risk med — category: goal state
  Why: assumption: the goal keeps its state in more than one place (baton, ledger, task rows). Earlier ideas reconcile them after disagreement ("Reconcile baton, ledger and repo on every resume", "Keep a shadow ledger rebuilt from git"). Making the baton a pure read of the ledger leaves nothing to disagree.
  Done when: deleting the baton file and running `fm goal` prints the same resume text, and a test finds no write path to the baton outside the renderer.

- **Collapse goal status words to four** — CLEAN — value 4 — effort S — risk low — category: vocabulary
  Why: assumption: status strings have drifted across modules (open, parked, stalled, superseded, stopped, done and so on). Four user-facing states (running, waiting on you, done, stopped) make every cell and the Goal page easier to write and probe.
  Done when: a grep over the goal modules finds every status string mapped to one of four names, and a test fails on a fifth.

- **Audit goal settings against real use** — CLEAN — value 3 — effort S — risk low — category: config
  Why: assumption: goal-related flags and settings have grown with each Mission. Keep a setting only if a ledger or decisions.md entry shows someone used a non-default value.
  Done when: `fm doctor` lists each goal setting with its observed non-default uses, and settings with none are removed or marked as removal candidates.

- **Make the empty-goal screen one sentence and one command** — FEATURE — value 3 — effort S — risk low — category: web UI, empty state
  Why: the pack lists no goal page, and the web UI is the only surface found. An empty state that says what a goal is and shows the one command to start one is the simplest cell to fill and probe.
  Done when: with no goal, the web UI Goal route renders at most two lines plus a copyable command, checked by a render test.

- **Show only the next action on the Goal page** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: earlier ideas propose boards, burn-ups, fog-of-war and hill charts. The simplest page shows the goal title, one "next row" and one "waiting on you" line, and links to the file for everything else.
  Done when: the Goal page contains no more than five text nodes for a live goal, and the next row matches `fm next`'s pick.

- **Fill each cell from the help text** — CLEAN — value 3 — effort S — risk low — category: coverage
  Why: assumption: `fm --help` and verb docstrings already name what each verb does. A cell may cite only a verb that appears in the help output, so the help text becomes the single source and nothing needs a second description.
  Done when: the sweep fails any cell whose cited verb is absent from the current help output.

- **Pause the fill at 15 cells and ledger the rest with a re-entry rule** — FIX — value 3 — effort S — risk low — category: coverage, scope
  Why: the standing rules count a cell only when it is grounded. A smaller grounded set beats 58 padded ones, and the unfilled ones carry a dated reason and a condition that reopens them, which keeps the "no idea killed" rule intact.
  Done when: every empty cell is either filled with a resolvable reference or listed with a reason and a re-entry condition, and the sweep counts zero templated cells.

- **Fix the bounded-help claim at ten lines** — CLEAN — value 3 — effort S — risk low — category: resume output
  Why: resuming after a crash or compaction is the capability's core. A hard ten-line limit, tested, stops the resume output from growing with each generation.
  Done when: a test fails if `fm goal` resume output exceeds ten lines on the biggest fixture goal.

- **Wild: make the plan an executable file** — FEATURE — value 4 — effort L — risk med — category: plan format
  Why: wild. Each row is one shell line that exits 0 when that row is finished, so "done" means running the file and no state has to be carried between sessions. This is the simplest possible finish oracle and works with any agent or harness.
  Done when: a three-row sample goal passes only after all three rows' commands exit 0, and killing the session midway then rerunning resumes at the first failing row.

- **Wild: delete the prose and keep a 58-line table** — CLEAN — value 3 — effort M — risk med — category: coverage format
  Why: wild. `coverage.md` becomes `cell,verb,file:symbol,probe` and is rendered to prose only for the site. There is no wording left to template, so duplicated phrasing cannot occur.
  Done when: the sweep's templating check is deleted as redundant and the table still round-trips to the existing site page.

- **Wild: run a goal on a one-page stranger test** — FEATURE — value 3 — effort M — risk low — category: simplicity check
  Why: wild. A tool-less child reads only the goal file and the resume text, then must say in two sentences what is done and what is next. Failure to do so means the state is too complicated to carry across a crash or compaction.
  Done when: for three fixture goals the child's two sentences match the ledger's done and next rows.

- **Remove one verb for each goal verb added by this fill** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: the standing lean rule says growth is paid for by deletion. The fill is the likely place for small additions to slip in, so this check is cheap insurance.
  Done when: `fm task finish` on the fill task reports the verb count unchanged or lower than at the start.

Next question: which goal states or settings exist only because of a past Mission and have no user-visible effect today?
Next question: if the web UI Goal page were the only surface that existed, which of the 58 cells could still be filled honestly?
