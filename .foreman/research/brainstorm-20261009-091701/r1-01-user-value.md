# Brainstorm — lens: user value

- **Run a merge-train lane fleet** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: JARVIS idled with 20+ queued tasks, and `fm lane merge` refused a dirty main while the main thread was mid-task. Foreman has lanes and `fm relate`, but no scheduler that uses them together.
  Done when: with 6 queued tasks of which 3 are independent, `fm run --fleet` starts 3 lanes in parallel, predicts file overlap before starting each, and lands them in dependency order with the gates re-run after each merge.

- **Close the downstream loop with a canary release** — FEATURE — value 5 — effort L — risk med — category: release
  Why: nearly every ask is "Foreman x.y.z … to GitHub main and JARVIS", and each fix comes from a JARVIS friction report that was relayed by hand. Assumption: JARVIS is one of several downstream projects.
  Done when: `fm release` replays each registered downstream project's recent guard commands and gate results against the candidate, blocks on any new refusal or regression, upgrades the projects, and a refusal in a downstream project later files a redacted, repro-carrying upstream task by itself.

- **Make cleanup a gate** — FEATURE — value 5 — effort M — risk low — category: hygiene
  Why: the user steered "cleanup requests never got done — trace why and fix". Cleanup of dead code, replaced functionality, stale briefs and docs has no owner in the task lifecycle.
  Done when: `fm task done` asks "what did this replace?", `fm sweep` lists unreferenced symbols, stale docs and obsolete briefs found by the diff, and an unresolved item becomes a queued CLEAN task that cannot be silently dropped.

- **Run an edit-time test sentinel with mutation proof** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: T-0214 is deferred. The `fm map` test links exist. Gates currently pass whether or not the tests would catch a break.
  Done when: after an edit, the linked tests run in the background and a red result is surfaced before the next edit. `fm audit` mutates the diff and reports any mutant that no test killed.

- **Turn guard refusals into self-fixing tasks** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: a long run of JARVIS-reported false refusals (symlink `rm`, `fm focus;` chains, lane caches, "no active task"). Each was found by a person.
  Done when: a refusal followed by the user overriding it or rephrasing the command within 2 turns is logged as a probable false positive. `fm friction` turns it into a minimal repro plus a proposed rule change that must pass the 5000-command replay.

- **Learn lessons with confidence and prune them** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: T-0217 (lesson confidence) and T-0035 (eval capture) are both deferred. `fm bench` and `fm evolve` already exist to gate changes.
  Done when: each lesson carries a score that rises when recalling it preceded a first-time pass. Lessons below the threshold are proposed for deletion, and a bench run shows the pruned set does no worse.

- **Run structured adversarial audits** — FEATURE — value 4 — effort L — risk low — category: review
  Why: T-0034 (`fm audit run`) is deferred. `fm audit` and `fm second` prepare reviews but do not execute them.
  Done when: `fm audit run` launches read-only reviewers with different lenses, each writing a findings file with file:line evidence. The task cannot close until each finding is fixed, disputed with a reason, or deferred as a task.

- **Fleet across machines** — FEATURE — value 4 — effort L — risk high — category: multi-machine
  Why: the user asked for "multi-machine and multi-agent work". `fm projects`, `fm session` and `fm serve` already cover one device.
  Done when: a task pinned to a second host over SSH runs in a lane there with the same guard and ledger, and its evidence and branch show up on the first host's UI.

- **Make estimates and pace predictive** — FEATURE — value 3 — effort M — risk low — category: budget
  Why: the user dropped token caps and wants no blocking until 75% usage. Foreman can instead forecast.
  Done when: before `fm run` starts, it prints the expected cost and duration per task from similar finished tasks. It schedules heavy tasks for the night window when usage is under pace, and blocks nothing below 75%.

- **Dream mode (wild)** — FEATURE — value 5 — effort L — risk med — category: autonomy
  Why: wild. `fm night`, `fm ideas` and lanes exist. The user keeps asking for "recursive" self-improvement.
  Done when: overnight, `fm night` builds the top brainstorm ideas speculatively in lanes with full gates, then leaves a morning digest of merge-ready branches, each with proof, and a one-keystroke accept or discard.

- **Build a taste twin that answers for the user (wild)** — FEATURE — value 4 — effort L — risk high — category: autonomy
  Why: wild. `fm taste` records keeps, drops and steers, and the user often steers after the fact ("shouldn't block until 75%").
  Done when: for an `?` item or L-plan approval, a model of the user's taste proposes an answer with a confidence. Above a threshold it proceeds under `autonomy full`, and every such auto-decision is logged and revocable in one command. The replay of past decisions shows at least 80% agreement before it is enabled.

- **Write a bug brief from a screen recording (wild)** — FEATURE — value 3 — effort L — risk med — category: capture
  Why: wild. `fm smoke` already drives a headless browser, and bug reports such as "band stuck on step 1/5" are visual.
  Done when: a short recording or HAR of a UI misbehaviour becomes a FIX brief with steps, a failing smoke script, and the screenshots as evidence. The brief closes only when the script passes.

- **Replay a task as a scrubbable story** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: `fm why`, `fm tour`, `fm pr` and the ledger hold the pieces. The user manages many sessions in the desktop app and cannot easily see how a result came about.
  Done when: `fm story T-xxxx` renders an HTML timeline of the plan, edits, evidence, decisions, surprises and cost, with a diff at each point, and the desktop app opens it from the task.

- **Check the product against real journeys** — FEATURE — value 4 — effort L — risk med — category: product check
  Why: the user asked "Foreman checks the product the way its user uses it". Today it is a headless browser at two viewport sizes.
  Done when: journeys are derived from briefs and recorded real sessions into replayable scripts (web, CLI, API). `fm smoke` runs them on a drained queue and reports a regression against the last green run.
