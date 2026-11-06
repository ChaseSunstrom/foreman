# Brainstorm — lens: simplicity

- **Wake deferrals with one-shot transient timers** — FEATURE — value 4 — effort M — risk med — category: scheduling
  Why: assumption: `systemd-run --user --on-calendar=… fm wake T-NNNN` creates no unit file, so it needs no install the user has to approve. Every dated deferral (T-2603 already counts them) would get its own timer when it is made. This replaces the always-on tick with a clock that exists only while there is something to wait for. Fall back to `at`, or to nothing, when neither is available.
  Done when: deferring a task with `--until` 30 seconds out, in a test run, makes `fm wake` fire once and no unit file remains under `~/.config/systemd/user`.

- **Backfill wake predicates onto the 30 "later: needs…" deferrals** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: T-0826 to T-0869 all read "later: needs evidence/cases/channel". None can wake itself, and nobody can say how many are already ready. Add a one-line shell predicate (exit 0 means ready) to each. Any session can evaluate them, so self-triggering becomes measurable today, with no timer.
  Done when: `fm deferred --ready` prints the tasks whose predicate passes, and the count is recorded in the first report.

- **Score each deferral's wake against the user's own memory** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: assumption: the real question is whether self-triggering beats the user remembering. At defer time, store the task id. If the user's asks mention it before the wake, mark the wake "redundant". If it fires first and is acted on, mark it "earned". This needs no install and gives a causal-ish grade.
  Done when: `fm doctor` prints "wakes: N earned, M redundant, K unseen", derived from the ask stream and the wake log.

- **Make the tick's output one overwritten file, `tick.md`** — CLEAN — value 3 — effort S — risk low — category: simplification
  Why: the idea list is full of tick ledgers, beat files, lateness ledgers and receipts. The state is the output. Rewrite one small file each run (what is due, what ran, when). SessionStart reads it and nothing else grows.
  Done when: after 100 tick runs in a test the state dir holds one `tick.md`, which is under 40 lines, and SessionStart quotes it.

- **Let the first prompt of each local day be the daily tick** — CLEAN — value 3 — effort S — risk low — category: scheduling
  Why: assumption: the 6-job interval tables can collapse to "daily on the first prompt, weekly on Monday's first prompt". The marker is a dated filename, `tick-2026-11-02`, and its existence means the tick already ran today, so double runs cannot happen. This is the cheapest install-free clock.
  Done when: two sessions on the same day run the daily jobs once, and a faked date change runs them again.

- **Run the tick with a constant argv and no shell** — SECURITY — value 3 — effort S — risk low — category: unattended safety
  Why: assumption: self-started work reading task titles or issue text is where injection would enter. The tick may spawn only fixed `fm` verbs with fixed arguments, and never a string built from a task field.
  Done when: a test that plants `; touch pwned` in a task title and runs the tick leaves no `pwned` file, and a grep finds no `shell=True` in the tick path.

- **Wake a deferral when a session touches its watched path** — FEATURE — value 3 — effort M — risk med — category: event triggers
  Why: PostToolUse hooks already run on every edit. A deferred task with `watch: path` surfaces itself the moment that path changes, with no clock and no install. Assumption: hook cost stays inside bench_hooks if the check is a set lookup.
  Done when: editing a watched file in a test prints the task's id once, and `bench_hooks.py` shows no p95 regression.

- **Wild: Put the due date in the filename so `ls` is the scheduler** — CLEAN — value 2 — effort S — risk low — category: simplification
  Why: wild. Deferred briefs would live as `T-0827.due-2026-11-10.md`. The user sees what is overdue without any verb, and the tick becomes a sorted `ls` plus a date comparison.
  Done when: `ls .fm/deferred | sort` lists due order, and `fm next` surfaces the same first item.

- **Wild: One line in AGENTS.md or CLAUDE.md as the clock for hookless harnesses** — FEATURE — value 3 — effort S — risk low — category: harness reach
  Why: wild. Codex, Gemini and opencode have no Foreman hooks, so the lazy tick never fires there. "On your first reply, run `fm tick --if-due`" is an instruction-based clock. Its compliance rate is measurable from the tick log.
  Done when: the tick log records a fire whose source is `agents-md`, from a non-Claude harness fixture.

- **Wild: Fire the user's next ask as a title-only draft on wake** — FEATURE — value 2 — effort M — risk med — category: usefulness
  Why: wild. When a deferral wakes, it posts a one-line "revisit T-0827? (y/n)" to the inbox instead of starting work. The yes-rate is then the usefulness metric, measured without an install and with no side effects.
  Done when: a wake writes one inbox line, and `fm doctor` shows the yes-rate once there are at least 10 wakes.

- **Wild: Delete the scheduler and compute "due" on read** — CLEAN — value 3 — effort M — risk med — category: simplification
  Why: wild. Remove tick jobs that only exist to notice dates. `fm next`, `fm status` and SessionStart compute overdue from the task files every time. Self-triggering is then a sort key, and the only thing left to grade is whether the user saw it.
  Done when: with the tick disabled, a deferral dated yesterday heads `fm next`, and the tick code loses one job.

Next question: What is the minimum number of wakes and "earned" grades needed before the user would trust self-triggering enough to spend the one yes on an install?
Next question: Which of the 30 deferred "later: needs…" items has been ready the longest without anyone noticing, and what does that say about every other silent wait?
