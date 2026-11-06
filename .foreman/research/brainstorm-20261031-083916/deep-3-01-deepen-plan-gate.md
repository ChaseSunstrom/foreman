# Brainstorm — lens: deepen: plan gate

- **Run the plan gate's checks as one "plan lint" that returns a scored verdict** — FEATURE — value 5 — effort M — risk med — category: plan gate
  Why: the existing ideas (costume options, paraphrased readings, unfalsified assumptions, undo lines, tier floor) are each a separate check. T-2285 shows the single check misses edge cases (an option starting with a flag or code). Combining them gives one gap list with a score per check, and one place to fix false positives.
  Done when: `fm task set` on a plan with a paraphrased reading and a falsifier-less assumption prints both gaps in one pass, and a fixture plan whose option starts with `--bench` is counted as an option.

- **Replace text-shape counting with a structural option check** — FIX — value 4 — effort S — risk low — category: plan gate
  Why: T-2285 was a plan-gate miss from counting text after a marker. Parse each option into verb, target and a differing-file or differing-command set, and count options that differ in at least one of those.
  Done when: a fixture with options "(1) --bench …", "(2) `sed -i …`", "(3) do less" passes, and three options with the same verb and target fail.

- **Make the tier floor follow the blast radius and the history of its files** — FEATURE — value 4 — effort M — risk med — category: plan gate
  Why: T-2277 already writes blast neighbours into Risks. The next step is to raise the tier floor for a task whose scope touches a file with past FIXes or reverts, so an "S" label cannot skip the M gate.
  Done when: an S task scoped to a file with 2+ past FIXes is refused at focus with "tier floor M: <reason>", and a clean file stays S.

- **Require a falsifier line for every low-confidence assumption** — FEATURE — value 4 — effort S — risk low — category: plan gate
  Why: T-2269 already requires a research note or spike first. A falsifier ("this is wrong if `<command>` prints X") makes the assumption testable, and the check can run it at focus.
  Done when: an assumption marked low confidence with no falsifier fails the gate, and one whose falsifier command runs and contradicts it blocks focus.

- **Pair every one-way step with a named undo or an explicit "no undo"** — FEATURE — value 4 — effort S — risk low — category: plan gate
  Why: the pack says Foreman stops for the user only when something is irreversible and ambiguous. A plan step that deletes, migrates, pushes or publishes with no undo line is that case, and the gate can find it from the step text.
  Done when: a plan step containing `rm`, `migrate`, `push` or `publish` with no `Undo:` line is refused, and `Undo: none (reason)` passes and is recorded.

- **Score the plan gate against past plans that went wrong** — CLEAN — value 4 — effort M — risk low — category: plan gate
  Why: the gate has never been checked by anything Foreman did not author, which matches a standing rule and one of the left-over questions. Replay closed tasks' plans (re-fixed, reverted, dropped) through the gate and report how many it would have flagged versus passed.
  Done when: `fm gate replay` prints flagged and passed counts split by outcome, with a precision figure for each check.

- **Learn which plan edits the user makes after accepting a plan, and pre-apply them** — FEATURE — value 3 — effort M — risk med — category: plan gate
  Why: a left-over question asks for the smallest plan edit the user makes most often. The edit diffs exist in the task history. Assumption: they are logged and clusterable (for example "added a test criterion", "narrowed scope").
  Done when: after 5 similar edits, the next plan carries the edit as a suggested line marked "learned from T-…", and the user can switch it off per kind.

- **Let a plan state when its "finished" definition may change, and log each change** — FEATURE — value 3 — effort S — risk low — category: plan gate
  Why: a left-over question asks whether the finish definition can change mid-goal. Add a `Criteria changes:` rule (who may change them, and what evidence is needed), so a builder lowering the bar silently shows up as a recorded edit.
  Done when: editing a criterion after focus writes a dated entry with the old and new text, and `fm task finish` lists it.

- **Wild: Run a rival planner blind and show only the differences** — FEATURE — value 4 — effort L — risk med — category: plan gate — wild
  Why: assumption: a second tool-less child from another model, given only the goal, produces its own readings and options. Overlap with the written plan means agreement. A reading or risk that appears only in the rival plan is shown as "you did not consider".
  Done when: for an L task, the plan gate output lists at least one rival-only reading or risk, or the line "rival found nothing new", and the rival never sees the plan.

- **Wild: Pre-mortem the plan, with a child told the plan failed and asked why** — FEATURE — value 3 — effort M — risk low — category: plan gate — wild
  Why: assumption: failure stories are cheaper than option lists. Each story must name a step and a command that would have shown the failure early; accepted ones become checks in the Verify section.
  Done when: an M/L plan gains at least 2 pre-mortem lines, each tied to a step number and a runnable check, before focus is allowed.

- **Wild: Show the plan as a short rehearsal run with no edits** — FEATURE — value 3 — effort L — risk high — category: plan gate — wild
  Why: assumption: the plan's commands can be dry-run in a throwaway worktree. Running every Verify command before the work shows which ones are already green (so they prove nothing) or cannot run at all.
  Done when: focusing an M/L task prints the list of Verify commands that pass before any edit, and flags them as "proves nothing".

- **Warn when a plan's confidence stays flat across many tasks** — FEATURE — value 3 — effort S — risk low — category: plan gate
  Why: Mission 8's predict-and-score feature records predictions and results. If a plan always says "high" and a third of those tasks are re-fixed, the stated confidence has stopped meaning anything.
  Done when: `fm doctor` reports confidence-vs-outcome by tier and warns when high-confidence plans fail as often as low ones.

- **Make the plan gate's refusal text the fix, with one runnable command** — FIX — value 3 — effort S — risk low — category: plan gate
  Why: the dropped fm run stall item shows that refusals which name their fix work well. Extend this so every gap prints the exact `fm task set ID --section …` line with a template to fill in.
  Done when: each gap kind in the test suite prints a copy-pasteable command, and a test runs that command against a fixture and clears the gap.

Next question: Which plan-gate checks has the user ever overridden or bypassed, and what did they do instead?
Next question: Does the gate treat a task made by `fm code`'s planner, or by a headless `fm run` session, the same as a user-made task, and who checks the checker there?
