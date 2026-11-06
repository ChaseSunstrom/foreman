# Brainstorm — lens: user value

- **Diagnose a silent run in the first ten seconds** — FIX — value 5 — effort M — risk low — category: reliability/trust
  Why: the nixie run "just isn't doing anything" while a planner burned 66k–133k tokens per call with no visible signal. T-1329 adds streaming progress, but nothing tells the user *why* it's quiet. Add a watchdog that, after N seconds without events, prints a one-line cause ("claude planner loading 14 plugins, 90k tokens of context, 41s in") plus the one key to cancel or switch runner.
  Done when: a fake CLI runner that sleeps 30s produces a "waiting on claude planner: no output for 10s, N input tokens" line in Activity and in `fm code --plain` output, asserted by a test.

- **Preflight the runner before the first request** — FEATURE — value 5 — effort S — risk low — category: setup
  Why: the user hit "fm not a command", then "no model, press m, pick claude". Assumption: a 3-second probe (binary found, logged in, one-token call, measured context cost) would catch these. Run it on first launch of `fm code` and cache the result per runner.
  Done when: with `claude` absent from PATH, `fm code` opens the app, shows "claude: not found" next to the other runners found, and a request is never sent to a broken runner.

- **Slim nested workers by default** — PERFORMANCE — value 5 — effort M — risk med — category: cost/speed
  Why: nested Claude Code loads every plugin and Foreman's own hooks, so each planner call costs 66k–133k tokens. T-1327 removes Foreman's context; go further and launch workers with a minimal settings profile (no unrelated plugins/MCP, project CLAUDE.md only). The guard stays on.
  Done when: bench shows planner input tokens under a stated ceiling (e.g. 20k) on the nixie-like fixture, with guard verdict corpus unchanged.

- **Make `fm code` answer "what should I work on?"** — FEATURE — value 5 — effort M — risk low — category: app home
  Why: the user wants a management app over many projects (T-1330 lists queue/inbox). Add a ranked "next best action" across all projects (unblocked, proof-ready, cheapest, stale-first) with one key to run it. This is the answer to launching with no request.
  Done when: with three fixture projects, the home screen's top row is the expected task and Enter starts it with the default runner.

- **Pick the runner per task automatically, and show why** — FEATURE — value 4 — effort M — risk med — category: routing
  Why: the user wants ANY CLI/model. The bench (`fm code bench`) already grades runners. Assumption: use those grades plus cost and availability to route (cheap local model for docs, claude for hard fixes), with a visible one-line reason and an override.
  Done when: given bench results for two runners, a docs task routes to the cheaper one and a fix task to the higher scorer, and the choice and reason appear in the run's event log.

- **Resume any interrupted run exactly where it stopped** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: quitting orphaned the planner; T-1326 kills it, which means work is lost. Since the harness owns stations and the event log, restart from the last completed station with `fm code --resume`, offered automatically on next open.
  Done when: killing a run mid-step-2 and reopening offers "resume at step 2 of 4", and the resumed run closes without redoing steps 1 and 2 (asserted by the event log).

- **Auto-brainstorm from friction, with a visible receipt** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the user said "I shouldn't even need to ask you"; T-detected phrases like "just isn't doing anything" are already listed as triggers. Close the loop: when friction is detected, queue a diagnose task, run it, and show "I noticed X, here is what I found and fixed" on next open. Never release or push without the standing grant.
  Done when: feeding the phrase "it just isn't doing anything" in a fixture session creates a queued diagnose task tagged with its source quote, visible on the home screen.

- **Quote-back the request into a checkable definition of done** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: "super improve X" is vague and led to long loops. Turn it into 3–5 testable criteria shown before work starts, editable in one key; the harness then closes against them.
  Done when: a vague request produces a criteria list with a runnable verify command each, and the run cannot close with any unverified.

- **Show per-project cost and time spent, weekly** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the user cares about duel cost and time (T-1231). Assumption: a per-project, per-runner weekly table in the home screen lets them see where tokens go.
  Done when: after two fixture runs on different runners, the table shows both with token and dollar totals matching the event logs.

- **Run the whole queue unattended with one stop-line** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: "dont stop until complete, full auto". `fm code --queue` that works every unblocked task across projects, pausing only on a "needs you" item, and ends with a digest.
  Done when: a fixture queue of three tasks with one blocked finishes two, skips the blocked one, and prints a digest naming it.

- **Wild: Adopt an existing Claude Code session into fm code** — FEATURE — value 3 — effort L — risk high — category: interop (wild)
  Why: assumption: users already have half-finished sessions. Read a Claude Code transcript, extract the request and progress, and continue it under the harness's proof discipline.
  Done when: pointing at a fixture transcript creates a task with its original request and a plan marking already-evidenced steps.

- **Wild: Type a sentence, get the runner** — FEATURE — value 3 — effort S — risk low — category: config (wild)
  Why: "better config/setup". `fm code setup "use local ollama for docs, claude for everything else"` writes the config lines and shows the diff before saving.
  Done when: that sentence yields a config with both rules, shown as a diff, with no write until confirmed.

- **Wild: A "rubber duck" runner that only asks questions** — FEATURE — value 2 — effort S — risk low — category: delight (wild)
  Why: a read-only runner that interviews the user about a vague idea, then hands a sharpened request to the real runner; fits the "super improve" style requests.
  Done when: running it makes zero file changes (checked by git status) and outputs a request with at least three concrete criteria.
