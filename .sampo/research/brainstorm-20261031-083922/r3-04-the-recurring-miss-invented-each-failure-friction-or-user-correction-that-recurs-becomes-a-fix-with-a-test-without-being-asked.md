# Brainstorm — lens: the recurring miss (invented): each failure, friction or user correction that recurs becomes a fix with a test, without being asked

- **Mine the "asked" stream for sibling gaps** — FEATURE — value 5 — effort M — risk low — category: recurrence
  Why: T-2285's "plan gate misses an option starting with a flag or code" and T-2289's "lane rm refuses .fm-scratch" are each one instance of a class (parser assumes prose; cleanup assumes known folders), found only after the user hit them. Assumption: asked lines share enough shape to cluster by touched module.
  Done when: closing a FIX from an asked line files one sibling-probe task per other verb sharing its parser or cleanup function, each with a failing-first test, and a fixture with two planted siblings yields exactly two tasks.

- **Turn each "what earlier brainstorms missed" ask into a permanent regression fixture** — FEATURE — value 5 — effort S — risk low — category: regression
  Why: the pack lists T-2285, 2288, 2289, 2290, 2291, 2292, 2326, 2327 as asks no idea predicted. They are already closed, but nothing says the same failure stays closed. Assumption: each has a reproducible input.
  Done when: `fm doctor` lists every missed-ask task id with a fixture path, and deleting one fixture turns doctor red naming the task.

- **Detect the user repeating a steer in different words** — FEATURE — value 4 — effort M — risk med — category: corrections
  Why: steers 2026-10-31 #1 to #3 restate the earlier "don't skip for budget" and "end-of-run exam" rules; repeats mean the first check didn't hold. Assumption: a cheap lexical plus Haiku match is enough to pair them.
  Done when: a second steer whose cold-read match to an existing rule exceeds a threshold prompts "same rule as <id>, its check ran N times and did not fire; here's why" instead of a new row.

- **Make a recurrence count against the fix that claimed it** — FEATURE — value 5 — effort M — risk low — category: fix survival
  Why: T-2272 opens fixes on 3+ recurring tasks, but the pack shows no step that reopens or demotes a fix whose signature returns. Assumption: signatures are stored with the closing task.
  Done when: replaying a signature after its fix closes reopens that task with "recurred after T-NNNN", and the signal-to-fix loop will not file a second duplicate.

- **Require the new test to fail on the pre-fix commit, automatically** — FEATURE — value 4 — effort M — risk low — category: test integrity
  Why: `fm task prove` exists for the user-facing path, yet correction-born fixes (T-2285, 2289) are small and a test that passes both ways is easy to write. Assumption: prove can be called from `fm task finish` for tasks of type FIX.
  Done when: finishing a FIX whose test passes on the start tree is refused, naming the test.

- **Count friction as a signal: retries, repeated commands, hand-edits after a plan** — FEATURE — value 4 — effort M — risk med — category: friction
  Why: the signal-to-fix loop reads failure signatures only; the earlier question "smallest plan edit the user makes most often" has no collector. Assumption: events already log commands and edits.
  Done when: an identical command run 3 times in a session, or the same plan section edited after acceptance in 3 tasks, appears as a friction signature and feeds the loop.

- **Rank recurring misses by cost to the user, not by count** — FEATURE — value 4 — effort S — risk low — category: prioritization
  Why: three failures in cheap tasks outrank one ship-red that blocked the whole queue under the current 3+ rule. Assumption: minutes and re-fix counts are recorded (T-2290 predictions suggest so).
  Done when: the loop's queue sorts by minutes lost plus reverts, and a fixture shows one costly miss ahead of three cheap ones.

- **Fence self-repairs per class with a visible autonomy level** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: mission 8 lets Foreman fix itself; the guard and hooks must stay intact (§6). Assumption: file paths define the class.
  Done when: a self-fix touching the guard, hooks or the lean-ratchet files is created as a proposal needing one yes, and a test confirms the diff is not applied unattended.

- **Show a weekly "missed, fixed, stayed fixed" line** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: nothing tells the user whether corrections are shrinking. Assumption: the user reads fm doctor.
  Done when: fm doctor prints counts of misses opened, closed and recurred over 7 days, matching a seeded ledger.

- **Wild: Replay a past correction against today's build nightly** — FEATURE — value 4 — effort M — risk low — category: regression
  Why: wild; the asked stream is a free corpus of inputs where Foreman once behaved wrongly. Assumption: most can be rebuilt as a command and an expected result.
  Done when: a nightly job runs the last 30 days of corrections and files a task for any that now reproduce, and a planted regression is caught within one run.

- **Wild: Mutation night for the repairer** — FEATURE — value 3 — effort L — risk med — category: self-testing
  Why: wild; a fix loop that is never attacked may be quietly weak. Assumption: a mutator can break one gate at a time on a worktree.
  Done when: each night one gate is mutated, the suite must go red, and a mutant that survives files a "gate X has no teeth" task.

- **Wild: A "that again" key** — FEATURE — value 4 — effort S — risk low — category: corrections
  Why: wild; the user's cheapest signal is frustration. Assumption: a two-word reply can be detected in the prompt hook.
  Done when: typing "that again" files a recurrence on the previous reply's verb, with the transcript excerpt, and shows the task id.

- **Wild: Repeat offender board** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: wild; five verbs probably cause most corrections. Assumption: corrections map to verbs.
  Done when: the web UI lists the top five verbs by corrections in 30 days, each linked to its open fix.

Next question: Which fixes closed in the last 30 days were actually re-fixed or reverted, and does the ledger say so?
Next question: What do the user's corrections have in common that a fixed list of signatures would never see?
