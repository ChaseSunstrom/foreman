# Brainstorm — lens: delight

- **Draw the plan as a fork map** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: the pack's mission is "exhaustive thinking" (readings, approaches, outcomes, blast radius) yet it lives as plan prose; the user's steers keep asking for it to be visible ("show the user every idea on a checklist page"). Render readings as branches, the chosen approach lit, the runner-up dimmed, blast radius as ripples from the touched file.
  Done when: opening a task's page in the web UI shows a fork map with each reading and approach as a node, the chosen one highlighted, and a screenshot test confirms the nodes match the plan file's Readings and Approach sections.

- **Write a "why this one" sentence at close** — FEATURE — value 4 — effort S — risk low — category: receipts
  Why: assumption: the finish receipt shows evidence but not the road not taken; one plain sentence ("chose A over B because B's probe failed on X") is what people forward. Pack shows race and runner-up ideas but no one-line surface.
  Done when: `fm task finish` prints one sentence naming the chosen approach, the best runner-up, and the deciding fact, and it fails the gate if the sentence is empty on an M or L task.

- **Name the save** — FEATURE — value 3 — effort S — risk low — category: guard/receipts
  Why: assumption: the guard and deliberation catch real mistakes silently. A close line like "Caught: the first reading would have deleted 3 files; reading 2 didn't" turns invisible thinking into a small moment of pride. Tied to the "Show what the guard saved me" idea trail.
  Done when: a task whose final approach differs from its first reading prints a "Caught:" line at close citing both, and a task with no change prints nothing.

- **Make "do less" a first-class chip** — FEATURE — value 3 — effort S — risk low — category: web UI
  Why: the mission text names "use what exists" and "do less" as required approaches, but they read as bullets like any other. In the options board, give them a distinct chip and a tally of how often they won, so choosing the smallest thing feels celebrated.
  Done when: the options board renders "use what exists" and "do less" with a distinct chip, and the page shows the count of closed tasks where one of them won.

- **Show a depth gauge that scales with risk** — FEATURE — value 3 — effort S — risk low — category: web UI
  Why: "scale the depth to the risk, so an S task doesn't pay an L task's cost" is invisible today. A small gauge on the task header (S: one line, L: full fork map) with the reason ("touches 14 files, one-way step") shows the thinking was sized on purpose.
  Done when: each task header shows a depth gauge with a one-line reason, and an S task shows the lowest setting with no fork map.

- **Give every coverage cell a "try it" line** — FEATURE — value 4 — effort M — risk low — category: Genesis grid
  Why: the 58 empty cells are the mission; the user's rule says a cell counts only with a concrete capability grounded in a file. Adding a runnable one-liner per cell makes the grid something to click through, and doubles as the grounding proof.
  Done when: every filled Exhaustive-thinking cell on the site/genesis page carries a command that runs and exits 0 in `fm genesis check`, and a cell without one is shown as unfilled.

- **Fill the Genesis grid as a live heatmap** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: coverage.md is a table of 13 capabilities by surfaces by stages; empty cells are hard to see in prose. A heatmap with empty, existing, grounded and n/a colours, cells that fill with a short animation when a task lands, makes progress visible.
  Done when: site/genesis renders the grid as coloured cells from coverage data, and the count of empty cells shown equals the count `fm genesis check` reports.

- **Turn edge cases into a swipeable deck** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: edge cases are listed in plans and forgotten. A card deck per task kind, built from past reopens, lets the user flick through "what bit us last time" before approving a plan.
  Done when: the plan page shows a deck of at least the edge cases from prior reopens in the same area, and dismissing a card records it as seen.

- **Hover a plan step to light up the user's words** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the user's recurring pain is letter defeating intent (steered rows about re-scoping, "the request's wording"). Hovering a step highlights the phrases in their original ask that justify it; a step with no highlight is visibly orphaned.
  Done when: in the web plan view, each step highlights the matching span of the ask on hover, and a step with no match gets an "unanchored" marker.

- **Print each plan as a haiku on the status line** (wild) — FEATURE — value 2 — effort S — risk low — category: status line
  Why: wild: a seventeen-syllable summary of the chosen approach and its flip condition is the thing people screenshot and show others; also forces a compact statement of the bet.
  Done when: with a plan accepted, the status line shows a three-line summary under a fixed length that names the approach and the condition that would flip it.

- **Collect caught edge cases in a bestiary** (wild) — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild: each edge case that a plan caught before it bit becomes a named creature with a sketch-style card and a first-seen date; the page becomes a collection the user browses and shows off, and doubles as the edge-case deck's source.
  Done when: a page lists every edge case a closed task marked "caught", each with a name, the task id and a count of times it recurred.

- **Argue with the road not taken** (wild) — FEATURE — value 3 — effort M — risk med — category: deliberation
  Why: wild: a button on a closed task that has a cold child argue for the runner-up for three paragraphs, with the evidence, so the user can disagree with the decision after the fact and see if it holds.
  Done when: pressing it on a task with a recorded runner-up produces a saved argument citing at least one file or command output, labelled as advisory and never changing the task state.

- **Pulse the blast radius as ripples** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: `fm graph blast` output is a list; the mission's "blast radius" is the part users skim. Ripples from the edited file, brighter near callers and tests, with unknown shown as a dashed ring ("unknown", not "none", per the steered rows), make risk feel physical.
  Done when: the blast view renders rings by hop distance from the graph output, shows unknown regions dashed, and respects the reduced-motion setting with a static version.

Next question: What does the user actually open after a task closes (receipt, web page, status line, or nothing), so delight is placed where it gets seen rather than where it is easiest to build?
Next question: Which of these touches would the user find noisy by the third week, and what kill switch or quiet-hours setting keeps delight from becoming one more injected byte under the lean ratchet?
