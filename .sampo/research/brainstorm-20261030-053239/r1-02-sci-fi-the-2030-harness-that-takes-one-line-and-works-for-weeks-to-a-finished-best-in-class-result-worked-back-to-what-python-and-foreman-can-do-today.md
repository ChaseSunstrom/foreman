# Brainstorm — lens: sci-fi: the 2030 harness that takes one line and works for weeks to a finished best-in-class result, worked back to what Python and Foreman can do today

- **Make the goal ledger one file a goal lives in** — FEATURE — value 5 — effort M — risk low — category: goal ledger
  Why: gap map's top missing item for #4: contents list, tasks, done-when and coverage are scattered across mission prompt, briefs and clauses. In 2030 a weeks-long goal is a single object; today it needs one `goal.md` per goal with frontmatter (id, state, contents[], each item → task ids → criteria → evidence hash).
  Done when: `fm goal new "<line>"` writes the file, `fm goal show` lists every contents item with its task ids and status, and `fm goal check` fails if an item has no task or a task has no done-when.

- **Issue a typed done-vs-stopped verdict** — FEATURE — value 5 — effort M — risk med — category: verdicts
  Why: the pack names usage limit, crash, drive cap, no-progress stop and the model saying "done" as indistinguishable today. Verdicts: DONE (all items evidenced fresh), STOPPED:<reason>, STALLED, BLOCKED. Assumption: stop reasons can be read from the Stop hook payload and the ledger.
  Done when: replaying five recorded stop scenarios (limit, crash, drive cap, no-progress, premature "done") yields five distinct verdicts, and only the all-evidenced goal yields DONE.

- **Block "done" in the Stop hook on unmet goal items** — FEATURE — value 5 — effort M — risk med — category: stop hook
  Why: gap "Clauses wired to the Stop hook"; the model saying "done" is currently the weakest signal. Stop re-reads the goal ledger and refuses with the first unmet item quoted as data (c.plain).
  Done when: a fixture goal with one unevidenced item makes the Stop hook return a block naming that item; with all evidenced it allows stop; bench_hooks stays inside its gate.

- **Ground the contents list in the repo and the user's words** — FEATURE — value 4 — effort L — risk med — category: grounding
  Why: gap "Grounded contents lists... not model boilerplate". Each item must cite a source: a file:line, a user quote, a competitor feature note from research/, or a coverage.md cell. Uncited items are dropped to a "speculative" bucket that cannot gate done.
  Done when: `fm goal plan` output has a `source:` on every gating item, and a test fails if a gating item's source doesn't resolve.

- **Re-inject the goal each session with a progress line** — FEATURE — value 4 — effort S — risk low — category: continuity
  Why: "carried across days" is tier 3; SessionStart and PreCompact already exist. Inject a ≤1 KB block: goal, N/M items done, next item, last verdict. Assumption: it fits under the 10 KB preview limit with other context.
  Done when: after a simulated kill and fresh SessionStart, the context contains the goal block with correct counts, and it disappears once the verdict is DONE.

- **Grade goals on the exam with a "stopped-early" kind** — FEATURE — value 4 — effort L — risk med — category: exam
  Why: the pack says a capability is done only when held-out scenarios pass. Add child-authored kinds: G-done (truly finished, must say DONE), G-stop (hard stop mid-way, must say STOPPED and resume), G-fake (model claims done with one item missing, must be refused). Arms: plain session vs Foreman.
  Done when: `fm exam` reports the three G kinds per arm, holdout split respected, and the Foreman arm beats plain on G-fake.

- **Add epics above tasks via depends_on rollup** — FEATURE — value 3 — effort M — risk low — category: structure
  Why: gap "Epics: a goal above tasks". Cheapest form: an epic is a goal's contents item; its status is computed from its tasks, no new task type.
  Done when: closing the last task of an item flips that item to done in `fm goal show` without manual edit, and reopening a task flips it back.

- **Replan on drift instead of only continuing** — FEATURE — value 3 — effort M — risk med — category: replanning
  Why: weeks-long goals meet changed repos and new user words; a static list rots. When the Stop hook or `fm resume` sees files in a contents item changed by others, mark the item "stale" and queue a re-check, never silently dropping it.
  Done when: editing a file cited by a done item moves it to stale and the goal's verdict is no longer DONE until it's re-evidenced.

- **Ship a goal surface on every channel** — FEATURE — value 4 — effort L — risk low — category: surfaces
  Why: the MUST list demands pane, MCP, fm code, other agents, Desktop and site parity, and prior missions show this is what gets forgotten. Scaffold the satellites when the goal is filed.
  Done when: a test enumerates the surfaces and fails if any lacks a goal view (pane line, read-only MCP `goal` tool, fm code command, shim text, site page).

- **Wild: write a "definition of finished" the user can veto in one line** — FEATURE — value 4 — effort M — risk low — category: delight — wild
  Why: autonomy forbids asking mid-run, but one up-front, skippable summary ("I will call this done when: 12 items") with a default-accept costs nothing and catches the wrong-goal failure early. Assumption: user reads it once at the start.
  Done when: `fm goal new` prints the list, proceeds on its own without input, and a later `fm goal veto <n>` removes an item with a ledger event.

- **Wild: run a cold "finish auditor" before DONE** — FEATURE — value 4 — effort M — risk med — category: agents — wild
  Why: the one-reviewer-per-task lesson, lifted to the goal. A tool-less child receives only the contents list and evidence summaries and must name any item whose evidence doesn't actually show it done.
  Done when: a planted goal with one hollow evidence entry is rejected by the auditor, and a clean goal passes with zero objections.

- **Wild: replay a goal's history as a timelapse on the site** — FEATURE — value 2 — effort M — risk low — category: delight — wild
  Why: the ledger is hash-chained and already drives the Genesis tower graph page; a goal's items turning green over days is the same export. Assumption: reuse of the genesis export code.
  Done when: `fm goal export` writes a page under site/ that animates items from the ledger order and matches site header, footer and style.css.

- **Estimate time to finish from item history** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: weeks-long work needs a "how far" answer; per-item cycle times already exist in task ledgers. Show a range, and say "unknown" under three closed items.
  Done when: `fm goal show` prints a remaining-work range after three items close, and "unknown" before.

- **Pin the completeness bar to the exam kind of the capability** — FEATURE — value 3 — effort S — risk low — category: done-definition
  Why: the MUST list (tests, exam, docs, CHANGELOG, site page, pane, surfaces) is prose today. Make it a template of standing items auto-appended to every goal's contents, so "done" cannot omit docs or surfaces.
  Done when: a new goal's contents includes each standing item, and removing one requires an explicit ledgered waiver.

Next question: Does a goal need its own budget and wall-clock bound so a weeks-long run can't spend unbounded money, and who enforces it without asking the user?
Next question: When two goals are open in one project, which one owns the Stop hook's decision, and how do their contents lists avoid overlapping tasks?
