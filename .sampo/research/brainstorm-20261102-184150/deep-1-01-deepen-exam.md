# Brainstorm — lens: deepen: exam

- **Make the Exam a three-valued, signed record (pass / fail / unmeasured)** — FEATURE — value 5 — effort M — risk low — category: exam
  Why: the list has "could not run" and "unmeasured, never pass" as separate ideas; combined, they are one record type. Evidence: the open question "when a snapshot cannot be taken, carry forward or block?" Assumption: today a failed read collapses into pass or fail.
  Done when: `fm exam brief T-id` run with the service stubbed down exits with a distinct code and writes `unmeasured` plus the reason beside the brief, and the close gate treats it as not-pass.

- **Score dissents against outcomes through the Exam's meter** — FEATURE — value 5 — effort M — risk med — category: exam
  Why: the carried gap says "dissents scored against outcomes", and the earlier question asks how many gen-3 briefs have a computable measure. Parsing unit, direction and threshold gives each dissent a testable claim ("this measure will not move").
  Done when: for a dissent attached to a brief, `fm outcomes --dissents` prints the dissent, the parsed measure and whether the reading later agreed, with at least one real gen-3 brief scored.

- **Audit gen-3 briefs for vacuous measures and file the tally** — CLEAN — value 4 — effort S — risk low — category: exam
  Why: directly answers the pack's first question, and the cookbook, the unit/direction parser and the cold replay all need a baseline count. Assumption: some briefs name a measure with no reading command.
  Done when: a file lists each gen-3 brief as computable, re-runnable cold, or vacuous, with counts, and `fm doctor` names the vacuous ones.

- **Replay Exams in a hermetic shell and report session-state dependence** — FEATURE — value 4 — effort M — risk med — category: exam
  Why: merges the hermetic-replay and "re-run by hand" ideas to answer "which Exams survive a cold process". Replay in an empty HOME and a clean env, diffing against the filed reading.
  Done when: `fm exam replay T-id` prints "cold-stable" or lists the env vars, files or session paths the reading needed.

- **Pair each measure with a counter-measure and a gaming probe** — SECURITY — value 4 — effort M — risk med — category: exam
  Why: the open question "when a measure is gameable, who finds out first?" The pair (target metric plus guardrail) is checked at filing by a cold child, so the builder doesn't discover it at close. Cost is one cheap read at filing instead of rework at close.
  Done when: a brief whose Exam has no counter-measure is refused at filing, and a planted gameable measure (for example "tests count rises") is flagged by the probe in a test.

- **Set a visited-vs-covered status per grid cell from typed asks** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: answers "exam passes but no typed ask landed in a cell all generation: covered or unvisited?" Join coverage.md cells with the user's asks and show passing-but-unvisited cells separately.
  Done when: `fm genesis check` prints a column of asks-per-cell for the generation and lists passing cells with zero asks as "unvisited".

- **Learn from user overrides which readings are noise** — FEATURE — value 3 — effort M — risk med — category: exam
  Why: the pack asks which readings the user opened or overrode. Count overrides per reading kind; high override plus later outcome survival suggests noise, while override plus later regression suggests skipped proof.
  Done when: `fm outcomes --readings` lists per reading kind opens, overrides and the later survival rate.

- **Carry forward the last good reading with an age stamp** — FEATURE — value 3 — effort S — risk low — category: exam
  Why: the offline case. Combines timestamping with unmeasured: show "last read 3d ago: 12, now unmeasured" and let the close gate set a staleness limit per measure class.
  Done when: with the source stubbed down, the Exam output shows the last value and its age, and a reading older than its limit blocks the close.

- **Wild: Run a ghost builder against every Exam before filing** — FEATURE — value 4 — effort L — risk med — category: exam (wild)
  Why: a tool-less child told only the Exam tries to make it pass with the cheapest degenerate change (delete the check, hard-code the value). If it can describe one, the Exam is filed with a hardening note. Extends "run the Mission against its own ghost".
  Done when: a seeded weak Exam in a fixture yields a named cheap exploit from the ghost, and a hardened version yields none.

- **Wild: Publish a calibration curve of Exam predictions versus 14-day survival** — FEATURE — value 4 — effort M — risk low — category: exam (wild)
  Why: the repo already ran M-12 (pooled forecasters on whether a close survives 14 days). Each Exam's predicted reading is checked at 14 days, giving a per-capability reliability diagram on the site. Assumption: enough closes accumulate.
  Done when: the site's genesis page shows a plotted curve with at least N closes and a table of the worst-calibrated capability.

- **Wild: Give every closed brief a mutation sanity run on its own Exam** — FEATURE — value 3 — effort L — risk med — category: exam (wild)
  Why: revert the brief's diff in a scratch worktree and confirm the Exam turns red. The "good world and bad world" idea made automatic; the repo's `fm task prove` already does this for tests.
  Done when: for a sample of closed briefs, `fm exam mutate T-id` reports red on reverted code, and the briefs where it stays green are listed as toothless.

- **Time-box and log each reading, with a budget across the Mission** — PERFORMANCE — value 3 — effort S — risk low — category: exam
  Why: merges the timeout, exit-class and 15-second budget ideas. Slow readings get cut and recorded, so a Mission's total Exam time is visible and bounded.
  Done when: a reading that sleeps past the cap is killed, recorded as `timeout` (a kind of unmeasured), and the Mission page shows the total Exam runtime.

- **Mine the Exam trailer into a searchable reading history** — FEATURE — value 3 — effort S — risk low — category: exam
  Why: with the Exam in a commit trailer and a diffable file per brief, one command can answer "how did this measure move across generations".
  Done when: `fm exam history <measure>` prints readings per brief with dates and the commits they came from.

Next question: Which Exam readings does the user actually trust enough to skip reviewing the diff, and does that trust track the measure's later survival rate?
Next question: What is the cheapest signal not authored by Foreman that could check an Exam's measure — an outside tool, a different-model read, or user spot checks?
