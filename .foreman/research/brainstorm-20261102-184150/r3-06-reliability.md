# Brainstorm — lens: reliability

- **Hash the fields each outcome measure reads** — FIX — value 4 — effort S — risk low — category: measures
  Why: assumption: a reading goes quiet if a ledger field is renamed. Every Exam outcome line would list the keys it reads, and `fm doctor` would store a schema hash for them. The pack shows T-2735 and T-2738 as breakage from a changed verb surface.
  Done when: renaming a ledger field in a fixture turns the dependent brief's cell red in `fm doctor`, naming the missing key, rather than letting it read as zero.

- **Score survival only over days the drive was alive** — FIX — value 5 — effort S — risk low — category: dissent scoring
  Why: assumption: the 14-day survival signal (M-12's question) counts wall-clock days. The pack shows usage-limit waits and "wait out real limits" steers, so a paused week could score every close as survived.
  Done when: a fixture ledger with a 10-day drive pause scores a close as "unobserved", not "survived", and the dissent score prints the live-day count.

- **Key brief filing by a content hash** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the pack shows repeated "Ship N commits" and re-run tasks (a T-2691-style refile and "approach 2" reruns). Re-running a crashed Mission should not file doubles.
  Done when: running the same Mission filing twice yields zero new T-ids and the second run prints the existing ids.

- **Keep a last-good copy of each tower file** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: standing rules require the tower to advance itself, and the pack shows lanes merging in mission order. A half-written `coverage.md` or `lineage.md` stalls every later sweep. Assumption: no copy exists today.
  Done when: truncating `coverage.md` in a scratch home makes the next sweep restore the last copy that passed `fm genesis check`, and it says so.

- **Quarantine the one brief whose Exam hangs the sweep** — FIX — value 4 — effort M — risk low — category: isolation
  Why: new Exam readings run live commands, and one hung or crashing reading shouldn't blank the sweep. Assumption: the sweep runs them in one pass.
  Done when: a planted Exam that sleeps forever is cut off at its timeout, marked "quarantined: timeout", and every other brief still reports.

- **Print a canary scan receipt on every "not built"** — FEATURE — value 4 — effort S — risk low — category: grounding
  Why: the map says "2176 files … 3 left out", so a canary can silently skip files. A "not built" claim without a denominator can't be trusted.
  Done when: each canary line shows files scanned, files skipped, elapsed time and the positive-control hit, and a canary that scanned under 95% prints "partial".

- **Run the dissent scorer on a planted-outcome ledger every sweep** — FEATURE — value 4 — effort M — risk low — category: dissent scoring
  Why: the carried gap is scoring dissents against outcomes, and a scorer that is wrong gives no signal. Assumption: no golden ledger covers it.
  Done when: a fixture with three dissents (one right, one wrong, one never observed) must score 1 / 0 / unobserved, and the sweep goes red if it doesn't.

- **Ledger each Exam's false-pass rate by measure kind** — FEATURE — value 4 — effort M — risk low — category: measures
  Why: the user's rule favours signals Foreman didn't author, and `fm outcomes` has re-ask evidence. Count briefs whose Exam passed and the user re-asked within 14 days, grouped by measure kind.
  Done when: `fm outcomes --exams` lists per-kind pass counts and re-ask counts, and a kind with a rate over a set bar is flagged.

- **Dry-parse every filed Exam command each sweep** — FIX — value 3 — effort S — risk low — category: command rot
  Why: T-2735 shows an unknown `list` action reached users. An Exam command can rot after filing as verbs change.
  Done when: renaming a verb flag in a fixture turns the Exam's cell red with "no longer parses", with no command run.

- **Wild: Plant one broken file in a shadow tower each generation** — FEATURE — value 3 — effort M — risk low — category: meta-check
  Why: wild; the sweep has no positive control of its own. Each generation would copy the tower, break one rule, and require the sweep to find it.
  Done when: the planted defect is reported by name, and a run that doesn't find it fails the generation.

- **Wild: Refuse readings stamped in the future** — SECURITY — value 3 — effort S — risk low — category: clocks
  Why: wild; a clock jump (the cases in "Time-shift every Exam reading") can make a stale reading look fresh. Each reading would carry the HEAD commit time and a monotonic counter.
  Done when: a reading stamped later than the newest commit plus a margin is rejected as "clock suspect" instead of passing.

- **Wild: Brownout one unattended Mission each month** — PERFORMANCE — value 3 — effort L — risk med — category: chaos
  Why: wild; fail 30% of child calls on a scratch copy and require the same set of briefs filed, within tolerance, and a receipt naming every retry.
  Done when: the brownout run's brief set equals the clean run's, or the diff is listed as "lost to faults" in the receipt.

Next question: Which Exam readings change meaning if the drive was paused, offline or running on another host when they were taken?
Next question: When a measure reads the same on the parent commit and the fixed one, who finds out first: the sweep, the cold reader or the user?
