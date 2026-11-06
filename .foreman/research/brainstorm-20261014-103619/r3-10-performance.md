# Brainstorm — lens: performance

- **Collapse the per-event Python spawn into one persistent hook server** — PERFORMANCE — value 5 — effort L — risk med — category: hook latency
  Why: 14 hook events each spawn Python, and the pack gates on `bench_hooks.py`. Earlier ideas covered a resident daemon and native `if` filters in general, but not the fallback path: a tiny shell shim that tries a unix socket first and only cold-starts Python when the socket is absent, so a crash degrades to today's behavior.
  Done when: `bench_hooks.py --runs 20` shows p50 for PreToolUse under 15 ms with the server up, and killing the server still yields correct verdicts (just slower).

- **Measure per-turn token cost of Foreman's injected context and enforce a budget in CI** — PERFORMANCE — value 5 — effort M — risk low — category: token cost
  Why: Foreman injects at SessionStart, UserPromptSubmit and PreCompact, and has 73 skills plus MASTER.md. Prior ideas said "cap the instruction tokens" and "keep context cache-stable", but none turns that into a gate. Assumption: the injected text is measurable by replaying hook output.
  Done when: `fm doctor` prints injected tokens per event and fails when a budget file is exceeded; a test proves a deliberately bloated injection trips it.

- **Lazy-load skill descriptions by task tier** — PERFORMANCE — value 4 — effort M — risk med — category: context size
  Why: 73 skills means 73 descriptions in every session's context, though an S-tier FIX needs about 6. Assumption: skill-listing cost is non-trivial. Generating a per-project subset (as plugin skill sets or path scopes) lets idle skills cost zero.
  Done when: a fresh session in a fixture repo lists fewer than 20 skills, and the e2e roundtrip still passes.

- **Snapshot-hash the whole done-tail so unchanged trees skip it** — PERFORMANCE — value 4 — effort M — risk med — category: gate speed
  Why: Recent commits show `fm task finish --run` always running the full suite once, even when every step has evidence. Earlier ideas covered per-test caching by input hash; this one keys the entire finish sequence on tree hash plus gate-config hash, with a forced-rerun escape hatch.
  Done when: finishing a second task on an identical tree plus config reports "reused @hash" with no test processes spawned, and any file change forces a full run.

- **Run the finish gates in a forked clone while the next step proceeds, and merge the verdict back** — PERFORMANCE — value 4 — effort L — risk high — category: pipelining
  Why: Gates run serially at close-out, which is dead time for the user. Earlier ideas had a side lane for verification of N while N+1 begins (wild). This version makes it default for S/M tasks, using a copy-on-write worktree and a verdict that blocks only the *close*, not the *start*.
  Done when: on a two-task queue, task 2's first edit timestamp precedes task 1's gate completion, and a failing gate re-opens task 1 automatically.

- **Profile the model's own idle: log every turn gap and attribute it** — PERFORMANCE — value 4 — effort S — risk low — category: idle time
  Why: The user complained "make sure it doesn't sit idle like it is" (T-0758). Nothing says why it idles. Instrument Stop, MessageDisplay and the wake paths with timestamps and classify each gap as waiting on the user, a gate, a child, a wake that never came, or a model stall.
  Done when: `fm idle` lists the last 24 h of gaps over 60 s, each with a cause label, and the T-0758 repro shows up as one concrete cause.

- **Cache the project map and ledger reads in a memory-mapped binary index** — PERFORMANCE — value 3 — effort M — risk low — category: startup
  Why: The map covers 341 files and the ledger grows forever; every hook and `fm` call re-parses state. Earlier ideas had SQLite indexing, but not a read-only mmap snapshot rebuilt on write that makes `fm status` and the statusline O(1).
  Done when: `fm status` on a 10× synthetic ledger runs under 30 ms, same as on the small one.

- **Pre-compute the next-step brief during the current step's tool latency** — PERFORMANCE — value 3 — effort M — risk med — category: speculation
  Why: Several ideas rehearse the next task while idle. This one is narrower: while a long Bash gate runs in the background, a haiku child drafts the next step's recon so it lands in context just as the gate returns.
  Done when: on a seeded two-step plan, step 2's recon file exists before step 1's gate returns, and is discarded if step 1 fails.

- **Reuse a reviewer's session across rounds with a per-round diff, not a fresh read** — PERFORMANCE — value 3 — effort M — risk med — category: token cost
  Why: Reviewers re-read the whole diff on every re-review. Earlier "continue the same reviewer" covers it loosely; this specifies sending only the delta since the last reviewed tree hash plus the prior findings, and measuring the saving.
  Done when: round-2 reviewer input tokens are under 40% of round 1 on a fixture, with the same findings caught.

- **Wild: Keep a hot-standby warmed Claude session per project that the next request is handed to** — PERFORMANCE — value 4 — effort L — risk high — category: cold start
  Why: assumption: cold session start plus context load dominates S-task latency. A headless session sits pre-loaded with the map and lessons, and `fm run` adopts it, so the first token arrives sooner. wild
  Done when: time from request to first tool call drops at least 40% against a cold `fm run` on the fixture repo.

- **Wild: Race the test suite against a "predicted red" model and stop early on the first confirmed failure** — PERFORMANCE — value 3 — effort M — risk med — category: gate speed
  Why: Failed gates cost the full suite's time. Order tests by failure likelihood learned from the ledger (not just tests linked to changed files), run in that order, and abort on the first red so the fix starts sooner. wild
  Done when: on replayed historical failures, median time to first red falls at least 50% versus the default order.

- **Wild: Show a live "latency tax" bill at close-out: seconds Foreman added versus bare Claude Code** — PERFORMANCE — value 4 — effort M — risk low — category: overhead visibility
  Why: The user asks for "faster" but has no figure for what the discipline layer costs. Sum hook time, injected tokens, gate time and idle gaps, then print a one-line receipt that makes regressions embarrassing. wild
  Done when: every finished task shows "Foreman overhead: Xs hooks, Y tok, Zs gates" and the figures match `bench_hooks.py` within 10%.

- **Auto-bisect hook-latency regressions per release in the release script** — PERFORMANCE — value 3 — effort S — risk low — category: regression guard
  Why: Releases ship via release.py. Hook speed is only checked by the manual bench. Run it at release time, compare it with the last release's stored numbers, and block on a regression above a threshold.
  Done when: a deliberately slowed hook fails `release.py` with the offending event named.
