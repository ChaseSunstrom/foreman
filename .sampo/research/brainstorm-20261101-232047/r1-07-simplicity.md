# Brainstorm — lens: simplicity

- **Fill the 58 cells from one rule table, not 58 sentences** — CLEAN — value 5 — effort M — risk med — category: coverage
  Why: the user's rule says templated cells don't count, yet the pack's own ideas repeat "fill by mechanism/probe/rule". Simplest honest form: a small file mapping each (area × surface × stage) to either a verb path, a session-path caller, or an n/a with a reason, where the *cell text is the verb name plus the file it lives in*. Nothing to template because nothing is prose.
  Done when: `fm genesis check` reports 0 empty cells and the templating lint finds no two cells sharing a phrase beyond the verb name.

- **Mark most Exhaustive-thinking cells n/a or existing, with the grep that proves it** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the Missions 3/4 lesson says "most of #11 and #12 were already built." Plan gate, race, `fm graph blast`, and `fm decide` exist per the pack's own idea list. Each cell records the file:line grep result.
  Done when: every "existing" cell names a path where `grep` finds the verb, and a test fails if the path disappears.

- **Collapse the plan-gate checks into one `plan lint` verdict** — CLEAN — value 4 — effort M — risk med — category: planning
  Why: assumption: readings, options, confidence, falsifier, tier floor and door-class checks are separate refusals today; the pack shows ~10 proposals adding more. One function, one ordered list of checks, one refusal text carrying the single fix command.
  Done when: adding a check is one list row and a refusal prints exactly one runnable command.

- **Make depth a single number derived from blast radius and reversibility** — FEATURE — value 4 — effort M — risk med — category: depth scaling
  Why: capability text says "scale depth to risk so an S task doesn't pay an L task's cost." Pack ideas pile on separate triggers (race, research, rival, tribunal). One score decides which fire.
  Done when: an S task with unknown-free blast gets zero extra ceremony and an L one-way task gets race plus rival, shown in `fm status`.

- **Stop asking when only one reading is left alive** — FEATURE — value 4 — effort S — risk low — category: asking
  Why: the user's rule: never block on questions about process; ask only for irreversible AND ambiguous. Ask-gate becomes one predicate and logs a decide-instead-of-ask receipt.
  Done when: a test with one reversible fork produces a `fm decide` row and no `fm ask`.

- **Delete a deliberation step for every one added** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: lean ratchet and "pay for new verbs with a deletion" appear repeatedly; exhaustive thinking is the area most likely to bloat.
  Done when: `fm task finish` on a task adding a plan-gate check lists the removed or merged check.

- **Show the deliberation as three lines at close** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: assumption: users can't see the thinking's worth. Line 1 readings considered, line 2 option picked and runner-up, line 3 what would change the pick.
  Done when: the finish receipt prints exactly those three lines for M and L tasks and none for S.

- **Reuse the exam's own scenarios as the coverage probes** — CLEAN — value 3 — effort M — risk low — category: coverage
  Why: existing child-authored exam items already exercise plan and race paths; citing them beats writing new probes.
  Done when: each non-n/a cell cites an exam item id that runs it.

- **Wild: Make the plan one sentence plus a falsifier** — FEATURE — value 3 — effort M — risk med — category: planning
  Why (wild): if the thinking is real it compresses. A plan that can't be said as "do X because Y; wrong if Z" is refused as unthought.
  Done when: the gate accepts a one-sentence plan with a runnable Z and refuses a long plan lacking one.

- **Wild: Let the cheapest model do the thinking once, then replay it** — PERFORMANCE — value 3 — effort L — risk med — category: cost
  Why (wild): cache readings and options by request-shape hash so a similar task reuses the deliberation instead of repaying.
  Done when: a second similar task skips option generation and the log shows the cache hit.

- **Wild: Delete the race verb; a race is just N lanes plus a judge file** — CLEAN — value 3 — effort M — risk high — category: simplification
  Why (wild): lanes and verify already exist; race is a thin composition.
  Done when: `fm race` is an alias printing the lane commands it expands to, with identical results on the existing race test.

- **Fold the "later from T-07xx" bundles that concern thinking into the grid** — CLEAN — value 2 — effort S — risk low — category: backlog
  Why: 28 deferred bundles are open work; thinking-related ones duplicate cells.
  Done when: the bundles are closed with a pointer to the cell that holds each idea.

Next question: Which of the 58 empty cells are empty because no real caller exists, versus because nobody wrote the line?
Next question: Does any existing plan-gate check have zero refusals in the ledger, and so be a candidate to merge?
