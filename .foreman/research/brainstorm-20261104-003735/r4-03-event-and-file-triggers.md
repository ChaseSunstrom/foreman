# Brainstorm — lens: event and file triggers

Answering one earlier question through this lens: if the main harness changed tomorrow, file-system, git-reflog and journald triggers keep working, but anything fed by PostToolUse or transcript tails silently stops. Nothing today tests that split.

- **Run affected tests on save, zero tokens** — FEATURE — value 5 — effort M — risk low — category: file triggers
  Why: the map already holds tests→src, and the request wants overnight progress without model spend. Nothing in the list runs the affected tests locally before a model is involved. A lane starts only when a test goes red.
  Done when: saving a source file runs only its mapped tests and writes a pass/red event, and a deliberate break files a brief while a clean save files nothing.

- **Skip semantic no-op file events** — PERFORMANCE — value 4 — effort M — risk low — category: file triggers
  Why: debounce and ignore-lists exist, but formatter runs, comment edits and generated-file rewrites still fire. Assumption: tree-sitter (named in standing rules) is available for the hash.
  Done when: a whitespace-only or comment-only save of a Python file emits no trigger, and a one-token logic change does.

- **Tell user edits from agent edits by joining inotify with the PostToolUse ledger** — FEATURE — value 4 — effort M — risk med — category: provenance
  Why: self-cause filters and loop breakers exist, but they guess. An exact actor label (user, a named lane, or unknown) lets "skip while the user is working in this tree" be precise. Unknown-actor writes are treated as untrusted.
  Done when: each file event in the spool carries an actor, and a lane's own edit never re-fires its trigger in a test.

- **Declare event joins and sequences** — FEATURE — value 4 — effort L — risk med — category: trigger rules
  Why: all listed triggers are single-event. Real work follows patterns such as "CI red within 10 minutes of a lockfile change" or "the same test fails on three saves in a row".
  Done when: a rule with `all_of` / `then_within` fires only on the pair in a replayed fixture, not on either event alone.

- **Fire a lane when an exam or outcome measure regresses** — FEATURE — value 4 — effort M — risk low — category: metric events
  Why: the pack shows drive stops up from 0 to 0.1 and failed tool calls up by half, but nothing starts work when such a ledger reading moves. The standing rule says a regressing capability gets its full arms run. This trigger makes that automatic.
  Done when: a planted rise in the failed-call rate in a scratch ledger files one diagnosis brief naming the capability and the delta, and files no second brief until the reading recovers.

- **Check watcher capacity (inotify watches, fds) in `fm doctor`, with a polling fallback** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: 2,358 files plus lane worktrees plus the editor can exhaust `fs.inotify.max_watches`, and the failure would be silent, so triggers just stop. This would also explain "overnight made no progress".
  Done when: doctor prints the watch count against the limit, and with the limit lowered in a test the watcher degrades to polling and logs it.

- **Turn PR review comments into a lane that addresses them** — FEATURE — value 3 — effort M — risk med — category: forge events
  Why: issue and CI watchers are listed, but review comments are the third common source of "work that should just start". The comment text is fenced as data, and the lane may only push a branch.
  Done when: a fixture comment containing an injected instruction is treated as data, and a clear request produces a branch with a passing test.

- **Watch the advisory feed against the lockfile** — FEATURE — value 3 — effort M — risk low — category: external events
  Why: lockfile-change watchers exist, but a CVE landing against an unchanged lockfile never fires. Any dependency bump it needs goes into the queued-installs "one yes" card.
  Done when: a fixture advisory matching a pinned version files an audit brief and adds the bump to the pending-yes card without installing anything.

- **Use git reflog as an event source** — FEATURE — value 3 — effort S — risk low — category: file triggers
  Why: resets, amends, rebases and checkouts happen outside any hook. Evidence tied to a commit goes stale silently, and an open lane's base can move. Reflog is harness-independent.
  Done when: an amend of a commit that has recorded evidence marks that evidence stale within one watcher cycle.

- **Send repeated failing shell commands to a help draft (wild)** — FEATURE — value 3 — effort M — risk med — category: shell events
  Why: assumption: a precmd hook can write `{cmd, exit, cwd}` to the spool. Three failures of the same command shape in ten minutes is a signal no one has used. The result is a draft, never an action, and arguments are redacted.
  Done when: three failing `cargo build` runs produce one draft note naming the error's first line, and a fourth within the window adds nothing.

- **Turn journald and coredump entries from the user's own dev services into repro tasks (wild)** — FEATURE — value 3 — effort M — risk med — category: system events
  Why: crashes while the user is away are invisible to CI and issue watchers. A crash with a stack trace is a ready-made brief. Assumption: user-level journal access.
  Done when: a synthetic crash entry creates a task with the trace, and the same trace signature arriving again increments a counter instead of creating a second task.

- **File a task from a screenshot dropped in a watched folder (wild)** — FEATURE — value 3 — effort S — risk low — category: file triggers
  Why: phone-synced or screenshot folders are the lowest-effort way for the user to say "this looks wrong". The brief gets the image and a rendered-artifact criterion; the folder name picks the repo.
  Done when: dropping a PNG in the folder creates a task with the image attached and a criterion to compare the rendered page.

- **Pre-warm for predicted events (wild)** — PERFORMANCE — value 2 — effort M — risk low — category: prediction
  Why: assumption: the spool shows recurring rhythms, such as CI usually following a push within a minute. Fetching the log and warming the worktree and local model before the event cuts event-to-first-tool latency.
  Done when: in a replay, the median latency for the predicted trigger kind drops against the unwarmed baseline, and a false prediction costs no more than a logged no-op.

- **Run a trigger-storm soak on a scratch repo (wild)** — CLEAN — value 3 — effort M — risk low — category: reliability
  Why: dedupe and loop breakers exist, but nothing exercises them together. Replay 10,000 mixed events, including agent-authored floods, against a full trigger set.
  Done when: the soak finishes inside a fixed CPU and spawn budget with zero duplicate lanes and zero loops, and the report is stored.

Next question: which trigger, left running for a month, would the user miss least, and what ledger line would show that before they have to say so?
Next question: when the machine is off at the moment of an event (the forge fired while suspended), which source lets the event be reconstructed afterwards, and which sources lose it for good?
