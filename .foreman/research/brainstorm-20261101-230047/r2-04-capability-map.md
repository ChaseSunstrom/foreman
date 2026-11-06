# Brainstorm — lens: capability map

- **Set an overlap policy per trigger** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: assumption: the pack shows a tick, `fm ci-watch` and lane work that can run long, but no rule for a fire that arrives while its last run is still going. Cron, Kubernetes CronJobs and Temporal all offer skip, queue or replace.
  Done when: a test fires a trigger twice with the first run still open, and the second is skipped, queued or replaces it as configured, with the choice logged.

- **Retry failed fires and keep a dead-letter list** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: assumption: a fire that fails (rate limit, offline, crash) currently has no stated retry. Add capped backoff, then park it in a dead-letter list that `fm doctor` and the morning note show.
  Done when: a stubbed fire that fails three times is retried at growing intervals, then appears in the dead-letter list with its error and a one-command replay.

- **Add jitter and API-budget awareness to watchers** — PERFORMANCE — value 3 — effort S — risk low — category: watchers
  Why: assumption: CI and issue watchers poll GitHub, and many repos on one user's tick would all poll on the same minute and hit rate limits. Renovate and Dependabot spread their load for the same reason.
  Done when: with 20 watched repos the poll times are spread across the interval, and a 403 rate-limit response makes the watcher back off to the reset time without erroring.

- **Run a post-ship verification ladder** — FEATURE — value 4 — effort M — risk med — category: CI watch
  Why: the pack shows `fm ci-watch --last-ship` settling ship bets once. Nothing re-checks the artifact later, so add timed checks (about +1h and +24h) that install it clean, run the first-use path and probe the published site.
  Done when: after a test ship, two later checks are queued by the tick, and a deliberately broken artifact fails the +1h check and files a task.

- **Import existing automation as trigger proposals** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: assumption: users already have crontab lines, GitHub Actions `on:` blocks and git hooks. Read them and propose an agent-side counterpart (for example "when this nightly job fails, open a lane"), queued for one yes. Zapier and n8n lean on imports like this.
  Done when: given a fixture repo with a cron-scheduled workflow, `fm triggers import` lists a proposal for it and installs nothing.

- **Pick the harness and model per trigger** — FEATURE — value 4 — effort M — risk med — category: routing
  Why: the pack stresses cheapest-model-that-can and Foreman running on Codex, Gemini and opencode. A fired trigger should declare which harness and tier runs it, with a fallback when the preferred one is rate-limited.
  Done when: a trigger with `harness: codex, tier: cheap` starts that child, and with Codex unavailable it falls back to the named second choice and logs why.

- **Give each trigger a scoped capability profile** — SECURITY — value 4 — effort M — risk med — category: safety
  Why: the pack's reach and guard rules cover sessions, but a self-started lane has no per-trigger limits. Each trigger would carry an allowlist of verbs, paths and network hosts, narrower than an interactive session's.
  Done when: a trigger limited to read-only plus `fm task` is denied an `Edit` outside its allowed paths, and the denial shows in the fire record.

- **Mirror calendar-based away mode** — FEATURE — value 3 — effort M — risk low — category: scheduling
  Why: assumption: the user's meetings, vacations and focus blocks (an ICS file or URL) are the best signal for quiet hours. Away mode would raise unattended autonomy and batch yeses, and meeting time would hold fires.
  Done when: with an ICS fixture containing a vacation week, the dispatcher reports away mode for those dates and queues no interrupting yes.

- **Watch the public site against main** — FEATURE — value 3 — effort S — risk low — category: watchers
  Why: the pack has a standing rule that the Genesis site publishes on every tower change, and a rule that public claims match the exam lines. Nothing checks that the live page is current or its links work.
  Done when: a scheduled probe compares the live `site/genesis` data hash with main, and a planted stale or 404 file produces a fix task.

- **Test triggers in CI with fixture event packs** — CLEAN — value 3 — effort M — risk low — category: developer experience
  Why: assumption: a trigger table needs regression tests, like GitHub Actions' `act` or Renovate's dry-run. A directory of recorded events plus the expected fires would run in `fm check`.
  Done when: `fm check` replays a fixture pack and fails when a changed trigger rule fires on an event it should ignore.

- **Hunt flaky tests on a schedule** — FEATURE — value 3 — effort M — risk low — category: CI watch
  Why: the pack shows `fm task finish` refusing on a failed full check, and an earlier idea asks for a flake ledger. A nightly lane would rerun failed jobs and suspect tests N times, then file a quarantine task with the numbers.
  Done when: a fixture test that fails one run in five is reported with its failure rate and a quarantine task, and a stable test is not.

- **Wild: Offer a local event feed over MCP** — FEATURE — value 3 — effort M — risk med — category: integrations
  Why: wild. Expose the trigger event stream as an MCP resource so Claude Code, Codex or Gemini sessions can subscribe, and a running session can react to "CI went red" without polling.
  Done when: an MCP client subscribed to the feed receives a test event within 5 seconds of a synthetic CI failure.

- **Wild: Ask "what do you wish ran itself?" once, from the user's history** — FEATURE — value 4 — effort M — risk low — category: unspoken needs
  Why: wild. Mine the user's past repeated manual sequences and `fm` verbs, then offer the top three as ready-to-install triggers with a preview on last week's data. This goes past the sentence-compiler idea by starting from observed behaviour.
  Done when: on a fixture history with a command run every Monday, the top proposal is a Monday trigger and it is never installed without a yes.

- **Wild: Let the user's phone camera drop work into the inbox** — FEATURE — value 2 — effort M — risk med — category: devices
  Why: wild. A shared folder watched by the tick turns a whiteboard photo or screenshot of an error into a captured task, with the image OCR'd locally. This gives the drop folder a mobile front end.
  Done when: a PNG of a stack trace dropped in the folder becomes a capture containing the extracted trace text, with no network call.

- **Wild: Replay a recorded week at fast speed** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: wild. Record a week of real trigger events locally, then play it through the whole dispatcher in minutes against a scratch tree, to show what the install would have done before the user says yes.
  Done when: replaying a fixture week produces a report of fires, skipped overlaps and spend, and writes nothing to the real repo.

Next question: which of the 59 cells would a self-started lane touch that a session-started lane never does, and has anyone checked that those cells run under the same guard?
Next question: what do users do after a self-started task lands (accept, edit, revert), and can that become the trigger's score instead of its own precision count?
