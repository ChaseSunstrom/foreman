# Brainstorm — lens: user value

- **Brief the user on return** — FEATURE — value 5 — effort M — risk low — category: continuity
  Why: the user's asks are mostly one-line, and a forever-loop and lanes can run for hours (T-0793, T-0792). Nothing in the pack says what the user sees when they come back.
  Done when: opening a session after 2+ idle hours with lane activity prints at most 6 lines: what shipped, what is waiting on the user, and what failed. A test checks each line against the task records.

- **Check before walking away** — FEATURE — value 5 — effort M — risk low — category: autonomy
  Why: assumption: unattended runs stall on predictable causes: a permission prompt, a blocked task (T-0325, T-0335), a spent usage budget, or a dirty tree. `fm away` lists these and fixes the fixable ones.
  Done when: `fm away` on a project with a seeded permission need and a spent risk budget lists both with a fix command, and exits 0 only when nothing would stall the loop.

- **Plan a session to fit a time box** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: the queue has 40+ open items with S/M/L sizes and no way to say "I have 45 minutes." Assumption: past task durations are recorded.
  Done when: `fm plan 45m` picks open tasks whose estimated durations sum to 45 minutes or less, then stops with a clean tree and a ship-ready list. A test uses a fixture history.

- **Learn allowlist rules from manual approvals** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: the guard hook blocks commands in bypass mode, and a block the user then overrides is a signal. Assumption: overrides are observable. This is distinct from policy-as-code because the rule is proposed from behaviour, not written by hand.
  Done when: after the user runs the same blocked command class 3 times by hand, Foreman proposes a narrowly scoped rule with an expiry. A test shows the rule allows that exact form and still blocks a variant.

- **Add a "least sure about" line to every close** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user's steers repeatedly correct things Foreman missed, such as a dirty file from another task, a `-k` that matched nothing, or a scratchpad write. The weak spot of each task is knowable at close, and naming it directs the user's review.
  Done when: `fm task done` output includes one line naming the least-covered changed path or assumption. A test closes a task with an untested branch and expects that branch named.

- **Show the ceremony tax per task** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: T-1231 and T-0866 want proof that discipline pays, but the user gets no per-task evidence. Assumption: gate and test time is already logged.
  Done when: the close receipt shows "Foreman overhead: Xs of Ys (Z%)" and the figures match the task's gate and run log.

- **Ask one question only when readings diverge** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: the asks are terse, with `@path` and DONE-WHEN hints, and the recurring failures are misreads, such as intake dropping an `@path`-only line or `-k` unioning with names. A single clarifying question, asked only when two plausible parses would change the files touched, costs less than a wrong task.
  Done when: an ask with two parses touching different files triggers one question naming both. An ask with a single parse triggers none. Both cases are covered by tests.

- **Auto-run green captures and report the revert rate** — FEATURE — value 5 — effort L — risk med — category: autonomy
  Why: many recent asks are Foreman's own captured micro-fixes: small FIX tasks with a scope and a DONE-WHEN, which the user then types back as "Ship Tn." Tiering these removes that round trip. The revert rate decides whether the tier stays.
  Done when: a capture that is FIX, scoped to one file, has a DONE-WHEN and an existing test runs in a lane without an ask. `fm stats` shows its revert rate, and a rate above a set threshold turns the tier off.

- **Give one "safe to close the laptop" verdict** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: assumption: the user ends sessions with uncertainty about running suites, unshipped tasks and live lanes. One command answers it.
  Done when: `fm bye` prints SAFE or lists blockers (a running suite, an unshipped closed task, a dirty tree). A test covers each blocker.

- **Wild: Review the user's hand edits** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the guard protects the user's own edits (an existing idea), but nothing in the pack uses them. When the user edits by hand, Foreman can run the gates, find the missing tests and propose proof. Assumption: the user edits by hand sometimes.
  Done when: `fm review-mine` on a tree with an untested hand edit returns a failing-test proposal and a gate result, without modifying the edit.

- **Wild: Write the status update for someone else** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: commits are chains of task ids ("T-2001: T-1998, T-1999, T-2000") that mean nothing to a manager or teammate. A plain-language summary is the missing step.
  Done when: `fm status --for-others --since 7d` prints at most 10 lines of user-visible outcomes with no task ids. A test confirms every line maps to a closed task.

- **Wild: Learn "done" from reverts** — FEATURE — value 4 — effort L — risk med — category: learning
  Why: assumption: reverted or hand-fixed tasks show where the DONE-WHEN was too weak. Mining them yields per-project close checks, such as "this module needs the integration run."
  Done when: after 3 reverts touching the same module, Foreman proposes an extra close check for that path. Replaying the history shows it would have caught at least 2 of the 3.

- **Wild: Say when Foreman is slower than plain Claude** — FEATURE — value 3 — effort M — risk med — category: honesty
  Why: the product's claim is discipline, but small fixes may not need it (T-0794, Lite mode). An honest "this task needed no ceremony" note, backed by past data, builds trust.
  Done when: for a task kind where recorded overhead exceeded the catch rate in 20+ closes, the next task of that kind shows a one-line note and offers `--lite`. A test uses fixture history.
