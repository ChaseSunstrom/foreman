# Brainstorm — lens: the reopened ticket (invented): what a user finds missing a week after done; each rework names a contents-list miss to prevent

- **Open a reopen ticket as a typed object** — FEATURE — value 5 — effort M — risk low — category: goal ledger
  Why: gap map lists no record of what happens after done; earlier ideas log "post-done additions" and "reopens" but none gives the reopen its own file linking back to a contents row. Assumption: reopens today surface as new T- tasks with no link to the goal.
  Done when: `fm reopen <goal> "<words>"` writes a ticket with fields (goal id, missing-item text, cause class, surface) and `fm goal show` lists it under the goal; a test proves a reopen with no matching contents row is flagged "unlisted miss".

- **Classify each rework by the question that would have caught it** — FEATURE — value 4 — effort M — risk low — category: miss taxonomy
  Why: the pack's "what earlier brainstorms missed" list is a flat list of eight asks; the user never learns which question class they belong to (consent, surface, cost, recall floor). Assumption: classes are few enough to enumerate (~10).
  Done when: each reopen carries a `question:` line from a fixed list, and `fm goal misses` prints counts per class; an exam scenario with a planted miss gets the expected class.

- **Run the contents list through the sibling-capability grid before sealing** — FEATURE — value 5 — effort M — risk med — category: completeness
  Why: Mission 3's briefs T-2120..2127 were each a satellite (exam repair, surfaces, ranking) that the first plan didn't list; the pack's questions ("which satellites would Initiative need that Genesis never had") say the same. Assumption: coverage.md's capability × verb × surface grid can be reused per goal.
  Done when: sealing a goal's contents fails if any cell of the grid is neither a row nor an explicit "n/a: reason"; the Mission 3 goal replayed through it yields the T-2120 class of row.

- **Ask "what did the last done goal need afterwards?" at plan time** — FEATURE — value 4 — effort S — risk low — category: planner prior
  Why: reopens repeat in shape (surfaces, exam repair, docs); a new goal's plan should inherit rows from the previous goal's reopens. Assumption: reopens are stored per project as above.
  Done when: planning a goal prints "inherited from reopens: N rows" with source tickets, and a test shows a prior reopen's row appearing in a new goal's draft.

- **Hold every done in a 14-day reopen window, then close it** — FEATURE — value 4 — effort S — risk low — category: warranty
  Why: "done" is final at once today; the user finds gaps a week later. Assumption: a warranty state can sit between done and sealed without breaking `fm task finish`.
  Done when: a goal shows `done (warranty to 2026-11-13)`, a reopen inside the window attaches to it, and a quiet window flips it to `closed` with a ledger event.

- **Reopen by user correction detection** — FEATURE — value 4 — effort M — risk med — category: signals
  Why: the user's "steered" lines ("widened — the live rerun showed…") are reopens in disguise, made as plain steers. Assumption: UserPromptSubmit can match a steer against a done goal's nouns.
  Done when: a prompt naming a done goal's item opens a draft reopen (proposed, never auto-filed) with the matched contents row, tested on three recorded steers.

- **Replay the reopen as an exam scenario automatically** — FEATURE — value 5 — effort L — risk med — category: exam
  Why: the exam grades capabilities only on child-authored kinds; every real reopen is a free, true-to-life scenario (the pack: "make the miss the next exam scenario"). Assumption: a reopen can be reduced to a planted missing row in a finished plan.
  Done when: `fm exam add --from-reopen R-NNN` creates a scenario whose pass condition is that the planner lists the missed row, and it enters the holdout split by hash.

- **Show "reopen rate" per goal size on the pane** — FEATURE — value 3 — effort S — risk low — category: surface
  Why: nothing shows whether the planner is improving; the exam grades only held-out kinds. Assumption: reopens per contents row is a stable metric.
  Done when: the pane and site show reopens ÷ rows for the last 10 goals, and the number is computed from ledger events only.

- **Wild: Send in a ghost newcomer at day seven** — FEATURE — value 4 — effort L — risk med — category: ghost user
  Why: wild; a cold, tool-less agent reads only README/CHANGELOG/site page and tries to use the shipped capability the way the user's words describe, filing every friction as a candidate reopen. Assumption: docs and the user's original words are enough to drive it.
  Done when: a seeded goal with a missing surface gets a ghost report naming that surface, and a goal that has the surface gets none.

- **Wild: Write the reopen the user will file before they do** — FEATURE — value 4 — effort M — risk med — category: pre-mortem
  Why: wild; at done, a cold model drafts three likely reopen tickets in the user's own phrasing, using past reopens as examples; each draft is checked against the diff and either fixed or listed as a known gap. Assumption: past reopens give enough style data.
  Done when: done prints "predicted reopens: 3, resolved: 2, open: 1", and over replayed history at least one prediction matches a real reopen.

- **Wild: A reopen autopsy page that grows a museum** — FEATURE — value 3 — effort M — risk low — category: site
  Why: wild; the site already has a Genesis page; a page per reopen with its goal, missed row, cause class and the rule it produced makes the planner's learning visible. Assumption: reopens contain no private text, so they can be published after scrubbing.
  Done when: `fm genesis export` emits a page per reopen with scrubbed text, and the page links to the rule it created.

- **Scrub and pool reopens across projects into a prior** — FEATURE — value 3 — effort M — risk med — category: privacy
  Why: one project's reopens are few; the miss classes are the transferable part. Assumption: stripping literals leaves only the class and surface.
  Done when: a test shows a reopen's file paths and quoted words absent from the pooled record, and a second project's draft contains the pooled class row only if its stack matches.

- **Make a reopen's own fix require a listed row first** — FIX — value 4 — effort S — risk low — category: discipline
  Why: Mission 3 shows repairs filed as new tasks (T-2120) with no mark on the goal's list, so the same hole stays open for the next goal. Assumption: briefs can carry a `goal_row:` field.
  Done when: `fm task finish` on a reopen-linked task fails until the goal's contents list contains the row, and the failure message names it.

Next question: When a reopen is really a new want rather than a missed row, how does the ledger tell them apart without asking the user?
Next question: Does a lesson learned from reopens ever need to be unlearned, and what shows that a prior row now only pads?
