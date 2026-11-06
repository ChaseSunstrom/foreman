# Brainstorm — lens: performance

- **Add a Foreman overhead share to every drive receipt** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the pack shows hook p95 benches and cold-start budgets, but nothing splits a run's wall time into model wait, tests, the ship gate and `fm` itself. Without that split, "lean" can't be checked against any one number.
  Done when: `fm run`'s end receipt prints the percent of wall time spent inside `fm` and its hooks, and a fixture run with an injected 2s hook delay shows that delay in the figure.

- **Ratchet injected tokens per session start and per prompt** — PERFORMANCE — value 5 — effort M — risk low — category: context cost
  Why: the pack has 1,388 skill files, many steers, and "count injected context in tokens, not characters" as a stated idea. Nothing yet fails a ship when the always-on prefix grows. Assumption: a tokenizer approximation is good enough for a ratchet.
  Done when: `fm ship` fails when the SessionStart plus per-prompt injection exceeds the stored budget by more than 2%, and names the emitter that grew.

- **Make ledger readers incremental with a verified-up-to cursor** — PERFORMANCE — value 4 — effort M — risk med — category: scaling
  Why: ledgers are append-only and hash-chained, and `verify-ledger`, `doctor`, `digest` and `outcomes` each re-read them in full. Earlier ideas only time the readers at 10× size; none removes the O(n) cost. Assumption: readers rescan from the top today.
  Done when: on a 10× fixture ledger, a second `fm doctor` run reads only the lines appended since the first, and truncating the cursor file falls back to a full verify with the same verdict.

- **Share one prompt-cache prefix across a brainstorm fan-out** — PERFORMANCE — value 4 — effort S — risk low — category: spend
  Why: every brainstormer gets the same long context pack plus one lens. Put the pack first and the lens last, so all N children hit the same cached prefix. "Keep the injected prefix byte-stable" covers the session, not the child fan-out. Assumption: children are launched close enough in time to share the cache.
  Done when: a 6-lens run shows cache-read tokens on lenses 2–6 at or above 80% of the pack size, recorded in the run's usage line.

- **Balance test shards by recorded durations across lanes** — PERFORMANCE — value 4 — effort M — risk low — category: ship gate
  Why: impacted-test selection and result caching are filed, but the full-suite backstop and nightly run (plugin/tests has 414 files) stay serial. Balancing by stored per-file durations cuts the critical path without skipping anything.
  Done when: the full suite split across 4 shards finishes in under 40% of serial time, and the union of shard results equals the serial pass/fail set.

- **Admit lanes by machine pressure, not a fixed count** — PERFORMANCE — value 3 — effort S — risk low — category: fleet
  Why: Missions 5–8 run parallel `fm lanes`, and state lives on tmpfs (`/run/user/1000`). A fixed lane count can starve the user's own work or hit memory limits. Gate each spawn on `/proc/pressure/{cpu,memory}` and free tmpfs space.
  Done when: under an injected memory-pressure fixture the drive holds a new lane and logs why, then releases it when pressure drops.

- **Flag serial tool calls that could have run in parallel** — FEATURE — value 3 — effort M — risk low — category: agent speed
  Why: the harness explicitly prefers parallel independent calls, and transcripts are already mined for other signals. Count runs of three or more consecutive independent reads or greps, then show the wasted round trips in the digest. Assumption: the transcript preserves the call order and results.
  Done when: a fixture transcript with 4 serial independent reads yields a "3 round trips avoidable" line, and a dependent chain yields none.

- **Give web UI views a render budget at 10k tasks** — PERFORMANCE — value 3 — effort M — risk low — category: web UI
  Why: the ledgers hold thousands of task ids, and the UI has golden-screenshot ideas but no performance gate. Add paginated or virtualized lists, ETag polling and a first-paint threshold.
  Done when: a 10k-task fixture paints the queue view in under 300 ms in the headless `fm shot` run, and an over-budget change fails the check.

- **Cap git calls per verb and cache by index mtime** — PERFORMANCE — value 3 — effort S — risk low — category: cold start
  Why: `fm status`, `map` and the doctor shell out to git repeatedly on big repos (2129 files here). A per-verb git-call counter, plus caching keyed on HEAD and index mtime, lowers the common-path latency.
  Done when: `fm status` makes at most 2 git subprocess calls on an unchanged tree, asserted in a test.

- **Wild: Give every verb a `--deadline` that degrades to a labelled partial answer** — FEATURE — value 4 — effort M — risk med — category: graceful degradation
  Why: wild. When a reader is slow, the hook or user waits. A deadline-aware verb returns what it has plus "partial: 3 of 5 ledgers read, denominators shown", which follows the stated rule to print the denominator on every "nothing found".
  Done when: with a 50 ms deadline against a 10× ledger, `fm doctor` exits in under 150 ms, marks the result partial, and lists the unread parts.

- **Wild: Report a "battery tax" for Foreman's idle wakeups** — FEATURE — value 3 — effort S — risk low — category: footprint
  Why: wild. Timers, the drive and the watchers run unattended. Sum their CPU seconds and wakeups per day from `/proc` or cgroup stats, and show it beside the lean row, so a laptop user sees what the always-on parts cost.
  Done when: `fm doctor` prints CPU-seconds and wakeups per day for each Foreman-owned unit, and a test unit that spins is ranked first.

- **Wild: Precompute the next likely proof while the model is still typing** — PERFORMANCE — value 3 — effort L — risk med — category: speculation
  Why: wild. While the model edits, run the prior task's proof command on a clean copy and keep the result keyed by tree hash. If the final tree hash matches, `fm task prove` returns instantly. This extends the filed prove cache by filling it ahead of need. Assumption: spare CPU exists during model waits.
  Done when: in a fixture where the final tree matches the speculated one, `fm task prove` returns the cached result in under 1 s, and a mismatched tree reruns the proof normally.

Next question: which `fm` verbs and hooks does the user wait on most in real sessions, measured per event from the hook ledger, and does the p95 differ between warm and first-of-day starts?
Next question: what share of total spend goes to Foreman's own children (brainstorms, cold reads, exams) versus the user's tasks, and has that share grown over the last four generations?
