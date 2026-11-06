# Brainstorm — lens: grid

- **Follow a dissent across split, merged and reopened tasks** — FIX — value 4 — effort M — risk med — category: scoring
  Cell: dissent × unattended run × wrong. Why: assumption: the dissent score binds to one task id, but the pack shows `fm task` splits and lane merges, so a dissent on T-A would score against a task that no longer exists or against a merged outcome.
  Done when: a fixture where a dissented task is split in two and one half is reopened scores the dissent once, against the surviving ids, and `fm outcomes` prints the lineage.

- **Require a minimum detectable change on every outcome measure** — FEATURE — value 4 — effort S — risk low — category: exams
  Cell: Exam × agent × unclear. Why: the pack's open question is how many gen-3 measures are vacuous. A target with no noise floor passes by luck (a bench rise inside its own spread already needed T-2727).
  Done when: filing refuses an `outcome:` line without a direction, a unit and a smallest meaningful change, and a fixture with a bare "improve" is refused.

- **Render each Exam reading with its age and cause when it cannot be taken** — FEATURE — value 3 — effort S — risk low — category: web UI
  Cell: web UI × user × missing. Why: the pack asks whether an unmeasurable snapshot should be "unmeasured" or block. The web UI is the only listed surface, and it has no state for "could not read".
  Done when: with the service stopped, the card shows "unmeasured since <time>: <reason>" and never green or red.

- **Time-shift every Exam reading across a clock jump and a timezone change** — FIX — value 3 — effort M — risk low — category: correctness
  Cell: Exam × unattended run × wrong. Why: assumption: windowed gauges and 14-day survival use wall time, and the drive runs through suspend. A reading near a boundary can flip.
  Done when: a test that replays one ledger under three clocks gives one verdict, or labels the reading "clock-dependent".

- **Warn when a hook-injected Exam note exceeds what the agent will read** — PERFORMANCE — value 3 — effort S — risk low — category: context
  Cell: hooks × agent × slow. Why: every brief now carries two more lines. T-2727 shows the hook p95 is already watched.
  Done when: `bench_hooks.py` includes a brief with the new Exam lines and fails if p95 rises past the spread.

- **Quote the user's own sentence next to each canary hit** — FEATURE — value 3 — effort S — risk low — category: grounding
  Cell: CLI × user × unclear. Why: assumption: a "nearest existing thing" line is hard to judge without the words it was matched to. Several drops here were "already built" cases.
  Done when: each canary line prints the matched clause and the existing verb, and a test checks both appear.

- **Block an Exam reading that writes to the tree it measures** — SECURITY — value 4 — effort M — risk med — category: safety
  Cell: Exam × other agents (lanes) × unsafe. Why: the guard refuses interpreter writes to Foreman's files (fmguard.py:292), but a live-state command in a lane can touch the lane's own worktree and change what it reads.
  Done when: a reading that creates a file in the repo exits "not read-only" and files nothing.

- **Hand a fresh builder only the Exam and one dissent, then score whether they agree** — FEATURE — value 3 — effort M — risk med — category: agents
  Cell: brief × other agents × unclear. Why: assumption: a brief only the author can read fails when a lane or a post-compaction session builds it.
  Done when: a cold child restates the Exam's pass condition and a mismatch with the filed text is recorded as a brief defect.

- **Show Mission pages read-only on a no-JavaScript fallback** — FEATURE — value 2 — effort S — risk low — category: site
  Cell: site × user × missing. Why: assumption: `site/genesis/index.html` loads data that `fm genesis live` publishes. A failed fetch likely shows a blank page.
  Done when: with scripts blocked, the page shows the last published Mission list and its date.

- **Wild: Pull the "stale tab" test into the grid** — FEATURE — value 3 — effort M — risk low — category: web UI
  Cell: web UI × unattended run × unsafe. Why (wild): a page left open overnight shows a green Exam that was true yesterday.
  Done when: a tab loaded before the last ledger write shows a dimmed card and refuses one-click actions.

- **Wild: Have a hostile lane try to pass its own Exam without work** — SECURITY — value 4 — effort L — risk med — category: exams
  Cell: Exam × agent × unsafe. Why (wild): the pack's Goodhart worry is real, because the builder writes the code the reading measures. A contest finds gameable measures before the user does.
  Done when: a planted vacuous Exam is satisfied by the adversary in a fixture and the filer flags it.

- **Wild: Keep a one-screen "empty cell" postcard in the pane header** — FEATURE — value 3 — effort S — risk low — category: delight
  Cell: pane × user × unclear. Why (wild): the left-out list is easy to forget; one rotating cell at a time is a small daily nudge.
  Done when: the header shows one empty cell with its sting and the command to act on it, and cycles daily.

**Cells left empty:** hooks × user × unsafe and web UI × agent × slow. The guard and web UI already carry those faults, and I found no evidence of a gap. Site × anyone × unsafe is also empty because the site is static and its leak scan exists (a prior idea).

Next question: which dissent in gen 1–3 was tied to a task that was later split, merged or reopened?
Next question: does any Exam live-state command in the filed briefs write anything when run twice?
