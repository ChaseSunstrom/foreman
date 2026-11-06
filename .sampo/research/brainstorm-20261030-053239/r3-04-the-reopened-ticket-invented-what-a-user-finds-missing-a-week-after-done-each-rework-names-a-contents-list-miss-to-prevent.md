# Brainstorm — lens: the reopened ticket (invented): what a user finds missing a week after done; each rework names a contents-list miss to prevent

Answering one earlier question through this lens: Initiative acts on repos nobody asked about, so its day-2 satellites are a per-repo off switch, a purge of everything it left behind, a spend cap shown beside the result, and an owner check. Those are lifecycle rows, which ideas 1, 3 and 4 below make mandatory.

- **Add a day-2 axis to the coverage grid** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: coverage.md is capability × verb × surface, so it stops at the first use. A reopen is usually a later life-stage: upgrade, turn off, undo, purge, recover, explain, scale. Assumption: most reopens fall into about eight such stages.
  Done when: `fm genesis check` fails a capability whose grid lacks a filled or reasoned-n/a cell for each of the eight stages.

- **Enumerate every lister, then check the new object appears** — FEATURE — value 5 — effort M — risk med — category: integration
  Why: the earlier Mission shipped "pane line, MCP, site, MASTER" as a late brief, a sign of a miss class (an object missing from status, export, doctor, purge). Assumption: listers can be found by grepping for functions that walk `tasks/`, the ledger or the briefs.
  Done when: a fixture adding a new object kind makes `fm goal close` list each existing enumerator that doesn't mention it.

- **Require an old-state fixture for any goal that touches stored state** — FIX — value 5 — effort S — risk low — category: migration
  Why: "unit tests missed shapes the live run hit (a table-less seed)". Assumption: a copy of the previous release's state dir can be committed as a fixture.
  Done when: a goal that changes a state schema can't finish without a test that opens the prior-release fixture and passes.

- **Diff the footprint before and after the done-when run** — FEATURE — value 4 — effort M — risk low — category: cleanup
  Why: nothing checks the files, worktrees, branches and ledger events a capability leaves behind. Assumption: users reopen with "what is this leftover file, and how do I remove it?"
  Done when: close prints a footprint list, and each entry names its purge command or is marked intentional.

- **Mine mistyped commands into aliases and hints** — FEATURE — value 4 — effort M — risk low — category: discoverability
  Why: the user's phrasings ("put/init", "live on", "seal") show a vocabulary that differs from the CLI's. Failed `fm` invocations are visible to the hooks. Assumption: the failures can be logged locally.
  Done when: an unknown subcommand typed twice appears in `fm doctor` with the nearest real command, and an accepted alias works.

- **Lint new numeric caps in the diff into settings or justifications** — CLEAN — value 4 — effort S — risk low — category: configuration
  Why: caps like "at most 3 a day", DRIVE_MAX and "2 dry rounds" recur, and users ask to change them. Assumption: the user will want each cap tunable.
  Done when: a diff adding a bare cap literal fails review until the cap reads from a named setting shown in `fm settings`, or carries a "fixed because…" line.

- **Hold a reopen reserve in the plan's budget** — FEATURE — value 3 — effort M — risk med — category: budgeting
  Why: reopens currently arrive as unplanned asks, as T-2120 to T-2127 did. Assumption: past reopen rework per goal size can be measured from the ledger.
  Done when: a goal's plan shows a reserved share, and a done goal with no reopen in its window releases it, both visible in `fm goal`.

- **Add an output-for-scripts row to every new verb** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: an unasked need is scripting; the user already chains `fm` through hooks and MCP. Assumption: `--json` and documented exit codes are missing on some verbs.
  Done when: a test walks the verb table and fails on any new listing verb without `--json` and a documented exit code.

- **Infer silent reopens from post-done churn** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: existing reopen detection reads the user's words. Many reopens are just a later task editing a done goal's files within a week. Assumption: file ownership per goal can be recovered from task evidence.
  Done when: an edit to a done goal's files within 14 days, under an unrelated task, files a suspected reopen citing the goal's contents list.

- **Wild: Replay a recorded first-use cast against HEAD** — FEATURE — value 3 — effort M — risk med — category: docs
  Why: assumption: docs rot because nothing re-runs the first-use walkthrough. At close, record the exact commands and outputs; a weekly job replays them against the current tree and flags drift.
  Done when: changing a command's output makes the weekly replay fail and name the cast and line.

- **Wild: Put a day-7 persona through the CLI before done** — FEATURE — value 3 — effort L — risk med — category: planning
  Why: assumption: a tool-less model given the user's own words, recent steers and the new help text can ask its first five follow-ups. Each must map to a contents row or the cut list, or the goal can't close.
  Done when: five persona questions appear in the closing receipt, each with its mapped row.

- **Wild: Keep a regret ledger of what each cut line cost later** — FEATURE — value 3 — effort S — risk low — category: scope
  Why: the cut list exists as an idea, but a cut is never scored. If a cut line reopens, its class gets a higher default for the next plan.
  Done when: reopening a cut line writes a regret event, and the next plan of the same capability class keeps the line by default.

Next question: Which reopen classes are caused by the user changing their mind rather than by a miss, and how does the ledger tell them apart before the planner learns from them?
Next question: What is the smallest day-2 stage list that would have caught every ticket in the "earlier brainstorms missed" list, and does it hold for the next eight?
