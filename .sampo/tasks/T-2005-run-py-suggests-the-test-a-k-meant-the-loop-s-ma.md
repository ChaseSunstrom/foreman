---
id: T-2005
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_run.py, plugin/lib/fmloop.py, plugin/tests/test_loop.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-29T15:48:04Z
updated: 2026-10-29T15:56:06Z
batch: [T-2003, T-2004]
base: 0f5e8a5c25c5e2ce8008e9b56d73f311e34a8f1f
base_tree: 2e0e05de4e2ff32fd2d3568c672354e019920310
plan0_at: 2026-10-29T15:48:18Z
plan0_scope: [plugin/tests/run.py, plugin/tests/test_run.py, plugin/lib/fmloop.py, plugin/tests/test_loop.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# run.py suggests the test a -k meant, the loop's main-thread round sweeps every lens
## Raw request
> T-2003: FIX: run.py's "no test matches test_doctor with -k core_integrity" gives no way forward when the test is named CoreIntegrity; it now suggests up to three test ids that match once case and underscores are ignored ("did you mean -k CoreIntegrity?")
> @plugin/tests/run.py @plugin/tests/test_run.py
> DONE-WHEN: a -k differing only in case and underscores gets the real name suggested :: python3 plugin/tests/run.py test_run -k UnknownNames
> T-2004: FIX: the forever loop's main-thread round (optional work dropped) asks only to review what just shipped, so rounds shrink to 1-3 follow-ups and the user has to ask for breadth again; step 2 now names the lenses to sweep in the main thread (user value, unspoken needs, reliability, speed, simplicity, docs, UI and motion), at least one grounded idea each
## Interpretation
Do T-2003, T-2004 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-2005. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-2003: a -k differing only in case and underscores gets the real name suggested — verify with `python3 plugin/tests/run.py test_run -k UnknownNames`
- [x] T-2004: with optional work dropped, the round brief names the lenses to sweep in the main thread — verify with `python3 plugin/tests/run.py test_loop -k lenses`
## Non-goals
## Approach (options → choice → why)
run.py: on a miss, rediscover unfiltered and suggest up to three ids whose folded form (lowercase, no underscores) contains the folded -k (exact for the snake-vs-Camel slip; difflib is noisier; case-insensitive -k would diverge from unittest's -k that run_one passes on). Loop: step 2's main-thread branch names the lenses (one constant), at least one grounded idea per lens, so a round can't shrink to follow-ups of the last diff.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-2003: run.py's "no test matches test_doctor with -k core_integrity" gives no way forward when…
2. [x] T-2004: The forever loop's main-thread round (optional work dropped) asks only to review what…
## Resume here
<!-- auto -->
- 2026-10-29T15:54:34Z steps 2/2 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/fmloop.py, plugin/tests/run.py, plugin/tests/test_loop.py, plugin/tests/test_run.py
- touched since last checkpoint: plugin/tests/test_run.py, plugin/lib/fmloop.py, plugin/tests/run.py, CHANGELOG.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ideas_tsv.py
## Docs impact
- CHANGELOG.md: Unreleased entry for T-2003 and T-2004. MASTER.md unchanged (run.py and the loop brief's wording aren't mapped there).
## Verification evidence
- `python3 plugin/tests/run.py test_loop test_run -k names_the_lenses -k filters_out_names` → ✗ exit 1 · Ran 2 tests in 1.8s (2 classes, 16 at a time; slowest: UnknownNames 1s, Loop 0s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 15991c2b40d9] (2026-10-29T15:48:33Z)
- `python3 plugin/tests/run.py test_loop test_run -k names_the_lenses -k filters_out_names` → ✗ exit 1 · Ran 2 tests in 1.6s (2 classes, 16 at a time; slowest: UnknownNames 1s, Loop 0s) / FAILED (2 classes) [ran] [tree 15991c2b40d9] (2026-10-29T15:48:33Z)
- `python3 plugin/tests/run.py test_loop test_run -k names_the_lenses -k filters_out_names` → ✗ exit 1 · Ran 2 tests in 1.7s (2 classes, 16 at a time; slowest: UnknownNames 1s, Loop 0s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 3809327fbfaa] (2026-10-29T15:50:11Z)
- `python3 plugin/tests/run.py test_loop test_run -k names_the_lenses -k filters_out_names` → ✗ exit 1 · ^^^^ / AttributeError: 'TestSuite' object has no attribute 'id' [ran] [tree 3809327fbfaa] (2026-10-29T15:50:11Z)
- `python3 plugin/tests/run.py test_loop test_run -k names_the_lenses -k filters_out_names` → ✗ exit 1 · Ran 2 tests in 2.4s (2 classes, 16 at a time; slowest: UnknownNames 1s, Loop 0s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 3c91aac9b903] (2026-10-29T15:50:23Z)
- `python3 plugin/tests/run.py test_loop test_run -k names_the_lenses -k filters_out_names` → exit 0 · Ran 2 tests in 1.3s (2 classes, 16 at a time; slowest: UnknownNames 1s, Loop 0s) / OK [ran] [tree 3c91aac9b903] (2026-10-29T15:50:23Z)
- (step 1) `python3 plugin/tests/run.py test_run -k UnknownNames` → exit 0 · Ran 3 tests in 2.0s (1 classes, 16 at a time; slowest: UnknownNames 2s) / OK [ran] [tree 3c91aac9b903] (2026-10-29T15:50:29Z)
- (step 2) `python3 plugin/tests/run.py test_loop -k lenses` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Loop 0s) / OK [ran] [tree 3c91aac9b903] (2026-10-29T15:50:30Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.2    45.9     150  [0] / SessionEnd                  35.5    38.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/* [ran] [tree c7acb6b77214] (2026-10-29T15:55:05Z)
- (ac 1) `python3 plugin/tests/run.py test_run -k UnknownNames` → exit 0 · Ran 3 tests in 2.0s (1 classes, 16 at a time; slowest: UnknownNames 2s) / OK [ran] [tree c7acb6b77214] (2026-10-29T15:55:56Z)
- (ac 2) `python3 plugin/tests/run.py test_loop -k lenses` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Loop 0s) / OK [ran] [tree c7acb6b77214] (2026-10-29T15:55:56Z)
- (audit intent) `self-review: walk loop keeps the suite branch first (continue) so ids only gets test cases; near-name fold only runs on a miss; loop brief change is wording behind the existing pace branch; full gates green (4205 tests)` → a -k that differs only in case/underscores now names the -k it meant; the main-thread loop round names every lens to sweep [tree c7acb6b77214] (2026-10-29T15:55:56Z)
- (audit edge) `self-review: walk loop keeps the suite branch first (continue) so ids only gets test cases; near-name fold only runs on a miss; loop brief change is wording behind the existing pace branch; full gates green (4205 tests)` → a -k with no fold match prints no did-you-mean (tested); suggestions capped at three [tree c7acb6b77214] (2026-10-29T15:55:56Z)
- (audit self) `self-review: walk loop keeps the suite branch first (continue) so ids only gets test cases; near-name fold only runs on a miss; loop brief change is wording behind the existing pace branch; full gates green (4205 tests)` → no findings [tree c7acb6b77214] (2026-10-29T15:55:56Z)
## Log
- 2026-10-29T15:48:04Z created
- 2026-10-29T15:48:14Z set tier=S, scope=['plugin/tests/run.py', 'plugin/tests/test_run.py', 'plugin/lib/fmloop.py', 'plugin/tests/test_loop.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-29T15:48:17Z focused
- 2026-10-29T15:56:04Z done
- 2026-10-29T15:56:06Z committed 66d8eee8 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- research mission-20261029-104513: Request: keep super ultimate recursive brainstorming, and implementing all ideas, super ultimate improve foreman in all ways
- research mission-20261029-104513.pack: keep super ultimate recursive brainstorming, and implementing all ideas, super ultimate improve foreman in all ways
- decision 2026-10-16: Recommendation: build the 9 grounded items T-1180..T-1188 with builders; the worktree-fm re-exec idea is skipped (unreviewed lane code would write r…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_loop.py
## Why not caught
T-1999 named the filtering -k but nothing compared it to the ids it filtered; the loop brief had no test for its pace-branch wording
## Lessons
- A miss message that names the filter is half the fix; the other half is comparing the filter to what it filtered out.
## Files touched
- plugin/tests/test_loop.py
- plugin/tests/test_run.py
- plugin/tests/run.py
- plugin/lib/fmloop.py
- CHANGELOG.md
