# Brainstorm — lens: performance

- **Move non-gating hooks to `async` and measure the saved wall-clock** — PERFORMANCE — value 4 — effort S — risk low — category: hooks
  Why: Pack lists 14 hook events, several purely recording (PostToolUse, SubagentStop, MessageDisplay, Notification, SessionEnd), and hooks are latency-gated by bench_hooks.py. Earlier ideas covered a resident daemon and native `if` filters, not async-vs-sync classification. Assumption: the host supports `async: true` on command hooks.
  Done when: each hook is tagged gating or recording in one table, recording hooks run async, and `bench_hooks.py --runs 20` shows a lower p95 turn-added latency with the ledger still complete in the e2e roundtrip.

- **Budget idle-turn cost with a cache-TTL-aware keepalive** — PERFORMANCE — value 4 — effort M — risk med — category: cache
  Why: The user said "make sure it doesn't sit idle". Using ScheduleWakeup or Monitor to wake a session after the prompt-cache TTL lapses means the whole context is re-billed and re-read slowly. Assumption: a TTL of about 5 minutes.
  Done when: `fm doctor` reports per-session idle gaps split into under-TTL and over-TTL, and the wake scheduler fires at under-TTL intervals when work is queued, with a test using a fake clock.

- **Give every Agent call a wall-clock and token budget, and log overrun by role** — PERFORMANCE — value 4 — effort M — risk low — category: delegation
  Why: Agent accepts per-call model and effort, and Foreman has 6 subagents but no delegation ROI measurement tied to latency (earlier ideas covered ROI ledgers generally, not the critical path). Assumption: SubagentStart/Stop timestamps are already in the ledger.
  Done when: `fm stats agents` lists p50/p95 duration and tokens per role and model, and flags roles whose median exceeds a configured budget.

- **Run independent gates concurrently with a shared read-only tree snapshot** — PERFORMANCE — value 4 — effort M — risk med — category: gates
  Why: Gates include `fm doctor`, the e2e roundtrip and bench_hooks, and the suite is 149 test files. Earlier ideas covered ordering, sharding and caching by tree hash, but not running unlike gates in parallel against one snapshot. Assumption: gates are currently sequential.
  Done when: the done-tail's wall-clock equals roughly its slowest gate (not the sum) on this repo, and a gate that mutates the tree is detected and forced serial.

- **Collapse the injected session preamble to a hash-addressed delta** — PERFORMANCE — value 3 — effort M — risk med — category: tokens
  Why: Resume after `/compact` or a new session re-injects the state each time. Earlier ideas covered cache-stable context and budgets, but not sending only what changed since the last injection to the same session. Assumption: the injected block is mostly stable between prompts.
  Done when: a second UserPromptSubmit in one session injects fewer bytes than the first on an unchanged queue, and the resume e2e still restores the exact step.

- **Profile startup of `fm` itself and lazy-import its 48 lib modules** — PERFORMANCE — value 3 — effort S — risk low — category: cold start
  Why: Every hook and CLI call spawns Python 3.12 and imports from plugin/lib, which has 48 modules. Assumption: the entry point imports eagerly.
  Done when: `python3 -X importtime plugin/bin/fm status` shows fewer modules loaded than before, and a CI check fails if a hook path imports a module from a deny-list (for example the bench or recall modules).

- **Stream-parse transcripts and the ledger with byte offsets instead of rescanning** — PERFORMANCE — value 3 — effort M — risk low — category: indexing
  Why: Mining catch rates, give-up points and lessons reads results across 1,000+ transcripts. The recent '✗ exit N' parser fix shows these scans are frequent. Assumption: scans re-read from the start.
  Done when: a second `fm` mining run over unchanged transcripts reads at most the appended bytes, verified by a counted-reads test.

- **Wild: Race the first test run against the builder's own typing** — PERFORMANCE — value 3 — effort L — risk med — category: speculation
  Why: wild. Once a PostToolUse edit lands, a background process runs the linked tests (the deferred T-0214 sentinel) and the result is waiting before the model's next turn.
  Done when: for a seeded edit, the failing-test result is in context at the next turn without an explicit run, with an added-latency bound under the hook budget.

- **Wild: Keep a hot spare `claude -p` child per project for `fm ideas` and reviewers** — PERFORMANCE — value 3 — effort M — risk med — category: warm pool
  Why: wild. The pack's headless children each cold start. A pooled, pre-primed child (map, MASTER summary loaded) answers the first call faster.
  Done when: the median time to the first output of a reviewer child drops measurably versus a cold start in a benchmark, and the pool is reaped on session end.

- **Wild: Print a "seconds Foreman added" line at every close-out, split by hooks, gates and idle** — PERFORMANCE — value 3 — effort S — risk low — category: transparency
  Why: wild. The user keeps pushing on speed, and the earlier idea of a latency bill needs the decomposition to be actionable. Assumption: hook timings can be summed per task from the ledger.
  Done when: `fm task finish` output shows hook, gate and idle seconds for the task, and they sum to within 5% of the measured wall-clock overhead.

- **Skip the done-tail for unchanged trees, and re-run only the criteria whose files changed** — PERFORMANCE — value 4 — effort M — risk med — category: gates
  Why: The recent change forced `fm task finish --run` to always run once as the final check, so repeated finishes pay the whole suite. Assumption: evidence can be indexed by file reads (an earlier idea covered staleness on touch).
  Done when: a second finish on an unchanged tree runs zero tests but still records fresh evidence referencing the tree hash, and a one-file change reruns only the linked tests.

- **Set the effort and model per step type from measured first-pass success per dollar** — PERFORMANCE — value 3 — effort M — risk med — category: routing
  Why: The user asked whether Foreman can spawn lower models (T-0755). Earlier ideas proposed a learned routing table, but not the cost-per-first-pass metric with an explicit fallback to a higher model on gate failure. Assumption: the ledger records model per lane.
  Done when: `fm stats routing` shows cost per passing step by model and step type, and S-tier lanes pick the cheapest model whose pass rate is above a floor, with an escalation test.

- **Wild: Make the band and pane read a single mmap'd snapshot written by the hooks** — PERFORMANCE — value 2 — effort M — risk low — category: UI
  Why: wild. The statusline and mod would not spawn Python at all, and refresh would be a file read (this goes past the earlier zero-spawn statusline idea by sharing the snapshot with the pane).
  Done when: the statusline renders in a single file read with no child process (verified by strace count), and the pane reflects a state change within one refresh tick.

- **Detect and kill hung gate processes with a per-gate p99 timeout learned from history** — PERFORMANCE — value 3 — effort S — risk low — category: gates
  Why: Flaky and slow gates stall unattended runs (the user complained about idle sitting). Assumption: gate durations are recorded in the ledger.
  Done when: a seeded gate that sleeps past 3× its historical p99 is terminated with a recorded reason, and the queue continues to the next task.
