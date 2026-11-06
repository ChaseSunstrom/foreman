# Brainstorm — lens: user value

- **Audit Foreman-tracked repos for committed credentials and Claude config secrets** — SECURITY — value 5 — effort M — risk low — category: credentials
  Why: the user asked for "credential finding/auditing in repositories/claude stuff" and better git tracking. Prior ideas only cover leak mining in history; nothing covers working-tree files, `.claude/` settings, MCP configs, or `.env` files that sit next to Foreman state.
  Done when: `fm audit secrets` on a fixture repo with a planted key in `.claude/settings.json` and a `.env` reports both with file:line, redacts the values in output, and exits non-zero.

- **Gitignore and untrack Foreman state automatically per repo** — FEATURE — value 4 — effort S — risk low — category: git tracking
  Why: the user asked for "better tracking of foreman stuff in git repositories". Assumption: state or worktree lane directories can show up as untracked or get committed by accident.
  Done when: after `fm init` in a fresh repo, `git status` shows no Foreman files, and a test fails if a lane worktree path or state file is staged by `fm task finish`.

- **Show a "restart-proof" resume check after --continue** — FIX — value 4 — effort M — risk med — category: drive
  Why: the user complained "you weren't reprompted when the session just continued", and a reload-resume race was dropped as unsolved. Both are the same failure: a silent stall that nobody notices.
  Done when: a test simulates the session resuming, a background completion landing during a mod reload, and a double reload. The drive restarts exactly once in each case, and a stall longer than N seconds with open work writes a visible ledger event.

- **Measure and report agent-side latency per turn** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: the user said it feels slow for the agents using Foreman, not for Foreman's own hooks (p95 about 30 ms). Assumption: the cost is extra round trips such as guard rewrites, separate planning calls and audit waits.
  Done when: `fm perf` lists, for the last 10 tasks, tool calls, guard-block rewrites and wall time split by Foreman overhead vs. real work, and names the top 3 sources.

- **Make parallel lanes budget-aware before launch** — FEATURE — value 4 — effort M — risk med — category: parallel
  Why: the user asked that parallel work not cause "context/speed/quality/usage issues". Assumption: lanes share one usage budget and each one pays the context-loading cost of the rules and the brief.
  Done when: `fm run --parallel 3` prints an estimated token cost and overlap risk before starting, refuses or reduces lanes when overlap or budget is exceeded, and a test covers the reduction.

- **Fail the build on any unpanelled row in the mod** — CLEAN — value 4 — effort M — risk low — category: ui
  Why: the user repeated four times that some output is not in panels, is duplicated, or has mismatched sections. Each round fixed single cases by hand.
  Done when: a mod test renders every row kind (reply, tool, edit, diff, dashboard, buttons, prompt echo) and fails if any appears outside a bordered panel or if a dashboard section appears twice.

- **Turn each user complaint into a permanent regression test automatically** — FEATURE — value 5 — effort M — risk low — category: self-improvement
  Why: the user's recurring complaints (duplicate dashboard, unpanelled messages, guard false positives) keep resurfacing in new forms, and they want recursive self-improvement.
  Done when: `fm friction` links a complaint to a test or a guard corpus entry, and a task cannot close a user-reported FIX without a linked failing-then-passing test.

- **Wild: Add a "show me" mode that renders the last turn as an image** — FEATURE — value 3 — effort L — risk low — category: ui
  Why: wild. The snapshot tool already exists through its own tmux. Foreman could capture what the user sees and attach it to the task as visual evidence, so "looks wrong" is checked on the actual frame.
  Done when: closing a UI task attaches a terminal snapshot to the evidence, and the audit lens can read it.

- **Wild: Run a "guard red team" subagent pair each night** — SECURITY — value 4 — effort L — risk med — category: guard
  Why: wild. Two real bypasses were found only while grounding false positives. An attacker subagent could mutate the command corpus while a defender subagent proposes narrow fixes.
  Done when: a nightly run produces either zero new bypasses or filed tasks with failing corpus tests, and it uses only Haiku.

- **Wild: Let Foreman answer "why is this slow?" with a one-shot trace** — FEATURE — value 3 — effort M — risk low — category: speed
  Why: wild. The user said "it feels slow, I don't know". A single command turns that feeling into a waterfall of where the time went in the last hour.
  Done when: `fm why-slow` outputs a ranked list of the three largest time sinks with the command or hook responsible.
