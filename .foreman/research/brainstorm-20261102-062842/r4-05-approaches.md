# Brainstorm — lens: approaches

- **Pin every tick grade to its clock class and refuse a pooled number** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: assumption: replay, session-edge, CI and real-timer ticks will all write rows, and one blended "tick precision" would let the free replay arms flatter the live ones. The pack's "form-only gauges" blind spot is the same failure.
  Done when: `fm doctor` prints n and the grade per clock class, and a test feeding a mixed ledger fails if any single aggregate line appears.

- **Run one tape through all drivers in `fm tick lab`** — FEATURE — value 5 — effort M — risk low — category: self-triggering
  Why: assumption: the existing candidates (virtual clock, session-edge lazy tick, null-tick arm, held-out share) are each graded separately. A shared recorded tape means any difference between drivers is caused by the driver, not by different inputs.
  Done when: one command replays a fixed tape through the session-edge, null and replay drivers and prints a single table of fires, lateness and held-out delta, identical on two consecutive runs.

- **Turn the deferred "later: needs…" items into the first free live sample** — FEATURE — value 4 — effort M — risk low — category: grading
  Why: the open work lists about 30 deferrals (T-0788…T-0869) that each name a wake condition in prose. Giving them machine-checkable predicates and replaying the repo history shows when each would have woken. That compares against when the user actually reopened it, with no install needed.
  Done when: `fm tick lab --deferrals` lists each deferral with its would-have-woken date and the user's actual touch date, for at least 10 of them.

- **Ladder the install ask: counterfactual card, 20-second rehearsal, then a 7-day self-removing trial** — FEATURE — value 4 — effort M — risk med — category: onboarding
  Why: the user hasn't installed the timer in a week of waiting (the gen-2 gap). Separate asks for the pitch, a transient-unit proof and a trial are each in the list; chained, each rung needs a smaller yes and a decline is remembered.
  Done when: a test walks all three rungs against a fake `systemd-run`, the trial unit removes itself, and a declined rung is not re-asked until the evidence changes.

- **Make the session-edge tick the default clock and the timer a promotion** — CLEAN — value 4 — effort M — risk med — category: approach
  Why: a tick that runs at Stop, SessionStart and the first prompt of a local day already works without installing anything. The timer then becomes an upgrade whose benefit is the measured lateness gap between the two.
  Done when: `fm doctor` shows the session-edge tick as live with no timer installed, and the timer card quotes median lateness with and without it, taken from the ledger.

- **Choose the tie-break for "useful" before any data arrives** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: assumption: with no live week, "useful" will otherwise be defined after seeing the results. A pre-registered rule (a fire is useful if the user acted on it or reverted nothing within N days, with n/a when the user was away) avoids that.
  Done when: the rule is a committed file, grading code reads only that file, and changing it after the first graded run is flagged in `fm doctor`.

- **Pair every tick job with a do-nothing baseline measured from the same tape** — FEATURE — value 4 — effort M — risk low — category: grading
  Why: the pack's control-arm steers (a free arm beating the session arm is a top gap) apply here. Without the baseline, "the tick helped" can't be told apart from "the user would have noticed anyway".
  Done when: each job's grade is printed as a delta against the null arm, and a job whose delta is not above noise is marked "no evidence".

- **Do less: grade only "a due job ran within its window" for two weeks** — CLEAN — value 3 — effort S — risk low — category: scoping
  Why: that is the one claim every driver can prove without a user present. Usefulness is deferred until a live sample exists, and the site claims shrink to match.
  Done when: the README and site wording about self-triggering cites only the on-time rate and its denominator, and the sweep fails any stronger claim.

- **Reuse the exam scaffolding by adding a tool-less child that plays the clock** — FEATURE — value 3 — effort M — risk med — category: exam
  Why: the standing rule says exam scenarios come from a separate tool-less child. Given a week of event rows and the trigger table in English, it says what should fire, and the real tick is scored against that blind answer.
  Done when: `fm exam` has a "trigger" kind whose scenarios were written without the code, and the result reports agreement with the tick per scenario.

- **Wild: book the human tick** — FEATURE — value 2 — effort M — risk med — category: surfaces
  Why: assumption: for some jobs the user's own session start is a better clock than a timer. Foreman proposes a 10-minute "tick slot" at the user's habitual start and measures whether showing up beats not showing up.
  Done when: a slot is offered once, its outcome (attended or skipped) is recorded, and the tick lab compares attended and skipped slots.

- **Wild: ship the tick tape as the bug report** — FEATURE — value 3 — effort S — risk low — category: support
  Why: a redacted tape of inputs, decisions and clock class lets a stranger or a cold child reproduce a misfire with no state access, and each reported misfire becomes a regression tape.
  Done when: `fm tick tape --redact` writes a file that replays to identical decisions in a clean directory, with paths and secrets scrubbed.

- **Wild: a falsification bounty each generation** — FEATURE — value 3 — effort M — risk low — category: assurance
  Why: assumption: the Seed already lists "break the claim" adversaries in general terms. Making it a standing item gives the tower a fixed question each generation: find a tape where the tick lies.
  Done when: each Seed files one task for a cold child to produce a failing tape, and the result is recorded as found or not found with the attempts listed.

Next question: Which of the user's current repos have due items today that no session would have touched, and what does that backlog look like in their own minutes?
Next question: When a grade comes from partial data (no live week), where does `fm doctor` say so, and would the user notice if it didn't?
