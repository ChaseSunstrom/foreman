# Brainstorm — lens: simplicity

- **Triage the 58 cells before writing any prose** — CLEAN — value 5 — effort S — risk low — category: coverage
  Why: the standing rule says a cell counts only if it names a concrete capability grounded in a file or a real gap. Lessons from Missions 3-6 say most of what was proposed was already built. Grep MASTER.md and `plugin/lib` once, tag each empty cell existing / gap / n/a with its proof, and only then write.
  Done when: a table of 58 rows exists, each tagged with a file path, a recorded gap, or an n/a reason, and the count by tag is printed.

- **Make a cell one resolvable reference of at most 140 characters** — CLEAN — value 4 — effort S — risk low — category: coverage lint
  Why: the templating rule rejects reused phrasing. A cell that is just a `path:symbol` plus a few words can't be templated, and a linter can check that it resolves. Assumption: the sweep can already resolve file paths.
  Done when: `fm genesis sweep` fails a cell with no resolvable reference or more than 140 characters, and passes the 58 filled cells.

- **Fill the cells by column rule, not cell by cell** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: the grid is capabilities × (surface × stage). Goal state lives in one place (assumption: the goal contents file and baton), so many stage cells for one surface share a single path. Write about 6 rules and let them stamp the cells. Each cell must still name a distinct capability, not reuse words.
  Done when: the 58 cells come from at most 8 rules, the templating check passes, and each rule cites a different file.

- **Accept n/a only after a counterexample search** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the standing rule requires n/a to be recorded. The simplest honest test is one grep for the surface name plus the capability's verb. An empty result is n/a, a hit makes it a cell.
  Done when: every n/a row carries the grep it ran and its empty result, and the sweep reruns the grep.

- **Add one `done-check` read to the existing goal verb** — FEATURE — value 5 — effort S — risk low — category: knows when done
  Why: the capability says it "knows when it's actually done rather than merely stopped". Assumption: goal contents rows already have a status. Print the unmet and unproven rows and exit non-zero, without a new verb or state file.
  Done when: on a goal fixture with one unmet row it exits non-zero and names the row, and on an all-met fixture it exits 0.

- **Treat every gap cell as a task only by root cause** — CLEAN — value 3 — effort S — risk low — category: task hygiene
  Why: the ideas so far include "turn gaps into tasks by root cause, not by cell", which fits the lesson that most proposals were already built. Fifty tasks from fifty cells would swamp the queue.
  Done when: the number of gap tasks filed is at most the number of distinct root causes listed, each task names its cells, and none duplicates an open task.

- **Stop the fill when a full column pass adds no distinct capability** — CLEAN — value 3 — effort S — risk low — category: stop rule
  Why: the pack asks for the 58 cells but also for no padding. A stop rule keeps the fill short, and leftover cells become recorded "inherit" or n/a rows.
  Done when: the fill log ends with a pass that added zero distinct capabilities, and every remaining cell has a recorded disposition.

- **Show one read-only Goal page in the web UI from the goal file** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: web UI is the only surface listed. Render contents rows, status and "unproven" straight from the file, with no new state, so the surface cells for #4 cite one real page.
  Done when: the page shows a fixture goal's rows with their status, an empty-goal state and an error state, and a test fetches it.

- **Pay for each added cell-supporting verb with a deletion** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: the standing lean rule says growth needs a measurement or a subtraction. Fill the cells by pointing at existing verbs and file a deletion task for any verb the triage finds duplicated.
  Done when: the net verb count after the mission is no higher than before, or each addition names the deletion task it pays with.

- **Wild: compute the grid live and store only exceptions** — CLEAN — value 4 — effort L — risk high — category: coverage
  Why: wild. If cells derive from the repo (verbs × surfaces × stages), `coverage.md` shrinks to a pinned snapshot plus a short exception list, and the empty-cell count can't rot. Assumption: verbs and stages carry machine-readable tags.
  Done when: deleting a cited feature in a scratch copy turns exactly its cells red, with no hand edit to `coverage.md`.

- **Wild: refuse the 59th cell unless one is retired** — CLEAN — value 2 — effort S — risk low — category: coverage
  Why: wild. A cap on row count forces each new cell to displace a weaker one, so the grid stays about the size of the real capability.
  Done when: adding a cell past the cap fails the sweep unless the same commit removes or merges one.

- **Wild: have a tool-less child compress the 58 cells to the distinct capabilities they really are** — FEATURE — value 3 — effort S — risk med — category: coverage
  Why: wild. Give a blind child only the cell labels and #4's text, and ask it to name the real capabilities. If 58 collapses to about 10, the fill is writing those ten and pointing the rest at them. It is a cheap consistency check on the whole mission.
  Done when: the child's list is stored beside the triage table, and each cell maps to exactly one capability in it.

- **Roll the plan forward in waves, not to the end** — FEATURE — value 3 — effort M — risk med — category: goal planning
  Why: assumption: a full best-in-class decomposition up front is long and goes stale across days. Keep detailed steps only for the next few rows, keep the rest as one-line stubs, and re-expand when a wave closes. It cuts the size of the state that has to survive a compaction.
  Done when: on a fixture goal with 20 rows, only the next 5 carry steps and `done-check` still counts all 20.

Next question: Which of the 58 cells can be filled by pointing at the goal contents file or the baton, and which need a capability that doesn't exist yet?
Next question: What is the smallest check that tells "finished" from "merely stopped" on a goal killed mid-run, and does any session path call it today?
