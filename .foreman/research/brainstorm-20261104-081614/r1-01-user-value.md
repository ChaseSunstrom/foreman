# Brainstorm — lens: user value

- **Hold out whole projects to prove the decider generalises** — FEATURE — value 5 — effort M — risk low — category: decider
  Why: 13 projects, 4,078 briefs, but Sampo is 1,767 and volt 773. The best intake-type score (0.73 vs 0.595 majority) was not split by project, and nothing beats majority on tier.
  Done when: `sampo model bench` reports leave-one-project-out accuracy per decision slot next to the majority baseline, and a slot is only switched to the model if it wins on every held-out project group.

- **Predict a brief's outcome before work starts** — FEATURE — value 5 — effort M — risk low — category: risk routing
  Why: briefs record done, blocked, reverted and later fixes. Labels exist, and routing to planner, escalate or extra audit lenses is where a user saves time and tokens. Assumption: outcome is predictable above base rate from the request, the touched files and the stack.
  Done when: a head scores each new brief, and on held-out projects its top-decile risk briefs revert or need a later fix at least 1.5x the base rate.

- **Judge whether a close will hold (false-done detector)** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: the uplift exam shows closes rising 4 → 5 while many are false-done. Briefs carry evidence runs plus later-fix labels, so closes that held and ones that didn't can be told apart.
  Done when: on Louhi runs the detector flags at least 70% of false-done closes at under 10% false blocks, and `task finish` consults it.

- **Distil a Smith actor from verified runs only** — FEATURE — value 4 — effort L — risk med — category: Smith
  Why: T-2971, with 74 journals. Only local-model runs whose tests went green and whose closes held are kept, which avoids the Claude-output terms issue. Loops are the main failure end (4 of 10).
  Done when: a LoRA on the 12B beats its untuned self on Louhi's held-out split (fixed ≥ 4/8 vs 3/8), with false-done not up.

- **Predict a Smith loop before the third repeat** — FEATURE — value 4 — effort S — risk low — category: Smith
  Why: T-2966 breaks loops on the third identical action, and loops end 4 of 10 runs. Journals give labelled trajectories. Assumption: the first two steps carry signal.
  Done when: a trajectory classifier fires on at least 60% of eventual loops by step two, with under 10% false fires on green runs, and routes to the planner there.

- **Suggest verify commands from the stack** — FEATURE — value 4 — effort M — risk low — category: criteria
  Why: criteria carry verify commands, and evidence runs carry exit codes, so "this command failed before and passed after" is a clean label. Generic across stacks (c, js, ts, python, ruby, rust).
  Done when: for held-out projects the suggested command runs and fails red-first on at least 60% of new briefs.

- **Gate every Rune generation with an adoption card** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the rule is "adopt only where the bench leads, retrain and re-bench every generation". Without a card each retrain is unaudited.
  Done when: the generation sweep retrains, benches on frozen held-out projects, prints per-slot win/loss/tie vs the previous model and majority, and rolls a regressing slot back automatically.

- **Keep a per-project adapter over a shared base, local only** — FEATURE — value 4 — effort M — risk med — category: privacy
  Why: sensitive projects must stay on the machine, and a project's quirks should not leak into the generic model. Repo-specific names are stripped from the shared base.
  Done when: a project flagged sensitive contributes zero rows to the shared set (checked by a test that greps the manifest), and its adapter loads only for that project.

- **Answer routine asks as the user's twin (wild)** — FEATURE — value 5 — effort L — risk high — category: autonomy
  Why: wild. The user is often away, with 149k ledger lines of asks, answers and steers, and the rule "never block on the user". A model trained on their past answers pre-fills `decide --kind costly` picks and shows each one in the final report with its confidence.
  Done when: on held-out past asks it matches the user's actual answer at least 80% on the ones it chooses to answer, and abstains on the rest.

- **Seed cold-start priors for a new project from sibling projects (wild)** — FEATURE — value 4 — effort M — risk med — category: transfer
  Why: wild. A new Sampo project has 0 briefs, while volt has 773. Retrieval over stripped lessons (bge-m3 recall@1 0.85) gives day-one priors, and the first brief on a new repo surfaces three relevant lessons from other projects.
  Done when: on a project with its history masked, retrieved lessons are marked useful by the later outcome more often than random lessons.

- **Plant bugs in any repo to mint unlimited verified scenarios (wild)** — FEATURE — value 4 — effort L — risk med — category: training data
  Why: wild. Louhi has 18 runs, which is thin for training. A model that mutates a project's code until a test fails yields scenarios in that project's own language and stack, graded for free by its tests.
  Done when: `sampo exam mint --project P` produces at least 20 scenarios whose red/green status is verified by running the tests.

- **Train a Ward classifier, plus an attacker to probe it** — SECURITY — value 3 — effort L — risk med — category: guard
  Why: guard refusals sit in the ledgers. The open question is whether the Ward and the funnel's local models share a text channel an attacker can reach. Assumption: refusal logs hold enough positives.
  Done when: the classifier adds no misses on a frozen red-team set, and a prompt-injection set against the funnel judges is run and reported.

- **Show which slots use a model, with a user veto** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: the model plugs into many places (decide, intake, playbook, foresight, loop breaker, judges). The user needs one page saying what is learned, what is rules, and what is switched off.
  Done when: `sampo models` lists every slot with source, held-out score vs majority and a one-line off switch, and each slot honours it.

- **Predict accept or reject for funnel output** — FEATURE — value 3 — effort M — risk low — category: ideas
  Why: the earlier question was whether the cheap funnel stages kill what a human later rejects. The user's own accept/reject history is the label. Assumption: enough history exists.
  Done when: the pre-filter's agreement with the user's past verdicts is reported per stage, and stages that disagree are dropped.

Next question: Which decision slot has the most user-labelled data per project and so can support a per-project adapter rather than only a shared base?
Next question: What does the model cost the user on a bad day (a wrong routing, a false close), and is that measured as well as the average gain?
