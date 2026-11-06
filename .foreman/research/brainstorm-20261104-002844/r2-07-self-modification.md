# Brainstorm — lens: self-modification

- **Turn each worktree failure into a repro test and a patch proposal** — FIX — value 5 — effort M — risk med — category: self-repair
  Why: the request says evidence and lease commands fail inside the builder worktree. Today someone has to notice that and file a task.
  Done when: a planted worktree failure of `fm evidence` produces a red test and a patch proposal in a lane within one tick, with no human filing.

- **Queue self-edits and apply them only at a goal boundary** — FEATURE — value 5 — effort M — risk low — category: safe points
  Why: resume was the worst area, and 2 of 6 needed a later fix. A gate or hook edited mid-goal changes the rules under the running agent. Assumption: the drive can tell where a goal ends.
  Done when: a self-edit landed during an open goal stays in `pending-upgrade`, and a hook run mid-goal still uses the old version. It activates when the goal closes.

- **Let self-edits tighten the done gate freely and require the user to loosen it** — SECURITY — value 4 — effort S — risk low — category: gate ratchet
  Why: 6 false dones are unchanged since gen 2, so the pressure runs toward stricter gates. A self-edit that relaxes a clause is the dangerous direction.
  Done when: a self-patch that removes or weakens a done clause is classified "loosening" and refused unless a user grant is present. A tightening patch lands without one.

- **Replay the failed resume with the edited text before accepting a skill or hook change** — FEATURE — value 4 — effort M — risk med — category: counterfactual replay
  Why: edits to injected text are judged only by reading them, not by whether the agent behaves differently. Assumption: a cheap model on the recorded transcript is a usable proxy.
  Done when: a proposed resume-card edit stores a before/after replay, and the edit is rejected if the next action matches the failing one.

- **Bisect the self-edit ledger when a hook starts failing** — FIX — value 4 — effort M — risk low — category: rollback
  Why: self-edits stack, and "roll back on worse outcomes" assumes the culprit is the latest one. Assumption: each self-edit is a separate revertable commit.
  Done when: with 5 self-edits and one planted bad hook change, `fm doctor` names the culprit commit and reverts only that one.

- **Migrate in-flight ledgers when a self-edit changes their schema** — FIX — value 4 — effort M — risk med — category: migration
  Why: goals run over days and crashes, so open goals hold state written by the old code. A reader change can silently misread it, which is the resume class of bug.
  Done when: a schema-changing self-edit ships a generated migration plus a test that reads a copied live goal ledger both before and after, and the edit is refused without them.

- **Add a self-modification digest to the resume card** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: after a compaction or crash the agent wakes up under possibly changed rules and doesn't know it.
  Done when: a resume after a mid-goal-boundary self-edit shows "rules changed since you left: <one line each>" in the first 40 lines of the card. It stays empty when nothing changed.

- **Self-tune the resume card from which lines the agent actually used** — PERFORMANCE — value 4 — effort M — risk low — category: self-tuning
  Why: the card is budgeted by line count with no measure of what is read. Assumption: a line counts as used if the next 20 tool calls reference its ids, paths or commands.
  Done when: after 10 resumes, a per-line use count exists and the lowest-used lines are demoted below the fold. A line that is never used is flagged.

- **Fence self-edits to the failure's own blast radius** — SECURITY — value 3 — effort S — risk low — category: scope fence
  Why: a patch for a worktree bug has no reason to touch the guard or ledger writers. Steers already protect a core, but only by path list.
  Done when: a self-patch touching files outside {stack-trace files, their tests, the named verb} is refused with the list of out-of-scope paths.

- **Wild: Write tripwire tests that guard against Sampo's own future shortcuts** — FEATURE — value 3 — effort M — risk low — category: anti-gaming
  Why: assumption: self-modification fails by quietly deleting what made it fail. Each false done leaves a test that lights up if a clause is removed, and only a sealed user waiver can delete it.
  Done when: removing the gate clause born from false-done F1 turns a tripwire red, and the self-edit pipeline can't delete that tripwire.

- **Wild: Collect agent confessions about what Sampo made harder** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: assumption: the agent in the worktree is the first to feel friction and gets no channel for it. A one-line "Sampo got in my way because…" at goal close is tallied, and a confession repeated 3 times becomes a self-repair candidate.
  Done when: three planted identical confessions open exactly one deduped task with the quotes attached.

- **Wild: Hold a nightly self-surgery rehearsal on a throwaway clone** — FEATURE — value 3 — effort L — risk med — category: dry run
  Why: assumption: a self-edit has not been tried in the same conditions as the live drive. Overnight, apply every pending self-edit to a clone and run the planted-fault scenarios, including forced compaction, a killed session and a worktree start.
  Done when: the morning card lists each pending self-edit as "survived" or "broke X", and nothing was applied to the live install.

- **Wild: Keep a self-version pinned to each goal as a receipt** — FEATURE — value 2 — effort S — risk low — category: provenance
  Why: assumption: when a true done later turns out false, the first question is which Sampo version said it. Stamp the done verdict with the hash of gate and hooks.
  Done when: every done verdict records a code hash, and `fm why done T-id` prints which self-edits postdate it.

Next question: Which goal-path capability has never been changed by Sampo's own hand, and is that because it is perfect or because nothing is allowed to touch it?
Next question: When a self-edit is reverted, does the false done that motivated it come back, and is anything watching for that?
