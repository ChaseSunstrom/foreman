# Brainstorm — lens: learning from outcomes

- **Join plan steps to their fates in a step-level outcome table** — FEATURE — value 5 — effort M — risk low — category: outcomes
  Why: the ideas list has outcome ledgers and stage attribution, but nothing at plan-step granularity. Steps retried, reverted, or later "reworked" are never tied back to the plan shape that produced them. Assumption: the ledger already has per-step events, since resume works at the exact step.
  Done when: `fm outcomes steps` lists, for the last 50 finished tasks, each step type with its retry rate, revert rate and rework rate, and the numbers match a hand count on 3 sampled tasks.

- **Make plan templates earn their place by outcome** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: assumption: intake picks approaches and step shapes from prose rules, with no feedback on which shapes finished first-time-clean. Past tasks are replayable via fm bench.
  Done when: for each task type, `fm plan --stats` shows first-pass rate per decomposition shape, and the intake skill cites the best-performing shape when its sample is at least 5.

- **Trace each lesson to the failure it was born from and the failure it later prevented** — FEATURE — value 4 — effort M — risk low — category: lessons
  Why: T-0217 gives lessons a confidence number, but a number alone won't show whether a lesson did anything. A lesson with a birth failure and a "saved" record can be defended or retired on evidence.
  Done when: `fm lesson show <id>` prints the origin task, every later task where recall surfaced it, and whether each of those passed first time. A lesson with no saves after 20 tasks is flagged.

- **Run a post-merge reality check at 24h and 7d** — FEATURE — value 5 — effort M — risk low — category: closed-loop
  Why: "done" is graded at the moment of closing, but the user's next message is where the real verdict lives (rework, a reopen, a steer). A delayed check turns that into data. Assumption: git history and the inbox can show later touches to the same files.
  Done when: a task finished 7 days ago gets an automatic verdict of stuck, touched-again, or reverted, and that verdict feeds the first-pass rate in `fm friction`.

- **Classify each user correction by the stage that should have caught it** — FEATURE — value 5 — effort M — risk med — category: corrections
  Why: the pack records steers such as "cleanup never got done" and "budget limits shouldn't block until 75%". Each is a failure that intake, plan, verify or the gate should have stopped, and the root cause is rarely logged by stage.
  Done when: every steer gets a stage tag (intake, plan, execute, verify, gate or policy). `fm friction` shows the per-stage counts, and the top stage proposes one concrete fix task.

- **Add a wrong-turn registry mined from reverted commits and abandoned lanes** — FEATURE — value 4 — effort M — risk low — category: dead-ends
  Why: reverts and discarded lane worktrees record an approach that failed, but the reason is lost. Plan time never consults them. This differs from the "dead-end atlas" idea by being mined automatically rather than curated.
  Done when: planning a task that touches files with a recorded dead end prints the earlier approach and why it was dropped. A seeded revert shows up in the next plan on that file.

- **Compare a planned footprint with the real one, and learn the correction factor** — FEATURE — value 3 — effort S — risk low — category: estimation
  Why: briefs carry a tier (S/M/L) and steps, and the diff gives the truth. Under- and over-scoping by task type is a learnable bias. Assumption: the diff-derived tier idea has not yet been joined to the plan's stated file list.
  Done when: `fm calibrate` reports the median ratio of actual to planned files and lines per task type, and intake applies the factor with a visible note.

- **Keep an agent-handoff yield table: which sub-agent outputs the main thread used or threw away** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: delegation ROI is mentioned, but not the fate of each returned artifact. If fm-recon findings are mostly ignored, it should spawn less. If fm-reviewer findings keep getting fixed, it should spawn more.
  Done when: every agent return is marked used, partly used or discarded when the task closes, and `fm agents --yield` ranks agent type by the share used per token spent.

- **Wild: Hold a replayed "what-if I'd listened" for every ignored warning** — FEATURE — value 3 — effort L — risk med — category: counterfactual
  Why: wild. Reviewer findings and risk entries that were dismissed are never scored afterwards. Replay the task with the warning obeyed and measure the difference. Assumption: fm bench can fork a task at one decision.
  Done when: for 5 dismissed warnings, the replay reports whether obeying would have changed the gate result or later rework, and the dismissals that turned out wrong feed reviewer weighting.

- **Wild: Give Foreman a seasonal report card written to its future self** — FEATURE — value 3 — effort S — risk low — category: reflection
  Why: wild. Instead of one "what I'd do differently" per task, a monthly document synthesises recurring misses, retired rules, proven rules and the three habits to change. It is injected at session start in under 300 tokens.
  Done when: running `fm retro --month` writes a card of at most 300 tokens. A bench replay with the card injected is compared against one without, and the delta is recorded.

- **Wild: Let the user's silence count as a signal, with a per-task "no complaint" streak** — FEATURE — value 3 — effort S — risk med — category: implicit-feedback
  Why: wild. Complaints are logged, but quiet acceptance isn't. A task the user built on, or never reopened, is weak evidence the approach worked. The same signal weights lessons and plan templates. Assumption: the next-message labelling idea doesn't cover silence over days.
  Done when: each finished task shows an acceptance state (built-on, untouched, or contested). Contested tasks lower the confidence of the lessons that were recalled for them.

- **Wild: Run a "same bug twice" detector that prosecutes the earlier fix** — FIX — value 4 — effort M — risk low — category: recurrence
  Why: wild. When a new FIX matches an old one by symptom fingerprint, Foreman opens a case against the earlier closed task. It asks why the fix, test or lesson didn't hold, then records which gate should have failed.
  Done when: filing a FIX similar to a closed one links the two, auto-creates a "why did it recur" finding, and adds a regression test proposal.

- **Gate lesson injection on measured benefit, per task type** — PERFORMANCE — value 3 — effort M — risk low — category: context
  Why: lessons are recalled by BM25, so relevance is textual, and context is finite. Ablation results (the earlier "attribute outcomes by ablation" idea) should decide which lessons are injected for which type of task. Here that means a retained-lesson budget per task type.
  Done when: injection per task type is capped to the lessons with a positive measured effect. A report shows the tokens saved and no drop in first-pass rate over 20 tasks.
