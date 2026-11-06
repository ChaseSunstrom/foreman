# Brainstorm — lens: bold bets

- **Borrow the tick from every session path** — FEATURE — value 5 — effort M — risk med — category: triggers
  Why: the week of live ticks waits on the user's timer install, and the standing rule says every capability must be called by a real session path. SessionStart, Stop, UserPromptSubmit and any `fm` verb run the overdue part of the `fm night` tick under a lock, and each ledger row records `source=borrowed|timer`. Assumption: the tick is idempotent and cheap enough to run inside the hook budget.
  Done when: with no timer installed, three simulated session starts spaced 3 hours apart write 3 tick rows with source=borrowed, the p95 hook bench stays within its ratchet, and `fm doctor` reports "ticks: 3 borrowed, 0 timer".

- **Record a tick tape and replay it on a virtual clock** — FEATURE — value 5 — effort L — risk med — category: measurement
  Why: the pack says self-triggering is unmeasured until the end-of-run exam. A tape of real hook events, commits and ledger writes, plus an injected clock, lets `fm night replay --days 7` run a week of ticks in seconds in a scratch copy. Assumption: hook events can be recorded without leaking secrets.
  Done when: replaying a recorded 7-day tape twice gives byte-identical fire lists, and each fire is graded "acted on within 7 days" from later git and task events.

- **Add a zero-token planted-event arm to the exam** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: standing rules require free arms before any session arm. A fixture repo with ground-truth events (red CI file, stale branch, expiring grant, usage-limit marker) is run under the virtual clock, and `fm exam` scores recall, precision and lead time for the trigger and watch families, with no model and no install.
  Done when: `fm exam run --agent free --kind trigger` prints per-family recall and precision over at least 20 planted events, and removing the dispatcher drops recall to 0.

- **Hold out a random share of fires to measure causal value** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: "acted on" alone can't tell a useful fire from work the user would have done anyway. About 1 in 5 eligible fires is withheld and logged as a shadow fire. `fm outcomes` compares the kept-rate of fired and withheld work. Assumption: the user accepts silently skipping some fires.
  Done when: the ledger holds fired and shadow rows with a seeded split, and `fm outcomes --by trigger` prints kept-rate for each arm.

- **Show an install counterfactual card** — FEATURE — value 4 — effort S — risk low — category: triggers
  Why: the user hasn't installed the timer and nothing shows what it would give them. Replaying their last 14 days of tape gives "a timer would have filed N tasks, caught M reds early and saved about X minutes". The yes-card then shows evidence instead of a request.
  Done when: `fm doctor` with no timer prints a replay-derived line with counts, and a test with a fixture tape asserts the numbers.

- **Mine existing unattended resumes as free live ticks** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the drive already waits out usage limits and the tower advances itself, so unattended wake-and-continue events exist today. Tag each as a tick-class event (waited N s, resumed correctly or not) and grade them as live data. Assumption: those events are logged with timestamps.
  Done when: `fm exam runs` or `fm doctor` lists resume events from the past 30 days, with the correct-resume rate.

- **Use the host's scheduler as the clock** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: T-0793 (cloud routines / remote lanes) is deferred, and a Claude Code or cloud routine that calls `fm tick` needs no systemd unit. The same shape works for Codex and Gemini via their own cron or loop features. Assumption: routines can run a shell tick, which is unverified.
  Done when: a routine definition is generated for each harness that supports one, and one real fire from it appears in the tick ledger as source=host.

- **Have a cold different-model child grade each night's fires** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: standing rules favour signals Foreman didn't author. A Sonnet or Haiku child sees only a fire's diff and trigger text and answers "would a maintainer want this?", so the grade is independent of Foreman's own outcome counts.
  Done when: each fire in the ledger gets a child verdict, and agreement with the user's keep/drop is reported once at least 20 are scored.

- **Make `fm doctor` say how much of the trigger path ran unattended** — FIX — value 3 — effort S — risk low — category: observability
  Why: the bet-settling tick is only visible as a timer's absence, and the lean row stays pending. Doctor shows borrowed vs timer ticks, the longest gap and tick debt (missed intervals) as one line with the omission stated.
  Done when: doctor prints a "tick debt" figure that drops to 0 after a borrowed tick, with a test for each state.

- **Wild: run a session-lived ticker with no unit files** — FEATURE — value 3 — effort M — risk med — category: triggers — wild
  Why: assumption: some users will never install a unit. A detached `setsid` loop with a pidfile and an 8-hour TTL ticks while the login lives, and removes itself with no residue; `fm eject` kills it.
  Done when: starting a session spawns one ticker, a second start reuses it, and after TTL no process or file remains.

- **Wild: a tick that follows the user's sleep** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: assumption: session gaps reveal the user's rhythm. Heavy fires are timed for the predicted idle window and held back when the user is mid-flow, and the morning card lists what ran.
  Done when: on a fixture history with a nightly gap, `fm night plan` places heavy work inside the gap and shows why.

- **Wild: replay a week in 60 seconds in the web UI** — FEATURE — value 3 — effort M — risk low — category: ui — wild
  Why: the tape replay already produces graded fires. A timelapse strip shows each tick, what woke, what was kept and what was withheld, so the user can judge self-triggering without waiting a week.
  Done when: the web UI page loads a tape, plays it with reduced-motion support, and lists each fire's grade.

Next question: which fires would the user act on without reading the evidence, and how would the tape tell kept from rubber-stamped?
Next question: what does a borrowed tick cost the user in hook latency and surprise, compared with a timer that runs while they're away?
