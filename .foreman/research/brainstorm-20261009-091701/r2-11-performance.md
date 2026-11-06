# Brainstorm — lens: performance

- **Profile where a task's wall-clock went** (`fm profile T-id`) — FEATURE — value 5 — effort M — risk low — category: performance
  Why: the pack has `fm cost` (tokens) and `fm friction`, but nothing splits elapsed time. The "slow-gate" signal (T-0424) and the repeated idle-session complaints suggest time is invisible. assumption: ledger events carry enough timestamps to attribute time.
  Done when: `fm profile` on a finished task prints a breakdown of model time, tool time, each gate, waiting on the user, and idle, and the parts sum to within 5% of the task's elapsed time.

- **Park a blocked task and keep going** — FEATURE — value 5 — effort M — risk med — category: throughput
  Why: the user asked "long-lived jobs and an empty queue never leave a session idle", and JARVIS idled with 20+ queued. An `fm ask` or a `?` item still stalls the one active task. assumption: a blocked task can be suspended without losing its resume point.
  Done when: with a pending ask on T-A, the drive focuses the next unblocked task, and answering the ask puts T-A back at its exact step. A test checks both.

- **Order gates by failure odds per second** — PERFORMANCE — value 4 — effort S — risk low — category: gates
  Why: `fm check` runs gates together, and sharding by duration is already proposed. Ordering by P(fail)/cost so cheap, likely failures stop the run first is not. The history is in the ledger. assumption: per-gate pass/fail history is recorded.
  Done when: on replayed history, mean time-to-first-failure on failing runs drops at least 30% against the fixed order, with identical verdicts.

- **Share one prompt-cache prefix across reviewer fan-out** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: `fm audit` freezes the diff and writes one brief per reviewer, but cache-stable context so far covers only the injected session context. Lens reviewers reading the same frozen diff can share a byte-identical prefix. assumption: the reviewers run on a provider with prompt caching.
  Done when: the cache-read token share on a 5-lens audit is above 70%, as shown by `fm cost`, and the briefs differ only after the shared prefix.

- **Serve repeat reads as ranges or deltas** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: `fm outline` and "read a range, not all" show that whole-file re-reads are a known waste. A PreToolUse hook could answer a second read of an unchanged file with "unchanged since your read at step 3" and a changed one with the diff. assumption: the hook can see the earlier reads in the session.
  Done when: in a replayed session with N repeated reads, the tokens returned fall by at least 40%, and no read of a changed file returns stale content.

- **Compact at a step boundary, not when the window fills** — FEATURE — value 4 — effort M — risk med — category: context
  Why: Foreman already resumes at the exact step after `/compact` and has a PreCompact checkpoint, but the timing is chosen by Claude Code. Compacting after verified evidence, with a fresh checkpoint, loses less. assumption: Foreman can suggest compaction through the drive or the UI.
  Done when: the drive prompts a compact only right after a step's evidence is recorded and context is above a threshold, and `resume` afterwards reproduces the same step in a test.

- **Make lane creation instant with copy-on-write dependency trees** — PERFORMANCE — value 3 — effort M — risk med — category: lanes
  Why: JARVIS builders symlinked `node_modules` to main and hit guard refusals, and tool caches had to be cleaned by hand before `lane rm`. A reflink clone of the dependency directories avoids both the install and the symlink hazard. assumption: the filesystem supports reflinks, with a plain-copy fallback.
  Done when: `fm lane new` on a project with a large `node_modules` takes under 2 s, the lane's dependencies are independent of main's, and `lane rm` removes them cleanly.

- **Record project performance as evidence, and block on regressions** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: the user asked that Foreman "checks the product the way its user uses it". The product's speed is part of that, but today only Foreman's own latency is gated. `fm smoke` already drives a headless browser, so it could also record load time and bundle size per task. assumption: the project declares a few metrics.
  Done when: a task that slows a declared metric by more than the set threshold cannot be marked done without an explicit, recorded waiver, and the metric history shows in `fm digest`.

- **Fit a task to a time budget** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: "give it 30 minutes" is a natural request the system can't express. This extends the proposed predictive pace and cost estimates. assumption: estimates exist for steps, which `fm profile` would supply.
  Done when: `fm task new --budget 30m` produces a plan that defers lower-priority steps, labels them as dropped, and the final report lists what was cut.

- **Degrade gracefully near the usage limit instead of blocking** — FEATURE — value 4 — effort M — risk low — category: budget
  Why: the user steered "budget/pace limits shouldn't block anything until 75% usage", and T-0320 made subagents wait only when usage runs ahead of pace. The step after 75% is cheaper modes rather than a hard wait: fewer lenses, smaller models for scouts, deferred night work. assumption: usage is readable live.
  Done when: simulated usage at 80% switches to the reduced mode and logs it, usage at 70% changes nothing, and nothing is refused outright.

- **Wild: Prepare the task while the user is still typing** — FEATURE — value 3 — effort L — risk med — category: latency
  Why: wild. The desktop app and the UI mod see the prompt box, so they could pre-run classification, `fm recall`, `fm impact` and `fm why` on the draft and hand the results to UserPromptSubmit already computed. assumption: a draft-text channel from the UI to Foreman is possible.
  Done when: submitting a drafted request reaches "plan shown" at least 2 s faster than a cold start, and the answer is identical to the cold path.

- **Wild: Schedule heavy work around the user's presence** — FEATURE — value 3 — effort M — risk low — category: scheduling
  Why: wild. The desktop tray, terminal activity and the existing `fm night` could infer when the user is away, then run reviewers and benchmarks then, and hold non-urgent asks until they return. assumption: presence can be sensed locally with no data leaving the machine.
  Done when: with the user idle for 20 minutes, queued non-urgent heavy jobs start. On return, the held asks arrive as one batch.

- **Wild: Keep a hot spare of the main thread's next step** — FEATURE — value 3 — effort L — risk high — category: speculation
  Why: wild. While gates run on task N, a speculative lane drafts the plan and first edits for N+1, discarding them if the gates fail. It is proposed in the pack only as pre-planning at idle, not as cancelable code. assumption: the next task is independent of N's files.
  Done when: when N passes, N+1 starts with its draft already in a lane, and a failed N leaves no stray branch or edits behind.

- **Wild: Hold a latency "race day" between plugin versions** — PERFORMANCE — value 2 — effort S — risk low — category: benchmarking
  Why: wild. `fm bench` replays tasks and `bench_hooks.py` gates hook latency. A leaderboard-style view would rank every release on time and tokens per solved case and show the trend in the UI. assumption: bench results are stored per version.
  Done when: the UI shows a per-release chart of time and tokens per case, and a release that is slower than the last by more than the set margin is flagged.
