---
id: T-1932
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T07:22:09Z
updated: 2026-10-29T08:04:07Z
base: 7f915dd44bd0792b968ec4fb4c8ddf3705acf88c
base_tree: 5672f564f40a656c6a96ccbd3e737d629a2fc0cd
plan0_at: 2026-10-29T07:50:15Z
plan0_scope: []
verified: strong
---
# Guard: system refusals for a program it can't read (a pipe into a shell, IFS, a script too
## Raw request
> Guard: system refusals for a program it can't read (a pipe into a shell, IFS, a script too long to parse) are still lifted by --allow system, though the message says the way through is a readable program; make them unliftable like T-1929's UNANALYSED (fmguard.py _unread, ~line 254)
## Interpretation
A system refusal for a program the guard can't read (_unread: a pipe into a shell or interpreter, IFS games, a script nested too deep or too long to parse) is lifted by --allow system. Nothing else in that program was checked, so a grant lets an unread program write core or remove anything. T-1929 made the UNANALYSED caps unliftable; these are the same kind of refusal.
## Assumptions (confidence)
## Acceptance criteria
- [x] every _unread system refusal (pipe into a shell, IFS, too deep, too long) stays refused under --allow system and its message names no grant; other system refusals are still lifted — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
Options: (a) in check(), treat got == 'system' and _unread(detail) like unanalysed(detail), so no grant lifts it; (b) fold the _unread strings into UNANALYSED (no: they are patterns, not fixed strings, and a substring match on other categories would catch paths); (c) leave system liftable and add a second finding in another category (no: more findings for one cause). Choice: (a), one clause in check() limited to category system; message() already omits --allow for these. Test: each unread shape is still refused with --allow system, its message says no grant lifts it, and a plain system refusal is still lifted by the grant.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test-first: table of unread shapes under --allow system; one clause in check(); message says no grant lifts it
## Resume here
<!-- auto -->
- 2026-10-29T07:51:34Z step 1/1: Test-first: table of unread shapes under --allow system; one clause in check(); message says no grant lifts it
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1931.txt
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 299 tests in 8.8s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 3801a7fda964] (2026-10-29T07:55:45Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_hooks` → ✗ exit 1 · Ran 504 tests in 67.0s (114 classes, 16 at a time; slowest: Stop 66s, NoTaskGate 53s, PreToolUse 50s) / FAILED (1 classes) [ran] [tree fc2761ef26c6] (2026-10-29T08:01:07Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_hooks` → exit 0 · Ran 504 tests in 46.0s (114 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 33s, PreToolUse 29s) / OK [ran] [tree fc2761ef26c6] (2026-10-29T08:02:51Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 299 tests in 8.8s (88 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree fc2761ef26c6] (2026-10-29T08:03:15Z)
- (audit intent) `one fm-reviewer pass (T-1932-review): 3 MEDIUM and 1 LOW, all fixed test-first; red on HEAD for all three unread details, green after` → every unread-program system refusal (pipe into a shell, IFS, too deep, parse budget, over 256 KB, sed -f, vim -S) stays refused under a system grant; other system refusals still lift [tree fc2761ef26c6] (2026-10-29T08:03:15Z)
- (audit adversary) `one fm-reviewer pass (T-1932-review): 3 MEDIUM and 1 LOW, all fixed test-first; red on HEAD for all three unread details, green after` → no bypass; free text containing the phrase can only over-refuse (T-1934 captured) [tree fc2761ef26c6] (2026-10-29T08:03:15Z)
- (audit edge) `one fm-reviewer pass (T-1932-review): 3 MEDIUM and 1 LOW, all fixed test-first; red on HEAD for all three unread details, green after` → sed -f and vim -S now get a hint (-e, -c); 256 KB script covered by a test [tree fc2761ef26c6] (2026-10-29T08:03:15Z)
- (audit operator) `one fm-reviewer pass (T-1932-review): 3 MEDIUM and 1 LOW, all fixed test-first; red on HEAD for all three unread details, green after` → the 3rd-repeat advice says do what the refusal says, not fm ask (hooks test) [tree fc2761ef26c6] (2026-10-29T08:03:15Z)
- (audit maintainer) `one fm-reviewer pass (T-1932-review): 3 MEDIUM and 1 LOW, all fixed test-first; red on HEAD for all three unread details, green after` → one unliftable() predicate shared by check, _message and fmhooks [tree fc2761ef26c6] (2026-10-29T08:03:15Z)
## Log
- 2026-10-29T07:22:09Z created
- 2026-10-29T07:43:28Z planned: it has criteria and steps
- 2026-10-29T07:50:15Z focused
- 2026-10-29T07:56:10Z tier S: 11 lines in 2 files, a strict tightening (only refusals that are already made without a grant)
- 2026-10-29T08:04:05Z done
- 2026-10-29T08:04:07Z committed 6237a093 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1929-review: Changes needed. The three caps are now unliftable and `check()` ordering is sound. One refusal in the same class is still liftable, and the `unan…
- T-1929 [SECURITY M, done, 1 steps] Guard refusals for lines too tangled to analyse are never lifted by a grant — lesson: Match refusal kinds on exact strings, never subs…
- research T-1924-review: Verdict: changes needed.** One adversary finding is real and new. The relative-`cd` change lets a line pass that was refused before. I ran nothin…
- decision 2026-10-21: T-1298: refusals for programs the guard couldn't read drop the --allow system route instead of keeping it
- the similar finished task took 1 steps
## Lessons
- A new unliftable class must reach every site that offers a grant: the message, the repeat advice and check; share one predicate
## Files touched
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmhooks.py
- plugin/tests/test_hooks.py
