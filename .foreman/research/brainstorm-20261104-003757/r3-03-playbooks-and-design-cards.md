# Brainstorm — lens: playbooks and design cards

- **Write a card per "tool-gap moment" shape, not per tool** — FEATURE — value 4 — effort M — risk low — category: cards
  Why: the pack's Mission is "finds or builds the plugin/skill/MCP/script it lacks", and earlier ideas cover ladders and skeletons but not a taxonomy of the *moments* (binary missing, wrong version, flag unknown, auth missing, network blocked, tool exists but unused). assumption: closed-task history has these shapes in recurring numbers.
  Done when: `research/cards/cards.jsonl` holds one card per moment shape (≥6), each with a trigger regex over real error text taken from ≥3 closed tasks, and a test shows each trigger fires on its sourced sample and not on the others.

- **Add a "stop-and-ask-which-rung" decision card for small models** — FEATURE — value 4 — effort S — risk low — category: playbooks
  Why: 4B/9B models over-build or under-build; nobody has given them a three-line decision (use PATH tool / write ≤40 line stdlib script / queue grant). assumption: failures in Smith local runs show over-building.
  Done when: a Louhi scenario set with 10 gaps shows the card raises the right-rung choice rate for qwen3.5 9B over bare by a recorded margin, or the card is retired with the numbers.

- **Store each card's "failure it prevents" as a replayable negative case** — FEATURE — value 4 — effort M — risk low — category: card testing
  Why: the admit rule is bare-vs-card lift, but a card with no stored failing input can't be re-measured when the served model changes. assumption: cards currently store prose, not the triggering transcript.
  Done when: every card row has `fail_case` (redacted transcript path), and `sampo louhi cards --recheck MODEL` reruns bare vs card on those cases and prints lift per card.

- **Make cards diff-reviewable by sorting by cell and forbidding cross-references** — CLEAN — value 3 — effort S — risk low — category: card hygiene
  Why: thousands of cards will be grown by 27B writers; a templated-phrasing rule exists for coverage cells but cards themselves need the same near-duplicate guard. assumption: the Moonscale funnel can be reused.
  Done when: adding a card whose shingle similarity to an existing same-cell card exceeds the threshold is refused with the neighbour's id.

- **Card the build step as a spec-first triple (passport, doctest, script)** — FEATURE — value 4 — effort M — risk low — category: playbooks
  Why: a small model building a tool fails by writing code before knowing the contract; a playbook ordering one-line passport → doctest that fails → body, with a checker per step, fits the 27B/9B ladder. assumption: grammar-constrained steps are available per profile.
  Done when: qwen3.5 9B produces a passing stdlib script for ≥7 of 10 held-out gap scenarios using the playbook, versus a recorded bare rate.

- **Tag cards with the smallest model that passes them and route by it** — FEATURE — value 3 — effort S — risk low — category: routing
  Why: the steer wants local models to match frontier via scaffolding; routing a task to the cheapest passing rung saves model-swap time (~3 min per switch noted). assumption: floor data exists after the first league.
  Done when: each card shows `floor_model`, and `sampo smith` picks a loaded model's cards first, with a test that no card is served to a model below its floor.

- **Add an "unsafe step" lint that every card must pass** — SECURITY — value 4 — effort S — risk low — category: card safety
  Why: cards direct installs and shell steps; a card saying `curl | sh` or `sudo pacman` violates the no-software-installs rule and the Ward. assumption: Ward can classify card steps as commands.
  Done when: a test feeds each card's command steps to the Ward and fails the build if any is refused or if a step installs without a grant line.

- **Serve one card at the failing tool call, capped at 600 chars** — PERFORMANCE — value 4 — effort M — risk med — category: retrieval
  Why: small models' effective context is short; injecting at failure rather than at start fits the existing "teach at the block" idea but with a hard card budget. assumption: PostToolUse can see the error text.
  Done when: a hook bench shows added latency under the existing budget, and a Louhi arm shows pass rate with injected card ≥ bare on missing-tool scenarios.

- **Wild: Let the small model's *failed attempt* be the card's worked example** — FEATURE — value 4 — effort M — risk med — category: cards (wild)
  Why: a card showing "here is what you'd do wrong, here is the fix" in the model's own style may transfer better than a clean recipe. assumption: contrastive examples beat clean ones for 4B-class models.
  Done when: an A/B in Louhi on 10 scenarios shows contrastive cards vs clean cards, result recorded either way.

- **Wild: A card that tells the model to say "I can't, here's the grant I need" as a first-class success** — FEATURE — value 3 — effort S — risk low — category: playbooks (wild)
  Why: small models fabricate tools; rewarding a correct refusal-with-grant-request teaches the install-grant queue's real use. assumption: scored "declined correctly" exists in Louhi.
  Done when: scenarios with an unavailable tool score a correct grant request as pass, and the card lifts that rate over bare.

- **Wild: Cards graded by a "blind apprentice" 4B that has never seen the repo** — FEATURE — value 3 — effort M — risk low — category: card testing (wild)
  Why: if the smallest model can follow it, the 27B can; one cheap gate for all cards. assumption: selfjev-4b/qwen3.5 4B is loadable overnight.
  Done when: each admitted card records the 4B's follow-through result, and the web UI Models page lists cards the 4B cannot follow.

- **Retire cards when the card text appears in a newer model's bare output** — CLEAN — value 3 — effort M — risk low — category: card lifecycle
  Why: scaffolds decay as models improve; detecting the model already doing the card's step unprompted gives a cheap retire signal without a full exam. assumption: step-level matching against transcripts is feasible by substring of the checker.
  Done when: a recheck marks cards `redundant` where bare passes the card's checker in ≥8/10 runs, and they drop out of retrieval.

- **Ship a design-card kind for the tool shelf UI itself** — FEATURE — value 2 — effort S — risk low — category: design cards
  Why: the pack has UI/design card cells but no card for rendering empty, quarantined, expired-grant states consistently. assumption: the illustrated forge tokens apply.
  Done when: a design card lists the five shelf states with token names, and a lint finds no shelf view using a colour outside them.

Next question: Which gap moments in real closed-task history were resolved by a plain shell one-liner rather than any tool or skill, and would a card for those be shorter than the gap?
Next question: Does a card that lifts the 27B also lift the 4B, or do small-model cards need to be written separately per size class?
