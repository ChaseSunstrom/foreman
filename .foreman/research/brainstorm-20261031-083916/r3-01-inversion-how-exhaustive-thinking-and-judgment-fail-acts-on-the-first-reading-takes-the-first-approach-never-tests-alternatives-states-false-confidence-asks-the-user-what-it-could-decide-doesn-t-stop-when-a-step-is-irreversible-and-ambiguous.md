# Brainstorm — lens: inversion: how exhaustive thinking and judgment fail: acts on the first reading, takes the first approach, never tests alternatives, states false confidence, asks the user what it could decide, doesn't stop when a step is irreversible and ambiguous

- **Report "unknown", not "none", in the blast-radius Risks** — FIX — value 4 — effort S — risk low — category: judgment
  Why: T-2277 writes co-change neighbours and past FIXes into Risks. A new or rarely touched path has no history, and an empty section reads as "safe". Assumption: the section is empty when `fm graph blast` finds nothing.
  Done when: a test focusing an M task on a path with no git history writes "blast: no history, risk unknown" in Risks and the plan gate counts it as a low-confidence assumption.

- **Pin a tier floor from the scope's blast size** — FIX — value 4 — effort S — risk low — category: plan gate
  Why: the tier gates (T-2269) rely on the tier the same model assigns, so under-tiering skips the readings and options checks. Assumption: nothing sets a floor today.
  Done when: focusing an S task whose scope paths have 10 or more co-change neighbours is refused with "tier floor M", and a test shows the S gate no longer passes it.

- **Catch a refusal followed by a filler-only edit** — FIX — value 4 — effort S — risk low — category: gate integrity
  Why: T-2285 showed the Approach count missing options that start with a flag or code, so the gate can be satisfied by wording instead of substance. Watch for a plan-gate refusal followed within minutes by an edit that adds only short or low-content text.
  Done when: a fixture of refuse-then-pad passes, and the second pass files a "gate gameable" capture naming the shape.

- **Make each pair of options carry a discriminating probe** — FEATURE — value 4 — effort M — risk med — category: exhaustive thinking
  Why: the first approach wins by default when options can't be told apart. Require a line like "if `<command>` shows X, option B beats A", so the race and the research trigger have something to run.
  Done when: an M/L plan whose options lack a probe is refused, and a test shows one with a runnable probe passes.

- **Freeze the race's verify before the lanes start** — SECURITY — value 4 — effort M — risk med — category: race integrity
  Why: when the builder writes the test and also judges the winner, writer and judge are the same model. This is the earlier "model on both sides" question applied to `fm lane race`.
  Done when: lanes get the verify file hash-locked read-only, and a lane that edits it is disqualified in the race record.

- **Score race candidates for independence** — FEATURE — value 3 — effort M — risk low — category: race integrity
  Why: two lanes from the same model and prompt often converge on one diff, so the race measured nothing. Assumption: lanes can share a model.
  Done when: the race result prints a pairwise diff similarity, and one above the threshold is recorded as "no real alternative" and not as a win.

- **Lint plan prose for unsupported certainty** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: false confidence arrives as words like "obviously", "should be fine" and "just". Turn each such phrase with no cited evidence into a low-confidence assumption row, which the existing rule then sends to research or a spike.
  Done when: a plan containing "this should just work" gains an assumption row and fails the gate until it has a research note or spike.

- **Batch questions into one digest under a per-goal ask budget** — FEATURE — value 4 — effort S — risk low — category: user interruptions
  Why: steer 3 says to keep going on everything a question doesn't block, yet each `fm ask` still interrupts alone. Batch the non-blocking ones to a natural boundary, with the default Foreman will take if unanswered.
  Done when: three non-blocking asks in one session appear as one digest, each with its default, and a cap of N is enforced.

- **Park the user-only row and continue on the rest** — FEATURE — value 5 — effort M — risk med — category: judgment
  Why: stopping the whole goal for one irreversible-and-ambiguous row wastes the wait. Build the reversible rows behind the parked one and record the park as a plan row.
  Done when: in a fixture with one user-only row and two free rows, the free rows close, the parked row shows as waiting, and nothing irreversible ran.

- **Show precedent before a decision is made** — FEATURE — value 3 — effort M — risk low — category: consistency
  Why: decisions are recorded with undo lines, but nothing reads them back, so the same fork gets decided differently next time. Assumption: decisions are keyed by scope path.
  Done when: recording a decision on a path with an earlier one prints it, and reversing it requires a "why changed" line.

- **Alarm when deliberation outweighs the work** — PERFORMANCE — value 3 — effort S — risk low — category: depth control
  Why: the mission warns that an S task shouldn't pay an L task's cost. Compare plan and race tokens with the final diff size per closed task.
  Done when: `fm doctor` lists tasks where planning cost exceeded 3x build cost, with the tier each should have been.

- **Wild: Run an opposite-day lane** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild. For a chosen L approach, one cheap lane builds the "do less" inverse. If it passes the same verify, the winner's margin was zero and the record says so.
  Done when: a fixture where the minimal option also passes marks the winner "not needed" in the race record.

- **Wild: Forecast the user's first complaint from their words alone** — FEATURE — value 3 — effort M — risk low — category: unspoken needs
  Why: wild. A cold child sees only the user's request and the finished diff and writes the first thing they'd object to. Anything the plan has no row for is a missing reading, caught before close.
  Done when: at L-task close, the forecast complaint is matched against plan rows, and a miss blocks close with the quoted gap.

- **Wild: Keep a "confidently wrong" hall of fame in `fm doctor`** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. List the highest-confidence claims later proven false, each with its evidence kind, so the calibration ledger gives the user something worth reading.
  Done when: `fm doctor --wrong` prints the top 5 with the claim, the stated confidence and the task that disproved it.

Next question: Which of the plan gate's checks can be satisfied by wording alone, and what is the minimal check that needs a command to have actually run?
Next question: When two lanes agree, how often is it because they share one model's blind spot and not because the answer is right?
