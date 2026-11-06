---
id: T-0259
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-04T05:37:55Z
updated: 2026-10-04T05:40:39Z
base: 7b6c604dacc115136abbeb581aa26702ac1eec98
base_tree: 104187a59410ea18705dfc29a3c0359f69b535ef
verified: strong
---
# fm intake: CONTEXT/DONE-WHEN lines between items belong to the item above; trailing ones still apply to all
## Raw request
> FIX!: fm intake gives every item of a multi-item block all the block's CONTEXT/DONE-WHEN/MUST lines — a line after a tagged item should belong to that item (block-level lines only before the first tag)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an interleaved multi-item block gives each item only its own CONTEXT/DONE-WHEN lines; a block whose lines all trail the items (the README form) still applies them to every item — verify with `python3 plugin/tests/run.py -k test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then per-item block lines in parse_intake and _raw_with_block
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_cli` → exit 0 · Ran 71 tests in 14.6s (16 classes, 16 at a time; slowest: TaskLifecycle 15s, StateViews 5s, Checks 4s) / OK [ran] [tree 1d22f1cfbe59] (2026-10-04T05:39:14Z)
- `python3 plugin/tests/run.py -k CaptureAndIntake` → ✗ exit 1 · Ran 6 tests in 1.0s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1d22f1cfbe59] (2026-10-04T05:39:17Z)
- `python3 plugin/tests/run.py -k CaptureAndIntake` → exit 0 · Ran 6 tests in 0.9s (1 classes, 16 at a time; slowest: CaptureAndIntake 1s) / OK [ran] [tree 1d22f1cfbe59] (2026-10-04T05:39:17Z)
- (ac 1) `python3 plugin/tests/run.py -k test_cli` → exit 0 · Ran 71 tests in 13.2s (16 classes, 16 at a time; slowest: TaskLifecycle 13s, StateViews 4s, Checks 3s) / OK [ran] [tree d37350deff40] (2026-10-04T05:40:38Z)
- (audit self) `self checklist: README form (trailing lines) unchanged — the existing canonical-order test still passes; interleaved lines go to the item above; continuation lines extend the right line; the hook's 'plus block lines' note counts per-item lines` → pass [tree d37350deff40] (2026-10-04T05:40:38Z)
## Log
- 2026-10-04T05:37:55Z created
- 2026-10-04T05:38:18Z planned from capture
- 2026-10-04T05:38:18Z focused
- 2026-10-04T05:40:25Z gate: full suite fails only on test_batch.py, the paused T-0257's red tests (not built yet); this task's own classes pass
- 2026-10-04T05:40:39Z done
- 2026-10-04T05:40:39Z committed 16e8e8a (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Release and changelog (skills/playbooks/references/release/release-and-changelog.md)
- T-0167 [FEATURE L, done, 5 steps] fm run --parallel N: independent queued tasks at once, each in its own lane, merged back only when gated and clean — lesson: A loop tha…
- research t0018-final-operator: Not directly related. I have sufficient evidence now. Let me finalize. [stale: plugin/uninstall.sh changed since it was written]
- T-0206 [FEATURE M, done, 3 steps] fm research ask: recall first, parallel web researchers per sub-question, every quoted claim re-fetched and checked, one note recorded …
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–5 steps
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
