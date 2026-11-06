# Brainstorm — lens: false-alarm economics: every finding spends the user's attention; what makes a finding trustworthy enough to act on unasked (proof first, precision, ranking)

- **Refuse any finding without a red-to-green proof pair** — FEATURE — value 5 — effort M — risk low — category: trust gate
  Why: the exam shows deterministic finders hit 0/108, and "proves each finding with a failing test" is the mission. A finding that can't produce a test that fails on the tree and passes on the fix never reaches the user; it is stored as a "suspicion" and not counted.
  Done when: on a fixture with 5 planted bugs and 5 clean-looking decoys, `fm find` surfaces only findings whose stored test fails pre-fix and passes post-fix, and the decoys yield zero surfaced items.

- **Measure precision per finder and mute those below a floor** — FEATURE — value 5 — effort M — risk low — category: precision ledger
  Why: assumption: each finder (bug, security, perf, flake) has a different hit rate; users abandon noisy tools quickly. Foreman already keeps lens_rates for brainstorms, so the pattern exists.
  Done when: `fm find stats` prints per-finder surfaced/accepted/dismissed counts, and a finder whose accepted rate stays under a configured floor over N=10 surfaced findings is auto-muted, with a journal line saying so.

- **Rank by expected value minus attention cost** — FEATURE — value 5 — effort M — risk med — category: ranking
  Why: the mission asks for ranking "by value". Rank score = P(real) × impact ÷ (fix effort + review minutes). P(real) comes from the proof state and the finder's precision. Assumption: impact can be approximated from blast radius (callers, hot files from `fm map`).
  Done when: given 6 findings with known outcomes, the ranking puts the 2 real high-impact ones above the 4 noise or low-impact ones, and each shows its score inputs.

- **Cap unasked findings per day with a budget the user sets** — FEATURE — value 4 — effort S — risk low — category: attention budget
  Why: the premise is "every finding spends attention". Scout already has MAX_CAPTURES, so a cap exists in spirit. Overflow findings wait in a digest and are never discarded.
  Done when: with a cap of 3 and 8 proven findings, exactly 3 are surfaced today, 5 sit in `fm find backlog`, and tomorrow's run surfaces the next top 3.

- **Reject a fix that makes a test pass by hardcoding it** — SECURITY — value 4 — effort M — risk med — category: fix integrity
  Why: a find→prove→fix pipeline with unattended lanes invites a fix that satisfies its own test without fixing the bug. Mutation of the test's inputs (a second, held-out input) catches it.
  Done when: a fixture fix that returns the test's literal is rejected by the generated variant input check, and a correct fix passes.

- **Run each new finder on a clean repo first and ship only if it stays silent** — FIX — value 4 — effort S — risk low — category: none-kind guard
  Why: the exam grades Mission 3 on the `none` kind (repos with no defects) as well as `bug`. A finder that flags a clean repo is penalised. Keep a corpus of known-clean repos as a release gate.
  Done when: CI runs all finders on 5 pinned clean repos and fails if any finding is surfaced.

- **Show a one-line "why you can trust this" on every finding** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: attention spent is lower when the evidence is visible at a glance: the failing test name, its output line, the file and line, and the command to rerun it.
  Done when: every surfaced finding renders the test id, the assertion message, and a copy-pasteable rerun command in under 4 lines.

- **Remember dismissals as fingerprints so a finding never returns** — FEATURE — value 4 — effort S — risk low — category: dismissal memory
  Why: assumption: the fastest way to lose trust is to show the same rejected finding again. Key on (rule, symbol, normalized code hash) so it survives line shifts, and reopen only if the code changes.
  Done when: dismissing a finding, then moving it 40 lines and rerunning, does not surface it; editing the flagged function does.

- **Gate Foreman's own setup failures out of user-project findings** — FIX — value 3 — effort S — risk low — category: scope hygiene
  Why: the pack notes probe_doctor may queue Foreman setup failures as tasks in user projects. That is a false alarm by construction.
  Done when: a project with a broken Foreman hook produces a `fm doctor` warning but no backlog task.

- **Escalate a finding's confidence with a second independent prover** — FEATURE — value 3 — effort M — risk med — category: cross-check
  Why: the pack already has "second cold review". A different model writes its own repro from the finding text alone; agreement raises the rank, disagreement demotes it.
  Done when: on a fixture of 10 findings, findings where the independent repro fails are demoted below those where it succeeds, with both results recorded.

- **Wild: Price each finding in minutes of the user's attention** — FEATURE — value 3 — effort M — risk low — category: attention price
  Why: wild. Show "costs you ~2 min to review, saves ~40 min if real", learned from how long the user actually took on past findings. Findings below break-even are held.
  Done when: the surfaced list shows a review-minutes estimate per finding, updated from measured past review times.

- **Wild: A bet ledger where Foreman stakes credibility on each finding** — FEATURE — value 3 — effort S — risk low — category: calibration
  Why: wild. Foreman states a probability that each finding is real, records the outcome, and prints a calibration curve; a poorly calibrated finder gets its stated confidence rescaled.
  Done when: after 20 resolved findings, `fm find calibration` shows predicted versus observed rates per bucket and applies a correction that reduces the Brier score on the next 10.

- **Wild: Plant canary bugs in a scratch copy to grade the finders before they touch the real repo** — FEATURE — value 4 — effort L — risk med — category: self-test
  Why: wild. The exam's planted defects are an outside signal. Mutating a scratch copy of the user's own project and checking that the finders catch the plants gives a per-repo recall estimate, which tells the user how much silence is worth.
  Done when: `fm find --calibrate` plants 10 mutations in a copy, reports recall, and a finder with recall under a floor is labelled "blind here" in its output.

- **Re-verify a surfaced finding before the user sees it** — FIX — value 3 — effort S — risk low — category: staleness
  Why: assumption: findings queued overnight may be fixed by a later commit. Rerun the stored failing test at surface time and drop it if it now passes.
  Done when: a finding whose test passes on the current HEAD is auto-closed with a "resolved upstream" note and never shown.

Next question: What is the user's measured tolerance (dismissals in a row before they stop reading), and can the precision floor be set from it rather than guessed?
Next question: Does a proof-first gate lower recall on bug kinds that resist a unit test (concurrency, UI, config), and what second-best evidence should those carry?
