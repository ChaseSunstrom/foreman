# Brainstorm — lens: reliability

- **Run the tick in time slices with a cursor** — PERFORMANCE — value 4 — effort M — risk med — category: tick
  Why: without an install the tick rides hook invocations, which have a latency budget and a timeout (assumption: a hook kill mid-tick is the likeliest silent failure). Each invocation does at most about 150 ms of work, then persists a step cursor, so a killed hook loses one slice instead of the whole pass.
  Done when: a test kills the hook at a random slice 50 times, and every job still completes within N sessions with no duplicate effects.

- **Write every job as a level-triggered reconcile** — CLEAN — value 5 — effort M — risk low — category: design
  Why: missed ticks are the core no-install problem, and an edge-triggered job ("on this event, do X") loses the event for good. A job that compares desired state to actual state each run self-heals after any gap.
  Done when: a lint fails any tick job that has no pure `desired(state)` and `actual(state)` pair, and a test skips 20 ticks in a row and gets the same end state as no skips.

- **Fail over unattended lanes across providers** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: assumption: a usage limit, outage or expired login on the primary harness looks like silence overnight. The tick retries the same brief on the next harness in a user-set chain (claude, codex, gemini, `fm code`), flags the receipt "ran on fallback", and never retries a brief the guard blocked.
  Done when: with the primary harness stubbed to fail, a fixture fire completes on the second harness and the receipt names both.

- **Preflight the unattended environment and record the cause** — FIX — value 4 — effort S — risk low — category: tick
  Why: the pack's "could-not-run" idea has no list of causes. Before spawning a lane the tick checks git state, the interpreter, network, free space on the children dir, and whether the login is still valid (a short read-only probe). A failure becomes `could-not-run: auth-expired`, not a missing result.
  Done when: five faults injected one at a time each produce a distinct logged cause, and `fm doctor` shows the latest.

- **Detect dirty session exits and catch up** — FIX — value 3 — effort S — risk low — category: tick
  Why: session-edge ticks fire on Stop, and a crashed or killed session never fires it. SessionStart writes an "open" marker and compares it with the last "closed" one, and an orphan marker counts as a missed edge that triggers a catch-up tick and a ledger line.
  Done when: killing a fixture session with SIGKILL makes the next SessionStart log `dirty-exit` and run the catch-up exactly once.

- **Give watcher cursors an overlap window and dedupe by identity** — FIX — value 4 — effort S — risk low — category: watchers
  Why: assumption: a high-water mark stored as a timestamp loses events that arrive late and duplicates events that arrive twice. Re-read the last K minutes each poll and dedupe on the source's own id.
  Done when: a fake forge that delivers events out of order and twice yields exactly one capture per event.

- **Run a cold-start tick smoke on every release** — SECURITY — value 3 — effort S — risk low — category: tick
  Why: the first tick on a fresh clone with empty ledgers and no config is the case no week of live data ever covers, and a bootstrap bug would look like "self-triggering doesn't work". `fm ship` runs it in a scratch HOME with no network.
  Done when: the release gate fails if that tick throws, writes outside the scratch dir, or emits no beat file.

- **Test the runbooks by running them** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: assumption: a doctor warning that points at prose rots. Each warning links to a generated runbook whose repair command is executed in a deliberately broken fixture in CI.
  Done when: every warning code has a fixture, and CI fails if the runbook's command leaves that warning still firing.

- **Print a verify line on every self-started result** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: it answers the open question "what would a one-line external check cost". Each fire's receipt ends with a `verify:` command that uses only git, gh or the repo's own test runner, so the user never has to trust `fm` to check `fm`.
  Done when: every fixture fire's receipt has a verify line that exits 0 when run in a clean shell without `fm` on PATH.

- **Set a freshness SLO per tick job and show its burn** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: "measurable without the install" needs a target, not only a lateness number. Each job declares a max staleness, and `fm doctor` shows the share of the last 14 days spent inside it, so the no-install world gets a score now.
  Done when: replaying a recorded tape with session-only ticks prints a per-job percentage, and a deliberately starved job shows red.

- **Wild: Skip real ticks at random to prove the alarm works** — FEATURE — value 3 — effort S — risk low — category: tick
  Why: wild. About 1% of real ticks deliberately skip one job and log "planned skip". The next session must show the overdue alarm for it, and a missing alarm is itself filed as a failure. This tests the alarm path under real use and not only in drills.
  Done when: a seeded planned skip is followed by an overdue notice within one session, and a silenced notice makes `fm doctor` warn.

- **Wild: Triangulate time from three clocks** — SECURITY — value 3 — effort S — risk low — category: tick
  Why: wild. Compare the system clock, the newest commit time and the beat file's mtime. If they disagree by more than a threshold (a dead RTC battery or a restored snapshot), time-dependent jobs refuse to run and say which clock looks wrong.
  Done when: a fixture that sets the system clock six months back makes due-time jobs report `clock-suspect` and spawn nothing.

- **Wild: Bisect a tick regression across golden tapes** — PERFORMANCE — value 3 — effort M — risk med — category: measurement
  Why: wild, and a mechanism for "name the commit behind a drop". `fm tape bisect` replays a frozen tape over the git history and returns the first commit where the useful-fire rate or lateness crossed a threshold, so a regression is found without waiting for another live week.
  Done when: a commit with a planted off-by-one in due-time logic is named by the bisect in a fixture repo.

Next question: if the whole tick layer is level-triggered and sliced, which of today's jobs still need an event payload that cannot be recomputed from state, and what is lost for those when a tick is missed?
Next question: for the user who never installs the timer, what is the longest gap between sessions in their own history, and does any job's freshness target fall inside it?
