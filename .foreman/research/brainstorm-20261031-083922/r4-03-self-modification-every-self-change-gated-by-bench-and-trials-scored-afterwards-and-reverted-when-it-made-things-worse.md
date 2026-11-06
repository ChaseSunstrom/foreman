# Brainstorm — lens: self-modification: every self-change gated by bench and trials, scored afterwards and reverted when it made things worse

Questions I can answer from this lens:
- **Model on both sides, no user-owned check:** the self-fix loop. A model writes the fix, and a model-written bench and cold read judge it. Idea 1 and the exam-freeze idea add checks outside that pair.
- **Numbers never checked by someone other than their producer:** the bench pass rates that gate self-changes. Ideas 1, 2 and 8 check them.

- **Demand an improvement bigger than the bench's own noise** — FEATURE — value 5 — effort M — risk low — category: gating
  Why: assumption: bench scores come from model-driven runs and vary run to run. T-0035 (run cases N times) is still deferred, so a +1 can pass as a win. The existing ideas cover held-out sets and shadow runs, not variance.
  Done when: `fm bench` stores a per-case noise floor (N≥5 runs on the unchanged tree), and a self-change is accepted only when its delta is above 2× that floor. A test with a no-op change reports "within noise, not accepted".

- **Plot a treadmill curve: today's Foreman against frozen past builds** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the user's steers need proof of real improvement. Per-change survival can hide a tower that gets 40 fixes better and nothing overall. Zero-token arms (finders, oracle, empty) are cheap to rerun on old tags.
  Done when: `fm selfchange curve` runs the free arms on today's tree and on builds from 30, 60 and 90 days ago, prints one line per build, and flags "flat or falling" when the newest isn't ahead.

- **Freeze the build while an exam runs** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: the end-of-run exam is the deciding score, and parallel `--jobs N` runs take hours. A self-change landing mid-run would make the score describe no single build.
  Done when: `fm exam run` writes the build hash and a freeze marker, and `fm ship` and the self-fixer refuse to merge while it exists. Every exam row records the hash.

- **Test pending self-changes in pairs before merging either** — FEATURE — value 4 — effort M — risk med — category: interaction
  Why: assumption: with up to 6 lanes and the signal-to-fix loop running unattended, two fixes that each pass alone may collide. Merge conflicts are forecast but semantic ones aren't.
  Done when: with two queued self-changes, the gate runs the bench on both merged and on each alone, and refuses the pair if the combined score is below the better single.

- **Put a trust region on learned numbers** — SECURITY — value 4 — effort S — risk low — category: learned params
  Why: the model router (T-2291), trigger precision (T-2276) and prediction scoring (T-2290) all adjust themselves from history. One bad week could swing them far.
  Done when: each learned parameter moves at most a set step per week, and a test feeding an extreme history shows it clamped with a "capped" line in `fm doctor`.

- **Count whether each fix's code path ever ran** — FEATURE — value 4 — effort M — risk low — category: survival
  Why: "held for 30 days" can mean the failure never recurred, or that the fix was never reached. The steers already require that capabilities be called from a real session path.
  Done when: each self-change records a hit counter on its guarded branch. After 30 days the ledger shows held-and-exercised, held-and-dormant or reverted, and dormant ones are flagged unproven.

- **Grow the bench from every revert** — FIX — value 4 — effort S — risk low — category: bench health
  Why: assumption: a reverted change means the bench lacked a case that would have caught it. Saturated benches (everything passes) can't discriminate.
  Done when: a revert opens a task that adds the failing scenario to the bench. `fm doctor` warns when a bench's pass rate has been 100% for 3 generations.

- **Select bench cases by the change's blast radius** — PERFORMANCE — value 4 — effort M — risk med — category: gate cost
  Why: gating every self-change on the full bench is slow. `fm graph blast` already gives co-change neighbours.
  Done when: a change touching `fmcode.py` runs only the mapped cases plus a random 10%, with a full run nightly. A test shows the subset catches a planted regression in the touched area.

- **Revert a change together with the changes built on it** — CLEAN — value 3 — effort M — risk med — category: ledger
  Why: assumption: later self-fixes often rely on earlier ones (T-2272 feeds T-2276). Reverting one alone could leave a broken dependent.
  Done when: each ledger entry lists the changes it builds on. `fm selfchange revert ID` prints the dependents and, after one yes, reverts them as a unit or declines.

- **Shrink each accepted self-change to its smallest passing diff** — CLEAN — value 3 — effort M — risk low — category: blast radius
  Why: the lean ratchet warns about growth, but a fix can carry hunks that nothing needs.
  Done when: before merge, hunks are dropped one at a time (delta debugging). The failing-first test and bench must still pass, and the merged diff is no larger than the minimal set.

- **Wild: Use the user's two machines as a natural A/B** — FEATURE — value 3 — effort L — risk med — category: experiment
  Why: wild; assumption: the user runs on more than one machine. Land a self-change on one only and compare corrections and reds per day against the other.
  Done when: `fm selfchange ab ID` assigns the change to a machine, and after 7 days prints both machines' correction counts side by side.

- **Wild: Let cheap models bet on whether a change will survive** — FEATURE — value 3 — effort M — risk low — category: forecasting
  Why: wild; the system already scores predictions. Three Haiku children each bet "holds" or "reverted" with a confidence, and their Brier score decides whose bets count.
  Done when: each proposed change stores three bets, and a unanimous low-confidence "reverted" sends it to the user's yes queue. Hit rates appear in `fm doctor`.

- **Wild: Keep a public fossil record of reverted self-changes** — FEATURE — value 2 — effort S — risk low — category: site
  Why: wild; the standing rule says the site follows Genesis. A page of what Foreman tried, why it failed and which case caught it is rare, honest and cheap.
  Done when: `fm genesis live` publishes `site/genesis/fossils` from the ledger, with the reason and the new bench case id for each revert.

Next question: which self-changes did the user undo by hand without telling Foreman, and how would it notice?
Next question: when the bench, the trials and the user's corrections disagree about a change, which one wins by rule?
