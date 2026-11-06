# Brainstorm — lens: context per turn

- **Route each hook line to the user or the model, never both** — FIX — value 5 — effort S — risk low — category: injection
  Why: SessionStart injects 2,733 characters twice. Assumption: one copy goes out as `additionalContext` and one as `systemMessage` (or a second plugin registers the hook), which no earlier idea separated.
  Done when: a captured SessionStart payload has each line in exactly one of the user-visible and model-visible fields, and the 2,733-character block reaches the model once.

- **Move the invariant block into the system-prompt position** — FEATURE — value 5 — effort M — risk med — category: cache
  Why: assumption: hook output lands in the message stream, while text from CLAUDE.md `@import` or `--append-system-prompt` joins the cached prefix. That prefix is identical across sessions and lanes. Only the volatile counters would stay in hooks.
  Done when: two fresh sessions show a non-zero `cache_read_input_tokens` on turn 1 for the Sampo block, and the hook payload shrinks by the moved bytes.

- **Detect cache breaks from usage fields** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: transcripts record cache_creation against cache_read per turn. Nothing in the pack checks whether a Sampo injection, a re-fire after compaction or a resume caused a spike. A leaner byte count that breaks the cache can cost more than it saves.
  Done when: `sampo burden --cache` lists the turns where cache_creation exceeded 3× the session median, each with the hook event that preceded it.

- **Inject the plan-before-edit contract at the first Edit or Write** — FEATURE — value 4 — effort M — risk med — category: lazy injection
  Why: the planning and one-task-at-a-time rules matter only when a file changes, and read-only sessions never need them. This is a different trigger from "teach at the block", which fires after a violation.
  Done when: a read-only session injects 0 plan-rule characters, and the first Edit turn carries the contract exactly once.

- **Keep Sampo state out of Grep, Glob and Read results** — FIX — value 4 — effort S — risk low — category: tool results
  Why: project state is 2.4 GB and the map lists 2,358 files, so one careless grep can pour ledger lines into the context. That is a per-turn burden none of the injection ideas address. Assumption: some state sits where the search tools can reach it.
  Done when: a Grep for a ledger-only string over the project returns 0 state hits, and a Ward-covered read of the ledger directory is refused with a pointer to the right verb.

- **Dedupe the injection against the user's own CLAUDE.md, memory and steers** — CLEAN — value 4 — effort M — risk low — category: duplication
  Why: assumption: standing rules such as "keep working the queue" and "no software installs" live in the user's memory files and in Sampo's steers, so the model reads them twice. Normalised sentence overlap would find them.
  Done when: `sampo burden --dupes` lists overlapping sentences by source pair, and the injected text drops each sentence found in a file the host already loads.

- **Let a local model pick the 3 rules this prompt needs, with a fixed fallback** — FEATURE — value 3 — effort M — risk med — category: relevance (wild)
  Why: the local qwen endpoint is free and idle. Sampo has about 40 rules but any one prompt touches only a few. A timeout falls back to the Ward line plus the fixed card.
  Done when: over 20 recorded prompts the tailored card averages under 40% of the full card's characters and keeps the Ward line in every case.

- **Spend a per-turn character allowance from a token bucket** — FEATURE — value 3 — effort S — risk low — category: budget
  Why: per-turn lines run 48 to 76 characters, and an exact total can't be fitted to every turn. Quiet turns earn allowance; a stall warning or a stage change spends it. This differs from a flat cap or a delta.
  Done when: a 50-turn replay never exceeds the bucket, and a turn with a Ward event is never refused for lack of allowance.

- **Price injections in token-turns, not characters** — CLEAN — value 4 — effort S — risk low — category: measurement
  Why: each per-turn line stays in history, so 76 characters over 200 turns is about 15,000 characters. The 2,733 characters at start are paid on every later turn too. Current gauges count only the emitted size.
  Done when: the ship gate fails if the replayed session's injected characters × remaining turns exceeds the recorded budget, and the report names the top source.

- **Draw a context flame chart per session in the web UI** — FEATURE — value 3 — effort M — risk low — category: visibility (wild)
  Why: a stacked area per turn, split by source (host, Sampo, tool results, user), with compaction cliffs and a marker where a Sampo injection fired. It shows the trend, which a point-in-time `sampo burden` cannot.
  Done when: the page renders a recorded 100-turn session with the injected sources shown separately, and it works without JavaScript.

- **Read 'MASTER.md refused' as a signal and answer it** — FIX — value 4 — effort S — risk low — category: docs
  Why: at 75,758 tokens, Read refuses MASTER.md outright. A hook on the failed Read could return the matching anchor and section list, so the agent doesn't give up or route around it. Distinct from sharding, which fixes the file itself.
  Done when: a refused Read of MASTER.md leaves the agent a section index of at most 600 characters, and a test asserts that this is the only text added.

- **Print the card's own price inside it** — FEATURE — value 2 — effort S — risk low — category: self-awareness (wild)
  Why: a first line such as `card: 700 tok, 4 turns paid` lets the model weigh its own overhead. A cold child can then report whether it changed behaviour, with no new gauge.
  Done when: the line appears once per session and its token figure matches the replay count within 5%.

- **Run the hostile-slow session soak: 500 turns, 3 compactions, 4 lanes** — PERFORMANCE — value 3 — effort M — risk low — category: soak
  Why: bench_hooks times a single hook, and the 48 to 76 character claim comes from short sessions. Long sessions after compaction may re-inject or grow.
  Done when: the soak prints characters injected per turn at turns 10, 100 and 500, and CI fails if the per-turn mean at turn 500 exceeds 1.2× that at turn 10.

Next question: which source contributes the most characters per closed task over a whole week (hook injection, tool output, doc reads or agent hand-backs), measured from transcripts rather than from hook payloads?
Next question: if the invariant block moves to the system prompt, does the Ward still hold when a user's own CLAUDE.md override or a different harness drops that text?
