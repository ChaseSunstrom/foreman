# Brainstorm — lens: 2030 worked back

- **Classify every event's author before it can start work** — SECURITY — value 5 — effort M — risk low — category: triggers
  Why: assumption: by 2030 most issues, PRs and CI comments are agent-written. The pack fences trigger text as data, but nothing separates a human issue from an agent-generated one. Each event gets a class (human / known-agent / bot / unknown), taken from forge metadata and the commit trailer in Sampo's own unattended commits. Each class maps to a grant tier.
  Done when: a fixture issue authored by an unknown agent starts a read-only diagnosis lane, and the same issue from the owner starts a build lane. Both outcomes are in the ledger.

- **Split each night's budget fairly across repos** — FEATURE — value 4 — effort M — risk low — category: scheduling
  Why: assumption: the user has several repos (Sampo, jarvis, site). One noisy repo's CI-red watcher could eat the whole local-model night. The allocator weights repos by the share of past overnight output the user accepted, and keeps a floor for each repo.
  Done when: a replay with one repo producing 10x the events leaves every other repo at least its floor of runs.

- **Print a measured "minutes returned" receipt in the morning card** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: the user wants overnight progress, but nothing says what it was worth. For each landed unattended result, find the closest closed task in history by kind and size. Show its median hands-on time as the estimate, with the range, and mark accepted against discarded output.
  Done when: the card shows "N accepted, ~X min (range)" computed from ledger rows. A run whose output was discarded counts zero.

- **Run a schedule conformance suite for DST, suspend and clock jumps** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: schedules that read fine in 2026 misfire across DST changes, laptop sleep and NTP steps. The suite uses fake clocks. It asserts exactly-once firing per intended slot and a single catch-up after a resume.
  Done when: tests cover spring-forward, fall-back, an 8-hour suspend and a backwards clock step, and none produces a double or a dropped fire.

- **Generate "what runs while you sleep" from the live registry and fail on drift** — CLEAN — value 4 — effort S — risk low — category: docs
  Why: docs are listed as thin. A hand-written trigger list rots. Render one page from the trigger file: each trigger's source, grant tier, model route, budget and last result. Add it to MASTER.md's index.
  Done when: changing a trigger without regenerating the page fails the doc check, and the page has no hand-typed trigger names.

- **Keep a weekly data-flow ledger of which model saw which bytes** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: privacy is listed as thin. Local models get unlimited background volume, but triggers also escalate to frontier models. Log per fire: model route, byte count, and the path classes sent (source, issue text, secrets-scrubbed). Roll these up into a weekly local-versus-sent summary.
  Done when: one command lists, for any fire, whether any bytes left the machine. A planted secret-shaped string never appears in a sent-bytes record.

- **Version the trigger file and test its migration against a frozen fixture** — CLEAN — value 3 — effort S — risk low — category: durability
  Why: the Foreman→Sampo rename shows names and shapes change under users. A trigger file written today must still load in 2030. Stamp a schema version and add a migration chain with a committed 2026 fixture.
  Done when: the fixture loads at HEAD through the chain and the fire decisions match the golden file.

- **Load-test the trigger intake with a synthetic agent-authored flood** — PERFORMANCE — value 3 — effort M — risk low — category: triggers
  Why: assumption: event volume rises sharply once agents file their own issues and PRs. Generate 10k mixed events in a scratch spool. Measure intake latency, queue depth and local-model saturation, and confirm the debounce and loop breaker hold.
  Done when: the run reports p95 intake time and the number of runs started, and the number started stays under the declared cap.

- **Seed starter triggers from the repo's existing automation** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: nothing in the pack says how a stranger gets a first trigger. Scan CI workflow files, Makefile and package scripts, and the user's cron or timers. Propose a trigger for each (red main, nightly tests, dependency audit), shown as a dry run and enabled only on a yes.
  Done when: on a fixture repo with a CI file, the proposals name each job and nothing is enabled until confirmed.

- **Wild: Publish a 7-day forecast calendar of expected unattended work, then grade it** — FEATURE — value 3 — effort M — risk low — category: user value
  Why: wild. Project from the schedules, the CI cadence and past event rates what each trigger will probably do. The user can strike a slot before it happens. Each week the forecast is scored against what ran, and the miss rate is shown.
  Done when: the calendar lists projected fires with counts, and the next week's report prints forecast against actual.

- **Wild: Run a monthly "sabbatical night" in observe-only mode and compare with what the user did by hand** — FEATURE — value 3 — effort M — risk med — category: evidence
  Why: wild. One night a month every trigger drafts but lands nothing. The next day, match the user's own commits and tasks against the drafts. The match rate shows whether the triggers are earning their keep.
  Done when: the report gives per-trigger overlap between draft and user action, and it lists triggers with zero overlap as retirement candidates.

- **Wild: Add a "lighthouse" wake path through a small always-on box** — FEATURE — value 3 — effort L — risk med — category: surfaces
  Why: wild, assumption: the workstation sleeps and the local models live on it. A tiny always-on device (a Pi or the router) holds the schedule, wakes the workstation with Wake-on-LAN, hands over the night's briefs, and sleeps it again afterwards. It uses no cloud.
  Done when: with the workstation suspended, a scheduled trigger wakes it, runs one scratch task, and returns it to sleep. The wake and the result both appear in the ledger.

Next question: Which of these triggers would the user still enable if every run's output arrived with no estimate of its worth, and what in the ledgers shows they read the output at all?
Next question: When the host ships native scheduling and events, which part of the trigger layer (the spec, the gate, the ledger or the budget) has no host equivalent, and is that the only part worth keeping?
