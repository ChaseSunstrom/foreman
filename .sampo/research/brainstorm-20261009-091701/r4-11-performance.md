# Brainstorm — lens: performance

- **Infer each gate's true inputs from the files it reads** — PERFORMANCE — value 5 — effort L — risk med — category: gate speed
  Why: wild. Tree-hash reuse and diff-based gate selection are already listed, but both assume the inputs are known. Trace file opens during a gate run (strace or fanotify, falling back to mtime sampling) and build a per-gate read-set. A gate is then skipped only when none of its real inputs changed.
  Done when: editing a file outside a gate's recorded read-set skips that gate, editing one inside re-runs it, and a test shows a planted hidden input (e.g. an env-file read) is learned after one run.

- **Schedule around the prompt-cache TTL** — PERFORMANCE — value 4 — effort M — risk low — category: token cost
  Why: assumption: the prompt cache expires after a short idle window. The drive idles, waits on background jobs, and offers queued work, and each gap can cost a cold re-read of the whole prefix. Order lane starts and reviewer fan-out inside one cache window, and have the drive issue the next prompt before expiry or deliberately let it lapse.
  Done when: `fm cost` reports cache-hit ratio per task, and a replayed queue shows a higher ratio with the scheduler than without.

- **Roll up transcripts and the ledger incrementally** — PERFORMANCE — value 4 — effort M — risk low — category: CLI latency
  Why: `fm cost`, `usage`, `digest`, `friction`, `taste` and `claude list` all derive from transcripts and the ledger, which only grow. Keep per-file byte-offset watermarks and materialized aggregates, so each run parses only the new tail and a full rebuild stays available as `--rebuild`.
  Done when: on a 1 GB transcript fixture, a second `fm cost` run is under 200 ms, and its output equals the full-rebuild output.

- **Tune lane concurrency like TCP** — PERFORMANCE — value 4 — effort M — risk med — category: orchestration
  Why: assumption: lane count is fixed or manual. JARVIS shows the queue backing up (20+ queued, idle sessions), and lanes also compete for CPU, RAM and API rate limits. Use additive-increase, multiplicative-decrease: add a lane while load, 429s and gate times stay healthy, and halve on rate-limit errors or swap.
  Done when: in a simulated run with injected 429s, concurrency falls within one cycle and recovers, and the ledger records each adjustment with its reason.

- **Rebase lanes continuously so merges are fast-forwards** — PERFORMANCE — value 4 — effort M — risk med — category: lanes
  Why: lane merge was refused beside a dirty main checkout (T-0403). A background rebase of each idle lane onto main, with a shared rerere cache, makes landing a ref move rather than a conflict negotiation.
  Done when: after main advances, an idle lane's merge-base equals main's tip within 60 s, and a conflicting rebase parks the lane with a named-files note instead of corrupting it.

- **Memoize bench and evolve by case reach** — PERFORMANCE — value 4 — effort M — risk low — category: self-improvement
  Why: `fm bench` and `fm evolve` replay whole tasks per candidate. Key each result by (plugin tree hash, case), and re-run only cases whose recorded hook and skill touches overlap the candidate's diff.
  Done when: changing one skill file re-runs only the cases that loaded it, and the memoized and full-run verdicts match on the whole bench.

- **Stream delta patches to the UI** — PERFORMANCE — value 3 — effort M — risk low — category: UI latency
  Why: `fm ui --json` and `projects --follow` appear to emit full snapshots, which grows with sessions and projects. Emit versioned JSON patches with an etag, and let Desktop and the web UI apply them.
  Done when: with 50 projects, an idle second sends under 1 KB, and the rendered state equals a fresh full snapshot after 1,000 random events.

- **Prefetch reads one plan step ahead** — PERFORMANCE — value 4 — effort M — risk med — category: round trips
  Why: wild. The plan names the next step's files, so Foreman can precompute `outline`, `impact` and `why` for them. It injects them through the hook before the model asks, with a hit-rate tracked in the ledger.
  Done when: on benched tasks, tool calls per task drop while pass rate holds, and a prefetch miss costs no extra tokens.

- **Rank gates by return on time** — PERFORMANCE — value 3 — effort M — risk med — category: gate speed
  Why: ordering gates by failure odds is already listed, but not scoring each gate's catch-rate per second. Gates with near-zero catches and high cost move to the release tier (never silently dropped), and the move is a recorded decision.
  Done when: `fm gates --roi` lists catches, seconds and tier per gate, and a gate demoted by the score still runs at release.

- **Learn output digesters from what the model reuses** — PERFORMANCE — value 4 — effort L — risk med — category: token cost
  Why: wild. `fm quiet` only does success-vs-tail. Mine transcripts for which lines of a noisy command's output the model actually quoted or acted on, then synthesize a per-command digester that keeps those line shapes and always keeps failures.
  Done when: for the five noisiest repeated commands, digested output is at least 70% smaller, and a replay shows no added re-run commands.

- **Rotate the session when the context slope turns bad** — PERFORMANCE — value 3 — effort M — risk med — category: long sessions
  Why: assumption: very long sessions get slower and costlier per turn. Track per-turn latency and tokens against context size, and at a measured knee do a curated handoff and fresh session instead of waiting for `/compact`.
  Done when: a long run shows a rotation at the configured threshold, and the new session resumes at the exact step with fewer tokens per turn.

- **Run test workers from a pre-imported fork server** — PERFORMANCE — value 3 — effort S — risk low — category: test speed
  Why: 88 test files that import fm modules repeat interpreter and import startup. Fork each test process from one warm parent, skipping any test that mutates module state.
  Done when: the gate's wall time drops at least 30% on the bench, and the pass/fail sets match the cold run.

- **Report flow metrics and recommend a WIP limit** — PERFORMANCE — value 3 — effort S — risk low — category: queue flow
  Why: JARVIS idled with 20+ queued tasks. Compute cycle time, queue age and blocked-wait share per task type from the ledger, and name the bottleneck (user asks, gates, lane merge, usage pace).
  Done when: `fm digest` shows one bottleneck line backed by numbers, and a seeded fixture with a slow gate reports "gates".

- **Compress briefs with a learned abbreviation dialect** — PERFORMANCE — value 2 — effort L — risk high — category: token cost
  Why: wild. Briefs, STATE and ledger lines are re-read every session. Evolve a terse, reversible notation per project, and keep it only if bench pass rate holds while injected tokens fall.
  Done when: bench pass rate is unchanged and the injected tokens per session drop at least 25%, with a lossless decode to plain text.
