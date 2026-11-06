# Brainstorm — lens: Claude Code native integration

- **Fork lanes from the planner's session** — FEATURE — value 5 — effort M — risk med — category: tokens/speed
  Why: assumption: `claude --resume <id> --fork-session` exists and reuses the prompt cache. Each lane now starts cold and re-reads the repo. The user's steers ask for big token savings and for orchestration of orchestrators.
  Done when: a 3-lane L task started via fork shows cache-read tokens above 80% of lane input in the transcripts, and lane input tokens are at least 40% lower than cold-start lanes on the same task.

- **Compile lessons and vetoes into path-scoped native rules** — FEATURE — value 5 — effort M — risk med — category: tokens
  Why: assumption: Claude Code loads `.claude/rules/*.md` files scoped by path globs. Foreman injects all rules at SessionStart. 73 skills plus the injected rules are a fixed per-session cost, and cutting that is the user's stated goal.
  Done when: a lesson tied to `plugin/lib/fmguard*.py` is absent from a session's context until a file matching that path is touched, and the SessionStart injection byte count drops measurably in `bench_hooks.py`.

- **Mirror plan steps into the native task list** — FIX — value 4 — effort S — risk low — category: step tracking
  Why: T-0759 reports work starting on other steps without the step pointer updating. Task-list calls are tool calls, so PostToolUse can see them, and the user sees step state in the host UI. Assumption: a TodoWrite-style tool exists, though it is not in the pack's tool list.
  Done when: starting step N without marking it in progress is flagged in the ledger, and `fm state` and the native list agree on every step in a replayed transcript.

- **Use prompt and agent hook types as cheap judges** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: assumption: hooks can be `type: prompt` or `type: agent`, run by a haiku-class model. The Stop and TaskCompleted gates are pure regex and state checks today. A haiku judge could read the close-out and the diff stat for "claims done without evidence" without spawning a `claude -p` child.
  Done when: a planted close-out claiming "tests pass" with no run result is blocked by the judge hook, and a clean close-out passes in under 3 seconds.

- **Scope every hook with native `if` filters** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: assumption: hook entries accept a permission-rule-style `if` such as `Bash(git *)`. Foreman registers 14 events and hooks are latency-gated. Filtering in the host skips the Python process entirely for Read, Grep and similar calls.
  Done when: `bench_hooks.py` shows zero guard process spawns across 200 Read and Grep calls, and the guard test suite still passes.

- **Subscribe to hook events Foreman ignores** — FEATURE — value 4 — effort M — risk med — category: resilience
  Why: assumption: the host emits StopFailure, InstructionsLoaded, FileChanged, CwdChanged and ConfigChange. T-0751 added usage-limit failover but has no host signal for a turn killed by a rate-limit error. T-0214 (edit-time test sentinel, deferred) needs FileChanged. T-0758 (idle) is partly explained by silent stops.
  Done when: a simulated StopFailure schedules a resume and records a ledger line, and FileChanged on a linked source file queues its mapped tests.

- **Ingest Claude Code's own telemetry locally** — FEATURE — value 4 — effort M — risk low — category: observability/privacy
  Why: assumption: OTel env vars make Claude Code emit per-request token and tool events. Foreman estimates cost from transcripts. A loopback-only collector gives exact tokens per step and per tool, and nothing leaves the machine.
  Done when: `fm cost T-xxxx` prints tokens by plan step from collected events, and the collector refuses non-loopback binds.

- **Run headless children with budget, fallback and schema flags** — FEATURE — value 3 — effort S — risk low — category: DX/reliability
  Why: assumption: `claude -p` accepts `--max-budget-usd`, `--fallback-model`, `--json-schema` and a bare mode that skips plugin and hook discovery. `fm ideas` and second-session children currently run with Foreman's hooks active. Bare mode would also cut their startup.
  Done when: a child given a $0.05 cap stops at the cap and exits with a typed error, and a bare-mode child shows no Foreman hook events in its transcript.

- **Inline live state into skills at invoke time** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: assumption: skills support shell preprocessing and a forked context. Many of the 73 skills open by running `fm state` or `fm task show` and spending a round trip. Preprocessing inlines that output.
  Done when: invoking the resume skill shows task state in its first model turn with zero tool calls, and a heavy skill run in a fork leaves the main context under 2k added tokens.

- **Enforce the return contract with agent-scoped hooks** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: assumption: subagent frontmatter can carry its own hooks and tool allowlists. The six agents rely on prose for their return format. A scoped SubagentStop can reject a reviewer return that lacks findings or a noticed field.
  Done when: a scout return missing the required fields is bounced once with a specific message, and the reviewer's `tools` allowlist excludes Edit and Write.

- **Export Foreman's decisions into Claude Code's native memory** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: a session without Foreman's hooks, such as a plain `claude` run or a headless child, forgets the user's vetoes and decisions. The native memory directory with its `MEMORY.md` index loads everywhere.
  Done when: a standing veto appears as a one-line memory entry, and a bare `claude -p` run in the project quotes it back.

- **Wild: Make Foreman a channel into the running session** — FEATURE — value 4 — effort L — risk med — category: devices
  Why: wild; assumption: Claude Code channels or MCP push can deliver external messages into a live session. The user doesn't want to be handed commands. A phone-side bot could post needs-you cards and receive "yes", "skip" or a new capture, replacing tmux send-keys.
  Done when: a message sent from a second device lands in the idle session within 5 seconds with its sender tagged, and a spoofed sender is rejected.

- **Wild: Shift output style per phase** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild; assumption: the output style can change between turns. Foreman already ships one style. Terse while building, skeptical while verifying, and a short story-shaped close-out would make each phase recognisable.
  Done when: crossing from build to verify flips the style in the ledger, and a snapshot test shows a different close-out shape.

- **Wild: Sync learned playbooks through a private plugin marketplace** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild; assumption: plugin marketplaces can be private git repos. Tasks ship to both GitHub main and JARVIS, so the user works across machines. Bench-proven playbooks published as skills would install everywhere on the next plugin update.
  Done when: a playbook promoted on machine A is invocable on machine B after one plugin update, with no manual copy.
