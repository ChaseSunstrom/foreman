# Brainstorm — lens: user value

- **Answer "what should I do next?" from the home screen** — FEATURE — value 5 — effort M — risk low — category: app home
  Why: the user wants fm code to be an app like claude and to "figure it out" without being told; T-1330 lists queue/inbox/blocked but nothing ranks them. Assumption: ranking can use task state, age, blockers and last-run outcome already on disk.
  Done when: `fm code` in a fixture with three projects (one blocked, one with a queued S task, one idle) shows the queued task first, with a one-line reason, and a test asserts the order.

- **Make a run's first 30 seconds visibly alive** — FIX — value 5 — effort S — risk low — category: trust
  Why: the nixie run "just isn't doing anything" for minutes at 66k–133k tokens per call. T-1329 covers streaming, but not a floor guarantee that something is on screen immediately (what is being launched, what it loads, how long it has been quiet).
  Done when: with a fake runner that prints nothing for 60 s, the screen shows the launched command, elapsed time and a named "waiting on <runner>" line within 2 s, and a test asserts it.

- **Turn a stalled run into a task automatically** — FEATURE — value 4 — effort M — risk low — category: self-repair
  Why: "I shouldn't even need to ask you"; the planned friction detector covers brainstorming, but a silent run itself should leave a diagnosis and an open task with the run log attached. Assumption: a stall threshold per runner can be learned from the bench.
  Done when: a fake runner that hangs triggers, after the threshold, a captured task whose body names the runner, last event and token count, and the run ends non-orphaned.

- **Ship `fm code doctor` that fixes the first-five-minutes path** — FIX — value 4 — effort M — risk low — category: setup
  Why: `fm` wasn't on the user's PATH outside Claude Code and no model was set. One command that checks PATH, finds runners, detects a duplicate Foreman (plugin plus CLI worker) and offers each fix with its exact command.
  Done when: in a HOME with no link and no config, `fm code doctor --fix` creates the PATH link, writes a default runner line, and a second run reports all green.

- **Show the cost of a request before it runs** — FEATURE — value 4 — effort M — risk low — category: cost clarity
  Why: planner calls at 66k–133k input tokens surprised the user. A pre-run estimate (runner, startup tax, expected calls) lets them pick a cheaper runner. Assumption: the startup tax can be measured by a one-token probe and cached.
  Done when: typing a request in the TUI shows "~N tokens, ~$X, runner R" before Enter, and the estimate is within 2x of the measured run in a bench fixture.

- **Keep one conversation across runs, per project** — FEATURE — value 4 — effort M — risk med — category: continuity
  Why: Claude-like apps feel continuous; fm code has runs but no thread. "Do that again but for the other module" currently has no referent.
  Done when: a second request saying "same for utils" in the same project resolves against the previous run's summary, and the plan quotes the resolved meaning.

- **Hand the user a "while you were away" digest across all projects** — FEATURE — value 4 — effort S — risk low — category: app home
  Why: the user runs several projects and long unattended runs; the idea list has a per-run digest but not a fleet-level one at app open. Assumption: run logs record finish times.
  Done when: opening `fm code` after two runs finished shows each with outcome, the proof line, and what needs the user, and a test asserts the text from fixture logs.

- **Let one sentence reroute a running task to another runner** — FEATURE — value 3 — effort M — risk med — category: runner control
  Why: "any CLI or model" is planned as a registry; mid-run switching when a runner is slow or expensive isn't, and the user currently has to quit and restart.
  Done when: pressing `m` mid-step and choosing codex finishes the current step on codex with the earlier steps intact, shown in the receipt.

- **Wild: Adopt an already-running Claude Code session as a lane** — FEATURE — value 3 — effort L — risk high — category: interop
  Why: wild; the user lives in Claude Code and fm code side by side. Assumption: Claude's session files are readable. The home screen lists live Claude sessions per project, with their Foreman task state.
  Done when: with a fixture session file, the home screen lists it under its project with the current task id.

- **Wild: Say the project in the request, let Foreman find it** — FEATURE — value 3 — effort M — risk med — category: multi-project
  Why: wild; "fix the flaky test in nixie" typed anywhere should route to ~/projects/nixie without a cd. Assumption: project discovery from disk is already planned.
  Done when: from an unrelated directory, a request naming a known project creates its task in that project and the confirmation shows the resolved path before running.

- **Wild: Rehearse a request against a dry-run runner first** — FEATURE — value 3 — effort M — risk low — category: confidence
  Why: wild; a "rehearsal" runs plan and checks only (fail-first proof) on the cheapest runner and shows whether the request is even checkable, before spending on the worker.
  Done when: `fm code --rehearse "<request>"` prints the plan, the failing check, and the estimated steps, and changes no files in the repo.

- **Wild: Publish a per-runner report card from the user's own history** — FEATURE — value 3 — effort S — risk low — category: runner choice
  Why: wild; the bench grades models on seeded tasks, but the user's real closed-versus-stuck history by runner and request kind is more persuasive and sits on disk already.
  Done when: `fm code runners` lists each runner with closed/stuck counts, median time and cost per request kind from local run logs, and says "no data" rather than guessing for empty cells.
