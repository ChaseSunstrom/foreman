# Brainstorm — lens: capability map

- **Poll forges with conditional requests** — PERFORMANCE — value 3 — effort S — risk low — category: watchers
  Why: assumption: the ci-watch and issue/PR watchers (ideas so far) poll with full GETs. Storing ETag/Last-Modified per source and treating a 304 as "nothing changed" makes a quiet tick cost near zero API quota. It also gives a clean "checked, nothing found" signal.
  Done when: a test with a fake forge returning 304 shows a repeat poll with no change spends 0 rate-limit units and logs `unchanged`.

- **Add metamorphic twins to every planted-event scenario** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the pack's measurement ideas plant positive events; the gap is false fires. Each planted event gets a twin with one minimal edit (a draft PR, a label missing, a branch outside scope) that must not fire. This grades precision without the user's install.
  Done when: `fm exam` prints fire recall and twin false-fire rate per trigger family, and a trigger that fires on any twin fails the run.

- **Mark triggers redundant with the repo's own automation** — FEATURE — value 4 — effort M — risk low — category: dedupe
  Why: assumption: many repos already run nightly CI, Dependabot/Renovate or pre-commit. A scan of `.github/workflows` schedules, `renovate.json` and `.pre-commit-config.yaml` marks any proposed trigger as "already covered by X" before it asks for an install yes. That keeps install cards honest and shorter.
  Done when: in a fixture repo with a nightly dependency-update workflow, the dependency-watch trigger is proposed as `redundant: renovate` and not offered.

- **Honour OS focus, screen lock and screen-share state** — FEATURE — value 3 — effort M — risk med — category: attention
  Why: the pack covers quiet hours and "defer while mid-flow" by inferring from timestamps. It does not read the real signals: Do Not Disturb, session lock, or an active screen share (PipeWire/portal). Notification text also gets two classes, lock-screen-safe (no repo or task names) and full.
  Done when: with a mocked screen-share flag, a fired note is written to the morning file only, and the lock-screen text contains no repo name.

- **Keep tick credentials in the OS keyring, off disk and env** — SECURITY — value 3 — effort M — risk med — category: secrets
  Why: assumption: watchers need forge tokens, and the pack only says "check read-only". The tick starts with no credentials and a watcher fetches its single token from the keyring (`secret-tool`/Keychain) only for its own poll. A child lane never inherits it.
  Done when: a test dumps the environment of a spawned lane and finds no token. A watcher with no keyring entry fails with a named `no-credential` outcome.

- **Divide the tick's time slice fairly across registered repos** — FEATURE — value 3 — effort S — risk low — category: scheduling
  Why: "Tick every registered repo" is in the pack, but a busy repo can starve the rest inside one fixed tick budget. Round-robin with per-repo carry-over, plus a lowest-recent-service-first ordering, makes each repo's staleness bounded.
  Done when: with 5 fixture repos and a budget for 2 jobs, every repo is served within 3 ticks and the ledger shows the order.

- **Scaffold a trigger and its test in one command** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the pack has the 30-line watcher contract and CI event packs, but they are separate pieces. `fm triggers new NAME` would write the rule line, a fixture event, an expected-outcome file and a twin (see above). The pass/fail run then works on day one.
  Done when: after the command, `fm triggers test NAME` runs red-then-green on the generated fixture with no edits.

- **Export tick metrics as a Prometheus textfile** — FEATURE — value 2 — effort S — risk low — category: observability
  Why: the pack covers OpenTelemetry (opt-in) but not the zero-dependency path. A `foreman_tick.prom` file (last tick age, fires, outcomes, lateness) works with node_exporter's textfile collector or a user's own `watch cat`.
  Done when: after a tick, the file exists with `foreman_tick_last_success_timestamp` and per-outcome counters that parse with a Prometheus text parser.

- **Wild: let commit trailers schedule follow-ups** — FEATURE — value 4 — effort M — risk med — category: triggers
  Why: wild. The pack has `fm:` marker comments. A trailer such as `Fm-After: 3d run full suite` or `Fm-When: CI-green on main, ship` lives in git history, travels across machines and harnesses, and needs no state file or install. Any session or tick path can read it.
  Done when: a commit carrying a trailer produces a dated pending follow-up in `fm next`, and amending it away removes the follow-up.

- **Wild: trigger on network and power context** — FEATURE — value 2 — effort M — risk low — category: triggers
  Why: wild. VPN connected, home vs office SSID, AC plugged in or lid opened are cheap local signals the pack's "machine-state events" don't name. Heavy work such as exams waits for AC power and a home network. A "back at my desk" fire runs the return-to-work briefing.
  Done when: with a mocked power-source change from battery to AC, a queued heavy job starts within one tick and is logged with `reason: ac`.

- **Wild: record forge events from the repo side as ground truth** — FEATURE — value 4 — effort M — risk med — category: measurement
  Why: wild. Grading self-triggering today leans on Foreman's own ledger. A committed, opt-in GitHub Actions workflow that does no work and only appends timestamped issue, PR and CI events to a `fm-events` branch gives an independent record for lead-time and missed-event grading even while the machine is off. It is an outward push, so it needs a per-repo yes.
  Done when: against a fixture event log, `fm exam` computes the share of events a tick noticed within 1 hour, and it differs from the self-reported fires.

- **Wild: reconstruct a missed fire after the fact** — FEATURE — value 3 — effort M — risk low — category: catch-up
  Why: wild. The pack coalesces missed schedules to one catch-up run. A retroactive evaluation also asks what each missed tick would have found, using timestamped git and forge history. "CI went red 03:12 and went green 04:40 on its own" is reported as a flake and not as a task, and "red since 03:12" is reported as a task.
  Done when: after a simulated 12-hour gap with a transient red CI, the catch-up note labels it `self-healed flake` and files no task.

Next question: what does a self-started result look like when it is correct but unwanted, and is there any signal besides a revert that records the user's indifference?
Next question: which self-triggering claim in the README or site could the repo-side event record disprove, and who checks it?
