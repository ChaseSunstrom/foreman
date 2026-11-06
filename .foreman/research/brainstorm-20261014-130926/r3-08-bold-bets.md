# Brainstorm — lens: bold bets

- **Drop the don't-repeat list from child prompts and dedupe afterwards** — PERFORMANCE — value 5 — effort M — risk med — category: tokens
  Why: this pack's "Ideas so far" runs to thousands of lines and is paid for by every child on every lens, and it still yields repeats. Strip it from the pack. Stream each child's output as JSONL, drop ideas that match the catalogue and shipped-feature index by local shingle/MinHash similarity, and abort a child once its last k ideas are all dupes. This combines "prune the pack", "stop early on dupes" and "mechanical pre-grounding" into one pipeline. Assumption: the repeat rate with no list is tolerable. A bench of two rounds can settle that.
  Done when: a round with the list removed uses at least 60% fewer input tokens and its post-dedupe novel-idea count is within 15% of a round run with the list.

- **Close tasks with a provisional done that finalizes or reopens** — FEATURE — value 5 — effort L — risk med — category: verification latency
  Why: finish waits on the whole done-tail (gates, audits, docs checks). Today it either blocks or skips. Split checks into fast and slow. After the fast ones pass, record `done(provisional)` and let the next task start. Slow checks finish in a background lane, and a late failure reopens the task with its evidence attached. Assumption: reopening is acceptable if it is loud and cheap.
  Done when: a task with a 90 s slow check shows done in under 15 s, and an injected late failure moves it back to active with the failing output linked.

- **Route agents by cache affinity, not only by tier** — PERFORMANCE — value 4 — effort M — risk low — category: agents
  Why: round 1 routes model and effort per tier but ignores which already-running agent holds the relevant files and prompt prefix in its cache. Keep a small pool of named agents (reviewer, recon, builder). Record the paths and tree hash each one has read, and send the next brief to the agent with the greatest overlap via SendMessage. Fall back to a fresh spawn when the best overlap is low or the agent's context is nearly full.
  Done when: in a replay of 20 queued tasks, routed sessions show at least 30% fewer re-read tokens than always-fresh spawns, measured from the usage stats.

- **Make child contracts: declare an estimate, enforce twice that, learn the error** — PERFORMANCE — value 4 — effort M — risk low — category: agents
  Why: children carry `--max-budget-usd` as a flat cap. Instead, each child's first line states expected turns, tokens and minutes. The runner kills at 2× and records the estimate error per role. Over time estimates tighten, caps shrink, and an overrun returns a typed partial result. This extends the round-1 caps into data-driven ones.
  Done when: `fm cost` shows per-role estimate error, and a deliberately runaway child is stopped at 2× its own estimate with a partial result saved.

- **Count tokens, not characters, for every budget** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: compact output triggers at 6,000 characters and context blocks are capped in bytes, but cost is tokens. Code and logs tokenize very differently. Calibrate a local estimator (per content class) against the real token counts in the statusline JSON, then use it for every threshold. Assumption: statusline input exposes usage precisely enough to calibrate against.
  Done when: the estimator's error against real counts is under 10% on 30 days of stored outputs, and the compact-output threshold is configured in tokens.

- **Add a stage-pipelined queue: plan N+1 and review N−1 while N builds** — FEATURE — value 4 — effort L — risk high — category: throughput
  Why: stages run serially in the main thread while the user waits. Treat the queue as a CPU pipeline. Planning is read-only, so it is safe to run early. Review runs on a frozen diff. Write conflicts are avoided by footprint overlap checks. This is the one scheduler that connects the existing separate ideas (overlap review, pre-plan, side lanes).
  Done when: a three-task queue with independent footprints finishes in at least 25% less wall-clock than serial, and an overlapping pair correctly falls back to serial.

- **Replay your own round to prove it helped before keeping it** — FEATURE — value 4 — effort M — risk low — category: self-measurement
  Why: round 1 shipped, and "claimed vs measured" is nobody's job. At round close, replay recorded hook payloads and the last N real task shapes through before and after builds, and report hook p50/p95, tokens per injected turn and guard verdict diffs as one table. Combines the receipt, shadow-replay and bench ideas into one close step.
  Done when: closing a round prints a table of at least 5 measured deltas, and a deliberately slowed hook is flagged red.

- **Retire tasks whose premise has expired using a premise ledger** — CLEAN — value 3 — effort S — risk low — category: queue hygiene
  Why: the open list holds many "later from T-0760" clusters and deferred items, such as T-0214 and T-0275, whose reasons may have changed. Each deferral stores a one-line premise (e.g. "needs per-project servers") and a probe command. A weekly sweep re-runs the probes and either wakes the item or closes it.
  Done when: every deferred task has a premise probe, and a task whose probe flips is moved to planned with a note.

- **Make child-spawning prefix-stable and measure the cache hit** — PERFORMANCE — value 4 — effort S — risk low — category: tokens
  Why: lens children share the pack but differ at the end. Put the shared pack first, the lens last, and make no per-run timestamps or random ids appear before the lens. Log cache-read share from usage per child.
  Done when: siblings of one `fm ideas` run report at least 70% cache-read tokens on every child after the first.

- **Wild: Treat the queue as a build graph (`fm make`)** — FEATURE — value 4 — effort L — risk med — category: orchestration
  Why: assumption: wild. Tasks declare inputs (files, decisions, research notes) and outputs. Re-running a round or a rebuilt task skips any target whose inputs hash is unchanged. Failed targets re-run alone, and dependents wait automatically. It generalizes gate caching to whole tasks.
  Done when: running `fm make` twice on an unchanged repo does no model work on the second run and prints "N up to date".

- **Wild: Fork a hunch lane that races the plan on every FIX** — FEATURE — value 3 — effort M — risk med — category: agents
  Why: assumption: wild. For FIX tasks, a cheap-model lane applies the most obvious minimal patch in a worktree while the main thread plans. If the lane's patch passes the repro and the verify, the plan collapses to review-only. Otherwise the lane's failure output seeds the plan for free.
  Done when: on 10 recorded FIX tasks, at least one closes via the hunch lane, and none closes without the verify passing.

- **Wild: Hold a "stranger test" for each round's user-visible surface** — FEATURE — value 3 — effort M — risk low — category: user value
  Why: assumption: wild. A cold child with only the README and `fm help` is asked to do five typical things (capture, plan, resume, ask, page). Every stall, wrong command or confusion is logged as a candidate task. It checks whether round 1's features can be discovered, which the board shows nobody has tested.
  Done when: each round close attaches a stranger-test transcript, and each failed step has a captured task.
