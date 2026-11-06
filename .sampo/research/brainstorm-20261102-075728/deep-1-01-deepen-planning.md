# Brainstorm — lens: deepen: planning

- **Ground the plan in a Plan Ledger that outlives sessions** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: the request is "carry the plan over days, across crashes and compactions"; the capability matrix, build/adopt/skip, hoisted rows and omissions list are separate ideas with no single stored unit. Assumption: no one-record-per-row store exists (T-0826 round ledger is deferred, a nearby pattern).
  Done when: killing a session mid-plan and restarting shows `fm plan show` with every row's state (survey, decision, omissions, owner task) unchanged.

- **Merge matrix, decision and omissions into one row schema** — CLEAN — value 4 — effort S — risk low — category: planning
  Why: assumption: separate lists drift. One row holds tool-source, capability, verdict (build/adopt/skip), reason, and a "deliberately omitted" flag; a skip without a reason is invalid.
  Done when: `fm plan check` rejects a row with a verdict but no reason, and an omission with no named source tool.

- **Close the plan by completeness evidence, not by running out of rows** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: the user wants it to know when it's "actually done rather than merely stopped"; capture-recapture and consensus/disputed-fringe are listed but unlinked. Combine: two independent surveys, overlap gives a coverage estimate, disputed fringe rows stay open until adjudicated.
  Done when: `fm plan done` refuses while estimated coverage is below a set bar or any disputed row is unadjudicated, and prints the numbers.

- **Tie each plan row to a falsifiable done-check at planning time** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: standing rules favor commands actually run; the user's own asks keep including DONE-WHEN lines. A row without a check command is a wish. Pairs with "drop rows smaller than one commit".
  Done when: `fm plan` rejects a row lacking a runnable check, and a row's check flips green only from a real run's output.

- **Re-plan on drift with a plan-vs-reality diff** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: the user's steers repeatedly re-scope tasks after reading code (T-2341, the fifth BEYOND row). Compare each row's grounding file/line to current HEAD at session start; stale rows are flagged, which absorbs "refuse to plan from a stale map".
  Done when: editing a file named in a row's grounding makes the next session start list that row as stale with the changed lines.

- **Order rows by dependency and expected value, and show the critical path** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the request says "decomposed and ordered"; fm next picks tasks today but the pack shows no plan-level ordering. Hoisted shared rows get priority because they unblock several goals.
  Done when: `fm plan order` prints a topological order where each hoisted row precedes all its dependents, and a cycle is reported.

- **Gate public names on a prior-art and namespace check inside the plan** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: the list has "check names" and "gate goal birth on prior art"; merge them into one step run before a goal is created (package registries, GitHub, existing `fm` verbs).
  Done when: creating a goal named like an existing fm verb or a taken package warns and requires an override reason.

- **Cap plan churn with a settling measure before build starts** — PERFORMANCE — value 3 — effort S — risk low — category: planning
  Why: assumption: replanning loops burn budget. Count rows added/removed/changed per revision; building is blocked while churn exceeds a threshold across the last two revisions.
  Done when: `fm plan` shows churn per revision and `fm drive` refuses to start rows while it is above threshold.

- **Score plan quality against outcomes and feed it back** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: bets and Brier calibration exist; plans don't. Record each plan's predicted rows/effort, then compare to what shipped, which rows were never needed, and which were added late. The result tunes the next plan's size cap.
  Done when: `fm outcomes --judgment` has a "plan" kind with a Brier for row-needed predictions.

- **Wild: rehearse the weakest row with a cheap model before committing** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. Pick the row with lowest confidence, have a Haiku child attempt it in a scratch worktree, and record where it stalled; the stall reveals missing sub-rows.
  Done when: a rehearsal record is attached to the row and at least one sub-row or note is added from the failure.

- **Wild: write the regret letter and the future README first** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: wild. A tool-less child writes the user's regret letter ("six months on, I wish it had...") and the finished README as a diff target; every sentence must map to a plan row or be flagged as a gap.
  Done when: `fm plan` lists unmapped README/letter sentences as candidate rows.

- **Wild: let a vague goal marinate overnight, then ask one question** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild; fm night already ticks unattended. The tick runs surveys and drafts with zero questions, and the morning session shows the draft, struck-through assumptions, and at most one question.
  Done when: a goal filed in the evening has a drafted plan with an assumptions list waiting at next session start, and no question was asked in between.

- **Wild: import any pasted plan and own only carrying and finishing** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: wild. Parse a plan from any chat into rows, attach checks and grounding, and flag rows lacking them rather than rewriting the plan.
  Done when: pasting a numbered plan creates rows with missing-check warnings and the plan can be carried to done.

Next question: Which plan rows has the user historically dropped or rewritten after seeing them, and can that rate set the size cap instead of a guess?
Next question: When a plan says done and the user disagrees a week later, what was missing, and was it a row the survey never listed?
