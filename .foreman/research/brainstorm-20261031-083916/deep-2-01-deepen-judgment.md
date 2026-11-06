# Brainstorm — lens: deepen: judgment

- **Decision ledger with a one-command undo** — FEATURE — value 5 — effort M — risk low — category: judgment
  Why: Mission 5 says "decides and records"; the list has "log every decision with a one-line undo" but nothing ties it to a surface. Each autonomous decision becomes a row (question, readings, pick, confidence, door type, undo command) shown on every surface, and `fm decision undo ID` reverts what it can.
  Done when: after a task makes 3 autonomous choices, `fm decisions` lists all 3 with confidence and undo, and undoing one restores the prior file or state in a test.

- **Door classifier from the guard's own rules** — FEATURE — value 5 — effort M — risk med — category: judgment
  Why: the guard already knows which commands are destructive (push, force, rm, mandate set); reuse that table to tag every plan step one-way or two-way instead of building a new classifier. Merges "classify by door type", "reversible vs irreversible" and "reversible step that becomes irreversible" (e.g. a branch that gets pushed).
  Done when: a plan with `git push` and `rm -rf` steps shows both as one-way, a sed edit as two-way, and a step whose two-way output feeds a later push is flagged escalating.

- **Ask gate: stop only on one-way AND disputed** — FEATURE — value 5 — effort M — risk med — category: judgment
  Why: the steer says "stops for me only when irreversible and ambiguous"; steer 3 says one `fm ask` for a cap, then keep going. Make `fm ask` refuse to send unless it carries a door tag, the competing readings, and why research couldn't settle it; otherwise it auto-decides and logs to the ledger. Parks the blocked row and continues the rest.
  Done when: an `fm ask` on a two-way choice is rejected with "decide and record", and one on a one-way, split choice is sent while other tasks continue.

- **Ambiguity as a vote across cheap samples** — FEATURE — value 4 — effort M — risk med — category: judgment
  Why: "ambiguous" is currently a feeling. Draw N=3 Haiku readings of the request at focus; agreement above a threshold means decide, a split means ambiguous. Zero-cost arms are favored by the testing-cadence steer. Assumption: Haiku sampling cost is acceptable at focus time only for M/L.
  Done when: a seeded vague goal yields a split vote recorded in the plan, and a clear goal yields unanimous readings, in a fixture test.

- **Minimax-regret picker with a fragility score** — FEATURE — value 4 — effort M — risk low — category: judgment
  Why: the plan gate requires 3+ options and a choice but not why that choice. Score each option against each reading (cost to redo if the reading is wrong) and pick minimax regret; print "fragility" = how many readings flip the pick.
  Done when: plan_gaps rejects a choice without a regret table for L tasks, and the table's pick matches a hand-computed fixture.

- **Calibration ledger: confidence vs outcome** — FEATURE — value 5 — effort M — risk low — category: judgment
  Why: Mission 8 already predicts minutes and attempts and scores them at close. Extend that to every stated confidence: bucket (60/80/95%) against outcome survival (not reverted, not re-fixed), and show the Brier score. A mismatch lowers the threshold at which Foreman researches. Uses a signal Foreman didn't author (outcome survival), per the standing rule.
  Done when: `fm calibration` prints per-bucket hit rates from closed tasks, and a bucket overconfident by more than 15 points tightens the research trigger in a test.

- **Research-changed-the-plan score** — FEATURE — value 3 — effort S — risk low — category: judgment
  Why: listed as an idea, no build yet. Diff the Approach section before and after a research note; if unchanged across many triggers on a given cause, raise that trigger's bar, and report "research confirmed" separately from "research changed".
  Done when: `fm triggers` shows a changed-plan rate for the research kind, computed from plan diffs in a fixture.

- **Blast radius says "unknown", not "none"** — FIX — value 3 — effort S — risk low — category: judgment
  Why: T-2277 writes co-change neighbours into Risks; with no history, an empty list reads as safe. Write "unknown: no co-change history for these paths" and treat unknown on a one-way step as ambiguity.
  Done when: focusing a task on a brand-new path writes "unknown" to Risks, and one with history lists neighbours.

- **Second key: a different vendor judges the one-way door** — FEATURE — value 4 — effort M — risk med — category: judgment
  Why: the open question "which verbs have a model on both sides with no user-owned check" and the steer for judges that aren't Foreman's own. Before any one-way step in bypass mode, a cold read by a different model family (via the Codex/Gemini adapters) must agree. Assumption: one non-Claude CLI is installed; otherwise it falls back to a different Claude tier and says so.
  Done when: with a stub second model that disagrees, the one-way step is held and the disagreement is recorded; with agreement it proceeds.

- **Wild: First-instinct tribunal** — FEATURE — value 3 — effort M — risk low — category: judgment — wild
  Why: assumption: first instinct is often the weakest pick. Before an L plan is accepted, record the instinct pick in a sentence, run the race and the evidence, then report whether evidence overturned it. Over time this shows when instinct is trustworthy and lets S/M skip the race.
  Done when: closed L tasks carry an "instinct vs final" field, and `fm calibration` reports the overturn rate.

- **Wild: Devil's advocate child for each one-way door** — FEATURE — value 3 — effort M — risk low — category: judgment — wild
  Why: a tool-less child gets only the plan and must write the single strongest paragraph for why this step ruins something, quoting the plan. A concrete quote is a blocker; a vague objection is advisory (mirrors the T-2246 cold-read rule).
  Done when: a seeded plan with a hidden data-loss step gets a quoting objection that holds the step; a safe plan gets none.

- **Wild: Pre-mortem rehearsal replays history** — FEATURE — value 4 — effort L — risk med — category: judgment — wild
  Why: assumption: past failures predict future ones. Before an L task, replay the plan's step types against the project's own failed and reverted tasks (fm graph, outcomes) and print the three nearest "how this went wrong last time" cases, with their fixes folded into Risks.
  Done when: an L plan touching a file with 2 past reverts shows those reverts, with task ids, in its Risks.

- **Park-and-continue queue for user-only rows** — FEATURE — value 4 — effort S — risk low — category: judgment
  Why: steer 3 says ask once and keep going on everything unblocked. A parked row records what unblocks it, expires into a digest, and, if the user later answers, auto-resumes the exact step. Shows one line at resume ("3 parked, 0 changed").
  Done when: a task with a user-only criterion is parked, the drive proceeds to the next task, and answering resumes the parked one.

- **Mid-goal "finished" amendments need a signed change** — FEATURE — value 3 — effort S — risk med — category: judgment
  Why: answers the open question about who may change the finished definition. Allow Foreman to tighten criteria itself (add a check) but never loosen without a user-owned grant; every amendment is a ledger row.
  Done when: a loosening edit to criteria by an agent is refused by the guard, and a tightening one is accepted and logged.

Next question: Which decisions in the ledger did the user later reverse, and what did those share (door type, confidence, task tier) that could predict the next reversal?
Next question: When the cheap-sample vote and the cold different-vendor read disagree, which one should win by rule, and is that rule itself something the user has ever stated?
