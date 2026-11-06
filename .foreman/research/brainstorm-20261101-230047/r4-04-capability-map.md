# Brainstorm — lens: capability map

- **Climb a per-trigger autonomy ladder** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: assumption: "file-a-task only" and "land on a branch" are listed as fixed defaults, but no idea says how a trigger earns more. Each trigger starts at *file a capture*, then *branch*, then *draft PR*, and moves up a rung only on a held streak plus one user yes. A miss drops it a rung.
  Done when: `fm triggers` shows each trigger's rung. A test promotes a fixture trigger after N held fires and one recorded yes, and demotes it after a reverted fire.

- **Add one-shot continuations that survive session death (`fm after`)** — FEATURE — value 5 — effort M — risk low — category: scheduling
  Why: Pillar 1 says never idle while a gate, build, pipeline or review runs, and `fm ci-watch` covers only CI. A generic "when X happens, resume this task with this note" would cover a pid exit, a file appearing, a run finishing or a PR review. The tick would own it, and it would delete itself after firing.
  Done when: a test kills the session, then touches the awaited file. The next tick resumes the task with its note exactly once, and the entry is gone.

- **Classify red CI as infra flake or code, then rerun or draft** — FEATURE — value 4 — effort M — risk med — category: CI watcher
  Why: 11 ship bets held in a row, so most reds are probably not code. Rerunning a signature-matched infra failure once costs nothing, and only a repeat red should become a fix lane.
  Done when: replaying a recorded runner-timeout log triggers one rerun and no lane. Replaying an assertion failure files a lane.

- **Poll each blocked task's blocker and file the single yes** — FEATURE — value 4 — effort S — risk low — category: blocked work
  Why: T-0325 (needs libappindicator), T-0418 (update foreman-ui to 0.6.1) and T-0335/T-0336/T-0337 are blocked on facts a probe can check: a package present, a host version, a CLI on PATH. When the probe flips, the tick files the exact install as one queued yes.
  Done when: a blocked task carrying a `--unblock-when` command flips to ready on the tick after the command passes, with the install card attached.

- **Add chat-ops comments as the control channel (`/fm why|stop|retry`)** — FEATURE — value 4 — effort M — risk med — category: issue watcher
  Why: assumption: an issue label starts work, but the user then needs a way to steer a self-started lane from where they are, the PR or issue thread. Only the repo owner's comments count, and issue text stays untrusted data.
  Done when: a fixture comment from the owner stops a lane, and the same text from another author is ignored and logged.

- **Claim work so watchers don't collide with humans or other agents** — FEATURE — value 3 — effort S — risk low — category: issue watcher
  Why: assumption: watchers over issues and PRs can duplicate a teammate's in-flight branch. The watcher skips any issue that is assigned, has a linked open PR or branch, or carries a claim marker. It writes its own marker before starting.
  Done when: a fixture issue with a linked branch is skipped with the reason logged, and an unclaimed one is started and marked.

- **Fire the full capability exam when a cheap arm regresses** — FEATURE — value 4 — effort S — risk low — category: exam trigger
  Why: steers of 2026-11-01 forbid long session arms except `--final` or `--regressing N`. Nothing starts the `--regressing` run itself. When the finders or Haiku arm drops for a capability, the tick queues that capability's full exam as one yes, with the cost shown.
  Done when: a seeded regression in a free-arm result file produces one queued exam card naming the capability. Without a regression, no card appears.

- **Watch the host's release notes and file deletion tasks for Foreman code they obsolete** — FEATURE — value 3 — effort M — risk med — category: subtraction
  Why: T-0794 (slim Foreman) and the lean ratchet want subtraction, and host-CLI drift is already a listed trigger. This version goes beyond a compatibility run: when a Claude Code, Codex or Gemini release adds a native feature, it files a cleanup candidate that cites the changelog line.
  Done when: a fixture changelog line about a native plan-mode feature files a CLEAN task linking the Foreman module it overlaps.

- **Scope triggers to subtrees with per-path owners and budgets** — FEATURE — value 3 — effort M — risk low — category: monorepo
  Why: assumption: the repo has `plugin/`, `site/` and `mods/` with different gates (2072 files). A trigger on `site/` should run only site gates and spend only its own budget.
  Done when: a change under `site/` fires only the site-scoped trigger, and a change under `plugin/` fires the other.

- **Run a nightly perf bench and auto-bisect a regression to a commit** — FEATURE — value 3 — effort M — risk low — category: regression watcher
  Why: `plugin/tests/bench_hooks.py --runs 20` is already a gate, and hook p95 is in the lean ratchet. A nightly run that bisects a p95 jump to one commit gives the lean "name the commit" idea a trigger, so nobody has to ask for it.
  Done when: a planted 40 ms sleep in a fixture history is named by the bisect as the offending commit.

- **Sweep stale branches and worktrees weekly into one batched yes** — CLEAN — value 2 — effort S — risk low — category: janitor
  Why: parallel lanes and the merge train leave branches and worktrees behind. The sweep lists those that are merged, abandoned or orphaned, with age and last commit. Nothing is deleted until the one yes.
  Done when: a fixture repo with 3 stale branches yields one card, and a yes deletes only those 3.

- **Wild: Re-check dated assumptions with a probe (`fm bet-on-date`)** — FEATURE — value 3 — effort M — risk low — category: hypotheses
  Why: wild. A plan or decision can carry "this holds until D, check it with command C". On D the tick runs C and reopens the task if C fails. Foreman's own "n/a" cells and "not-yet" blockers are the first customers.
  Done when: a task with a past due date and a failing probe reopens on the next tick, citing the probe output.

- **Wild: Show the held rate of self-started work on a README badge** — FEATURE — value 2 — effort S — risk med — category: proof of work
  Why: wild. The proof-before-presentation rule says public numbers must come from a producing command. A badge saying "self-started fixes held 14 of 15, last 30 days" would be computed from the trigger log and would go red if the log is stale.
  Done when: the badge text is regenerated by a command and the sweep fails if it disagrees with the log.

- **Wild: Add a physical "start my day" tag that plays the morning note aloud** — FEATURE — value 2 — effort M — risk low — category: surfaces
  Why: wild. A phone NFC shortcut or a keyboard chord hits a loopback endpoint. Foreman prints (or reads aloud, locally) the morning note and asks the queued yes items one at a time. It reuses the notes and yes sheet that other ideas already propose.
  Done when: the endpoint call returns the same text as `fm morning` and records that it was read.

Next question: which trigger families does the user actually act on in the first week, by the trigger log, and does that match the families the 59 cells assume?
Next question: what does a trigger do when two events need different harnesses or models and only one budget slot is free?
