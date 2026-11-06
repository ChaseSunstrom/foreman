# Brainstorm — lens: simplicity

- **Give endpoint models the same worker path as CLIs** — CLEAN — value 5 — effort L — risk med — category: runners
  Why: the pack shows two execution paths, harness-run slots for models and CLI runners judged per changed file. Every new feature (stall detection, progress, bench, lean profile) has to be built twice. A tiny built-in worker that speaks the CLI runner contract on top of an endpoint would leave one path. Assumption: the slot loop can be expressed as a worker process without losing its checks.
  Done when: `fm code bench` runs one seeded task against a models.json endpoint and against a CLI runner through the same code path, and a grep finds a single runner-launch function.

- **Merge models.json and code.toml into one config file** — CLEAN — value 4 — effort S — risk low — category: config
  Why: the pack has `models.json` plus `$FOREMAN_HOME/code.toml`, and the user asked that "one config line picks the default". This is about one file the user sees, not the path helper that was dropped earlier. Assumption: users have few hand-edited entries.
  Done when: an old pair of files is read and rewritten into one file on first run with no behaviour change, and `fm code runners` names that single file as the source.

- **Cut the four line-mode switches to one `--format`** — CLEAN — value 3 — effort S — risk low — category: CLI surface
  Why: T-1343 left `--plain`, `--json`, `--dry-plan` and "a pipe" all deciding whether to skip the app. One `--format app|plain|json` with auto-detection when it is absent gives users one thing to remember. Keep the old flags as hidden aliases.
  Done when: all old invocations produce byte-identical output through the new flag, and `fm code --help` lists one format option.

- **Remove Python TUI extensions until a second real one exists** — CLEAN — value 3 — effort S — risk low — category: TUI
  Why: the pack mentions extensions plus a firewall that switches off slow or failing ones, which is machinery for a feature with no evidence of users. T-0166 shows even the existing UI code is hard to untangle. Assumption: no extension exists outside the repo's own fixtures.
  Done when: the extension loader and firewall are deleted, the TUI suite stays green, and a documented one-line way to restore them from git history is left in the changelog.

- **Hold one open FEATURE per area** — CLEAN — value 4 — effort S — risk low — category: queue
  Why: Open work lists about 40 deferred "Later from T-…" briefs and a 29-brief round-1 slate, while the user keeps asking for more. A WIP limit makes `fm task new` for FEATURE refuse while another brief is open in the same area, and offers to defer or merge instead. This differs from the earlier idea of archiving the tail, because it stops the pile growing at the source.
  Done when: creating a second FEATURE in an area with one open prints the open ID and a merge or defer command, and a test shows the limit does not apply to FIX.

- **Show detected-only runners as one line, not entries** — CLEAN — value 3 — effort S — risk low — category: runners
  Why: opencode, qwen, cursor-agent, goose and amp are "detected only", so they appear in lists but cannot run, and T-0335 to T-0337 show the same trio blocked for months. List only runnable runners and add one line, "5 more detected, not yet runnable".
  Done when: `fm code runners` and the app's `m` picker show runnable runners only, plus that line, and the registry keeps the detection data.

- **Freeze default routing to a three-line rule** — CLEAN — value 4 — effort S — risk low — category: runners
  Why: the idea pile holds dozens of learned-router, tournament and quota proposals, but the shipped behaviour is already simple: the user's pick, then the claude CLI, then the first runnable. Writing that rule down, printing it in the plan header and testing it blocks speculative routing work until the bench has data. Assumption: nobody has asked for learned routing.
  Done when: the plan header names which of the three rules chose the runner, and a test covers each rule.

- **Share one stall classifier between TUI, events and doctor** — CLEAN — value 3 — effort S — risk low — category: diagnosis
  Why: T-1336 added stall causes (no output, a prompt, a rate limit, silent) for the TUI, and the request list shows `fm code why`, `fm doctor` and preflight lamps all needing the same answers. One pure function over the last events and process state keeps those answers from diverging.
  Done when: a grep shows one cause-classifying function, and the same fixture of events yields identical wording in the event stream, the TUI and `fm doctor`.

- **Route every feature through three seams** — CLEAN — value 4 — effort L — risk med — category: architecture
  Why: stall detection, live progress, the lean profile, bench, the guard's judge and the proposed upstream adoption are each wired into the loop separately. Defining before-step, after-step and on-event as the only extension points lets new capabilities be added without touching the loop. Wild: this is a refactor-first bet and the three seams may prove too few. Assumption: most current features fit those three.
  Done when: the loop file has no feature-specific branches, and moving one existing feature (stall detection) onto a seam changes no test output.

- **Wild: Run a delete-and-see pass nightly** — CLEAN — value 4 — effort M — risk low — category: subtraction
  Why: assumption: the 77 modules in `plugin/lib` and 239 test files hold code that nothing observable depends on. A nightly job stubs out one module or function at a time in a scratch copy and runs the gates. Anything that stays green becomes a queued deletion brief with the evidence. This differs from coverage-based dead-code reports because it measures what the suite and e2e notice, not what executes.
  Done when: a run on a scratch copy files at least one real deletion brief (or reports zero) and never touches the working tree.

- **Wild: Make the loop card the executable spec** — CLEAN — value 4 — effort M — risk low — category: documentation
  Why: the README says plan → task → checks fail first → steps → checks pass → close. Writing that as a ten-line script that a stub runner actually executes means the card cannot drift, and any new feature must show which line it extends. Assumption: the full loop can run against a no-model stub, which the "do nothing" dry-mode idea also needs.
  Done when: CI runs the card against the stub runner and fails if the printed card and the actual phases differ.

- **Wild: Treat "etc." as one bounded round, not an open loop** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the user writes "etc.", "recursive until dry", "I shouldn't even need to ask", and pushes back with "don't stop until complete". The simple reading is a standing mandate with a fixed stop rule: one round, a budget, stop when a round yields no accepted idea. Foreman then needs no new vocabulary. It may reuse the convergence certificate idea, but this is the only user-facing rule: the word "etc." means "one more round, then report".
  Done when: a request ending in "etc." runs exactly one extra brainstorm-and-build round within a stated budget, and ends with a report that says why it stopped.
