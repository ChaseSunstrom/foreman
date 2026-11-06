# Brainstorm — lens: bold bets

- **Gate ceremony on a learned regret score** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: assumption: the c14 hand-edit mining and the ceremony-per-task-kind item (T-1266) can be joined, so P(user rewrites these lines within 7 days) is predicted from diff size, proof kind, paths and model. High-score tasks get a plan menu and a second look; low-score ones get the light path.
  Done when: `fm doctor` prints held-out AUC of the regret score over the last 50 landings against a "predict the base rate" baseline, and a test shows a high-score fixture task gets the extra step.

- **Run one anticipation governor** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: the slate holds dozens of independent predictors (whispers, cards, pre-drafts, shelves, mood). Only a per-day interrupt cap is mentioned, so nothing arbitrates between them. Proposed: every predictor files its output with an estimated user-seconds gain and cost, a single arbiter spends a daily budget, and dismissals shrink that predictor's share.
  Done when: with three fake predictors firing at once, a test shows only the highest net-value one is shown, and dismissals lower the next day's share.

- **Prime other harnesses with the anticipation card** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: the standing rule says Foreman isn't Claude-specific, and T-0335/36/37 show Codex/Gemini/opencode sessions get little. Proposed: write the card into a fenced region of AGENTS.md/GEMINI.md at close, so any harness starts primed.
  Done when: after a close, the fenced region in AGENTS.md matches the card, and the next close replaces it without touching text outside the fence.

- **Pre-merge the futures** — FEATURE — value 3 — effort L — risk med — category: speculation — wild
  Why: assumption: speculative stubs of the top 3 predicted asks can be applied in a scratch worktree overnight. Where they collide, or all need the same missing piece, that shared prerequisite is filed as one task. Nobody has proposed checking predicted asks against each other.
  Done when: for a fixture with two predicted asks that touch one function, the nightly run files exactly one prerequisite task naming both.

- **Park `fm ask` for the user's learned present window** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: `fm ask` has timeouts and the drive keeps working while it waits. Proposed: learn the hours the user actually answers, hold non-urgent questions for the next such window, and take a stated lowest-regret default if the deadline passes first.
  Done when: a replay of ledger timestamps shows a non-urgent question deferred to the learned window, and an urgent one asked immediately.

- **Seal the claim–consumer pair on every new gauge** — CLEAN — value 3 — effort S — risk low — category: measurement
  Why: the pack records repeated gauge defects (T-2667 burden miscounting, T-2583 criterion arithmetic). Proposed: a gauge can't land without a registered consumer decision and a hand-computed known answer; a lint refuses otherwise.
  Done when: adding a gauge without those two fields fails `fm check` with the missing field named.

- **Ledger-gap anticipation: forecast the day each reader goes wrong** — PERFORMANCE — value 3 — effort M — risk low — category: scale
  Why: earlier questions ask about caps and windows picked without running them on the user's history. Proposed: replay each reader on the real ledger scaled 2×, 5× and 10× at tick time, and warn with a projected date when a reader crosses its latency bar.
  Done when: `fm doctor` lists each windowed reader's projected breach date, and a planted slow reader shows a date within the test horizon.

- **Hand-wins precedence table with a surfaced conflict** — FIX — value 4 — effort M — risk med — category: trust
  Why: an earlier question asks which side readers trust when the user's hand and Foreman both change the tree, queue or ledger. Proposed: one table for the precedence, enforced by a test per entry, plus a one-line "I yielded to your edit of X" at the next surface.
  Done when: a test edits a queued task by hand while the drive holds it, and the hand edit survives and is named in the next `fm next`.

- **Wild: Turing-test the predictor on the user** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: assumption: the user will enjoy a weekly five-second game. They see their real next ask beside the predicted one in random order and guess which is real. Unguessable means the predictor is good, and every miss becomes a labelled example.
  Done when: `fm` shows a pair, records the guess, and `fm doctor` reports guess accuracy over the week.

- **Wild: Keep a "things you've stopped asking about" shelf** — FEATURE — value 3 — effort S — risk low — category: unspoken needs — wild
  Why: the slate is all about what the user will ask next. Nothing watches asks that quietly stopped after one or two uses (the drops list shows several ideas the user let die). Proposed: list such topics monthly with "solved, abandoned, or forgotten?" and a one-key answer.
  Done when: a fixture ledger with a topic asked three times then silent for 30 days appears on the shelf, and answering "solved" removes it.

- **Wild: Replay the user's worst day on every release** — PERFORMANCE — value 3 — effort M — risk med — category: resilience — wild
  Why: assumption: the ledgers hold at least one day dense with failures (usage limits, crashes, blocked asks). Proposed: freeze it as a fixture and replay it through hooks, readers and `fm next` before each ship, comparing the user-facing output line by line.
  Done when: `fm ship` fails when a replay of the frozen day changes any user-facing line without a recorded reason.

- **Count anticipation hits only if the user did not have to be told** — CLEAN — value 3 — effort S — risk low — category: measurement
  Why: assumption: many "hits" come from Foreman printing the next command and the user running it, which proves nothing. Proposed: score a hit only when the user's ask precedes or differs from the printed hint.
  Done when: a test where the user runs a printed `Next:` command verbatim counts as no hit, and one where they ask the same thing unprompted counts as a hit.

Next question: Which of the predictors proposed so far would the user notice missing after a month, and what would answering that cost to measure?
Next question: Does the slate's growth (hundreds of ideas per brainstorm) reduce the share of ideas the user actually accepts, and who owns throttling it?
