# Brainstorm — lens: deepen: coverage

- **Build a cell compiler that emits coverage.md from a rule table plus a trace corpus** — FEATURE — value 5 — effort L — risk med — category: coverage
  Why: five earlier ideas converge on "rule table, not 58 sentences"; combined with live deliberation traces it makes every cell a derived row (capability × surface × stage → file:line or n/a + counterexample grep), so templating is impossible by construction.
  Done when: `fm genesis coverage --compile` regenerates all 58 Exhaustive-thinking cells, each with a resolvable reference of ≤140 chars, and the templated/duplicate check reports zero.

- **Add a cell-triage pass that tags each empty cell existing / gap / n/a with its proof before any prose** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the Lesson from Missions 3 and 4 says most of #11 and #12 were already built; the standing rule says an n/a counts only if it is recorded. Triage first avoids building what exists.
  Done when: a triage file lists all 58 cells with a verdict and a grep or file reference each, and the verdict counts are printed by `fm genesis check`.

- **Turn every gap cell into a probe scenario for the exam's tool-less child** — FEATURE — value 4 — effort M — risk med — category: coverage × exam
  Why: the standing rule wants weakness-finding from signals Foreman didn't author. A cell becomes real when a child-authored scenario exercises it, and the exam already has the machinery.
  Done when: each gap cell links to a scenario id, and `fm exam scorecard` groups results by coverage cell.

- **Make "reach" a column: each cell names the session path that calls its capability** — FEATURE — value 4 — effort S — risk low — category: coverage × reach
  Why: the reach standing rule fails capabilities that exist only as verbs, and the open questions ask which trigger verbs no session path calls. A cell without a caller isn't covered.
  Done when: `fm genesis check` flags any cell whose reach field names no hook, skill, drive step or tick, and the 58 cells show zero such flags or an explicit gap.

- **Add unattended-and-no-user stage columns to the grid** — FEATURE — value 4 — effort M — risk low — category: coverage × unattended
  Why: the left-over questions ask which steers assume an interactive session and which unattended failures leave no trace. Stages today are plan/act/verify; "runs with nobody present" and "user returns after a week" are missing.
  Done when: the grid has both columns for Exhaustive thinking, each filled with a file reference, an n/a with proof, or a filed gap task.

- **Link each cell to a depth-scaling check: S tasks must not pay L costs** — FEATURE — value 4 — effort M — risk med — category: coverage × cost
  Why: the capability text says to scale depth to risk. A cell in the S-task column must show the deliberation actually shrinks, measured in tokens or seconds from the ledger.
  Done when: `fm cost` reports deliberation tokens per task tier, and the S column cells cite a number at or below a stated threshold.

- **Shadow-fill with two independent fillers and file their disagreements as gap candidates** — FEATURE — value 4 — effort M — risk low — category: coverage × verification
  Why: the cold-read rule needs a second view. Where a Haiku filler and a Sonnet filler disagree on existing vs gap, someone is wrong, and that is where the sweep's tasks should start.
  Done when: running both fillers yields a disagreement list, each item resolved by a grep-backed verdict recorded in the cell.

- **Store only exceptions: compute the grid live from the repo and diff it against a pinned snapshot** — CLEAN — value 4 — effort L — risk med — category: coverage × drift
  Why: the hand-written coverage.md rots as code changes (T-2532 and T-2536 changed what exists). Live computation turns rot into a visible diff at `fm ship`.
  Done when: `fm genesis sweep` fails when a cited file or symbol in a cell no longer resolves, naming the cell.

- **Wild: Let a stubborn-reader child try to prove each filled cell false** — FEATURE — value 4 — effort M — risk low — category: coverage × adversarial
  Why: wild. A child that sees only the cell text and the repo and tries to find the named capability failing catches cells that sound grounded but aren't, which is the weakness the "cells must be real" steer targets.
  Done when: each cell has a "survived challenge on <date>" mark, and one planted fake cell is caught in a test.

- **Wild: Refuse the 59th cell unless an existing one is retired or merged** — CLEAN — value 3 — effort S — risk low — category: coverage × lean
  Why: wild. This ties the lean-substance rule to the grid, so coverage can't grow by sprawl, and cells that merge show which capabilities were really one.
  Done when: adding a cell past the cap fails `fm genesis check` unless the same change removes or merges one, with the reason recorded.

- **Wild: Have a tool-less child compress the 58 cells into the distinct capabilities they really are** — FEATURE — value 3 — effort S — risk low — category: coverage × dedupe
  Why: wild. If 58 cells collapse to about 20 distinct capabilities, the rest are the same idea at different surfaces, and the template-detection rule is satisfied honestly instead of by rewording.
  Done when: the child returns a clustering, and every cluster of 3 or more cells gets a shared reference or a recorded reason they differ.

- **Replay a cell as a scar: record the real incident that proves its capability matters** — FEATURE — value 3 — effort M — risk low — category: coverage × evidence
  Why: grounding in "has the failure ever happened (ledger, decisions.md)" from the Lesson. A scar count tells the next Seed which cells guard something real and which are speculative.
  Done when: each cell shows 0 or more linked ledger entries, and the Seed's ranking cites the scar counts.

Next question: Which of the 58 cells would still be empty if the standing "n/a needs a counterexample search" rule were enforced, and are those the true gaps?
Next question: Does anything in the sweep verify that a filled cell's cited file still behaves as claimed after later generations change it, or only that the file exists?
