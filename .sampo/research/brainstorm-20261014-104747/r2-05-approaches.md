# Brainstorm — lens: approaches

- **Measure idle gaps before fixing them** — FIX — value 4 — effort S — risk low — category: observability
  Why: T-0758 says "make sure it doesn't sit idle", yet every earlier idea assumes a cause (tmux nudges, Monitor, ScheduleWakeup). Transcripts already have timestamps, so classify each gap by cause first (waiting on a background agent, a hook deny loop, the model asking, queue empty) and fix only the top cause.
  Done when: `fm idle` prints a per-cause table of gaps over 60s for the last 30 days, and the top cause is named in the task that fixes it.

- **Run one persistent hook daemon behind thin shims** — PERFORMANCE — value 4 — effort L — risk med — category: hooks
  Why: 14 hook events fire on every turn and are gated by `bench_hooks.py`. Each call pays Python startup plus imports. A warm daemon on a unix socket keeps the state and indexes loaded. Assumption: startup is a large share of current hook latency.
  Done when: `bench_hooks.py --runs 20` p95 for PreToolUse drops at least 40% against the current baseline, and a killed daemon falls back to the cold path with identical decisions.

- **Mirror the guard's hardest blocks into native deny rules** — SECURITY — value 4 — effort M — risk med — category: defense in depth
  Why: Foreman runs in bypass mode, so the guard hook is the only barrier. If the hook crashes or times out, nothing stops `rm -rf ~` or a script piped to bash. Generating Claude Code permission deny rules from the guard's core rules gives a second layer. Assumption: deny rules still apply in bypass mode.
  Done when: with the guard hook disabled, `echo 'rm -rf ~' | bash` is refused by Claude Code's own permission layer, and `fm doctor` flags any drift between the two rule sets.

- **Contain what the guard can't prove instead of refusing it** — FEATURE — value 4 — effort M — risk high — category: guard
  Why: Several dropped items (quoted heredoc writing runtime-computed paths, `python -c` importing fmcli) were refused because the guard can't see the target. T-0275 is also open. Running those commands under Claude Code's bash sandbox, with writes limited to the task worktree, turns "refuse" into "run safely". Assumption: the sandbox is available in this environment.
  Done when: a heredoc that writes to a computed path runs, can write only inside the worktree, and a write attempt outside it fails with the sandbox error recorded as evidence.

- **Keep injected context byte-stable to preserve prompt-cache hits** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: SessionStart and UserPromptSubmit inject Foreman context on every prompt. Anything that changes mid-prefix (timestamps, step counters, queue order) invalidates the cache from that point on. Assumption: the injected block currently varies between turns.
  Done when: a test diffs consecutive injections and fails if the stable prefix changes. Volatile fields move to a tail section, and a measured cache-read share rises on a replayed session.

- **Shadow-run a native replacement before retiring the Foreman mechanism** — CLEAN — value 4 — effort M — risk low — category: migration
  Why: Many earlier ideas replace tmux send-keys, `fm notify`, the lane plumbing and the findings format with native tools. None says how to prove parity. Run both paths for a week, log disagreements, and delete the old path only when disagreements are zero.
  Done when: `fm parity` reports per mechanism the count of old and new triggers and the mismatches, and retiring a mechanism requires a zero-mismatch report.

- **Learn the model ladder by shadow-running cheap models on finished tasks** — FEATURE — value 5 — effort L — risk med — category: model routing
  Why: T-0755 asks for lower-model agents. Routing rules guessed up front are weak. Re-run a sample of S-tier tasks on haiku and sonnet in worktrees, score them by verify outcome and cost, and build a per-task-class table. Eval cases and bench holdout from 1.2.27 already exist to score with.
  Done when: `fm ladder` shows pass rate and cost per (task class, model, effort), and the router reads it and reports its choice per step.

- **Set effort in subagent frontmatter and measure it** — FEATURE — value 3 — effort S — risk low — category: subagents
  Why: Subagent frontmatter can set effort, but none of the 6 agents does. Scout and recon are read-only and plausibly need `low`, while reviewer and debugger may need more. A bench compares before and after.
  Done when: each agent file declares an effort, and a before/after table of tokens and review catch rate on the eval set shows no catch-rate drop.

- **Keep one warm reviewer and message it each new diff** — PERFORMANCE — value 3 — effort M — risk med — category: orchestration
  Why: Every close-out spawns a fresh reviewer that re-reads context. SendMessage to a live reviewer would reuse its loaded context across a task's steps. Assumption: SendMessage can continue a finished subagent.
  Done when: a three-step task's review tokens fall at least 30% against fresh spawns, and findings are identical on a fixture with a seeded bug.

- **Expose Foreman state as an MCP server** — FEATURE — value 3 — effort M — risk low — category: integration
  Why: Claude reads queue, step and lessons through Bash calls that each trigger PreToolUse. Typed MCP tools (`foreman.step`, `foreman.recall`, `foreman.capture`) skip the shell and the guard parse. They also work from other clients such as Codex and Gemini (T-0335).
  Done when: Claude Code lists the MCP tools, `foreman.capture` creates a task, and the Bash call count per task drops on a replayed session.

- **Wild: Hedge S tasks with two models and keep the first verified pass** — FEATURE — value 3 — effort L — risk med — category: speed
  Why: assumption: the user values speed and cheap tokens (their steers). Launch haiku and sonnet builders in sibling worktrees. The first one to pass the task's gates wins and the other is cancelled. This uses idle parallel capacity to cut wall-clock time and often cost.
  Done when: a task flagged `--hedge` merges only the winning worktree, and the ledger shows both lanes' costs and the loser's cancel time.

- **Wild: Compile Foreman's own CHANGELOG into a "what changed in CC" diff of the tool list** — FEATURE — value 3 — effort M — risk low — category: self-tuning
  Why: assumption: new CC tools keep appearing, as this pack's "unused" list shows. Snapshot the tool and hook inventory each session, and when it differs from the last snapshot, auto-capture a task per new capability with a one-line integration sketch.
  Done when: adding a fake tool to a fixture inventory produces a captured task naming it.

- **Wild: Run `fm night` as a dream-mode of speculative prep, not just execution** — FEATURE — value 3 — effort M — risk low — category: autonomy
  Why: `fm night` pre-plans only the first queued L task (T-0730). With haiku-tier agents, also draft plans for every captured task, pre-read the likely files, and prepare briefs. The next day starts at step one without a planning wait.
  Done when: after a night run, every captured task has a draft plan marked "unreviewed", and starting one skips plan generation.
