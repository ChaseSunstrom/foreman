# Brainstorm — lens: deepen: research proof

**Answers to earlier questions (research-proof lens)**
- A model writes the research note and a cold model reads it, with no user-owned check between them. A source ledger with an exact-match quote check would be that check, and it costs zero tokens.
- Foreman's own site stats, trigger precision and exam recall are computed only by the code that produced them. Nobody else recomputes them.

**Ideas**

- **Build a claim ledger as the one research evidence kind** — FEATURE — value 5 — effort M — risk low — category: research proof
  Why: the pack lists nine research-proof ideas that all need one record: claim, source, quote, fetch date, hash, status. Assumption: no such store exists yet, since T-2273 and T-2288 cover only typed, data and perf proof.
  Done when: `fm task finish` on a research task refuses to close without a ledger file, and each row has all six fields.

- **Verify every quote by exact match against a stored snapshot** — FEATURE — value 5 — effort S — risk low — category: research proof
  Why: a fabricated or paraphrased citation is the commonest research failure, and a string search catches it for free. This fits the standing rule to use signals Foreman didn't author. Assumption: sources are fetchable as text.
  Done when: a test ledger with an invented quote fails `fm prove --research`, and the same ledger with a real quote passes.

- **Tag each claim by how it was learned: ran, read, or recalled** — FEATURE — value 5 — effort S — risk low — category: provenance
  Why: a model can't cite its own memory. Claims with no source are the riskiest, yet they look identical to sourced ones. Assumption: the writer can be forced to pick a class.
  Done when: a "recalled" claim can't be the sole basis for closing a task, and the unproven rollup lists it.

- **Turn decision-driving claims into executable probes** — FEATURE — value 5 — effort M — risk med — category: docs vs code
  Why: Mission 7 asks for docs checked against code. A claim like "library X supports Y" can be run as a tiny test against the installed version, which beats any citation.
  Done when: a claim marked `probe:` runs its command and records pass or fail, and a false claim turns the ledger row red.

- **Show a proof ladder on every surface** — FEATURE — value 4 — effort S — risk low — category: unproven rollup
  Why: T-2273 counts typed and inconclusive evidence. Research needs finer labels: cited-only, quote-verified, probe-verified, corroborated. Whatever can't be proven stays labelled unproven.
  Done when: `fm status` and the web UI show per-rung counts for done research tasks.

- **Fan out stale or flipped claims to every dependent task and decision** — FEATURE — value 4 — effort M — risk med — category: provenance
  Why: a claim is the cause of a plan, a steer or a decision, so when it expires or is refuted those should reopen. Assumption: tasks and decisions can name claim ids.
  Done when: marking a claim refuted adds a "re-check" note to each task citing it, visible in `fm next`.

- **Use per-kind half-lives and a staleness sweep** — FEATURE — value 4 — effort S — risk low — category: freshness
  Why: version numbers, prices and API behaviour rot quickly, while language semantics last. `fm doctor` can name expired claims, the same way it names a missing steer check.
  Done when: a claim older than its kind's half-life shows in `fm doctor`, and re-verifying resets the clock.

- **Check source independence by origin, not by URL** — FEATURE — value 4 — effort M — risk med — category: corroboration
  Why: "two sources" that are syndicated copies or cite each other prove nothing. This deepens the circular-source idea: cluster by canonical upstream and by shared text shingles, and require two independent roots for high-stakes claims.
  Done when: two mirrored pages count as one root, and a claim needing two roots fails with one.

- **Hunt counter-evidence with a blind tool-less child** — FEATURE — value 4 — effort M — risk med — category: adversarial
  Why: this matches the standing rule to use a different model that never sees the writer's reasoning. It gets only the claim and searches for contradictions. An unresolved dispute gets labelled unproven.
  Done when: a seeded known-false claim is flagged by the child, with its counter-source recorded in the ledger.

- **Recompute Foreman's own published numbers with an independent script** — CLEAN — value 4 — effort S — risk low — category: self-audit
  Why: answers the earlier question about unchecked numbers. Site stats, trigger precision and held-out recall come only from the producing code. Assumption: raw events are enough to recompute them.
  Done when: a second small script reproduces each published number from raw events, and `fm doctor` flags any mismatch.

- **Replicate research blind and diff the conclusions** — FEATURE — value 4 — effort M — risk med — category: replication — wild
  Why: assumption: a child given only the original question and no claims, re-deriving the answer, is the strongest check against a shared writer-judge blind spot. Disagreement is a flag and agreement raises confidence.
  Done when: a replication run writes a diff of conclusions to the ledger, and a disagreement blocks "proven".

- **Score Foreman's research calibration against what later held** — FEATURE — value 3 — effort M — risk low — category: calibration — wild
  Why: T-2290 already records predictions and scores them for effort. Extending it to claims means recording confidence before the research and scoring it when a claim is later refuted or confirmed. This gives a per-source-type reliability curve.
  Done when: `fm stats` shows a calibration table for claims, and the plan gate asks for a spike where past confidence ran too high.

- **Learn source trust from outcomes, per user** — FEATURE — value 3 — effort M — risk med — category: source reputation — wild
  Why: assumption: domains whose claims were later reverted or refuted should lose weight, which resembles trigger routing learning from drops. The trust list stays local and editable.
  Done when: a domain with 2+ refuted claims is marked "check twice" on the next research task.

- **Archive sources locally, with opt-in external archiving** — FEATURE — value 3 — effort M — risk med — category: local-first — wild
  Why: sources disappear, and a content-addressed local vault keeps a claim checkable offline. Sending a URL to an archive service publishes it, so that step needs an explicit setting, off by default.
  Done when: with the setting off, a dead link still verifies against the local snapshot, and nothing leaves the machine.

Next question: Which research claims have already shaped a shipped decision, and could any be re-checked today to see whether it still holds?
Next question: Where does the user decide a source is good enough, and can that judgement be stored once as a reusable trust rule?
