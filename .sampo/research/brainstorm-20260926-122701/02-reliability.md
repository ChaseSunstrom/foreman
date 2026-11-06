# Brainstorm — lens: reliability

- **Fall back to the last committed guard when the working-copy guard raises** — FIX — value 5 — effort M — risk med
  Why: T-0033. A half-applied guard edit made every write fail closed, and recovery needed an unusual command. The fallback must stay fail-closed for `core`, `remote` and `plugin`; assumption: the committed copy can be loaded from git or a cached snapshot without a network call.
  Done when: a test that injects a syntax error into the working-copy guard still sees `rm -rf` blocked, a plain `fm` recovery command allowed, and a doctor line naming the fallback.

- **Add a guard regression corpus of legitimate and adversarial commands** — FIX — value 4 — effort M — risk low
  Why: the guard's text heuristics blocked the agent's own legitimate edits (quoted paths, "claude plugin" strings). The doctor warning is about 2 hook errors caused by this.
  Done when: a fixture file of at least 40 allow and block cases (including those two known false positives) runs in the test suite, and any heuristic change that flips a case fails the test.

- **Give hooks a crash breadcrumb and an error budget in doctor** — FIX — value 4 — effort S — risk low
  Why: `fm doctor` shows "2 hook errors" but the pack gives no way to see the cause. Assumption: hook exceptions are currently logged only as counts.
  Done when: a forced exception in each hook type writes one line (hook, exception, timestamp) to a size-capped local log, and `fm doctor` prints the latest cause.

- **Make state writes atomic and locked, with a crash-injection test** — FIX — value 4 — effort M — risk med
  Why: assumption: `fm sync` imports before each command, `fm run` and background reviewers all write concurrently, but the pack does not confirm temp-file-plus-rename or locking.
  Done when: killing a writer mid-write leaves parseable state, and 20 parallel `fm` writes lose no updates.

- **Save reviewer output tails automatically and add `audit prep --note`** — FEATURE — value 4 — effort M — risk low
  Why: reviewer output files are huge and the agent saves the tail by hand. That is error-prone, and findings can be lost. T-0031 is the same lens-brief problem.
  Done when: `fm audit record <file>` stores the bounded verdict and findings tail in the audit record, and `fm audit prep --note "..."` appears in every lens brief.

- **Test that rules, eval copies, MASTER and CHANGELOG do not drift** — CLEAN — value 3 — effort S — risk low
  Why: every behaviour change touches MASTER.md, CHANGELOG, the rules and the eval copies of the rules. The rules file is near its 60-line budget.
  Done when: a test fails if the eval rules copy differs from the plugin rules, the rules file exceeds its line budget, or a CHANGELOG entry is missing for a changed hook or CLI command.

- **Add a no-progress watchdog to the Stop-hook drive loop** — FIX — value 3 — effort M — risk med
  Why: the Stop hook forces continuation while background reviewers leave the agent idle-waiting. Assumption: there is no bound on consecutive drives that change no state.
  Done when: N consecutive continuations with no evidence, step or audit change stop the drive, and the reason is recorded and shown in the next `fm status`.

- **Add a "done elsewhere" status for captured requests** — FIX — value 2 — effort S — risk low
  Why: T-0032. A request finished inside another task can only be marked "dropped", which misreports the outcome.
  Done when: `fm` can mark a request done-elsewhere with a task reference, and status, queue and audit views show it distinctly from dropped.
