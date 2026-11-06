# Brainstorm — lens: what the user would notice and love

- **Show a "what I just did for you" receipt on every turn end** — FEATURE — value 5 — effort M — risk low — category: trust UI
  Why: assumption: the user watches the pane but can't tell at a glance what a long drive accomplished. Their pushback pattern (evidence quality, proof packs, tours) shows they want verifiable work. A one-glance receipt (files touched, criteria turned green, spend, anything refused or assumed) is what people show others.
  Done when: ending a drive turn renders a card listing changed files, criteria red→green counts, cost and open assumptions, and a test asserts each field is populated from the ledger.

- **Add a "refusal inbox" that collects every guard block and unmet gate as one list** — FEATURE — value 4 — effort M — risk low — category: guard UX
  Why: friction shows three guard false positives (`git stash list`, heredoc, read-only python) plus the user denying an rm. Blocks are scattered across turns. One place with reason code, "allow once" and "never block this" makes the guard feel fair, and it never weakens it.
  Done when: `fm refusals` lists the last N blocks with reason codes, and `fm refusals allow <id>` records a scoped, precise allow that a replay case then confirms.

- **Make `fm doctor` heal-on-sight with a before/after diff** — FIX — value 4 — effort M — risk med — category: reliability
  Why: four zero-byte git objects broke `git diff` and doctor passed. A doctor that finds the problem and offers a one-line repair, showing what moved aside, turns a scare into a non-event. Existing ideas cover detection. This adds a repair and a receipt.
  Done when: with an injected empty loose object, `fm doctor` reports it, `fm doctor --fix` moves it aside, and `git diff` works afterwards. A test covers it.

- **Ship "ask Foreman anything" over the ledger (`fm why`)** — FEATURE — value 4 — effort M — risk low — category: explainability
  Why: assumption: the user will ask "why did you do X?" once drives run unattended. Briefs, decisions, surprises and evidence already exist, so a stdlib lookup that joins them by file or task, with no model call, answers cheaply and with citations.
  Done when: `fm why <path>` prints the tasks, decisions and surprises that touched the file, each with an id, and returns "nothing recorded" otherwise.

- **Merge the overlapping inbox into three named pipelines and cut the rest** — CLEAN — value 4 — effort S — risk low — category: scope control
  Why: the inbox has about 20 planned items, and many overlap (bench judge, regression court, shadow-user soak, counterfactual ledger, skill duels). The user wants "groundbreaking", not a longer list. Proposal: a proof-and-judge pipeline, an interop pipeline, and a night-shift pipeline. Cut the dependency-release watch and lesson confidence until one of them needs them.
  Done when: the inbox holds ≤ 3 umbrella items with their members listed as steps, and the cut items are recorded as dropped with reasons.

- **Wild: Let the pane show the drive as a living map of the repo** — FEATURE — value 3 — effort L — risk low — category: delight
  Why: wild. `fmmap` already knows imports and impact. A pane that lights up the files being touched, with green and red halos from gate results, makes work visible and gives people something to screenshot.
  Done when: the UI view model emits per-file state (idle/editing/red/green) from the repo map, and a UI test renders at least one lit node.

- **Wild: Run a "dry-run drive" that rehearses the queue without edits** — FEATURE — value 4 — effort M — risk low — category: predictability
  Why: wild. Before a long unattended drive, simulate it: read each brief, predict tier, spend and likely stalls (missing verify commands, unverified assumptions, guard categories it will hit), then ask the user for the grants up front. This kills mid-drive waits, which are the top friction (18×).
  Done when: `fm drive --rehearse` prints per-task predicted cost and a list of guard categories needing approval, and makes no writes outside state.

- **Pre-request approvals bundle: ask once for the whole queue's grants** — FEATURE — value 4 — effort S — risk med — category: guard UX
  Why: approvals are per-context, so long drives stall on them. A single reviewed list of scoped grants, shown with the rehearsal, keeps the guard intact and removes the mid-drive nag. It needs explicit user yes, and nothing outward is ever included.
  Done when: the grants list is written only after the user confirms, each grant is scoped by command pattern and task, and an unlisted action still blocks.

- **Wild: Let Foreman write the user a weekly "what I learned about how you work" note** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Corrections, vetoes, drops and steers are already data. A short, private, editable summary ("you keep narrowing criteria to permanent checks; you deny deletes") lets the user confirm or correct the model of them, and feeds the veto and preference checks. It stays local.
  Done when: `fm me` prints sections generated from the ledger, each with a cited source, and a confirm or reject action updates the stored preference.

- **Wild: Add "undo this task" as one command with a verified rollback** — FEATURE — value 4 — effort L — risk high — category: safety net
  Why: wild. The tour, proof and per-task commits make a clean revert possible. `fm undo ID` reverts the task's commits in a lane, re-runs the gates from before, and proves the tree is back. That makes ambitious unattended drives feel safe to run.
  Done when: after a finished task, `fm undo ID --dry` lists the commits it would revert, and a real run in a throwaway repo restores the earlier tree with passing pre-task gates.

- **Cut or merge: drop "second-Foreman daily review" into the night-shift pipeline** — CLEAN — value 2 — effort S — risk low — category: scope control
  Why: it duplicates the standing transcript review and the shadow-user soak. Run it as a night-shift job, not its own feature.
  Done when: the inbox item is removed and the night-shift brief lists the daily review as a step.
