---
id: T-0155
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T07:00:19Z
updated: 2026-10-03T07:02:26Z
base: e696e454187e2d486e04d9c1fbfaf8548d0a9164
base_tree: d0f549a2acfdb77129c1b5082bc29d6a030bdcbe
verified: strong
---
# Guard: a backtick counts as execution unless every interpreter in the command treats it as text; versioned interpreter names are recognised
## Raw request
> Guard: a backtick counts as execution unless every interpreter in the command treats it as text; versioned interpreter names are recognised
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] versioned and alternative interpreter names running a backticked plugin install are blocked; the markdown heredoc still passes — verify with `python3 plugin/tests/run.py -p test_guard.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests, then fix
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, PluginChanges 0s, Publish 0s) / OK [ran] [tree 8a7411ad1a0e] (2026-10-03T07:02:26Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, PluginChanges 0s, Publish 0s) / OK [ran] [tree 8a7411ad1a0e] (2026-10-03T07:02:26Z)
- (audit adversary) `self-review against both automated findings, with the scratchpad check t155_check.py over every substitution form` → the regression (double-quoted backticks unread after T-0150) is fixed by extracting every backtick body outside single quotes and checking it recursively, so bare and double-quoted forms both reach check_bash; dollar-paren keeps its token path; single-quoted literals still read as a block (fails closed). A backtick now counts as execution unless every interpreter present treats it as text (default-deny instead of an allow list), and versioned or alternative names (ruby3.2, jruby, irb, php8.3) are recognised, which also widens when the interpreter checks run. t155_check.py: a recursive home delete in double-quoted backticks, in double-quoted dollar-paren and bare, and a force push in a substitution are all blocked; the guard test table covers the versioned-interpreter and mixed python+ruby cases; the markdown Python heredoc passes [tree 8a7411ad1a0e] (2026-10-03T07:02:26Z)
- (audit self) `self-review against both automated findings, with the scratchpad check t155_check.py over every substitution form` → no findings [tree 8a7411ad1a0e] (2026-10-03T07:02:26Z)
## Log
- 2026-10-03T07:00:19Z created
- 2026-10-03T07:00:20Z focused
- 2026-10-03T07:02:26Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- T-0150 [SECURITY S, done, 1 steps] Guard: a backtick counts as code execution only where it executes, and a claude call inside backticks is caught there
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- research T-0120-review: Verdict
- the similar finished task took 1 steps
- start here (files T-0150 touched): plugin/tests/test_guard.py, CHANGELOG.md, plugin/lib/fmguard.py
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A pre-tokenisation rewrite changes what every later check sees: fix gaps by adding a reader (extract and recurse), not by rewriting the input
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
