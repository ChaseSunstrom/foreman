---
id: T-1570
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T18:09:25Z
updated: 2026-10-22T19:35:21Z
done_in: T-1585
---
# Guard: env -u CLAUDECODE (or CLAUDE_CODE_ENTRYPOINT) in front of an fm command makes fm ve
## Raw request
> Guard: env -u CLAUDECODE (or CLAUDE_CODE_ENTRYPOINT) in front of an fm command makes fm verbs that read those variables (fm settings set, the safety gate's attended check) act as if run from the user's terminal; refuse unsetting or overriding them in a Bash command
## Interpretation
fm verbs read CLAUDECODE and CLAUDE_CODE_ENTRYPOINT to know Claude is running them (fm settings set consults the guard; the safety gate treats a run as unattended). A Bash command that unsets or overrides them (env -u CLAUDECODE, env -i, unset, CLAUDECODE=) makes those verbs act as if the user ran them. Refuse that in the guard.
## Assumptions (confidence)
## Acceptance criteria
- [ ] env -u CLAUDECODE, env -i, unset CLAUDECODE or CLAUDECODE= in front of a command are refused; ordinary env VAR=x cmd still passes — verify with `cd plugin/tests && python3 -m unittest test_guard.ClaudeEnv`
## Non-goals
## Approach (options → choice → why)
Options: have each verb also check a parent-process marker (fragile); chosen: a guard rule on the command text: env -u/-i, unset and assignments naming CLAUDECODE or CLAUDE_CODE_ENTRYPOINT are refused with a reason; reuses the env-prefix parsing the guard already has.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] refuse unsetting or overriding Claude Code's own variables
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T18:09:25Z created
- 2026-10-22T18:13:46Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-10-22T18:46:54Z batched into T-1585
- 2026-10-22T19:35:21Z done in T-1585 (batch)
## Follow-ups captured
