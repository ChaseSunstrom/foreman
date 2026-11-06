# Brainstorm — lens: deepen: grid

Answers to the carried questions my lens can reach:
- **Typed vs filed asks:** the grid can answer it. If every task carries a cell id and an origin (typed or filed), anticipation can be scored on typed asks only.
- **Wrong vs right-but-not-now:** an ignored anticipation keeps its cell. If a later typed ask lands in that cell, it was early rather than wrong.

- **Give every cell a permanent id and a history** — FEATURE — value 5 — effort M — risk low — category: grid
  Why: the existing "canonicalize cell ids" idea stops at naming. Dropped items, steers and tasks all point at cells by prose. A cell ledger records the id, every state change (empty, idea, path, n/a), the task that changed it, and the outcome later.
  Done when: `fm genesis check` fails if a cell's state changes without a ledger line, and `fm cell show <id>` prints its full history.

- **Print "what I left out" from the grid on every request** — FEATURE — value 5 — effort M — risk med — category: exhaustive thinking
  Why: the Mission is "say what it left out". The grid is the only structure that knows the full space. Each brief lists the cells it touched, the cells it deliberately skipped and why (n/a or deferred), and the empty cells nearby.
  Done when: a filed brief contains a "Left out" block with at least one cell id for each neighbouring row or column, and a test fails when it is missing.

- **Expire every n/a unless a reason keeps it alive** — FIX — value 4 — effort S — risk low — category: grid
  Why: this extends "revoke an n/a with a user story". The standing rule says only proven harm or exact duplication removes an idea. An n/a is a quiet removal, so each one carries a re-check date and a falsifier: "n/a unless a user does X". The seed retries expired ones.
  Done when: each n/a in coverage.md has a falsifier and a date, and the seed lists the expired ones first.

- **Score each cell by the typed asks that landed in it** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: assumption: the user's typed asks (ship, kill test, Mission requests) cluster in a few cells. Mapping each ask to a cell, with origin recorded, gives a real demand heat per cell that Foreman did not author.
  Done when: `fm outcomes --cells` prints demand per cell, counting typed asks only, and the empty high-demand cells head the next seed.

- **Add the failure-mode column from dropped items** — FEATURE — value 4 — effort M — risk low — category: grid
  Why: the dropped list shows recurring classes ("review.md marks it gap", "by design: the guard refuses…", "premise already met"). Dropped-premise-already-met is its own failure mode. Each cell is read against it: "could this cell's brief rest on a premise already met?"
  Done when: coverage.md has the new column filled for at least the 13 capability rows, and a spot check catches one real premise-met case.

- **Make a cell's Exam name an outcome measure and a live-state reading** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: this is the carried gap. A cell counts only if its exam names what changed for the user and reads the live state, for example `fm next` output, rather than the writer's own test.
  Done when: `fm genesis check` rejects a brief whose Exam lacks both fields, and one existing Mission passes.

- **Put a canary beside each non-empty cell** — FEATURE — value 4 — effort M — risk med — category: canaries
  Why: the carried gap says "canaries near the idea". Each cell gets one cheap probe that goes red if the cell's capability silently stops being called by a session path, which ties to the reach rule.
  Done when: a canary file per cell exists, and breaking a session-path call turns exactly one canary red.

- **Score dissents against outcomes** — FEATURE — value 4 — effort M — risk med — category: dissent
  Why: carried gap. Each cold-read dissent is stored with its cell and later marked right or wrong by what survived 14 days. Dissenters that are right more often than not get more weight.
  Done when: `fm outcomes --dissents` prints a hit rate per reviewer model, with at least 10 scored.

- **Draw the grid as a web board with fill, heat and age** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the only surface is the web UI, and the user wants to see everything on a checklist before anything is skipped. Cells show a state colour, demand heat, last-touched age and the task behind them. Empty cells pulse gently. A click opens the ledger.
  Done when: the page renders the rows by columns, shows loading and empty states, and a screenshot test shows one pulsing empty cell.

- **Test the axes, not just the cells** (wild) — FEATURE — value 4 — effort L — risk med — category: meta-grid
  Why: wild. A child that sees only the user's typed asks proposes a column or row the grid lacks. If it lands on one of the asks as unplaceable, the axis is missing.
  Done when: the child's unplaceable list for the last 20 typed asks is non-empty or provably empty, and each item is either grown through `fm genesis grow` or recorded as placed.

- **Run a cell sniper that tries to prove a filled cell is templated** (wild) — SECURITY — value 3 — effort M — risk low — category: red team
  Why: wild. The rule "no phrasing reused across rows" is checked by string similarity. An adversarial child rewrites one cell to pass the check while meaning the same thing and sees whether the check catches it. If it passes, the check is weak.
  Done when: the sniper's best attempt is caught by the check, or the check is fixed and a regression test is added.

- **Find a cell from the sentence the user repeats** (wild) — FEATURE — value 4 — effort M — risk med — category: unspoken needs
  Why: wild, and it answers the repeated-pipeline-sentence question. Three similar asks in a window match to the nearest cell. If no cell fits, a candidate row is proposed and the user is told once.
  Done when: replaying the last 30 asks yields at least one proposed row, and the proposal appears once in the final report.

- **Flag the diagonal: capabilities that exist on one surface and one stage only** — CLEAN — value 3 — effort S — risk low — category: grid
  Why: assumption: many rows are filled in one column only, usually the shell stage, and look covered. A report of rows with a single filled cell finds the thin coverage the sweep calls clean.
  Done when: `fm genesis check` prints single-cell rows, and the seed's first items come from that list.

Next question: Which cell of the grid has the highest typed-ask demand, and has no session path calling its capability?
Next question: When a cell's exam passes but no typed ask has landed in it for a whole generation, is it covered or just unvisited?
