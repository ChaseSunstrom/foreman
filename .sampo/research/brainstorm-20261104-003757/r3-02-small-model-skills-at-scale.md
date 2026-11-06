# Brainstorm — lens: small-model skills at scale

- **Mint a card from every tool-building trace** — FEATURE — value 5 — effort M — risk low — category: card factory
  Why: Mission 7 builds tools for gaps, but the pack shows cards (T-2909) are written by hand or by the 27B; the build trace itself (search → build → negative control → quarantine) is never turned into a replayable small-model card.
  Done when: after a tool is built, `cards.jsonl` gains a card whose steps cite the trace's commands, and a bare-vs-card Louhi pair on the same gap is recorded.

- **Compile cards into slot-filling runners** — FEATURE — value 5 — effort L — risk med — category: scaffolding
  Why: a 4B/9B follows numbered steps poorly in free text; the standing steer is "match frontier through scaffolding". Assumption: a state-machine runner where the model fills one slot per call, validated by a grammar, beats prose cards.
  Done when: the same card run as runner vs prose on qwen3.5 4B shows a paired pass-rate in the Louhi scorecard.

- **Fill card-grid cells by failure mining** — FEATURE — value 5 — effort M — risk low — category: coverage
  Why: the grid (kind × stack × stage × surface) exists but "thousands of cards" can't be hand-written; closed-task failures and `fm friction` are a free source of which cells matter.
  Done when: `sampo cards gaps` lists empty cells ranked by failure count, and one generation's new cards each cite a failure id.

- **Store per-card lift and retire at half-life** — FEATURE — value 4 — effort M — risk low — category: card lifecycle
  Why: the Moonscale funnel dedupes but nothing says a card still helps once the served model changes (the llama-swap endpoint swaps models).
  Done when: each card row carries `lift`, `model`, `measured_at`; a model change marks cards stale and a card passing bare is retired with a recorded reason.

- **Cross-model card authoring: the writer never grades** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: the standing rule says cold reads and signals Foreman didn't author; a card written by qwen3.8-27b and scored by it is self-graded.
  Done when: admit refuses a card whose writer model equals its lift-arm model, test included.

- **Retrieve cards at the failure, not at the start** — FEATURE — value 4 — effort M — risk med — category: retrieval
  Why: small models have short effective contexts; injecting top-k up front wastes it. Assumption: a PostToolUse hook can match error text via the local embedder.
  Done when: a seeded failing command makes exactly one relevant card appear in the next turn, under a character cap.

- **Print "dumbest model that passes" on every card** — FEATURE — value 4 — effort M — risk low — category: model floor
  Why: the not-yet items (selfjev-4b, Jeff) wait on exams; a per-card floor gives routing data for free.
  Done when: `sampo cards show ID` prints the smallest profile with a paired pass, or "unmeasured".

- **Graduate mechanically-followed cards into scripts** — CLEAN — value 4 — effort M — risk low — category: card to code
  Why: a card whose steps never branch is a script wearing prose; scripts cost zero tokens.
  Done when: a detector flags cards with ≥90% identical traces across runs and drafts a script plus test.

- **Lint cards for size, one-verb steps and a checker** — CLEAN — value 3 — effort S — risk low — category: quality
  Why: at thousands of cards, drift in shape is the main risk; the write rules exist for candidates but not for card form.
  Done when: admit rejects a card over N chars, with a step holding two verbs, or with no verifiable check line.

- **Cassette cards: replay a frontier run with branch points** — FEATURE — value 5 — effort L — risk med — category: trace distillation (wild)
  Why: wild: record a frontier session's tool calls once; the small model steps through, each branch point being a classifier choice by Jev/Kev.
  Done when: a 9B completes a recorded task via the cassette in Louhi where bare it failed.

- **Card tournament: rivals for one cell, loser merged** — FEATURE — value 4 — effort M — risk med — category: evolution (wild)
  Why: wild: two models write rival cards for a cell; Louhi picks the winner; the loser's unique steps fold in only if lift holds.
  Done when: a cell shows two candidates, their paired scores and one merged survivor.

- **Let the failing model write its own post-mortem card** — FEATURE — value 4 — effort M — risk med — category: self-repair (wild)
  Why: wild: a 4B fails, writes "what I'd do differently", and the card is admitted only if a retry passes.
  Done when: a failed scenario yields a card whose retry passes, recorded with both runs.

- **Poison one card per exam to test blind trust** — SECURITY — value 3 — effort S — risk low — category: robustness
  Why: cards are injected into small models that follow them literally; a planted unsafe step shows whether the Ward and the model catch it.
  Done when: the exam reports whether the poisoned step was followed, flagged or blocked.

Next question: which card kinds does a 4B follow better as text than as a runner, and does the answer hold across the model swap?
Next question: what is the cheapest signal, with no model call, that a card is the reason a run passed?
