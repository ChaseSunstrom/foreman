# Brainstorm — lens: small-model skills at scale

- **Mint cards from the tool-building trace itself** — FEATURE — value 5 — effort M — risk med — category: card factory
  Why: Mission 7 builds tools (script, test, quarantine, grant); each successful build is a frontier trace of exactly what a 4B/9B model lacks. Cards today are written by hand or by the 27B (T-2909 part 1). Assumption: traces are stored per build.
  Done when: one finished tool build yields a card in `research/cards/cards.jsonl` with numbered steps and a verb menu, and a cold qwen3.5-9B re-runs it to a passing test of that tool.

- **Compile a card into a checklist runner (state machine) the model only fills slots in** — FEATURE — value 5 — effort M — risk med — category: scaffolding
  Why: the steer is "scaffolding makes small models match frontier"; free prose cards still rely on the model's planning. Assumption: a card step can be typed as {ask, verify-command, next}.
  Done when: `sampo smith --card ID --model qwen3.5-4b` walks the steps, each verified by a command, and finishes a fixture task with zero free-form planning turns.

- **Run a per-card bare-vs-card lift arm in Louhi and store lift on the card** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the standing rule says a capability counts only when measured; Uplift part 1 gives Smith-on-local scoring. Cards admitted without lift will be thousands of noise lines.
  Done when: each card row has `lift_by_model` filled from paired runs, and `sampo cards list --unlifted` is empty before a card is served.

- **Retrieve cards at the failure, keyed on the error text, not at session start** — FEATURE — value 4 — effort M — risk low — category: retrieval
  Why: injection size is a main concern in earlier ideas (MASTER.md, SessionStart weight); small context windows make start-time card dumps costly. Assumption: tool errors are catchable in the Smith loop.
  Done when: a failing command in Smith pulls at most 2 cards by error shingle and token cost per turn stays under a set budget in the hook bench.

- **Grow the card grid by failure mining, filling empty (kind × stack × stage × surface) cells first** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the grid exists (T-2909); thousands of cards need a source that is not the writer's imagination. Closed tasks and local-model exam failures are real signals Sampo didn't author.
  Done when: `sampo cards gaps` lists empty cells ranked by exam-failure count, and a generation run fills the top 20 with admitted cards.

- **Write one card per tool gap: a "tool-gap ladder" (find, build stdlib-only, ask grant)** — FEATURE — value 4 — effort S — risk low — category: tool acquisition
  Why: Mission 7 is exactly this decision; small models skip straight to "install X". Done when: a 4B model given a missing-tool fixture follows the ladder and produces a tested stdlib script instead of a grant request when one suffices.

- **Distil a floor model per card: find the smallest model that passes it and print that on the card** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: the model list spans 4B to 27B; routing by measured floor saves the 27B's ~3 min swap cost (steer on llama-swap). Done when: each card carries `floor_model`, and Smith picks the resident model that meets it before asking for a swap.

- **Tournament merge: rival cards for one cell compete in Louhi, losers fold into the winner** — FEATURE — value 4 — effort M — risk med — category: dedupe/quality
  Why: thousands of cards drift into near-duplicates; Moonscale's funnel already dedupes candidates by embedding. Done when: cells with more than 3 cards drop to the top-lift 1–2 with a recorded merge log.

- **Retire cards by half-life when the served model changes or the model passes bare** — CLEAN — value 3 — effort S — risk low — category: lifecycle
  Why: the fingerprint of the endpoint changes with model swaps; stale cards cost context. Done when: re-running a changed profile marks cards `retired` where bare pass ≥ card pass, and they stop being retrieved.

- **Poison-test every card: a cold reader must flag a planted unsafe step** — SECURITY — value 3 — effort S — risk low — category: card safety
  Why: cards instruct weak models to run commands; they must pass the Ward and the injection rules. Done when: admit rejects a card containing a planted `curl | sh` or fence-escape step, in a unit test.

- **Wild: Let the failing small model write its own post-mortem card, verified by a retry** — FEATURE — value 4 — effort M — risk med — category: self-learning — wild
  Why: assumption: the model's own failure phrasing is the vocabulary it will later retrieve on. Done when: a card authored after a 4B failure makes the same 4B pass the identical fixture on retry, else it is discarded.

- **Wild: A nightly "gladiator league" where each local model plays every card and the leaderboard goes on the Models page** — FEATURE — value 3 — effort M — risk low — category: observability — wild
  Why: the GPU idles at night and the user wants thousands of skills grown each generation. Done when: a morning table shows model × card-kind pass rates with day-over-day deltas.

- **Wild: Cassette cards — record a frontier run as a replayable script of tool calls with branch points a small model steps through** — FEATURE — value 4 — effort L — risk med — category: replay — wild
  Why: strongest scaffold is a frontier run itself; the Smith loop already has structured tool calls. Done when: replaying a cassette with a 9B on a variant fixture reaches the same verified end state, branching at least once.

- **Wild: Dumbest-model floor test for the tool forge — a 4B must be able to *use* every forged tool from its one-line passport alone** — FEATURE — value 3 — effort S — risk low — category: tool usability — wild
  Why: a tool no small model can call is not scaffolding. Done when: each forged tool's passport passes a 4B calling-exam before it is promoted.

Next question: Which card kinds does a 4B model fail on for reasons no card can fix (context length, tool-call format), and should those go to a trained adapter instead?
Next question: What is the real card hit rate in a live Smith session: how often is a retrieved card actually followed, and does the transcript show it?
