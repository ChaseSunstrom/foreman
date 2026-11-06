# Brainstorm — lens: capability map

- **Run unprovable commands in the Claude Code sandbox instead of refusing them** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: three of the dropped items are guard refusals it couldn't prove safe: heredocs writing to computed paths, `$_` args, and pipe-fed scripts. Each ends in a refusal or a "by design" shrug. Assumption: the host's native sandbox (filesystem-write-scoped) can wrap a Bash call from a PreToolUse rewrite.
  Done when: a quoted heredoc whose Python writes to a runtime-computed path runs inside the sandbox with writes limited to the task directory, a test shows a write into the core tree fails, and the command isn't refused.

- **Serve hooks from one resident daemon** — PERFORMANCE — value 5 — effort L — risk med — category: latency
  Why: 14 hook events each spawn a Python process, and `bench_hooks.py` exists because latency is the gate. An earlier idea was dropped for adding a hook process per Read. Assumption: hooks can be thin shims, or http-type hooks, that talk to a unix-socket server.
  Done when: `bench_hooks.py --runs 20` shows p50 for PreToolUse at least 3x lower than the spawn-per-call baseline, and the daemon restarts itself after being killed mid-session.

- **Keep injected context byte-stable for the prompt cache** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: the user keeps pushing for token savings and the team already mines transcripts. SessionStart and UserPromptSubmit injections that carry timestamps, counters or reordered lists break the cached prefix. Assumption: cache read/creation counts are in the transcripts.
  Done when: `fm doctor` reports cache-read ratio per session from transcripts, and a replay of two consecutive prompts shows the injected block is byte-identical when nothing changed.

- **Generate path-scoped rules from lessons** — FEATURE — value 4 — effort M — risk low — category: tokens
  Why: lessons are recalled globally, and T-0365 only covers a generated CLAUDE.md section. Native `.claude/rules` with path globs load only when matching files are touched. Assumption: path-scoped rules are supported in the user's CC version.
  Done when: a lesson tied to `plugin/lib/fmguard*.py` lands in a rules file scoped to that glob, is absent from a session that never touches it, and `fm doctor` flags stale rules.

- **Expose Foreman state as an MCP server** — FEATURE — value 4 — effort M — risk med — category: integration
  Why: queue, plan, evidence and lessons live behind the `fm` CLI and hooks, so IDE sessions, subagents and other tools can't query them structurally. Assumption: a stdio MCP server declared in the plugin starts without extra user setup.
  Done when: a Claude Code session without Foreman hooks can call `foreman.task_current` and `foreman.queue` and gets the same data as `fm task show`. Writes need a guard-checked tool.

- **Steer running subagents with SendMessage** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: Agent calls are background by default, but Foreman only waits for them or kills them, so a drifting builder wastes its whole run. Assumption: SendMessage can address a live subagent from the parent.
  Done when: a PostToolUse check that sees a builder edit outside its step scope sends it a correction, and a test shows the builder's next edit lands in scope without a restart.

- **Budget the skill listing** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: there are 73 skills, and every session pays for their names and descriptions. The ideas so far only run `/skill-doctor` for correctness, not for cost. Assumption: descriptions are what costs tokens.
  Done when: `fm doctor` prints total description tokens per skill and fails above a set budget. After trimming, the listing is at least 30% smaller and the skill-trigger evals still pass.

- **Map each plan step to a rewind point** — FEATURE — value 3 — effort M — risk med — category: recovery
  Why: `task revert` exists, and the user reports steps changing without the step being updated. A native checkpoint at each step boundary would let "undo step 3" restore both files and conversation. Assumption: checkpoints can be referenced from a hook or from `fm`.
  Done when: `fm task rewind <step>` restores the files to that step's boundary, resets the step pointer, and keeps later evidence recorded as discarded.

- **Review on a different model than the builder** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: reviewers are sonnet and the builder inherits, so reviewer and builder errors are correlated, and the forge-a-pass work shows the team cares about fooling its own gate. Assumption: per-call `model` is honored.
  Done when: close-out picks a reviewer model different from the builder's, the choice is recorded, and the eval inbox shows reviewer precision per pairing.

- **Wild: fork the session at a plan step and race approaches** — FEATURE — value 4 — effort L — risk high — category: exploration
  Why: assumption: session resume with fork is available headlessly. At an ambiguous step, fork N children with different approaches, each in a worktree. Verification evidence picks the winner and the rest are discarded. This goes beyond the existing "competing attempts" idea because it reuses the full conversation context.
  Done when: one task runs two forked attempts, both end with recorded evidence, and the loser's worktree is removed.

- **Wild: pre-run read-only recon for the next queued task while the user is away** — PERFORMANCE — value 3 — effort M — risk low — category: speculation
  Why: `fm night` pre-plans only the first L task. Idle time is what the user complained about (T-0758). Assumption: recon outputs are cacheable against a commit hash.
  Done when: starting the next task finds a recon digest for the current HEAD, and a test shows it's discarded when HEAD moves.

- **Wild: ghost user answers routine `fm ask` prompts from past decisions** — FEATURE — value 4 — effort L — risk high — category: autonomy
  Why: `fm decide` already records past choices, and the user never wants to be handed commands or left waiting. A haiku-class agent answers only prompts that match a recorded decision, and escalates everything else. Assumption: past decisions are queryable.
  Done when: a repeated prompt is answered with a citation to the original decision, a novel prompt always reaches the user, and a destructive ask is never auto-answered.
