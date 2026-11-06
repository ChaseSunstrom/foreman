# Brainstorm — lens: deepen: web ui

- **Unify the Deliberation page into one "Thinking" workspace with a request-to-decision spine** — FEATURE — value 5 — effort L — risk med — category: web ui
  Why: the category has ~6 near-duplicate ideas (options board, fork map, readings/race page, plan board, depth gauge). Gen-0 #2 is one capability, so it wants one page: readings → approaches (including "use what exists" and "do less") → outcomes/failure modes → blast radius → race → chosen plan, each a collapsible stage on a vertical spine, fed from the plan file and race results.
  Done when: opening the page for a task with a recorded plan shows all six stages in order with data from that task, and an empty stage shows a named empty state instead of nothing.

- **Hover-to-provenance: every plan step links back to the user's words and forward to its evidence** — FEATURE — value 4 — effort M — risk low — category: web ui
  Why: combines "hover a plan step to light up the user's words" with proof runs. The user's recorded asks and steers are in the pack; a step that cites no ask is itself a finding. Show the step, the quoted words, and the command that proved it.
  Done when: hovering a step highlights its source quote and the page lists any step with no source under an "unanchored" badge.

- **Make the 58-cell grid actionable: click a cell to see its grounding, its gap and a "file task" button** — FEATURE — value 5 — effort M — risk med — category: web ui
  Why: the request is to fill 58 empty cells; the rule says a cell counts only when it names a concrete file-grounded capability with no reused phrasing. The heatmap should flag templated or duplicated cells (red) beside empty ones (grey) so users see why a cell doesn't count.
  Done when: the heatmap shows empty, templated, duplicated and filled as four distinct states, and clicking an empty cell shows its row, column and nearest grounded neighbours.

- **Add a "why not" ledger: rejected approaches stay visible with the evidence that rejected them** — FEATURE — value 4 — effort S — risk low — category: web ui
  Why: the standing rule says no idea is killed for ambition, and only proven harm or duplication removes one with the reason recorded; the page should show each loser and its reason, plus an "argue for the runner-up" button that spawns a lane.
  Done when: every non-chosen approach on the page shows a recorded reason or a "no reason recorded" warning.

- **Scale the depth gauge to risk and show the cost paid** — FEATURE — value 3 — effort S — risk low — category: web ui
  Why: gen-0 says an S task shouldn't pay an L task's cost. A gauge showing the depth chosen versus the tokens and seconds spent makes over- and under-thinking visible, and ties to the outcome-survival data.
  Done when: each task card shows a depth badge (S/M/L) plus cost spent, and a task whose spend is more than twice its tier median is marked.

- **Add an "as of" stamp and stale banner to every panel, and a "since you left" digest on the home view** — FEATURE — value 4 — effort M — risk low — category: web ui
  Why: the open questions ask what the user sees after a week away, and how they learn a trigger died when they rarely open the UI. Fold both into one landing page: what ran, what died silently (OS kill, expired auth), what needs a human yes.
  Done when: killing a lane's process without a log entry makes the next page load show it under "died without a trace", with a timestamp.

- **Show blast radius as live ripples that mirror `fm graph blast` and flag untested rings** — FEATURE — value 3 — effort M — risk low — category: web ui
  Why: the radius output exists; rendering rings by distance, with the ring's tests marked present or missing, tells a reviewer where a change is unproven.
  Done when: a change touching a file renders its dependents in rings, and a ring with no covering test is outlined.

- **Edge-case deck that persists into a bestiary of cases that later bit** — FEATURE — value 3 — effort M — risk low — category: web ui
  Why: merges two listed ideas. Cards come from each plan's edge cases; a card is promoted to the bestiary when a later failure matches it, giving the exhaustive-thinking capability a measured payoff.
  Done when: a recorded failure that matches a card's edge case marks it "caught" and the bestiary count rises.

- **Reduced-motion and keyboard parity for every board** — FIX — value 3 — effort S — risk low — category: web ui
  Why: assumption: the new pages (heatmap, deck, ripples, fork map) are motion-heavy, and the pillar asks for accessibility and empty/loading/error states on each.
  Done when: with `prefers-reduced-motion` set, no board animates, and every action reaches by Tab with a visible focus ring.

- **Wild: Decision Garden — each decision grows from a seed, and abandoned branches stay as pressed flowers** — FEATURE — value 2 — effort L — risk low — category: web ui
  Why: wild. Fork map plus the why-not ledger rendered as a garden: branches that survived to a shipped outcome bloom, ones that were rejected wilt but stay clickable. Nobody asked; it makes the long record of decisions pleasant to browse.
  Done when: the garden page renders one plant per decision, and clicking a wilted branch opens its recorded reason.

- **Wild: Replay the thinking as a scrubbable timeline, with a "what if I'd chosen the runner-up" ghost run** — FEATURE — value 4 — effort L — risk med — category: web ui
  Why: wild. Plans, races and proof runs are timestamped; a scrubber replays them and a ghost lane shows the runner-up's result from the parallel race, so you can check the choice by evidence, not first instinct.
  Done when: dragging the scrubber to any time shows the page state at that moment, and the ghost lane shows the runner-up's test outcome.

- **Wild: Pre-mortem mode: before a plan is accepted, the page shows a child's guess at how it will fail and the user can bet on it** — FEATURE — value 4 — effort M — risk med — category: web ui
  Why: wild. Ties into the existing bets and Brier calibration: a tool-less child writes three likely failures, the user (or Foreman) assigns percentages, and they settle when the task closes. Failure modes become scored predictions.
  Done when: a plan shows three pre-mortem items with percentages, and closing the task settles each held or missed in the calibration data.

- **Share a read-only snapshot link of the Thinking page for a cold reviewer** — FEATURE — value 3 — effort M — risk med — category: web ui
  Why: assumption: cold reads by a different model need the same view the user sees; a static export keeps data local and avoids publishing anything outward without a setting.
  Done when: an export command writes one self-contained HTML file of the page, with no network references.

Next question: Which of these pages are reached by a real session path (session start, fm next, the drive) rather than only by opening the UI, and what does the user get if they never open it?
Next question: What does the web UI show for a task whose plan was written by a non-Claude harness (codex, gemini, opencode, fm code), and is the stage data the same shape?
