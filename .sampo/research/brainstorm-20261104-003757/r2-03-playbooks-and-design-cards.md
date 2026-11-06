# Brainstorm — lens: playbooks and design cards

- **Write a tool-gap playbook as a branching card, not prose** — FEATURE — value 5 — effort M — risk low — category: playbooks
  Why: Mission 7 needs find→build→test→use→queue-grant, and the 27B/qwen3.5 4B/9B models lose long prose. Assumption: a card is a short numbered menu where each step names one verb (`plugins find`, script skeleton, `task prove`, grant queue) and a pass/fail branch to the next step.
  Done when: a 4B model, given only the card and a planted missing tool (e.g. shellcheck), reaches "grant queued" or "tool tested" with no step skipped, in 3 of 3 runs on the exam arm.

- **Gate each card on a bare-vs-card pair run** — FEATURE — value 5 — effort M — risk low — category: card admit
  Why: the steer says local models must match frontier "through scaffolding", and the user's rule says a free arm that beats the session arm is a top gap. Assumption: the admit check in T-2909 doesn't yet require a measured lift.
  Done when: `cards.jsonl` rejects a card with no recorded paired result (same model, same scenarios, with and without the card), and the rejection names the missing pair.

- **Seed the card grid from closed-task failures, not from writing** — FEATURE — value 4 — effort M — risk low — category: card mining
  Why: the pack's grid (kind × stack × stage × surface) risks the templated-cell problem the user already forbade. Assumption: `fm outcomes` and the friction ledger hold enough local-model failures to cluster by cell.
  Done when: each new card cites a failure id, and a sweep finds zero cards whose body matches another card's with only the stack word swapped.

- **Add fill-in-the-blank script skeleton cards for the commonest tool shapes** — FEATURE — value 4 — effort S — risk low — category: playbooks
  Why: "build the script" is the step a 4B model fails most. Assumption: gaps cluster into about 6 shapes (linter wrapper, JSON filter, file converter, API probe, log grep, test runner shim), each with fixed slots, a `--selftest` flag and a negative control.
  Done when: a 9B model fills the slots for 5 of 6 shapes and the produced script passes its own selftest, including a case that must fail.

- **Run a ladder per local model: bare, card, card plus grammar menu, frontier help** — PERFORMANCE — value 5 — effort L — risk med — category: scaffold ladder
  Why: the not-yet items (selfjev-4b, jeff, Jevlike, Von) wait on an exam arm "against the path they replace", and the model switch costs ~3 minutes, so runs must batch by resident model. Assumption: Louhi's `--agent smith --model` exists (T-2908).
  Done when: `sampo louhi` prints, per model and tool-gap scenario, the lowest rung that passes, with run count and cost, and one model swap per batch.

- **Retrieve cards at the moment of failure, not at session start** — FEATURE — value 4 — effort M — risk med — category: retrieval
  Why: the 2.4 GB/injection-size threads in the pack show start-of-session text is already too heavy. Assumption: a PostToolUse hook can match an error (command not found, import error) to one card and inject only that card, under a character cap.
  Done when: a missing-binary error injects at most one card of ≤600 characters, and a session with no failure injects none (a hook-output size test).

- **Retire cards that a model passes bare** — CLEAN — value 3 — effort S — risk low — category: card lifecycle
  Why: the pack's retire-when ideas and the lean rule (growth with no gain files a subtraction). Assumption: re-measuring on a model change is cheap on the free arm.
  Done when: when the served model changes, each card is re-run bare, and any card with no lift is marked dormant and stops being retrieved, with the reason recorded.

- **Lint cards for size, one-verb steps and a checker** — CLEAN — value 3 — effort S — risk low — category: card quality
  Why: the steer wants thousands of cards, and without a lint the store grows past what a 4B context can use. Assumption: a limit of about 400 tokens and a named pass/fail command per step.
  Done when: a card with a step lacking a verb or a check fails the write, and the store's p95 card size is printed.

- **Wild: Let the failing model write its own card as a post-mortem, accepted only if a retry passes** — FEATURE — value 4 — effort M — risk med — category: self-written cards
  Why: assumption: a model's own wording is easier for that model to follow, and the retry gives a cheap truth signal.
  Done when: a failed 9B run yields a draft card, the same 9B retries with it, and the card is filed only on a pass, with before/after recorded.

- **Wild: A card tournament where rivals for one cell compete on the exam and the loser is merged into the winner** — FEATURE — value 4 — effort M — risk low — category: card evolution
  Why: this keeps the store from sprawling toward thousands of near-duplicates, matching the Moonscale funnel's dedupe idea. Assumption: two models can author rival cards for the same gap cheaply.
  Done when: each cell holds one champion, the losing card's distinguishing step is folded in only if it raised the champion's score, and the loss is logged.

- **Wild: Print the "dumbest model that passes" on every card** — FEATURE — value 3 — effort S — risk low — category: card metadata
  Why: it turns the steer's "local models match frontier" claim into a per-task floor the router can use. Assumption: the ladder gives pass data for at least three model sizes.
  Done when: each card shows its smallest passing model and rung, and `fm next` routing for that task kind picks a model at or above it before escalating.

- **Wild: Cassette cards: record a frontier tool-building run once, replay it stepwise for small models** — FEATURE — value 5 — effort L — risk med — category: trace compilation
  Why: frontier wins compiled into branching playbooks fits the steer exactly. Assumption: traces can be reduced to verb steps with checks and parameter slots, and the small model only fills the slots.
  Done when: a recorded find/build/test run of a tool compiles to a card, and a 9B model replays it on a new tool of the same shape and passes the same checks.

- **Compile a card into a plain script once it is followed mechanically** — CLEAN — value 3 — effort M — risk low — category: card graduation
  Why: if every model follows the card the same way, the model adds nothing. Assumption: usage logs show steps taken with no variation.
  Done when: a card with 20 identical-path runs produces a script, and the card is replaced by a one-line pointer to it.

Next question: Which tool-gap scenarios in the exam come from the child that never sees Sampo's code, so card lift isn't measured on scenarios the card authors already knew?
Next question: When a card tells a small model to queue an install grant, what exactly does the user see, and is that preview checked cold by a model that has never seen the card?
