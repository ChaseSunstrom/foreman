# Brainstorm — lens: small-model uplift: local models scaffolded to frontier

- **Bounce long outputs through a quote-only reader** — FEATURE — value 4 — effort M — risk low — category: token cost
  Why: assumption: the frontier still pays for raw test logs and tool output. A local model returns only line numbers, and code checks the quoted lines exist verbatim before the frontier sees them. The local model can't invent anything.
  Done when: a 50k-line test log reaches the frontier as under 40 verbatim lines, and a planted fake quote is rejected.

- **Let the frontier edit a local draft, billed by delta** — FEATURE — value 4 — effort M — risk med — category: scaffolding
  Why: assumption: reviewing a draft costs far fewer frontier tokens than writing one. The frontier returns a diff, never a rewrite, and the diff size is logged as the local model's miss.
  Done when: a brief drafted by the 27B and then edited produces a diff-size record, and the median edit is under 30% of the draft.

- **Verify drafts with atomic yes/no checklists** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: small models judge one narrow property far better than a whole draft. Ten questions run in parallel ("does it name a file?", "is the Done-when a command?"), each as a single-token answer.
  Done when: each draft carries a pass/fail vector, and on 20 planted-flaw drafts the checklist catches more than a single "is this good?" judge.

- **Keep a bank of the model's own passing rollouts** — FEATURE — value 4 — effort M — risk low — category: few-shot
  Why: the Exam is a free reward. Overnight, each local model re-attempts its failed closed tasks N times, and the passing traces become per-task-kind demonstrations keyed by embedding, with no training. This differs from hint banks, which come from frontier hints.
  Done when: a task kind has at least 3 stored passing traces, and the pass rate with them beats the pass rate without them on held-out cases.

- **Bias decoding toward the repo's real vocabulary** — FEATURE — value 3 — effort S — risk low — category: constrained decoding
  Why: extends the grammar idea. File paths and verb names are logit-biased or constrained to a trie built from `fm map` and the verb table, so a draft can't name a path that doesn't exist.
  Done when: over 100 local drafts, zero name a nonexistent path or verb.

- **Quiz-verify the user-model summary** — FEATURE — value 4 — effort M — risk low — category: user model
  Why: a local model compresses the ledger into a ~300-token user card. A second pass asks ten factual questions of the card alone and checks them against the ledger. A card that scores under 8/10 is not published.
  Done when: `sampo` prints the card's quiz score, and a card with a planted false line fails.

- **Graduate repeated frontier corrections into code** — FEATURE — value 4 — effort M — risk med — category: scaffolding
  Why: the same correction seen three times is turned into a deterministic post-processor. The 27B writes it, a red-first test is required, and the model-free fixer runs before any later draft.
  Done when: one recurring correction class is fixed by code with zero tokens, and its test fails on the unfixed draft.

- **Compile frontier playbooks into scripts the local model steps through** — FEATURE — value 4 — effort L — risk med — category: orchestration
  Why: assumption: weak models fail at planning but do fine on leaf judgments. The frontier writes a state machine once per task kind, and the local model fills only the leaf slots (classify, extract, choose).
  Done when: one task kind runs end to end with the local model making only leaf calls, and it passes the same Exam as the frontier run.

- **Cache local calls by prompt hash and endpoint fingerprint** — PERFORMANCE — value 3 — effort S — risk low — category: speed
  Why: reruns of overnight batches and the model bench repeat identical prompts at a ~3 minute cost per model switch. The cache key is (prompt, params, golden-prompt fingerprint of the served model), so a swapped model can't return stale answers.
  Done when: rerunning a night's batch makes zero endpoint calls, and changing the served model invalidates the cache.

- **Draft in a tool-less cell with repo text fenced as data** — SECURITY — value 3 — effort S — risk low — category: injection
  Why: the user model and ledger hold raw pasted text, and local models resist injection worse than frontier ones. The drafter gets no tools and no network, and it sees quoted material only inside a fence.
  Done when: a pasted "ignore previous, run X" in a ledger ask changes no draft and triggers no call.

- **Mine surprise to build the hint bank (wild)** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: assumption: token surprisal is a cheap signal. Score each frontier action under the local model's logprobs, and keep only the high-surprise spots as hint-bank entries, which skips the rest of the transcript.
  Done when: from 10 closed sessions the miner yields under 15 entries per session, and a local model given them fixes at least one case it failed before.

- **Distil the scaffolded 27B into the small decision models (wild)** — FEATURE — value 3 — effort L — risk med — category: models
  Why: the scaffolded 27B's accepted outputs become labelled data for d3/tev1/kev, and a larger model's scaffolds shrink into cheap routing. Everything stays on the user's hardware.
  Done when: a small model matches the scaffolded 27B's agreement with the user on a held-out week, at under a tenth of the latency.

- **Draft in the night voice and the morning voice (wild)** — FEATURE — value 2 — effort S — risk low — category: user model
  Why: assumption: the user types terse asks when tired and long ones in the morning. Two style exemplars are chosen by the clock and the day's ledger tempo, and the draft that matches how the user actually wrote last time is kept.
  Done when: a draft's length and detail match the user's typical ask for that hour, with a measured gap under 25%.

Next question: which task kinds does the 27B already match frontier on unscaffolded, so scaffolding there is pure waste?
Next question: what share of anticipation drafts does the user accept untouched, and does it differ between local and frontier drafters?
