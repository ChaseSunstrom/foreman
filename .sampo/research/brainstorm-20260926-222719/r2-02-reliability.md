# Brainstorm — lens: reliability

- **Reject test evidence when the run proves nothing** — FIX — value 4 — effort S — risk low
  Why: the pack's vacuous-verify lint is static ("can't fail", pipe hides exit). A command that exits 0 with "Ran 0 tests", "no tests ran" or all-skipped still passes, and `--affected` narrowing makes that likelier. Assumption: `fm check` and evidence capture see the runner's output.
  Done when: a criterion whose verify command collects 0 tests, or skips every test, is recorded as not-evidence, and a fixture test for pytest and unittest summaries shows it.

- **Detect test tampering at done** — SECURITY — value 4 — effort M — risk med
  Why: red→green (`fm task prove`) covers new tests. Nothing covers a task turning a red suite green by editing existing tests (deleting assertions, adding skip/xfail, loosening expected values, dropping the test count). Assumption: the per-task diff and the pre-existing test files are identifiable.
  Done when: a fixture task that weakens an existing test makes `fm task done` refuse until a reason is recorded or the user says yes, and a fixture that only adds tests passes untouched.

- **Validate audit verdicts as structured data** — FIX — value 4 — effort M — risk low
  Why: L tasks rely on one combined read-only reviewer pass, and a bad pass is invisible: empty, truncated, timed out, or "looks good" with no citations. Only brainstorm children have output validation. Assumption: the audit result is recorded from free-form reviewer text.
  Done when: `fm task done` accepts a lens as fresh only if the record has a verdict, the diff hash it covered, and at least one cited file or hunk per lens. An empty or truncated reviewer result, and a timeout, all leave the audit unmet.

- **Put an error boundary around every `fm` command** — FIX — value 3 — effort S — risk low
  Why: the pack covers hooks failing open, but not the CLI. An uncaught traceback burns tokens and leaves the model guessing whether to retry, fix its input or give up. Assumption: today's failures print raw tracebacks.
  Done when: exit codes are split into usage, gate-refused, state-problem and internal. An injected exception prints one line plus a crash-file path and no traceback, and a test asserts the exit code and line length for each class.

- **Check that every command reference resolves** — CLEAN — value 3 — effort S — risk low
  Why: 40 playbooks, the skills, the rules and the injected notes all name `fm` subcommands and flags. The pack has many "shrink or stub the text" ideas but no check that the references still exist. A stale one makes the model run a failing command and spend turns recovering.
  Done when: a test extracts each `fm …` invocation and file path from those texts and validates it against the argparse tree and the plugin layout. Renaming a flag fails it.

- **Run every child process non-interactively** — FIX — value 3 — effort S — risk low
  Why: the process-group kill and 12 h expiry suggest hangs already happen. Pagers, y/n prompts, TTY detection and color codes are still not normalized for verify commands, `fm quiet` and `fm run`. Assumption: children inherit the caller's stdin and env.
  Done when: children get stdin=/dev/null, `CI=1`, `PAGER=cat`, `NO_COLOR=1`, `GIT_TERMINAL_PROMPT=0`. A fixture verify command that waits for input fails within seconds and names the prompt, instead of waiting for the timeout.

- **Make mutating `fm` commands retry-safe** — FIX — value 3 — effort M — risk med
  Why: after a tool timeout, a compaction or a resumed session the model often repeats a command. Hook events are deduped and multi-step commands are journaled, but a repeated `fm task done` or `fm focus` can still double-apply or fail confusingly. Assumption: not all commands are idempotent today.
  Done when: each mutating command run twice in a row gives the same end state, and the second call says "already done: <what>" with exit 0. A table-driven test covers every mutating command.

The remaining reliability ideas (sync conflicts, more lock reaping, log rotation) are marginal next to the ~200 already listed, so I'm stopping at seven.
