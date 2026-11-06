# Brainstorm — lens: the second opinion (invented): a cold rival that sees only the request designs it differently; every place the plans differ is a reading or approach the first one missed

- **Run a cold rival planner on the request alone and diff readings** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: Mission 5 asks for "the readings of the request" and every approach, yet T-2269's gate only checks that the first plan names options. Nothing proves the readings are complete. Assumption: a second planner that sees only the request text (no repo, no first plan) lists readings and approaches the writer missed.
  Done when: `fm plan rival ID` writes a table of readings and approaches in both plans, with the rival's extras flagged, and a fixture where the first plan omits a reading shows it listed.

- **Fence the rival from the first plan in code** — SECURITY — value 4 — effort S — risk low — category: independence
  Why: A "blind" rival that can read the first plan isn't blind. Earlier ideas fence it in the prompt only. Assumption: the rival runs as a tool-less child like these brainstormers.
  Done when: a test feeds the rival's input builder a plan containing a marker string, and the marker never appears in the child's prompt.

- **Treat rival disagreement as the ambiguity signal for stopping** — FEATURE — value 5 — effort M — risk med — category: judgment
  Why: Mission 5 #8 says stop only when something is irreversible and ambiguous, but "ambiguous" has no measure. Two blind plans that pick different readings is a measured fork. Assumption: reading-level disagreement correlates with later user corrections.
  Done when: `fm ask` is raised only if a step is irreversible AND the two plans' chosen readings differ. A test with agreeing readings proceeds and records the decision.

- **Score the rival against outcomes, not taste** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: The user's rule is to tune from signals Foreman didn't author. When a rival-only reading later matches a reopen, a user steer, or a reverted commit, count it a hit. Assumption: reopens and reverts carry task ids that can be matched to readings.
  Done when: `fm triggers` lists a rival hit-rate per tier, computed from closed tasks, and a fixture with one matching reopen shows 1 hit.

- **Let the rival write the "do less" option first** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: The gate counts 3+ options, and the plan-gate gap (T-2285) shows options get padded. Asking the rival for the smallest option first counters that. Assumption: the first plan rarely leads with the minimal option.
  Done when: the rival output has a "smallest option" line, and the gate fails an L plan whose options contain no option the rival ranked as smaller than the chosen one.

- **Race the two plans' definitions of finished on one held-out scenario** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: The open question "does the plan's finished definition ever need to change" shows the definition of done is a reading too. Assumption: both plans' done-when commands can run against the same planted-fault scenario from the exam harness.
  Done when: `fm plan rival --done` runs each plan's verify against a scenario with a known false-done and reports which one catches it.

- **Diff the plans in a three-column table with the user's words** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: The pack's user-words block shows the user steering by their own phrases. A table of the user's quote, plan A's reading and plan B's reading lets them veto in one word. Assumption: the web UI plan view can take a table.
  Done when: the plan page shows the table, and each row has a keep-A/keep-B/both control that writes a decision.

- **Cache rival plans by request hash and skip S-tier** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: A rival on every task would cost tokens against the lean-ratchet rules. Assumption: S tasks rarely gain from a second plan, so the skip is logged and the user can override it.
  Done when: an S task logs "rival skipped (S)", and a repeated request hash reuses the stored rival plan without a new child run.

- **Use a different model family for the rival** — SECURITY — value 3 — effort M — risk med — category: independence
  Why: Standing rule: cold reviews should use a different model. A rival from the same family shares blind spots. Assumption: `fm agents` can route a tool-less child to Codex or Gemini.
  Done when: the rival's record names a model different from the planner's, and `fm doctor` warns when both are the same.

- **Flag plans where both rivals agree too easily** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: Near-identical plans from the same prompt shape suggest shared bias, not truth. Assumption: a token-overlap score between the two readings sets is a usable proxy.
  Done when: above an overlap threshold, the plan records "agreement may be shared bias" and the research trigger fires once; a fixture of two copies triggers it.

- **Wild: Hold a debate round where each plan kills the other in one paragraph** — FEATURE — value 3 — effort M — risk med — category: judgment
  Why: wild. Each plan must name the other's most expensive wrong assumption. The survivor's assumptions get falsifiers.
  Done when: the debate file holds two paragraphs, and every named assumption becomes a plan row with a check.

- **Wild: Run a standing rival that reads the user's steers as a stranger** — FEATURE — value 3 — effort M — risk med — category: intent
  Why: wild. Steers are the user's strongest signal. A stranger-reader lists how each could be carried out in a way the user didn't mean, which turns "malicious compliance" into a check.
  Done when: each new steer gets a "misreadings" list stored beside it, and one misreading becomes an automatic check.

- **Wild: Publish "where the rival disagreed" as a weekly page on the site** — FEATURE — value 2 — effort S — risk low — category: transparency
  Why: wild. The site already refreshes stats daily (T-2326). A weekly page of real disagreements and who was right makes the calibration claim checkable.
  Done when: genesis publish writes the page from the rival log, with outcomes marked pending or resolved.

- **Wild: Plan the request at a tenth and ten times the budget** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. A rival told to finish in one tenth the effort shows what is optional. One given ten times shows what is missing. The gaps between the plans are the cut lines.
  Done when: `fm plan span ID` prints the rows present only in the large plan and absent in the small, labelled must or could.

Next question: Which of the user's past corrections were readings of the request that a blind second plan would have produced on day one?
Next question: Does the rival's cost beat the cost of the reopens it prevents, measured per tier?
