# Brainstorm — lens: capability map

- **Ingest a PRD, ticket or pasted spec as a goal source** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: assumption: users arrive with Linear, Jira or GitHub issue text, or a pasted PRD, not a vague sentence. Every listed intake idea starts from a sentence. Rivals such as Kiro, Spec Kit and Copilot Workspace start from a document.
  Done when: a fixture PRD with 3 planted contradictions yields contents rows plus an ambiguity list naming all 3, each quoted from the source.

- **Write a column charter with one worked example and one non-example per stage** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the pack's rules count a cell only if it is concrete and not templated, but fillers and cold readers are never shown what "concrete" means per stage. Each column needs a canonical filled cell and a rejected one.
  Done when: `coverage.md` links a charter file with 2 samples per stage, and the filler and cold-read prompts both embed it.

- **Run a row-zero "clean clone builds and tests" check before a plan is accepted** — FEATURE — value 4 — effort S — risk low — category: plan gate
  Why: the pack has a fresh-clone replay only at finish, and a red baseline snapshot. A multi-day goal that starts on a repo that cannot build wastes day one.
  Done when: a fixture repo with a broken install step makes plan accept print "row 0 red: <command, exit code>" and add a first row to fix it.

- **Turn non-functional budgets into measured contents rows** — FEATURE — value 4 — effort M — risk med — category: finish
  Why: a best-in-class version has a startup time, bundle size, hook p95 and page weight. The pack's budgets are Foreman's own lean ratchet, not rows a user's goal carries.
  Done when: a goal with "page loads fast" gets a row "p95 < N ms, baseline M ms recorded at plan time" and finish fails if no measurement ran.

- **Build a journey matrix (persona × journey × state)** — FEATURE — value 4 — effort M — risk med — category: completeness
  Why: the pack covers a sealed demo script and rival parity tables, but not a grid of journeys against empty, loading, error and first-run states. Those are the usual gaps in the "finished" version a user judges.
  Done when: a goal with a UI lists its journeys with a state per cell, and an empty state with no row or no n/a reason blocks "finished".

- **Inventory every setting, flag and env var a goal adds** — FEATURE — value 3 — effort S — risk low — category: docs/settings
  Why: a complete product has defaults, docs and a doctor check for every knob, and the pack's inventory ideas stop at triggers. A knob added mid-goal is a classic undocumented leftover.
  Done when: `fm goal finish` diffs the config surface against the plan's start commit and lists any new key lacking a default, a doc line or a test.

- **Add a Now/Next/Later portfolio page across goals** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the pack has arbitration between two live goals, a WIP limit and a parked shelf, but nothing shows all goals together as a roadmap. Linear and Basecamp offer that view.
  Done when: the web UI lists live, parked and finished goals in three lanes, each with its stop reason and last-touched age, drawn from files only.

- **Audit licences and notices for what a goal added** — SECURITY — value 3 — effort S — risk low — category: ship
  Why: the pack covers supply-chain diffs and found tools, but not a licence and NOTICE check when a goal vendors or adopts code. Finishing a feature this way can silently break the project's own licence.
  Done when: a fixture goal that vendors a GPL file into an MIT repo fails finish with the file and licence named.

- **Let a goal declare no-ship windows** — FEATURE — value 2 — effort S — risk low — category: scheduling
  Why: assumption: users don't want the end-of-goal ship on a Friday night or while they are travelling. The pack's calendar idea only covers away mode, not holding a ship.
  Done when: with a window set, `fm ship` on that goal refuses with the window's end time, and a user-only override exists.

- **Wild: Hold a "newcomer's first hour" scoring run of the finished goal** — FEATURE — value 4 — effort L — risk med — category: finish
  Why: wild. A tool-less child gets only the README and the finished repo and must perform the goal's headline journey. Its failed steps become the last rows. Rival lists have docs checks, but none score an unfamiliar user's attempt.
  Done when: a seeded README with one missing install step makes the child's run fail at that step, and finish cannot close until that row is fixed.

- **Wild: Compile "finished" into a changelog the user can sign** — FEATURE — value 3 — effort M — risk low — category: finish
  Why: wild. At plan time, write the release note the finished version will earn, one line per row. At finish, diff the promised note against what shipped and have the user strike any line they no longer want. This is the press-release idea turned into a checkable contract.
  Done when: finish prints promised versus delivered lines and refuses "done" while a promised line has no closed row.

- **Wild: Rank rival products' public issue trackers into candidate gaps** — FEATURE — value 3 — effort L — risk med — category: capability map
  Why: wild. The capability-map lens leans on the model's memory of rivals. Their open issues are real, current gaps, and they also show which "complete" features users actually complain about.
  Done when: a refreshed cache of 3 named rivals' top-voted issues yields at least 5 candidate rows, each with a source link, filtered against what is already built.

- **Lint that every cell's cited verb is reachable from a session path, per harness** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: this answers the earlier questions on harness dependence and unread outputs. The pack suggests a harness field per probe, but nothing derives it mechanically from hook registration, so cells could cite Claude-only paths by accident.
  Done when: the sweep prints per-cell reach for Claude Code, `fm code` and hookless harnesses, and flags any cell that is Claude-only without saying so.

Next question: Which capabilities does a cold newcomer never discover because no surface mentions them, even though the cell for them is filled?
Next question: Of the 58 cells, which would a rival's users also expect, and which are only meaningful for Foreman's own discipline model?
