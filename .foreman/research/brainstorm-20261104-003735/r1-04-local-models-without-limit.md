# Brainstorm — lens: local models without limit

- **Add a local triage gate in front of every trigger** — FEATURE — value 5 — effort M — risk low — category: triggers
  Why: Mission 6 starts work without the user, and local compute is free but frontier turns are not. Every file, CI and issue event is first classified by a local decision model (Jev, systemone) into ignore, dedupe, file or wake.
  Done when: a replay of 100 recorded events shows ≥90% dropped or merged locally, and each wake carries a one-line local reason.

- **Run triggers as systemd user timers and path units, not a resident process** — FEATURE — value 4 — effort M — risk low — category: scheduling
  Why: assumption: a daemon is one more thing that silently dies, and the drive stops are already a symptom of that. `sampo schedule add` writes a declarative unit that fires `sampo trigger run NAME` once and exits.
  Done when: killing every sampo process still lets a path-unit fire the trigger on the next file change, and `sampo doctor` lists the units.

- **Add a free lane with no budget cap** — FEATURE — value 5 — effort M — risk med — category: local models
  Why: the user wants local models "without limit" for background volume. Task kinds such as lint triage, doc-claim extraction, cold-read pre-passes and brainstorm volume get a lane class whose spend is metered in seconds of GPU, never in dollars, and whose output is never trusted without a check.
  Done when: a task flagged `lane=free` runs with the paid budget at $0, and the ledger shows GPU-seconds and the check that accepted it.

- **Order the night's local work by resident model** — PERFORMANCE — value 4 — effort S — risk low — category: scheduler
  Why: the pack says a llama-swap switch costs about 3 minutes and /running isn't relayed. The scheduler groups queued jobs by model, runs the 27B first and swaps once at a recorded point.
  Done when: a 40-job night with two models shows exactly one swap in the log.

- **Repair malformed tool calls locally before they fail** — FIX — value 4 — effort M — risk med — category: reliability
  Why: failed tool calls are up by half. A grammar-constrained local repairer fixes the JSON/arguments of Smith-on-local calls, retrying once before the call reaches the host.
  Done when: on the recorded failed calls, ≥50% are repaired and pass, with a before/after failure rate in `sampo louhi`.

- **Run a drive sentry on the local model** — FIX — value 5 — effort M — risk low — category: drive
  Why: drive stops appeared (0 to 0.1) and T-2873/2901 show the running-set logic keeps misjudging. A cheap local check every 5 minutes compares the drive's heartbeat, live OS processes and the queue, then resumes or records a typed stop reason.
  Done when: a planted phantom hold is released within 20 minutes and the stop appears in the morning card with its cause.

- **Draft CI-red fixes in a scratch worktree overnight, held for one yes** — FEATURE — value 5 — effort L — risk med — category: CI watcher
  Why: the CI/issue watchers in the request are only useful if the red build is already fixed by morning. A local Smith reads the log, attempts the fix, runs the repo gates and leaves a branch plus a verdict, never pushed.
  Done when: a seeded failing test gets a branch with a green gate run and an unmerged card in `fm next`.

- **Batch every install a trigger needs into one yes card** — FEATURE — value 4 — effort S — risk low — category: installs
  Why: the request says installs are queued for one yes. A local pre-check reports licence, size and checksum for each, so the single approval is informed.
  Done when: three queued installs show up as one card, and one approval installs all three.

- **Replay 30 days of history through a trigger before enabling it** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: assumption: an unattended rule that fires 400 times is the worst failure. `sampo trigger dry-run` prints what would have fired, with estimated GPU-seconds and paid turns.
  Done when: enabling a trigger is refused if its replay exceeds the stated caps.

- **Race several local attempts at each new issue and keep the best passing one** — FEATURE — value 4 — effort L — risk med — category: issues
  Why: GPU time is free, so redundancy beats quality. Three lanes with different scaffolds run the same Exam, and only a passing result is surfaced.
  Done when: for a seeded issue, the report names the winning scaffold and shows the two losers' Exam output.

- **Wild: Compile plain-sentence triggers into rules with a local model** — FEATURE — value 3 — effort M — risk med — category: triggers
  Why: wild. The user says "when CI goes red on main, try a fix"; the local model writes the rule file and a replay test, and the rule is live only if the test passes.
  Done when: one sentence yields a rule plus a passing dry-run, with no hand-written YAML.

- **Wild: Run a dream shift that mines closed tasks for the follow-up the user would have asked** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: wild. Idle GPU runs brainstorm lenses over each day's closed tasks and files only ideas that pass a wildness and duplicate filter, matching the user's complaint that moons weren't wild enough.
  Done when: the morning card lists ≤5 candidates, each with its source task and the nearest existing item.

- **Wild: Yield the GPU the moment the user shows up** — FEATURE — value 3 — effort M — risk low — category: local models
  Why: wild. Keyboard, session or display activity pauses background generation so the user's own model gets the endpoint; the paused job resumes at idle.
  Done when: starting an interactive session suspends the queue within 10 seconds and resumes it afterwards.

- **Mark every local-made result unwitnessed until verified** — SECURITY — value 4 — effort S — risk low — category: trust
  Why: unattended output from small models must not reach main. A local result carries a status that only an Exam run or a frontier check can upgrade, and ship refuses unwitnessed commits.
  Done when: `fm ship` rejects a commit authored by a free-lane task that has no verified Exam.

Next question: which background tasks does the user actually accept from a local model with no review, and does the ledger show that?
Next question: what does a trigger do when the endpoint is down or mid-swap at 3 a.m., and who finds out?
