# Brainstorm — lens: deepen: auto-start

- **Gate auto-start on one "should Genesis start?" predicate with a visible reason** — FEATURE — value 5 — effort M — risk med — category: auto-start
  Why: the category lists many guards (dry vs blocked, safe tree, cooldown, breaker, ceiling) as separate ideas. assumption: they collapse into one pure function over queue, tower, tree, budget and history.
  Done when: `fm genesis should-start --json` returns `{start: bool, reasons: [...]}` and a table-driven test covers each guard (dry, blocked, dirty tree, cooldown, ceiling, breaker, Genesis-made work).

- **Count "dry" only over user-origin work** — FIX — value 4 — effort S — risk low — category: dry-queue
  Why: "Don't let Genesis-made work count as queue dry" and "detect blocked, not finished". The open list shows many deferred or blocked tasks (T-0325, T-0335, T-1207), which a naive count calls empty or busy. Tasks carry an origin tag (assumption).
  Done when: with only deferred, blocked and genesis-origin tasks open, the verdict is `blocked`, not `dry`. With zero open tasks it is `dry`. Both cases are tested.

- **Propose first, run on a yes, and let a standing grant promote the proposal** — FEATURE — value 5 — effort M — risk med — category: consent
  Why: the routing line in rules/foreman.md is protected core, so auto-start needs a candidate plus the user's yes. The site-publish grant ("standing grant") is the precedent. A first-run proposal is one line with a cost estimate. After N accepted proposals Foreman offers to make it automatic, and the grant is scoped to project and budget.
  Done when: the first dry queue yields a one-line proposal with an estimate and no tower written. `fm genesis auto on --budget 5` is recorded, and the next dry queue starts unprompted within that budget.

- **Charge each auto-start against what the last one produced** — FEATURE — value 4 — effort M — risk low — category: economics
  Why: "Charge auto-start for what the last auto-start produced". Exam scores and `fm outcomes` 30-day survival already exist. Cooldown grows when the last tower closed few scenarios per dollar, and shrinks when it paid off.
  Done when: after a tower with zero closed scenarios, the next cooldown is at least double. After a high-yield tower it resets. Both are asserted from fixture ledgers.

- **Trip a breaker on Genesis's own failure rate, with a human-readable postmortem** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: the "Trip an auto-start breaker" idea. When two consecutive towers abort, drift-fail or lose selection, auto-start disables itself and writes `why-paused.md` into the tower. The tower-archaeology lens needs the files alone to say why it stopped.
  Done when: two failing towers flip `auto` to paused. `fm genesis status` shows the reason. Re-enabling needs an explicit command.

- **Authenticate the trigger with a signed intent record** — SECURITY — value 3 — effort M — risk low — category: trust
  Why: "Authenticate the auto-start trigger". A pasted repo file or a prompt-injected note must not be able to start a week of usage. Only the loop, the scout and the user's CLI may write the trigger. Each is HMAC-stamped with a per-install key.
  Done when: a hand-written `trigger.json` with no valid stamp is ignored and logged. A loop-written one starts the run.

- **Trigger on project events, not just emptiness** — FEATURE — value 4 — effort M — risk med — category: triggers
  Why: "Trigger a generation from project events". Candidates are a failing exam regression, a new language or framework appearing in the map, a gap-map score crossing a threshold, and the site or docs lag measure (T-2073) passing a limit. Each event maps to a smaller scoped generation, not a full tower.
  Done when: adding a new top-level language directory in a fixture repo raises a scoped proposal naming that event. No proposal appears when nothing changed.

- **Schedule auto-start into usage-reset windows** — PERFORMANCE — value 3 — effort M — risk low — category: scheduling
  Why: the economics lens asks when to wait for a usage reset. A proposal can carry "start after the reset, estimated N% of window". An idle-machine check keeps it off the user's working hours.
  Done when: with a fixture budget of 90% spent, the verdict is `defer-until <reset>`. The loop picks it up at that time in a simulated clock test.

- **Pre-flight dry run: show what the tower would write without spending** — FEATURE — value 4 — effort M — risk low — category: transparency
  Why: a one-line proposal is thin on its own. `fm genesis preview` generates the tool-less gen-0 draft only, plus the planned missions and the coverage grid size, so the yes is informed. assumption: the gen-0 writer is one cheap tool-less call.
  Done when: preview writes nothing outside a temp dir, prints gen-0 headings, mission count and a cost range, and the repo tree is unchanged afterwards.

- **Wild: Genesis heartbeat that wakes on the project's pulse** — FEATURE — value 3 — effort L — risk med — category: ambient — wild
  Why: assumption: a project that has gone quiet is exactly where a self-directing harness is most useful. A tiny daemon watches git, CI and the map, and wakes Genesis like a gardener on a seasonal rhythm, running a gap sweep after merges, a spec drift check weekly, and a full tower only after a long drought.
  Done when: in a simulated week of events, the heartbeat emits exactly the expected sweep, drift and tower triggers, and none while a lane is active.

- **Wild: Auto-start by committee: the proposal must survive a tool-less skeptic** — FEATURE — value 3 — effort M — risk low — category: judgment — wild
  Why: assumption: a self-start is costly when wrong. A cheap tool-less child reads only the project summary and argues against starting ("the queue is empty because the project is done"). The start proceeds only if the skeptic's best objection fails a rubric.
  Done when: on a fixture of a finished project the skeptic blocks. On a fixture with planted gaps it passes. Both verdicts are logged.

- **Wild: Pay-it-forward budget, where a tower must earn its next one** — FEATURE — value 3 — effort M — risk med — category: economics — wild
  Why: assumption: a fixed allowance is blunt. Each project holds a token balance that grows only when its past towers' work survives 30 days (`fm outcomes`). A project with no survival history gets one small probationary tower.
  Done when: a project with two surviving towers gets a larger ceiling than a fresh one, and a project whose towers were reverted gets zero. Both are shown by `fm genesis status`.

- **Wild: Cold-start auto-start for a stranger repo, with a "first ten minutes" ladder** — FEATURE — value 4 — effort M — risk med — category: cold-start — wild
  Why: the cold-start lens, assuming no history and no gap map. Rung 1 is read-only (map, gates, a one-line guess at the kind of project). Rung 2 is the proposal. Rung 3 is a small tower limited to MUST and NEVER discovery. Nothing escalates without a yes, and the ladder is saved so a later session resumes at the rung.
  Done when: in an empty fixture repo, `fm genesis` stops at rung 2 and writes a resumable `ladder.md`. A fresh session resumes from that file alone.

- **Let the user veto cheaply: "not now", "not this project", "never ask"** — FIX — value 3 — effort S — risk low — category: consent
  Why: the user has dropped nudges before (the anti-idle push, the repeated pointer), so repeated proposals will get tuned out. Each answer is stored and honored, and the "never" answer is per project.
  Done when: after "not this project", no proposal is raised for that project again. A "not now" suppresses it for the cooldown. Each is tested.

Next question: What does a user who has never typed `fm genesis` do when an auto-start proposal appears, and does the proposal alone make the cost and the "no" path obvious?
Next question: Which signal separates a project that is truly finished from one whose queue is dry, other than the gap map?
