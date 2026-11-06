# Brainstorm — lens: small-model skills at scale

- **Gate every card on a bare-model exam before it enters the store** — FEATURE — value 5 — effort M — risk low — category: skill quality
  Why: the steer says scaffolding must make 4B–27B match frontier, and T-2909 only has "write-time admit". Assumption: admit currently checks form, not lift.
  Done when: `sampo cards admit` runs the card's scenario on the target small model with and without the card, and refuses a card whose pass rate doesn't rise by a recorded margin.

- **Compile frontier traces into stepwise playbooks a small model walks** — FEATURE — value 5 — effort L — risk med — category: scaffolding
  Why: T-2908 runs Smith on local models. Small models fail at long planning; they do fine at one decided step. Assumption: no trace-to-playbook compiler exists.
  Done when: a passing frontier trace on a closed task becomes a numbered playbook, and qwen3.5-9B via Smith passes that task using only the playbook, in the exam.

- **Fill the card grid by failure mining, not by writing** — FEATURE — value 5 — effort M — risk low — category: card supply
  Why: "thousands of cards" can't be hand-written. Every failed local-model exam run (T-2908) is a labelled gap in kind × stack × stage × surface.
  Done when: a nightly lane turns each failed run into a draft card keyed to its grid cell, and the grid shows cells filled by mined cards with their lift.

- **Route cards by retrieval from the task, capped by the model's measured effective context** — FEATURE — value 4 — effort M — risk low — category: retrieval
  Why: the model-bench and embedder work (qwen3-embedding, bge-m3) exist, and a 4B model drowns in long injections. Assumption: no per-model card budget yet.
  Done when: Smith on a 4B receives at most N cards of at most M characters, N and M read from the model bench, and a test shows recall of the right card at rank ≤3 on held-out tasks.

- **Grammar-constrain card-driven steps to a verb menu** — FEATURE — value 4 — effort M — risk low — category: structured output
  Why: small-model failures are mostly malformed or free-form output; Sampo's own verbs are a closed set.
  Done when: Smith on gpt-oss 20B emits only valid verb calls under a grammar, and the malformed-call rate in the exam drops to zero on the scenario set.

- **Show per-card lift and decay on a Models/Cards page** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the Louhi scorecard exists but is per capability, not per card; the user wants numbers on the site.
  Done when: the web UI lists each card with n runs, with/without pass rates, last re-measured model version, and flags cards whose lift fell below zero.

- **Re-measure cards when the served model changes, and retire the ones that stopped helping** — CLEAN — value 4 — effort M — risk low — category: maintenance
  Why: the model switch on llama-swap costs ~3 minutes and models change often; the no-removal steer exempts proven harm. Assumption: lift is model-specific.
  Done when: a model id change queues a re-exam of its cards, and a card with negative lift is marked dormant with its measurement as the reason.

- **Escalate to the frontier only when a small-model jury disagrees** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: $200 budget, thousands of cards; cheap models should carry the volume. Assumption: a 3-sample vote correlates with error.
  Done when: on held-out scenarios, escalation fires on a measurable share of wrong answers at under a stated share of calls.

- **Have the 27B write cards, and a different small model test them cold** — FEATURE — value 4 — effort M — risk med — category: authoring
  Why: the user's local-first rule plus the "separate tool-less child" rule on exams. Writer and tester being different models limits self-agreement.
  Done when: every admitted card records writer and tester model ids, and the two differ.

- **Wild: Distil the scaffolded 27B's accepted runs into LoRA adapters per stack** — FEATURE — value 4 — effort L — risk high — category: local training
  Why: wild; thousands of passing card-guided runs are a training set that makes the cards unnecessary at the margin.
  Done when: a stack adapter on the 9B beats the same 9B with cards on a held-out set, or the result is recorded as not-yet.

- **Wild: A card tournament where cards for the same cell compete, losers are merged into winners** — FEATURE — value 3 — effort M — risk low — category: card supply
  Why: wild; thousands of near-duplicate cards will rot retrieval, and the dedupe funnel from Moonscale already exists to reuse.
  Done when: two cards in one cell are run head to head on the same scenarios and the loser is folded in, with the margin recorded.

- **Wild: A "dumbest model" floor: find the smallest model that passes each card's task and print it on the card** — FEATURE — value 3 — effort M — risk low — category: capability map
  Why: wild; it makes the claim "4B matches frontier" per task rather than overall, and shows where scaffolding runs out.
  Done when: each card shows the smallest tested model that passes with it, and the Models page sorts tasks by that floor.

- **Wild: Let cards be written by the failing model itself as a post-mortem, then verified by retry** — FEATURE — value 3 — effort S — risk med — category: self-improvement
  Why: wild; the model that fails knows what it got wrong; a retry with its own note is a free test.
  Done when: a failed run produces a note, the retry with the note passes, and only then is the note stored as a candidate card.

Next question: Which task kinds do small models fail at for reasons no card can fix (context length, tool-call format, reasoning depth), and does the exam say so?
Next question: Does a card that lifts the 9B also lift the 4B, or are cards model-size specific enough to need separate grids?
