# Brainstorm — lens: what the user would notice and love

- **Show a "what changed since you left" card on session start** — FEATURE — value 5 — effort M — risk low — category: delight
  Why: The user runs long drives and sleeps through night-shift work, then must reconstruct state. The pack has fm tour, fm pr, and the UI pane, but nothing greets a returning user with a before/after. Distinct from the "morning report" idea: this diffs the ledger, so it works after any absence, not only at night.
  Done when: after a session with 3 finished tasks, starting a new one prints a ≤10-line card listing the tasks closed, the gates that went red then green, spend, and the one decision needing the user's yes.

- **Add a one-key "explain this refusal" for every hook block** — FEATURE — value 4 — effort S — risk low — category: transparency
  Why: Three guard false positives in the friction log (git stash list, python heredoc, read-only state reads). The user hits blocks and can't tell guard bugs from real policy. Existing ideas cover learning from false positives, not the in-the-moment message. Each block should name its rule, the matching token, and the exact `fm allow` line.
  Done when: blocking `git stash list` prints rule id, matched fragment, and a copy-pasteable narrow allow command, and a test asserts all three appear for each guard category.

- **Type the first-time-close streak into the pane** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the user shows the pane to others. Reviewers find 3–7 real issues every batch, so a "closed first time, zero audit findings" counter is rare and meaningful. It is the honest version of the "celebrate a clean close" idea, tied to real evidence rather than confetti.
  Done when: a task that closes with no gate reruns and no reviewer findings increments a streak shown in the UI, and any reviewer finding resets it, covered by a foreman-ui test.

- **Make `fm doctor` take a crash-recovery drill** — FIX — value 4 — effort M — risk low — category: reliability
  Why: Four zero-byte git objects broke `git diff` and doctor passed. Existing ideas say "detect corrupt objects". Go further: doctor also tests that each state file parses, that the ledger's last line is whole, and that hook scripts are executable, then prints one repair command per fault.
  Done when: a test seeds an empty loose object and a truncated ledger line, and doctor exits nonzero naming both with a repair command.

- **Show the cost of a request before accepting it** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: The user has repeatedly stressed tokens and cost ("without sacrificing cost"). Budgets cap after the fact. At intake, estimate spend from similar finished tasks by tier and type in recall, and show a range with the tier chosen.
  Done when: `fm task new` on a request similar to three finished M tasks prints an estimated dollar range from their actual spend, and says "no history" when there is none.

- **Wild: Let the user ask "what would you do differently" and get a replayed diff of the plan** — FEATURE — value 3 — effort L — risk med — category: counterfactual
  Why: wild. Users steer mid-task ("criterion widened", "verify corrected") often. Re-run planning with the correction applied from step zero and show how the plan would have differed, so the user learns which words steer Foreman best.
  Done when: `fm whatif ID "<steer>"` prints a step-by-step plan diff for a finished task without touching its state.

- **Wild: Generate a one-page "Foreman year in review" HTML** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. The ledger, bench, lessons, and friction history make a shareable story: tasks closed, bugs caught by gates, lessons that fired, the bench trend line. It is something people show others, and it exercises the data pipeline.
  Done when: `fm recap --html` writes one self-contained file under 200 KB with no external requests and contains task counts that match the ledger.

- **Wild: Add a "pair mode" where Foreman narrates its intent in one line before every risky edit and the user can veto by typing** — FEATURE — value 3 — effort M — risk med — category: collaboration
  Why: wild. The user's "no" is already a veto, but only after they speak. Pre-announcing turns steering into a first-class, low-friction interaction and feeds the veto store with real data.
  Done when: with pair mode on, an edit to a file in a configured risky glob emits an intent line and pauses until a one-word reply, and the reply "no" is stored as a veto.

- **Wild: Offer a self-explaining `fm next` that answers "why this and not that"** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: wild. Hints now go quiet when ignored, so the user sees less and may not know why. A `--why` flag lists the candidates considered and what ranked the chosen step first.
  Done when: `fm next --why` prints at least two rejected candidates with a one-line reason each, drawn from the real queue.

- **Merge the overlapping inbox items into three named pipelines and cut the rest** — CLEAN — value 4 — effort S — risk low — category: scope
  Why: The inbox lists about 17 planned items, many overlapping (bench judge, regression court, shadow-user soak, counterfactual ledger, skill duels). Recommend merging them into "proof" (judge, regression court, counterfactual), "soak" (shadow-user, stranger test), and "scout" (landscape, release watch). Cut debate-pair review and shadow plan review, since the single reviewer already finds real issues and these double child spend.
  Done when: the inbox shows at most 10 items, each merged item links its absorbed sources, and the cuts are recorded as decisions with revisit triggers.
