# Brainstorm — lens: approaches

- **Compile plans into programs with per-step pre/postconditions** — FEATURE — value 5 — effort L — risk med — category: planning
  Why: assumption: plans are prose steps; the recent "step evidence moves the current step" fix (T-0406) shows progress is inferred from evidence after the fact. A plan DSL where each step names a checkable precondition and postcondition would let Foreman advance, resume and verify steps itself.
  Done when: a plan with three steps runs under `fm`, a step whose postcondition fails stays current, and a deliberately broken step is flagged without the model reporting it.

- **Grade every proof on an evidence-strength ladder** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: assumption: done-gates check that evidence exists, not how strong it is. Rungs: asserted, ran an existing test, red→green reproduced, observed in the product via smoke, user-attested. Each task tier would require a minimum rung. This differs from vacuous-proof rejection because it ranks all proofs, not just filters the empty ones.
  Done when: `fm task done` on a FIX with only an "asserted" proof is refused, and `fm digest` shows the rung distribution for the week.

- **Estimate an instruction change's effect from old logs before running it** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: `fm evolve` and `fm bench` need replays or live runs to judge a change (T-0035 evals are still deferred). Off-policy estimation reweights the existing ledger of finished tasks by whether the injected context matched the candidate, giving a cheap pre-screen before spending bench budget.
  Done when: for a candidate rule edit, `fm evolve --estimate` prints an effect estimate with an interval, and on a past change the sign agrees with the later bench result.

- **Run a live blackboard that lanes publish to and subscribe from** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: assumption: lanes only share state through briefs and merges. Evidence of friction: lane merge conflicts with main-thread work (T-0403) and a lane's guard refusals the main thread never saw. A typed pub/sub board ("I changed API X", "gate Y is flaky", "file Z is leased") means lanes learn about each other mid-run.
  Done when: lane A posts a changed-signature fact and lane B's next turn shows it without any human relay.

- **Keep durable state in git refs so sync and multi-machine come free** — FEATURE — value 4 — effort L — risk high — category: state
  Why: `fm sync` mirrors state one way into `.foreman/`, and fleet ideas all need a transport. Storing the ledger as append-only entries under `refs/foreman/*` (merged as a grow-only set) reuses git's push, pull and auth. Trade-off: concurrent edits to mutable brief fields need a deterministic merge rule.
  Done when: two clones each add tasks offline, and after push and pull both show the union with no manual merge.

- **Throttle autonomy by unreviewed-diff debt** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: `autonomy=full` never asks mid-run and the queue keeps draining, so unreviewed change piles up. Measure lines or tasks the user hasn't opened (via `fm tour` reads, PR views or commit-author checks). Past a threshold, drop to standard autonomy and offer a review packet. Assumption: the "read" signal is available.
  Done when: after N closed tasks with no tour or PR view, the drive switches to asking mode and says why.

- **Export a live task as a portable bundle another machine or person resumes** — FEATURE — value 4 — effort M — risk med — category: handoff
  Why: a `git bundle` plus the brief, ledger slice, evidence and resume point would let a task move between devices, harnesses or humans without a fleet. The pack has `fm session` and `fm export`, but nothing task-shaped. Doing less than the fleet gives most of the value.
  Done when: `fm task pack T-x` on machine A and `fm task unpack` on machine B resume at the same step with the same evidence.

- **Show open criteria as editor diagnostics over LSP** — FEATURE — value 3 — effort M — risk low — category: editor surface
  Why: surfaces listed are the web UI, band, pane and desktop; the user's own editor sees nothing. A tiny LSP server could mark lines touched by open criteria, vetoes that apply to a file (`fm vetoes`), and the "why" lessons for that line (`fm why`).
  Done when: opening a file with an active-task criterion shows a diagnostic, and it clears when the criterion passes.

- **Raise a Goodhart alarm on Foreman's own metrics** — FEATURE — value 4 — effort M — risk low — category: self-measurement
  Why: friction, bench and evolve all optimize measured signals, and the friction slow-gate signal itself needed a fix (T-0424). Flag when a proxy such as gate pass rate, lesson count or cleanliness rises while rework, user steers or reopened tasks don't fall.
  Done when: seeded history where pass rate rises and rework stays flat produces a named warning in `fm friction`.

- **Schedule the queue with a constraint solver and explain infeasibility** — FEATURE — value 3 — effort M — risk med — category: scheduling
  Why: the pack shows 20+ queued tasks and an idle JARVIS session. Encode dependencies, file leases, budget pace and lane count as constraints, and when nothing fits say exactly which constraint binds ("T-0214 waits on lease X") instead of "nothing else to do". Trade-off: needs file-footprint estimates to be good.
  Done when: with a seeded conflicting queue, `fm next` names the binding constraint and offers the best feasible set.

- **Wild: Search over steps like a game tree, using partial gate scores as the value** — FEATURE — value 4 — effort L — risk high — category: search
  Why: wild; assumption: hard L tasks are raced whole today. Instead, branch lanes at decision points, score each by gates passed so far, prune low scorers and expand the best. This costs more per hard task but wastes less than full races.
  Done when: on a seeded task with two plausible designs, the search abandons the failing branch before its first full gate run and merges the passing one.

- **Wild: Detect rubber-stamp approvals and raise the stakes display** — SECURITY — value 3 — effort S — risk low — category: ask integrity
  Why: wild; `fm ask` grants rest on the user's next message. If approvals come within a second of a long, high-category request, or repeat verbatim, Foreman shows the concrete command diff and requires a typed confirmation. It guards against approval fatigue, which is invisible to the guard itself.
  Done when: a test approving a core-category grant in under 1 second triggers the stronger confirmation prompt.

- **Wild: Harvest expiring usage quota on low-priority backlog** — FEATURE — value 4 — effort M — risk med — category: budget
  Why: wild; the budget logic already knows pace (T-0320, "no blocking until 75%"). When a usage window is about to reset with plenty unspent, `fm night`-style runs should pull deferred, safe tasks (CLEAN, RESEARCH, eval capture such as T-0035) forward, in lanes, with merges held for review.
  Done when: with a window 90% elapsed and 50% unused, `fm budget` shows queued deferred tasks started in lanes, none merged without approval.
