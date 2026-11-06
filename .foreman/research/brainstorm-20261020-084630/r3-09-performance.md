# Brainstorm — lens: performance

- **Make SessionStart non-blocking** — PERFORMANCE — value 4 — effort M — risk low — category: startup
  Why: assumption: SessionStart currently does map age checks, doctor-style probes and resume scans before the first prompt. The pack shows many such features (map refresh, resume offer, "welcome back", greeting) but no time-to-first-prompt measurement.
  Done when: SessionStart reads one precomputed snapshot file (written by Stop or a background refresher) and `bench_hooks.py` shows its p95 CPU time under a fixed bound with a 1,500-file map.

- **Nudge parallel tool calls** — PERFORMANCE — value 4 — effort S — risk low — category: turns
  Why: assumption: the model often issues independent reads or greps one per turn. Every extra turn re-pays the context, which is the cost driver in the long-session +60% finding. Nothing in the ideas list targets call batching.
  Done when: a transcript scanner flags runs of 3+ consecutive independent read-only calls, a one-line note fires once per session on the third, and a replayed fixture shows the scanner's flag rate.

- **Chain bookkeeping in one `fm` call** — FEATURE — value 4 — effort M — risk low — category: turns
  Why: the user asked for "fewer turns spent on Foreman itself." Step done, criterion tick and task close are still separate tool calls. Inferring bookkeeping removes some of them; chaining removes the rest at low risk.
  Done when: `fm step done 2 + ac 1 + close` runs as one call with one combined output line, and an e2e roundtrip closes a task in one fewer tool call than before.

- **Memoize guard verdicts by command shape** — PERFORMANCE — value 3 — effort M — risk med — category: hooks
  Why: "Skip the guard subprocess for harmless read-only calls" is listed, but repeated non-trivial commands (test runs, git status) are re-parsed every time. A verdict cache keyed by a normalized token shape plus a hash of guard rules and relevant state avoids that. Risk: the guard must never weaken.
  Done when: the 24-dangerous and 25-everyday corpora give identical verdicts with the cache on and off, and a cold-vs-warm run shows lower hook CPU time on repeated commands.

- **Set reasoning effort per phase** — PERFORMANCE — value 3 — effort M — risk med — category: cost
  Why: assumption: bookkeeping and mechanical edits don't need the same reasoning effort as planning. Cost parity (T-1231) is the user's top open goal, and Foreman's premium is output and turn overhead. Ablate on the duel before shipping.
  Done when: a duel arm with low effort for bookkeeping turns shows lower cost at the same hidden-test pass rate over 3 runs, or the idea is dropped with the numbers recorded.

- **Run duel cases concurrently under one budget governor** — PERFORMANCE — value 3 — effort M — risk low — category: benchmarks
  Why: the benchmark runs (`--runs 3`, long-session, marathon) are slow and cost-capped by hand. A shared dollar governor with per-case caps lets cases run in parallel and aborts cleanly at the ceiling.
  Done when: a 6-case suite finishes in under half the sequential wall time and stops launching new cases when the cap is hit, with the stop recorded in the results file.

- **Keep a warm fork-server for the test suite** — PERFORMANCE — value 3 — effort M — risk med — category: dev loop
  Why: `plugin/tests/` has 226 files, and CI was recently red on CPU-time bounds. Most per-test time is interpreter and `fmlib` import. Tiers are listed; a fork-server that imports once and forks per test is not.
  Done when: the fast tier runs at least 2x faster locally than separate `python3` invocations, with identical pass/fail results.

- **Rotate and compress cold ledger segments** — PERFORMANCE — value 3 — effort M — risk low — category: state
  Why: the ideas list has tail-by-offset, sidecar indexes and shards, but no bound on growth. The repo has 1,000+ briefs and months of ledger, and `.foreman` also holds transcript copies.
  Done when: segments older than N days are gzipped with a rollup file, every ledger reader returns the same aggregates, and `.foreman` size stops growing linearly in a 1,000-session synthetic run.

- **Refresh `fm map` incrementally by git tree hash** — PERFORMANCE — value 3 — effort M — risk low — category: indexing
  Why: the map covers 1,560 files and is regenerated for packs. Re-mapping only changed subtrees (via `git ls-tree` hashes) keeps it fresh without a full walk.
  Done when: after touching one file, `fm map` re-reads only that file's subtree and its output is byte-identical to a full rebuild.

- **Budget site weight and fix first paint together** — PERFORMANCE — value 2 — effort S — risk low — category: site
  Why: T-1244 shows the stored theme applying only after load, causing a flash. Add a tiny inline head script and a CI check on page bytes and render-blocking requests, since the Benchmarks page keeps growing.
  Done when: no theme flash in a screenshot diff at load, and CI fails if any page exceeds its recorded byte budget.

- **Wild: Move the hook hot path to a native binary** — PERFORMANCE — value 3 — effort L — risk high — category: hooks
  Why: wild; assumption: Python startup dominates hook latency on every tool call. A small compiled guard (verdict table plus shell tokenizer) handles the common allow path, and anything unusual falls through to the Python guard. The guard must never weaken, so it needs a differential test against the Python one.
  Done when: native and Python verdicts match on the full mined-refusal corpus and the 49 benchmark commands, and p95 hook latency on the allow path drops by a stated factor.

- **Wild: Verify speculatively on a copy-on-write snapshot at every edit** — PERFORMANCE — value 4 — effort L — risk med — category: proofs
  Why: wild; close-time proofs are serial turns. Running the task's verify commands in an overlay snapshot after each edit, in the background, makes `fm task prove` an instant lookup of a result already computed for that exact tree.
  Done when: closing a task whose last edit was more than N seconds earlier takes under one second to prove, and a stale snapshot never counts as proof for a different tree.

- **Wild: Bisect performance regressions nightly** — PERFORMANCE — value 3 — effort M — risk low — category: regression
  Why: wild; CI bounds only catch a regression after the fact. A nightly job that runs `bench_hooks.py` using CPU counters and bisects to the offending commit would file the task itself (assumption: counters are stable enough on one runner).
  Done when: a deliberately slowed hook on a branch is bisected to the right commit and a task naming that commit is created.
