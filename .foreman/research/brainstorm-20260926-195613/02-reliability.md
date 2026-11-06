# Brainstorm — lens: reliability

- **Prove regression tests fail without the fix** — FEATURE — value 5 — effort M — risk med
  Why: the pack says Foreman can't tell a weak test from a real regression test except by TDD instructions. Assumption: the frozen diff from `fm audit prep` can be reverted in a scratch copy.
  Done when: for a FIX task, `fm task done` refuses if the new test also passes on the pre-change tree (run in a temp `git worktree` or copy, never the user's tree), and accepts one that fails before and passes after. A unit test covers both cases.

- **Capture a baseline and classify flaky vs. regression** — FEATURE — value 4 — effort M — risk low
  Why: `fm check` only knows "exit 0", has no baseline, and has no flaky detection.
  Done when: `fm focus` records the pre-change gate results. On a failure, `fm check` reruns that gate N times, then labels it `preexisting`, `flaky` or `regression` in the evidence and ledger. A test with a deliberately unstable stub is classified `flaky`.

- **Match new failures against past fixes** — FEATURE — value 4 — effort M — risk low
  Why: the pack says failure causes aren't collected or matched against earlier fixes, and 3 failures just block the task.
  Done when: each failure is stored in the ledger as a normalized signature (command, first error line, touched files). A repeat signature adds one factual line to the "Next" note (≤400 chars) that cites the earlier task and its fix. A test replays two failures and sees the citation.

- **Measure "Next" hint compliance and promote ignored steps to gates** — FEATURE — value 4 — effort M — risk med
  Why: the pack says the "Next" line is only a hint and Claude can ignore procedures. Assumption: PostToolUse events are enough to judge whether the following action matched the hint.
  Done when: `fm doctor` prints a per-procedure ignore rate from the ledger. A procedure ignored more than X% of the time is flagged as a gate candidate. Hook p95 stays under 150 ms.

- **Fix T-0040 and T-0042, the two inbox reliability bugs** — FIX — value 3 — effort S — risk low
  Why: both are in the inbox. The guard treats `git fetch` as a tree write, and `fm task new --ac` can't attach verify commands, so M/L tasks made that way can't be focused.
  Done when: `git fetch` passes the guard while `git push` and `git reset --hard` are still handled as before. `fm task new --ac "text::cmd"` yields an M task that `fm focus` accepts. Each has a test.

- **Run targeted tests first, using a learned file-to-test map** — PERFORMANCE — value 3 — effort M — risk med
  Why: Foreman doesn't know which tests cover which files. Assumption: evidence records tie changed files to passing test commands.
  Done when: `fm check --fast` runs the mapped tests for the changed files before the full gate. The full gate is still required by `fm task done`, which keeps a wrong mapping from giving false confidence. A test shows that a wrong mapping still fails at done.

- **Attach a check and revisit trigger to each decision** — FEATURE — value 3 — effort M — risk low
  Why: in full autonomy nothing later checks whether a recorded decision held up or was reversed.
  Done when: decisions.md rows gain `check` and `scope` fields. When a later task touches that scope, or a check fails, the decision is surfaced once in the "Next" note. Reversals are logged.

- **Turn each blocked or failed task into an eval case** — CLEAN — value 3 — effort M — risk low
  Why: `claude plugin eval` has only 5 cases, and the pack names it the regression referee.
  Done when: `fm evals add <task>` generates a case from a blocked task's ledger. The suite grows from 5 and stays green.
