# Brainstorm — lens: user value

- **Open a steer inbox the tower reads between stages** — FEATURE — value 5 — effort M — risk low — category: steering
  Why: the user steers constantly mid-run ("I want foreman to just genuinely be smarter", standing rules for the whole run), and today that depends on a session happening to be open. Assumption: a steer arriving mid-generation currently waits for the next session.
  Done when: `fm genesis say "never touch the demo"` mid-run is shown verbatim at the next stage boundary, lands in the charter candidates with its quote, and yields a regression scenario.

- **Weight the coverage grid by what the user actually asks for** — FEATURE — value 5 — effort M — risk med — category: prioritization
  Why: the recent asks skew heavily to site polish, motion, docs freshness and cards, yet a grid with "no empty cells" treats every cell equally. Revealed preference should set the order and the spend.
  Done when: on a fixture history that is 70% UI asks, the UI cells rank first in the mission order and `status` prints the weights and where they came from.

- **Deliver each generation as one reviewable branch with a lineage-written PR body** — FEATURE — value 4 — effort M — risk low — category: delivery
  Why: the user cares about what shipped to main (ship replays, standing publish grants), and a tower of docs is not a diff they can approve. Assumption: generation output is currently spread across tasks and lanes.
  Done when: a finished generation yields `genesis/gen-N` with one commit per closed scenario and a PR body listing scenarios closed, cost and what lost, and nothing lands on main without a yes.

- **Promote any ask repeated three times into a standing sweep** — FEATURE — value 5 — effort M — risk low — category: recurring asks
  Why: favicon, stale fm code section, site motion, demo and docs lag were each asked separately, though they are one class: "a surface drifted from the code". Surface-lag measurement (T-2073) covers this one class only.
  Done when: replaying the user's ask log creates a standing sweep after the third same-class ask, with its own exam scenario, and a fourth occurrence is caught before the user types it.

- **Mine friction digests and repeated nudges into gen-0 candidates** — FEATURE — value 4 — effort S — risk low — category: self-knowledge
  Why: the pack cites a friction digest where one nudge fired 33 times and the user dropped several. That is rich evidence of what the user does not want, and it is not used for the charter.
  Done when: a gen-0 draft lists NEVER candidates each citing a digest line, and dropped items never reappear as missions.

- **Give every tower doc three reading depths on the page** — FEATURE — value 4 — effort M — risk low — category: tower page
  Why: the user asked for every doc readable in full plus per-generation detail, and a full doc is a wall of text, which they asked to replace elsewhere. Assumption: the page currently shows full text only.
  Done when: each doc has a one-line, one-paragraph and full view, with the short forms generated and checked against the full text, and the choice persists per reader.

- **Answer "what's weakest right now?" from live tower state** — FEATURE — value 4 — effort S — risk low — category: query
  Why: the user steers by looking, and the tower has gap map, exam results and not-yet entries but no direct question interface. Assumption: today they must open files or the page.
  Done when: `fm genesis ask "what should I worry about?"` answers in at most five lines, each citing a scenario or ledger entry, with no tool calls to the model beyond one summarizing call.

- **Honor quiet hours and focus windows** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: auto-start and detached publish act while the user may be mid-edit. Assumption: no schedule signal exists today.
  Done when: with `quiet 09:00-18:00` set, no generation starts or publishes in that window and the deferral is logged with the time it will resume.

- **Wild: Import a taste rubric from three products the user admires** — FEATURE — value 4 — effort L — risk med — category: taste
  Why: wild. The user keeps asking for polish ("animated and well made", named looks, motion playbook), which is taste, not a checklist. Dropping three URLs or screenshots could produce rubric scenarios scored by a tool-less judge.
  Done when: three reference screenshots produce a rubric of at least 8 checkable UI criteria, and the exam fails a deliberately plain page on at least half of them.

- **Wild: A/B taste duels that train the rubric** — FEATURE — value 4 — effort M — risk low — category: taste
  Why: wild. When two rewrites tie on exam, show the two renders side by side and take one keystroke. Ties are exactly where "closes more scenarios" cannot decide.
  Done when: a tie renders two screenshots, one keypress picks a winner, and the pick is stored as a weighted preference reused in later tie-breaks.

- **Wild: Tap a node on the tower graph to say "more of this" or "less of this"** — FEATURE — value 3 — effort M — risk med — category: steering
  Why: wild. The live graph is already the user's favourite surface; making it a control surface turns watching into steering with no typing.
  Done when: tapping a mission node and choosing "less" lowers its priority in the next generation's Seed, and the page shows the change with the user's mark.

- **Wild: Let Genesis tell the user what they will ask next, then score itself** — FEATURE — value 3 — effort M — risk low — category: forecasting
  Why: wild. Blind-spot work shows eight asks nobody predicted. A weekly sealed list of "you'll probably ask for X" turns misses into a visible hit rate.
  Done when: a sealed list of five predictions is written before a week starts, graded against the week's real asks, and the hit rate is shown on status.

Next question: Which of the user's recurring ask classes (surface lag, polish, stale docs) would a fresh project's Genesis not see until it has months of history, and what stands in for it on day one?
Next question: When the user says "make this great", which single outcome do they feel first, and has anyone asked them?
