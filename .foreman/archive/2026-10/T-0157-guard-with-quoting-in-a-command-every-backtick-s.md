---
id: T-0157
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T07:03:50Z
updated: 2026-10-03T07:04:51Z
base: 73f121d880b311df568c3060a43be65d297ea6a9
base_tree: 8a7411ad1a0ebeb61a445d729d15571e7e44e163
verified: strong
---
# Guard: with $'…' quoting in a command, every backtick span is checked
## Raw request
> Guard: with $'…' quoting in a command, every backtick span is checked
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an ANSI-C quoted escaped quote before a live backtick no longer hides it — verify with `python3 plugin/tests/run.py -p test_guard.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then fix
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, PluginChanges 0s, Authorization 0s) / OK [ran] [tree 6920922e566e] (2026-10-03T07:04:50Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: GitDestructive 0s, PluginChanges 0s, Authorization 0s) / OK [ran] [tree 6920922e566e] (2026-10-03T07:04:50Z)
- (audit adversary) `self: one early return in _backtick_bodies; the two new rows were red before` → the reviewer's input (an ANSI-C quoted escaped quote before a live backtick) and a plugin-install variant now block; any command using dollar-single-quote reads every backtick span, including ones that are really single-quoted (fails closed, may over-block); the quote scan is unchanged otherwise [tree 6920922e566e] (2026-10-03T07:04:50Z)
- (audit self) `self: one early return in _backtick_bodies; the two new rows were red before` → no findings [tree 6920922e566e] (2026-10-03T07:04:50Z)
## Log
- 2026-10-03T07:03:50Z created
- 2026-10-03T07:03:50Z focused
- 2026-10-03T07:04:51Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0150 [SECURITY S, done, 1 steps] Guard: a backtick counts as code execution only where it executes, and a claude call inside backticks is caught there
- T-0155 [SECURITY S, done, 1 steps] Guard: a backtick counts as execution unless every interpreter in the command treats it as text; versioned interpreter names are recog…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- similar finished tasks took 1–1 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
