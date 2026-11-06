---
id: T-0159
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T07:18:35Z
updated: 2026-10-03T07:19:50Z
base: 4d30413aa915940090c0dc8761904fcc4f4a4a89
base_tree: 131a7e0e06b561d03c531cc841f29605f6b464db
verified: strong
---
# Guard: shell keywords before a command (do, then, else, elif, if, while, until, {, !) no longer hide it
## Raw request
> Guard: shell keywords before a command (do, then, else, elif, if, while, until, {, !) no longer hide it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a recursive home delete after do/then/else/{/! in loops, ifs and groups is blocked — verify with `python3 plugin/tests/run.py -p test_guard.py`
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
- (ac 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: PluginChanges 0s, GitDestructive 0s, RmOutside 0s) / OK [ran] [tree 71b791d474ce] (2026-10-03T07:19:50Z)
- (step 1) `python3 plugin/tests/run.py -p test_guard.py` → exit 0 · Ran 44 tests in 0.1s (15 classes, 16 at a time; slowest: PluginChanges 0s, GitDestructive 0s, RmOutside 0s) / OK [ran] [tree 71b791d474ce] (2026-10-03T07:19:50Z)
- (audit adversary) `self: one set of keywords skipped where wrappers are skipped; rows for loops, ifs, else, groups, negation and a force push in a loop were red first` → keywords are skipped only as leading words of a simple command, as bash parses them; a command literally named do/then can't exist in bash at that position, so nothing new passes; case arms were already split at ); scratch t151_check.py shows every keyword form blocked now [tree 71b791d474ce] (2026-10-03T07:19:50Z)
- (audit self) `self: one set of keywords skipped where wrappers are skipped; rows for loops, ifs, else, groups, negation and a force push in a loop were red first` → no findings [tree 71b791d474ce] (2026-10-03T07:19:50Z)
## Log
- 2026-10-03T07:18:35Z created
- 2026-10-03T07:18:35Z focused
- 2026-10-03T07:19:50Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- research T-0108-review: [instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok
- research t0018-final-adversary: HIGH** — `plugin/lib/fmguard.py:201-222` (`classify_tree` / `_new_context_file` / `_protected_roots`) — Tree-write commands (`cp -r`, `ta…
- T-0144 [SECURITY L, done, 3 steps] Guard: leave out only real top-level fm --run arguments from the interpreter claude-check (a fake --run in a heredoc or -c body hid co…
- similar past tasks were L: consider --tier L
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
