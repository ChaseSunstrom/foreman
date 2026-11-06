# Brainstorm — lens: the skeptical user (invented): does it do what the user meant, not what the test says; the user's own words become the acceptance check

- **Bind each clause of the ask to a falsifier at focus** — FEATURE — value 5 — effort M — risk med — category: intent proof
  Why: "Count the clauses of every ask" and "Pin the ask's verbs and nouns" exist as ideas, but nothing links a clause to a command that must fail before and pass after. T-2285 and T-2289 were asks the user made because an earlier check matched the test, not the meaning.
  Done when: `fm task focus` on a task whose ask has 3 clauses writes 3 clause→verify rows, and `fm task finish` refuses while any row has no command that failed on the start tree.

- **Run the user's past corrections as a regression pack** — FEATURE — value 5 — effort M — risk low — category: intent proof
  Why: "Plan gate misses an option whose text starts with a flag" (T-2285) is a correction of a prior gate. Steers and corrections are stored but not replayed against new work.
  Done when: each recorded correction has a replayable check, and `fm check` runs them all and names the correction quote when one fails.

- **Show a skeptic's "could this pass while wrong?" line per criterion** — FEATURE — value 4 — effort S — risk low — category: unproven
  Why: the unproven rollup counts typed evidence, but not criteria whose command would pass on a wrong implementation (e.g. `grep` of a string). assumption: a cheap model-free heuristic (command only greps, only checks exit 0 on a no-op) catches most.
  Done when: a criterion whose verify command passes on an empty diff is flagged "can't fail" in `fm task show` and the rollup.

- **Let the user phrase the acceptance check in plain words and compile it** — FEATURE — value 5 — effort L — risk med — category: acceptance
  Why: the user's asks are often a sentence ("fm lane rm refuses a lane holding .fm-scratch/: treat it as throwaway"). assumption: sentences of the form "when X, Y" map to a command plus expected output.
  Done when: `fm task accept ID "when I run fm lane rm on a lane with .fm-scratch, it removes it"` creates a scratch-repo script that fails before and passes after, shown to the user for a one-key yes.

- **Diff the behaviour, not the code, at close** — FEATURE — value 4 — effort M — risk med — category: close receipt
  Why: the user reads diffs poorly as proof of intent; "what would I see differently" is the question. Perf and migration kinds already record before/after.
  Done when: finish prints "before: <output> / after: <output>" for the task's acceptance command, run on both trees.

- **Flag diff hunks that no criterion mentions** — FEATURE — value 4 — effort M — risk low — category: scope
  Why: the skeptic fears unrequested behaviour; the plan gate checks plan content, not what the diff did beyond it. assumption: path/symbol overlap with criteria and scope paths is a good-enough signal.
  Done when: finish lists files or functions changed outside any criterion's or scope's named paths, and the list is empty or acknowledged.

- **Reopen-as-signal: count the user's follow-up asks that restate a closed task** — FIX — value 4 — effort M — risk low — category: feedback
  Why: T-2285, T-2288, T-2289 are asks that follow earlier closes; no ledger says "this close missed the meaning".
  Done when: a new ask with high overlap to a closed task's criteria is linked as a miss, and `fm triggers` shows a per-proof-kind miss count.

- **Require a literal read-back before the first edit** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: assumption: many meaning gaps start at focus. The agent restates the ask in one line using the user's nouns; the user's veto is one word.
  Done when: focus on an M/L task prints the read-back and waits at most N seconds or proceeds on default, recording it.

- **Check the final answer's claims against the evidence rows** — FEATURE — value 4 — effort M — risk med — category: claims
  Why: the Stop gate checks done, not that each sentence ("migrations are reversible") has a row behind it.
  Done when: a sentence in the final message with a number or "now does X" and no matching evidence row is listed as unproven in the finish output.

- **Wild: Hire a literal-minded implementer that gets only the user's sentence** — FEATURE — value 4 — effort L — risk med — category: blind re-implementation
  Why: wild. A cold child builds from the ask alone in a scratch tree; where its behaviour differs from the real fix on the acceptance script, the ask was ambiguous or the fix over-reached.
  Done when: finish shows a "divergences" list from running both on 5 generated probes.

- **Wild: Play the task back as a one-line demo the user can paste** — FEATURE — value 4 — effort S — risk low — category: receipts
  Why: wild. Every close ends with `fm replay T-NNNN`: a single command that shows the new behaviour in a throwaway copy, so a skeptic checks with their own eyes.
  Done when: the command runs offline on a fresh clone and prints the before/after for the task's acceptance line.

- **Wild: Score the user's trust per proof kind from what they re-check themselves** — FEATURE — value 3 — effort M — risk med — category: trust
  Why: wild. When the user runs the demo, opens the diff, or re-asks, that is a signal the proof didn't convince; kinds they never double-check are earning trust.
  Done when: `fm proof trust` lists kinds by re-check rate with counts, and a rate over a threshold prompts for a stronger kind.

- **Wild: Pre-register the meaning before work and sign it** — FEATURE — value 3 — effort S — risk low — category: acceptance
  Why: wild. The user's clause list is hashed at focus; a mid-task change to "finished" requires the user's own verb, so the builder can't quietly redefine the target.
  Done when: editing criteria after focus without the user-run verb makes finish refuse and name the diff.

Next question: Which of the user's recent asks (T-2285, T-2289, T-2326) would a clause-to-falsifier binding have caught before they had to ask?
Next question: When the user's sentence is ambiguous, who picks the reading, and is that choice ever shown back with a veto?
