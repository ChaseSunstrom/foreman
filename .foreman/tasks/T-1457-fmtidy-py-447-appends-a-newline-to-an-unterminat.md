---
id: T-1457
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/tests/test_tidy.py]
depends_on: []
source: discovered
created: 2026-10-22T13:52:44Z
updated: 2026-10-23T08:12:45Z
base: bf09dd103b3f2bc327297c25f2d2b81a4a9d21cd
base_tree: 78cb6e73fb8f15bd0d2df11a7c27c5feddca4040
plan0_at: 2026-10-23T08:12:15Z
plan0_scope: [plugin/tests/test_tidy.py]
verified: strong
---
# fm tidy's ledger roll keeps a crash-damaged (NUL) line in the rolled prefix byte for byte, and ends an unterminated last line with a newline in the archive; tested
## Raw request
> fmtidy.py:447` appends a newline to an unterminated last line when archiving. Harmless to the hash, but worth a test with a NUL line in the rolled prefix
> (noticed by an agent; research T-1456-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a roll whose old months hold a NUL line archives it byte for byte, a last line with no newline is archived newline-terminated, and fm verify-ledger still passes — verify with `python3 plugin/tests/run.py test_tidy`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the test (behaviour as built)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 35 tests in 4.2s (13 classes, 16 at a time; slowest: Apply 4s, StalePlans 4s, Rollback 3s) / OK [ran] [tree fecc42095f90] (2026-10-23T08:12:37Z)
- (audit intent) `self` → pass: the reviewer's case (a NUL line in the rolled prefix, an unterminated last line) is tested; fm verify-ledger still passes after the roll [tree fecc42095f90] (2026-10-23T08:12:37Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 35 tests in 4.0s (13 classes, 16 at a time; slowest: Apply 4s, StalePlans 3s, Rollback 3s) / OK [ran] [tree fecc42095f90] (2026-10-23T08:12:42Z)
- (audit intent) `self: intent` → behaviour as built is now pinned by a test, NUL bytes and the added newline both [tree fecc42095f90] (2026-10-23T08:12:42Z)
- (audit self) `self: intent` → no findings [tree fecc42095f90] (2026-10-23T08:12:42Z)
## Log
- 2026-10-22T13:52:44Z created
- 2026-10-23T08:12:13Z planned from capture
- 2026-10-23T08:12:14Z set scope=['plugin/tests/test_tidy.py']
- 2026-10-23T08:12:15Z focused
- 2026-10-23T08:12:44Z done
- 2026-10-23T08:12:45Z committed 444a6cb1 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1456-review: Verdict: changes needed.** One HIGH adversary finding. I could not run code (read-only, no shell), so each finding is proved by tracing `fmledger…
- T-1456 [SECURITY M, done, 3 steps] Ledger names crash damage and accepts it once — lesson: A tamper-evident chain needs a defined, explicit path through accidental damag…
- research T-1065-review: Verdict: changes needed.** Two MEDIUM findings, both about failures breaking normal use. I only read the code. This session had no shell, so I ra…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Preflight
Changed in scope since this was planned (2026-10-22): plugin/tests/test_tidy.py; re-ground the plan against them before editing
## Lessons
- A review note that says harmless still earns a test that shows it
## Files touched
- plugin/tests/test_tidy.py
