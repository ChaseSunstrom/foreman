# Brainstorm — lens: small-model skills at scale

- **Mint a card per toolchain error code, zero tokens** — FEATURE — value 5 — effort M — risk low — category: scale
  Why: the steer asks for thousands of cards. Compilers and linters already publish one explanation per code (`rustc --explain`, ruff and clippy rule docs, mypy and tsc codes, pytest outcomes). Parsing them needs no model, and I couldn't find anything in the pack that does this. Assumption: those tools are on PATH or vendored.
  Done when: `sampo cards gen --source rustc` writes at least 400 cards that pass the card lint, each with a failing-snippet and fixed-snippet pair, with zero model calls logged.

- **Convert the 1,396 existing skills into small-model form** — CLEAN — value 4 — effort M — risk med — category: scale
  Why: `plugin/skills/` holds 1,396 files written for frontier readers. A deterministic splitter could cut each into one-verb, ≤600-character steps with a checker line, and flag the ones that can't be cut. Assumption: most skills split cleanly.
  Done when: a report lists the share converted, the share flagged "needs a human", and a 4B bare-versus-card pair on 20 converted skills.

- **Retrieve fix-pattern cards by error-text signature** — FEATURE — value 4 — effort M — risk low — category: retrieval
  Why: the repo has many FIX commits and closed tasks. Cards keyed on the normalized failing output (paths, line numbers and ids stripped) hit at the moment of failure better than keyword search over task prose does. Assumption: commit messages or tasks keep the failing text.
  Done when: on 30 held-out closed FIX tasks, the right card ranks in the top 3 at least 50% of the time, measured zero-token.

- **Stop each skill exam early with sequential testing** — PERFORMANCE — value 4 — effort S — risk low — category: performance
  Why: a model switch on the endpoint costs about 3 minutes, and fixed-N lift runs for thousands of cards will eat the night. A sequential probability ratio test ends a run as soon as lift or no-lift is clear.
  Done when: the same 50-card lift sweep finishes in under 60% of the model-calls of fixed-N with the same pass/fail verdict on at least 95% of cards.

- **Warm the local server's prompt cache with the likely skill bundle** — PERFORMANCE — value 3 — effort M — risk med — category: performance
  Why: the 27B re-prefills the same stack-and-skill prefix every turn. A byte-stable bundle per (stack, stage) lets llama.cpp prefix caching hit, and `fm next` knows the stage a few seconds early. Assumption: the endpoint exposes prompt caching.
  Done when: time-to-first-token for the second turn of a skill-carrying prompt drops at least 40% in a recorded bench.

- **Measure pairwise skill interference** — FEATURE — value 3 — effort M — risk low — category: quality
  Why: lift is scored one card at a time, but small models get confused when two cards are in context, and nothing in the pack checks that. Run each card alone, then in pairs with its nearest neighbours, and record any pair that scores below either alone.
  Done when: an interference table is stored on the cards, and the retriever refuses to co-load a flagged pair.

- **Add `sampo skill try NAME --model PROFILE`** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: authors currently wait for a full Louhi run. A 10-second bare-versus-card diff on three fixtures against the chosen model would close the loop while writing a card. Assumption: three fixtures are enough for a first signal.
  Done when: the command prints bare pass/fail, card pass/fail and the output diff, and finishes in under 30s on the 9B.

- **Ship an offline pocket pack for laptops and phones** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: devices and privacy are thin in the pack. Cards chosen by a manifest sniff (about 50 for the stack) pack into one file under 2 MB with an embedding index, so a 4B with no endpoint and no network can still use them. It also keeps install weight down given the 2.4 GB concern.
  Done when: a pack built for a Python repo loads in a fresh scratch home with the network blocked, and a retrieval query returns a card.

- **Tag each card with where it came from, and block private ones from export** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: cards mined from the user's transcripts or repos could carry paths or names into the public starter shelf or the site. A provenance label (public-source, mined-private, authored) is checked at export.
  Done when: planting a canary string in a mined-private card makes `sampo cards export --public` fail, and an authored card exports fine.

- **Flag contradictory cards before they ship** — CLEAN — value 3 — effort M — risk med — category: quality
  Why: at thousands of cards, two cards will give opposite advice for neighbouring cells. Embedding neighbours plus a cheap local judge, with a quoted-line rule so it only counts when it quotes both lines, can find them.
  Done when: a seeded contradictory pair is caught, and a clean set of 200 cards raises no false flag above 5%.

- **Wild: let the 4B write a card from its own failure, and trust it only if a second cold 4B passes using it** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: assumption: wild. Cards written by the model that failed carry its real confusion, and the cold second model is the independent check that the card helps and isn't merely echoing the failure. Cards are produced at the model's own scale.
  Done when: over 20 failures, the share of authored cards that raise a fresh 4B's pass rate on the same task is reported next to the 27B-authored rate.

- **Wild: replay a card's lesson as a flashcard quiz before the task** — FEATURE — value 2 — effort S — risk low — category: delivery
  Why: assumption: wild. Instead of pasting the card, the harness asks the small model a one-line question the card answers. If the model answers right, the card is skipped, which saves context and gives a per-model "already knows" signal.
  Done when: on 30 cards, the quiz-gated path uses at least 30% fewer card characters at equal pass rate.

- **Wild: dream shift: the idle GPU writes tomorrow's cards from today's failure log** — FEATURE — value 4 — effort L — risk med — category: scale
  Why: assumption: wild. At night, with the resident model fixed for the whole run to avoid switches, the 27B drafts cards for the day's failure clusters, a different small model grades them cold, and the morning card lists survivors. This is the "grown every generation" steer made continuous.
  Done when: a morning report shows N drafted, M passing a cold bare-versus-card pair, and zero filed without that pair.

- **Wild: a card's "why I exist" is a runnable repro; a card whose bug no model hits any more is auto-retired** — CLEAN — value 3 — effort M — risk low — category: lifecycle
  Why: assumption: wild. Storing the original failing prompt as the card's replay case lets each model upgrade cheaply show which cards its bare run now passes.
  Done when: swapping in a new model id produces a list of cards that now pass bare, and they are marked dormant, not deleted.

Next question: which card kinds does the 4B fail at because of the model's context handling rather than missing knowledge, and would a different delivery (quiz, menu, grammar) fix them where text does not?
Next question: when thousands of cards exist, what is the retrieval miss rate on real failures, and who notices a silent miss?
