# Brainstorm — lens: the skeptical user (invented): does it do what the user meant, not what the test says; the user's own words become the acceptance check

- **Compile each user ask into a "meant-it" check the user can read** — FEATURE — value 5 — effort M — risk med — category: acceptance
  Why: the user's asks are phrased as outcomes ("fm lane rm refuses a lane holding .fm-scratch/: treat as throwaway"), yet the task closes on whatever tests the builder wrote. Plan-gate misses (T-2285) show the written check diverged from the stated intent.
  Done when: closing a task prints the user's original sentence beside the command that proves it, and `fm task finish` fails if any clause of the ask has no mapped check.

- **Run the user's sentence through a blind re-implementer** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: standing rule says weakness-finding must use signals Foreman didn't author. A cold child that sees only the user's words (not the plan or tests) writes a tiny behaviour probe; disagreement with the builder's tests is flagged.
  Done when: a task with a probe whose result differs from the builder's tests shows "meaning gap" on `fm task show` and blocks done until resolved.

- **Flag tests that pass on the pre-change tree for a different reason** — FIX — value 4 — effort M — risk low — category: proof
  Why: red-first exists, but a test can fail first for an unrelated cause (import error, missing fixture) and turn green for the wrong one. Assumption: `fm task prove` currently checks only fail→pass.
  Done when: prove records the failure message before the change and fails if it doesn't mention a symbol or path from the criterion.

- **Quote the ask's nouns in the diff evidence** — FEATURE — value 3 — effort S — risk low — category: traceability
  Why: asks name concrete things (`.fm-scratch/`, `--bench`, `fm mandate set`). A cheap check that each named token appears in the diff or in a run command catches work that satisfies a neighbouring problem.
  Done when: finish lists each backticked token from the ask with the file:line or command where it was touched, and an unmatched one is shown as "unaddressed".

- **Make "unproven" show the reason in the user's words** — FEATURE — value 4 — effort S — risk low — category: unproven rollup
  Why: T-2273 counts typed/inconclusive evidence, but the user can't tell which clause of their ask is the unproven one.
  Done when: each rollup row is "your ask: '…clause…' — only typed, no run", with one command to run the missing proof.

- **Replay the ask against a mutation of the fix** — FEATURE — value 4 — effort M — risk med — category: mutation proof
  Why: unit tests can pass while the behaviour the user meant is absent. Reverting one hunk at a time and rerunning the verify tells whether each change is actually load-bearing for the claim.
  Done when: finish reports hunks whose revert leaves every criterion green as "unwitnessed change".

- **Let the user write the acceptance line first, with a sample** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the steer log shows the user restating intent after builds ("also make sure the website is updated, it doesn't look like it has been"). An example input and expected output given at intake becomes the first red test.
  Done when: `fm task new --example "in → out"` creates a failing test from the pair, and closing without it passing is refused.

- **Verify docs claims against the shipped command by running them** — FEATURE — value 4 — effort M — risk low — category: docs proof
  Why: Mission 7 lists docs-against-code, and the website being stale was found by the user, not Foreman. README and site copy quote commands and numbers.
  Done when: `fm prove --docs` extracts fenced commands and quoted stats from README/site, runs or recomputes them, and lists any that mismatch.

- **Score the builder's "done" against the user's later corrections** — FEATURE — value 3 — effort M — risk low — category: outcome learning
  Why: dropped items ("premise doesn't hold", "already covered") and re-asks show meaning drift. Counting reopens/corrections per task kind gives a measured "meant-it rate", not a self-authored pass rate.
  Done when: `fm outcomes` prints meant-it rate per tier from user follow-ups within N days, and doctor warns when it falls.

- **Wild: Hire an adversarial user-twin that tries to prove the task didn't do what you meant** — FEATURE — value 4 — effort L — risk med — category: red team
  Why: wild; the skeptical user's habit is "show me". A tool-less child reads only the ask and the receipt, then lists three ways the work could satisfy the test but not the request.
  Done when: the receipt carries those three objections and each has a run command or an explicit "accepted by user" mark.

- **Wild: Make the user's exact words the commit message trailer and the site changelog line** — FEATURE — value 2 — effort S — risk low — category: legibility
  Why: wild; keeps the original sentence travelling with the change so later readers judge it against what was asked, not what was summarized.
  Done when: every merge commit carries `Asked:` with the verbatim text, and the genesis site page shows it.

- **Wild: Play back the behaviour as a one-screen before/after the skeptic can rerun** — FEATURE — value 4 — effort M — risk low — category: demo proof
  Why: wild; `fm shot`/`fm flow` exist for UI, but CLI and data tasks lack the equivalent. A recorded before/after transcript on the start tree and current tree answers "show me it does it".
  Done when: `fm task finish` attaches a replayable two-pane transcript, and a reviewer reruns it with one command.

- **Detect asks whose acceptance can't be machine-checked and say so up front** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: Mission 7 requires unprovable things be labelled. Better to label at focus time ("this ask needs your eyes") than at close.
  Done when: focusing a task lists clauses with no possible automated proof and routes them to a user-owned check row.

Next question: Which of the user's past asks were later reopened or re-asked, and what single clause of the original sentence did the shipped check not cover?
Next question: Where does a model write the check and the same model judge it, with no clause of the user's words in between?
