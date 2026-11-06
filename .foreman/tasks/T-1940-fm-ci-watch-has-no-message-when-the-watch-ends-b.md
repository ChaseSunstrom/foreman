---
id: T-1940
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T08:41:58Z
updated: 2026-10-29T08:58:24Z
base: b0ee29231a16c7a301389ee047d5326a570c9159
base_tree: e42cfad1b4c5b2205da1a19b1318cf6096972c3b
plan0_at: 2026-10-29T08:53:35Z
plan0_scope: []
verified: strong
---
# Fm ci-watch has no message when the watch ends because polling saw no run at all. It could
## Raw request
> fm ci-watch has no message when the watch ends because polling saw no run at all. It could say whether gh or the API was used and the last error
> (noticed by an agent; research T-1939-review)
## Interpretation
When fm ci-watch gives up without seeing a finished run, say where it looked (gh or GitHub's public API), so a silent hour is explicable.
## Assumptions (confidence)
## Acceptance criteria
- [x] the gave-up message names the public API when it was used — verify with `python3 plugin/tests/run.py test_ci_watch`
## Non-goals
## Approach (options → choice → why)
watch already tracks via (T-1939): append ' (read through GitHub's public API)' to the gave-up message when via is set. Alternatives: keep the last HTTP error (rejected for now: _api's None hides it, more plumbing for a rare case); a --verbose flag (rejected: one fixed phrase is enough).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then one-line change in fmci.watch
## Resume here
## Docs impact
CHANGELOG (T-1939 entry)
## Verification evidence
- `python3 plugin/tests/run.py test_ci_watch` → ✗ exit 1 · Ran 5 tests in 2.4s (1 classes, 16 at a time; slowest: CiWatch 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 0f04bc9b0a59] (2026-10-29T08:53:55Z)
- `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 5 tests in 1.7s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree 0f04bc9b0a59] (2026-10-29T08:53:55Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 5 tests in 1.7s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree 0f04bc9b0a59] (2026-10-29T08:53:57Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 5 tests in 1.7s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree d4ca2908ddb1] (2026-10-29T08:58:20Z)
- (audit edge) `S: lenses only, the T-1939 reviewer raised it` → only when via is set; gh-only watches keep the old message (existing tests) [tree d4ca2908ddb1] (2026-10-29T08:58:20Z)
- (audit adversary) `S: lenses only, the T-1939 reviewer raised it` → fixed text, no untrusted input in the message [tree d4ca2908ddb1] (2026-10-29T08:58:20Z)
- (audit self) `S: lenses only, the T-1939 reviewer raised it` → no findings [tree d4ca2908ddb1] (2026-10-29T08:58:20Z)
## Log
- 2026-10-29T08:41:58Z created
- 2026-10-29T08:49:08Z set tier=S, type=FEATURE
- 2026-10-29T08:49:09Z planned: it has criteria and steps
- 2026-10-29T08:53:35Z focused
- 2026-10-29T08:58:22Z done
- 2026-10-29T08:58:24Z committed 53f6cfa5 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1939-review: Verdict: changes needed.** The fallback does what the acceptance criterion says, but it hides gh's error on a private repo or a rate-limited IP. …
- T-1939 [FEATURE M, done, 3 steps] fm ci-watch falls back to GitHub's public API when gh is missing or logged out — lesson: A fallback to an unauthenticated API must turn…
- playbook rust (fm playbooks show review/rust)
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Lessons
- none: a one-line follow-up to T-1939's lesson
## Files touched
- plugin/tests/test_ci_watch.py
- plugin/lib/fmci.py
- CHANGELOG.md
