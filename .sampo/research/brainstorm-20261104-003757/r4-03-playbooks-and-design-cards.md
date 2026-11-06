# Brainstorm — lens: playbooks and design cards

- **Ship a "tool-gap fork" design card per stack** — FEATURE — value 5 — effort M — risk low — category: playbooks
  Why: Mission 7 asks for find-or-build-or-ask, but earlier ideas stay prose-level. A branching design card (does the tool exist on PATH? in `plugins find`? stdlib-able in under 60 lines? needs a grant?) with one yes/no per node gives a 4B model a walkable tree. Assumption: the card store (T-2909) takes branching steps, not only linear ones.
  Done when: for 5 stacks (python, node, rust, shell, docs), a 4B model on 10 recorded gap scenarios reaches the correct leaf (find/build/ask/decline) in at least 8 of 10 more often than bare, per `sampo louhi`.

- **Cut a card per forged-tool shape, not per tool** — FEATURE — value 4 — effort M — risk low — category: design cards
  Why: Thousands of cards are wanted; per-tool cards can't scale, but tool shapes can (stdin-to-JSON filter, file linter, diff summariser, MCP read-only wrapper, fixture generator). Each card holds a skeleton, a doctest and a negative control. Assumption: about 20 shapes cover most gaps.
  Done when: 20 shape cards exist and a 9B model forges 8 of 10 unseen gap tools from a card, each passing its own doctest and a failing negative control.

- **Add a "refusal is success" card family** — FEATURE — value 4 — effort S — risk low — category: playbooks
  Why: Small models over-build. Cards for "already on PATH", "host does this natively", "a one-liner is cheaper" and "needs a grant, so ask" score declining as a pass. The pack shows many ideas on retirement but no card that teaches stopping.
  Done when: on 10 decoy scenarios (tool already exists), a card-guided 9B declines the build in at least 9, against a measured baseline for the bare model.

- **Mine cards from `fm friction` and the 8 "missed asks" tasks** — FEATURE — value 4 — effort M — risk low — category: card grid
  Why: Earlier brainstorms asked for failure mining, but the pack's own list of missed asks (T-2887 to T-2909) is a ready corpus of real misses. Each becomes a card "when you see X, check Y first", such as "proper noun with no referent: look it up before building", "jarvis/Claude named in a scene: use the role word".
  Done when: at least 8 cards are written from those tasks, each with the ask text that triggered it, and a replay of the original ask on a 27B shows the card prevents the same miss in at least 6.

- **Tag each card with its dumbest passing model and route by it** — PERFORMANCE — value 4 — effort M — risk low — category: routing
  Why: The standing steer is local models matching frontier through scaffolding, and a model switch costs about 3 minutes. Each card records the smallest model that passes it, so the drive picks the resident model and queues by it.
  Done when: `sampo cards show NAME` prints a `floor:` model, and the drive's local queue for one night makes at most one model switch.

- **Compile a followed card into a script and keep the card as its docstring** — FEATURE — value 4 — effort L — risk med — category: graduation
  Why: A card that a model walks mechanically 5 times is a script waiting to happen; steps then cost no tokens. Assumption: step traces are recorded per card use.
  Done when: one card with at least 5 logged uses is compiled to a script whose output matches the card-walked result on those 5 inputs, and the card is flagged "compiled".

- **Write a design card for the install-grant request itself** — FEATURE — value 3 — effort S — risk low — category: grants
  Why: Install grants are queued, and a small model's request will be vague. A fill-in card (tool, why this one, what it can touch, what was tried first, how to undo) keeps the grant reviewable in one glance.
  Done when: a 9B's grant request filled from the card has all 5 fields in at least 9 of 10 scenarios, and the reviewer view renders them as one block.

- **Lint cards for one-verb steps and a checkable end** — CLEAN — value 3 — effort S — risk low — category: card quality
  Why: The standing rule that every tower file gets a cold read implies cards need a mechanical gate too. Reject cards with steps longer than 25 words, with no verifiable last step, or with a cross-reference to another card.
  Done when: `sampo cards lint` fails a seeded bad card on each of the 3 rules and passes the current store.

- **Wild: Cassette cards — record one frontier tool-forging run as a branching tape** — FEATURE — value 5 — effort L — risk med — category: replay
  Why: Frontier runs already solve the hard decisions once. Strip the tool calls to a tape with branch points ("test failed → go to step 4b"), then a 4B steps through it, filling only the slots that differ. Assumption: tape slots can be typed and checked.
  Done when: a 4B replays one tape on 3 new gaps of the same shape and passes the gap's tests on 2 of 3 with no frontier calls.

- **Wild: Scar cards written by the failing small model itself** — FEATURE — value 4 — effort M — risk med — category: self-written cards
  Why: When a 9B fails a forge, it writes a post-mortem card ("I assumed X; the error showed Y"), and the card enters the store only if a retry that reads it passes. The failure mode is learned from the model's own habits.
  Done when: of 10 failed forges, at least 3 produce a scar card that flips a retry to pass, and cards that don't flip it are discarded.

- **Wild: Poisoned-card canary in every exam run** — SECURITY — value 4 — effort S — risk low — category: robustness
  Why: Cards go into small-model context as instructions, and a bad one (curl | sh as a step) would be followed blindly. One planted unsafe card per run measures whether the model or the Ward catches it.
  Done when: the exam reports a per-model "followed the poisoned card" rate, and the Ward blocks the unsafe step in 100% of seeded runs.

- **Retire a card when the model passes without it** — CLEAN — value 3 — effort S — risk low — category: card lifecycle
  Why: Cards cost context and models improve. A re-run on a new model id with the card hidden shows whether it still earns its place. Assumption: the model id is recorded per measurement.
  Done when: after a model-id change, the sweep marks cards that pass bare as dormant and lists the count in the morning card.

Next question: Which gap shapes occur in the user's real closed-task history often enough (three or more times) to deserve a shape card, and has anyone counted them?
Next question: When a card-guided 4B and a bare frontier model disagree on find/build/ask, which one has been right on the held-out gaps?
