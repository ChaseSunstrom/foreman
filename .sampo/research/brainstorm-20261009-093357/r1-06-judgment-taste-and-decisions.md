# Brainstorm — lens: judgment, taste and decisions

- **Sort every fork into one-way and two-way doors** — FEATURE — value 5 — effort M — risk low — category: judgment
  Why: assumption: Foreman asks or proceeds by tier, not by how hard a choice is to undo. Interrupts are a recurring complaint in the steers and asks.
  Done when: a mid-task fork touching a schema, public CLI name or deletion is tagged one-way and escalated, while a two-way fork is decided and logged with a one-line revert recipe, shown by a test over both kinds.

- **Order plan steps by uncertainty removed per cost** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: planning.md has passes but the pack shows no rule for step order. Failures after step 6 of 7 come from risky unknowns left until last.
  Done when: `fm task plan` marks each step with an unknown (high/low) and a cost, and for a fixture plan it puts the cheapest disconfirming probe first.

- **Run a Chesterton's-fence check before any deletion** — FEATURE — value 4 — effort S — risk low — category: judgment
  Why: the user said cleanup requests never got done, and cleanup is becoming a gate. Deleting blind is the opposite failure.
  Done when: a CLEAN brief that removes code must carry a "why it existed" line from git log or blame and the callers searched, and the done-gate rejects a deletion without it.

- **Detect sunk cost and replan fresh at half budget** — FEATURE — value 4 — effort M — risk low — category: reasoning
  Why: the drive blocks after 3 failed attempts. Nothing re-estimates "start over from here" against "continue" before then.
  Done when: at 50% of a step's time or attempt budget a recon pass writes a from-scratch estimate beside the continue estimate, and the ledger records which was chosen and why.

- **Write a regret ledger by comparing outcomes with the rejected options** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: M/L briefs already list 3+ options but never revisit them. Outcome data (rework, reverts, blocks) is already in the ledger.
  Done when: for a finished task with rework, `fm regret T-xxxx` prints the chosen option, the best rejected one by hindsight, and the signal that tipped it.

- **Set a "good enough" bar and a gold-plating tripwire at intake** — FEATURE — value 4 — effort S — risk low — category: judgment
  Why: assumption: the briefs have acceptance criteria but no stopping rule. Without one, polish and scope creep look like diligence.
  Done when: the brief has a done-ness bar line, and the drive flags edits outside the criteria's files after all criteria are checked.

- **Argue against each FEATURE before it is built** — FEATURE — value 4 — effort S — risk low — category: judgment
  Why: the user's drops are mostly "YAGNI" or "working as intended". A built-in steelman for not building would reach those verdicts earlier.
  Done when: a FEATURE M/L brief has a "case against" with a cheaper alternative and a skip recommendation, and a test shows a duplicate of an existing command gets "skip" proposed.

- **Learn the user's rules by quizzing with contrast cases** — FEATURE — value 5 — effort M — risk med — category: taste
  Why: steers like "budget limits shouldn't block until 75%" are stored as one-off statements. A threshold or exception is the thing that generalises wrongly.
  Done when: after a steer, Foreman drafts 3 borderline cases, the user's yes/no answers refine the stored rule, and later matching cases cite that rule.

- **Order precedence between the user's words, vetoes, decisions, lessons and defaults, and show which one won** — FEATURE — value 4 — effort S — risk low — category: decisions
  Why: the pack has many memory kinds (vetoes, decisions, lessons, tripwires) with no stated order. Conflicts surface as surprises.
  Done when: a one-page precedence table is enforced in recall output, and each recalled item shows "applied" or "overridden by X".

- **Pin exemplar files as the taste reference for builders and reviewers** — FEATURE — value 4 — effort M — risk low — category: quality
  Why: the rule is to write code that reads like the surrounding code, but nothing selects which code is the model one. A reviewer lens can only check against a named exemplar.
  Done when: `fm exemplar add path` stores it, builders get it in their prompt, and a taste lens flags a diff that departs from it.

- **Wild: Play a ten-second taste duel in idle moments** — FEATURE — value 3 — effort M — risk med — category: taste
  Why: wild. Pairwise "which diff or wording do you prefer?" cards are quick to answer and build the taste model faster than explicit interviews.
  Done when: 10 answered duels change a stored preference weight, and a later plan cites that weight.

- **Wild: Hold a coin-flip re-decision audit** — FEATURE — value 3 — effort M — risk low — category: judgment
  Why: wild. Randomly re-decide 1 in 20 logged decisions blind with a different model, and treat disagreement as a signal to review the decision, not as a verdict.
  Done when: the nightly job picks a decision, re-decides it from its inputs, and files a review item only if the two disagree.

- **Wild: Keep a "road not taken" shelf** — FEATURE — value 3 — effort S — risk low — category: decisions
  Why: wild. Keep rejected approaches with their revisit triggers, and surface one when its blocking reason has changed, for example a dependency upgrade or a Claude Code feature.
  Done when: a rejected option with a trigger reappears in a task's recall once the trigger condition is true.
