---
id: T-2180
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T15:41:07Z
updated: 2026-10-31T03:54:07Z
base: 81432c0201f68c53f7e3d355b5f93937d41cf0f2
base_tree: bb9a2c3ee1a797df7f4027129a5e09736f1a9eaa
plan0_at: 2026-10-31T03:44:17Z
plan0_scope: []
verified: strong
---
# One CLEAN verdict regex for drift and the cold read, with tests that CLEANUP and 'Not CLEAN' don't pass
## Raw request
> drift` and the new `_read` both use `^[\s*]*CLEAN\b` (so "CLEAN" at the start of any line passes). It could be a shared constant with a test for "CLEANUP needed" or "Not CLEAN"
> (noticed by an agent; research T-2166-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] drift and _read share one constant matching a whole-line CLEAN verdict; 'CLEANUP needed', 'Not CLEAN' and 'CLEAN-ish' don't pass, 'CLEAN' and '**CLEAN**' do — verify with `cd plugin/tests && python3 -m unittest -q test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests on both readers; one CLEAN constant
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis 2>&1 | tail -15` → ✗ exit 1 · Ran 144 tests in 91.599s / FAILED (failures=2) [ran] [tree 6ea1b0d923a1] (2026-10-31T03:46:01Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis 2>&1 | tail -6` → exit 0 · Ran 144 tests in 119.490s / OK [ran] [tree 169e92e52f8b] (2026-10-31T03:48:10Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis 2>&1 | tail -6` → exit 0 · Ran 144 tests in 119.490s / OK [ran] [tree 169e92e52f8b] (2026-10-31T03:48:10Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis` → exit 0 · Ran 144 tests in 60.139s / OK [ran] [tree 169e92e52f8b] (2026-10-31T03:49:14Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead test_genesis.GenesisDrift` → ✗ exit 1 · Ran 30 tests in 10.511s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree 9aec6b917f18] (2026-10-31T03:51:54Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead test_genesis.GenesisDrift` → exit 0 · Ran 30 tests in 11.005s / OK [ran] [tree 9aec6b917f18] (2026-10-31T03:51:54Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis` → exit 0 · Ran 144 tests in 43.721s / OK [ran] [tree 9aec6b917f18] (2026-10-31T03:52:57Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis` → exit 0 · Ran 144 tests in 44.217s / OK [ran] [tree 9aec6b917f18] (2026-10-31T03:53:43Z)
- (audit edge) `self: one CLEAN_VERDICT (whole line: optional spaces and asterisks, CLEAN, optional asterisks, period or spaces) used by the cold read and drift; CLEANUP, Not CLEAN, CLEAN-ish and 'CLEAN but …' fail, CLEAN, **CLEAN** and CLEAN. pass; the stray-quote and objection checks are untouched; test_genesis 144 green; red-to-green proven` → a reply with CLEAN on one line and an objection on another still fails through the named-line and quote checks, unchanged [tree 9aec6b917f18] (2026-10-31T03:53:43Z)
- (audit self) `self: one CLEAN_VERDICT (whole line: optional spaces and asterisks, CLEAN, optional asterisks, period or spaces) used by the cold read and drift; CLEANUP, Not CLEAN, CLEAN-ish and 'CLEAN but …' fail, CLEAN, **CLEAN** and CLEAN. pass; the stray-quote and objection checks are untouched; test_genesis 144 green; red-to-green proven` → no findings [tree 9aec6b917f18] (2026-10-31T03:53:43Z)
## Log
- 2026-10-30T15:41:07Z created
- 2026-10-31T03:43:39Z planned from capture
- 2026-10-31T03:43:40Z set approved=True
- 2026-10-31T03:43:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2180.builder.md
- 2026-10-31T03:44:16Z focused
- 2026-10-31T03:51:30Z merged worktree-agent-aeb7b5eb320a7c6b0 (3 file(s))
- 2026-10-31T03:51:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aeb7b5eb320a7c6b0
- 2026-10-31T03:51:31Z focused
- 2026-10-31T03:52:57Z scope: plugin/lib/fmgenesis.py (CLEAN_VERDICT), plugin/tests/test_genesis.py, CHANGELOG.md
- 2026-10-31T03:54:07Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research T-2155-review: Changes needed.** The `exam.jsonl` refusal is correct and tested, but the request's second half, the forged-Verdict case, isn't fixed. [stale: pl…
- research T-2104-review: Verdict: changes needed.** One HIGH finding makes sweep red for good once its Mission tasks are archived. A MEDIUM finding makes a cold read that…
- decision 2026-10-30: Genesis drift skips the paid cold read when the deterministic check already found drift: one read per clean candidate
- similar past tasks were M: consider --tier M
## Lessons
- Two readers of one verdict share one pattern, with negative examples in the test
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
