# Brainstorm — lens: reliability

- **Fall back to a committed copy of the whole hook path, not just fmguard** — FIX — value 5 — effort M — risk med
  Why: T-0037. A bug in fmcore stopped the hook from loading the active task, so core grants vanished and the fix was refused. The committed fallback covers only fmguard.
  Done when: a test injects a raise into the working-copy fmcore, and the hook still loads the active task with its core grants and `fm status` still runs from the committed copy.

- **Add `fm recover`, a standalone stdlib script that works when fmcore is broken** — FEATURE — value 5 — effort S — risk low
  Why: the user had to run `git checkout` by hand after the lockout. Assumption: a script with no fmcore imports can restore `plugin/lib` from HEAD after a yes prompt.
  Done when: with fmcore deliberately corrupted, `fm recover` prints the diff, asks for the user's yes, restores the files, and `fm doctor` passes.

- **Warn right after an edit leaves plugin/lib unimportable** — FEATURE — value 4 — effort S — risk low
  Why: two self-lockouts today (guard, then core library). Assumption: a PostToolUse import check limited to edits under `plugin/lib` fits the 150 ms budget.
  Done when: after an edit that breaks an import, the next hook output names the file, the error and the `fm recover` command. Edits elsewhere add no measurable latency.

- **Make state loading tolerant per field and quarantine bad files** — FIX — value 4 — effort M — risk med
  Why: one unreadable task field currently disables the whole task, its grants and `fm` itself. Assumption: the loader is all-or-nothing today.
  Done when: a task file with one malformed field loads with defaults and a doctor warning, and a wholly corrupt file is moved to `state/quarantine/` without blocking other tasks.

- **Run a corpus of legitimate agent edits through the guard in the test suite** — FIX — value 3 — effort S — risk low
  Why: the guard blocked the agent's own heredoc edits, quoted paths and "claude plugin" strings, and each guard regression was caught only by the full suite.
  Done when: a fixture of at least 30 legitimate commands must all pass, a matching set of dangerous commands must all block, and the test fails on any change in either set.

- **Test that the rules and eval copies match the source rules file** — CLEAN — value 3 — effort S — risk low
  Why: every behaviour change touches MASTER.md, CHANGELOG, the rules and the eval copies of the rules, and the rules file is near its 60-line budget.
  Done when: a test fails if the eval copies differ from the source rules or the rules exceed the line budget, and the message names the differing file.

- **Have `fm audit run` write a bounded structured findings file (T-0034)** — FEATURE — value 4 — effort L — risk med
  Why: reviewer output is huge and the agent saves the tail by hand, so findings can be lost, and a background reviewer makes the agent idle-wait.
  Done when: each lens produces a findings file with a size cap and fields for severity, file and claim, and `fm audit` shows the same counts the done gate uses.

- **Let `fm run` resume after usage limits with persisted backoff** — FIX — value 3 — effort M — risk med
  Why: known limitation, "`fm run` stops at usage limits". Assumption: the limit reset time can be read from the error output.
  Done when: a simulated limit error leaves the queue intact and `fm run` resumes at the recorded time without repeating finished steps.
