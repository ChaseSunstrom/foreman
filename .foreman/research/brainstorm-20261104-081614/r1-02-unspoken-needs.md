# Brainstorm — lens: unspoken needs

- **Ship a calibrated "will this close hold?" scorer** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: Smith's new close scaffold produced "many false-done" (closes 4→5 with 1/8 fixed). Every closed brief records whether it later got a fix or revert, which is a free label that isn't Claude's text. The user will want the done-gate to say "I doubt this".
  Done when: on held-out projects, the scorer's AUC at predicting a later-fix or revert beats a majority and a test-exit-code-only baseline, and `fm task finish` shows its score.

- **Make every model abstain, with a measured coverage-vs-accuracy curve** — FEATURE — value 5 — effort S — risk low — category: calibration
  Why: nothing beats majority on tier (0.58) and intake type only reaches 0.73. A decider that always answers is worse than one that says "ask the big model". Assumption: the user wants fewer wrong auto-decisions, not more answers.
  Done when: each decision head emits a confidence, and on the 200-task bench the answered subset reaches ≥0.85 accuracy at a reported coverage.

- **Hold out whole projects and strip names in the training build** — SECURITY — value 5 — effort M — risk med — category: generality
  Why: the user said "not just the sampo repo". Sampo is 1,767 of 4,078 briefs, so a naive split learns Sampo's vocabulary. The pack states generality must be proven by holding out projects.
  Done when: `sampo model bench` reports leave-one-project-out scores per project, and a test shows a name-scrubbed brief and the raw one differ by <1 point.

- **Add a per-project consent flag that the trainer enforces** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the constraints say a sensitive project's data never leaves the machine and may be excluded. Nothing yet records which of the 13 projects is which. Assumption: the voice-assistant codebase may be private.
  Done when: a project marked `no-train` yields zero rows in the dataset build, and a test fails if the flag is ignored.

- **Learn the user's accept/reject history as an interruption filter** — FEATURE — value 5 — effort M — risk med — category: user model
  Why: the standing rules say "never interrupt the user mid-run" and "never block on the user". The ledgers hold 149k lines including asks, answers and steers. A model that predicts "the user would say yes" lets the drive proceed with `fm decide` and keeps the user out of the loop.
  Done when: on held-out ask/answer pairs it predicts the user's answer above the majority baseline, and the report lists every auto-answer it made.

- **Gate adoption through a registry with one-command rollback** — FEATURE — value 4 — effort M — risk low — category: lifecycle
  Why: "adopted only where the bench shows it leads" and "every Rune generation retrains and re-benches". Without a registry of model, data hash, bench and slot, each generation becomes a manual comparison.
  Done when: `sampo model status` lists each slot's active model with its bench, and `sampo model rollback SLOT` restores the previous one in one step.

- **Share the GPU: schedule training around the moons funnel and exams** — PERFORMANCE — value 3 — effort M — risk med — category: scheduling
  Why: one 16 GB card serves Ollama, the Jeff stack and the 10k moons run, and a remote model switch costs ~3 min. Training will collide with a run already in flight. Assumption: LoRA on 0.6–4B fits only when Ollama is idle.
  Done when: a training job queues behind a running funnel, resumes after, and a test shows no OOM kill of either job.

- **Distil only verified Smith runs, and keep every refusal as a negative** — FEATURE — value 4 — effort L — risk med — category: distillation
  Why: loops are the main end (4/10 exam runs) and the 27B traces have exit codes. Runs that looped or closed falsely are labelled data for the loop breaker, so they shouldn't be discarded.
  Done when: the dataset holds green runs as positives and looped or false-done runs as labelled negatives, and the loop breaker's head beats the current repeat-action rule on held-out runs.

- **Seed a new project from its nearest siblings (wild)** — FEATURE — value 4 — effort M — risk med — category: cold start
  Why: assumption: a project with 5 briefs has no data of its own. bge-m3 title→brief recall@1 is 0.85, so the first brief can borrow priors from the closest projects' briefs and lessons, scrubbed of names.
  Done when: on a project with <10 briefs, the borrowed priors beat the generic model on the next 10 tasks' intake type.

- **Fine-tune a small adapter per project over the shared base (wild)** — FEATURE — value 4 — effort L — risk high — category: personalization
  Why: volt has 773 briefs and the git tool 143, enough for a project-local LoRA that never leaves the machine. It only ships if it beats the generic head on that project's held-out tail.
  Done when: a per-project adapter is built, benched against the base, and dropped automatically when it doesn't win.

- **Train a "user twin" that drafts steers before they are said (wild)** — FEATURE — value 4 — effort L — risk high — category: foresight
  Why: steers are the user's strongest signal. The steer-expansion exam already exists, and foresight already predicts the next request. A model trained on steer history could propose "you will want X" as filed drafts, not actions.
  Done when: on held-out dates, ≥1 in 5 of its drafts matches a steer the user later gave, scored by a cold judge.

- **Run overnight self-play on replayed commits (wild)** — FEATURE — value 3 — effort L — risk med — category: self-improvement
  Why: the long-horizon tier already rolls back real repos to past commits. Unattended runs on those replays could produce verified traces for each Rune generation, at zero dollar cost.
  Done when: one overnight run yields N verified traces into the dataset with dedupe and no manual step.

- **Detect training-text injection before it enters the corpus** — SECURITY — value 3 — effort S — risk low — category: poisoning
  Why: the briefs include raw requests and pasted content. A pasted instruction that is trained in could steer the decider or the Ward. This answers the earlier question about a shared text channel. Assumption: no ledger shows it yet.
  Done when: a planted "ignore the rules" row is quarantined from the build and listed in the dataset report.

- **Report drift per project so retraining isn't blind** — FEATURE — value 3 — effort S — risk low — category: monitoring
  Why: every Rune generation retrains, but a project's vocabulary and task mix shift. Without drift alarms the bench could stay green on stale data.
  Done when: `sampo model drift` flags a project whose recent briefs score >X below its training-era score, and doctor names it.

Next question: Which of the 4,078 briefs' outcome labels (done, blocked, reverted, later fixed) are actually trustworthy, and does the model's label noise differ across the 13 projects?
Next question: What does a user see the first time a trained slot overrides a rule-based one, and how would they know it did?
