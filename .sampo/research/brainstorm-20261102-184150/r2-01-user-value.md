# Brainstorm — lens: user value

- **Rank left-out cells by value of information** — FEATURE — value 4 — effort M — risk low — category: prioritisation
  Why: assumption: the pack lists many ways to record or show left-out cells but none says which one to probe first. A cell is worth probing when a cheap check (a grep canary, a `--json` read) could change the plan.
  Done when: `fm mission leftout` prints cells in order of (probe cost, plan-change chance), and a test shows a cell that one grep would settle outranks one that needs a model run.

- **Compile the user's "I'd know it worked if…" sentence into the Exam** — FEATURE — value 4 — effort M — risk med — category: measures
  Why: the carried gap says every Exam must name an outcome and a live reading, but a builder-authored measure can be gamed. The user's own words ("asked: ship…", "steered: the unblock command takes commas") show they judge by concrete observed results.
  Done when: a brief filed with a plain-words success sentence gets an `outcome:` line that quotes it, and filing refuses a brief whose outcome line doesn't share a noun with the sentence.

- **Check up a whole Mission in one command** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: the user repeatedly asks to ship and verify batches (T-2676 and others). No single verb reads every open brief's live reading and prints one verdict line.
  Done when: `fm exam mission <id>` runs each brief's live reading under a 60 s total budget and prints `N held, M changed, K unread`, with a test using a planted flipped reading.

- **Seal each Exam by content hash at filing** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: assumption: a builder can quietly reword an Exam it's about to fail. The standing rule says a failing run's criteria can't be edited (T-2702 drop), but nothing enforces it mechanically.
  Done when: editing a filed Exam's outcome or live line makes `fm task finish` refuse unless an `amend` record with a reason exists, and a test covers both paths.

- **Print the Mission's long pole** — PERFORMANCE — value 3 — effort S — risk low — category: speed
  Why: assumption: a Mission's wall time is dominated by one stage (grounding, a cold read, or the slowest lens) that nobody sees. The pack mentions many costs but no timing breakdown for the Mission itself.
  Done when: the Mission report ends with per-stage seconds and names the longest stage, checked against a fixture run with one stage artificially delayed.

- **Run a zero-token exhaustive pass first** — FEATURE — value 4 — effort M — risk low — category: simplicity
  Why: steers prefer free arms before session arms. Grid building, canaries, the verb table and the nouns-sweep need no model.
  Done when: `fm mission --free` files a grid with every cell marked `checked-free` or `needs-model`, spends $0 (receipt shows it), and a test confirms no child was spawned.

- **Link each brief to the doc line it changes** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: assumption: briefs that change behaviour often land without a MASTER.md line, and the user then has to ask for docs to catch up.
  Done when: closing a brief that touches a verb with no matching MASTER.md anchor prints a warning naming the anchor to add, and a fixture test fails on the undocumented case.

- **Match the number of briefs to what the user closed last time** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: open work already holds 30+ deferred "Later from" tasks. Filing more briefs than get closed grows the pile the user must triage.
  Done when: the Mission filer caps briefs at the trailing-3-Mission closed count (floor 3), moves the rest to a named overflow shelf, and the receipt shows both numbers.

- **Mark grounding steps as local or sent** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: the privacy angle is thin in the pack. A canary grep never leaves the machine; a model spot check does.
  Done when: each grounding claim in a Mission file carries `local` or `sent:<bytes>`, and the Mission report totals bytes sent, checked by a test with one mocked model call.

- **Show what the user gets to stop doing** — FEATURE — value 4 — effort M — risk med — category: value
  Why: assumption: the user's value is fewer re-asks. Each closed brief could name one repeated ask from their ledger that it should end, and an outcome reading can then count it.
  Done when: a brief's outcome line names a task-title pattern, and `fm outcomes` reports how many matching asks arrived after close, with a fixture covering zero and nonzero counts.

- **Let two briefs compete and the user pick (wild)** — FEATURE — value 3 — effort M — risk med — category: taste
  Why: wild; the user keeps dropping and steering items, so which of two candidate fixes they prefer is a rich taste signal. Today the choice is made silently.
  Done when: for one cell, two briefs are built in separate lanes and one yes/no choice is recorded with its reason, then shown in the next pack's anti-pattern slice.

- **Hand the user a one-line "worth a look" per Mission (wild)** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: wild; assumption: the user reads one line, not a Mission page. A tool-less child writes the single sentence it would say aloud to the user about the most surprising finding, scored later by whether the user opened that brief.
  Done when: the Mission report starts with that sentence, and the opened-or-not result is logged after the next session.

- **Spend the left-out budget on a monthly random cell (wild)** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: wild; assumption: the unvisited cells hide the next surprise. One random empty cell a month gets a $0 free-arm probe, and its result goes in the morning card.
  Done when: a seeded draw picks a cell, the probe result is recorded, and the card shows "probed: <cell>, found: <x>".

Next question: Which of the user's last 20 asks would a zero-token exhaustive pass alone have caught, and which needed a model?
Next question: Does the user read the Mission page at all, or only the finish card, and what would they miss if the page vanished?
