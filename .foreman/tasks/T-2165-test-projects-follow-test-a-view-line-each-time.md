---
id: T-2165
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_projects.py]
depends_on: []
source: discovered
created: 2026-10-30T14:14:08Z
updated: 2026-10-30T14:20:23Z
base: 93cf6b98ca3e041163ae36c47d9d4c54e156b922
base_tree: de28690094e607e9a28f79eb579e8b51049e7ef9
plan0_at: 2026-10-30T14:14:19Z
plan0_scope: [plugin/tests/test_projects.py]
verified: strong
---
# test_projects Follow.test_a_view_line_each_time_the_project_changes is flaky: fm capture…
## Raw request
> test_projects Follow.test_a_view_line_each_time_the_project_changes is flaky: fm capture makes more than one state change, so the follower can print an intermediate line still at inbox_total 0; read lines until inbox_total is 1 within the timeout (failed fm ship of 93cf6b98 in the scratch tree)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the follow test waits for the line with inbox_total 1 instead of taking the next line, and passes 20 runs in a row — verify with `for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do python3 plugin/tests/run.py test_projects >/dev/null 2>&1 || exit 1; done`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] read lines until inbox_total is 1 (bounded by the read timeout)
## Resume here
<!-- auto -->
- 2026-10-30T14:14:39Z step 1/1: read lines until inbox_total is 1 (bounded by the read timeout)
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_projects` → exit 0 · Ran 7 tests in 0.9s (5 classes, 16 at a time; slowest: Projects 1s, Follow 1s, VersionSkew 0s) / OK [ran] [tree a297675d052e] (2026-10-30T14:16:40Z)
- (ac 1) `for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do python3 plugin/tests/run.py test_projects >/dev/null 2>&1 || exit 1; done` → exit 0 · (no output) [ran] [tree a297675d052e] (2026-10-30T14:16:59Z)
- (ac 1) `for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do python3 plugin/tests/run.py test_projects >/dev/null 2>&1 || exit 1; done` → exit 0 · (no output) [ran] [tree a297675d052e] (2026-10-30T14:17:25Z)
- (audit edge) `self: reread the loop: it reads lines until inbox_total is 1, each read bounded by the time left before a 10 s deadline (at least 0.1 s), so a stuck view still fails via read_line's no-line assertion; no other test in the file takes the next line after a multi-write command` → an intermediate line at 0 is skipped; a view that never reaches 1 fails at the deadline [tree a297675d052e] (2026-10-30T14:17:25Z)
- (audit self) `self: reread the loop: it reads lines until inbox_total is 1, each read bounded by the time left before a 10 s deadline (at least 0.1 s), so a stuck view still fails via read_line's no-line assertion; no other test in the file takes the next line after a multi-write command` → no findings [tree a297675d052e] (2026-10-30T14:17:25Z)
## Log
- 2026-10-30T14:14:08Z created
- 2026-10-30T14:14:13Z set scope=['plugin/tests/test_projects.py']
- 2026-10-30T14:14:13Z planned: it has criteria and steps
- 2026-10-30T14:14:18Z focused
- 2026-10-30T14:17:40Z done
- 2026-10-30T14:17:41Z committed fe25294c (1 file)
- 2026-10-30T14:17:53Z guard authorization added: publish
- 2026-10-30T14:20:23Z publish grant used by fm ship
## Follow-ups captured
## Behaviour lock
none: a test-only fix; the follower's one-line-per-change behaviour is what the test should allow
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- T-1923 [SECURITY M, done, 1 steps] Guard judges tree writes after a cd to a folder it can't name — lesson: bare is None whenever a command word is computed: branches gat…
- decision 2026-10-23: T-1259: build the compaction storm and the window sweep, tested with the bench's fakes; the measured sweep (real Haiku sessions) waits until weekly …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Regression test
none: a timing flake (a follow line landing between fm capture's writes) can't be made red on demand; the 20-run loop (AC 1) and the scratch-tree suite in fm ship are the checks
## Files touched
- plugin/tests/test_projects.py
