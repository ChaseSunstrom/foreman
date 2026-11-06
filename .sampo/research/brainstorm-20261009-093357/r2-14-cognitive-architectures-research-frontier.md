# Brainstorm — lens: cognitive architectures (research frontier)

- **Resolve impasses with typed subgoals, then chunk the result** — FEATURE — value 5 — effort L — risk med — category: reasoning core
  Why: the pack's stuck handling is a flat "3 failed attempts → block" plus a proposed stuck ladder; nothing turns a solved impasse into reusable skill. Soar's universal subgoaling is the missing piece. Each impasse (tie between approaches, no applicable step, conflicting criteria, a gate that can't fail) opens a subgoal with its own specialist and a bounded budget. The resolution is cached as a chunk keyed on a state signature (task type, failing check, files) and consulted before the next impasse of that shape. Assumption: signatures can be derived from ledger events.
  Done when: replaying a bench task with a seeded impasse resolves via the cached chunk with zero subgoal agents spawned, and the ledger records the chunk id.

- **Recall by activation, not text match** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: `fm recall` is BM25 over past briefs, lessons and failures. ACT-R activation scores instead combine recency and frequency decay with spreading activation from the current context (open files, the co-change graph, the active step). Lessons tied to code being touched surface without matching words, and stale ones fade without hand-pruning. Assumption: co-change data from `fm map` is usable as the spreading graph.
  Done when: on a bench of past tasks, activation recall ranks the lesson that preceded a first-time pass in the top 3 more often than BM25 does, and `fm recall --why` shows each score's terms.

- **Auction context admission through a global workspace** — FEATURE — value 4 — effort M — risk med — category: context
  Why: many sources inject notes (lessons, vetoes, tripwires, hook warnings, lane results), and T-0044 already worries about injection quality. In global-workspace theory, specialists bid with a salience score and only the top few are broadcast to the main thread in a fixed token budget. Bids come from relevance to the current step, severity, and novelty (not shown this session). The ledger keeps losing bids so ablations can check what was dropped. Assumption: bid inputs are cheap to compute inside hooks.
  Done when: per-turn injected tokens never exceed the budget, and `fm friction` lists the top suppressed bids with a count of times each later proved relevant.

- **Run a critic–selector layer over the ledger** — FEATURE — value 4 — effort L — risk med — category: metacognition
  Why: Minsky's model has critics that recognise a kind of trouble and selectors that switch the way of thinking. The pack has many one-off passes (audit, debate, spike) but nothing that notices *when* to run which. Critics are cheap ledger-pattern matchers such as scope creep, repeated reads without edits, plan-vs-diff divergence, and rising user corrections. Each critic names a selector (replan, spike, ask, second opinion, shrink step). Which critics ever changed an outcome is tracked so dead ones are deleted. Assumption: ledger events carry enough signal.
  Done when: three seeded trouble patterns each fire the correct critic within a bounded number of events, and a critic that never changes an outcome over N tasks is flagged for removal.

- **Route by a feeling-of-knowing probe** — FEATURE — value 4 — effort M — risk med — category: metacognition
  Why: SOFAI-style arbitration. Before planning or reading, a cheap probe estimates familiarity (a near-duplicate solved task, a covered area, a recorded chunk). High familiarity takes a reflex path (reuse the plan skeleton, light verification). Low familiarity takes deliberate recon, a premise check, or a second opinion. The probe is scored against actual rework, so the thresholds are learned. Assumption: briefs plus outcomes give enough labels.
  Done when: bench tasks split into reflex and deliberate routes, and the reflex route's rework rate is no worse than the baseline at lower median token use.

- **Snapshot situation awareness at step boundaries** — FEATURE — value 3 — effort S — risk low — category: reasoning
  Why: Endsley's three levels (perceive, comprehend, project) map onto what the resume and compaction path loses. A 10-line snapshot stored at each step boundary holds the facts observed, what they mean for the criteria, and what will probably happen next. The next snapshot is diffed against the last, and unexplained deltas become notes. This also gives `/compact` a curated handoff. Assumption: the existing step records can hold it.
  Done when: after a forced `/compact`, the resumed session's first action cites the last snapshot's projection, and a diff with an unexplained fact raises a note.

- **Run a cognitive battery of faculty micro-evals** — FEATURE — value 4 — effort M — risk low — category: evals
  Why: the bench replays whole tasks. A psychology-style battery isolates faculties: set-shifting (the requirement changes mid-task), inhibition (resist the tempting wrong fix), working-memory span (N simultaneous constraints), source monitoring (who said what), and calibration. Each is a small deterministic scenario with a scored result per model and instruction version. The scores feed `fm evolve` and model-upgrade decisions. Assumption: scenarios can run in `fm bench` harness fixtures.
  Done when: `fm bench --battery` prints a per-faculty score table and a seeded regression in an instruction file lowers the matching faculty's score.

- **Measure working-memory span and size plans to fit** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: assumption: brief violations rise past some number of live constraints, and the pack hints at this (oversized briefs get split, criteria are dropped, T-0317-style misses). From transcripts, compute violations as a function of open criteria, vetoes and files in play per model. Intake then caps constraints per step or lane at that knee and splits above it. Fewer silent drops on L work.
  Done when: for a replayed set of L tasks, a plan above the measured span is split automatically, and the criteria-miss rate on split plans is lower than on the unsplit baseline.

- **Map problems by relational structure to find cross-project analogues** — FEATURE — value 3 — effort L — risk med — category: analogy
  Why: recall by text finds similar words, not similar problems. A task is encoded as a small relational graph (what depends on what, what changed, what failed). Structure-mapping then retrieves a solved task with the same shape, possibly in another project, and transfers its plan skeleton with explicit "mapping breaks here" notes. This is the reasoning behind "transplant a fix", made general. Assumption: briefs and diffs are structured enough to graph.
  Done when: for a held-out task, the retrieved analogue shares no keywords with it but its plan skeleton, once adapted, covers at least half of the final steps.

- **Drive attention from an affect-like appraisal state** — FEATURE — value 3 — effort M — risk med — category: control
  Why: the ledger already has the raw appraisals, such as novelty, goal progress, perceived control (gate passes against failures), and time pressure. Compute them as a small state and let them set dials: low control raises exploration and shrinks the step, high novelty raises verification strictness, high progress allows batching. This is a principled replacement for fixed thresholds like "3 failures". Assumption: these dials are tunable through settings.
  Done when: a seeded run with rising failures changes step size and verification level before the third failure, and the state is visible in `fm status`.

- **Wild: Use one expected-uncertainty currency for every action choice** — FEATURE — value 4 — effort L — risk high — category: active inference
  Why: wild. The pack has separate rules for when to read, probe, ask the user, run a test, spawn a scout or deliberate. An active-inference scheduler scores each candidate action by expected reduction in uncertainty over the open criteria and hypotheses per unit cost, and takes the best. The ask-the-user cost comes from the attention meter. This gives a single explainable "why this next".
  Done when: on 20 replayed steps, `fm why-next` ranks the actions, and the top-ranked one matches a human-judged good move in a majority of cases.

- **Wild: Recombine distant memories in a night "REM" pass** — FEATURE — value 3 — effort M — risk low — category: creativity
  Why: wild. Dream passes replay failures, but REM-like sleep forms remote associations. A tool-less pair of children is given two unrelated lessons or decisions from different projects and asked for a transfer hypothesis. Candidates are bench-gated, and survivors are queued as proposals, never applied silently. Assumption: enough cross-project lessons exist.
  Done when: a night run emits a list of cross-lesson hypotheses, each with a bench result, and at least one is promoted or rejected with evidence.

- **Wild: Detect "aha" moments and promote them instantly** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: wild. Insights show up as a sudden drop in uncertainty: a long thrash followed by a one-line fix, a reversed hypothesis, or a new term appearing in the reasoning. Spot that signature in the ledger, capture "what I now believe and what made me change it" at once while the context is fresh, and queue it as a draft lesson with the probation flow. Assumption: the signature is detectable from events like hypo state changes.
  Done when: a replayed FIX task with a reversed hypothesis produces a draft lesson that names the old and new belief and the disconfirming evidence.
