# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Compile triggers to the OS's own timers and path units** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: Request asks for schedules and file triggers. systemd user timers and `.path` units already do both. Sampo would write `triggers.toml` into unit files and run no daemon, which also removes a source of "drive stopped".
  Done when: `sampo trigger apply` creates a user timer and a path unit, the Sampo process is not running, and touching the watched file starts a headless session.

- **Replay 30 days of history through proposed triggers before enabling** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: Failed tool calls rose by half and drive stops appeared, so an unvalidated trigger is risky. Git log, CI runs and issues already hold the events.
  Done when: `sampo trigger dry-run RULE --days 30` lists what would have fired, with the count and the closest human action taken within 24h.

- **Tag each fired run "would have happened anyway"** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: A trigger is obsolete if the user does the work first. Assumption: commits and issue closes within 24h can be matched by file overlap.
  Done when: the trigger ledger shows a per-rule share of runs preempted by the user, shown in `sampo doctor`.

- **Suspend triggers whose output nobody takes** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: Unattended work only counts if it is merged or read. Standing rule: capabilities must earn their keep.
  Done when: a rule whose last N runs went unmerged and unopened for 14 days is suspended, and the morning card says so.

- **Add a tool-failure budget to trigger-born sessions** — FIX — value 5 — effort S — risk low — category: reliability
  Why: Failed tool calls are up by half, and an unattended session can burn the night retrying. Assumption: failure counts are readable from hook events.
  Done when: a seeded run with 5 consecutive tool failures ends with a "could not run" record and a retry deferred to the next window, not looping.

- **Run a nightly trigger-set duel against plain `claude -p`** — FEATURE — value 4 — effort M — risk med — category: obsolescence
  Why: The inversion lens. If the host's cron or routine produces equal accepted output, Sampo's layer for that trigger kind is dead weight. This builds on the earlier idea of a quarterly duel by running per trigger, nightly, and keeping a cost.
  Done when: `sampo exam triggers` prints per-kind accepted-output rates for both arms, using local models in the bare arm to cost nothing.

- **Label the cloud-routine alternative per rule** — FEATURE — value 3 — effort S — risk low — category: triggers
  Why: T-0793 defers cloud routines, and CI and issue watchers need no laptop if they run in the forge. Each rule should state whether it needs local models or local files, and if not, offer to export it as a forge workflow.
  Done when: `sampo trigger list` shows a "needs this machine: yes/no, because…" column.

- **Break-even gate for local versus hosted background volume** — PERFORMANCE — value 4 — effort M — risk low — category: local models
  Why: The user wants unlimited local volume, but a model switch costs about 3 minutes and hosted small models get cheaper. The current batching ideas don't compare against hosted price.
  Done when: for a queued batch, a recorded line says "local: X min, Y accepted; hosted: $Z" and routing follows the cheaper path with a stated reason.

- **Queue installs as one signed manifest diff** — SECURITY — value 3 — effort M — risk med — category: installs
  Why: The request says installs are "queued for one yes". Assumption: a package-manager-native hook could replace this later, so the manifest should be a plain list any installer can consume.
  Done when: all queued installs show as one list with source, hash and the trigger that wanted each, and one yes applies all or none.

- **Wild: Write the shutdown notice for each trigger on day one** — FEATURE — value 3 — effort S — risk low — category: obsolescence
  Why: Wild. Every trigger is created with a 30-day expiry and a stated "this becomes unnecessary when…" line, for example when the host ships it. A cold child checks the line against host release notes.
  Done when: a trigger with no retire-when line is refused at creation.

- **Wild: Mine shell history to propose triggers, then retire them when habits stop** — FEATURE — value 4 — effort M — risk med — category: unspoken needs
  Why: Wild. The user's recurring manual commands are the real trigger list. Assumption: shell history is readable locally and never sent anywhere.
  Done when: Sampo proposes three triggers from a week of history with the evidence lines, and drops one after the habit is absent for 21 days.

- **Wild: Publish triggers as an open event→brief spec with a conformance test only** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: Wild. If Sampo's real product is the rules and checks, any harness should be able to run them. Sampo ships the test suite and a reference runner for Codex, Gemini CLI and opencode, and no more.
  Done when: one trigger file passes the conformance test on two different agent CLIs.

- **Wild: A sealed morning bet** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: Wild. Before sleep, Sampo writes "by 7am, N triggers fire, M merge" and grades itself in the morning. Repeated misses lower how much work it takes on.
  Done when: the morning card shows forecast versus actual and the next night's cap changes accordingly.

Next question: If the user disabled every trigger for a week, which would they ask to switch back on first, and does the ledger already say?
Next question: Which trigger-born commits were reverted or rewritten by hand within a day, and what do they share?
