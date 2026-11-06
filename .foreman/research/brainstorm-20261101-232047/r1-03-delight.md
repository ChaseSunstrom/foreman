# Brainstorm — lens: delight

- **Draw the plan as a fork map** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: web UI is the only surface; the plan gate already holds readings, approaches and a chosen one. Branches grow in as they stream (loading state), the chosen path glows, pruned ones fade with a one-line reason.
  Done when: a task with 2+ approaches renders a map in the web UI, the chosen branch is highlighted, each pruned branch shows its reason, and a screenshot test passes for the empty, loading and filled states.

- **Name the save** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: assumption: users rarely see exhaustive thinking pay off. When a rejected reading, a race loser or a blast-radius neighbour would have failed, the close receipt says so once, e.g. "Approach B would have broken `fmcli` test X."
  Done when: a fixture task whose runner-up fails its verify prints exactly one "save" line at `fm task finish`, and a task with no save prints none.

- **Write the "why this one" sentence** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: assumption: the choice is recorded but not phrased for humans. One plain line names the winner, the runner-up and the deciding evidence, and goes in the finish receipt and the commit trailer.
  Done when: the finish output contains "Chose X over Y because …" with the evidence cited from a real run, for every task that had 2+ approaches.

- **Pulse the blast radius as ripples** — FEATURE — value 3 — effort M — risk low — category: web UI, motion
  Why: `fm graph blast` exists but its output is a list. Rings radiate from the changed file, and files pulse by distance, so a wide change looks wide.
  Done when: the web UI blast view renders rings from `fm graph blast` JSON, honours `prefers-reduced-motion` by showing static rings, and has a test that the ring count equals the distance levels.

- **Hover a plan step to light up the user's words** — FEATURE — value 4 — effort M — risk low — category: web UI, trust
  Why: the user's complaint history is "that isn't what I meant." Each plan step links to the phrase in the request it serves, and steps with no linked phrase are flagged as unrequested.
  Done when: hovering a step highlights its source span in the request pane, and a step with no span shows an "unrequested" chip in a test fixture.

- **Show a depth gauge that scales with risk** — FEATURE — value 3 — effort S — risk low — category: status line
  Why: the capability says to scale depth to risk. A small "thought: light / standard / deep (1 reading, 2 approaches)" chip shows an S task isn't paying L cost, which makes the restraint visible.
  Done when: the status line shows the chip, and S, M and L fixture tasks produce three different labels with correct counts.

- **Give every coverage cell a "try it" line** — FEATURE — value 4 — effort M — risk med — category: coverage, docs
  Why: the mission is to fill 58 empty cells, and the standing rule says a cell counts only if it names a concrete capability with no phrasing reused. Each cell carries one runnable command, and the dedupe lint rejects two cells with the same command.
  Done when: all 58 new cells have a distinct command that exits 0 in a fixture repo, and the templating lint passes.

- **Fill the Genesis grid as a live heatmap** — FEATURE — value 3 — effort M — risk low — category: site, motion
  Why: `site/genesis` is current via `fm genesis live`. Cells fill with a short fade as they pass the lint, templated cells show hatching, and the counter ticks down toward zero empties.
  Done when: `site/genesis` renders the grid from `coverage.md` data, shows hatching for a templated fixture cell, and its empty-cell count equals the sweep's count.

- **Turn edge cases into a swipeable deck** — FEATURE — value 3 — effort M — risk med — category: web UI, plan
  Why: assumption: long edge-case lists get skimmed. One card per case, with keys for "matters" and "ignore"; the "matters" ones become the test list, and ignored ones are recorded with a reason.
  Done when: marking 3 of 5 cards "matters" produces 3 red-first test stubs on the task, and the 2 ignored cases appear in the receipt.

- **Make "do less" a first-class chip** — FEATURE — value 2 — effort S — risk low — category: design language
  Why: the capability names "use what exists" and "do less" as required approaches, but they read like any other option. They get a fixed chip style across the pane, web UI and receipts, so their absence is obvious.
  Done when: the plan view renders "reuse" and "do less" chips, and a plan lacking either shows a visible empty chip instead.

- **Wild: Collect caught edge cases in a bestiary** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Each edge case the plan caught before it reached users becomes a card with a name, a one-line "how it bites," and rarity by blast radius. The web UI shows the collection, and the user shows it to others.
  Done when: closing a task with a recorded save adds one card to the bestiary page, and duplicates of the same signature increment a count instead of adding a card.

- **Wild: Argue with the road not taken** — FEATURE — value 3 — effort M — risk med — category: plan, delight
  Why: wild. Click a pruned branch and a cheap tool-less child defends it in three lines, using only the plan text, so the user can test the rejection before approving. Cached per branch.
  Done when: clicking a pruned branch returns at most 3 lines referencing that branch's recorded reason, with a logged cost under a fixed cap.

- **Wild: Print each plan as a haiku on the status line** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. A 5-7-5 summary of the chosen approach from a cheap model, kept beside the commit and collected on a "plans so far" site page. Playful, and it shows whether the plan can be said simply.
  Done when: an accepted plan stores a three-line summary, the status line shows it, and a plan whose summary exceeds three lines is rejected and regenerated once.

Next question: Which of the gate-0 capabilities has a plan or receipt visible only after the fact, and what would the user see during the work instead?
Next question: Does any delight touch above work with `prefers-reduced-motion`, a screen reader and a monochrome terminal, and does a test prove it?
