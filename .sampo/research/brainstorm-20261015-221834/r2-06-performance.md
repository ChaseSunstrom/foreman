# Brainstorm — lens: performance

- **Resume without re-reading: snapshot the transcript's tail as a digest** — FEATURE — value 4 — effort M — risk low — category: resume cost
  Why: T-1028 plans worktree-builder resume, and the pack lists "Skip re-verifying unchanged proofs on resume" but nothing about the token cost of re-orienting a resumed agent. assumption: resumed builders re-read the brief, diff and ledger in full.
  Done when: a resumed builder's first turn injects a digest of ≤1,500 tokens (task, branch, last three steps, failing check), and a test asserts the cap on a 200-step ledger.

- **Time-budget every hook with a self-measured kill switch** — PERFORMANCE — value 4 — effort S — risk med — category: hook latency
  Why: the pack has bench_hooks.py and sampling ideas, but no runtime guard. The user's complaint that the Stop hook drove a harness session shows hooks run long and unbounded. assumption: some hooks can exceed ~200ms on large repos.
  Done when: a hook that sleeps past its budget is cut off, logs a "slow hook" ledger row, and the turn proceeds. A test with a sleeping stub hook proves it.

- **Coalesce pane redraws to the changed region** — PERFORMANCE — value 4 — effort M — risk med — category: pane render
  Why: the pane now carries a node graph, Gantt rows, a live tree, animation and a dock that "fills exactly" (0.12.0–0.14.0, T-1033). Each added motion element raises the cost of a full repaint. assumption: the pane redraws whole sections per tick.
  Done when: an idle session with all animations on repaints ≤1 row per tick in a frame-count test, and CPU stays under a stated % in a 60 s soak.

- **Index the ledger once into a sidecar of offsets by task and day** — PERFORMANCE — value 3 — effort M — risk low — category: state io
  Why: History, closes-per-day, Today charts, work bar and Agents graph all read the ledger. T-gather already broke on one bad line, so every reader parses raw lines. This goes beyond "tail by offset" by adding per-key seek tables that every consumer shares.
  Done when: Today/History queries on a 100k-line ledger read <5% of the file bytes (measured by a counting reader) and rebuild the sidecar when it is deleted.

- **Memoize the card selector by (file imports hash, deps hash)** — PERFORMANCE — value 3 — effort S — risk low — category: context injection
  Why: T-1036 injects cards by imports and deps across 1,084+ cards, and T-1037 will grow the library. Selection runs at every edit. "Index cards by import" is listed, but a cache of the result per edit is not.
  Done when: a second edit to an unchanged-import file selects cards with zero card-file reads, and a test counts the opens.

- **Rank injected cards by marginal value and drop the ones already known this session** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: the user wants "least token use". With more cards firing per edit, repeats multiply. Per-turn token caps exist as an idea, but not de-duplication across a session or compaction.
  Done when: injecting the same card twice in one session adds 0 bytes the second time, and re-injects once after /compact, as an asserted test.

- **Replace polling in the pane with a ledger-append wake pipe** — PERFORMANCE — value 3 — effort M — risk med — category: pane latency
  Why: the pane shows live state (Activity lanes, live tree). assumption: it polls on a timer, which wastes cycles when quiet and lags when busy.
  Done when: the pane updates within 100 ms of a hook write and uses 0 wakeups per second when idle, measured by a strace/wakeup counter script.

- **Batch worktree creation and prime the dependency dir by hardlink** — PERFORMANCE — value 3 — effort M — risk med — category: fan-out
  Why: parallel builders and resumed worktrees each pay checkout and install cost. A warm pool is listed, but dependency priming (node_modules, venv) is the slow part. assumption: builders re-install per worktree.
  Done when: a fresh worktree is test-ready in under a set time on a fixture with deps, and an install count of 0 is asserted.

- **Wild: Content-addressed proof cache shared across worktrees and clones** — FEATURE — value 4 — effort L — risk med — category: gate speed
  Why: wild. "Skip re-verifying unchanged proofs" covers one resume; this keys passing test runs by tree hash plus command, so a teammate's clone or a sibling builder reuses a green result it never ran. It extends the git-carried hints idea to proofs.
  Done when: two worktrees at the same tree hash run the gate once, and the second reports "proof reused from <id>".

- **Wild: Speculative second builder that races the first on a hard task and loses gracefully** — FEATURE — value 3 — effort L — risk high — category: fleet
  Why: wild. Idle machine capacity is wasted while one builder grinds. A second builder takes a different approach in its own worktree, and the first to pass the gate wins and the other is checkpointed, not deleted. assumption: budget allows it, and the USD cap needs enforcing.
  Done when: on a task flagged `--race`, two worktrees run, exactly one merges, and the loser's branch remains resumable.

- **Wild: Self-profiling Foreman that files its own slow-path tasks** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: wild. The user asked why Foreman hasn't "really improved." Hook and verb timings already exist in bench. This closes the loop: when a verb's p95 regresses against its recorded baseline for three sessions, Foreman opens a task with the flame summary attached.
  Done when: a synthetic 3x slowdown in one verb produces exactly one deduplicated task containing the timing table.

- **Cap resident memory of the pane and long-lived children, and restart them on a leak** — FIX — value 2 — effort S — risk low — category: stability
  Why: the pane and live tree run for whole sessions, and the harness already leaked state across compacts (the env prelude repeated 8x). assumption: long sessions grow memory without a bound.
  Done when: a 2-hour simulated session keeps pane RSS under a stated ceiling, or restarts it once and logs the restart.

- **Skip compaction-time re-exports by hashing the env file block** — FIX — value 3 — effort S — risk low — category: tokens
  Why: the user reported the Bash prelude repeating Foreman's exports 8x. Each repeat is wasted tokens and shell startup. The pack lists detect-and-repair, but the prevention is a check-before-append.
  Done when: running SessionStart ten times leaves exactly one export block in the env file, and a test asserts this.
