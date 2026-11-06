# Brainstorm — lens: delight

- **Echo every capture in under 100 ms** — FEATURE — value 4 — effort S — risk low — category: intake, speed
  Why: Foreman captures new requests instead of chasing them, but the user only learns it landed after the model's turn. Assumption: the UserPromptSubmit hook can print one deterministic line before the model starts. The classifier is already regex-first and hooks are measured at ~35 ms.
  Done when: submitting `FIX: x` prints `captured T-NNNN FIX · queued behind T-MMMM` in the hook output, and `bench_hooks.py` shows that path under 100 ms p95.

- **Turn gate waits into a review tour** — FEATURE — value 4 — effort M — risk low — category: waiting, review
  Why: gates and the reviewer already leave the user idle for minutes. Related ideas cover filling the *model's* wait time, not the human's. During a long `fm check` or `fm task finish`, the pane or Artifact shows the task's diff in dependency order with one-line explanations, so the wait becomes the review.
  Done when: while a gate is running, `fm tour` prints the ordered diff summary. Finishing a task with the tour opened records that it was viewed.

- **Sleep until the usage window resets, and say so** — FEATURE — value 4 — effort S — risk low — category: unattended, quota
  Why: long drives hit plan limits. Assumption: the reset time is readable from the statusline JSON or the limit error. Instead of stalling, Foreman parks the queue, sets a title like `💤 resumes 14:00 · 4 queued`, schedules one wake at that time, and resumes at the exact step.
  Done when: a simulated limit error produces a parked state with a resume time, and a fake clock past that time fires exactly one wake.

- **Give every sub-agent a delegation slip** — FEATURE — value 4 — effort M — risk low — category: agents, legibility
  Why: the agents area is thin, and delegation is opaque to the user. For each child spawned, store a 6-line slip: the brief given (3 lines) and what came back (3 lines). Name it in the band and open it with `fm slip ID`. This is a surface for the work, not a new gate.
  Done when: after a lane or reviewer runs, `fm slip <lane>` prints the brief and return, and each slip is under 600 chars.

- **Hold a lane huddle before parallel launch** — FEATURE — value 3 — effort S — risk low — category: agents, fleet
  Why: `fm run --parallel` starts lanes with no human-readable plan. Before launch, print 3 lines per lane (goal, files it may touch, model/effort, ETA from history) with one key to go. Skip it for a single lane.
  Done when: `fm run --parallel 2` shows the huddle and waits for confirmation, and `--yes` skips it.

- **Print the answer line first, details after** — PERFORMANCE — value 3 — effort S — risk low — category: perf, CLI feel
  Why: perf is thin, and slow `fm` verbs feel slower than they are. Every verb prints its one-line answer immediately, then streams the detail. Assumption: `fm map` and `fm doctor` buffer their whole output today.
  Done when: for `fm doctor` and `fm map`, time to first stdout byte is under 150 ms, enforced by a bench case.

- **Surprise me: a gift diff from the deferred pile** — FEATURE — value 3 — effort M — risk med — category: delight, backlog — wild
  Why: 13+ deferred and captured tasks sit idle. When the queue drains and the user is away, Foreman picks the smallest low-risk deferred task, does it in a lane, and leaves it as one reviewable diff. A single key keeps or discards it, and the choice is logged as taste signal. This differs from spending leftover budget silently because the user gets a wrapped, optional result.
  Done when: an empty queue plus an idle flag produces exactly one gift lane. Discard leaves the main tree untouched.

- **Keep a time-debt ledger of Foreman's own mistakes** — FEATURE — value 4 — effort M — risk low — category: trust, ritual — wild
  Why: the user keeps relaying false positives and bugs (guard false positives, the `exit N` miss, empty-diff closes). When one is fixed, Foreman writes a one-line apology with an estimated cost (`cost you ~6 min, fixed T-0812`) and the greeting shows a running "owed vs repaid" tally. Assumption: the cost is estimated from the ledger's timestamps between report and fix.
  Done when: closing a task tagged as a Foreman bug adds a ledger line with minutes. `fm debt` prints the total.

- **Throw back requests that just became cheap** — FEATURE — value 4 — effort M — risk low — category: memory, unspoken needs — wild
  Why: the user said "etc. etc. etc.", and dropped and deferred ideas carry a reason. When a newly shipped task removes that reason (for example, LSP arrives or the mod update unblocks), the next greeting says `You asked about X in October; it's now an S`. This is a delight version of reactivation triggers, aimed at the user rather than the queue.
  Done when: a deferred task with `unblocked_by: T-N` surfaces once in the greeting after T-N closes, and not again.

- **Run a crew roll call in the agents' own voices** — FEATURE — value 2 — effort S — risk low — category: agents, personality — wild
  Why: agents (reviewer, recon, builder) have stats but no presence. `fm crew` prints one first-person line each: `reviewer: idle. 3 findings upheld this week, 1 waved off.` It reuses data Foreman already records and adds no new store.
  Done when: `fm crew` prints one line per installed agent from ledger data and exits in under 300 ms.

- **Name each round, and put the name on the title and tag** — FEATURE — value 2 — effort S — risk low — category: ritual, identity
  Why: the user steers in rounds ("recursively improve"), but round 1 and round 2 are only numbers. Derive a one-word name from the dominant cluster (`Round 2 · Liveness`) and use it in the session title, the commit trailer and the catalogue page heading.
  Done when: `fm research show` and the session title include the derived name, and it is stable across reruns.

- **Quiet-hours acknowledgement for hands-off stretches** — FEATURE — value 3 — effort S — risk low — category: unattended, calm
  Why: after "leave unattended" or a long ask-free run, the user returns not knowing what was deliberately deferred. When Foreman parks a question with a default, it adds one line to the return greeting: `3 parked: defaults applied, tap to change`. Assumption: parked asks already record their default.
  Done when: the greeting lists parked asks with their defaults, and changing one re-queues the affected task.
