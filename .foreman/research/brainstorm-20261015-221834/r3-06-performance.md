# Brainstorm — lens: performance

- **Cache the resume scan as a per-worktree stat-keyed index** — FEATURE — value 4 — effort S — risk low — category: resume speed
  Why: T-1028 plans "find a stopped builder's worktree, branch, task and brief"; assumption: this walks `git worktree list` plus ledger on every SessionStart, which is slow with many worktrees.
  Done when: with 30 worktrees, the resume lookup reads one index file, and a second run spawns zero git subprocesses (counted by a test shim).

- **Make `fm ui` worktree listing incremental** — PERFORMANCE — value 3 — effort S — risk low — category: pane cost
  Why: "fm ui lists worktrees" (T-0.12.0) and the Agents node graph redraw on each tick; assumption: it re-lists all worktrees per frame.
  Done when: an unchanged worktree set costs no `git` calls across 100 pane ticks, verified by call count.

- **Budget the card selector by imports on the edit path** — PERFORMANCE — value 4 — effort M — risk med — category: edit-time latency
  Why: the request is to inject cards by imports and deps across 1,084 cards (only 6 ever fired). Scanning the library at each edit would blow the hook budget. Distinct from the existing memoize idea: this sets a hard ms ceiling and falls back to deps-only matching when over it.
  Done when: `bench_hooks.py` shows the PostToolUse card path under a stated ms at 5,000 cards, and a test shows over-budget degrades to the coarse match, not a skip.

- **Lazy-load card bodies, keep only a trigger table in memory** — PERFORMANCE — value 3 — effort S — risk low — category: memory/IO
  Why: 1,158 skill files and growing card libraries (T-1037 bulk growth) make full parsing expensive; assumption: cards are parsed whole on load.
  Done when: selecting cards reads only a compact trigger file, and card bodies are opened only for the cards injected.

- **Skip hint lookup when the error has no fingerprint** — PERFORMANCE — value 3 — effort S — risk low — category: known fixes
  Why: T-1032 offers known fixes after failures; running lookup on every tool result is wasteful. Gate it on a cheap failure signal (nonzero exit or error token) first.
  Done when: a successful Bash result performs zero hint-store reads, asserted in a test.

- **Chunk the Agents graph layout so it recomputes only on topology change** — PERFORMANCE — value 3 — effort M — risk low — category: pane cost
  Why: the node graph, live tree (T-1033) and work bar all animate; assumption: layout is recomputed each frame even when only a status colour changed.
  Done when: a status-only update reuses cached node positions; layout runs are counted and stay at 1 over a 50-tick status flip.

- **Cap the brainstorm pack by tokens with a reused prefix** — PERFORMANCE — value 3 — effort S — risk low — category: token cost
  Why: this pack repeats "The user's own words" twice and carries about 300 prior idea titles; every lens pays for it. Dedupe sections and keep the stable prefix first so caching hits.
  Done when: the built pack contains each section once and the stable prefix is byte-identical across lenses.

- **Collapse idea-history into clusters before feeding it back** — PERFORMANCE — value 3 — effort M — risk low — category: token cost
  Why: "Ideas so far" is a long flat list with many near-duplicates ("Resume any stopped agent…" appears about five times). Send one line per cluster with a count.
  Done when: the prior-ideas block shrinks at least 60% on this pack, and a test shows no cluster is lost.

- **Wild: Pre-warm a worktree for the next queued task during the current close** — PERFORMANCE — value 3 — effort M — risk med — category: latency hiding
  Why: assumption: worktree creation plus dependency priming is the dead time between tasks in the queue. Wild.
  Done when: the next builder starts with its worktree already on disk, and an unused pre-warm is reaped within a set time.

- **Wild: Hot-reload the pane from a ledger tail instead of re-gathering** — PERFORMANCE — value 4 — effort L — risk med — category: pane cost
  Why: `gather()` in `fmwatch.py` re-reads recent ledger and history; the pane must fill the dock exactly and redraw often. Apply events as deltas to a held model and rebuild only on drift. Wild.
  Done when: a 10,000-line ledger costs the same per tick as a 100-line one, measured by a bench.

- **Wild: Self-timed Foreman that demotes its own slowest hook rule** — PERFORMANCE — value 3 — effort L — risk high — category: self-tuning
  Why: the user wants Foreman to genuinely improve itself, and the latency tests exist already. Let it log per-rule cost, then propose moving the worst offender to async or Stop-time, as a reviewable patch rather than silently. Wild.
  Done when: a seeded slow rule is flagged in a weekly report with a drafted patch, and nothing is changed without approval.

- **Bound resume cost by a transcript-tail digest cap** — PERFORMANCE — value 3 — effort S — risk low — category: resume speed
  Why: resuming a stopped builder should not replay a long transcript. Cap the "where was I" digest at a fixed token size, keeping the last plan step, last failing command and diff stat.
  Done when: the digest for a 5 MB transcript is under the cap and still names the open step and last failure.
