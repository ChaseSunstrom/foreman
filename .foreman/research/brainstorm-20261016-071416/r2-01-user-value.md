# Brainstorm — lens: user value

- **Gate measured claims on before/after numbers** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: the queue and past ideas are full of PERFORMANCE and cost claims (hook latency, import cost). The 80 ms import-cost brief was dropped because cProfile's figure was wrong, so unmeasured claims have already cost a task. Assumption: `fm task finish` can tell a perf-type task.
  Done when: a PERFORMANCE task claiming a speedup is refused at finish unless a stored before and after measurement from the same command is attached. A test with a fake timer shows both outcomes.

- **Preview a contract against the queue** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: `fm contract --until --usd` shipped (T-1158), but the user is AFK and can't tell beforehand what will fit. Assumption: closed-task history gives a usable cost and time estimate per task.
  Done when: `fm contract --plan --until 06:00 --usd 10` lists which queued tasks fit and which would be left out and why. A test with a seeded ledger gets the expected split.

- **Score the mission's pillars at the end** — FEATURE — value 4 — effort S — risk low — category: reporting
  Why: this mission has 7 pillars and a "final report" pillar, but nothing maps them to evidence. The user would otherwise have to trust a prose summary. Assumption: pillars can be stored as a checklist at mission start.
  Done when: the final report has one row per pillar (done, partial or not done) with a link to the task, commit or screenshot. A test with one pillar lacking evidence marks it "not done".

- **Break repeated-action loops on the main thread** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: lane tripwires exist as ideas, but the weak-model standing ask suggests the main thread also loops (the same failing call, the same `cd` retry). Assumption: tool-call shape plus identical results is detectable in the PostToolUse hook.
  Done when: replaying a recorded transcript with the same failing Bash call three times injects one "change approach" line with the last distinct error. A control transcript injects nothing.

- **Step down to cheaper capacity at the budget edge** — FEATURE — value 4 — effort M — risk med — category: cost
  Why: a `--usd` contract currently means stop. For an AFK user, finishing mechanical tasks on a cheaper or local model beats idling. Assumption: tasks carry a mechanical flag or size S.
  Done when: with a fake spend meter at 90% of the budget, the drive picks only S or mechanical tasks and routes them to the cheap tier. At 100% it stops and prints the receipt.

- **Merge overlapping open briefs** — CLEAN — value 3 — effort S — risk low — category: queue
  Why: the queue has T-0788 to T-0799 and T-0826 to T-0832 "Later from…" briefs, many sharing themes (T-0794 and T-0862 to T-0864 both cover onboarding and slimming). Mission packs keep listing them. Assumption: text overlap is a good enough signal.
  Done when: `fm tidy` proposes merge groups for open briefs above an overlap threshold and applies one on `--apply`. A fixture with two near-duplicate briefs ends with one.

- **Demote stale "active" tasks at session start** — FIX — value 3 — effort S — risk low — category: queue hygiene
  Why: T-0275 is "active" among a deferred and blocked backlog, with no sign of current work. Active tasks that nobody touches mislead `fm next` and the pane. Assumption: ledger shows no event for it in N days.
  Done when: a task active with no ledger event for 3 days is moved to "paused" with a reason and shown in `fm todo` or the greeting. A test with a fake clock covers it.

- **Register a real-path probe per surface** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: pillar 5 asks to verify on the real path (browser, device) and not only in tests. Screenshot-gating exists for the pane only. Assumption: file globs map to surfaces.
  Done when: `fm surface add web --probe "<cmd>" --paths "ui/**"` is stored, and closing a task that touched those paths runs the probe and records its output. A test with a fake probe sees it run once and be skipped for unrelated edits.

- **Add one autonomy dial** — FEATURE — value 4 — effort M — risk med — category: settings
  Why: the user's standing asks are "no asking", "mechanical enforcement" and "token-cheap", yet they are spread across contract, guard, ceremony and lane settings. Assumption: a handful of presets can map onto the existing settings.
  Done when: `fm dial 0..4` sets named presets, printing every setting it changed and its before value. A test checks that each level is reversible.

- **Run a shadow round on a throwaway clone (wild)** — FEATURE — value 3 — effort L — risk med — category: autonomy
  Why: assumption: a clone is cheap with copy-on-write. A rehearsal would show what a round of tasks would touch, so the user can approve a bigger unattended run knowing what it does.
  Done when: `fm rehearse` runs the next N tasks in a clone, and the report lists the files changed, gates red or green, and the cost. The main checkout is byte-identical afterwards.

- **Draft the user's status update from closes (wild)** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: assumption: the user answers to someone (a boss, a client, or just their own memory). The ledger already holds what closed, what blocked and what was reverted, so a weekly update is a render.
  Done when: `fm standup --days 7` prints 5 plain-language lines from a seeded ledger and names nothing unverified as done.

- **Let the user type a phrase to widen or narrow a running contract (wild)** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: assumption: the user will want to change "until 06:00" mid-run from a phone without opening the repo. A mid-run steer file is already an idea, but a typed contract amendment with a receipt is new.
  Done when: writing `extend 2h` to the steer file moves the stop time, and the final receipt shows both the original and the amended bound. An amendment that raises the spend limit is refused unless it was pre-authorized.
