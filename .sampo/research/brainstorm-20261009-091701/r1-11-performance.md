# Brainstorm — lens: performance

Reading "performance" as speed, cost and throughput: hook latency, gate time, queue utilisation, token spend and cold starts. The pack shows `bench_hooks.py`, the slow-gate friction signal, and sessions idling with 20+ tasks queued. Everything else below is marked as an assumption.

- **Run hooks through a resident daemon** — PERFORMANCE — value 4 — effort L — risk med — category: latency
  Why: assumption: every PreToolUse, PostToolUse and Stop hook starts a fresh `python3` that re-imports the fm modules. `bench_hooks.py` exists, so latency already matters.
  Done when: `bench_hooks.py --runs 20` shows median guard-hook latency at least 5x lower with the daemon up, and the hooks fall back to the cold path when it is down, with identical decisions on the 5000-command replay.

- **Run only the gates a diff can affect** — PERFORMANCE — value 5 — effort M — risk med — category: gates
  Why: `fm map` already links tests to source and `fm impact` finds dependents, but `fm check` runs the whole gate. T-0424 shows slow gates are a recorded friction.
  Done when: after editing one lib file, `fm check --impacted` runs only the linked tests, and `fm task done` still runs the full gate before closing.

- **Reuse gate results by tree hash** — PERFORMANCE — value 4 — effort M — risk low — category: caching
  Why: T-0424 notes "reused 0.0 s passes" in the ledger, so reuse is already informal. Lanes and the main checkout often re-run identical trees.
  Done when: running a gate twice on an identical tree hash records a cache hit with the original evidence, and any file change, or a change to the gate command or environment, forces a real run.

- **Dispatch lanes from the queue automatically** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: JARVIS idled with 20+ queued tasks, and the T-0401 and T-0429 drive fixes still depend on the model choosing to start a lane. `fm relate` and `fm impact` supply the dependency and file-overlap data.
  Done when: with 6 queued tasks and no pairwise file overlap, `fm drive` keeps N lanes running up to a configured cap. Overlapping tasks are serialised, and a test shows the schedule.

- **Route each step to the cheapest model that passes** — FEATURE — value 5 — effort L — risk med — category: cost
  Why: `fm bench` replays finished tasks and `fm cost` splits tokens by task. Together they can show which task types pass first time on a smaller model. Classify, intake, recon and reviewer lenses are likely candidates (assumption).
  Done when: `fm bench` reports pass rate and cost per model per task type, and a routing table drawn from it is applied to `fm run`, with a one-flag revert.

- **Keep the injected context cache-stable and measured** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: SessionStart, UserPromptSubmit and the statusline all inject text, and `fm cost` only shows totals. Assumption: volatile fields such as timestamps and counters sit ahead of stable text and break the prompt-cache prefix.
  Done when: `fm cost --context` lists bytes injected per hook, the stable text comes first, and a test fails if a hook's output prefix changes between two identical-state calls.

- **Index briefs, ledger and recall in SQLite** — PERFORMANCE — value 3 — effort M — risk med — category: storage
  Why: assumption: `recall`, `queue`, `relate`, `digest` and `why` scan markdown briefs and event files. With 430+ tasks and growing, these commands will slow down.
  Done when: `fm recall` on a 1000-task synthetic store returns in under 100 ms, the index rebuilds from the files if deleted, and the files remain the source of truth.

- **Bisect hook-latency regressions automatically** — PERFORMANCE — value 3 — effort S — risk low — category: regression
  Why: `bench_hooks.py` and `fm friction` already exist, but nothing ties a slowdown to a commit.
  Done when: `fm friction` flags a latency p95 rise over a threshold and names the first commit that crossed it, using `git bisect run` on the bench.

- **Wild: Start verification of task N in a side lane while N+1 begins** — FEATURE — value 4 — effort L — risk high — category: pipelining
  Why: wild, assumption: the done-gate, review lenses and `fm smoke` are mostly waiting time. Today the main thread waits on them before the next task starts.
  Done when: a task's gate and smoke run in a worktree snapshot while the next task starts. A failure there pauses the new work, reopens the earlier task and names the failing evidence.

- **Wild: Pre-plan queued tasks at idle in the background** — FEATURE — value 4 — effort M — risk med — category: speculation
  Why: wild: `fm night` already runs budgeted background work and `fm second plan` can use another model. Planning is latency the user waits for at task start.
  Done when: an idle queue gets drafted plans for its next 3 tasks, each stamped with the tree hash it assumed. When the task starts, a plan whose hash still matches is reused and a stale one is discarded.

- **Wild: Shard gates across machines** — FEATURE — value 3 — effort L — risk high — category: multi-machine
  Why: wild: the pack lists multi-machine work as wanted, and `fm serve` plus `fm session` already manage remote-capable sessions. Heavy gates could run on idle boxes.
  Done when: `fm check --remote host` ships the tree by `git`, runs the shard there and returns signed evidence into the ledger, with the local run as fallback.

- **Keep a pool of warm headless sessions for `fm run`** — PERFORMANCE — value 3 — effort M — risk med — category: cold start
  Why: `fm run` starts a fresh `claude -p` per task, which means plugin load, SessionStart injection and cold caches each time (assumption about cost).
  Done when: a benchmark shows time-to-first-tool-call per queued task falling by a measured margin with the pool, and a session is never reused across tasks without a clean-context check.

- **Shard gates by measured duration** — PERFORMANCE — value 3 — effort M — risk low — category: gates
  Why: T-0424 added gate timing over real runs, so per-test and per-gate durations are available to balance a split.
  Done when: `fm check` splits independent gates and test files across CPUs by recorded duration, total wall time drops against the serial run, and failures print in a stable order.

- **Enforce a latency and cost budget in the done-gate** — CLEAN — value 3 — effort S — risk low — category: guardrails
  Why: the evals and benches measure correctness. Nothing stops a hook change from adding 200 ms per tool call (assumption).
  Done when: the gates fail a change that exceeds the committed p95 guard latency or hook-injected bytes, and a lowered budget requires a recorded `fm decide`.
