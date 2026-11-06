# Brainstorm — lens: self-modification

- **Fence trigger-born sessions from the trigger registry** — SECURITY — value 5 — effort S — risk low — category: separation of powers
  Why: assumption: sessions started by a schedule, file watcher, CI or issue can in principle edit the file that defines triggers, the Ward and the done-gate. That makes self-start plus self-edit a privilege-escalation loop.
  Done when: a planted trigger-born session that tries to write the trigger file, the Ward rules or the gate is refused with a named reason, and the same write from a user-started session passes.

- **Re-install the plugin after ship, with a canary and rollback** — FEATURE — value 4 — effort M — risk med — category: self-deploy
  Why: T-0418 (installed foreman-ui behind source) and the "installed vs source drift" items show shipped changes don't reach the running copy by themselves. Unattended self-triggering makes that gap worse.
  Done when: after `fm ship`, a hook re-installs, runs `fm doctor` plus the hook canary, and restores the previous install if either fails. A test with a planted broken release shows the restore.

- **Re-exec the drive at an idle tick after code lands** — FIX — value 4 — effort M — risk med — category: drive
  Why: the recent drive fixes (T-2873, T-2900, T-2901) changed running-set logic. A drive process started before the fix keeps the old logic in memory while the new code is on disk.
  Done when: the drive compares its loaded module hash with disk at each tick. When they differ and no agent is mid-step, it re-execs with the same state, and a test shows it picks up a changed constant without losing the queue.

- **Generate failed-tool-call rewrite rules as data, replay-gated** — FEATURE — value 5 — effort M — risk med — category: tool reliability
  Why: the request cites failed tool calls up by half. Fixing those by hand doesn't scale. Argument-shape failures such as bad paths, quoting and missing flags can be fixed deterministically.
  Done when: a rules file (match signature → rewrite) is proposed from the failure ledger. A rule goes live only if replaying the last 30 days of failures fixes at least N of them and breaks no previously successful call.

- **Distil a standing-grant proposal from the install-yes history** — FEATURE — value 4 — effort S — risk low — category: unattended grants
  Why: the request says installs are queued for one yes. If the user says yes to the same class every time (for example pinned embedding models from a known registry), the queue is friction a self-edit could remove.
  Done when: after K identical yeses, `sampo next` offers a draft grant that is scoped, expiring and revocable. It takes effect only on the user's yes, and a test shows it never covers a class that was ever refused.

- **Keep all drive and trigger tunables in one genome file** — CLEAN — value 3 — effort S — risk low — category: tunables
  Why: the drive's constants (LONG_JOB_S, debounce, pace, re-push rules) are spread over modules. Self-tuning edits to code are riskier than edits to data.
  Done when: every tunable is read from one file with bounds and a default. A test fails if a numeric constant used by the drive is defined outside it, and self-edits are allowed only on this file.

- **Gate self-edits on a land-while-running drill** — SECURITY — value 3 — effort M — risk low — category: self-edit safety
  Why: assumption: the hazard of unattended self-modification is not the edit but the moment it lands mid-run (half-written module, a ledger schema changed under a live lane).
  Done when: a drill lands a candidate edit while a fake lane is mid-task and passes only if the lane finishes and the ledger stays readable by both versions.

- **Wild: Evolve the genome overnight on replayed nights** — FEATURE — value 4 — effort L — risk med — category: self-tuning
  Why: wild. The local models give unlimited volume. A mutator proposes genome variants, each variant is scored by replaying recorded event streams through the drive (stops, idle gaps, failed calls), and the user sees only the winning diff in the morning card.
  Done when: one overnight run produces a genome diff that lowers replayed drive stops on a held-out week by a stated amount, with the old genome one command away.

- **Wild: Mutate triggers to test the loop breaker** — SECURITY — value 3 — effort M — risk low — category: chaos
  Why: wild. A lane generates adversarial trigger rules (self-caused file events, CI failures caused by its own fixes, issue ping-pong) in a scratch repo and checks that the depth cap and self-cause filter stop each within the budget.
  Done when: a generated suite of at least 20 looping triggers all halt within the cap, and a deliberately broken breaker makes the suite fail.

- **Wild: Make every stall write its own patch proposal** — FEATURE — value 4 — effort M — risk med — category: drive self-repair
  Why: wild. The request names drive stops as a top gap. A stall record (typed cause, last 50 ticks) feeds a local-model lane that drafts a fix into a quarantine branch, then replays the stall against it.
  Done when: for a replayed historical stop, the lane produces a branch whose replay no longer stops. It is held for one yes, never merged on its own.

- **Wild: Hold a monthly "pull the plug on one trigger" drill** — FEATURE — value 2 — effort S — risk low — category: trigger hygiene
  Why: wild. The sentry disables one random trigger for a week and records whether anyone noticed (re-asks, manual runs). Triggers nobody missed become retirement proposals.
  Done when: the drill's ledger lists each disabled trigger with a noticed/unnoticed result, and an unnoticed one shows up as a retirement proposal in the next morning card.

- **Split self-edit rights by trigger origin in the ledger** — CLEAN — value 3 — effort S — risk low — category: provenance
  Why: assumption: once edits come from timers, watchers and CI, "who made this edit" is unanswerable without a cause stamp.
  Done when: every self-edit commit carries a trailer naming its wake reason, and `sampo outcomes` can group reverts by that reason.

Next question: When a self-triggered session's output is wrong overnight, what single record would let the user see which trigger, which edit and which model caused it in under a minute?
Next question: Which self-edits has the user reverted by hand, and do those cluster on any one surface that unattended edits should never touch?
