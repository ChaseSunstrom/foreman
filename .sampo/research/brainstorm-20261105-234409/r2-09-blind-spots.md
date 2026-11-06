# Brainstorm — lens: blind spots

- **Pin which surface each missed ask hit before brainstorming the pack** — FIX — value 5 — effort M — risk low — category: coverage
  Why: T-3312 (Kalevala depth), T-3316 (headroom census), T-3321 (fleet claims on git refs) and T-3340 (measure what the user feels) were each asked by the user, not predicted. The question a brainstorm should have asked: “for each of these four asks, on which surface (CLI, web UI, phone, unattended) did the user hit the gap, and which lens owns that surface?” The class still missing: a per-surface “I had to say this myself” log that feeds the next pack’s blind-spot section, and a check that every open surface row in coverage.md names a missed ask it will close.
  Done when: the pack builder stamps each “what earlier brainstorms missed” line with its surface, and `fm genesis check` fails if a surface has a missed ask but no open cell.

- **Force the “below-20-briefs” question onto the whole decider before training** — FEATURE — value 5 — effort M — risk low — category: genericity
  Why: The user asked “what does a project with fewer than 20 briefs get from a shared model, and where is the line below which the model should say nothing?” — a question no brainstorm raised. The class still missing: an honest cold-start contract (retrieval-only, abstain, or sibling-seed) with a measured floor, a `sampo doctor` line naming the model’s confidence ceiling for the current repo, and a retire-when predicate that says “this project is too small for a model.”
  Done when: a fresh clone with 15 briefs shows “model: abstain, retrieval-only, n=15” in `sampo status`, and a canary test proves the model never emits a verdict below the floor.

- **Name the “who consumed this output” question for every gauge and print** — FIX — value 4 — effort S — risk low — category: docs
  Why: T-3353 (tonight’s lessons into prompts) and T-3342 (the .foreman/ mirror still named foreman) are docs/visibility gaps nobody predicted. The question: “who reads each printed number, in what grammar, and what do they do with it?” The class still missing: a consumer table for every gauge (user, model, hook, site), a “what I took you to mean” diff on each printed change, and a dead-reader check that lints prints nobody’s path consumes.
  Done when: every `fm` printed number has a `consumed-by:` tag, and a lint fails if a tag names a path that no session or surface reads.

- **Ask “what did this rename break on a live machine?” at every name change** — FIX — value 4 — effort M — risk med — category: security
  Why: T-3342 (36 code sites still name .foreman/) and the T-2967 guard path miss are the same class: a rename or migration that breaks on a live path no test covers. The question: “does every alias and old path still resolve on the user’s real home, and does the guard still protect it?” The class still missing: a rename ledger that lists every old name, every surface it appears in, and a retire-when predicate; a live-path probe in `fm doctor`; and a guard canary that fires on the new real path, not the symlink.
  Done when: `fm doctor` prints “alias foreman → sampo: 36 sites, guard: armed on real path,” and a kill-and-rename drill leaves the guard refusing the new path.

- **Run the “is the GPU busy?” question as a first-class scheduler** — PERFORMANCE — value 4 — effort M — risk low — category: performance
  Why: The user asked “what does the model path do when the GPU is busy with the moons funnel, and is the fallback measured?” No brainstorm predicted that the training, serving and funnel would share one GPU. The class still missing: a slot-pool scheduler that names the GPU, yields to the user’s model, and logs every preemption; a measured fallback (kNN, retrieval-only, rules) per slot; and a “GPU is busy, model: kNN” line in `sampo status`.
  Done when: the moons funnel at 100% GPU drops the decider to kNN within 2 s, the morning card logs “yielded 3×, fallback: kNN,” and the bench shows the fallback’s score.

- **Ask “which silent-cut does this training row contain?” before any model sees it** — SECURITY — value 5 — effort M — risk med — category: security
  Why: The user asked “which model decision is made from text a repo or tool wrote rather than the user, and can that text change the outcome without a ledger trace?” and “count every silent cut in the training pipeline.” No brainstorm predicted that a tool-written or silently-cut row could steer a model. The class still missing: a provenance tag on every row (user, tool, repo), a silent-cut counter in the pipeline, a quarantine for tool-written text, and a canary row that flips the model’s verdict to prove the trace works.
  Done when: every training row has a `source:` tag, the pipeline prints “silent cuts: 4, quarantined: 2,” and a planted tool-written canary is flagged before it reaches the model.

- **wild — Run a “stranger with 15 briefs” drill every Rune generation** — FEATURE — value 5 — effort M — risk med — category: genericity
  Why: The cold-start question (below) is only honest if tested by someone who hasn’t read MASTER.md. The question: “what does a user who has never seen this repo, on their 15th brief, need to see to know which slot is model-driven and how to turn it off?” The class still missing: a zero-context exam (a tool-less child reads only `sampo status` and the morning card and must name the model’s verdict and the off-switch), a “I don’t understand this line” log, and a retire-when the model stops helping a stranger.
  Done when: a cold child on a 15-brief repo names the decider’s verdict, its confidence, and the off-switch in under 60 s, and the pack’s blind-spot section quotes the child’s first “I don’t understand” line.

- **wild — Turn every “I had to say this” ask into a standing blind-spot class** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: The user’s own asks (T-3312, T-3316, T-3321, T-3340, T-3353) are a list of classes no brainstorm predicted. The question: “what is the class behind each ask, and what else in that class is still missing?” The class still missing: a `blind-spots.md` in the tower that names each class, the ask that surfaced it, and the open items it implies; a sweep that checks every open blind-spot class has an owner and a retire-when predicate.
  Done when: `blind-spots.md` lists at least 6 classes, each with its surface, its missed ask, and its open items, and `fm genesis check` names any class with no owner.

