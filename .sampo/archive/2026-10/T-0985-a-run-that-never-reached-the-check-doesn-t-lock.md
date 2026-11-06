---
id: T-0985
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T22:50:55Z
updated: 2026-10-15T22:54:39Z
base: 8ba321469c3021b1ad1a51c94178850aeebac5ea
base_tree: 44d272be81357896efbbc575738e248e47d17cdc
verified: strong
---
# A run that never reached the check doesn't lock a criterion: fm task ac edit can fix a wrong verify path
## Raw request
> A run that never reached the check doesn't lock a criterion: fm task ac edit can fix a wrong verify path
## Interpretation
Both recorded demo sessions (T-0979) wrote a criterion whose verify command had a wrong path, ran it, saw it fail to even start, and then had to drop the task and recreate it, because any evidence locks the criterion (T-0342, to stop weakening a failing check). A run that never reached the check isn't a failing check; it shouldn't lock. Small models hit this hardest.
## Assumptions (confidence)
## Acceptance criteria
- [x] A criterion whose only evidence is runs that never reached the check (exit 127, or 'No such file', "can't open file", 'No module named X' or pytest's 'file or directory not found' naming a path or module from the verify command itself) can still be edited with fm task ac edit; a check that ran and failed for any other reason stays locked — verify with `python3 plugin/tests/run.py -k NeverRanUnlocks`
## Non-goals
## Approach (options → choice → why)
Options: has_evidence for the edit lock ignores runs whose output says the verify itself couldn't start, matched against a path or module the command names (chosen: keeps T-0342's protection for checks that ran); allow any edit with a logged reason (weakens the lock); make add-time unrunnable detection smarter (can't know a module path until it runs).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing NeverRanUnlocks tests
2. [x] has_evidence(ac=n) skips never-ran runs for the edit lock; the refusal names the reason; docs
## Resume here
## Docs impact
MASTER, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k NeverRanUnlocks` → ✗ exit 1 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: NeverRanUnlocks 1s) / FAILED (1 classes) [ran] [tree 377d042b4542] (2026-10-15T22:51:26Z)
- (step 1) `python3 plugin/tests/run.py -k NeverRanUnlocks` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: NeverRanUnlocks 1s) / OK [ran] [tree 6e4e0c1ece0c] (2026-10-15T22:52:26Z)
- (step 2) `python3 plugin/tests/run.py test_never_ran test_core test_verification test_execution test_hooks` → exit 0 · Ran 238 tests in 58.7s (49 classes, 16 at a time; slowest: Stop 59s, PreToolUse 35s, SessionStart 27s) / OK [ran] [tree 6f6a9156c095] (2026-10-15T22:54:27Z)
- (ac 1) `python3 plugin/tests/run.py -k NeverRanUnlocks` → exit 0 · Ran 2 tests in 3.0s (1 classes, 16 at a time; slowest: NeverRanUnlocks 3s) / OK [ran] [tree 6f6a9156c095] (2026-10-15T22:54:36Z)
- (audit intent) `self: red then green; the 'ran and failed' lock is tested to hold` → a wrong verify path is fixed in place, not by dropping and recreating the task [tree 6f6a9156c095] (2026-10-15T22:54:36Z)
- (audit adversary) `self: red then green; the 'ran and failed' lock is tested to hold` → only runs whose failure names a file or module the verify command itself names (or exit 127) are exempt, so a real failing check can't be edited weaker; the mark is written by fm from the real output, not typed [tree 6f6a9156c095] (2026-10-15T22:54:36Z)
- (audit edge) `self: red then green; the 'ran and failed' lock is tested to hold` → unittest 'No module named X', python 'can't open file', shell 'No such file or directory', pytest 'file or directory not found', exit 127 [tree 6f6a9156c095] (2026-10-15T22:54:36Z)
## Log
- 2026-10-15T22:50:55Z created
- 2026-10-15T22:51:02Z focused
- 2026-10-15T22:54:38Z done
- 2026-10-15T22:54:39Z committed afd3619 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0765 [FIX S, done, 2 steps] A verify that can't run at all (python3 -m <missing module>, an fm subcommand fm doesn't have) is refused when the criterion is added — les…
- T-0414 [FIX M, done, 3 steps] Guard: a data-reading python -c is judged by what runs before it — lesson: A parser that drops quoting can't be trusted about structure the…
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
## Why not caught
none: it took real sessions (the T-0979 recordings) to show the drop-and-redo; fm bench replays never wrote a wrong verify path
## Lessons
- A lock meant to stop weakening a failing check must not fire on a check that never ran: that's a typo, not a result
## Plan gaps
- failed first: step 1 Failing NeverRanUnlocks tests
## Files touched
- plugin/tests/test_never_ran.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
