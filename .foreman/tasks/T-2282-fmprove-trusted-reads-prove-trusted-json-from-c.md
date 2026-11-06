---
id: T-2282
type: SECURITY
tier: M
status: captured
priority: urgent
scope: []
depends_on: []
source: discovered
created: 2026-10-31T06:12:29Z
updated: 2026-11-06T03:53:55Z
---
# fmprove._trusted reads prove-trusted.json from c.state_dir(), which honours…
## Raw request
> SECURITY: fmprove._trusted reads prove-trusted.json from c.state_dir(), which honours FOREMAN_STATE/FOREMAN_HOME, so a session that sets FOREMAN_STATE to a folder holding its own prove-trusted.json makes any tree 'trusted' and fm prove / fm find --ladder run repo code: an env var counting as consent, against T-2202. Read the trust file only from the real home state (or refuse trust when the state dir is overridden), with a test
## Interpretation
fmprove._trusted reads prove-trusted.json from c.state_dir(), which honours FOREMAN_STATE/FOREMAN_HOME, so a command like 'FOREMAN_STATE=/tmp/x fm prove PATH' with a session-written /tmp/x/prove-trusted.json would count as the user's yes (T-2202 says no env var counts as consent). The same applies to fm find --ladder (T-2239).
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
1) a guard rule: a session's command that overrides FOREMAN_STATE or FOREMAN_HOME for an fm call is refused as core (the test runner sets them inside its own process, not on a command line); 2) read trust from a path derived from the install (PLUGIN_ROOT/../state) ignoring env — rejected: the test harness would then read and write the real user's trust file; 3) sign the trust file with a key in the real state — rejected: the key's location has the same env problem. Choice 1, but it widens the guard and its adversarial cases are guard-bypass forms, which the user stopped this run from enumerating: so it is built only on the user's go-ahead.
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-31T06:12:29Z created
- 2026-10-31T06:12:51Z set priority=urgent
- 2026-10-31T06:35:34Z blocked: needs the user (final report): the fix is a guard rule (refuse a session's fm command that overrides FOREMAN_STATE/FOREMAN_HOME); its adversarial cases are guard-bypass forms, which this run must not enumerate (the user's stop); process-local alternatives can all be forged by a session (analysis in Approach)
- 2026-11-06T03:53:55Z unblocked
## Follow-ups captured
