---
id: T-0907
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T18:39:16Z
updated: 2026-10-15T18:42:06Z
base: 27b3d75c66e07d77ad70fb87547da846658bf236
base_tree: 6d71610aae159ee35197da84cdcb1f446a653dab
verified: strong
---
# Stop claims gate: doc edits after a green run, unlisted runners (mvn, gradle, dotnet, deno, node --test, bats, make -jN) and list-form notifications no longer misjudge 'tests pass'; fm checkpoint/toxic aren't test runs
## Raw request
> Stop claims gate: doc edits after a green run, unlisted runners (mvn, gradle, dotnet, deno, node --test, bats, make -jN) and list-form notifications no longer misjudge 'tests pass'; fm checkpoint/toxic aren't test runs
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the T-0886 test plus the reviewer's reproducers pass — verify with `python3 plugin/tests/run.py -k Stop`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing cases in test_hooks Stop, then fix _TEST_CMD, doc edits, notification text, redact
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k Stop` → ✗ exit 1 · Ran 40 tests in 27.1s (1 classes, 16 at a time; slowest: Stop 27s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 36d49183aa2b] (2026-10-15T18:41:35Z)
- `python3 plugin/tests/run.py -k Stop` → exit 0 · Ran 40 tests in 27.1s (1 classes, 16 at a time; slowest: Stop 27s) / OK [ran] [tree 36d49183aa2b] (2026-10-15T18:41:35Z)
- (ac 1) `python3 plugin/tests/run.py -k Stop` → exit 0 · Ran 40 tests in 27.1s (1 classes, 16 at a time; slowest: Stop 27s) / OK [ran] [tree 36d49183aa2b] (2026-10-15T18:42:05Z)
- (step 1) `python3 plugin/tests/run.py -k Tour` → exit 0 · Ran 4 tests in 1.9s (1 classes, 16 at a time; slowest: Tour 2s) / OK [ran] [tree 36d49183aa2b] (2026-10-15T18:42:05Z)
- (audit edge) `self: reviewer's reproducers as tests (mvn then README edit no longer held; fm checkpoint/toxic not runs; list-form notification keeps the turn); requirements.txt counts as prose for this gate, accepted (a missed hold, never a false one)` → make -j8 test, ./gradlew test, mvn -q test matched; fm check still matched [tree 36d49183aa2b] (2026-10-15T18:42:05Z)
- (audit self) `self: reviewer's reproducers as tests (mvn then README edit no longer held; fm checkpoint/toxic not runs; list-form notification keeps the turn); requirements.txt counts as prose for this gate, accepted (a missed hold, never a false one)` → no findings [tree 36d49183aa2b] (2026-10-15T18:42:05Z)
## Log
- 2026-10-15T18:39:16Z created
- 2026-10-15T18:39:16Z focused
- 2026-10-15T18:41:36Z scope: fmcore.DOC is fmmap's doc pattern moved so the Stop hook can share it without importing fmmap
- 2026-10-15T18:42:05Z done
- 2026-10-15T18:42:06Z committed d289d77 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0886 [FEATURE M, done, 2 steps] The Stop hook checks the final message's specific claims (tests pass, fixed, verified) aga — lesson: Judge a run by its verdict, not by…
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- T-0820 [FIX M, done, 4 steps] Round-1 review fixes (medium): auto-evidence honours failure summaries, bench replays aren't one-off, record_pid survives overlap and stops…
- decision 2026-09-26: T-0018 plan self-approved under full autonomy after self-critique: umbrella with rounds (one core ask), per-round reviewer audits, green gates each …
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmcore.py
- plugin/lib/fmmap.py
- plugin/lib/fmhooks.py
