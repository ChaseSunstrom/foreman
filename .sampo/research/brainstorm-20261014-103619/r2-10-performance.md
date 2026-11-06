# Brainstorm — lens: performance

- **Compile the guard's static rules into native permission rules** — PERFORMANCE — value 4 — effort M — risk med — category: hooks
  Why: assumption: Claude Code's `permissions.deny`/`ask` still apply under bypass mode. The guard spawns a Python hook for every Bash call, and bench_hooks.py gates latency. Generate deny rules from the guard's table for decidable cases (`rm -rf ~`, `curl|bash`). Leave the hook only the residual that needs parsing.
  Done when: bench_hooks shows Bash PreToolUse spawns drop ≥50% on a replayed session, and a parity test proves the generated rules and the hook agree on the guard corpus.

- **Re-topologise hooks by event** — PERFORMANCE — value 4 — effort M — risk low — category: hooks
  Why: 14 hook events are registered. Assumption: the host supports `async` hooks, an `if` filter, and `http` hooks. Make bookkeeping hooks (ledger, MessageDisplay, Notification) async, narrow matchers or add `if` filters so irrelevant tools never spawn a process, and merge or split same-event hooks by measured critical path. Optionally route the hot ones over HTTP to `fm serve`.
  Done when: `fm doctor` prints a per-event table (spawns, p50, p95, blocking vs async), and total blocking hook ms per tool call falls ≥30% in bench_hooks.

- **Cut output tokens between tool calls (silent-worker style)** — PERFORMANCE — value 4 — effort S — risk med — category: output
  Why: assumption: decode time dominates turn latency, and an output style already exists. Switch the style by phase: no prose between tool calls while executing, full prose at the close-out and on asks. Measure with the transcript parser already in use.
  Done when: on 20 replayed tasks, median output tokens between tool calls fall ≥40% with no drop in bench pass rate.

- **Replace `claude -p` micro-judgments with native prompt hooks** — PERFORMANCE — value 3 — effort M — risk med — category: latency
  Why: assumption: prompt-type hooks run a single-turn small-model call. Fuzzy checks (tier classification, steer-vs-question) currently pay a child-process cold start. Use a prompt hook where the answer is a short verdict.
  Done when: one such judgment is moved over, its median latency is lower than the `claude -p` path, and its verdict agrees with the old one on ≥95% of a recorded corpus.

- **Give `claude -p` children a lean profile** — PERFORMANCE — value 3 — effort S — risk low — category: children
  Why: fm ideas, second-session and reviewers start full sessions. Assumption: a settings override can drop plugins, MCP servers and Foreman's own hooks for read-only children. Foreman's own hooks firing inside its children is waste and a recursion risk.
  Done when: child cold-start time and first-turn input tokens are measured before and after, and both drop ≥25% with identical outputs on a fixed prompt.

- **Diet each subagent's tool schema** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: six subagents and 482 transcripts exist, and every tool definition costs tokens every turn. Read first-turn cache-creation tokens per agent from the transcripts, then set `tools`/`disallowedTools` to the minimum each role needs.
  Done when: a table of schema tokens per agent exists, and scout and recon first-turn tokens are down ≥20% with their evals unchanged.

- **Skip injecting what the context already holds** — PERFORMANCE — value 3 — effort M — risk med — category: context
  Why: assumption: UserPromptSubmit and SessionStart re-inject STATE and brief text on many turns. Check the live transcript since the last compact. If the same hash is still in view, inject a one-line pointer instead.
  Done when: injected bytes per turn fall ≥40% on a replayed 30-turn session, and resume after `/compact` still re-injects in full.

- **Spool the ledger per session and merge at close** — PERFORMANCE — value 3 — effort M — risk med — category: state
  Why: lanes and sessions share one central ledger. Append to a per-session spool on tmpfs (`/run/user`), then merge into the durable ledger at Stop, PreCompact and SessionEnd. This removes lock contention and fsync from the hot path.
  Done when: 8 concurrent lanes writing 1k events each show no lock waits and lower p95 write latency, and a kill -9 mid-run loses at most the unmerged spool, which `fm doctor` recovers.

- **Add an S-task express lane with an overhead budget** — PERFORMANCE — value 4 — effort M — risk med — category: ceremony
  Why: the user keeps asking for faster. Ceremony (brief, plan, review, close-out) costs the same on a one-line FIX as on an L task. Measure overhead (hook ms + injected tokens + non-work turns) as a ratio of task time. S FIX tasks skip optional passes when the ratio would pass a threshold.
  Done when: S-tier tasks show overhead ≤15% of wall-clock in the ledger, and the done-gate still requires recorded evidence.

- **Make the statusline a zero-spawn file read** — PERFORMANCE — value 2 — effort S — risk low — category: statusline
  Why: assumption: the statusline command runs a process on every refresh. Hooks write a precomputed line to a file, and the statusline command becomes a `cat` or tiny shell.
  Done when: statusline render time is <5 ms (measured) and the content is identical to the current output on a fixture.

- **Capture slow hook runs from the real environment** — PERFORMANCE — value 3 — effort S — risk low — category: observability
  Why: bench_hooks is synthetic. When any hook exceeds its budget in real use, write its phase timings (imports, state load, work) to a ring file, and show the top offenders in `fm doctor`.
  Done when: an artificially slowed hook shows up in `fm doctor` with its slowest phase named.

- **Offer a guarded `fm do` recon bundle (wild)** — FEATURE — value 4 — effort L — risk high — category: round trips
  Why: wild. The model often chains read → grep → read → test as separate round trips. `fm do` takes a list of read-only ops in one Bash call, and each op is judged by the guard (one PreToolUse covers the bundle) and returns digested output.
  Done when: a bundle of 5 reads and greps completes in one tool call, any write op in it is refused, and round trips per recon phase drop ≥50% on a replay.

- **Hedge slow read-only children (wild)** — PERFORMANCE — value 2 — effort M — risk low — category: tail latency
  Why: wild. For idempotent children (fm ideas lenses, scouts), launch a duplicate when a call passes its p90 and keep the first answer. Pay double only on the tail.
  Done when: p99 of fm ideas wall-clock falls ≥30% on 20 runs, at <10% extra tokens.

- **Keep the prompt cache warm when the user is about to return (wild)** — PERFORMANCE — value 3 — effort M — risk med — category: cache economics
  Why: wild. A rewrite of a large context costs far more than a cache read. Predict the return time from the user's past gaps. If the expected saving beats the ping cost, schedule one tiny keep-alive via ScheduleWakeup or a session cron just before the TTL, and skip it when the user is likely gone.
  Done when: a simulation over recorded session gaps shows net token-cost savings, and the live feature logs each ping's cost against the cache hit it earned.
