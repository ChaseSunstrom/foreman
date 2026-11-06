# Brainstorm — lens: performance

- **Stub re-reads of unchanged files** — FEATURE — value 4 — effort M — risk med — category: context cost
  Why: the long session costs ~60% more because context grows faster, and re-reading files is the largest repeat cost. Assumption: the foreman-ui mod's `tool.check` or a tool-result hook can swap a result.
  Done when: a second Read of an unchanged file in one session returns a stub ("unchanged since call N, hash h"). A replayed long-session case shows fewer input tokens and the same hidden-test pass rate.

- **Take user-only skills out of the model's listing** — PERFORMANCE — value 3 — effort S — risk low — category: skills
  Why: 15 skills are ~3,200 of ~9,600 listing chars, re-sent after every compaction. Assumption: `disable-model-invocation: true` removes a skill from the listing but leaves `/skill` usable.
  Done when: the post-compaction listing is smaller by the measured bytes of the skills marked user-only, and `doctor` confirms they still run by name.

- **Compact when the cache is already cold** — PERFORMANCE — value 3 — effort S — risk low — category: compaction
  Why: the Idle compaction row exists in `/config`, and unattended drives have gaps. After a gap the cache has expired, so compacting then costs no more than the next turn would. Assumption: the cache TTL is about 5 minutes.
  Done when: in a replayed marathon with scripted gaps, the drive triggers compaction at the gap, and total cost is at or below the compact-at-limit baseline.

- **Rank `fm` verbs by tokens returned to the model** — PERFORMANCE — value 4 — effort S — risk low — category: output size
  Why: bookkeeping calls drive the long-session overhead, and T-0828 (compact output) is deferred with no data on which verbs matter.
  Done when: `fm usage --tokens` lists verbs by total output tokens per session from the ledger, and the top 5 are shortened with a measured drop on the long-session benchmark.

- **Cap subagent returns by contract** — PERFORMANCE — value 3 — effort S — risk med — category: subagents
  Why: scouts and reviewers return prose into the main context, and the context tax is where Foreman loses to plain Claude Code. Assumption: current scout output is unbounded.
  Done when: bundled subagent prompts require a result of ≤300 tokens with the full output in a file path. A check fails any bundled agent without that clause, and recorded returns stay within the cap.

- **Choose the cache TTL per run type** — PERFORMANCE — value 3 — effort S — risk med — category: cost
  Why: unattended drives pause between turns for minutes, and each pause can cost a full-prefix cache miss. Assumption: the installed Claude Code has a 1-hour cache option.
  Done when: `fm run` sets the longer TTL only for unattended runs, and a Haiku-capped A/B shows lower cost per verified pass.

- **Precompile pycs for hooks at install** — PERFORMANCE — value 2 — effort S — risk low — category: hook latency
  Why: every hook is a Python process, and `bench_hooks.py` is already a gate. Assumption: cold imports dominate p50 on a fresh install or after an upgrade.
  Done when: the install step writes unchecked-hash pycs. First-run hook p50 after install is within 10% of warm p50 in `bench_hooks`.

- **Schedule gates longest-first from recorded durations** — PERFORMANCE — value 3 — effort M — risk low — category: gates
  Why: the gate set is `fm doctor`, the e2e roundtrip, and the bench, and CI has already needed CPU-time bounds on slow runners (T-1248).
  Done when: `fm gate` runs independent gates concurrently, ordered by a stored duration history, and wall time drops against the serial baseline with identical results.

- **Split the test suite into fast and full tiers with a time budget** — PERFORMANCE — value 3 — effort M — risk low — category: tests
  Why: `plugin/tests/` has 226 files and the macOS job is red (T-1249). A pre-commit tier would give faster feedback than waiting for CI.
  Done when: `fm test --fast` finishes under a declared budget, CI fails if it exceeds it, and the full tier still runs on push.

- **Add per-writer ledger shards, merged on read** — PERFORMANCE — value 2 — effort M — risk med — category: concurrency
  Why: parallel lanes and subagents all append to one ledger. Assumption: lock waits show up under 4+ builders.
  Done when: a 4-writer stress test shows zero lock waits and no lost or reordered entries, and readers return the same view as before.

- **Wild: Write the compaction summary ourselves from the ledger** — FEATURE — value 4 — effort L — risk high — category: compaction (wild)
  Why: the marathon showed 7 compactions and the long session showed Foreman compacting more often. A deterministic summary built from the ledger and the active task would be small and free.
  Done when: a forced-compaction run using the ledger-built summary passes the same hidden tests as the default summary, with fewer post-compaction tokens.

- **Wild: Add a live cost-parity governor** — FEATURE — value 4 — effort L — risk med — category: cost (wild)
  Why: the user wants Foreman cheaper than plain Claude Code, but today it is +10–14% on small tasks and +60% on the long one.
  Done when: the governor tracks Foreman's tax per session against a token-model baseline. Above a configured ratio, it drops the lowest-value hook notes, never guard rules, and logs each drop.

- **Wild: Keep a nightly $1 Haiku replay of the cost benchmarks** — FEATURE — value 3 — effort M — risk low — category: regression (wild)
  Why: the cost deltas were hard-won (Haiku +29% down to +14%) and nothing stops them creeping back.
  Done when: a scheduled job runs a fixed 3-case slice under a hard dollar cap and files a FIX brief if cost per verified pass rises more than the noise band.
