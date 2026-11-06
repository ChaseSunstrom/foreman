# Brainstorm — lens: delight

- **Draw the plan as a fork map** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: the web UI shows readings, options and the race only as text; the plan gate checks "options" by text shape. A map with the user's words at the root, one branch per reading, and the chosen path lit makes deliberation visible at a glance.
  Done when: opening a task with a plan renders a tree with one node per reading and approach, the chosen path highlighted, and a screenshot test confirms the node count equals the plan's options.

- **Name the save at close** — FEATURE — value 5 — effort S — risk low — category: receipts
  Why: assumption: deliberation is invisible when it works. The user steers on "proof before presentation" and "plain words". A one-line close receipt such as "Considered 3 readings; the runner-up would have deleted your cache; dropped" shows what thinking bought.
  Done when: `fm task finish` prints a "what deliberation changed" line, or "nothing to think about" for S tasks, and a test covers both.

- **Pulse the blast radius as ripples** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: `fm graph blast` output is a list. Concentric rings by hop distance, with files that failed in past tasks shaded, make risk felt without reading.
  Done when: the plan page shows rings from `fm graph blast` data, honours reduced-motion, and shows "unknown" (not an empty ring) when blast can't be computed.

- **Hover a plan step to light up the user's words** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: steers show repeated pain over a "letter defeats intent" gap (T-2525 and the "meant it" ideas above). Hovering a step highlights the phrase of the request it serves and flags steps tied to no phrase.
  Done when: every plan step in the UI links to a quoted span, or is marked "unrequested", and a test covers both.

- **Show a depth gauge that says why** — FEATURE — value 3 — effort S — risk low — category: status line
  Why: the capability says "scale depth to risk". A small gauge reads "deep: touches the guard, one-way step" or "light: one test file". The user can trust S tasks aren't taxed.
  Done when: `fm status` and the UI print the depth and its single cause, and the cause comes from the same value the gate uses.

- **Give every coverage cell a "try it" line** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the 58 empty cells must be real and untemplated by the user's rule. A runnable one-liner per cell makes each one concrete, and templating is hard when each line must differ and run.
  Done when: each filled cell carries a command that exits 0 on the feature and non-zero when it is removed in a scratch copy, and the sweep rejects duplicate lines.

- **Fill the Genesis grid as a live heatmap** — FEATURE — value 3 — effort M — risk low — category: site
  Why: the standing rule publishes site/genesis on every tower change, so the grid is already published. Cells shade by state (existing, gap, n/a, unread) and each links to its proof, with new fills briefly glowing.
  Done when: site/genesis renders the grid from coverage data, empty cells are visibly hollow, and the cell count matches `fm genesis` output.

- **Make "do less" a first-class chip** — FEATURE — value 4 — effort S — risk low — category: plan UI
  Why: the capability names "use what exists" and "do less", and many earlier ideas show models skipping them. A fixed chip in every options row, always listed first, with a one-line "what stays undone", makes it easy to pick.
  Done when: the plan gate rejects an options list lacking a do-less or use-existing entry (S tasks excepted), and the UI shows it as a pinned chip.

- **Turn edge cases into a swipeable deck** — FEATURE — value 3 — effort M — risk low — category: review UX
  Why: an assumption: users skip long edge-case lists. One card at a time (input, expected, covered by test: yes/no), with keys to mark "build"/"skip", gives a quick way to review.
  Done when: the UI lists a task's edge cases as cards, keyboard-navigable, and marks are saved on the task.

- **Wild: Collect caught edge cases in a bestiary** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. Each edge case that deliberation caught before it shipped gets a name and a tiny sprite, shown in a page that fills in over time. It proves thinking paid off, and users show it to others.
  Done when: a bestiary page lists creatures created from closed tasks' edge-case rows, with each linking to its task and test.

- **Wild: Argue with the road not taken** — FEATURE — value 3 — effort L — risk med — category: deliberation
  Why: wild. A button on the runner-up approach opens a short replay: "if we had chosen this, here is the diff and where it fails." It uses the race's recorded lane when there was one, and a cheap-model sketch otherwise, labelled as such.
  Done when: clicking the runner-up shows the race lane's real diff and failing verify, or a sketch with an "unverified" label.

- **Wild: Print each plan as a haiku on the status line** — FEATURE — value 1 — effort S — risk low — category: delight
  Why: wild. A 5-7-5 summary of the chosen approach and its biggest risk, generated from plan fields, makes a glance memorable. It is off by default and costs no model call.
  Done when: with the setting on, the status line shows three lines built from plan fields, and with it off, nothing changes.

- **Collapse the deliberation to three lines at close** — FEATURE — value 4 — effort S — risk low — category: receipts
  Why: the deliberation produces readings, options, races and doors, while the user's steers favour "plain receipts". Three lines: the reading chosen, the road not taken and why, and one thing it did not prove.
  Done when: the close output has at most three deliberation lines plus a link to detail, checked by test.

Next question: Which of the 58 empty cells would the user actually notice missing, and does any past correction or reopen point to them?
Next question: What does the user feel when deliberation works and nothing visible happens, and where would a moment of delight, such as a receipt or a map, belong?
