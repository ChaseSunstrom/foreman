# Brainstorm — lens: blind spots

Answers to earlier questions first.

- **Notice-when-missing outputs:** the eight missed asks (T-2533 to T-2554) share one shape: a gauge, timer or learner existed, but one input, dimension or liveness signal was missing. The user only learned this after it cost a task.
- **Cells that quietly depend on Claude Code:** assumption: any cell citing hook notes, PreToolUse or SessionStart injection. I can't verify this from the pack.

The question a brainstorm should have asked each time was "what does this thing not see about itself?" The ideas below apply that question to the whole project.

- **Enumerate every injection site, then require a ratchet row** — FEATURE — value 5 — effort M — risk low — category: lean
  Why: T-2533 and T-2535 both extended the lean ratchet one dimension at a time after the user noticed. Assumption: other emit points are still uncounted.
  Done when: a scan lists every place text is emitted into model context. `fm doctor` fails when one has no ratchet row, and a planted new emit fails the test.

- **Derive the learner-input taint graph from code** — CLEAN — value 5 — effort M — risk low — category: user model
  Why: T-2554 happened because the user model read Foreman's own captures. This was found by hand and no check exists.
  Done when: the sweep statically lists every ledger each learner reads and which writers feed it. It goes red if a Foreman-authored writer reaches a learner, and a test with a planted writer proves it.

- **Give every refusing verb a `--check` that the writer runs first** — FEATURE — value 4 — effort S — risk low — category: tower
  Why: T-2547 added a refusal at `fm genesis put`, which fires after a child has already spent its tokens on the Mission.
  Done when: each refusing verb has a dry-run mode, and the Mission writer's template calls it on its draft. A Mission with a missing grounding line fails before `put`.

- **Detect a repeated steer as an enforcement failure** — FEATURE — value 4 — effort M — risk med — category: steers
  Why: the user has restated rules several times, e.g. ship via `fm ship`, and the cold-read rule. A restated steer means its automatic check missed something. Assumption: this happens often enough to measure.
  Done when: a new user message matching an existing steer at a stated similarity bar files a task naming the steer and the check that failed to catch it. It passes a backtest on the steer history.

- **Build a silent-death inventory with one liveness row each** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: T-2542 covered only systemd timers. Night ticks, lanes, ci-watch, the web UI server and exam children can die the same way. Assumption: not all have liveness reads.
  Done when: one table lists every unattended process, its expected cadence and its last-seen time. `fm doctor` WARNs on any row missing a probe, and a killed child shows up stale.

- **Count a cell only if its cited path is reachable from an entry point** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: this answers "which outputs does no session path read". The sweep checks that a cited file exists, not that anything calls it.
  Done when: the import and call graph from hooks, `fm next` and the drive marks each cell's symbol reachable or not. An unreachable cell is red, with a test using a dead symbol.

- **Tag each cell with a harness-and-history class** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: this answers the two open questions on harness dependence and too little history. The cells don't record what they need to be measured.
  Done when: each of the 58 cells carries `harness: any|claude-only` and `backtest: measurable|plant-only`. The sweep prints the counts, and a cell without tags fails the lint.

- **Surface the commands the user types to verify Foreman** — FEATURE — value 3 — effort M — risk med — category: observability
  Why: T-2542 came from the user checking systemd by hand. Assumption: shell history is a legitimate local-only, opt-in source.
  Done when: with an explicit setting on, `fm night` lists repeated manual verification commands (`systemctl`, `git log`, `ls`) as candidate gauges, with nothing leaving the machine.

- **Wild: plant known blind spots in a fixture project and score the brainstorm** — FEATURE — value 4 — effort L — risk low — category: meta
  Why: wild. There is no recall number for brainstorming. Eight misses are anecdotes, but planted gaps (an uncounted emit, a polluted ledger, a dead timer) give a measurable rate.
  Done when: `fm ideas` run on a fixture with N planted gaps reports how many it named, and the score is recorded per lens.

- **Wild: disable one quiet output for a day and see if anyone notices** — FEATURE — value 3 — effort M — risk med — category: observability
  Why: wild. This is the only direct way to find outputs whose absence is invisible. It overlaps the earlier "silent day" ideas but adds a notice-test against the user's next messages. Assumption: it only works for non-safety outputs.
  Done when: a log shows which suppressed output the user mentioned within 24 hours, and the guard is never in the candidate set.

- **Wild: have a child write the follow-up asks from the closing diff alone** — FEATURE — value 3 — effort M — risk low — category: foresight
  Why: wild. A tool-less child sees only the diff and the close receipt, writes three follow-up asks, and is scored against the user's real next asks. Every miss becomes a blind-spot candidate.
  Done when: a nightly job reports hit rate and files each miss as a brainstorm seed.

- **Make every gauge declare its denominator and omissions in one line** — CLEAN — value 3 — effort S — risk low — category: gauges
  Why: the "Flag silent changes in what a gauge omits" ideas are scattered across the list and none is enforced. The lean gauges already needed a follow-up to say what they leave out.
  Done when: every `fm doctor` gauge prints `counts X, omits Y`, and a test fails on a gauge without it.

Next question: Which generated artifact has a producer and a validator that live in different tasks, so one can drift from the other?
Next question: Which of the user's eight misses would still be missed if the brainstorm had run on the pack as it stood before the miss?
