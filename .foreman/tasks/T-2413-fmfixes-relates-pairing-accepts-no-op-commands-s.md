---
id: T-2413
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmfixes.py, plugin/lib/fmmiss.py, plugin/tests/test_fixes.py, plugin/tests/test_miss.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-31T14:49:12Z
updated: 2026-11-02T01:09:53Z
base: 8549dbc95bc643dbbc875f58e49569ee02cb5b7b
base_tree: d21c4fd418e5e42a074fd54153a5d8d92b83d38f
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T01:00:25Z
plan0_scope: [plugin/lib/fmfixes.py, plugin/lib/fmmiss.py, plugin/tests/test_fixes.py, plugin/tests/test_miss.py, CHANGELOG.md]
verified: strong
---
# fmfixes pairs no fix whose command is a no-op (touch, mkdir, true, :, test, echo)
## Raw request
> fmfixes._relates` pairing accepts no-op commands such as `touch NAME`, which pollutes the fix store (`fmfixes.add`) as well as the new gate
> (noticed by an agent; research T-2369-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a failed command followed by 'touch NAME' (or mkdir, true, :, test, [, echo, printf as the run's only step) pairs no fix and adds nothing to the fix store; a real fix naming the same subject still pairs; fmmiss's no-op check reads the same list — verify with `python3 plugin/tests/run.py test_fixes test_tool_loop test_tool_queue`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: _relates('pytest tests/test_a.py', 'touch tests/test_a.py') is False and 'pytest -q tests/test_a.py' still True; the PostToolUse pairing path stores no fix for the touch
2. [x] fmfixes: NOOPS (moved from fmmiss, plus echo and printf) and _relates refuses a command whose every && step starts with one; fmmiss._noop uses fmfixes.NOOPS; Why not caught; CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_fixes` → ✗ exit 1 · Ran 19 tests in 9.1s (3 classes, 16 at a time; slowest: KnownFixes 9s, Fix 0s, Vague 0s) / FAILED (1 classes: test_fixes.KnownFixes) [ran] [tree 3e28eb46dc47] [world 2f1906870a] (2026-11-02T01:00:45Z)
- (step 1) `python3 plugin/tests/run.py test_fixes` → exit 0 · Ran 19 tests in 9.3s (3 classes, 16 at a time; slowest: KnownFixes 9s, Fix 0s, Vague 0s) / OK [ran] [tree 3bf5003a7094] [world 2f1906870a] (2026-11-02T01:01:58Z)
- (step 2) `python3 plugin/tests/run.py test_fixes test_tool_loop test_tool_queue test_tool_proof` → exit 0 · Ran 83 tests in 33.1s (7 classes, 16 at a time; slowest: MissLoop 33s, ToolProof 32s, GrantQueue 14s) / OK [ran] [tree 3bf5003a7094] [world 2f1906870a] (2026-11-02T01:02:32Z)
- `python3 plugin/tests/run.py test_fixes` → ✗ exit 1 · Ran 19 tests in 10.4s (3 classes, 16 at a time; slowest: KnownFixes 9s, Fix 0s, Vague 0s) / FAILED (1 classes: test_fixes.KnownFixes) (start tree + this task's tests) [ran] [tree 3bf5003a7094] [world 2f1906870a] (2026-11-02T01:02:52Z)
- `python3 plugin/tests/run.py test_fixes` → exit 0 · Ran 19 tests in 9.2s (3 classes, 16 at a time; slowest: KnownFixes 9s, Fix 0s, Vague 0s) / OK [ran] [tree 3bf5003a7094] [world 2f1906870a] (2026-11-02T01:02:52Z)
- (ac 1) `python3 plugin/tests/run.py test_fixes test_tool_loop test_tool_queue` → exit 0 · Ran 57 tests in 33.2s (5 classes, 16 at a time; slowest: MissLoop 33s, GrantQueue 14s, KnownFixes 9s) / OK [ran] [tree 5bae01a91c47] [world 2f1906870a] (2026-11-02T01:09:27Z)
- (audit edge) `self-review: _relates now refuses a command whose every && step starts with a no-op (touch, mkdir, true, :, test, [), checked before the subject match; a no-op step before a real command (touch x && mytool) still pairs; fmmiss reads the same NOOPS from fmfixes (it imports fmfixes already), so the miss gate and the store agree` → 'touch mytool' and 'mkdir -p mytool' pair nothing; 'mytool --check --fix' still pairs; an empty command pairs nothing [tree 5bae01a91c47] (2026-11-02T01:09:27Z)
- (audit self) `self-review: _relates now refuses a command whose every && step starts with a no-op (touch, mkdir, true, :, test, [), checked before the subject match; a no-op step before a real command (touch x && mytool) still pairs; fmmiss reads the same NOOPS from fmfixes (it imports fmfixes already), so the miss gate and the store agree` → no findings [tree 5bae01a91c47] (2026-11-02T01:09:27Z)
## Log
- 2026-10-31T14:49:12Z created
- 2026-11-02T00:39:43Z planned from capture
- 2026-11-02T01:00:24Z focused
- 2026-11-02T01:00:25Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T01:01:49Z criterion 1 verify: `python3 plugin/tests/run.py test_fixes test_miss` → `python3 plugin/tests/run.py test_fixes test_tool_loop test_tool_queue`
- 2026-11-02T01:02:53Z scope: CHANGELOG.md entry; test_miss doesn't exist: fmmiss is covered by test_tool_loop and test_tool_queue
- 2026-11-02T01:09:51Z done
- 2026-11-02T01:09:53Z committed 180aef8b (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2369-review: Verdict: changes needed.** The core loop works: log the miss, lead in `fm next`, refuse finish and done, resolve by run evidence. But the module-…
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- research T-1032-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** changes needed. Two MEDIUM findings should be fixed befor…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_fixes.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md; re-ground the plan against them before editing
## Why not caught
The pairing tests used real retries; fmmiss got its no-op list for its own fix_paired check (T-2372), but fmfixes' store, which feeds it, never did.
## Lessons
- Keep one list of commands that prove nothing and have every pairing read it; two lists drift
## Plan gaps
- failed first: step 1 red test: _relates('pytest tests/test_a.py', 'touch tests/test_a.py') is False and 'pytest -q tests…
## Files touched
- plugin/tests/test_fixes.py
- plugin/lib/fmfixes.py
- plugin/lib/fmmiss.py
- CHANGELOG.md
