# Brainstorm — lens: deepen: trust

- **Publish a signed run bundle per benchmark row** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the existing "link every number to its raw run" and "fm bench repro" ideas both need one artifact: transcripts, hidden-test results, cost ledger, model ID, Foreman and Claude Code versions (2.1.301 vs 2.1.304), hash-chained. The pack says every site claim must be measured and prose figures are hard-coded (T-1246).
  Done when: `fm bench verify <bundle>` recomputes a published row's pass count and cost from the bundle alone and exits non-zero if any byte was altered.

- **Generate every site figure from the bundles at build time** — FIX — value 5 — effort M — risk low — category: site
  Why: T-1246 says prose figures are hard-coded; the pack shows the numbers moved (+29% → +14%), so stale prose is a live risk.
  Done when: the site build fails if any number in the Benchmarks prose lacks a bundle reference, and changing a bundle changes the rendered figure.

- **Add a claims ledger with expiry** — FEATURE — value 4 — effort M — risk low — category: claims
  Why: Foreman last adapted to 2.1.301 while 2.1.304 is out; measured claims go stale when Claude Code changes. Assumption: claims are listed as structured entries.
  Done when: each claim records the Claude Code version it was measured on, and the page shows "unverified on 2.1.304" and CI warns once a claim is behind the newest release.

- **Lead the cost story with the 60% long-session premium** — FIX — value 4 — effort S — risk low — category: honesty
  Why: Foreman is ~60% dearer on the long session ($0.095 vs $0.059) and +10–14% on small tasks. Putting that beside the safety result before the user finds it is the trust move; the user wants cheaper and faster.
  Done when: the Benchmarks page's first screen shows cost and time deltas, including the losses, next to the safety numbers.

- **Run a safety-regression canary on every Claude Code release** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: "the guard must never weaken" and the 24-dangerous/25-everyday corpus already exists. New releases change hook behavior (the `decider: "person"` and `tool.check` changes, the 12-hook limit).
  Done when: CI runs the 24+25 corpus against the newest Claude Code and fails if any dangerous command passes or any everyday one is stopped.

- **Wild: Publish a live false-positive wall** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: "0 of 25 everyday commands stopped" is a small sample, and the guard blocks real work. Users can submit commands they were wrongly stopped on, and the corpus grows publicly. wild
  Done when: the page shows the corpus size and the false-positive rate recomputed from the corpus, and a submitted command becomes a regression test.

- **Add a receipt for every guard refusal that says what it saw** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: the dropped T-premise item shows refusals needed replaying with `fm guard try` to judge them. A one-line, replayable receipt would make guard decisions auditable by users.
  Done when: each refusal prints a rule ID and a `fm guard try` command that reproduces it.

- **Wild: Add an adversarial bounty for the guard** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: it extends the "beat Foreman" challenge to the safety claim: any command that does harm and passes gets added to the corpus with credit. wild
  Done when: a documented submission path exists and a passing bypass becomes a failing test before it gets fixed.

- **Show a per-session honest bill split** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: the 60% premium comes from bookkeeping calls and hook notes, and 15 skills occupy ~3,200 of ~9,600 listing characters, re-sent after every compaction. Users need to see where Foreman's tokens go.
  Done when: `fm cost` splits a session's tokens into task work, hook notes, bookkeeping calls and skill listing, and the totals match the transcript to within 2%.

- **Pre-register benchmarks with committed hidden-test hashes** — FEATURE — value 3 — effort S — risk low — category: benchmarks
  Why: it turns "pre-register each benchmark" into something checkable: commit the hash of the hidden tests and the run plan before running, so results can't be reshaped afterward.
  Done when: a published row links to a commit that predates its run and contains the hash of its hidden tests.

- **Wild: Run a public overnight marathon stream** — FEATURE — value 3 — effort L — risk med — category: demo
  Why: the marathon found 3 extra fixes through 7 compactions. A live, capped, cheap (Haiku) run with a running cost counter and a plain-Claude control lane next to it makes the claim observable. wild
  Done when: a page streams both lanes' diffs, hidden-test status and dollar spend until the cap, and ends with a final table.

- **Separate the "measured" and "believed" claims in the README** — CLEAN — value 3 — effort S — risk low — category: honesty
  Why: the README's "plan before it edits" and "proves its work" claims sit beside measured results. Marking which have a benchmark prevents unmeasured claims from borrowing the measured ones' credibility.
  Done when: each README claim links to a bundle or carries an explicit "not benchmarked" tag.

- **Wild: Make a counterfactual replay of the user's own past session** — FEATURE — value 3 — effort L — risk med — category: trust
  Why: it combines "score your own session" and the ghost bill: replay a user's local transcript's prompts with plain Claude on Haiku, capped, and report cost and pass differences, with data kept local. wild
  Done when: `fm bench mine --cap 2` produces a report from one local session without sending anything beyond the model calls the user approved.
