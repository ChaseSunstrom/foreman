# Brainstorm — lens: approaches

Answers to two earlier questions from this lens (from the pack only):

- **Which jobs need to run on time:** the pack suggests settled bets and the digest, since calibration windows are 30 days. Everything else can be eventual. I assume this; the pack has no usage data.
- **Which tick outputs can be settled outside Foreman:** the pack names none. CI and forge events are the natural candidates, and nothing in it says they are wired to a grade.

Approaches, best first. Each one is a distinct way to get a complete plan and an honest "done":

- **Gate goal birth on prior art** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: assumption: the pack shows row-level "adopt/skip" ideas but nothing at goal level. A goal that already exists as a finished OSS tool should be adopt/fork/build before any plan is written. Trade-off: one extra search step, and it can be wrong about fit.
  Done when: `fm goal new "<vague goal>"` prints a prior-art block (up to 5 candidates, each with adopt/fork/build) before any plan rows exist, and a fixture goal with a known library lists that library.

- **Land every row dark behind a flag** — FEATURE — value 4 — effort M — risk med — category: stop-safety
  Why: assumption: the pack says plans must survive days and crashes, and a mid-goal stop shouldn't change main's behaviour. Rows land default-off and finish flips them in one reviewed commit. Trade-off: flag plumbing for every row, which doesn't suit refactors.
  Done when: in a fixture goal stopped after row 3 of 6, main's behaviour is unchanged and `fm goal finish` flips all flags in one commit.

- **Bake off planning methods on closed goals** — FEATURE — value 4 — effort M — risk low — category: plan quality
  Why: the pack has competing decompositions (one-shot, survey+merge, waves) but no data choosing between them. Run each method on the last N closed goals and score by rows later added as scope growth. Trade-off: needs enough closed goals, which is an assumption.
  Done when: `fm goal bakeoff` prints a per-method miss rate on ≥5 closed goals and the default method is set from it.

- **Run a null-engine arm against the goal engine** — CLEAN — value 4 — effort S — risk low — category: do-less
  Why: the pack's steers want subtraction by evidence, and no comparison exists between the engine and a plain `goal.md` plus a resume prompt. Run a kill-and-resume drill on both. If the plain file recovers within a set margin, retire the extra goal verbs. Trade-off: the drill is only as good as its planted faults.
  Done when: one drill report shows engine versus plain-file resume success on the same kills, with the verbs to keep or cut named.

- **Rank rows by documentation weight in rival docs** — FEATURE — value 3 — effort M — risk low — category: prioritisation
  Why: assumption: the pack ranks by the user's minutes lost and by demand evidence, but not by how much space each capability gets in best-in-class docs (headings, pages, examples). It is a zero-token proxy for what users need. Trade-off: docs overstate marketing features.
  Done when: given three rival doc trees, the tool outputs a ranked capability list with heading counts, and the top three land as must-rows.

- **Cap planning spend as a share of build spend** — FEATURE — value 3 — effort S — risk low — category: budget
  Why: assumption: the pack shows plan churn gauges but no stop-loss on planning itself. If planning exceeds, say, 15% of the estimate, it forces a first walking-skeleton row. Trade-off: the threshold is a guess until data exists.
  Done when: a fixture goal whose planning passes the cap gets a printed "start building" decision, and the cap is recorded in the plan.

- **Force a decision on the third deferral of a row** — FEATURE — value 3 — effort S — risk low — category: plan debt
  Why: the pack has about 30 "later: needs…" deferrals that wake only on a human's memory. A row deferred three times must be cut, spiked or given a wake predicate. Trade-off: it can nag on rows that are legitimately parked.
  Done when: the third deferral of a fixture row is refused without a cut, spike or wake predicate.

- **Require two keys for "done"** — FEATURE — value 3 — effort S — risk low — category: finish verdict
  Why: the pack proposes an oracle, a cold child and a shell-only recompute separately. Done needs the oracle green and an independent shell recompute agreeing, with disagreements logged as a typed stop reason. Trade-off: it is stricter, so goals finish later, and it needs the oracle to be computable in shell.
  Done when: a fixture where the oracle passes and the recompute fails ends as "stopped: keys disagree", not "done".

- **Detect padding by the novelty of new plan rows** — FEATURE — value 3 — effort S — risk low — category: plan integrity (wild)
  Why: wild. The pack's adversary lane could pass the sweep with 58 cheap cells, and its templating test is a 20-line shingle overlap. Compress the plan with gzip and flag rows that add near-zero extra bytes (pure rewording). No tokens spent. Trade-off: it also flags legitimately terse rows.
  Done when: a fixture plan of 30 distinct rows plus 20 reworded duplicates is flagged on the duplicates and passes the original 30.

- **Drive the rival product black-box to extract the contents** — FEATURE — value 4 — effort L — risk high — category: plan contents (wild)
  Why: wild. The pack plans from docs and memory, but not from using the best-in-class product. Install it in a sandbox, have a cold child drive its CLI or web UI and record each observed behaviour as a candidate row. Trade-off: licensing, a heavy install, and it only works when the product runs locally.
  Done when: against a fixture CLI with 12 planted behaviours, the extraction recovers ≥10 as rows.

- **Forecast the first month's issue tracker as rows** — FEATURE — value 3 — effort M — risk low — category: plan contents (wild)
  Why: wild. A tool-less child writes 20 plausible user issues for v1.0, seeded by the user's own past issues. Each deduped issue becomes a candidate row, and the plan records which were kept. Trade-off: the model's guesses can echo its priors, so the user's real issues need to be in the seed.
  Done when: running it on a closed goal produces ≥3 candidate rows that match issues actually filed later.

- **Run a stub user for a simulated week on a fixture build** — FEATURE — value 3 — effort L — risk med — category: finish verdict (wild)
  Why: wild. Done is judged by a stub user who knows only the steers and the goal sentence and works the product for a scripted week. Their written complaints are the remaining rows. Trade-off: it costs tokens and the stub's tastes are invented.
  Done when: against a fixture product with 2 planted flaws, the stub's complaint list names both.

Next question: Which goals has the user actually closed so far, and how many were later re-opened or grew in scope, so the bake-off and the null-engine arm have a real corpus?
Next question: Does `fm` currently run on the committed library or the working copy when a goal row is resumed after a crash, and could the two disagree about what "done" means?
