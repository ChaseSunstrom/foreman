# Brainstorm — lens: approaches

- **Mine hidden-test tasks from Foreman's own history** — FEATURE — value 5 — effort M — risk med — category: benchmarks
  Why: T-0866 and T-0867 are deferred for lack of cases, and the repo has ~1,277 closed tasks, most with tests added in the fix commit. Taking the commit's tests as hidden tests and the brief as the prompt gives realistic, multi-file cases at no authoring cost. Assumption: enough commits cleanly separate the tests from the fix.
  Done when: `fm bench mine` emits at least 20 cases, each with a base commit, a prompt and hidden tests that fail at base and pass at the fix, and a validation run confirms all of them.

- **Add a "native-max" control arm** — FEATURE — value 5 — effort M — risk low — category: benchmarks
  Why: the pack's only comparator is plain Claude Code. A sceptic will say that plan mode, the todo list and a good CLAUDE.md already give you most of Foreman. This arm is the fair rival and tests whether Foreman is more than that. Assumption: native features can be configured headlessly.
  Done when: the long-session suite reports three arms (plain, native-max, Foreman) with pass counts and cost per correct session.

- **Report expected spend per correct result, failures included** — FIX — value 4 — effort S — risk low — category: honesty
  Why: round 1 shipped cost per fully correct session, a mean over passing runs only. Plain passed 3 of 6 and Foreman 6 of 6, so a user who reruns until it works pays mean cost ÷ pass rate. Plain's shipped number leaves its failed runs out. Foreman wins by more under this measure, and the page can't be accused of flattering either side.
  Done when: the page shows total spend ÷ passing runs for both arms, with the formula in a tooltip and the figure generated from the results file.

- **Find the request-count crossover and use it** — PERFORMANCE — value 4 — effort M — risk med — category: ceremony
  Why: Foreman costs 10–50% more on short tasks and wins on 8-request sessions. Sweeping 1–8 sub-requests on Haiku would locate the break-even point. The hook would then switch to a thin profile below it. Assumption: the crossover is stable enough to hard-code.
  Done when: a published sweep names the crossover count, and a hook test shows prompts below it getting the thin profile.

- **Trace CI escapes back to the task that closed** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the Linux 3.12 CI went red on the 4-of-8 queue timing after tasks had closed green. Nothing links a later red build or reopened brief to the closing proof. That "escape rate" is the honest held-rate that T-0867 wants.
  Done when: `fm escapes` lists each red CI or reopened task with the task id that closed it, and the rate shows in `fm doctor`.

- **Restart from the ledger after two reds** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: repairing on top of a confused context is costly. A fresh context that reads only the brief, the lessons and the failing output may reach green for less. Assumption: the second attempt rarely needs the first attempt's dead ends.
  Done when: a seeded failing task goes from two reds to a fresh-context retry that passes. A bench row compares cost against continuing in place.

- **Have an adversary write edge tests before the code** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: plain Claude Code failed hidden tests in half the long sessions, which suggests missed edge cases per sub-request. A separate Haiku context that sees only the request writes the edge tests, so the implementer can't shape them. Cost is one cheap call per sub-request.
  Done when: on the long-session suite, adversary tests catch at least one defect that the model's own tests missed, and cost per correct session doesn't rise more than 10%.

- **Publish the ceremony Pareto frontier** — FEATURE — value 3 — effort M — risk low — category: benchmarks
  Why: with several ceremony levels run on the same cases, the page can show cost against pass rate. The shipped default would be the knee of that curve rather than a guess.
  Done when: the Benchmarks page plots at least three profiles and the default profile sits on the frontier.

- **Run independent sub-requests in parallel lanes inside a session** — PERFORMANCE — value 3 — effort L — risk high — category: speed
  Why: the user wants faster. The pack measures cost but not wall-clock, and T-0792 lanes sits deferred. Assumption: cost may rise from duplicated reads, so it is only worth shipping if time falls more than cost rises.
  Done when: an 8-request session with independent items finishes in at least 30% less wall-clock, and its cost per correct session is reported beside it.

- **Wild: evolve the config nightly under a dollar cap** — FEATURE — value 3 — effort L — risk med — category: self-tuning
  Why: assumption: the knobs (note budget, compaction window, ceremony profile) interact. A nightly Haiku search on paired seeds, capped at about $1, promotes a setting only if it wins on paired runs and passes the ratchet.
  Done when: a nightly job proposes a config change with a paired-run table, or a "no win found" entry.

- **Wild: re-execute any ledger point under different Foreman settings** — FEATURE — value 3 — effort L — risk high — category: debugging
  Why: `fm fork <turn>` would restore the worktree at a turn and replay the recorded tool results against a changed hook set. It shows where the injected notes and refusals diverge at zero model cost. Assumption: tool results replay deterministically enough.
  Done when: replaying a recorded session with one note type disabled prints the first divergent event and the byte difference.

- **Wild: let Foreman work its own deferred briefs as the live benchmark** — FEATURE — value 4 — effort L — risk med — category: dogfooding
  Why: more than 30 deferred "Later from…" briefs already exist with written criteria. Running Foreman and plain Claude Code on the same brief in sandboxed worktrees at a Haiku cap gives a continuing, real, unfaked scoreboard. Each brief is graded by its own verify command.
  Done when: one brief runs in both arms nightly, and the scoreboard records pass, cost and time for each.
