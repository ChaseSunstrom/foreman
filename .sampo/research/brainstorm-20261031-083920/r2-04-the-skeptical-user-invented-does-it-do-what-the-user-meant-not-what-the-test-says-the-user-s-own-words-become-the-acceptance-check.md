# Brainstorm — lens: the skeptical user (invented): does it do what the user meant, not what the test says; the user's own words become the acceptance check

- **Pin the ask's verbs and nouns as a checklist before work starts** — FEATURE — value 5 — effort M — risk med — category: intent proof
  Why: the user's recurring asks (T-2285, T-2288, T-2289) were each a literal edge case their earlier tests didn't cover; assumption: a mechanical extraction of the ask's nouns/verbs is cheap and free of model judgement.
  Done when: `fm task new` from a prompt writes an "Ask terms" list, and `fm task finish` fails when a term appears in neither the diff, a test name, nor an evidence line.

- **Require one test that fails for the reason the ask names** — FEATURE — value 5 — effort M — risk med — category: red-first
  Why: "Flag tests that pass on the pre-change tree for a different reason" was listed, but no capture of the failing message exists; the user's T-2285 miss was a test that passed on the wrong grounds.
  Done when: red-first evidence stores the failure text, and finish refuses if that text shares no Ask-term with the user's sentence.

- **Let the user write one acceptance line in their own words and run it** — FEATURE — value 5 — effort S — risk low — category: acceptance
  Why: pack steers show the user states the behaviour outright ("fm prove --migration runs up, down, up"); assumption: a `--meant "<cmd>"` slot on a task would be used when offered.
  Done when: `fm task new --meant "cmd"` stores a command the user owns, finish runs it, and a task with a model-written meant-command is labelled unproven.

- **Show the diff of behaviour, not code, at close** — FEATURE — value 4 — effort M — risk med — category: receipts
  Why: the user asked for a plain receipt (T-0795) and for "does it do what the user meant"; assumption: running the task's verify command on the start tree and the end tree, side by side, is the clearest proof.
  Done when: the close receipt prints "before: <output> / after: <output>" for the meant-command, in the user's words as the header.

- **Re-read the ask after the build, blind to the plan** — FEATURE — value 4 — effort M — risk med — category: cold review
  Why: the open question about writer and judge on both sides; a tool-less child sees only the user's sentence and the final behaviour and says whether the two match.
  Done when: finish records a verdict containing a verbatim quote of the ask; a verdict without a quote is advisory and shown as such.

- **Track the user's corrections as misses against the first "done"** — FEATURE — value 4 — effort S — risk low — category: outcomes
  Why: T-2285 and T-2289 are follow-ups to just-closed tasks (same family), evidence that the first done was premature.
  Done when: a task that spawns a FIX within a set window of closing is counted in `fm outcomes` as "reopened by the user", with the new ask quoted.

- **Mark a criterion that no command could falsify** — FIX — value 4 — effort S — risk low — category: unproven
  Why: unproven rollup counts typed evidence, but the pack shows no check that a criterion could fail at all; assumption: many criteria are phrased "works" with a verify of `true`.
  Done when: `fm task new` warns when a criterion's verify command exits 0 on the start tree, and the rollup lists these as "cannot fail".

- **Flag unrequested behaviour in the diff** — FEATURE — value 3 — effort M — risk med — category: scope
  Why: the skeptic's reverse question: did it do more than meant? The pack's plan-gate ideas cover missing rows, not extras.
  Done when: finish lists changed files and public behaviours with no Ask-term or plan row, each shown with a one-word accept key.

- **Offer a "meant it?" prompt on the user's first look** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: assumption: a one-key yes/no after a close, tied to the task, is the cheapest independent signal Foreman doesn't author.
  Done when: `fm task meant ID yes|no` records the answer, and the scorecard shows the yes-rate per tier and model.

- **Wild: Run the user's sentence through a literal-minded implementer** — FEATURE — value 3 — effort L — risk med — category: red team
  Why: wild; a child told to satisfy only the exact words, with minimal code, reveals ambiguity the real builder papered over.
  Done when: for an M/L task, the literal build's behaviour differs from the real one on a stored case, and the difference is shown as "your sentence allows both".

- **Wild: Make the commit message the user's quote with a replay command** — FEATURE — value 3 — effort S — risk low — category: traceability
  Why: wild; every commit trailer carries the verbatim ask and the one command that shows it working, so a stranger re-verifies from `git log`.
  Done when: `git log` on a shipped task shows an `Ask:` and `Replay:` trailer, and the replay command exits 0 on a clean checkout.

- **Wild: Run a weekly "did we mean it?" audit of last week's closes** — FEATURE — value 3 — effort M — risk low — category: proof decay
  Why: wild; replay each stored meant-command against the current tree and file a FIX for any that now fails or whose Ask-terms vanished from the code.
  Done when: the audit prints a pass/fail table and opens one task per failure.

Next question: Which of the user's own sentences have been closed as done but later contradicted by a steer, and what did those have in common?
Next question: Can a meant-command be inferred from the user's phrasing often enough to be the default, or must it always be asked?
