# Brainstorm — lens: unspoken needs

- **Never Idle: wake itself with ScheduleWakeup and Monitor** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: T-0758 "make sure it doesnt sit idle like it is"; today idle sessions are woken by tmux send-keys, which is fragile. ScheduleWakeup, Monitor and CronCreate are unused (0 references).
  Done when: a session with queued tasks and a stalled Stop is resumed by a native wakeup (no send-keys) within N seconds, shown by a test that kills the tmux path.

- **Step Truth: bind the active step to what the tool calls touch** — FIX — value 5 — effort M — risk med — category: discipline
  Why: T-0759 "it will start working on different steps without updating the step". PostToolUse already sees the files and commands; the user wants the step marker kept honest without asking.
  Done when: editing files linked to step 3 while step 2 is marked active auto-advances or flags the step, and a test replays a transcript showing the marker following the work.

- **Model Ladder: pick the cheapest model and effort per step** — FEATURE — value 5 — effort M — risk low — category: cost
  Why: T-0755 "spawn agents of lower models? haiku/sonnet". The Agent tool takes per-call `model` and `effort`, but only S-tier lanes pass "sonnet" and the builder inherits. The user keeps asking for tokens saved.
  Done when: each plan step carries a model and effort tier derived from size and past catch rates, and `fm task show` lists the tier actually used per step.

- **Findings In the Host UI: emit reviewer output through ReportFindings** — FEATURE — value 4 — effort S — risk low — category: review
  Why: the reviewer subagent returns prose that Foreman parses itself; ReportFindings is typed and rendered by the host (0 references). The deferred T-0034 wants a structured findings file.
  Done when: a close-out review produces ReportFindings entries that `fm task finish` reads back as the review evidence.

- **Phone Ping: send PushNotification when the user is truly needed** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: fm notify only runs a user shell command, and the user "never wants to be handed commands". Blocked-on-you, done and failed-gate events are exactly when to push. Assumption: PushNotification works in bypass mode.
  Done when: a blocked task triggers one push (rate-limited, deduplicated), and a test asserts silence for routine progress.

- **Review Tiers: map task size to built-in /code-review levels** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: the built-in /code-review has low…max levels and /security-review, /simplify exist, and Foreman runs its own reviewer. Pairing the level to the task's tier and risk class avoids double review cost.
  Done when: S tasks use low, tasks touching guard or hooks use max plus /security-review, and the choice is recorded in the task.

- **Worktree-Native Main Thread: use EnterWorktree for risky tasks** — FEATURE — value 4 — effort M — risk med — category: safety
  Why: worktrees are used only for lanes through Agent isolation. The main thread can move into a worktree via EnterWorktree, which would make "task revert with dependents" (T-0751) a cheap worktree discard.
  Done when: an L-tier FIX runs in a worktree and ExitWorktree merges only after gates pass, with a test of discarding on failure.

- **LSP Impact Gate: check references before an edit closes** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: LSP (definitions/references) is unused, while Foreman uses fm map test links that are text-based. A rename or signature change should list unupdated callers as evidence.
  Done when: changing a function signature without updating a caller blocks the step and names the caller file:line.

- **Cloud Routines Night Shift: move fm night to /schedule** — FEATURE — value 4 — effort L — risk high — category: scheduling
  Why: fm night pre-plans locally, which needs the machine on. RemoteTrigger and Agent isolation "remote" would let the queue run when the laptop is shut. Assumption: the repo is reachable from the cloud and the user opts in per repo.
  Done when: an opt-in routine runs the queue's S tasks in the cloud and posts a result file that the next local session ingests.

- **Artifact Cockpit: publish the live plan as a private claude.ai page (wild)** — FEATURE — value 4 — effort L — risk med — category: UI
  Why: Frontier 11 wants a cockpit; Artifact with ArtifactData and ArtifactComments gives a phone-viewable page where a comment becomes a captured request. Never used so far. Assumption: Artifact content is private, redacted and opt-in (it leaves the machine).
  Done when: a redacted plan/queue page updates after each task and a comment on it appears as a captured T-item.

- **Cross-Machine Foreman: use SendMessage and ListAgents between sessions (wild)** — FEATURE — value 3 — effort L — risk med — category: orchestration
  Why: fm bus talks only to local tmux panes; SendMessage reaches other local, cloud and Remote Control sessions, so a laptop and a server could share one queue and a handoff.
  Done when: a task captured on one machine is claimed by an idle session on another and the claim is visible in `fm bus`.

- **Hook Latency Budget Visible to the User: surface bench results in the band** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: hooks are latency-gated by bench_hooks.py, but the user only sees failures at gate time. Showing the live p95 in the statusline would catch a slow hook early.
  Done when: the statusline shows hook p95 and turns amber past budget, verified by a fixture with an injected slow hook.

- **Self-Tuning to New CC Releases: detect new tools and hooks and draft integrations (wild)** — FEATURE — value 4 — effort M — risk low — category: maintenance
  Why: this very request ("integrate better with new CC features") will recur with every release, and the unused-features list was found by hand grep. Assumption: the tool list and hook events can be read from `claude` at run time.
  Done when: `fm doctor` lists tools and events that Claude Code exposes and Foreman never references, and files each as a captured task once.

- **Ask From The Page: answer fm ask grants by phone (wild)** — FEATURE — value 3 — effort M — risk high — category: remote control
  Why: when the guard blocks and needs a plain-word grant, the user must be at the terminal. Combining PushNotification with an Artifact "ask Claude" approval would let them approve from anywhere. Assumption: the user can authenticate the approval so a stray comment can't grant.
  Done when: a push links to a page whose approval writes a one-time grant matching the exact blocked command, and an unauthenticated comment grants nothing.
