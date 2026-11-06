---
id: T-0719
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:56:36Z
updated: 2026-10-09T16:59:07Z
base: e157abfe0734bb6abc176efeedcd88c85c17c49d
base_tree: 71a544ca0fde57259b04f9037b8ddb81ffee099b
verified: strong
---
# Commit T-0671's review fixes: mark the .env test fixture as an allowlisted secret
## Raw request
> Commit T-0671's review fixes: mark the .env test fixture as an allowlisted secret
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] committed with the secrets gate passing — verify with `git log -1 --format=%s`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] pragma on the fixture line, commit T-0671's files
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_autonomy_user.py` → exit 0 · Ran 15 tests in 3.5s (3 classes, 16 at a time; slowest: TasteVetoes 4s, AskDigest 2s, CaptureFromFile 1s) / OK [ran] [tree ffa84e5f0885] (2026-10-09T16:56:46Z)
- (ac 1) `git log -1 --format=%s` → exit 0 · Guard: pipe-into-shell closes its review's gaps: option values, -s, groups, computed names, inline code that runs stdin (T-0716) [ran] [tree ffa84e5f0885] (2026-10-09T16:59:06Z)
- (audit edge) `self: one pragma comment on a test fixture; full fm check passed on this tree` → the secrets gate still flags real credentials; only the line marked as a fixture passes [tree ffa84e5f0885] (2026-10-09T16:59:06Z)
- (audit self) `self: one pragma comment on a test fixture; full fm check passed on this tree` → no findings [tree ffa84e5f0885] (2026-10-09T16:59:06Z)
## Log
- 2026-10-09T16:56:36Z created
- 2026-10-09T16:56:36Z focused
- 2026-10-09T16:59:06Z done
- 2026-10-09T16:59:07Z committed 399fd65 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0392 [FIX S, done, 1 steps] Allowlist the T-0390 test fixture's placeholder secret line (committed in 5912e40 without the marker) — lesson: Never run a commit in paral…
- T-0669 [SECURITY L, done, 8 steps] Guard hardening: fuzzer escape classes 2-5 and 7-9, one close-out run — lesson: batch close-out works: one red run for all rows, fixtu…
- playbook Security Reviewer (skills/playbooks/references/review/security.md)
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar finished tasks took 1–8 steps
- start here (files T-0392 touched): plugin/tests/test_hooks.py
## Regression test
none: a commit-hygiene fix (a fixture comment), the T-0671 suite is its check
## Files touched
- plugin/tests/test_autonomy_user.py
