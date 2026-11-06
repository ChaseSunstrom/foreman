# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Scan the forge for automation that already does the job** — FEATURE — value 4 — effort S — risk low — category: overlap
  Why: assumption: much of Mission 6 (CI and issue watchers, dependency installs) duplicates Dependabot, Renovate, scheduled Actions and assignable forge agents. Earlier ideas retire verbs after the host ships them, but none looks at the user's own repo first.
  Done when: in a repo with `dependabot.yml`, `sampo trigger add deps` refuses with "already covered by dependabot.yml" and the reason is in the ledger.

- **Step aside when another agent owns the issue** — FIX — value 3 — effort S — risk low — category: collision
  Why: assumption: the issue watcher can race a forge-native agent or a human assignee. Done when: an issue assigned to anyone (human or bot) or labelled `bot-handled` is skipped, and the skip is logged with the assignee.

- **Eject triggers to standalone scripts** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: the user wants overnight progress; if Sampo vanished tomorrow, the triggers should keep firing. Earlier ideas compile to timers, but each fire still calls Sampo. Done when: `sampo trigger eject` writes a systemd unit plus a shell script that runs with `PATH` stripped of `sampo` and still starts the headless agent with the brief text.

- **Write briefs as plain prompts that any agent can run** — CLEAN — value 3 — effort S — risk low — category: portability
  Why: briefs and Exams are Sampo-shaped, so an obsolete Sampo strands them. Done when: every triggered brief renders to one markdown file that `claude -p`, Codex and Gemini accept unchanged, tested with a fixture.

- **Bid each background job to the cheapest executor** — FEATURE — value 4 — effort M — risk med — category: routing
  Why: the user asked for unlimited local use for background volume, and T-0793 lists cloud routines as a later option. Done when: for a sample job, `sampo route --explain` prints bids from local, headless Claude and a cloud routine (cost, expected pass rate, latency), and the lowest passing bid runs.

- **Report morning value in one number: unattended progress per dollar** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the stops and failed-call rates are inputs, not the goal the user stated. A single number lets any mechanism, including a rival one, replace Sampo's. Done when: the morning card shows tasks closed with a verified Exam divided by spend, with a 7-night trend, from existing ledgers.

- **Run placebo nights (wild)** — FEATURE — value 3 — effort M — risk med — category: evidence
  Why: nobody has measured whether the user needs triggered work at all. On a random 1 night in 7, triggers draft but hold their results. Done when: after four weeks, `sampo outcomes` shows the share of held drafts the user redid by hand versus the share of landed ones they kept.

- **Publish results as forge comments and branches, with no Sampo needed to read them** — FEATURE — value 3 — effort M — risk med — category: surface
  Why: a result that lives only in Sampo's pane dies with Sampo. Done when: a triggered fix appears as a branch plus a PR comment with the command output quoted, and removing the plugin leaves it fully readable.

- **Probe for the host's native schedule at startup and defer to it (wild)** — FEATURE — value 3 — effort M — risk med — category: host drift
  Why: assumption: the host will add routines or an events API. Done when: a fake host that exposes a `schedule` verb makes `sampo doctor` print "native available, Sampo trigger X now redundant" and offer a one-key switch.

- **Hold a "manual week" drill (wild)** — FEATURE — value 3 — effort S — risk low — category: evidence
  Why: no trigger has earned its slot against doing nothing. Done when: turning all triggers off for 7 days writes a digest of what the user did by hand that a trigger would have done, per trigger.

- **Keep a growing list of triggers that fired but changed no outcome (wild)** — FEATURE — value 3 — effort S — risk low — category: pruning
  Why: noise-producing triggers are what users turn off first. Done when: a trigger with 10 fires and zero landed results is auto-parked, and its row shows in the web UI with an "unpark" action.

- **Run Mission 6's acceptance suite against a bare scheduler** — FEATURE — value 3 — effort M — risk low — category: baseline
  Why: the arm that decides obsolescence is plain cron plus `claude -p` on the same overnight queue. Done when: `sampo exam` reports both arms on the same scenarios, with Sampo's lead (or lack of one) shown first.

- **Park a trigger whose gate never stopped anything** — CLEAN — value 3 — effort S — risk low — category: pruning
  Why: the Ward and done-gate are the core. If they never intervene in triggered sessions, the trigger layer needs only the scheduler. Done when: a 30-day empty "gate stopped" ledger flags that trigger in `sampo doctor`.

Next question: if the user's overnight queue ran entirely on a host-native scheduler, which of Sampo's checks would they still miss by morning, and where is that recorded?
Next question: what share of triggered work did the user simply ignore at the first read, and does any ledger separate "ignored" from "not yet seen"?
