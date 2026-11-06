# Brainstorm — lens: grid

Surfaces here are the web UI and the CLI it reads from. Actors are the user, the agent, other agents (lanes) and the unattended run. The failure modes are missing, wrong, slow, unsafe and unclear. I skipped cells the "ideas so far" list already fills.

- **Re-score every dissent at +7 and +30 days, attributed by file overlap** — FEATURE — value 4 — effort M — risk low — category: dissent
  Cell: unattended run × wrong.
  Why: the carried gap is "dissents scored against outcomes". A score taken at close misses regressions that surface a week later, and credits or blames a dissent for changes in files it never touched. Assumption: dissent records name the files they concern.
  Done when: a seeded dissent whose files regress on day 8 flips from "vindicated" to "unscored: no overlap" or "vindicated late", and `fm outcomes` prints both horizons.

- **Require the Exam's outcome measure to read differently on the parent commit** — FIX — value 5 — effort M — risk low — category: briefs
  Cell: agent × wrong.
  Why: the carried gap says every brief's Exam names an outcome measure. A measure that reads the same before and after the change is vacuous. Filing should run it against the parent tree.
  Done when: filing a brief whose outcome command returns an identical value on HEAD and HEAD~ is refused, naming the command and both values.

- **Stamp each live-state reading with state dir, uid, home and host** — FIX — value 4 — effort S — risk low — category: briefs
  Cell: unattended run × wrong.
  Why: a "live-state reading" taken in a scratch home or under another uid can pass as live. Earlier ideas bind a reading to the checkout; none bind it to the state directory.
  Done when: a reading taken with `HOME` pointed at a scratch dir is shown as "scratch, not live" and cannot satisfy a brief's live line.

- **Run a tombstone canary before "not built" is claimed** — FEATURE — value 4 — effort S — risk low — category: canaries
  Cell: agent × missing.
  Why: the canary-near-the-idea gap. Earlier canaries look for existing features. A canary over drops, reverts, removed verbs and not-yet.md finds ideas that were built and then rejected.
  Done when: an idea matching a dropped item prints "dropped T-nnnn: reason" beside the "not built" claim.

- **Open every Mission page with a one-line interpretation and its outcome in checkable words** — FEATURE — value 4 — effort S — risk low — category: clarity
  Cell: web UI × user × unclear.
  Why: assumption: the user can't tell which reading of "exhaustive thinking" was taken, or how they would check it. Scope width is recorded, but not shown as a sentence.
  Done when: the web UI page for a Mission has a first line reading "I took this to mean … ; you can check it by …", and a test fails if the line is empty.

- **File unmeasurable outcomes as dated bets** — FEATURE — value 3 — effort M — risk low — category: briefs
  Cell: user × missing.
  Why: some outcomes have no data yet, and a hard Exam rule would block those briefs or push people to invent a measure. A third state with a collection date keeps them honest.
  Done when: a brief with `outcome: bet until 2026-12-01 (collect X)` files, is counted apart from measured briefs, and surfaces on that date as "unsettled".

- **Show the grid delta between Missions** — FEATURE — value 3 — effort M — risk low — category: coverage
  Cell: web UI × user × unclear.
  Why: the coverage claim "N cells filled" says nothing about movement. A delta shows which cells flipped, which were newly created, and which went stale.
  Done when: the Mission page lists cells that changed since the previous Mission, in three groups: filled, emptied and new.

- **Require every actor row to hold one filled cell before a Mission closes** — CLEAN — value 3 — effort S — risk low — category: coverage
  Cell: other agents × missing.
  Why: the surfaces line names only the web UI, so the "other agents" and "unattended run" rows are the likeliest to stay blank without anyone noticing. Briefs skew toward the user and agent rows.
  Done when: closing a Mission with an empty actor row is blocked unless the row carries a recorded n/a with a reason.

- **Run Exam live-state commands in a no-write, no-network sandbox** — SECURITY — value 4 — effort M — risk med — category: exam safety
  Cell: other agents × unsafe.
  Why: a lane or child authors the Exam command, and a read-only classification by regex can be fooled by a command that writes. Running it under a sandbox makes read-only true by construction.
  Done when: an Exam command that tries to write to the state dir or open a socket fails inside the sandbox and the brief is refused.

- **Wild: let the dissenter stake budget on its dissent** — FEATURE — value 3 — effort M — risk med — category: dissent
  Cell: agent × wrong.
  Why: assumption: dissents are cheap to write, so they are noisy. A dissenter lens that is vindicated by the outcome earns extra lens budget in the next round; one that is overruled and wrong loses some.
  Done when: lens budgets in the next `fm ideas` run differ by prior dissent score, and the shift is printed.

- **Wild: send a pre-mortem postcard dated 30 days out** — FEATURE — value 3 — effort S — risk low — category: briefs
  Cell: user × unclear.
  Why: each brief writes how it expects to fail, with a live-state predicate. If the predicate matches on the date, the web UI shows the postcard. The user gets an advance warning in their own terms.
  Done when: a seeded brief whose failure predicate becomes true shows its postcard on the web UI, and one whose predicate stays false does not.

- **Wild: have a screenshot-only child reconstruct what was left out** — FEATURE — value 3 — effort M — risk low — category: exhaustive
  Cell: web UI × user × missing.
  Why: a tool-less child sees only screenshots of the Mission page and lists what it thinks the request skipped. The list is diffed against the left-out receipt. Anything it names that the receipt doesn't is a presentation gap.
  Done when: the diff is stored per Mission, and a seeded omission hidden from the page shows up as a mismatch.

**Cells left empty**
- **Web UI × any × slow:** earlier ideas on render budgets, streaming and last-good snapshots already fill it.
- **Unattended run × unsafe:** the caps, grants and guard ideas fill it.
- **Web UI × agent × missing:** a read-only page has nothing an agent needs that `--json` doesn't already give.

Next question: which briefs filed under Genesis gen 3 carry an outcome measure that the dissent score could actually be computed from, and how many are vacuous?
Next question: when the user reads a Mission page, which cell do they open first, and does the grid order match it?
