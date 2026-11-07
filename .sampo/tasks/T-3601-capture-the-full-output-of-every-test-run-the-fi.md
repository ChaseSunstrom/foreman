---
id: T-3601
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-07T03:47:45Z
updated: 2026-11-07T03:47:45Z
steer_method_rate: 0.218
---
# Capture the full output of every test run the first time it runs (to a log file or by…
## Raw request
> why do you need to rerun tests to figure out which oine failed, why cant you just see it? again, why do I even need to say this
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Capture the full output of every test run the first time it runs (to a log file or by not truncating it, with no `tail`, `head`, or `grep` that discards failure details), so the failing tests, their names, and the error messages are visible without a rerun.
- Never rerun a test suite just to learn which tests failed or why. Read the output already captured. Rerun only after a code change, or when a specific failure needs a narrower run with more verbosity or isolation.
- Report failures from that output by name, with the assertion or error text and file:line, before proposing a fix.
- Use the runner's own failure summary (for example a failures-only report, JUnit/JSON output, or `--tb`/verbose flags) so the failing set is explicit in one pass, and configure that on the first run rather than after a failure.
- When a run is long, pipe it with `tee` to a log file so the complete output stays on disk and can be re-read or searched without executing again.
- Apply this to every test, lint, type-check, and build command, not only the test suite, and to every project and session, without being reminded.
- Where the project's test command, scripts, Makefile, CI config, or CLAUDE.md define how tests run, update them (or note it there) so full failure output is kept by default, and keep this as a standing instruction in memory.
- This is local and non-destructive, so act on it directly. Anything outward-facing (pushing, publishing, CI changes on a remote) still needs the user's explicit go-ahead.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-07T03:47:45Z created
## Follow-ups captured
