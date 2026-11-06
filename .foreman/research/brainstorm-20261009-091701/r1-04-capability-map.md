# Brainstorm — lens: capability map

- **Mutate the proof of a finished task** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: T-0342's criterion verified with `-k a or b`, which ran no tests, yet it counted as evidence. A passing gate says nothing if the tests can't fail. Mutation-testing tools (mutmut, Stryker) address this, and Foreman has no equivalent.
  Done when: `fm mutate T-id` applies small mutations to only the task's diff, reruns its linked tests, and reports survivors. A seeded test-free diff is reported as "unproven".

- **Reject empty verifications** — FIX — value 4 — effort S — risk low — category: verification
  Why: the `-k` incident above shows that a recorded pass can mean zero tests ran. Assumption: the test runners' output can be parsed for collected/ran counts.
  Done when: recording evidence whose command ran 0 tests is refused with "0 tests ran". A regression test covers the `-k` case.

- **Race competing attempts on a hard task** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: lanes, builders and gates exist, but each task gets one attempt. SWE-agent-style best-of-N would pay off on L tasks and on ones that fail their first gate. Assumption: budget pace allows it, since the user wants no caps before 75% usage.
  Done when: `fm lane race T-id --n 3` starts three worktrees with differing approach hints. It merges the one that passes the gates with the smallest diff and records the losers' summaries as lessons.

- **Run the queue as a dependency graph across lanes** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: `fm relate` already derives build-on edges, and JARVIS had 20+ queued tasks while the session idled. T-0401 only offers up to 3 tasks in turn. A scheduler could run independent tasks in parallel lanes and merge them in order.
  Done when: `fm run --lanes 3` runs two independent tasks concurrently and a dependent third only after its parent merges. A test confirms the merge order and that a conflict stops only the affected branch.

- **Bisect the regression a sentinel finds** — FEATURE — value 4 — effort M — risk low — category: self-repair
  Why: `fm sentinel` reports checks that now fail but stops there. Plugins like git-bisect-run automate the next step, and `fm why` already links commits to tasks.
  Done when: a failing sentinel check triggers an automatic bisect. It names the offending commit and task, then reopens that task with the failing output attached, tested on a seeded breakage.

- **Make the red team break the diff before done** — FEATURE — value 4 — effort M — risk low — category: review
  Why: reviewers read the diff, but nothing tries to falsify it. `fm audit` (T-0034) is deferred and is read-only lenses.
  Done when: a done-gate for M/L tasks runs an adversarial agent that must produce a failing test or a stated "no break found" with the attempts listed. A seeded bug is caught.

- **Replay the product journey and diff it per task** — FEATURE — value 4 — effort M — risk med — category: product check
  Why: `fm smoke` checks the product once at two viewports. The user asked for "checks the product the way its user uses it". Journeys could be saved and screenshotted before and after each task.
  Done when: `fm smoke --journey` replays recorded steps, attaches before/after screenshots to the brief and `fm pr`, and fails on an unexplained visual diff.

- **Test that resume survives compaction** — FEATURE — value 4 — effort M — risk low — category: context
  Why: resuming at the exact step is the core promise and T-0406 shows step state drifting from reality. No eval measures it.
  Done when: an eval takes a mid-task session, simulates `/compact`, and checks that the next action matches the checkpoint. It runs in `fm bench`.

- **Forecast cost and fit work to the budget** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: pace and budget are tracked per day and per task, and `fm cost` has history. Estimates come from the S/M/L guess only.
  Done when: `fm next` shows a predicted token range from similar past briefs. When usage runs ahead of pace, the drive prefers tasks that fit the remaining allowance.

- **Quarantine flaky gates** — FEATURE — value 3 — effort S — risk low — category: verification
  Why: T-0424 had to correct slow-gate stats from reused 0.0 s passes, so gate history is noisy. Assumption: flakiness exists in some projects' tests.
  Done when: a gate that flips pass/fail without a code change across three runs is flagged. It is reported as flaky rather than a regression, and logged to friction.

- **Turn production signals into briefs** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: intake only parses what the user pastes ("There's new bug feedback", T-0317). CI failures, issue trackers and crash logs could feed it, as Renovate and Sentry-to-ticket bots do.
  Done when: `fm intake --from ci|gh-issues` captures deduplicated briefs with the repro snippet and a source link. Running it twice creates no duplicates.

- **Train a taste proxy that pre-answers asks** — FEATURE — value 5 — effort L — risk high — category: autonomy — wild
  Why: `fm taste` knows kept, dropped and steered choices, and the user keeps pushing against being blocked (budget limits at 75%, no idle sessions). Assumption: past decisions predict low-risk approvals.
  Done when: in full autonomy a low-risk `fm ask` is answered from taste with its evidence cited in the ledger. Anything touching guard categories still goes to the user, and the user can undo the answer.

- **Run tasks in disposable microVM sandboxes** — SECURITY — value 4 — effort L — risk med — category: isolation — wild
  Why: the guard parses shell strings and keeps needing patches for new forms (T-0275, `bash -lc`, symlink `rm`). Parsing alone can't close every hole. A container or microVM with network policy would be a second layer for unattended `fm run`/`night`.
  Done when: `fm run --sandbox` executes a task in a throwaway container with only the lane mounted. A test shows a write outside the lane and an unlisted network call both fail.

- **Share bench-proven lessons between teams** — FEATURE — value 3 — effort L — risk med — category: learning — wild
  Why: `fm share` already exchanges lessons opt-in, and `fm bench` can score a lesson against replayed tasks. A signed pack would admit only lessons that don't regress the benchmark.
  Done when: `fm share pack` bundles redacted lessons with their bench delta. Importing one runs the bench and rejects a pack that lowers the score.

- **Dream overnight on old failures** — FEATURE — value 4 — effort L — risk med — category: self-improvement — wild
  Why: `night`, `evolve`, `friction` and `evals` exist separately. The user asked for recursive improvement of "yourself". T-0035 (eval capture) is deferred and would feed this.
  Done when: `fm night` picks a blocked or failed task, builds an eval from it, proposes an instruction change on an evolve branch, and leaves it for review only if it beats the bench.
