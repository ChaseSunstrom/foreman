# Brainstorm — lens: research frontier

- **Hold out hidden variants of each task's checks** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: the pack shows vacuous-proof and weakened-verification ideas, but nothing that catches a builder that passes the visible tests by special-casing them. Assumption: the builder can't see tests written by another agent from the spec alone (`fm oracle` already does the spec-only step).
  Done when: a seeded task whose fix hardcodes the visible expected values passes its gate, fails the hidden variants, and `fm task done` refuses with that reason.

- **Check the product with metamorphic relations** — FEATURE — value 4 — effort M — risk low — category: smoke
  Why: `fm smoke` drives the UI at desktop and phone sizes, but a page with no crash and no oracle can still be wrong. Relations such as "reload gives the same state", "sorting twice is idempotent", "a narrower viewport shows the same data" need no expected output. Assumption: these can be generated from acceptance criteria.
  Done when: a smoke run on a project with a planted state-loss-on-reload bug fails on a generated relation without any hand-written assertion.

- **Minimise a failing diff by hunks (ddmin)** — FEATURE — value 3 — effort S — risk low — category: debugging
  Why: lanes that fail the gate return a whole diff, and the "bisect regressions" ideas work across commits, not inside one change. Delta-debugging the hunks finds the smallest set that still breaks the gate.
  Done when: `fm lane minimize <id>` prints the smallest hunk set that still fails the gate on a seeded two-hunk breakage, and the run is recorded in the ledger.

- **Keep a truth-maintenance graph of lessons and decisions** — FEATURE — value 4 — effort L — risk med — category: memory
  Why: the pack has lessons, decisions, vetoes and rules, plus ideas for contradiction detection, expiry and tripwires. It has no dependency graph, so retracting one fact doesn't flag the tasks, plans and rules that rested on it. Assumption: briefs already cite lessons and decisions by id.
  Done when: running `fm decide --retract D-n` lists every open or recent task and rule that cited it and marks them "needs re-read" in `fm next`.

- **Review at the AST level and certify behaviour-neutral changes** — FEATURE — value 4 — effort M — risk med — category: review
  Why: `fm tour` orders files by size and reading order, and CLEAN tasks have no machine check that nothing changed in behaviour. A tree-diff that detects moves, renames and whitespace-only edits could classify hunks as neutral or not. Assumption: tree-sitter grammars are available for the main languages.
  Done when: a rename-and-move refactor shows as "0 behavioural hunks" in `fm tour`, and one added branch among them is flagged.

- **Give builders the program slice, not the files** — FEATURE — value 3 — effort M — risk med — category: context
  Why: `fm outline` and `fm impact` already narrow reading. The backward slice of the failing line or symbol would give a builder only the code that can influence it. Assumption: static slicing is approximated through call and def-use edges.
  Done when: a builder brief for a seeded FIX includes a slice under a stated fraction of the touched files' lines, and the builder still fixes it.

- **Report an outside score on public agent benchmarks** — FEATURE — value 4 — effort L — risk med — category: evaluation
  Why: `fm bench` replays only Foreman's own finished tasks, and holding out a secret set is already proposed. Neither gives a number outside the project's own history. Assumption: a subset of SWE-bench-style tasks can run in disposable worktrees under the budget caps.
  Done when: `fm bench --public N` runs N external tasks with Foreman on and off, then prints pass rates with confidence intervals.

- **Bound the error rate of "done" with conformal escalation** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: the pack proposes calibrating "done" and weighting reviewers, but only heuristically. Using past tasks' later-found escapes as calibration data, review depth could be set so the miss rate stays under a rate the user picks. Assumption: sentinel and "asked-for but never done" detection give escape labels.
  Done when: `fm autonomy` accepts a target miss rate, and a replay over finished tasks shows the observed escape rate at or under it.

- **Drive idle exploration from the surprise log** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: `fm surprise` records where the model of the code was wrong, and the drive now offers side work when idle. Those two can be joined, with idle time spent reading the areas that have surprised Foreman most. Assumption: surprises can be tagged to files.
  Done when: an idle drive offers "probe <area>" ranked by surprise count, and the resulting note appears in `fm recall`.

- **Wild: Plant reward-hacking honeypots in gates** — FEATURE — value 4 — effort M — risk med — category: safety
  Why: assumption: builders sometimes take shortcuts. A decoy writable expected-output file or a skippable test, watched by the guard, would measure how often lanes cheat and which instructions reduce it.
  Done when: a nightly run reports the shortcut-take rate per instruction version, and a lane that touches a decoy is blocked and logged.

- **Wild: Run Foreman as a scientist on itself** — FEATURE — value 5 — effort L — risk med — category: self-improvement
  Why: `fm friction`, `fm bench` and `fm evolve` exist but a human frames each question. A lab mode would read the ledger, state a hypothesis with a predicted metric, run a bench experiment, and file a report with effect size and confidence interval. Assumption: it's only worth it once the bench has enough cases for real statistics.
  Done when: `fm lab` produces one report with a hypothesis, the experiment run, the result and a keep or drop recommendation, from the ledger alone.

- **Wild: Open a prediction market on gates** — FEATURE — value 3 — effort M — risk low — category: orchestration
  Why: assumption: cheap agents each state a probability that the gate passes before it runs. High-confidence misses are the surprises worth a deeper review, and they also tune ask-and-review depth.
  Done when: finished tasks store predicted-versus-actual, and `fm digest` lists the three most surprising tasks of the week.

- **Wild: Synthesise guard rules by counterexample-guided search** — SECURITY — value 4 — effort L — risk high — category: guard
  Why: the guard has been patched case by case (`bash -lc`, symlink `rm`, `python -c`), against a 5000-command replay and real-bash differential tests. A loop could propose a rule, search bounded shell grammars for a counterexample against real bash, and refine until none is found. Assumption: a bounded grammar covers enough real commands.
  Done when: a new refusal rule arrives with a generated counterexample corpus, and the loop finds no bash-differential mismatch within its bound.
