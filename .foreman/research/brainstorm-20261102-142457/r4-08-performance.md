# Brainstorm — lens: performance

- **Virtualize `time.sleep` across the test suite** — PERFORMANCE — value 4 — effort M — risk med — category: test speed
  Why: assumption: with 414 test files covering timers, lock timeouts, usage-limit waits and drive pacing, real sleeps and timeouts make up a measurable share of ship-gate wall time. The fake-clock idea exists for readers only, not for waits.
  Done when: a conftest-level virtual clock replaces sleep and monotonic across the suite, and a before/after run of the full suite shows wall time down by the measured sleep share, with identical pass/fail.

- **Run likely-to-fail tests first** — PERFORMANCE — value 4 — effort S — risk low — category: ship gate
  Why: assumption: flakes.json and the ledgers already hold per-test fail history and durations. A red ship gate currently pays for the whole run before it says so.
  Done when: replaying the last 30 red gates, the first failing test starts within the first 10% of the run in at least 80% of them.

- **Cache test results per file by measured dependency hash** — PERFORMANCE — value 4 — effort M — risk med — category: ship gate
  Why: the existing ideas cache by whole-tree hash or by static impact guesses. Tracing which modules and files each test file actually opens gives a sound per-file key, so editing one lib module reruns only its dependents.
  Done when: a one-line edit to a single `plugin/lib` module reruns only test files whose traced dependencies include it, and the full suite still runs as a nightly backstop with identical results.

- **Call `fm` in-process from tests instead of spawning it** — PERFORMANCE — value 3 — effort M — risk low — category: test speed
  Why: assumption: many of the 414 test files launch `fm` as a subprocess. Each launch pays interpreter start and imports for a call that could be `main(argv)`.
  Done when: a census lists subprocess spawns per test file, the top 20 are converted, and suite time drops while one e2e roundtrip keeps the real subprocess path.

- **Record lock-wait time per state lock** — PERFORMANCE — value 3 — effort S — risk low — category: concurrency
  Why: the recent commit T-2653 shows `LockTimeout` is a real failure class, but nothing says which lock is hot when lanes, ticks and hooks overlap.
  Done when: each lock acquisition logs wait milliseconds, and `fm doctor` prints the top three locks by p95 wait over 7 days, or says "no contention".

- **Batch small cold reads into one child call** — PERFORMANCE — value 3 — effort M — risk med — category: model cost
  Why: the steers require a cold Haiku read on every tower file, with Sonnet on any non-pass. Each read is its own `claude -p` start with a repeated charter. Assumption: items can be judged independently in one structured call.
  Done when: reading 10 files costs at least 40% fewer tokens and less wall time than 10 separate calls, with per-item verdicts agreeing with the unbatched verdicts on a planted-fail set.

- **Flag redundant reruns on an unchanged tree** — PERFORMANCE — value 3 — effort S — risk low — category: waste
  Why: the prove cache covers only `fm prove`. Sessions also rerun the same test or build command on the same tree hash with no edit between. Assumption: the transcript and ledger carry enough to detect this.
  Done when: the finish receipt lists "N reruns on an unchanged tree, M seconds", and a planted duplicate command is flagged in a test.

- **Bench hooks under contention and run background work at idle priority** — PERFORMANCE — value 4 — effort M — risk low — category: hook latency
  Why: `bench_hooks.py` measures a quiet machine, but the user lives with hooks while the drive, lanes or the ship gate are running. Assumption: nothing sets nice/ionice on unattended children.
  Done when: the bench has a "suite running" mode, drive and gate children start under `nice`/`ionice` idle, and hook p95 under load stays within 1.5× the quiet p95 (gated).

- **Memoize the Genesis sweep per cited-file hash** — PERFORMANCE — value 3 — effort M — risk med — category: tower speed
  Why: the sweep re-runs after every fix task closes, and each coverage cell cites a file. Unchanged cells need no re-check. Assumption: sweep checks are pure functions of the cited files.
  Done when: a second sweep after touching one file re-checks only cells citing it, and a sweep diff against a full run is empty.

- **Keep a warm pool of cold-read children** — PERFORMANCE — value 3 — effort L — risk high — category: child latency — wild
  Why: assumption: `claude -p` start-up dominates short tool-less calls. A long-lived stream-json child per model, with context reset between items, would remove it. The risk is context leaking between independent reads.
  Done when: median cold-read latency drops at least 30%, and a canary string planted in read N never shows up in read N+1.

- **Fork-server for tests** — PERFORMANCE — value 3 — effort M — risk med — category: test speed — wild
  Why: assumption: each test file re-pays Python start and `fm` library imports. A pre-imported zygote that forks per test file pays them once and keeps tests isolated.
  Done when: suite wall time falls at least 25% on a 4-core run with no new cross-test failures across 3 shuffled runs.

- **Tune install settings with a 5-second host microbench** — FEATURE — value 3 — effort M — risk med — category: host tuning — wild
  Why: assumption: the best daemon on/off choice, lane count and shard count differ across hosts. This host keeps scratch on a tmpfs under `/run/user`, and others will differ. The tuner writes a plain config the user can read.
  Done when: `fm doctor` shows the chosen profile with the numbers behind each choice, and the bench on a deliberately slow-disk fixture picks a different profile than on tmpfs.

- **Start the cold read when a tower file is saved** — PERFORMANCE — value 2 — effort M — risk med — category: speculation — wild
  Why: assumption: tower files change rarely between save and filing, so a verdict computed at save is usually ready by filing. It is discarded when the content hash differs.
  Done when: filing a tower file whose hash matches a finished speculative read adds zero wait, and a changed file never uses the stale verdict.

Next question: which Foreman waits does the user actually sit through (ship gate, `fm doctor`, hook latency, or model children), measured in their minutes per week, so the order above can be set by pain, not by guess?
Next question: how much of the full suite's wall time is sleeping, subprocess spawn or real work? No idea here is sized until that profile exists.
