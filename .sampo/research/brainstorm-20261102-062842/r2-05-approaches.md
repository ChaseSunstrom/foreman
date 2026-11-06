# Brainstorm — lens: approaches

- **Tick every registered repo from any Foreman session** — FEATURE — value 4 — effort M — risk med — category: triggers
  Why: assumption: the pack shows session-borne ticks only for the current repo, while the user works across many repos. Any session start or stop would run due ticks for all repos in the project registry under a time cap. That cuts lateness with no timer. The trade-off is hook latency and touching repos the user isn't in, so it files captures only.
  Done when: with two fixture repos and no timer, a session in repo A makes repo B's overdue trigger fire once, and the lateness ledger records source `peer-session`.

- **Compute lead-time potential from CI and git timestamps** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the gap is "unmeasured until the exam", and the repo already holds event timestamps (CI red, issue open) next to task-creation timestamps. For each closed task, take the hours between the earliest detectable event and the human start. That table is a usefulness measure needing no install and no live week. The trade-off is that it measures potential, not realised value.
  Done when: `fm tick leadtime` prints per-trigger-family median hours earlier, with n and the baseline named, from the last 60 days of history.

- **Mutation-score the trigger layer** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: assumption: the planted-event and replay arms exist or are proposed, but nothing shows they would notice a broken trigger. Flip each condition, threshold and debounce in a scratch copy, and require a red result from the replay or contract arms. The survivors list shows where "measured" is false comfort. The trade-off is runtime, so run it in the night tick.
  Done when: a report lists mutants killed and survived per trigger, and a deliberately weakened debounce is reported as a survivor until a test kills it.

- **Stamp every fire with an input digest and replay it** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: assumption: today a fire is only graded after the fact, and "why did this fire?" can't be re-run. The fire row stores the inputs it decided on (events, clock, steers hash). `fm tick replay ID` re-decides offline and must match. That makes every live fire a reproducible exam item and a shareable bug cartridge.
  Done when: replaying a stored fire on a clean checkout gives the same decision, and a tampered input digest is reported as a mismatch.

- **Write executable trigger contracts** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: assumption: the proposals so far grade outcomes but never state what a trigger promises. Each trigger gets a small file with a "fires when" fixture, a "must not fire when" fixture (user present, over budget, own output) and its expected output kind. Contract pass rate is measurable at once and `fm doctor` can show it per trigger. The trade-off is fixture upkeep.
  Done when: every registered trigger has at least one fire and one must-not-fire fixture, and `fm doctor` WARNs on a trigger with none.

- **Prove driver equivalence across session, replay and timer** — FEATURE — value 3 — effort M — risk med — category: measurement
  Why: assumption: grading the session-borne tick says nothing about the timer the user hasn't installed. Run one event tape through the session driver and the replay driver, and render the timer unit and check its calendar with `systemd-analyze calendar` (no install). Require identical decisions. A match lets the grade of one driver carry to the others. The trade-off is that it can't prove the real scheduler fired.
  Done when: one tape gives identical decision lists on all drivers, and a seeded divergence fails the check.

- **Fuzz the dispatcher with forged events and invariants** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: assumption: self-made events, duplicate fires and fires while the user is present are the likely failures, and fixed fixtures won't find the unexpected ones. Generate random ledger and event states on an injected clock. Assert: no double fire, no fire while present, budget held, no loop on own output. Shrink any failure to a minimal case.
  Done when: 1,000 seeded runs pass, and a planted bug (fire on own output) is caught and shrunk to under 10 events.

- **Calibrate the cold-read grader with planted labels** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: the standing rules lean on cold reads, and the pack proposes a cold child grading the week's fires. Without a check, a lenient judge turns "graded" into noise. Mix labelled good and bad fires into the tape, score the judge's agreement, and publish it beside every grade.
  Done when: the tick scorecard shows judge agreement on the planted set, and a judge below 80% marks every grade "unreliable".

- **Run the tick on a stock-sh shim** — CLEAN — value 2 — effort M — risk med — category: portability
  Why: do-less approach. Hardened or odd hosts, like this one, can fail the Python hot path or the unit's environment. A 60-line POSIX script does only the due-check and the capture-filing, and the full tick runs when a session exists. The trade-off is two implementations to keep equal.
  Done when: the shim and the Python tick give identical due sets on the fixture tape, and a CI check fails if they diverge.

- **Rig a real systemd in a container** — FEATURE — value 3 — effort L — risk high — category: devices
  Why: assumption: the real scheduler is the one thing the install-free arms can't test, and a transient timer on the user's host is still a footprint. A rootless container with systemd runs the real unit at 60x compressed intervals. The trade-off is that the hardened kernel may block it, so fall back to skip with a named reason.
  Done when: a 10-minute run shows the unit firing on schedule in the container and leaves nothing on the host.

- **Wild: Model the no-install world with a queueing fit** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild. Fit the user's session-start times to an arrival process and predict expected tick lateness p50 and p95 for session-borne ticks. Then check the forecast against the realised lateness ledger. This gives the install pitch a prediction that can be wrong in public.
  Done when: `fm tick forecast` prints predicted lateness, and after 14 days a line shows the forecast against actual.

- **Wild: Heckle the tick with a blind adversary** — FEATURE — value 3 — effort M — risk low — category: exam
  Why: wild. A tool-less child sees only the trigger contracts and writes a week of events meant to cause misfires, such as lookalike CI text and bursts. Every misfire becomes a permanent contract fixture. The trade-off is child cost, kept under the current budget by running it only at generation end.
  Done when: one heckler run yields at least one new failing fixture or a recorded "no misfire found" with its event count.

- **Wild: Ride git's own housekeeping as a clock** — FEATURE — value 2 — effort S — risk med — category: triggers
  Why: wild, assumption: git's `pre-auto-gc` hook fires when git does automatic housekeeping in a repo, and the user's repo is where the work happens. Add a repo-local hook (no timer, no user-level unit) that runs the due-check. It is weaker than a timer because auto-gc fires irregularly, so the lateness ledger labels the source.
  Done when: after a forced `git gc --auto` in a fixture repo, a due trigger fires once with source `git-housekeeping`.

Next question: Which trigger families have event timestamps in git or CI history precise enough to compute lead time, and which have none?
Next question: If the user never installs the timer, which of these arms still count as "measured" in the end-of-run report, and what would gen-0 call that?
