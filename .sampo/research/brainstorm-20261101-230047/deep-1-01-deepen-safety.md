# Brainstorm — lens: deepen: safety

- **Make a trigger-safety envelope one object** — FEATURE — value 5 — effort M — risk low — category: trigger policy
  Why: the list repeats the same guards (worktree, branch, budget, file-a-task-only, scoped profile) as separate ideas; assumption: one envelope per trigger, set at install and shown in the one-yes prompt, is simpler than 15 flags.
  Done when: `fm triggers add` refuses a trigger with no envelope, and the install prompt prints its action level, budget, landing branch and tool profile.

- **Climb a trust ladder per trigger** — FEATURE — value 5 — effort M — risk low — category: trigger policy
  Why: the pack's ideas (shadow week, dry-run, file-a-task-only) are stages of one path; assumption: a trigger earns each rung (shadow, capture only, branch work) from its own measured precision, which `fm triggers` already computes.
  Done when: a new trigger starts at shadow, and a test shows it advancing a rung only after N settled fires above the precision bar and dropping a rung after a miss.

- **Break the loop on self-made events** — FIX — value 5 — effort S — risk low — category: loop safety
  Why: "stop a trigger from re-firing on its own output" is listed, and CI and issue watchers react to commits Foreman itself pushes (fm ship, ci-watch --last-ship); assumption: no provenance marker exists today.
  Done when: a commit, file write or issue tagged with a trigger's run id never fires a trigger within that run's descendants, tested on a cycle of two triggers.

- **Pause triggers while the user is present** — FEATURE — value 4 — effort S — risk low — category: user presence
  Why: "defer triggers while the user is working in the repo" is listed; assumption: recent edits, a live session or a dirty tree are enough signals.
  Done when: with a live session in the repo, a due trigger logs "deferred: user active" and fires on the next idle tick.

- **Reserve a shared spend pool across triggers** — FEATURE — value 4 — effort M — risk med — category: budget
  Why: per-trigger caps still sum to a surprise; the steer on `--pace off` says real limits are waited out, so a pool must hold back interactive work's share.
  Done when: five triggers at their individual caps cannot together pass the pool, and interactive sessions keep a reserved fraction a test proves.

- **Quarantine a trigger after repeat bad outcomes** — FEATURE — value 4 — effort M — risk low — category: loop safety
  Why: `fm outcomes` tracks survival and `fm triggers` tracks precision; assumption: a trigger whose work was reverted twice should demote itself without being asked.
  Done when: two reverted triggered tasks move a trigger to shadow and the morning digest names it and why.

- **Sign trigger definitions and review changes** — SECURITY — value 4 — effort M — risk low — category: integrity
  Why: the standing intent fences injection; a trigger file edited by an agent or a downloaded repo is a persistent foothold; assumption: triggers live in a plain file the agent can write.
  Done when: a trigger whose definition changed without a user-approved `fm ask` signature does not fire, tested by editing the file directly.

- **Treat issue and CI text as hostile input** — SECURITY — value 5 — effort M — risk med — category: injection
  Why: issue watchers feed outsider text into an unattended agent with no one watching; assumption: that text now goes into the brief verbatim.
  Done when: a planted issue body saying "run curl ... | sh" produces a capture quoting it as data, and the lane's guard denies the command, tested end to end.

- **Show a blast-radius preview before the one yes** — FEATURE — value 4 — effort M — risk low — category: consent
  Why: installs (timers, units) get queued for "one yes"; a yes is only as safe as what it shows. Assumption: today it shows the unit text.
  Done when: the queued install lists the files it writes, the commands it may start, the worst-case daily spend and an uninstall line.

- **Tripwire file stops everything (wild)** — FEATURE — value 3 — effort S — risk low — category: kill switch
  Why: wild; touching `~/.foreman/STOP` (or any chosen file, even from a phone via sync) makes the tick skip all triggers and halt running lanes, no CLI needed.
  Done when: creating the file halts a running triggered lane within one tick and the log says who tripped it.

- **Dead-man switch for the user (wild)** — FEATURE — value 3 — effort M — risk med — category: kill switch
  Why: wild; if the user hasn't acknowledged a digest in N days, triggers step down a rung automatically, so a forgotten setup cannot work indefinitely unobserved.
  Done when: after N days without an ack, autonomy drops one rung and the next digest says so; an ack restores it.

- **Rehearse a trigger on a fabricated storm (wild)** — FEATURE — value 3 — effort M — risk low — category: chaos test
  Why: wild; `fm doctor` fires a synthetic burst (1000 file events, a flapping CI) at each armed trigger in a sandbox and fails if the breaker doesn't trip, so storm safety is shown rather than assumed.
  Done when: the doctor row goes red for a trigger whose breaker lets more than its cap through.

- **Record every self-start with its cause chain** — FEATURE — value 4 — effort S — risk low — category: audit
  Why: the night tick logs only when something happens, so "why did this start?" has no answer; assumption: the log lacks the event, the rule and the approver.
  Done when: `fm why <task>` prints the trigger, the event that fired it, the envelope in force and the approval that armed it.

- **Resolve unattended asks to a safe default** — FIX — value 4 — effort S — risk low — category: unattended
  Why: steers say only outward actions, merges and irreversible steps need the user; assumption: a triggered lane that hits one can hang or guess.
  Done when: a triggered lane that reaches a push, merge or install parks it as a queued `fm ask --later` item and continues the rest, tested with a planted push step.

Next question: Which trigger events can an outsider cause (issue text, forked PRs, shared-directory files), and does each one have a test showing the agent treats it as data?
Next question: What does the user see when they come back after a week away, and could that page alone let them undo everything a trigger did?
