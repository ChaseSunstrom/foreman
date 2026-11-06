# Brainstorm — lens: bold bets

- **Grade each trigger with a Bayesian posterior seeded from the replay tape** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the stated gap is that a week of live ticks can't be graded without the install. A replay tape gives a prior, and each real edge fire (session start/stop, `fm` verbs) updates it. This assumes the replay tape from earlier ideas exists or gets built.
  Done when: `fm exam tick` prints, per trigger family, a posterior mean and a 90% interval. A test that appends one live fire to a fixture ledger changes the numbers, and the interval narrows.

- **Stop grading early with a sequential test that names the evidence still missing** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: assumption: live fires are sparse, so a fixed-week design wastes time. A sequential probability ratio test returns pass, fail or "need ~N more fires" as soon as the data allows.
  Done when: a 1,000-run simulation at a known fire-keep rate reaches a verdict within the expected sample count with under 5% wrong verdicts. `fm doctor` prints "need N more" for an undecided trigger.

- **Keep a measurement-debt ledger: which arm grades each capability today** — FEATURE — value 4 — effort M — risk low — category: tower
  Why: the request says self-triggering stays "unmeasured until the end-of-run exam". The standing "lean substance" rule only handles growth without a measurement, not the reverse. Each capability would name its current arm (free, Haiku, live, none) and its age.
  Done when: `fm genesis sweep` has a measurement-debt row that goes red when a capability shows "none" for more than one generation. A fixture with one such capability proves it.

- **Drill the undo of every self-start nightly in a scratch clone** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: this answers the earlier question about the first hour after an unattended mistake. An undo that has never run is an unchecked output. The drill replays the undo for the last N fires in a scratch copy and compares tree hashes.
  Done when: `fm night` reports "undo verified for K of K fires". A planted fire with a corrupt undo bundle shows as failed in a test.

- **Run a cheap due-check on every PostToolUse so long sessions still tick** — FEATURE — value 4 — effort S — risk med — category: clock
  Why: edge ticks at session start and stop starve a six-hour session. A stat-only comparison against the next-due timestamp costs almost nothing. Risk: the hook latency gate, which `plugin/tests/bench_hooks.py` already enforces.
  Done when: a simulated three-hour session with no start or stop event fires a due job within one tool call of its due time. The `bench_hooks.py` p95 delta is under 1 ms.

- **Wild: duel Claude Code's native scheduled tasks on the same planted week** — FEATURE — value 4 — effort L — risk med — category: exam
  Why: the existing control arms are a do-nothing arm and a one-line cron. The honest rival is the host's own scheduler. The exam would run a planted-event week through both and score lead time and keep rate. Assumption: the host exposes a scriptable scheduler.
  Done when: one scorecard shows Foreman's edge tick and the native-scheduler arm on identical planted events, with lead time per event class.

- **Interleave two trigger policies in one fire stream to pick cadence and thresholds** — FEATURE — value 3 — effort M — risk low — category: tuning
  Why: A/B comparison needs weeks of data. Interleaving alternates which policy chooses each fire and credits whichever one the user acts on, so it converges on far fewer events. Assumption: two candidate policies exist for some job.
  Done when: a simulation with a known better policy picks it in at least 90% of 200 runs using under half the events a split test needs.

- **Compare event-to-notice latency across the user's repos with and without edge ticks** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: the user's other repos on disk, where no session runs, are a free control group. The comparison is difference-in-differences on CI-red-to-first-touch time. Assumption: more than one repo is registered.
  Done when: `fm exam tick --cohort` prints median notice latency for ticked and unticked repos. A two-repo fixture with a planted gap shows the expected difference.

- **Score "acted on" by echo: does the user's next prompt reuse the note's phrases?** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: this answers "which outputs does the user act on without checking". Clicks don't exist in a terminal, but transcripts do. Phrase overlap between a fire's note and the user's next three prompts is a no-install proxy for being read.
  Done when: a fixture transcript pair scores high for an echoed note and near zero for an ignored one. `fm outcomes` shows an echo rate per trigger.

- **Wild: breed new triggers by genetic search over the replay tape** — FEATURE — value 3 — effort L — risk med — category: discovery
  Why: assumption: triggers are small specs (event, filter, action, budget), so a search can mutate them and score each against the tape. A cold read then explains why a survivor works. The result is triggers nobody wrote. This goes beyond tuning thresholds on existing ones.
  Done when: on a fixture tape with a planted precursor pattern, the search proposes a spec matching it. It beats the do-nothing baseline on held-out weeks.

- **Wild: let the user's phone report presence through a LAN shortcut to the local web UI** — FEATURE — value 2 — effort M — risk med — category: surface
  Why: assumption: "at the desk, away, asleep" is the fact the tick lacks, and a phone Shortcut that taps a local endpoint is the cheapest sensor. It must stay opt-in and LAN-only, with nothing leaving the hardware.
  Done when: with the setting off, the endpoint refuses. With it on, a tap changes the tick's hold-fires state, and a test shows the state expiring after a set time.

- **Wild: publish the tick scoreboard as a living benchmark with its own cheating test** — FEATURE — value 3 — effort L — risk med — category: exam
  Why: the standing rule demands signals Foreman didn't author. The scoreboard would ship the planted-event generator and a deliberately cheating tick (it reads the answer file). A scoreboard that can't flag the cheater is invalid.
  Done when: the benchmark scores the cheating tick as invalid. Both the honest tick and the do-nothing arm score as valid.

Next question: Which self-triggering measure could be inflated by tasks the tick files and Foreman then closes itself, and what ratio would show it?
Next question: When the user installs the timer later, what is the first number they would want to see, and can the pre-install arms already produce it?
