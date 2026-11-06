---
id: T-0394
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-09T02:35:12Z
updated: 2026-10-09T02:37:12Z
base: cc66d4a8969b54f36362efed2cc5d54b4c5d39a3
base_tree: cc48f829173f713870e4ff37c0a290d34d537c4a
verified: strong
---
# CLEAN: the guard's refusal of a plain git merge on Foreman's own repo should name fm lane
## Raw request
> CLEAN: the guard's refusal of a plain git merge on Foreman's own repo should name fm lane merge ID (builders and the main thread typed git merge --no-ff by hand)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the refusal of git merge on Foreman's tree names fm lane merge — verify with `python3 plugin/tests/run.py -k test_git_merge_refusal_names_lane_merge`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then tag the finding and add the hint
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_git_merge_refusal_names_lane_merge` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: MergeHint 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2aeb41ea935a] (2026-10-09T02:35:50Z)
- `python3 plugin/tests/run.py -k test_git_merge_refusal_names_lane_merge` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: MergeHint 0s) / OK [ran] [tree 2aeb41ea935a] (2026-10-09T02:35:50Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.0    34.7     150  [0] / SessionEnd                  29.9    31.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 933 tests in [ran] [tree ee4467522d45] (2026-10-09T02:37:07Z)
- (ac 1) `python3 plugin/tests/run.py -k test_git_merge_refusal_names_lane_merge` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: MergeHint 0s) / OK [ran] [tree ee4467522d45] (2026-10-09T02:37:07Z)
- (audit intent) `self: only the refusal text changes; the replay corpus shows no verdict change` → a git merge refused on Foreman's tree names fm lane merge (test); other core refusals don't (test) [tree ee4467522d45] (2026-10-09T02:37:07Z)
- (audit edge) `self: only the refusal text changes; the replay corpus shows no verdict change` → 'merge' as any git argument adds the hint, message text only, never the decision [tree ee4467522d45] (2026-10-09T02:37:07Z)
- (audit self) `self: only the refusal text changes; the replay corpus shows no verdict change` → no findings [tree ee4467522d45] (2026-10-09T02:37:07Z)
- (audit intent) `self: only the refusal text changes; the replay corpus shows no verdict change` → a git merge refused on Foreman's tree names fm lane merge (test); other core refusals don't (test) [tree ee4467522d45] (2026-10-09T02:37:12Z)
- (audit edge) `self: only the refusal text changes; the replay corpus shows no verdict change` → 'merge' as any git argument adds the hint, message text only, never the decision [tree ee4467522d45] (2026-10-09T02:37:12Z)
- (audit adversary) `self: only the refusal text changes; the replay corpus shows no verdict change` → the note is appended to a block's detail after classification; nothing reads it to decide, so it can't turn a refusal into a pass (replay: 0 newly allowed) [tree ee4467522d45] (2026-10-09T02:37:12Z)
- (audit self) `self: only the refusal text changes; the replay corpus shows no verdict change` → no findings [tree ee4467522d45] (2026-10-09T02:37:12Z)
## Log
- 2026-10-09T02:35:12Z created
- 2026-10-09T02:35:33Z focused
- 2026-10-09T02:37:12Z done
- 2026-10-09T02:37:12Z committed 4cd6e18 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261009-review: 1. **Answer.** Two guard-related frictions are grounded in code: the guard misreads remote interpreter code run over `ssh` as local Foreman…
- T-0234 [FEATURE L, done, 4 steps] Implementation subagents in lane worktrees — a foreman:fm-builder agent (Edit/Write/Bash) — lesson: A contract a subagent must keep nee…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar past tasks were L: consider --tier L
## Behaviour lock
none run before the first edit (missed). Instead: fm replay over 5000 real commands after the change shows 0 newly blocked and 0 newly allowed, so no verdict moved; the change only appends message text for a core tree write whose git args include 'merge'.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
