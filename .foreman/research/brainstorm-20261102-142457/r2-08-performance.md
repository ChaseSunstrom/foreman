# Brainstorm — lens: performance

- **Launch hooks with `python -I -S` and a frozen import set** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: assumption: hooks start cold Python on every call. The pack shows `plugin/tests/bench_hooks.py` and many hook-latency ideas, but none touch interpreter flags. `-S` skips `site`, `-I` skips user site and env lookups. This also helps with the planted-`json.py` risk.
  Done when: `bench_hooks.py --runs 20` shows a lower median for every hook, and the hook test suite passes with the flags on.

- **Seek windowed readers to the window start** — PERFORMANCE — value 4 — effort M — risk low — category: ledger reads
  Why: readers such as digest, outcomes and `check_usage_burn` ask for "the last N days", and the pack notes ledger growth and a "10× ledger size" timing idea. Binary-search or reverse-read the ledger by timestamp, so cost scales with the window and not the file. This differs from the listed "verified-up-to cursor" because it needs no stored state.
  Done when: a 10× synthetic ledger gives the same digest output, and read time for a 7-day window is flat as the file grows.

- **Verify the hash chain from the last checkpoint** — PERFORMANCE — value 3 — effort M — risk med — category: integrity cost
  Why: `verify-ledger` and `fm drill --restore` walk the whole chain. Write a checkpoint every N lines holding the running hash, verify only the tail on routine runs, and verify in full nightly. Assumption: full verification is already the slowest doctor row.
  Done when: tail verification on a 10× ledger is under a set millisecond budget, and a flipped byte before the checkpoint is still caught by the full pass.

- **Count fsyncs per hook and group-commit ledger appends** — PERFORMANCE — value 3 — effort M — risk med — category: write path
  Why: assumption: each ledger append does its own flush. The hash chain and the torn-tail work (T-2664) mean durability matters, so measure before changing. Batch the appends inside one hook invocation into a single write plus one fsync.
  Done when: a strace-based test shows at most one fsync per hook call, and the torn-write drill still passes.

- **Run doctor checks in parallel and print a timing table** — PERFORMANCE — value 3 — effort S — risk low — category: doctor
  Why: `fm doctor` has accumulated many checks (state durability, ledger conservation, model-ID probes, restore drills). Run the independent read-only checks in a thread pool, and add `--timing` with the slowest rows first.
  Done when: wall time drops against serial execution on the same state, and `--timing` lists every check with milliseconds.

- **Build the skill trigger index at install time** — PERFORMANCE — value 3 — effort M — risk low — category: skills
  Why: `plugin/skills/` holds 1388 of the 2129 files. Precompute one JSON file of names, descriptions and triggers so routing never walks the tree. This is not the listed bundle-packing idea, because the files stay as they are.
  Done when: skill lookup opens one file, an index-versus-tree consistency check passes, and a stale index is rebuilt automatically.

- **Keep a warm pool of lane worktrees** — PERFORMANCE — value 3 — effort M — risk med — category: lanes
  Why: parallel `fm lanes` (Missions 5–8) each create a worktree and wait for it. Pre-create idle worktrees at the current HEAD and re-point them on claim. Assumption: worktree creation is a visible share of lane start.
  Done when: time from lane spawn to first command drops against the cold path, and a reclaimed worktree always starts clean (tested).

- **Gauge the prompt-cache hit ratio per session** — PERFORMANCE — value 3 — effort S — risk low — category: token cost
  Why: "Keep the injected prefix byte-stable" is listed, but nothing measures whether it works. Read cache-read versus cache-creation tokens from the transcript usage and flag a session whose ratio falls. It then also serves as an outside check on `fm cost`.
  Done when: `fm cost` prints the hit ratio, and a deliberate prefix change in a fixture lowers it and triggers the flag.

- **Ratchet peak memory and open file descriptors per verb** — PERFORMANCE — value 2 — effort S — risk low — category: footprint
  Why: the existing ratchets cover time and tokens, not memory. The tmpfs under `/run/user/1000` is RAM, and the drive and lanes run for long stretches. Record the maximum RSS and fd count in the bench.
  Done when: the bench fails when a verb's peak RSS grows past its stored baseline by more than the noise floor.

- **Benchmark hooks against recorded real payloads** — PERFORMANCE — value 3 — effort M — risk low — category: benchmark realism
  Why: assumption: `bench_hooks.py` uses synthetic inputs. Real tool-result payloads are large (diffs, test output) and can dominate the cost. Sample redacted real hook inputs into a fixture corpus and run the p95 over them.
  Done when: the bench reports p95 per payload size bucket, and the corpus includes at least one input larger than 1 MB.

- **Wild: Compile the guard to a native binary that hooks prefer** — PERFORMANCE — value 4 — effort L — risk high — category: guard speed
  Why: wild. The guard sits on every Bash call, and cold Python is the floor for hook latency. Emit the rule table to a small static binary (Go or Rust, built if a toolchain exists). Hooks use it when present and fall back to Python otherwise. Verdicts are differential-tested against the Python guard on the replay corpus.
  Done when: the binary and the Python guard return identical verdicts on every replay case, and the binary's median hook time is several times lower.

- **Wild: Keep a derived columnar sidecar of the ledgers for instant aggregates** — PERFORMANCE — value 3 — effort L — risk med — category: read model
  Why: wild. A rebuildable, memory-mapped sidecar (class, time, task, cost columns) makes digest, outcomes, usage and the web UI Today charts sub-millisecond. The ledger stays the source of truth and the sidecar is deleted and rebuilt on any mismatch, so it fits the "derived, rebuild nightly" idea.
  Done when: deleting the sidecar and rebuilding gives byte-identical `fm digest` output, and the digest is faster on a 10× ledger.

- **Wild: Give every hook and verb a millisecond line in a shared budget** — PERFORMANCE — value 3 — effort M — risk low — category: perf governance
  Why: wild. Treat latency as a currency. A table of per-hook millisecond allowances sums to a total session-overhead ceiling. A new feature must name its cost, and a task that adds to a hook's time without taking from another fails the ship gate, which is more specific than the listed "pay for each new verb with a removal".
  Done when: `fm ship` fails on a fixture change that raises hook p95 past its allowance, and the budget table prints in `fm doctor`.

- **Show a header within 100 ms for slow verbs** — PERFORMANCE — value 2 — effort S — risk low — category: perceived speed
  Why: `fm map`, `fm doctor` and `fm exam` can run for seconds with nothing printed. Print the first useful line at once and stream the rest. This is perceived latency, so it is unlike the listed `--deadline` partial answers.
  Done when: for each named slow verb, time to first output is under 100 ms in a test with a stubbed slow step.

Next question: which hook or verb does the user actually wait on most in a normal day, measured on their real machine, and is that the one the bench measures?
Next question: how much of Foreman's wall-clock overhead per task is spent waiting on its own ceremony (plan, prove, finish) compared with the model, and would the user trade any of it for speed?
