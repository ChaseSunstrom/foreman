---
id: T-0988
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py,plugin/tests/test_hooks.py,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-15T23:15:46Z
updated: 2026-10-15T23:16:53Z
base: 3f282cf736d41186fd2520c6070b70ec5f265e69
base_tree: 4430e0dcb0ac7214a7f85a4334c82dbc1b966ce8
verified: strong
---
# SessionStart appends Foreman's exports to the env file on every start/compact: the Bash prelude repeats them (8x seen)
## Raw request
> SessionStart appends Foreman's exports to the env file on every start/compact: the Bash prelude repeats them (8x seen)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two SessionStarts of one session write the exports once — verify with `python3 plugin/tests/run.py -k SessionStart`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] write only what isn't there
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k SessionStart` → ✗ exit 1 · Ran 13 tests in 10.5s (1 classes, 16 at a time; slowest: SessionStart 10s) / FAILED (1 classes) [ran] [tree e13f76601c27] (2026-10-15T23:16:03Z)
- (step 2) `python3 plugin/tests/run.py -k SessionStart` → exit 0 · Ran 13 tests in 10.6s (1 classes, 16 at a time; slowest: SessionStart 10s) / OK [ran] [tree ed86d17392a2] (2026-10-15T23:16:21Z)
- (step 2) `python3 plugin/tests/run.py -k SessionStart` → exit 0 · Ran 13 tests in 10.6s (1 classes, 16 at a time; slowest: SessionStart 10s) / OK [ran] [tree 2343fb58f89e] (2026-10-15T23:16:41Z)
- (ac 1) `python3 plugin/tests/run.py -k SessionStart` → exit 0 · Ran 13 tests in 10.6s (1 classes, 16 at a time; slowest: SessionStart 10s) / OK [ran] [tree 2343fb58f89e] (2026-10-15T23:16:52Z)
- (audit edge) `self: read the writer; the env file is shared by every SessionStart hook, so 'not in' rather than 'endswith'; an unreadable file appends as before` → a new session id is a new pair and is appended; a missing file is created [tree 2343fb58f89e] (2026-10-15T23:16:52Z)
- (audit self) `self: read the writer; the env file is shared by every SessionStart hook, so 'not in' rather than 'endswith'; an unreadable file appends as before` → no findings [tree 2343fb58f89e] (2026-10-15T23:16:52Z)
## Log
- 2026-10-15T23:15:46Z created
- 2026-10-15T23:15:47Z focused
- 2026-10-15T23:16:53Z done
- 2026-10-15T23:16:53Z committed d2fa96a (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-0370 [FIX M, done, 2 steps] Guard: a $(…) substitution no longer turns off variable tracking, so a literal S=/tmp/… stays known — lesson: Before widening what the guar…
- decision 2026-09-26: fm sync keeps the automatic import at session start and before fm commands: imported content can't grant, mark runs, count as audits or take focus, …
- likely tests for the scope: plugin/tests/test_hooks.py
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
