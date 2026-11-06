# Brainstorm — lens: deepen: calibration

- **Unify the bet ledger into one write-once calibration table** — FEATURE — value 5 — effort M — risk low — category: calibration ledger
  Why: the category lists ~10 variants (confidence ledger, prediction row at plan accept, pre-registered rows, forecaster scoring). T-2290 already records predictions of minutes and attempts at focus. One append-only `calibration.jsonl` with kind (confidence, race-winner, ask-answer, minutes, attempts), stated value, evidence class, and outcome slot beats five separate stores.
  Done when: `fm calibration show` lists rows from at least three kinds, and a test shows that editing a closed row's stated value is refused.

- **Print a per-evidence-class reliability table in fm doctor** — FEATURE — value 5 — effort M — risk low — category: calibration report
  Why: T-2285/T-2288 and "Unproven rollup" show evidence kinds are already classified (run, typed, inconclusive). Stated confidence has never been scored against them.
  Done when: `fm doctor` prints buckets (e.g. 50/70/90%) × evidence class with n, hit rate and gap, and it prints "too few" under n=5 instead of a number.

- **Cap stated confidence by the strongest evidence present, with a learned cap** — FEATURE — value 4 — effort M — risk med — category: confidence cap
  Why: the plan gate (T-2269) demands a research note for low-confidence assumptions, but nothing stops "high" being claimed on typed evidence. Assumption: the cap starts hard-coded (typed ≤ 60%, run ≥ 90% allowed), then moves to the ledger's observed hit rate per class.
  Done when: closing a task with typed-only evidence and a stated 90% records 60% and prints why; a test moves the cap after seeded misses.

- **Show the recalibrated number beside the stated one** — FEATURE — value 4 — effort S — risk low — category: calibration display
  Why: a calibration curve only matters if the user sees it where decisions happen (plan, ask, close). Assumption: needs the reliability table above.
  Done when: a plan's confidence line reads "stated 85% → history says 68% (n=14)" and falls back to the stated value alone under the n threshold.

- **Score every stop: did the answer change the plan?** — FEATURE — value 5 — effort M — risk low — category: ask scoring
  Why: the standing rule is to stop only when irreversible and ambiguous (Mission 5 #8). Prediction of the user's answer before each `fm ask` plus a "plan diff after answer" check turns stops into a measurable rate. Stops whose answer matched the guess are candidates to auto-decide next time.
  Done when: `fm ask` writes a predicted answer row first, closing the ask scores match/changed-plan, and `fm triggers` shows the stop-useful rate.

- **Decay confidence when the files it rests on change** — FEATURE — value 4 — effort M — risk med — category: staleness
  Why: the pack's `fm graph blast` already knows file neighbours, and an assumption verified before a merge may be stale after it. Assumption: each confidence row stores the paths and tree hash it relied on.
  Done when: editing a path listed in a row flips it to "stale" in `fm task show`, and the done-gate asks for re-earning only on rows tied to the task's criteria.

- **Score the runner-up on close and report race regret** — FEATURE — value 4 — effort M — risk low — category: race regret
  Why: T-2271 races the runner-up only when stuck, and T-2277 names alternatives in the plan. When a chosen approach later gets re-fixed or reverted (the T-2291 router already reads that signal), we can see whether the rival would have fared better.
  Done when: a reverted task with a recorded rival shows "rival never tried" or "rival won the race"; `fm triggers` reports a rate of rival-would-have-won.

- **Flag plans where the readings and approaches agree too easily** — FEATURE — value 3 — effort M — risk med — category: ambiguity
  Why: the plan gate only counts options (3+ names); it cannot see three near-copies. Assumption: a cheap lexical or cold-Haiku distinctness check, with disagreement among independent readings as the ambiguity signal.
  Done when: a plan whose three Approach options share >80% of their tokens gets a gap naming it, and a test with three truly distinct options passes.

- **Lint plan prose for unsupported certainty** — FEATURE — value 3 — effort S — risk low — category: plan lint
  Why: the user's blocking-vs-advisory pattern (T-2246 quotes a clause or stays advisory) suggests the same grounded rule: words like "certainly" or "obviously" need an attached command or file reference, otherwise advisory.
  Done when: `fm task check` lists hedge or certainty words with no adjacent evidence reference, as advisory only, with a test on both.

- **Wild: Make lanes bet before they run** — FEATURE — value 3 — effort M — risk med — category: lane markets
  Why: wild. Each `fm lane race` lane files a predicted pass-probability and cost before starting. Winner selection stays evidence-based, but the surprise rate trains the router (T-2291) and shows which model/tier pairs are over-confident.
  Done when: a race writes one bet per lane, and `fm lane` prints Brier score per model after 10 races.

- **Wild: Weekly calibration quiz with a cold Haiku child betting on past tasks** — FEATURE — value 3 — effort M — risk med — category: external judge
  Why: wild. This answers "numbers never checked by someone other than the producer": a tool-less Haiku sees the task's plan only, bets on its outcome, and its Brier score is compared with Foreman's own. It is a signal Foreman didn't author, per the standing rule.
  Done when: `fm calibration quiz` reports Foreman's vs. Haiku's Brier on the last 20 closed tasks, using the zero-token arms when the budget is zero.

- **Wild: Autopsy each decision a week later** — FEATURE — value 3 — effort M — risk low — category: delayed scoring
  Why: wild. Many misses surface after close (reverts, re-fixes, red after merge, user rewording). A scheduled pass rescored closed rows at +7 days and amends the outcome slot via a new row, not an edit.
  Done when: a task reverted on day 5 shows an "autopsy" row that changes its bucket in the reliability table.

- **Price the miss: weight the Brier score by blast radius and reversibility** — FEATURE — value 4 — effort S — risk low — category: weighted scoring
  Why: `fm graph blast` gives a cost proxy, and the stop rule hinges on irreversibility. A miss in a 40-file blast should count more than one in a docs fix.
  Done when: the reliability table has a weighted column, and a test shows a high-blast miss moving it more than a low-blast one.

Next question: Which outcome signals (revert, re-fix, red after merge, user rewording) are trustworthy enough to score confidence against, and which are noise the user would reject?
Next question: When the calibrated number and the stated one diverge for a month, does the user want Foreman to act on it automatically (tighter gates) or only report it?
