---
id: T-0892
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T16:40:34Z
updated: 2026-10-15T16:44:39Z
base: b2cbed87b8d07d70003f85d67d3bfc1bb4210609
base_tree: 5a1b0d953946b41bf913eae8be883ba59cd9c61c
verified: strong
---
# Guard: T=$(mktemp -d) resolves to a scratch folder, so a later rm -r $T isn't an unresolvable target
## Raw request
> Guard: T=$(mktemp -d) leaves T unknown, so a later rm -r $T is refused as an unresolvable target; resolve a bare $(mktemp -d) assignment to a scratch path (keep X=$(mktemp -d); rm -rf $X/../.. blocked, test_guard.py:184)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a mktemp -d variable can be removed; $X/../.. still blocks — verify with `python3 plugin/tests/run.py test_guard test_guard_diff`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red rows in test_guard, then _track_vars resolves a bare $(mktemp -d)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_git` → exit 0 · Ran 101 tests in 4.4s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree 90022784c382] (2026-10-15T16:42:29Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 101 tests in 4.7s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 90022784c382] (2026-10-15T16:42:39Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 101 tests in 4.4s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree 90022784c382] (2026-10-15T16:42:39Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_diff` → exit 0 · Ran 101 tests in 4.4s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree 90022784c382] (2026-10-15T16:44:38Z)
- (audit adversary) `self review: a bare NAME=$(mktemp -d) (or backticks, optionally quoted) is read as TMPDIR-or-/tmp/tmp.mktemp before analysis, the same as writing that literal; -p/--tmpdir/templates and other substitutions stay unknown` → the rewrite only ever names a folder under the temp dir, so it can't widen what a write or delete reaches beyond a literal /tmp path the guard already judges; $X/../.. still resolves to / and blocks (test row kept), -p {fhome} still blocks; fm replay over 3300 real commands: 0 newly allowed [tree 90022784c382] (2026-10-15T16:44:38Z)
- (audit self) `self review: a bare NAME=$(mktemp -d) (or backticks, optionally quoted) is read as TMPDIR-or-/tmp/tmp.mktemp before analysis, the same as writing that literal; -p/--tmpdir/templates and other substitutions stay unknown` → no findings [tree 90022784c382] (2026-10-15T16:44:38Z)
## Log
- 2026-10-15T16:40:34Z created
- 2026-10-15T16:41:28Z planned from capture
- 2026-10-15T16:41:28Z focused
- 2026-10-15T16:44:39Z done
- 2026-10-15T16:44:39Z committed 92ce4ac (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0370 [FIX M, done, 2 steps] Guard: a $(…) substitution no longer turns off variable tracking, so a literal S=/tmp/… stays known — lesson: Before widening what the guar…
- T-0151 [FEATURE M, done, 1 steps] Guard: rm resolves $VAR set to a literal earlier in a straight-line command — lesson: Resolve state only where the shell's own control …
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- similar finished tasks took 1–2 steps
## Why not caught
none: a known gap (unknown after any substitution); surfaced by the self-improvement pass from a real block
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
