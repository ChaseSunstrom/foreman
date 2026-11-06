---
id: T-1934
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T07:57:58Z
updated: 2026-10-29T08:26:30Z
base: 775098ad511c46ff7dd238eb26796e8127c56b84
base_tree: 87f4530dba61a428c94e787f000126c54824c380
plan0_at: 2026-10-29T08:23:27Z
plan0_scope: []
verified: strong
---
# The `_unread` substring test on free text (the T-1929 pattern) remains. A path such as /et
## Raw request
> the `_unread` substring test on free text (the T-1929 pattern) remains. A path such as /etc/"can't read" makes an ordinary system-folder refusal unliftable
> (noticed by an agent; research T-1932-review)
## Interpretation
A system refusal whose path holds "can't read" is taken for a program the guard never read, so the user's system grant can't lift it. Match the guard's own wording instead.
## Assumptions (confidence)
## Acceptance criteria
- [x] A system grant lifts a refusal whose path holds can't read — verify with `python3 plugin/tests/run.py test_guard -k couldnt_read`
## Non-goals
## Approach (options → choice → why)
Every guard message for unread text says "the guard can't read"; test that phrase. Rejected: list every message exactly (brittle as messages change).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test, then the narrower phrase
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_guard -k couldnt_read 2>&1 | grep -E "^(FAIL|AssertionError|Ran|OK|FAILED)"` → ✗ exit 1 · Ran 301 tests in 11.8s (88 classes, 16 at a time; slowest: Mutation 11s, GuardAgainstBash 9s, Trust 8s) / FAILED (1 classes) [ran] [tree ccb8835bf5d4] (2026-10-29T08:23:54Z)
- `python3 plugin/tests/run.py test_guard -k couldnt_read` → ✗ exit 1 · Ran 301 tests in 9.6s (88 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 7s, Trust 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6dceaba00d1a] (2026-10-29T08:24:53Z)
- `python3 plugin/tests/run.py test_guard -k couldnt_read` → exit 0 · Ran 301 tests in 8.8s (88 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 6dceaba00d1a] (2026-10-29T08:24:53Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_evasions test_guard_exec_vectors` → exit 0 · Ran 301 tests in 12.1s (88 classes, 16 at a time; slowest: Mutation 12s, GuardAgainstBash 9s, Trust 8s) / OK [ran] [tree d38640e44997] (2026-10-29T08:26:01Z)
- (ac 1) `python3 plugin/tests/run.py test_guard -k couldnt_read` → exit 0 · Ran 301 tests in 8.8s (88 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree d38640e44997] (2026-10-29T08:26:17Z)
- (audit adversary) `Narrowed one substring test to the guard's own phrase; every guard message for unread text holds it (grep of fmguard); red-green proved; guard + hook suites 506 OK; replay cases clean` → a path holding the whole phrase still reads as unread, which only over-refuses (the safe direction); no unread-program refusal lost the phrase [tree d38640e44997] (2026-10-29T08:26:17Z)
- (audit edge) `Narrowed one substring test to the guard's own phrase; every guard message for unread text holds it (grep of fmguard); red-green proved; guard + hook suites 506 OK; replay cases clean` → the existing unread cases (IFS, sed -f, vim -S, written-then-run, too long, too deep) all stay unliftable in the same test [tree d38640e44997] (2026-10-29T08:26:17Z)
- (audit self) `Narrowed one substring test to the guard's own phrase; every guard message for unread text holds it (grep of fmguard); red-green proved; guard + hook suites 506 OK; replay cases clean` → no findings [tree d38640e44997] (2026-10-29T08:26:17Z)
## Log
- 2026-10-29T07:57:58Z created
- 2026-10-29T08:23:25Z set tier=S, type=FIX
- 2026-10-29T08:23:26Z planned: it has criteria and steps
- 2026-10-29T08:23:27Z focused
- 2026-10-29T08:26:28Z done
- 2026-10-29T08:26:30Z committed fc8f4374 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1932-review: Changes needed. The core change is correct, but the third-refusal advice still points to a grant that can't help, and one unread-program refusal …
- T-1936 [FIX S, done, 1 steps] The `"too deep" in f[1]` substring test at 4072 and 4080 also matches `("rm-outside", "com — lesson: Match guard refusals by their exact te…
- research T-1929-review: Changes needed. The three caps are now unliftable and `check()` ordering is sound. One refusal in the same class is still liftable, and the `unan…
- decision 2026-10-21: T-1298: refusals for programs the guard couldn't read drop the --allow system route instead of keeping it
- the similar finished task took 1 steps
## Why not caught
The T-1932 tests checked unread messages and an rm-outside path, never a system refusal whose path held the words
## Lessons
- A test on refusal text should key on wording only the guard writes, not words a path can hold
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
