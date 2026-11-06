# Brainstorm — lens: context per turn

- **Fire SessionStart once per session id** — FIX — value 5 — effort S — risk low — category: context
  Why: the pack says SessionStart injects 2,733 characters twice. Likely causes are two registered hooks (the sampo and foreman shim plugins both list the same hook) or a resume/compact re-fire. Assumption: the shim plugins' `dependencies` double-register it.
  Done when: a fresh session's transcript contains the session-start block exactly once, including when both `foreman` and `sampo` plugins are installed. A test counts occurrences.

- **Shard MASTER.md into a readable index plus per-verb pages** — CLEAN — value 5 — effort M — risk low — category: docs/context
  Why: at 75,758 tokens, Read refuses MASTER.md, so sessions can't consult the docs. Keep a short MASTER.md index, with anchors and "use when" lines, over `docs/master/<verb>.md` files that are each under 8k tokens.
  Done when: every file under the master docs passes Read without an offset, and a lint checks that every anchor in the index resolves.

- **Add a per-turn context budget table with an owner per line** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the 48 to 76 characters of per-turn burden are measured but not attributed. Print each injected string with its source hook, characters and the ledger row that justifies it, ranked by cost.
  Done when: `fm burden --turn` lists every per-turn string with its source and size, and the total matches the measured 48 to 76.

- **Replace repeated reminders with a content-hash stamp** — PERFORMANCE — value 3 — effort S — risk low — category: context
  Why: a per-turn note that is unchanged since the last turn carries no new information. Emit it once, then only a 6-character hash tag, or nothing, until it changes.
  Done when: over a 20-turn recorded session, the per-turn characters fall below the 48 floor, and an edit to the note re-emits it in full.

- **Compress the session-start block to a stable prefix plus a delta** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: the 2,733 characters are mostly the same on every session. Keep a fixed, cache-friendly prefix, and put the changing parts (open task, grants, warnings) in a short suffix below 400 characters. This also helps the prompt-cache hit rate.
  Done when: the byte-identical prefix is at least 80% of the block across two sessions on different days, and the suffix is capped at 400 characters.

- **Set a retention policy for the 2.4 GB project state** — FIX — type PERFORMANCE — value 4 — effort M — risk med — category: state
  Why: the state is 2.4 GB, and readers that scan it slow the hooks. Compact old transcripts, cold ledgers and lane worktrees into dated archives, keeping hash-chain anchors.
  Done when: `fm gc --plan` prints what it would reclaim, a real run keeps the state under a stated ceiling, and `fm doctor` still verifies the chain.

- **Fail the ship gate when injected context grows without a waiver** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: the lean substance rule exists, but no gate holds the hook-injected text. A committed baseline file holds the chars per hook and per turn.
  Done when: adding 100 characters to any injected string fails the gate until the baseline is updated with a recorded reason.

- **Wild: Read the context as a diet — a daily "calories" card** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: assumption: the user enjoys seeing weight. A one-line card, such as "yesterday Sampo cost you 11k tokens of context; 62% was read at turn 1", gives the lean story a visible number.
  Done when: the session-start suffix or `fm` shows yesterday's injected tokens, and `fm burden` agrees with it.

- **Wild: Make the agent answer "what did you learn from the injected text" at turn 5** — FEATURE — value 3 — effort M — risk med — category: evaluation — wild
  Why: assumption: some injected characters are never used. A probe drops a field from the injection at random and checks whether the answer changes.
  Done when: a report ranks the injected fields by how often their removal changed the outcome, and at least one zero-effect field is marked for deletion.

- **Wild: Hold a "one-page Foreman" turn — first prompt gets a 300-character context** — FEATURE — value 4 — effort M — risk med — category: context — wild
  Why: assumption: a first-turn minimum is enough, and the rest can be pulled on demand through `fm why`. Everything else lives behind named pointers.
  Done when: in an A/B on 9 held-out scenarios, the 300-character arm passes at least as many as the full block, and the context saved is reported.

- **Serve MASTER.md sections through a tiny `fm doc <verb>` verb** — FEATURE — value 4 — effort S — risk low — category: docs/context
  Why: Read refuses the file, and agents grep blindly. A verb returns just one verb's page and its anchor neighbours, so a query costs about 500 tokens instead of 75k.
  Done when: `fm doc ship` prints under 8k tokens, and every verb in `fm help` resolves.

- **Wild: Give every injected line a "last used" date and let unused lines die** — CLEAN — value 4 — effort M — risk med — category: lean — wild
  Why: assumption: lines that no later tool call or answer refers to have no use. After 30 days without a reference, a line moves from always-injected to on-demand, and a tombstone notes it.
  Done when: the injected total falls after a 30-day replay, and no exam scenario that passed before fails.

- **Log hook output sizes per event in the bench** — PERFORMANCE — value 3 — effort S — risk low — category: observability
  Why: `bench_hooks.py` times hooks, but the pack gives no sign that it records characters out. Per-event output size, beside the timing, shows which hook is the heavy one.
  Done when: the bench output includes a chars column per hook, and a regression of more than 10% in chars fails like a timing regression.

Next question: which of the injected strings has the model actually acted on in the last 14 days of real transcripts, and which has it never cited?
Next question: when the state directory is cut from 2.4 GB, which reader is the first to get slow or wrong, and is that on the hook path?
