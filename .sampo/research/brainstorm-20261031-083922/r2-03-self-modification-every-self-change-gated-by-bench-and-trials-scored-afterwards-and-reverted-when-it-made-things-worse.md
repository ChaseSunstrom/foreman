# Brainstorm — lens: self-modification: every self-change gated by bench and trials, scored afterwards and reverted when it made things worse

- **Write a prediction before every self-change and score it at day 7** — FEATURE — value 5 — effort M — risk low — category: self-change ledger
  Why: T-2290 already scores predictions of minutes and attempts, and the earlier ideas include a self-change ledger with verdicts, but nothing pre-registers what a fix is expected to change. Without a written prediction (which signature stops recurring, which bench number moves, by how much) a self-fix can only be judged "green", never "worked".
  Done when: `fm selfchange show ID` prints the stated prediction, the measured outcome after 7 days, and a verdict of held, no effect or worse, and a self-change task can't close without a prediction line.

- **Revert a self-change automatically when its own signature returns or a bench number slips** — FEATURE — value 5 — effort M — risk med — category: auto-revert
  Why: T-2272 turns recurring signatures into FIX tasks and the lean ratchet (T-2281) warns on growth, but both only warn; nothing reverses a change that made things worse. The user's 2026-10-31 steer #3 says to keep going rather than stop, so a revert must be a queued task, not a halt.
  Done when: in a fixture, a merged self-fix whose bench median regresses past the noise band yields a revert commit on a lane, gated by the same suite, and the ledger marks the change "reverted: regression".

- **Hold out a trials set the self-fixer cannot read** — SECURITY — value 5 — effort M — risk low — category: anti-gaming
  Why: standing rule says weakness-finding uses signals Foreman didn't author, and the cold reads check for metric-gaming. A fixer that sees every trial can overfit to it. assumption: the current self-fix loop reads the same fixtures it is scored on.
  Done when: trial cases sit in a path the fix lane's guard denies reading, and `fm doctor` fails if the fixer's transcript touched one.

- **Make the bench measure the checker before the change is trusted** — FIX — value 4 — effort M — risk low — category: gate validity
  Why: the pack's open question asks which verbs have a model on both sides with no user-owned check. A bench that cannot go red proves nothing. Plant a known regression (slow a hook by 30 ms) and confirm the gate fails before using it to approve a self-change.
  Done when: `fm selfchange canary` injects three planted regressions and the run fails if any gate passes them; the result shows in `fm doctor`.

- **Cap self-change blast radius by area and per day** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the guard, hooks and USER_ONLY_FM verbs (T-2252) are the user's. Self-fixes touching them should be impossible by path rule, not by cold read alone. assumption: no path-based fence exists today beyond the guard's command rules.
  Done when: a self-change lane that edits the guard, a mandate verb or the steer store is refused at ship with a named reason, and a daily count over N queues the rest.

- **Require a fix-of-fix check: a self-change needing a second fix is quarantined and its class loses autonomy** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: recent history shows chains (T-2283 filed again, then deduped, then T-2285 fixing the plan gate that T-2269 added). Count them per area and demote that area to "propose only".
  Done when: after two chained fixes in one area, new self-fixes there arrive as drafts needing one yes, shown in `fm triggers`.

- **Shadow-run a self-change on the last 30 days of recorded hook inputs before it merges** — PERFORMANCE — value 4 — effort L — risk med — category: replay
  Why: bench_hooks.py measures speed, but a changed hook can also change decisions. Replaying logged hook inputs and diffing the decisions finds silent behaviour change (a guard that now allows what it blocked). assumption: hook inputs are logged or can be.
  Done when: the replay prints "N decisions changed" with each diff, and any guard decision flipping from deny to allow blocks the merge.

- **Score every learned rule by the user's corrections afterwards** — FEATURE — value 4 — effort M — risk low — category: outcome scoring
  Why: the "asked" stream shows the user correcting plan-gate behaviour repeatedly. A rule born of a correction that draws another correction within 14 days is scored "not fixed" and reopened with both texts attached.
  Done when: `fm selfchange show` lists the user's later corrections per change and reopens one when a match appears.

- **Wild: Mutation night, where the self-improver is attacked by its own tests** — FEATURE — value 3 — effort L — risk med — category: meta-testing
  Why: wild. Overnight, break each gate in a throwaway worktree (invert a comparison, skip a check) and see whether the trials notice; unnoticed mutants become FIX tasks for the gates themselves.
  Done when: a nightly report gives a mutation score for the self-change gates and files one task per surviving mutant.

- **Wild: A one-key undo window after every self-change** — FEATURE — value 3 — effort S — risk low — category: user control
  Why: wild. The user can say "undo" within a day and Foreman reverts, records the reason as a steer and never retries the same approach. Corrections by the user are the strongest signal on whether a change was worse.
  Done when: `fm selfchange undo ID` reverts the change, files a standing rule naming the approach and the next self-fix on that signature uses a different approach.

- **Wild: Run the old build against the new failure to prove the fix did it** — FEATURE — value 4 — effort M — risk low — category: causal proof
  Why: wild. Many "fixes" pass because the signature went away by chance. Replaying the stored failing input on the pre-fix tree (red) and the post-fix tree (green) attributes the improvement to the change, and the pair is kept as a permanent regression probe.
  Done when: each self-fix stores its failing input and both runs' output, and the ledger refuses "held" without that pair.

- **Pick the cheapest model for self-fixes by their own survival record** — PERFORMANCE — value 3 — effort S — risk low — category: model routing
  Why: T-2291 routes lanes by how tasks held up. Extend it so a self-fix by Haiku that was later reverted raises the floor for that class, while the ones that held lower it.
  Done when: `fm lane brief` for a self-fix cites revert rates per tier and model for its area.

- **Show a weekly self-change scorecard: held, no effect, reverted, undone** — FEATURE — value 3 — effort S — risk low — category: visibility
  Why: the user can't trust autonomous change without seeing its net effect. Pair the count with the steer and correction rates so the claim and the number sit side by side (matches the standing rule on exam numbers).
  Done when: `fm doctor` and the site show the four counts with the denominator, and a net-negative week turns the self-fix trigger to propose-only automatically.

Next question: Which self-changes today have no recorded pre-change measurement, so their effect could never be scored even in principle?
Next question: When a self-change is reverted, what stops the signal-to-fix loop (T-2272) from filing the same fix again next week?
