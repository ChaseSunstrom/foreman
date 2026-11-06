# Brainstorm — lens: deepen: triggers

- **Make one trigger table, one tick, one output** — FEATURE — value 5 — effort M — risk med — category: triggers
  Why: the category list converges on this: a single rules file read by `fm night`'s tick, whose only output is a capture (never running work). Evidence: the night tick already exists and logs only on events; `fm triggers` already groups captures by trigger with precision. Assumption: the tick can read the file cheaply, within the hook budget.
  Done when: `fm triggers list` prints every armed rule from one file, and a test shows a schedule, a file change and a CI failure each producing exactly one capture with the rule id.

- **Shadow-arm every new trigger and replay it before the install yes** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: Mission 3's lesson was that ideas had no failure behind them. A trigger is grounded only if it would have fired on real history. Event logs and `fm ci-watch` history exist. Assumption: 30 days of events are retained.
  Done when: `fm triggers arm R` shows "would have fired N times, M led to a task the user kept" and refuses to queue the install yes when N is 0.

- **Score every trigger by acted-on rate and quarantine the ignored** — FEATURE — value 4 — effort S — risk low — category: triggers
  Why: `fm triggers` already computes precision per trigger. Closing the loop (a trigger below its floor over 10 firings goes to quarantine, logged with the reason, never silently deleted) matches the "only proven harm removes an idea" steer.
  Done when: a test with a rule whose last 10 captures were dropped shows it quarantined, and `fm doctor` names it with its precision.

- **Give each trigger a budget, debounce and storm breaker** — FEATURE — value 4 — effort S — risk low — category: triggers
  Why: file and git events burst (a checkout touches thousands of files). Assumption: no debounce exists today for file triggers.
  Done when: a simulated 500-file event burst yields one envelope and one capture, and a rule over its daily budget logs "suppressed" instead of firing.

- **Watch the watchers from outside the session** — FEATURE — value 4 — effort M — risk med — category: triggers
  Why: the open question "is a guard that never fires alive or silent?" applies to timers too. The night tick logs only on events, so silence is ambiguous. Assumption: a tiny heartbeat line per tick is acceptable.
  Done when: `fm doctor` distinguishes "tick ran 288 times, nothing to do" from "tick has not run for 2h", and a killed timer is reported within one interval.

- **Fire on machine state, not only clocks** — FEATURE — value 3 — effort M — risk med — category: triggers
  Why: Assumption: users want "when the usage window resets", "when on AC power and idle", "when a backend finishes downloading". The pack shows usage-limit waits and pace already tracked, so those states are readable.
  Done when: a rule `on usage-reset` produces a capture the first tick after a recorded limit ends, in a test with a fake clock.

- **Seed suggested triggers from stack cards and the repo's own CI** — FEATURE — value 3 — effort M — risk low — category: triggers
  Why: 1219 stack cards exist; manifests reveal the CI config, lockfiles and audit tools. Suggestions would go through the one-yes install queue. Assumption: cards can carry a small `triggers:` field.
  Done when: in a fixture repo with a lockfile and a GitHub workflow, `fm triggers suggest` proposes a lockfile-change rule and a CI-failure rule, each shown with its replay count.

- **Promote a trigger from capture to action only on earned precision** — FEATURE — value 4 — effort M — risk high — category: triggers
  Why: the pack's autonomy steers (initiative, never idle) want work to start unattended, yet the standing rule on risk keeps outward actions behind a yes. A ladder (capture, then draft task, then started lane) earned by acted-on rate keeps that balance.
  Done when: a rule at 90% acted-on over 20 firings is offered a one-yes promotion, and an unpromoted rule can never start a lane (tested).

- **Make `fm night`'s tick report one digest line per day** — FEATURE — value 3 — effort S — risk low — category: triggers
  Why: the user sees triggers only when they act. A single morning line ("7 fired, 2 kept, 1 quarantined, 0 stuck") makes the system's aliveness visible without noise.
  Done when: the nightly digest contains that line, and it is omitted on days with zero rule activity.

- **Wild: `fm when "<sentence>"` compiles a sentence into a rule line** — FEATURE — value 4 — effort M — risk med — category: triggers
  Why: wild. "When CI fails on main, file a task" becomes one line in the plain trigger file, shown back for one yes. Parsing is a tool-less Haiku call with the rule grammar as a closed schema, falling back to a refusal when it can't map it.
  Done when: five sample sentences each compile to the expected rule line, and an unmappable one is refused with the grammar shown.

- **Wild: mine standing orders from the user's own steers and repeated asks** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: wild. The steers list repeats patterns ("after every push, watch CI", "before each Seed, run the cross-cutting review"). Detect a request typed 3+ times and offer it as a rule with the replay count.
  Done when: on the recorded steer history, `fm triggers mine` proposes at least one rule, each citing the messages that justify it.

- **Wild: a trigger that fires on its own absence** — FEATURE — value 3 — effort M — risk low — category: triggers
  Why: wild. "No ship in 7 days", "no exam run since the last capability merge", "inbox untouched for 3 days" are dead-man rules, which fit the open question about silent guards and unfired standing rules.
  Done when: a rule `absent ship 7d` fires once in a test with a fake clock and a ship record 8 days old, and not again until a new ship resets it.

- **Wild: a trigger rehearsal page on the web UI** — FEATURE — value 3 — effort M — risk low — category: triggers
  Why: wild. The web UI is the only surface. A timeline shows each rule's would-fire and did-fire marks over 30 days, with empty/quarantined/storm states, so the user sees the system's behavior before granting a yes.
  Done when: the page renders a fixture's three rules with distinct states and a screenshot test passes.

Next question: Which triggers does a real session path actually call (per the reach check), and do any trigger verbs exist that no session or tick ever invokes?
Next question: When a trigger's output lands in the capture inbox, does `--round-first` hold it back so that the user never sees the rule working?
