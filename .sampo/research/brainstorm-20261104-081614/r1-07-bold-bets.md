# Brainstorm — lens: bold bets

- **Train one shared Sampo Head, scored leave-one-project-out** — FEATURE — value 5 — effort M — risk med — category: decider
  Why: intake type reaches only 0.73 vs 0.595 majority and nothing beats majority on tier, and one project is 43% of the data. A single bge-m3 embedding with several small heads (intake type, tier, playbook, risk, next request) trained on 12 projects and tested on the 13th shows whether it generalises. Assumption: shared structure across projects is enough for the heads to transfer.
  Done when: on a project held out of training, intake type beats that project's majority baseline by at least 0.10, and the report prints the per-project table.

- **Build a false-done judge from later-fix labels** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: Smith's new close scaffold raised closes 4→5 with many false-done, and the briefs record "later fixes", reverts and evidence exit codes. Label closes that were later reverted or re-fixed as false-done, and train on brief, evidence and diff summary. Strips Claude's text from inputs, so only outcomes and local traces are used.
  Done when: AUC above 0.75 at predicting later-fix on held-out projects, and Smith's close step consults it and blocks flagged closes in a Louhi run.

- **Distil Smith's actor from green-only runs, with rejection sampling** — FEATURE — value 5 — effort L — risk med — category: Smith
  Why: T-2971. The 27B and 12B generate runs over Louhi train scenarios and real S tasks, and only runs whose tests passed and whose closes held are kept as SFT data. A LoRA on a 4–9B model goes through jeff-train. Local-model traces avoid the Claude-output terms.
  Done when: the tuned 4B or 9B fixes more held-out Louhi scenarios than its base (qwen3.5:4b is at 0/8 alone), with no rise in false alarms.

- **Predict a loop or dead run from the journal prefix** — FEATURE — value 4 — effort S — risk low — category: Smith
  Why: loops are the main end of runs (4/10) and the T-2966 breaker only fires on the third identical action. A small sequence classifier over 74 journals plus the new Louhi runs fires after step 3 or 4 and escalates to the planner early.
  Done when: it flags at least 70% of runs that later looped at under 20% false positives, and median steps-to-escalate drops in a Louhi rerun.

- **Add a cost-aware model router trained on outcomes** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: the fleet has 4B, 12B, 27B, a 35B MoE with a 3-minute switch cost, and Claude, with $0 spend by default. Learn from brief features and past outcomes which rung first passes at the lowest cost, and fall back through the ladder. Assumption: enough per-model outcomes exist (Louhi arms plus Smith journals).
  Done when: on held-out tasks the router matches always-27B pass rate at no more than 60% of the model-seconds.

- **Run a nightly Rune retrain with a registry and automatic rollback** — FEATURE — value 5 — effort M — risk med — category: lifecycle
  Why: "every Rune generation retrains and re-benches" and "adopt only where the bench leads". Build a versioned model registry, a frozen held-out set that is never trained on, adoption by bench lead only, and a rollback on regression. The sweep and `sampo doctor` report it.
  Done when: a generation produces a signed manifest with data hash, bench and adopted/rejected verdict per head, and a deliberately worsened candidate is rejected automatically.

- **Provide a sensitivity-aware data pipeline with name stripping** — SECURITY — value 5 — effort M — risk med — category: data
  Why: a sensitive project's data must never leave the box and must be excludable, and the model has to be generic. Replace repo-specific names with placeholders, tag each project train/eval/never, and prove the stripping works by checking the score drop when names are put back. Assumption: a per-project flag can be set in project config.
  Done when: a project marked never contributes zero rows to any training file (checked by a test scanning outputs), and a seeded canary string never appears in model inputs.

- **Fine-tune the embedder contrastively on briefs and lessons for cross-project recall** — FEATURE — value 4 — effort S — risk low — category: recall
  Why: title-to-brief recall@1 is 0.85 and each project's lessons could help the others (compiler lessons for the game). Train on title/brief/lesson pairs and measure retrieval across projects.
  Done when: cross-project lesson recall@5 beats stock bge-m3 on held-out projects, and `sampo next` or the playbook surfaces one such lesson in a real session.

- **Train a preference model on the user's accept/reject history to prefilter the funnel** — PERFORMANCE — value 4 — effort M — risk med — category: moons
  Why: an earlier question asks whether cheap funnel stages kill what the user later rejects. Learn from accept/reject, steers and drops, then rank candidates before any 27B judge call. This cuts cost as moons rise 100×.
  Done when: at the same recall of user-accepted moons, it removes at least 50% of candidates before judging, and the judge-call count drops in a funnel run.

- **Train a Ward risk head on guard refusals and test it adversarially** — SECURITY — value 4 — effort M — risk high — category: guard
  Why: the ledgers have guard refusals, and the T-2967 core-path bug shows rule gaps. A learned second opinion catches paraphrased variants, but it must never override a deterministic refuse. Question left: whether the Ward and funnel models can be attacked through the same text channel.
  Done when: a red-team set of obfuscated risky commands is flagged at a higher rate than the rules alone, with a false-refuse rate the user's ledger tolerates, and the rules still decide alone when the model is off.

- **Build the Kev-twin: a model that answers asks as the user would** — FEATURE — value 5 — effort L — risk high — category: autonomy — wild
  Why: the user is often away, the standing rule says never interrupt, and asks, answers and steers are in the ledgers. A twin trained on those predicts the user's answer with a confidence. High confidence answers go through `sampo decide --kind costly` for the final report; low confidence waits.
  Done when: on held-out ask/answer pairs it matches the user's real answer at least 80% when confident, and every twin-made decision is listed in the report.

- **Run a bug-planting adversary for infinite Louhi scenarios** — FEATURE — value 4 — effort L — risk med — category: exam — wild
  Why: Louhi has 18 runs in six languages, too few to train on and tied to hand-made scenarios. A model plants realistic bugs in any Sampo project's repo, and only plants where tests turn red and a fix exists are kept, giving unlimited verified training problems and a curriculum.
  Done when: it generates 50 scenarios on a project outside Louhi, each failing before and passing after the reference fix, and Smith's score on them is reported per project.

- **Rehearse plans in a learned world model of tool results** — FEATURE — value 3 — effort L — risk high — category: simulation — wild
  Why: 150k ledger lines and 74 journals pair actions with exit codes and outputs. A small model predicts whether a command passes or what it prints, so the planner prunes plans before running them on the 16 GB card. Assumption: predictions are accurate enough to beat guessing on test exits.
  Done when: it predicts test pass/fail exit codes for held-out evidence runs at over 85%, and the planner shows fewer wasted real runs.

- **Add a project adapter stack: generic base plus a small per-project LoRA** — FEATURE — value 4 — effort M — risk med — category: personalisation — wild
  Why: genericity and fit pull against each other. Keep the base trained across projects and give each project a cheap adapter (volt's 773 briefs, the game's 59), built locally, never merged into the base for sensitive projects.
  Done when: the adapter beats the base on that project's held-out briefs, and a sensitive project's adapter file exists only in its own directory.

Next question: which head, if it only matched majority, would still be worth shipping because it makes a session path cheaper, and which head's gain would hide in a bench that scores accuracy and not cost or interruption?
Next question: how much does one project (Sampo itself, 1,767 briefs) dominate the leave-one-out result, and does a model that wins there still lead on the small projects with under 100 briefs?