- **wild — Replay the user’s last 30 days of “I had to say this” moments as a held-out test** — FEATURE — value 5 — effort L — risk med — category: genericity
  Why: The blind-spot question is only useful if it can predict the next ask. The question: “can a model trained on the ledger predict the user’s next unsaid ask, and how far off is it?” The class still missing: a 30-day replay that scores the model against the actual asks, a per-surface hit rate, and a “predicted but not asked” shelf that shows what the model thought the user would say. The risk is overfitting to the user’s own style, so the replay must use a different model as judge.
  Done when: the replay prints “hit rate: 4/9, per surface: CLI 3/6, web UI 1/3,” and the morning card shows the top “predicted but not asked” item.

- **Ask “what does the user’s silence mean?” as a label, not a gap** — FEATURE — value 4 — effort M — risk med — category: unspoken needs
  Why: The user asked “what does a project with fewer than 20 briefs get?” and “which model-backed slot has the worst failure when it is silently wrong?” — both are about silence. The question: “when the user says nothing for 48 h, is that acceptance, abandonment, or confusion?” The class still missing: a silence classifier (accept / abandon / confused) trained on the ledger’s own follow-up words, a “silence means” line in `sampo status`, and a retire-when the classifier’s error rate exceeds a threshold.
  Done when: `sampo status` prints “silence: accept (48 h, 3 prior accepts)” on a closed task, and a canary test proves the classifier flips on a planted “I’ll re-ask later” message.

- **wild — Let the user’s undo be the only label, and the model’s job be to predict it** — FEATURE — value 5 — effort L — risk high — category: training
  Why: The user asked “what does the user’s cost of being wrong mean, not accuracy?” and “can that text change the outcome without a ledger trace?” Both point to the undo as the ground truth. The question: “is the user’s undo a stronger label than the test going green, and does the model know it?” The class still missing: a negative label from every undo, a “model predicted, user undid” regret ratio per slot, a canary that undoes a task and checks the model flags it, and a retire-when the regret ratio exceeds a threshold.
  Done when: every undo lands in the training lake as a negative, the morning card prints “regret: 2/12 this week,” and a planted undo is flagged by the model within one session.

- **Ask “what breaks when I say no to this steer?” at the moment the steer is stored** — FIX — value 4 — effort S — risk low — category: docs
  Why: The user asked “what does a user who never read MASTER.md need to see?” and “what does the model do when the GPU is busy?” — both are about the cost of a decision. The question: “what breaks if I turn this steer off, and what does that cost?” The class still missing: a “what breaks” line on every steer, a “cost of being wrong” gauge per steer, and a retire-when the steer’s cost drops below a threshold.
  Done when: every steer in `steers.md` has a `what-breaks:` line and a `cost:` number, and `fm doctor` flags any steer with no `what-breaks`.

- **wild — Run a “no model, no Sampo” week and log every ask the user had to make** — FEATURE — value 5 — effort M — risk med — category: blind spots
  Why: The whole blind-spot class is about asks the user had to make. The question: “what does the user ask for when Sampo is off, and what does that reveal about what Sampo should do?” The class still missing: a one-week ablation where Sampo is disabled, every user ask is logged, and a diff against the last week with Sampo on. The risk is disrupting the user’s work, so the ablation must be opt-in and logged as a “wild” drill.
  Done when: the ablation week logs every ask, the morning card prints “Sampo off: 7 asks, Sampo on: 2 asks, diff: +5,” and the pack’s blind-spot section names the top 3 asks Sampo should have predicted.

- **Ask “what does the next user on this project need to see?” at every Rune generation** — FEATURE — value 4 — effort S — risk low — category: genericity
  Why: The user asked “what does a user who never read MASTER.md need to see?” and “what does a project with fewer than 20 briefs get?” Both are about the next user, not the current one. The question: “what does the next person who uses this repo need to see to trust the model?” The class still missing: a “next user” card in `sampo status` that names the model’s verdict, its confidence, the off-switch, and the “what breaks” line; a retire-when the next user’s hit rate drops below a threshold.
  Done when: `sampo status` prints a “next user” block with verdict, confidence, off-switch and “what breaks,” and a cold child reads it in under 60 s.

- **wild — Let the model draft the user’s next “I didn’t ask for that” pushback before it is said** — FEATURE — value 5 — effort M — risk high — category: unspoken needs
  Why: The user asked “which model-backed slot has the worst failure when it is silently wrong?” and “what does the user’s cost of being wrong mean?” Both are about the pushback that hasn’t been said yet. The question: “can the model predict the user’s next pushback, and what does that reveal about the model’s blind spots?” The class still missing: a pushback predictor that drafts the user’s next “I didn’t ask for that” from the ledger, a “predicted pushback” line in the morning card, and a retire-when the predictor’s hit rate exceeds a threshold (meaning the model is too accurate to be useful).
  Done when: the morning card prints “predicted pushback: ‘you touched the guard again, I said no’” and the user’s actual pushback matches within 24 h; the pack’s blind-spot section quotes the predicted pushback.

Next question: for each of the six “what earlier brainstorms missed” tasks, which surface (CLI, web UI, phone, unattended) did the user hit the gap on, and which lens owns that surface?
Next question: what is the measured floor below which the decider should abstain on a project with fewer than 20 briefs, and which canary test proves it?
