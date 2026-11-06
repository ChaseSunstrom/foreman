---
id: T-2064
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T23:48:10Z
updated: 2026-10-30T00:09:59Z
base: 03b7feea5759378b99eed42c845a93e36c8a944c
base_tree: d30a7ecfe748e11c741d920ae5be20b1dd194d38
plan0_at: 2026-10-29T23:48:10Z
plan0_scope: []
verified: strong
---
# test_ship's --check test fails when a commit hash ends in 'add' (substring match on 'add a')
## Raw request
> test_ship's --check test fails when a commit hash ends in 'add' (substring match on 'add a')
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the check test matches the subject as a word, so a hash ending in 'add' can't satisfy 'add a' — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] match subjects as words in test_check_says_whether_main_has_the_commits_without_the_grant
## Resume here
<!-- auto -->
- 2026-10-30T00:09:00Z step 1/1: match subjects as words in test_check_says_whether_main_has_the_commits_without_the_grant
- git: foreman/build; 6 uncommitted: CHANGELOG.md, plugin/tests/test_ship.py, plugin/tests/test_site_build.py, site/build.py, site/index.html, site/pages.py
- failures met: assertionerror: 'lost the proof mark' not found in 'pages.py:0: syntaxwarning: "\\`" is a…; style.css
## Docs impact
plugin/tests/test_ship.py
## Verification evidence
- (step 1) `python3 -c "assert 'add a' not in 'origin main lacks 8f54fadd add b'"` → red as expected (exit 1) · ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ / AssertionError [ran] [tree f051472970a2] (2026-10-29T23:48:21Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ship` → exit 0 · Ran 17 tests in 10.5s (1 classes, 16 at a time; slowest: Ship 10s) / OK [ran] [tree ce28bb8f06e2] (2026-10-29T23:48:56Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 4275 tests in 335.2s (1004 classes, 16 at a time; slowest: Worker 182s, Stop 111s, Bench 96s) / FAILED (1 classes) [ran] [tree ce28bb8f06e2] (2026-10-29T23:55:09Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ship` → exit 0 · Ran 17 tests in 14.2s (1 classes, 16 at a time; slowest: Ship 14s) / OK [ran] [tree 7ecc8dbd636e] (2026-10-30T00:09:36Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 4997 new to the corpus / guard cases: 124 labelled, 0 drifted [ran] [tree 7ecc8dbd636e] (2026-10-30T00:09:36Z)
- (audit intent) `self-review of the one-line diff: the --check test's stdout assertion now matches 'add a' as words, the main_log() membership checks stay exact` → the flaky assertion is the only change; the test still fails if --check lists commit a [tree 7ecc8dbd636e] (2026-10-30T00:09:36Z)
- (audit edge) `self-review of the one-line diff: the --check test's stdout assertion now matches 'add a' as words, the main_log() membership checks stay exact` → a hash ending in 'add' ('8f54fadd add b') no longer matches; \badd a\b still matches 'lacks 1234 add a' [tree 7ecc8dbd636e] (2026-10-30T00:09:36Z)
- (audit adversary) `self-review of the one-line diff: the --check test's stdout assertion now matches 'add a' as words, the main_log() membership checks stay exact` → test-only change, no runtime path [tree 7ecc8dbd636e] (2026-10-30T00:09:36Z)
- (audit operator) `self-review of the one-line diff: the --check test's stdout assertion now matches 'add a' as words, the main_log() membership checks stay exact` → fm ship no longer fails a good push about one run in 16^3 on this test [tree 7ecc8dbd636e] (2026-10-30T00:09:36Z)
- (audit maintainer) `self-review of the one-line diff: the --check test's stdout assertion now matches 'add a' as words, the main_log() membership checks stay exact` → the message on the assertion says why it's a word match [tree 7ecc8dbd636e] (2026-10-30T00:09:36Z)
- (audit self) `self-review of the one-line diff: the --check test's stdout assertion now matches 'add a' as words, the main_log() membership checks stay exact` → no findings [tree 7ecc8dbd636e] (2026-10-30T00:09:36Z)
## Log
- 2026-10-29T23:48:10Z created
- 2026-10-29T23:48:10Z focused
- 2026-10-29T23:56:13Z paused: focus moved to T-2062
- 2026-10-30T00:02:51Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-30T00:02:51Z focused
- 2026-10-30T00:09:56Z done
- 2026-10-30T00:09:59Z committed 7e4fccfa (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1825 [FEATURE M, done, 3 steps] FEATURE: fm run (headless) skips a model call when the tree and the failing check's output — lesson: count list items by line start, no…
- research T-1929-review: Changes needed. The three caps are now unliftable and `check()` ordering is sound. One refusal in the same class is still liftable, and the `unan…
- T-1921 [FIX M, done, 3 steps] Guard reads a substitution behind 'cd /abs &&' from the starting folder too — lesson: When the guard trusts a cd folder, check the parsed a…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–3 steps
## Why not caught
the assertion matched 'add a' as a substring; a random hash ending in 'add' before ' add b' satisfies it, about once in 4,096 runs
## Lessons
- Asserting a short phrase is absent from output that holds random hex is flaky: match words, or compare parsed fields
## Files touched
- plugin/tests/test_ship.py
- site/build.py
- site/pages.py
