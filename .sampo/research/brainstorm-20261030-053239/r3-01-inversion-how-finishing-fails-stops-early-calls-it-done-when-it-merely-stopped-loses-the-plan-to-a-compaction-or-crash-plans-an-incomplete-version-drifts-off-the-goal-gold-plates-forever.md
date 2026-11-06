# Brainstorm — lens: inversion: how finishing fails — stops early, calls it done when it merely stopped, loses the plan to a compaction or crash, plans an incomplete version, drifts off the goal, gold-plates forever

- **Run the finish checklist red-first** — FEATURE — value 5 — effort M — risk low — category: done verdict
  Why: gap map shows DONE-WHEN lines become criteria, but nothing shows each was ever red. A verify command that exits 0 on zero tests, or on a grep that matches nothing, "finishes" a goal vacuously.
  Done when: `fm goal` runs every criterion's verify command on the base tree at plan time. One already green is flagged "vacuous or already done" and can't count toward finish until it is shown red or marked pre-existing.

- **Tripwire on criterion edits** — SECURITY — value 5 — effort S — risk low — category: anti-weakening
  Why: assumption: under pressure the cheapest path to "done" is rewording a done-when or swapping in an easier verify command. The pack guards tests and the charter, not criteria.
  Done when: a criterion's text and verify command are hashed into the ledger at seal. An edit that changes either fails `fm task finish` unless an `fm decide` entry records the diff. A test covers a weakened regex.

- **Block done on debt introduced during the goal** — FEATURE — value 5 — effort M — risk med — category: stub detection
  Why: the MUST says "everything finishes completely", but `finish` checks criteria only. Stubs, `NotImplementedError`, new skips and "follow-up" text pass if no criterion names them.
  Done when: a diff scan from goal start finds added TODO/FIXME/skip/stub markers. Each must be a cut-list entry or a task, or done is refused with the file:line list. A fixture with one planted stub is refused.

- **Write an enforcement-ran receipt per stop** — FIX — value 4 — effort S — risk low — category: fail-open
  Why: hooks are bounded by the bench gate and a ~10 KB cap, and the Stop drive can time out. A silently skipped drive looks identical to a clean "done".
  Done when: every Stop consult writes a ledger line. SessionStart reports "unguarded stop" for a previous session with none. A test kills the hook mid-run and sees the report.

- **Detect edit oscillation before the drive cap burns** — PERFORMANCE — value 4 — effort M — risk low — category: stuck
  Why: the no-progress stop and DRIVE_MAX count turns, not thrash. A session flipping between two states of a file looks like progress.
  Done when: recurring file-content hashes within a task (A→B→A) trigger a replan or `fm decide` prompt, and the drive stops spending. A replayed oscillating transcript trips it in under N turns.

- **Keep a goal stack across interruptions** — FEATURE — value 4 — effort M — risk low — category: drift
  Why: the user's words show a stream of steers and side asks. Nothing says a goal displaced by a side request ever comes back.
  Done when: an off-goal UserPromptSubmit pushes the goal to a stack. When the side task closes, the next SessionStart or Stop re-injects it first. `fm goal` shows the stack.

- **Derive seam criteria from depends_on edges** — FEATURE — value 4 — effort M — risk low — category: planning gaps
  Why: decomposition covers parts but not joins. Surfaces shipped one at a time (CLI, MCP, pane) each pass alone, yet the end-to-end path is never a row.
  Done when: each depends_on edge yields an auto-added criterion running the producer's output through the consumer. A two-task fixture with a broken seam fails the goal while both tasks are green.

- **Escrow the last-mile budget** — FEATURE — value 4 — effort S — risk low — category: tail satellites
  Why: usage limits and drive caps hit the tail first, and the tail is docs, CHANGELOG, site page and pane line. The MUST lists them, so they're what gets cut.
  Done when: the goal reserves a fixed share of its budget and time for satellite tasks. Core tasks can't spend it, and a run ending with core done and satellites unstarted is classed "stopped".

- **Pin an ambition tier from the user's words** — FEATURE — value 3 — effort M — risk low — category: gold-plating
  Why: "best-in-class" in gen-0 and "quick fix" in a steer need different contents lists. Today the list size is whatever the model feels.
  Done when: a goal records a tier (sketch/solid/best-in-class), chosen via `fm decide` with the user's quoted words as the reason. The contents list lines carry the tier, and a change of tier is a ledger event.

- **Write the release text first, then audit its claims** — FEATURE — value 4 — effort M — risk low — category: done definition
  Why: assumption: CHANGELOG, README and site claims get written last and describe what was intended.
  Done when: the CHANGELOG entry is drafted at plan time as numbered claims. At finish each claim must map to an evidence line, and an unmapped or false claim blocks done.

- **Search the repo for each contents row before planning it** — FEATURE — value 3 — effort S — risk low — category: grounded plan
  Why: "what exists for #4 today" was hand-assembled in the pack. A planner that rebuilds an existing capability inflates scope and drifts.
  Done when: each row is tagged new, extend or already-there with the matching `file:line`. An already-there row becomes a verify-only task.

- **Hedge tripwire on the closing message** — FEATURE — value 3 — effort S — risk low — category: premature done
  Why: the model's "done" is untrusted data. "Should work", "I haven't run" and "remaining" are cheap, deterministic signals of a stop.
  Done when: a closing message matching a hedge list while criteria are open raises a "stopped, not done" verdict on the pane. Fixtures with and without hedges give both outcomes.

- **Wild: Sleepwalk drift test** — FEATURE — value 3 — effort M — risk med — category: drift
  Why: wild. Give a tool-less model only the last N ledger events and diffs with names scrubbed, and ask what is being built. Low similarity to the goal text means drift that task-to-row tracing can't see.
  Done when: a planted off-goal week of events scores below threshold, while an on-goal week scores above it.

- **Wild: Impossible-goal canary** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: wild. A goal with contradictory criteria can only end as "cannot finish, here's why". The exam covers looks-done, not unfinishable, which is where gold-plating forever lives.
  Done when: the exam has a kind whose correct verdict is "blocked: contradiction N". An arm that keeps working or claims done fails it.

- **Wild: Deletion-only closer** — FEATURE — value 3 — effort S — risk low — category: gold-plating
  Why: wild. Before done, a cold pass may only propose cuts from the contents list. Many cuts means the plan was padded. None means it was tight.
  Done when: closing a goal records a cut proposal count. Accepted cuts go to the cut list, and a padded fixture yields at least one cut.

Next question: What would a goal's own "pause" look like, such as the user deliberately parking it, and how does it differ in the ledger from a stop and from a dormant one?
Next question: Which of these checks must run inside the Stop hook's byte and time budget, and which must move to an out-of-band auditor?
