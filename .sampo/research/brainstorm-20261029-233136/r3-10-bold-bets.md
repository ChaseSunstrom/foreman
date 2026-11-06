# Brainstorm — lens: bold bets

- **Run Genesis against a rival harness in a public arena** — FEATURE — value 5 — effort L — risk med — category: proof
  Why: the user steered toward outside signals (head-to-head vs plain Claude Code on held-out scenarios); the exam already has foreman and plain session arms. Extend to a standing, versioned ladder (plain Claude, Foreman gen-N, Foreman+Genesis) on a rotating hidden third, with scores published on the Genesis site page.
  Done when: `fm genesis arena` runs three arms on one held-out set, writes per-arm pass/cost/time to exam.jsonl, and the site page shows the ladder with Genesis-on beating Genesis-off on at least one generated project.

- **Let Genesis write its tower for a project it can't run** — FEATURE — value 4 — effort L — risk med — category: coverage
  Why: assumption: strangers include stacks fm exam doesn't generate (6 languages only). Bold version: Genesis builds a black-box harness (CLI/HTTP/file-diff oracles) from the README alone, so any repo gets a tower.
  Done when: on a fixture repo in a language outside the six, `fm genesis init` yields a gen-0 plus ≥9 scenarios, with the empty arm failing all of them.

- **Make Genesis the loop's default idle behavior** — FEATURE — value 5 — effort M — risk high — category: autonomy
  Why: the request says it starts when the queue runs dry; routing in rules/foreman.md is protected core, so the work is a candidate patch plus the user's yes. Bold framing: the patch ships as a single reviewable diff with a dry-run showing what the last 30 days of idle gaps would have triggered.
  Done when: `fm genesis autostart --replay 30d` prints the would-have-fired events and the exact rules diff, and nothing changes without the user's yes.

- **Compile the gen-0 into an executable constitution** — FEATURE — value 5 — effort L — risk med — category: governance
  Why: drift is checked by `fm second` reading prose. Compile each MUST/NEVER into a runnable predicate (guard rule, test or lint) so drift becomes a failing command, not an opinion.
  Done when: every MUST/NEVER in a generated gen-0 maps to a check id, and a deliberately violating rewrite fails at least one check.

- **Tower tournament: N gen-1 candidates from different Seeds, one survives** — FEATURE — value 4 — effort L — risk med — category: selection
  Why: the request says selection keeps a rewrite only if it closes more scenarios than its parent; with one lineage that's a hill climb. Run 3 Seeds in parallel lanes (fm lane race exists), select on closures per dollar.
  Done when: `fm genesis run --seeds 3` produces three gen-1 branches, a lineage entry naming the winner and the losers' closure counts.

- **Mine the project's history into scenarios the author never saw** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the user's steers/drops are a rich signal (each dropped item and each correction is a regression). Turn fix/revert commits and steers into held-out scenarios, replayed against the empty arm.
  Done when: a repo with 5 fix commits yields ≥5 scenarios, each failing at the pre-fix commit and passing at the fix.

- **Ship a one-page "what Genesis would do" dry run** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: assumption: a first-time user won't hand a self-directing tower a repo blind. `fm genesis plan` prints draft gen-0, estimated scenarios, cost quote and the stop rule, running nothing.
  Done when: the plan prints without writing to the tower and its cost quote is within 2× of the first real generation's actuals.

- **Fork-and-judge: Genesis proposes a rule change only after winning on a cloned project** — FEATURE — value 4 — effort L — risk med — category: self-modification
  Why: self-edits need measurement. Run each template/lens change on two held-out generated projects; promote only if both improve.
  Done when: a template change that wins on one project but loses on the other is rejected in the ledger.

- **Wild: Genesis time-capsule — seal a prediction of the project at +30 days and grade it** — FEATURE — value 3 — effort M — risk low — category: calibration — wild
  Why: assumption: nothing currently tests whether the spec's idea of "best-in-class" matches where the project actually goes. Seal a hashed forecast (features, tasks, asks); fm outcomes grades it later, and the miss rate tunes the writer.
  Done when: a sealed forecast file exists with a hash, and a 30-day grade command reports hits and misses.

- **Wild: A speciation mode that grows two towers for one project (conservative vs aggressive) and shows the diff** — FEATURE — value 3 — effort L — risk med — category: exploration — wild
  Why: the user said no idea killed for ambition. Two temperaments of gen-0 from the same repo show which MUSTs are real and which are the writer's temperament.
  Done when: `fm genesis fork --temper bold|careful` writes two gen-0s and a page listing MUSTs unique to each.

- **Wild: Genesis ghost-writes the user's next ask** — FEATURE — value 4 — effort M — risk low — category: anticipation — wild
  Why: the blind-spots list (T-2073…T-2090) shows the user keeps asking for siblings of what shipped. Train a predictor on the ask history, queue top 3 predicted asks as deferred tasks, and score hit rate weekly.
  Done when: after a week, `fm genesis ghost --score` shows predicted vs actual asks with a hit rate.

- **Make the tower resumable by a stranger with only the repo** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: tower storage lives under fm genesis, not the repo. Add `fm genesis pack` to export the tower as a repo-local, hash-stamped bundle so a clone on another machine resumes correctly.
  Done when: cloning the repo plus the bundle on a clean machine and running `fm genesis status` shows the same generation and next step.

- **Wild: Self-hosting proof — Genesis rebuilds Foreman's own gen-0 from nothing and is graded against the hand-written one** — FEATURE — value 5 — effort M — risk low — category: proof — wild
  Why: the request's own exam: self-written gen-0 covers every MUST, NEVER and section of the hand-written one. Run it on a frozen Foreman snapshot with history withheld, and show the coverage table on the site.
  Done when: the coverage table lists every hand-written MUST/NEVER/section as covered, partial or missing, with at least 80% covered on a fresh snapshot.

Next question: Which of these bets would the user actually be comfortable running unattended overnight, and what receipt would let them trust it by morning?
Next question: What happens to a tower when the project's purpose pivots, and who decides gen-0 is now wrong?
