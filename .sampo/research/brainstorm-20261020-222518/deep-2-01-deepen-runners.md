# Brainstorm — lens: deepen: runners

- **Build a runner ledger that grades every runner per task kind** — FEATURE — value 5 — effort M — risk low — category: runners
  Why: bench exists (`fm code bench`) and 7/7 request kinds closed on claude only; audition, route-cheapest and fallback ideas all need one shared record of pass rate, cost, seconds per kind. Assumption: bench results can be stored per runner/kind in Foreman's home.
  Done when: after two fake-runner runs of different kinds, `fm code runners --stats` prints pass rate, median cost and seconds per runner per kind, read from a ledger file.

- **Route each step to a runner by ledger and budget** — FEATURE — value 5 — effort L — risk med — category: routing
  Why: the harness fills one small JSON slot at a time, so planning, step edits and verify-fixing can go to different runners (cheap local model for slots, claude for hard edits). Assumption: the harness can switch runner between stages.
  Done when: with a config of `plan: A, edit: B`, a fake run's event log shows plan by A and edit by B, and the guard judged both.

- **Fall back across runners on classified failures** — FEATURE — value 4 — effort M — risk med — category: resilience
  Why: the user's nixie run stalled with no signal; failures (rate limit, auth, timeout, schema drift, silence) deserve different responses. Assumption: failures can be classified from exit code and stderr.
  Done when: a fake runner that exits with "rate limit" makes the run continue on the next runner, and the receipt names why it switched.

- **Hand off half-done work between runners with a packet** — FEATURE — value 4 — effort M — risk med — category: handoff
  Why: stopping and switching runners today restarts; the harness already owns plan, step status and diff. Packet = plan + done steps + git diff + last failing check. Assumption: the harness state is serializable.
  Done when: killing runner A mid-step and resuming with runner B starts at the unfinished step and doesn't redo closed ones (test asserts step count).

- **Run a startup-tax doctor that trims nested CLI cost** — PERFORMANCE — value 5 — effort M — risk low — category: startup
  Why: the nixie planner burned 66k–133k input tokens per call from plugins and hooks. Measure a one-token call per runner, report tokens and seconds, and suggest flags (no plugins, bare settings). Assumption: each CLI has a way to run lean.
  Done when: `fm code doctor` lists each runner's tokens and seconds for a "reply ok" call and flags any above a configured budget.

- **Detect a silent runner and say so within 20 seconds** — FIX — value 5 — effort S — risk low — category: liveness
  Why: "it just isn't doing anything" is the user's direct complaint. Combine heartbeat (T-1329) with a stall verdict: no bytes, no child CPU, no file change shows "waiting on claude, 40s, no output, tokens so far unknown".
  Done when: a fake runner that sleeps 30s produces a stall cue in Activity by second 20, tested with a shortened threshold.

- **Define runners as 8-line manifests, learned by probing** — FEATURE — value 4 — effort M — risk med — category: config
  Why: users want "ANY CLI". A manifest (command, prompt-by-arg-or-stdin, output format, plan flag, resume flag, lean flags) is data; `fm code runners add NAME` runs `--help` and a probe to draft it. Assumption: help text is parseable well enough for a draft the user confirms.
  Done when: adding a fake CLI via a manifest runs a task to close with no Python changes.

- **Race two runners on one task and keep the cheaper green one** — FEATURE — value 3 — effort L — risk med — category: racing — wild
  Why: assumption: git worktrees give isolation. Both run in separate worktrees, checks decide, the cheaper passing diff lands, and the ledger learns from the race.
  Done when: a fake race where both pass lands the cheaper diff and discards the other worktree, and the receipt shows both costs.

- **Cap spend per runner and per project** — SECURITY — value 4 — effort M — risk low — category: budget
  Why: with cloud keys and many projects, an unattended full-auto run can overspend. Assumption: token usage is reported by most runners, estimated otherwise.
  Done when: a run with a 1000-token cap stops with a named "budget" verdict and a resumable state.

- **Let a runner prove it can't see outside its project** — SECURITY — value 4 — effort M — risk med — category: isolation
  Why: managing many projects with many CLIs raises the stakes; the guard judges changed files, but a worker can read another project. Run a canary read test per runner on setup and report it.
  Done when: `fm code doctor` shows a canary result per runner, and a fake runner that reads a canary outside the project is flagged.

- **Build a runner pit-crew that auto-heals setup** — FEATURE — value 3 — effort M — risk low — category: setup — wild
  Why: the user hit `fm` missing from the shell. Doctor finds a CLI not logged in or not on PATH, then offers the exact fix command, with consent, and re-probes. Assumption: fixes can be listed per known CLI.
  Done when: with `codex` removed from PATH in a test, doctor prints the install/PATH step and `--fix` applies the PATH link and re-checks green.

- **Replay a recorded run on a different runner** — FEATURE — value 3 — effort M — risk low — category: evaluation
  Why: `--record` and event logs exist; replaying the request and checks against runner B gives an A/B on the user's real work without new prompts. Assumption: the request and criteria are in the event log.
  Done when: `fm code replay RUN --runner B` reruns the same request and prints a side-by-side of the two receipts.

- **Run a runner that is a human** — FEATURE — value 2 — effort S — risk low — category: runners — wild
  Why: a "CMD {prompt}" runner already exists; make an `$EDITOR` runner that opens the step as a file, so the harness judges a person's edit like any worker. Useful for demos and for taking over a stuck step.
  Done when: a test using a scripted editor as the runner closes a task through the same guard and checks.

- **Pool runners as a fleet with per-runner concurrency lanes** — FEATURE — value 4 — effort L — risk high — category: fleet
  Why: the home screen spans many projects (T-1330); the queue could use free runners in parallel, with leases keeping one writer per project. Assumption: lease code from the worker work extends to runners.
  Done when: two queued tasks in two projects run concurrently on two fake runners while a third in one of them waits for its lease.
