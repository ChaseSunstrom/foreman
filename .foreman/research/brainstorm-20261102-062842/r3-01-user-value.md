# Brainstorm — lens: user value

- **Trust a repo's triggers by hash before any edge tick honors them** — SECURITY — value 5 — effort S — risk low — category: security
  Why: assumption: the lazy tick runs at SessionStart/Stop in whatever repo the user opens, and the pack has the committed `triggers.toml` idea but nothing about an untrusted clone declaring triggers. The pack's open "untrusted checkout" ideas cover only the guard.
  Done when: a fixture clone with a hostile `triggers.toml` fires nothing on SessionStart until `fm trust` records its hash. Editing the file revokes trust, and `fm doctor` lists the repos that are trusted.

- **Time-slice the edge tick with resumable checkpoints** — PERFORMANCE — value 4 — effort M — risk med — category: performance
  Why: the gates include `bench_hooks.py`, and T-2605 compares median wall time on a loaded bench. A tick that piggybacks on Stop/SessionStart must never spend more than a few ms there, so heavy jobs should run in slices and resume at the next edge.
  Done when: with a 50 ms slice cap, a 400 ms job completes across several edges. Per-edge added p95 stays under the cap in `bench_hooks.py`, and a kill mid-slice resumes without redoing finished steps.

- **Replay the last tick tape through old and new code on every upgrade** — FIX — value 4 — effort M — risk low — category: developer experience
  Why: assumption: tapes exist once tick replay lands, and `fm release` and `fm ship` already gate on suites. The incident class is "the upgrade silently changed what fires", which is invisible to unit tests.
  Done when: `fm ship` prints the fires that differ between the previous release and the working copy on the newest tape. A deliberately altered due-time rule shows up as a named diff.

- **Match synthetic weeks to the user's real activity histogram** — FEATURE — value 4 — effort M — risk med — category: agents (wild)
  Why: wild. One recorded week grades only that week, so a generator draws weeks from the user's own session-timestamp distribution (hours, gaps, weekends) with planted events. Self-triggering can then be graded across hundreds of plausible weeks with no install.
  Done when: `fm exam` runs N generated weeks with a fixed seed and reports fires, lateness and useful-fire rate with a spread. Two runs with the same seed give identical output.

- **Shrink a dropped fire to its minimal triggering event** — FEATURE — value 3 — effort M — risk low — category: developer experience (wild)
  Why: wild. Delta-debug the event envelope and repo state until the smallest input that still fires is left. The user then sees "this fired because of X alone" instead of a log, and the same shrunk case becomes a regression tape.
  Done when: `fm why FIRE_ID --shrink` outputs an event with at most 3 fields that reproduces the fire. That case is saved under the exam fixtures.

- **Require a birth tape before any new tick job may arm** — CLEAN — value 4 — effort S — risk low — category: docs
  Why: the "Later from T-07xx" bundles show jobs accumulating with no measure. A job that ships a tape is graded from its first commit and documents itself by example.
  Done when: registering a job without a tape plus an expected-fires file fails `fm check`. `fm doctor` lists existing jobs without one.

- **Show the cost of the unmeasured week in the user's own minutes** — FEATURE — value 5 — effort S — risk low — category: user value
  Why: the gap is "a week of live ticks graded waits on the user's install". Session-start staleness already gives a no-install baseline, so name it: "3 things sat 41 h before a session noticed", from the user's own ledgers.
  Done when: SessionStart prints one line with real figures when staleness exceeds a threshold, and nothing otherwise. The same figure is the first row of the tick scoreboard.

- **Poison the tick's own inputs weekly with a hostile fixture repo** — SECURITY — value 4 — effort M — risk low — category: security (wild)
  Why: wild. The pack says issue and CI text is untrusted, but no check shows the tick holds up. A fixture repo with injected issue text, a symlinked state dir, a huge ledger and a forged beat file runs through the tick each night.
  Done when: the nightly digest reports "hostile fixture survived" or names the failing vector. A planted bypass turns it red.

- **Write a one-page "what runs without you" doc from the live registry plus the user's tape** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: assumption: the docs describe triggers generally, but the user needs to see what runs on their machine. The page lists each job, its edge, its last fire and what it touched, and is rebuilt on every change.
  Done when: `fm doctor --docs` regenerates the page, and a test fails if the page lists a job the registry doesn't have or omits one it does.

- **Hand the lazy tick to the specialist sub-agent that fits the job** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: assumption: tick jobs currently run as one dispatcher. A router can send "red CI", "stale deferral" and "dependency advisory" to cheap, scoped lanes with the caps and checks already in the pack.
  Done when: a planted red-CI event produces a lane with a per-job spend cap and a landed `night/` branch. The same event run twice produces one lane.

- **Run the tick in a "quiet receipt" mode that proves what it did not do** — FEATURE — value 3 — effort S — risk low — category: user value (wild)
  Why: wild. Silence reads as dead. Each edge tick writes one line ("checked 6 sources, 0 due, 0 spent, 0 files touched") that the status line can show on demand.
  Done when: after any edge tick `fm tick --last` prints that line. A test confirms the user's working tree hash is unchanged.

- **Decay a trigger the user hasn't read in three weeks** — FIX — value 4 — effort S — risk low — category: user value
  Why: assumption: unread output is the cheapest failure to miss. A job whose results go unopened should go quiet and ask once whether to keep it.
  Done when: a job with 3 weeks of unopened output stops filing captures and adds one yes-card. A single read restores it.

- **Let a recorded tick tape double as a bug-report attachment** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the pack lists redacted-tape export. The second-order value is that a maintainer can replay the user's exact week on a virtual clock without access to the repo.
  Done when: `fm tick --export` yields a tape with paths hashed and text redacted. Replaying it on another machine reproduces the same fire list.

Next question: Which of the user's tick fires would they have caught themselves within an hour anyway, and how would we know without the install?
Next question: What does the user do when a self-started result is wrong at 3 a.m. with no session open, and which of those steps still have no verb?
