# Brainstorm — lens: approaches

- **Bake off each native feature against Foreman's own path before adopting it** — FEATURE — value 5 — effort M — risk low — category: adoption
  Why: the Delta Reads drop shows native overlap can quietly make a custom path pointless (CC already stubs repeat reads). The unused list has about a dozen candidates and no way to decide which are worth wiring. Approach: run the old and native paths over replayed tasks, score tokens, latency and idle minutes, and adopt only winners. Trade-off: it needs a bench harness, but it stops integration for its own sake.
  Done when: `fm adopt bench wake` prints a table of send-keys against SendMessage on 20 replayed tasks, and a candidate that doesn't win is recorded as rejected.

- **Mirror the plan into the native todo list and derive the step pointer from it** — FIX — value 5 — effort M — risk med — category: step tracking
  Why: T-0759 reports work starting on other steps without the step being updated. The model already updates native todos every turn, so a PostToolUse hook on TodoWrite can move the pointer instead of relying on Foreman's own `fm task step` calls. The user also sees the plan in CC's own UI. Trade-off: two sources of truth, so the ledger stays authoritative and flags a mismatch.
  Done when: marking a todo in_progress moves `fm task` to that step, and a test that does work with no todo change gets a warning.

- **Compile static guard rules into native permission deny rules and hook `if` prefilters** — PERFORMANCE — value 4 — effort M — risk med — category: hook latency
  Why: the hooks are latency-gated (bench_hooks.py) and the guard spawns Python on every Bash call. Obviously-safe and obviously-banned patterns can be settled by CC itself, so the hook only sees the ambiguous middle. Assumption: deny rules and the hook `if` field both apply in bypass mode. Trade-off: rules exist in two places, so generate them from one table to avoid drift.
  Done when: bench_hooks shows a measurable drop in p50 hook spawns per 100 Bash calls, and a differential test shows no verdict changes.

- **Turn `fm ask` into a native AskUserQuestion with a pre-selected default and deadline** — FEATURE — value 4 — effort S — risk low — category: asks
  Why: the user "never wants to be handed commands" and asks are currently free text. A structured multiple-choice with Foreman's recommended option first costs one keystroke and is parseable. Assumption: the tool is available to the main thread. Trade-off: it only works while someone is at the terminal, so keep the push/Artifact route for away time.
  Done when: a blocking ask renders as options with the default marked, and the chosen option lands in `fm ask` state with no parsing of prose.

- **Generate path-scoped `.claude/rules/*.md` from lessons and vetoes** — PERFORMANCE — value 4 — effort M — risk low — category: context
  Why: lessons are injected by hooks at session start, which costs context and a process per session. CC loads path-scoped rules natively, only when matching files are touched, with no hook latency. Assumption: this CC build supports `paths:` frontmatter in rules. Trade-off: rules are static files, so regenerate them on lesson change and delete stale ones.
  Done when: touching `plugin/lib/fmbudget.py` loads only its lessons, with no hook spawn and a smaller injected-context byte count in the session start.

- **Run Foreman's own review and recon skills as forked, model-pinned skills** — CLEAN — value 3 — effort M — risk low — category: delegation
  Why: T-0755 asks about cheaper models. The skill frontmatter fields (model, effort, a forked-subagent context) are unused, and 73 skills are mostly run on the main model. Assumption: those fields exist in this CC. Trade-off: it changes the output path, so a forked skill returns a summary and not an inline transcript.
  Done when: five chosen skills carry model/effort frontmatter and a smoke run shows them executing on haiku or sonnet while the main thread stays on its own model.

- **Scope hooks inside skill and agent frontmatter so the discipline loads only where needed** — PERFORMANCE — value 3 — effort M — risk med — category: hooks
  Why: the 14 hook events fire for every session and every subagent, including scouts that only read. Assumption: component-scoped hooks are supported. Trade-off: a lane that skips the guard is a hole, so keep the guard global and scope only the bookkeeping hooks.
  Done when: a scout run spawns no bookkeeping hooks, and the guard still blocks a dangerous command in the same run.

- **Dual-run a native mechanism in shadow before cutting over** — FEATURE — value 3 — effort S — risk low — category: migration
  Why: wake-by-keystroke is fragile, and the native route (SendMessage/ListAgents) is unproven here. Send both, log whether each landed, and flip the default only after N matching sessions. Trade-off: some duplicate wakes during the trial, so dedupe by message id.
  Done when: `fm doctor` reports shadow agreement (for example 48/50) per migrated mechanism and a one-line cutover command.

- **Use the statusline's input JSON as the pace and cost sensor** — PERFORMANCE — value 3 — effort S — risk low — category: telemetry
  Why: the statusline already runs on every refresh and receives context, cost and session data. Writing that to a small state file gives the budget and pace code live numbers without rescanning transcripts. Assumption: the fields are stable. Trade-off: it only updates while the statusline renders.
  Done when: `fm pace` reads the freshest sample and matches the transcript-derived value within 2%, with no transcript read.

- **Add `fm can "<capability>"` that probes the live tool list and answers with evidence (wild)** — FEATURE — value 3 — effort S — risk low — category: self-knowledge
  Why: T-0755 ("can foreman spawn agents of lower models?") is a question about CC itself, and Foreman's knowledge goes stale. The command checks the session's tool schema and the installed CC help and returns yes/no with the quoted source. Trade-off: it answers only what the schema shows.
  Done when: `fm can "spawn haiku agents"` returns the Agent `model` parameter quoted from the live schema.

- **Mint a slash command per queued task and milestone (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: the user steers by typing short phrases. Generated `/t-0757` and `/next` commands that autocomplete with the task title turn queue steering into two keystrokes. Trade-off: command clutter, so expire them on task close.
  Done when: `/t-0757` autocompletes in a fresh session and prints that task's brief and current step.

- **Replace the plan-review prompt with native plan mode, with Foreman's pivot table as the plan body (wild)** — FEATURE — value 3 — effort M — risk med — category: plan review
  Why: T-0730 pre-plans tasks without a plan review, and users already know the native approve/reject UI. Foreman would enter plan mode, post the plan, and treat approval as the plan-reviewed mark. Assumption: ExitPlanMode can be driven from a hook-injected flow. Trade-off: bypass mode may skip the dialog, so it needs a fallback.
  Done when: an M task shows the native approval, and approval writes the same plan-reviewed record as today.

- **Put a "what changed since you last looked" diff in the SessionStart greeting from a native-feature manifest (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: the user asked for integration with new CC features, and new tools appear silently. A manifest of tool names seen at the last session, diffed at start, can say "two new tools since Tuesday: X, Y; one fits T-0757". Trade-off: one line of context per session, only when the diff is non-empty.
  Done when: a session started with a faked new tool name prints one adoption line, and a session with no change prints nothing.
