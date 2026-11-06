# Brainstorm — lens: self-modification: every self-change gated by bench and trials, scored afterwards and reverted when it made things worse

- **Score every self-change against its own stated prediction** — FEATURE — value 5 — effort M — risk low — category: self-repair
  Why: T-2290 already scores minutes/attempts predictions, but a self-made fix (T-2272 signal→fix) never records "this signature should stop recurring in N tasks". Without that, a fix is judged done when it merges, not when the signal dies.
  Done when: each task spawned by the signal-to-fix loop stores a target signature and a window, and `fm doctor` lists fixes whose signature recurred after merge.

- **Auto-revert a self-change that regresses its bench** — FEATURE — value 5 — effort M — risk med — category: rollback
  Why: the lean ratchet (T-2281) only warns when footprint grows; nothing reverts. Ship records exist per commit, so a post-merge bench/hook-p50 regression can be tied to a commit.
  Done when: a seeded regression (a hook made 2x slower) in a throwaway repo is reverted by `fm selfcheck` into a new commit with a reason, and a test proves it.

- **Hold out trials the self-fixer never sees** — SECURITY — value 5 — effort M — risk low — category: anti-gaming
  Why: steers require signals Foreman didn't author; a loop that fixes its own failures and passes its own tests can overfit. assumption: the fix loop currently runs the same bench it learns from.
  Done when: a self-change is accepted only if it passes a held-out trial set whose cases are absent from the fixer's context, verified by a test that greps the brief.

- **Cap self-change blast radius per day** — SAFETY→SECURITY — value 4 — effort S — risk low — category: guard
  Why: self-triggering (#11) plus self-repair (#7) can compound unattended. Guard and hooks are the most dangerous things to self-edit.
  Done when: a self-authored task touching guard files or hooks needs a user yes, and more than N self-merges per day pauses the loop with a visible reason; both are tested.

- **Keep a self-change ledger with verdicts** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: nothing in the pack shows one place listing "what Foreman changed about itself, why, and did it help". The user's recurring asks are fix-by-fix with no rollup.
  Done when: `fm selfchanges` prints each self-authored commit with trigger, prediction, 7-day outcome (kept/helped/hurt/reverted) and the page on the site shows it.

- **A/B a self-change on shadow before it goes live** — PERFORMANCE — value 4 — effort L — risk med — category: trials
  Why: the model router and trigger routing learn from outcomes but apply immediately. assumption: no shadow mode exists (T-0828 mentions shadow only for compact output).
  Done when: a changed router/trigger rule runs in shadow for K tasks, logs would-have-chosen vs actually-chose, and promotes only if it wins by a stated margin.

- **Detect a learned rule the user keeps correcting** — FIX — value 4 — effort M — risk low — category: correction loop
  Why: user corrections are the stated input to #7, but the pack shows the user filing misses (T-2285, T-2288) rather than Foreman noticing them first.
  Done when: two user edits/drops of the same learned-rule output within a week auto-open a task naming the rule and demoting it to advisory.

- **Quarantine a self-fix that needed a second fix** — FEATURE — value 3 — effort S — risk low — category: self-repair
  Why: T-2283/dropped "same failure, dedupe missed" shows fixes spawning fixes. A fix re-fixed within 3 tasks should lower the loop's confidence for that signature class.
  Done when: a re-fixed self-fix reduces the auto-filing rate for its signature class, visible in `fm triggers`.

- **Prove the checker before trusting its verdict** — SECURITY — value 4 — effort M — risk low — category: meta-verification
  Why: the earlier open question "numbers never checked by someone other than the producer". Bench and trials gating self-change are only as good as their ability to fail.
  Done when: before gating, each gate is run against a planted-bad change and must fail it; a gate that passes it blocks all self-merges and says so.

- **Wild: Mutation-test the self-improver** — FEATURE — value 3 — effort L — risk med — category: adversarial
  Why: wild. A nightly lane plants a subtle regression in a copy of Foreman and checks the self-repair loop finds and reverts it, scoring its own detection rate.
  Done when: a nightly report states planted-regression catch rate and drops below a threshold open a task.

- **Wild: Two-vendor handshake for self-changes** — FEATURE — value 3 — effort M — risk low — category: review
  Why: wild. Writer is one vendor's model, the cold read a different one, per the "signals Foreman didn't author" steer; no user-owned check sits between them today.
  Done when: a self-change merges only with a cold read from a different model family, recorded in the ledger.

- **Wild: Self-change "undo window" with a one-key revert** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. After any unattended self-merge the next session's first line offers `fm undo` with the diff in a sentence, expiring in 48h.
  Done when: `fm undo` restores the pre-change tree for the last self-merge and a test covers it.

Next question: Which self-changes today bypass the bench because they touch only prose, rules or skills, and how would a regression there be seen?
Next question: What does "worse" mean for a self-change the user can't measure, and who defines the metric before the change rather than after?
