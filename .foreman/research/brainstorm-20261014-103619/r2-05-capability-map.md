# Brainstorm — lens: capability map

- **Make Foreman the session's main agent** — FEATURE — value 5 — effort M — risk med — category: native integration
  Why: assumption: a plugin can ship a default `agent` setting plus a main-thread agent definition. Today Foreman uses an output style, a statusline and per-session hooks, and the pack shows no main-agent definition. A real agent can carry its own tools, model, effort and hooks scoped to it, so sessions that don't use Foreman pay no hook cost.
  Done when: a fresh session in a Foreman project reports the Foreman agent as active, and a session outside one spawns zero Foreman hook processes (checked in `bench_hooks.py`).

- **Filter every hook natively before it spawns Python** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: assumption: hook entries support an `if` permission-rule filter such as `Bash(git *)`, beyond the tool-name matcher. Hooks are latency-gated, and Read, Grep and Glob calls likely start a Python process to learn nothing.
  Done when: `bench_hooks.py` shows 0 spawns for Read and Grep, and the p95 per tool call drops against the current baseline.

- **Rewake the model from slow hooks instead of blocking** — PERFORMANCE — value 4 — effort M — risk med — category: hooks, async
  Why: assumption: async hooks can wake Claude when they exit with a failure code. The edit-time test sentinel (T-0214) and long gates could then run after PostToolUse and surface only a failure, with no tmux keystrokes.
  Done when: an edit that breaks a linked test produces a model-visible failure within N seconds while the edit's own tool call returns without waiting.

- **Mirror plan steps into the host's native task list** — FEATURE — value 4 — effort S — risk low — category: step tracking
  Why: T-0759 reports that Foreman starts other steps without updating the current one, and TaskCompleted is already hooked. Mirroring the plan into the host's checklist lets the user see drift, and lets a hook compare native and fm state.
  Done when: `fm task plan` creates native entries, finishing a step flips the matching native entry, and a mismatch is flagged in `fm doctor`.

- **Bridge native plan mode to `fm` plan review** — FEATURE — value 3 — effort M — risk med — category: plan mode
  Why: assumption: plan mode and its approval step can be answered by a hook. Foreman has its own plan review but the pack shows no tie to the host's plan approval. Users outside bypass mode would get the native approve or edit UI over the fm plan.
  Done when: approving the native plan marks the fm plan reviewed, and an edit made in the native UI appears in the fm plan.

- **Generate path-scoped rules and skills from lessons** — PERFORMANCE — value 4 — effort M — risk low — category: context cost
  Why: assumption: rules and skills accept a `paths:` frontmatter that loads them only when matching files are touched. Foreman ships 73 skills and injects lessons at session start. Native scoping costs zero hook time and zero tokens until a matching file is read.
  Done when: a lesson pinned to `plugin/lib/fmguard*` appears in context only after that path is read, measured by the injected-token count at SessionStart dropping.

- **Wire the remaining hook events and report coverage in `fm doctor`** — FEATURE — value 4 — effort M — risk low — category: hooks
  Why: 14 events are used. Assumption: PostCompact, StopFailure, ConfigChange, InstructionsLoaded, CwdChanged, FileChanged and WorktreeCreate also exist. PostCompact can verify resume landed on the right step. StopFailure can trigger the usage-limit failover. ConfigChange can catch mid-session hook tampering.
  Done when: `fm doctor` lists every documented event as wired or deliberately skipped, and the PostCompact check fails a test where the step pointer is lost.

- **Run semantic done-gate checks as prompt or agent hooks** — FEATURE — value 3 — effort M — risk med — category: done gate
  Why: assumption: hooks can be a prompt or agent type evaluated by a small model with tools. Checks like "does this claim exceed the evidence" currently need Foreman's own subprocess. A native agent hook runs inside the host's budget and timeout handling.
  Done when: a close-out with an unproven claim is blocked by the hook, and one with proven claims passes, in an e2e test.

- **Hard-cap every headless child with schema, budget and turn limits** — SECURITY — value 4 — effort S — risk low — category: headless children
  Why: `fm ideas`, second-session and the other `claude -p` children are tool-less or autonomous. Assumption: `--json-schema`, `--max-budget-usd` and `--max-turns` exist. They give structured output with no parser drift and a bounded cost per child.
  Done when: a child that loops stops at its cap with a typed error, and malformed output fails schema validation rather than reaching a parser.

- **Precompute skill state with dynamic context injection** — PERFORMANCE — value 3 — effort S — risk low — category: skills
  Why: assumption: skills can embed shell output that is rendered before the model sees them. Skills such as resume and close-out likely spend a tool call first on `fm task show`.
  Done when: invoking the resume skill shows the current step in its first model turn with 0 preceding tool calls.

- **Answer MCP elicitation requests from recorded decisions** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: assumption: an Elicitation hook can answer MCP servers' mid-call questions. Foreman runs unattended and never wants to hand the user commands, but such a prompt stalls a night run. Foreman can answer from decisions and vetoes, or defer to the digest.
  Done when: a fixture MCP server's elicitation is answered from a stored decision, and an unknown one is queued as an ask with a default.

- **Wild: Compile vetoes and decisions into the host's auto-mode classifier rules** — SECURITY — value 3 — effort M — risk med — category: second guard
  Why: wild. Assumption: auto mode takes prose allow and deny rules. Foreman's guard is deterministic and bypass-mode. A native classifier fed the user's own vetoes is an independent second judge, and disagreement between the two becomes a guard-bug signal.
  Done when: a command the guard allows but a veto forbids raises a logged disagreement in a replay test.

- **Wild: Park a headless child on a deferred approval and resume it from the phone** — FEATURE — value 3 — effort M — risk med — category: devices, asks
  Why: wild. Assumption: a hook can defer a permission decision so a `-p` run pauses and resumes later. Night children hit a decision, park, push one line to the phone, and resume exactly where they stopped after the answer.
  Done when: a scripted child pauses on a deferred ask, and answering it continues the same session with its context intact.

- **Wild: Map lanes onto native agent teams with a shared task list** — FEATURE — value 3 — effort L — risk high — category: fleet
  Why: wild. Assumption: the experimental agent-teams feature gives teammates a shared task list and a mailbox. If the fm queue is exposed as that list, teammates claim work natively and idle ones are woken by the host, which addresses T-0758 without Foreman's own wake machinery.
  Done when: a two-teammate run drains three queued fm tasks with no `send-keys` calls and the ledger shows each claimed once.
