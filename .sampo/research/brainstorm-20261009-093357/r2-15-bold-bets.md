# Brainstorm — lens: bold bets

- **Backtest every idea against the ledger** — FEATURE — value 5 — effort M — risk low — category: judgement
  Why: Evidence: 835 ideas and 20+ captured tasks carry hand-guessed "value 4/5" scores, and the ledger holds real blocks, steers and friction. Existing ideas backtest instruction edits only; this extends the method to features. Assumption: ledger events are structured enough to match a predicate.
  Done when: `fm idea backtest C031` runs a stated predicate over the ledger, prints the matching event count and examples, and flags an idea with zero matches as "no evidence in history".

- **Keep one case file per task that every thinking pass writes into** — CLEAN — value 5 — effort L — risk med — category: architecture
  Why: Evidence: dozens of queued ideas (hypotheses, predictions, kill-criteria, dissent, assumptions, door types) would each add their own file and command, which cuts against the user's "cleanup never got done" complaint. Assumption: the briefs can host a validated schema.
  Done when: hypotheses, options with kill reasons, predictions and decisions live in one schema-validated file, `fm task lint` fails on a decision with no evidence or a prediction never scored, and at least 3 existing passes write there instead of to their own files.

- **Run Foreman's methods on a small workflow runtime** — FEATURE — value 5 — effort L — risk high — category: reasoning engine
  Why: Evidence: debugging, audit and planning are prose skills (72 of them), so compliance is hoped for and bench can only score a whole skill. Assumption: a handful of node types (probe, fan-out, vote, gate, ask, loop-until) is enough.
  Done when: the debugging ladder runs from a workflow file, emits a node-level trace, and `fm bench` scores a variant of one node in isolation.

- **Instrument first: add a tool-building agent before hard debugging** — FEATURE — value 4 — effort M — risk low — category: agent types
  Why: Evidence: 3 failed attempts → block is the current fallback, and fm-debugger is read-only and hypothesis-only. Assumption: a throwaway analyser (AST query, log slicer, call-graph script) often settles the question that guessing fixes don't.
  Done when: on a seeded intermittent bug, a fm-instrument lane writes a probe script, its output is attached as evidence, and the script is discarded unless reused twice.

- **Add an architect agent whose design ships with fitness functions** — FEATURE — value 4 — effort M — risk med — category: agent types
  Why: Evidence: no agent type owns design; L plans are written by the main thread. Existing layering and model-check ideas are gates, not an owner. Assumption: 2–3 executable checks per design is a workable size.
  Done when: an L FEATURE plan has a fm-architect design naming at least 2 executable fitness checks, which persist in the repo's gates and fail a later task that violates them.

- **Learn step size per task type** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: Evidence: "smallest next step" and the stuck ladder trigger only after failure. Assumption: the ledger shows first-pass rate by step count and file span.
  Done when: planning for a task type with past thrash splits steps to the learned size, and `fm task plan` shows the rule and the numbers behind it.

- **Find queued tasks that obsolete or undo each other** — FEATURE — value 3 — effort S — risk low — category: queue
  Why: Evidence: about 20 captured tasks overlap (C056 and C038, T-0446 and T-0445, the guard tasks). Conflict ideas so far cover files, not intent. Assumption: a cheap pairwise read of brief titles and approaches is enough.
  Done when: `fm queue overlap` lists pairs where building one rewrites or makes the other moot, with the sentence that shows it, and Drive skips ordering them wrongly.

- **Show the Pareto front of plans for L tasks** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: Evidence: intake requires 3+ options, but they are prose and not scored on shared axes. Assumption: cost, risk, surface added and reversibility can be estimated from bench history.
  Done when: an L brief shows its options as rows scored on those four axes, dominated options are marked, and the chosen option names its row.

- **Fake-door every idea before building it** — FEATURE — value 4 — effort S — risk low — category: product sense — wild
  Why: assumption: with a single power user, the cheapest demand test is a stub verb or button that says "not built yet, noted" and counts attempts. It would sort the pile by what the user actually reaches for.
  Done when: a captured idea can be armed as a stub, the stub records each use in the ledger and does nothing else, and `fm idea` ranks by real attempts over 14 days.

- **Show the live mind: an editable board of the current question, hypotheses and bets** — FEATURE — value 5 — effort L — risk med — category: desktop UI — wild
  Why: Evidence: the user steered toward the Tauri app with agent management, and asked for visible "thought process". Assumption: hypotheses and predictions are already structured, via the case file above.
  Done when: in the desktop app, striking out a hypothesis card injects a steer into the running session and the next ledger entry cites it.

- **Minimise each lesson by cheap-model replay** — FEATURE — value 4 — effort M — risk low — category: learning — wild
  Why: assumption: the shortest insight that lets a cold Haiku-class agent pass a replayed task is the lesson worth recalling. Lessons now grow unchecked, and fm bench can already replay tasks.
  Done when: a lesson is shortened by search until the replayed pass rate drops, and the stored version is the shortest that still passes in at least 2 of 3 runs.

- **Track a thinking clock per phase and learn the ratio that predicts first-pass success** — FEATURE — value 3 — effort S — risk low — category: metacognition
  Why: Evidence: profiling exists only as an idea, and the user's pace and budget steers show they care about time. Assumption: phase boundaries (understand, plan, build, verify) are recoverable from the ledger.
  Done when: `fm friction` reports, per task type, the time split of first-pass successes against reworked tasks, and intake warns when a plan skips the phase that successes spend longest on.

- **Run a request-dialect bake-off on the user's last 100 messages** — FEATURE — value 3 — effort M — risk low — category: intake
  Why: Evidence: the pack's steers ("trace why and fix", "shouldn't block anything until 75%") are terse and implicit. Assumption: past messages can be labelled with the outcome that followed.
  Done when: intake variants are replayed on those messages, and the one with the fewest later corrections is reported with the cases where they differ.
