# Brainstorm — lens: blind spots

Blind-spot questions asked of the whole project, grounded in the eight missed asks (T-2534 to T-2566). Each idea names the question behind it. Everything here runs without the user installing a timer.

- **Make the tick a pure function with an injected clock** — FEATURE — value 5 — effort M — risk low — category: testability
  Why: Question: "what part of unattended work can't be observed without waiting?" The pack shows live-tick grading waiting on the user's install (T-2542 came after the fact). Assumption: the tick currently reads the wall clock and live state directly.
  Done when: `fm night tick --as-of <ts> --state <snapshot> --json` prints the same decisions twice, and a test steps it through 7 simulated days in under 10 seconds.

- **Grade ticks by lateness against a session-borne baseline** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: Question: "who runs the tick when the timer doesn't?" Session hooks can run due tick work when the last beat is stale. Each row records `due_at`, `ran_at` and `source` (timer or session). The lateness distribution is the measurable stand-in for a week of live ticks.
  Done when: `fm doctor` prints median and worst lateness split by source from at least 20 rows, and a test shows a session start running a due item exactly once.

- **Hold out 10% of eligible fires to measure causal value** — FEATURE — value 5 — effort M — risk med — category: evaluation
  Why: Question: "how would we know the tick caused the outcome rather than the user doing it anyway?" Bets give a Brier score but no control arm; the standing rule asks for control arms. Assumption: a skipped fire can be logged as a counterfactual row.
  Done when: skipped fires are recorded with `holdout=1`, and `fm outcomes --by trigger` shows the user-did-it-manually-within-24h rate for held-out versus fired.

- **Add a tool-less-child timeline exam kind for self-triggering** — FEATURE — value 5 — effort L — risk med — category: exam
  Why: Question: "what grades self-triggering other than Foreman's own fixtures?" The standing rule requires scenarios from a child that never sees the code, and the task says it's unmeasured until the final exam. The child writes event timelines (CI red at 02:00, a stale issue, a usage-limit wait) with the expected act or abstention; the sim tick plays them and scores precision, recall and lateness.
  Done when: `fm exam run --kind trigger --agent free` scores 12 child-authored timelines at zero tokens and prints precision, recall and lateness per timeline.

- **Rehearse the install with a transient unit before asking for it** — FEATURE — value 4 — effort M — risk med — category: install
  Why: Question: "what does the user find out only after installing?" Assumption: `systemd-run --user --on-active=30s` exists as an uninstall-free probe. The rehearsal fires once and records linger state, PATH, environment and exit status. It needs a one-time grant because it starts a process outside the session.
  Done when: `fm night rehearse` fires a harmless transient timer, reports "would run / would not run, because X", and leaves no unit file behind.

- **Treat unreviewed tick output as unseen, not dropped** — FIX — value 4 — effort S — risk low — category: user model
  Why: Question: "what do unattended acts write that learners read as the user's own signal?" This is the T-2554 class. A tick-filed task the user never opened should not count as a rejection in the dropped ledger or the foresight negative model. Assumption: expiry currently maps to "dropped".
  Done when: a task with `origin=tick` and no user touch expires as `unseen`, and a test shows `fmforesight` excludes it from its negatives.

- **Mine transcripts for the user's waits to rank triggers** — FEATURE — value 4 — effort M — risk low — category: discovery
  Why: Question: "which of the user's idle gaps does Foreman not know about?" Long gaps after a red test, a usage-limit pause or a CI wait show where an unattended start would have saved real hours. This differs from the shell-history habit mining already proposed.
  Done when: `fm triggers waits` lists the top 5 gap types with total hours from the last 30 days of transcripts and the trigger each one would map to.

- **Ask what each decision procedure does on partial input** — CLEAN — value 4 — effort M — risk low — category: reliability
  Why: Question: "which selectors return keep or no-decision when half their inputs are missing?" T-2566 (select ignoring held-out-only lines) is one instance. Sweep the tick, sweep, select, bets and outcomes. Each must emit one of `decided`, `abstained (n of m inputs)` or `failed`.
  Done when: a table-driven test feeds each procedure empty, half and full inputs and fails any that returns a bare keep.

- **Put a one-line external check on every self-started result** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: Question (carried over): "which output does the user act on without checking anything outside Foreman?" A tick-filed fix or note carries a `check:` line, a command that uses no Foreman code (for example `git log -1 --stat X` or `gh run view N`).
  Done when: every tick-filed item has a `check:` line that a test runs and finds exits 0 on a good fixture.

- **Test premises against a held-out clock** — FIX — value 3 — effort S — risk low — category: reliability
  Why: Question: "what does a first-time scenario assume that a reused one doesn't?" The T-2334 and T-2606 style premise fixes show tests built on a fixed state. Run each tick test at day 0, day 8 and after a 3-day gap.
  Done when: the tick suite runs under three simulated starting states and all pass.

- **Wild: Play the tick tournament** — FEATURE — value 3 — effort L — risk low — category: evaluation
  Why: wild. Race an interval scheduler, an event-driven one and a session-borne one over the same recorded week; the scoreboard is lateness, cost and kept results. It answers "which design" with data before any install.
  Done when: `fm night tournament --week <id>` prints one line per scheduler with lateness, spend and kept results.

- **Wild: Hatch a tick-egg on the status line** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. It shows 🥚 until the first self-started result the user keeps, then changes to the hard hat with a count. It answers "did anything happen while I was away?" at a glance and marks the first real proof of self-triggering.
  Done when: the status line shows the egg with zero kept results and the hat after one, driven by the ledger.

- **Wild: Replay last Friday evening as a ghost shift** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: wild. Show the user what the tick would have done during their real last offline stretch, with the diff it would have prepared and the `check:` lines. That makes the value visible before any install yes.
  Done when: `fm night ghost --since "last friday 18:00"` prints a timeline of would-have-acted items, each tied to a real commit or CI run.

Next question: Which Foreman component keeps working in a degraded way for weeks because no session path ever reads its output, and what's the cheapest signal that would expose it?
Next question: For each self-trigger decision, who would notice if it were wrong for a month, and what is their one-line check?
