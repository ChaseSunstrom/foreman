# Brainstorm — lens: deepen: done-detection

- **Build a finish oracle compiler that every goal must pass to close** — FEATURE — value 5 — effort L — risk med — category: done-detection
  Why: Gen-0 #4 says it "knows when it's actually done rather than merely stopped"; the pack shows 58 empty coverage cells with no closure test. Assumption: goals today close on task status, not on an executable check.
  Done when: `fm goal close` refuses a goal with no oracle file, and a goal whose oracle command exits non-zero stays open, shown in a test.

- **Type every ending as done, stopped, shrunk or blocked** — FEATURE — value 5 — effort M — risk low — category: done-detection
  Why: the user's own steers separate "merely stopped" from done (usage-limit pauses, killed sessions, compaction). Assumption: the ledger records one "closed" state.
  Done when: the goal record carries an `ending` enum with a reason, and `fm next` treats only `done` as final, covered by a unit test per value.

- **Falsify the oracle at the goal's start commit** — FEATURE — value 5 — effort M — risk low — category: oracle-quality
  Why: the standing rule "T-2546 failed its bar; backtest before shipping" and `fm task prove` (test fails without the change) already exist at task scale. Assumption: no goal-scale equivalent.
  Done when: closing a goal runs its oracle against the start commit and refuses if the oracle already passes there.

- **Flag goals that finish by shrinking** — FEATURE — value 4 — effort M — risk low — category: done-detection
  Why: coverage cells may be filled with `n/a` to reach "no empty cells"; the user's rule counts only grounded cells. Assumption: row-count drops are not compared today.
  Done when: a goal whose plan lost more than N rows or whose cells moved to n/a without a recorded reason gets a `shrunk` ending flagged in `fm doctor`.

- **Re-derive done from the repo at every resume** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: the goal must survive "days, crashes and compactions"; a stored "done" can go stale after a revert. Assumption: resume trusts stored state.
  Done when: after a simulated crash plus a `git revert` of a closed row's commit, resume reopens that row, shown in an e2e test.

- **Bisect to the row that broke the oracle** — FEATURE — value 3 — effort M — risk low — category: regression
  Why: a goal's rows close at different commits; when the oracle later fails, nobody knows which row regressed. Assumption: oracle runs are per-goal only.
  Done when: `fm goal why-red` names the first commit and row at which the oracle fails, tested on a planted regression.

- **Grow a goal regression suite as rows close** — FEATURE — value 4 — effort M — risk low — category: regression
  Why: coverage.md cells are checked for existence by the sweep, not for still working (the open question about a cited path still firing). Assumption: closed cells are not re-run.
  Done when: each closed row appends its probe to a suite the sweep runs, and breaking a closed row's path turns the sweep red.

- **Mutate the finish oracle** — FEATURE — value 3 — effort M — risk med — category: oracle-quality
  Why: an oracle that passes broken code is the failure mode of "done". Assumption: oracles are never tested for sensitivity.
  Done when: a mutation pass flips a planted fault into the repo, and an oracle that still passes is reported as weak.

- **Verify the anti-goals before closing** — FEATURE — value 3 — effort S — risk low — category: done-detection
  Why: gen-0 MUSTs and NEVERs and the standing intent fence what must not happen. Assumption: goals list only positive criteria.
  Done when: a goal can carry `not:` checks, and one failing blocks closing with the check named.

- **Make oracle outcomes three-valued** — FEATURE — value 3 — effort S — risk low — category: done-detection
  Why: probes that cannot run on a non-Claude harness (an open question in the pack) are neither pass nor fail. Assumption: outcomes are boolean.
  Done when: oracle results are pass, fail or unknown, and any unknown blocks closing while naming the missing capability.

- **Map the blind regions before saying finished** — FEATURE — value 3 — effort M — risk low — category: coverage
  Why: the pack asks which cells have too few events to backtest. Assumption: no per-cell measurability is recorded.
  Done when: the finish report lists cells that are planted but unmeasured, and the goal's final line says "done except N unmeasured".

- **Wild: run an adversary lane that tries to prove the goal isn't done** — FEATURE — value 4 — effort L — risk med — category: adversarial
  Why: wild; the cold-read rule already uses a different model to catch gaming. A lane with one job, finding a user-visible gap the oracle misses, makes closing a contested verdict. Assumption: a spare cheap lane exists.
  Done when: the adversary's finding either files a new row with evidence or logs a "no gap found after N tries" line before close.

- **Wild: a finished? court with a blind prosecutor** — FEATURE — value 3 — effort L — risk med — category: adversarial
  Why: wild; a prosecutor sees only the original vague goal and the repo, never the plan, so it judges the goal as the user wrote it and not the plan's reading of it. Assumption: plan drift from the user's words is real.
  Done when: the prosecutor's list of unmet expectations is diffed against the plan and unmatched items become rows or recorded rejections.

- **Wild: plant a decoy open row to see if finish notices** — TEST — value 2 — effort S — risk low — category: self-test
  Why: wild; a canary. A hidden bogus row inserted at 90% progress proves the closure path actually reads the open list. Assumption: closure could silently skip rows.
  Done when: closing with a decoy present is refused, and a build that lets it through fails the nightly check.

- **Wild: goal autopsy letter on close** — FEATURE — value 2 — effort S — risk low — category: reporting
  Why: wild; the user reads the final report, not the ledger. A one-page letter says what finished, what was cut, what was never measured, and what the oracle cannot see. Assumption: the user wants one honest page.
  Done when: closing writes the letter into the final report, with each claim linked to a ledger line.

Next question: Which goals did the user close by hand while the plan still had open rows, and what did they know that the plan didn't?
Next question: Does anything in a goal's life (rows, oracle, ending) survive a change of harness mid-goal, such as Claude Code to `fm code`?
