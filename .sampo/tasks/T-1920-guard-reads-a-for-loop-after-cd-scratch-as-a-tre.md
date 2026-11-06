---
id: T-1920
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T05:23:35Z
updated: 2026-10-29T06:04:22Z
base: a2204d4d2dee3896d46d65c3fc522f78aae31fbe
base_tree: d0087b515b986838667f1090a0f8598bb62ecf78
plan0_at: 2026-10-29T05:53:14Z
plan0_scope: []
verified: strong
---
# Guard reads a compound after 'cd <scratch> &&' as a tree write over Foreman
## Raw request
> Guard reads a for loop after 'cd <scratch> && ' as a tree write over Foreman, though the hint names that very route (cherry-picks in a loop in a scratch worktree were blocked as core)
## Interpretation
A cd before && into an existing scratch folder should hold through a for/while/if/{ } compound after it; today any compound keyword makes the whole line branchy, so the cd is never certain and Foreman's tree stays a possible cwd.
## Assumptions (confidence)
## Acceptance criteria
- [x] A for/while/if/{ } compound with no cd-like word in it, after 'cd <scratch> &&', runs in the scratch folder; adversarial cases (a cd inside, a ; or || after, fake or escaped keywords, a redirect-made separator, a newline-split fake opener) still block as core — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
Options: (a) mask each innermost compound whose body names no cwd mover (cd pushd popd eval source . trap mapfile readarray) to one word in _top, so 'cd X && C' is an && chain; (b) a sticky 'in a compound' flag in the walk plus masking (cds inside stay uncertain, but a loop repeats: a later cd moves the next pass's earlier commands); (c) a real bash parser (none in stdlib). Choice: (a); a compound with a mover stays branchy as before, so nothing a loop repeats can move. Guards: the opener must be at command position (start, or an unescaped ; & | ( newline or '{ ' before it, through do/then/else/elif/time words), not after a redirect's & or |; the closer after an unescaped separator; no masking when quote masking failed closed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Adversarial table in test_guard, red
2. [x] Mask mover-free compounds in _top; table green
3. [x] Review, full test_guard
## Resume here
<!-- auto -->
- 2026-10-29T05:57:24Z step 3/3: Review, full test_guard
- git: foreman/build; 2 uncommitted: plugin/lib/fmguard.py, plugin/tests/test_guard.py
- touched since last checkpoint: plugin/lib/fmguard.py, plugin/tests/test_guard.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1920.txt
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_guard 2>&1 | grep -E "^(FAIL|ERROR)|arg=|Ran|OK|FAILED" | head -20` → ✗ exit 1 · Ran 294 tests in 10.6s (88 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 8s, Trust 7s) / FAILED (1 classes) [ran] [tree c5f117fc253b] (2026-10-29T05:53:54Z)
- (step 1) `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 294 tests in 7.9s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / FAILED (1 classes) [ran] [tree c5f117fc253b] (2026-10-29T05:54:05Z)
- (ac 1) `python3 plugin/tests/run.py test_guard 2>&1 | grep -E "^(FAIL|ERROR)|arg=|Ran|OK|FAILED|Error" | head -20` → ✗ exit 1 · Ran 294 tests in 10.9s (88 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 9s, Trust 7s) / FAILED (1 classes) [ran] [tree 8db359aca014] (2026-10-29T05:55:00Z)
- (step 2) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 294 tests in 10.5s (88 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 8s, Trust 7s) / OK [ran] [tree 25caf64d8c2b] (2026-10-29T05:56:02Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 294 tests in 8.7s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 25caf64d8c2b] (2026-10-29T05:56:19Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 294 tests in 8.0s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 25caf64d8c2b] (2026-10-29T05:56:19Z)
- (step 3) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 294 tests in 7.9s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree 2e5ae6862ba0] (2026-10-29T06:03:30Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 294 tests in 7.9s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree a1586d85545b] (2026-10-29T06:04:11Z)
- (audit intent) `one fm-reviewer adversary pass: 2 HIGH bypasses, a quoted cd hidden from the mover check and for-x read as an opener, plus 1 LOW duplicate _MOVERS; all confirmed red and fixed test-first` → the cherry-pick loop, if, while and brace group after cd scratch && now pass; anything that may move the shell still blocks [tree a1586d85545b] (2026-10-29T06:04:11Z)
- (audit adversary) `one fm-reviewer adversary pass: 2 HIGH bypasses, a quoted cd hidden from the mover check and for-x read as an opener, plus 1 LOW duplicate _MOVERS; all confirmed red and fixed test-first` → quoted or escaped cd, computed command word, a substitution naming cd, glued keywords, escaped separators, redirect separators, ANSI-C quoting, a cd in a loop body, a ; or || after the compound: all block, table rows [tree a1586d85545b] (2026-10-29T06:04:11Z)
- (audit edge) `one fm-reviewer adversary pass: 2 HIGH bypasses, a quoted cd hidden from the mover check and for-x read as an opener, plus 1 LOW duplicate _MOVERS; all confirmed red and fixed test-first` → nested compounds mask innermost first; a brace group or braced variable inside a compound keeps it branchy, conservative; a function body never masks [tree a1586d85545b] (2026-10-29T06:04:11Z)
## Log
- 2026-10-29T05:23:35Z created
- 2026-10-29T05:24:01Z lead: fmguard.py ~3238 — a for/if body's ';' and '||' read as a new mixed-list segment, so base (the cwd before 'cd X &&') rejoins cwds; the compound after && should inherit the chain's cwd. Repro: cd <scratch>/w && for s in a b; do git cherry-pick $s || break; done
- 2026-10-29T05:53:08Z set type=FIX, title=Guard reads a compound after 'cd <scratch> &&' as a tree write over Foreman
- 2026-10-29T05:53:13Z planned: it has criteria and steps
- 2026-10-29T05:53:14Z focused
- 2026-10-29T06:04:21Z done
- 2026-10-29T06:04:22Z committed 71996c22 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1891 [FIX S, done, 3 steps] Guard keeps a cd certain for && commands after it when the line has || — lesson: A cd's certainty depends on the operator before it, not on…
- T-1897 [FEATURE M, done, 3 steps] Guard hints for tree writes over Foreman and edits with no task; readable rule names — lesson: A hint that sends Claude to a second gua…
- playbook Ship a branch to main (fm playbooks show release/ship-to-main)
- decision 2026-10-28: T-1803 step 3: the next-step hint does not name the top routed book
- similar finished tasks took 3–3 steps
- start here (files T-1891 touched): plugin/tests/test_guard.py, CHANGELOG.md, plugin/lib/fmguard.py
## Why not caught
_top treated every compound keyword as a branch, a deliberate fail-closed shortcut; no test ran a compound behind a certain cd, so the false block on the guard's own suggested route went unseen until a push hit it
## Lessons
- When masking text for one check, keep it length-aligned with the original so a second check can read what the mask hid, quotes and substitutions, at the same offsets
## Plan gaps
- failed first: step 1 Adversarial table in test_guard, red
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
