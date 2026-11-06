---
id: T-2304
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T09:33:13Z
updated: 2026-10-31T09:44:48Z
base: af2cb346f66ad2d263cd00e7b0b2bf48fab04b34
base_tree: 5c4d78add54351c124c02d91e28ed9baf93d4224
plan0_at: 2026-10-31T09:33:14Z
plan0_scope: []
verified: strong
---
# Long-tier goals are passable from their text: checks only from the task's own commits, the goal names the new names and flags the checks reach, and lists the checks as done-when
## Raw request
> Long-tier goals are passable from their text: checks only from the task's own commits, the goal names the new names and flags the checks reach, and lists the checks as done-when
## Interpretation
l001 graded the foreman arm 0/6, but the defect was the exam's: T-1674's check calls fmwatch._shown and T-2262's reads fmlong.KILL_T, names the goal never states, so a correct implementation under another name fails; and T-2225's checks include T-2181's read-check tests, added by another task interleaved in the window. Make each goal passable from its text alone without handing over the tests.
## Assumptions (confidence)
## Acceptance criteria
- [x] A window's checks are only the test ids its own task's commits added (each commit's ids minus its parent's), so a test added by an interleaved task's commit is never a check — verify with `python3 plugin/tests/run.py test_long`
- [x] The goal text names each module attribute the checks reach that the base lacks and the target defines (e.g. fmwatch._shown) and each new --flag the checks pass that the base's code never mentions, under 'The checks use these new names:' — verify with `python3 plugin/tests/run.py test_long`
- [x] The goal text lists each check's test name, humanized, under 'Done when:', and no test body or assertion text — verify with `python3 plugin/tests/run.py test_long`
## Non-goals
## Approach (options → choice → why)
Options: 1) state the interface the checks touch (new module attributes, new CLI flags) and the checks' names in the goal, and take checks only from the task's own commits; 2) keep only windows whose checks touch no new private names (filter the pool, goal unchanged); 3) give the hidden tests to the agent (a test-passing task, no longer a goal). Choice 1: keeps every window, reads like a well-written ticket (names and done-when), never shows assertions; 2 shrinks the pool to the easy windows; 3 measures nothing about finishing a goal.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests on a small git repo: an interleaved task's test is no check; a check calling mod.new_name puts mod.new_name in the goal; a check passing --new-flag puts it in the goal; the goal lists the checks' names and no assertion text
2. [x] fmlong._windows keeps each commit; _scenario takes new ids per own commit; a _interface helper (ast over the check functions, base vs target module names, --flags absent from the base's code) builds the goal's extra lines
## Resume here
<!-- auto -->
- 2026-10-31T09:36:40Z step 1/2: Red tests on a small git repo: an interleaved task's test is no check; a check calling mod.new_name puts mod.new_name in the goal; a check passing --new-flag puts it in the goal; the goal lists the checks' names and no assertion text
- git: foreman/build; 2 uncommitted: plugin/lib/fmlong.py, plugin/tests/test_long.py
- touched since last checkpoint: plugin/tests/test_long.py, plugin/lib/fmlong.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_long -k names_what_its_checks_reach` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Long 1s) / FAILED (1 classes) [ran] [tree f523064354bc] (2026-10-31T09:33:56Z)
- `python3 plugin/tests/run.py test_long -k names_what_its_checks_reach` → ✗ exit 1 · Ran 1 tests in 2.4s (1 classes, 16 at a time; slowest: Long 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 04964f728529] (2026-10-31T09:34:53Z)
- `python3 plugin/tests/run.py test_long -k names_what_its_checks_reach` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Long 1s) / OK [ran] [tree 04964f728529] (2026-10-31T09:34:53Z)
- (step 2) `python3 plugin/tests/run.py test_long test_exam` → exit 0 · Ran 77 tests in 80.2s (18 classes, 16 at a time; slowest: ExamAuthors 80s, ExamGen 65s, Long 55s) / OK [ran] [tree 04964f728529] (2026-10-31T09:36:17Z)
- (step 2) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 35 tests in 25.2s (7 classes, 16 at a time; slowest: Long 25s, Approvals 1s, Stop 1s) / OK [ran] [tree aa5c9c730cfb] (2026-10-31T09:43:21Z)
- (ac 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 35 tests in 25.0s (7 classes, 16 at a time; slowest: Long 25s, Approvals 1s, Stop 1s) / OK [ran] [tree aa5c9c730cfb] (2026-10-31T09:44:03Z)
- (ac 2) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 35 tests in 25.0s (7 classes, 16 at a time; slowest: Long 25s, Approvals 1s, Stop 1s) / OK [ran] [tree aa5c9c730cfb] (2026-10-31T09:44:03Z)
- (ac 3) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 35 tests in 25.0s (7 classes, 16 at a time; slowest: Long 25s, Approvals 1s, Stop 1s) / OK [ran] [tree aa5c9c730cfb] (2026-10-31T09:44:03Z)
- (audit intent) `one fm-reviewer pass (adversary, edge, operator, maintainer): MEDIUM module resolution (first match, stdlib names), MEDIUM no cache per module file, LOWs (from-imports and dotted imports missed, git grep timeout, parse RecursionError, unbounded done lines, thin test); fixed: exact path first then every suffix candidate, stdlib names skipped, from m import n handled, top names cached per (rev, file), timeouts and parse errors caught, done lines fitted to 80 and deduped, test extended with base-known names and flag staying out and a from-import name coming in; l002 regenerated from Foreman's repo: goals name fmcore.lazy, fmfind._ts_rules, fmdoctor.slowest; oracle 6/6, empty 0/6` → a long goal is passable from its text: the new names and flags its checks need and what done means, never the tests [tree aa5c9c730cfb] (2026-10-31T09:44:03Z)
- (audit adversary) `one fm-reviewer pass (adversary, edge, operator, maintainer): MEDIUM module resolution (first match, stdlib names), MEDIUM no cache per module file, LOWs (from-imports and dotted imports missed, git grep timeout, parse RecursionError, unbounded done lines, thin test); fixed: exact path first then every suffix candidate, stdlib names skipped, from m import n handled, top names cached per (rev, file), timeouts and parse errors caught, done lines fitted to 80 and deduped, test extended with base-known names and flag staying out and a from-import name coming in; l002 regenerated from Foreman's repo: goals name fmcore.lazy, fmfind._ts_rules, fmdoctor.slowest; oracle 6/6, empty 0/6` → parse-only ast over trust-gated repo text, nothing executes; flags regex-bounded and passed after -e with -F; goal lines c.plain'd and fitted [tree aa5c9c730cfb] (2026-10-31T09:44:03Z)
- (audit edge) `one fm-reviewer pass (adversary, edge, operator, maintainer): MEDIUM module resolution (first match, stdlib names), MEDIUM no cache per module file, LOWs (from-imports and dotted imports missed, git grep timeout, parse RecursionError, unbounded done lines, thin test); fixed: exact path first then every suffix candidate, stdlib names skipped, from m import n handled, top names cached per (rev, file), timeouts and parse errors caught, done lines fitted to 80 and deduped, test extended with base-known names and flag staying out and a from-import name coming in; l002 regenerated from Foreman's repo: goals name fmcore.lazy, fmfind._ts_rules, fmdoctor.slowest; oracle 6/6, empty 0/6` → an interleaved task's test is no check; a check renamed later drops out (own ids intersected with the target's); stdlib-named repo files ignored; dotted imports without an alias aren't followed (rare) [tree aa5c9c730cfb] (2026-10-31T09:44:03Z)
- (audit operator) `one fm-reviewer pass (adversary, edge, operator, maintainer): MEDIUM module resolution (first match, stdlib names), MEDIUM no cache per module file, LOWs (from-imports and dotted imports missed, git grep timeout, parse RecursionError, unbounded done lines, thin test); fixed: exact path first then every suffix candidate, stdlib names skipped, from m import n handled, top names cached per (rev, file), timeouts and parse errors caught, done lines fitted to 80 and deduped, test extended with base-known names and flag staying out and a from-import name coming in; l002 regenerated from Foreman's repo: goals name fmcore.lazy, fmfind._ts_rules, fmdoctor.slowest; oracle 6/6, empty 0/6` → one ls-tree per window and one parse per (rev, file); a slow git probe drops that probe, not the gen [tree aa5c9c730cfb] (2026-10-31T09:44:03Z)
- (audit maintainer) `one fm-reviewer pass (adversary, edge, operator, maintainer): MEDIUM module resolution (first match, stdlib names), MEDIUM no cache per module file, LOWs (from-imports and dotted imports missed, git grep timeout, parse RecursionError, unbounded done lines, thin test); fixed: exact path first then every suffix candidate, stdlib names skipped, from m import n handled, top names cached per (rev, file), timeouts and parse errors caught, done lines fitted to 80 and deduped, test extended with base-known names and flag staying out and a from-import name coming in; l002 regenerated from Foreman's repo: goals name fmcore.lazy, fmfind._ts_rules, fmdoctor.slowest; oracle 6/6, empty 0/6` → _parse shared; the goal is built in _scenario so key.json and run.json hold the same text [tree aa5c9c730cfb] (2026-10-31T09:44:03Z)
## Log
- 2026-10-31T09:33:13Z created
- 2026-10-31T09:33:13Z focused
- 2026-10-31T09:36:46Z paused: focus moved to T-2305
- 2026-10-31T09:39:24Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T09:39:24Z focused
- 2026-10-31T09:43:37Z scope: plugin/lib/fmlong.py (_windows commits, _parse, _top_names, _interface, _scenario, gen), plugin/tests/test_long.py, MASTER.md, CHANGELOG.md (also carries T-2305's changelog line)
- 2026-10-31T09:44:46Z done
- 2026-10-31T09:44:48Z committed 322b5ec9 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-31: Long tier l001's foreman 0/6 is an exam defect, not a score: hidden checks need private names the goal never states (fmwatch._shown, fmlong.KILL_T) …
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
## Why not caught
the long tier's exam of the exam was oracle 6/6 and empty 0/6, which a goal no honest answer can pass still meets: nothing checked that a goal's text states what its checks need
## Lessons
- An exam-of-the-exam needs a middle arm: oracle and empty bound the grader, but only an independent implementation from the goal text shows a goal is passable; private names and interleaved tests hide between the two ends
## Plan gaps
- failed first: step 1 Red tests on a small git repo: an interleaved task's test is no check; a check calling mod.new_name…
## Files touched
- plugin/tests/test_long.py
- plugin/lib/fmlong.py
- MASTER.md
- CHANGELOG.md
