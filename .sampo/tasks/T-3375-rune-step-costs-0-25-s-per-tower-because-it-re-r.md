---
id: T-3375
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py]
depends_on: []
source: discovered
created: 2026-11-06T06:21:36Z
updated: 2026-11-06T14:24:46Z
base: a846d571795977e2cd5def425617add80f4ea3c8
base_tree: d4e495c56c3a0c401b4d601f3308d70d06762abc
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T08:56:54Z
plan0_scope: []
builder_returned: 2026-11-06T09:14:52Z
lane_stop: merged 2026-11-06T10:45:16Z
verified: strong
unproven: [meaning, perf-typed]
---
# rune.step costs ~0.25 s per tower because it re-reads the ledger ~80 times; the Rune…
## Raw request
> PERF: rune.step costs ~0.25 s per tower because it re-reads the ledger ~80 times; the Rune export spends ~3 s of 13 s on 26 towers (T-3266)
## Interpretation
Reading 1: speed up rune.step by scanning the ledger once per state, output unchanged. Reading 2: cut how many times step calls it (ruled out: the calls are cheap, the scan is 85 ms).
## Assumptions (confidence)
## Acceptance criteria
- [x] step output is identical with the cache and the ledger is scanned once per state, and an appended event is seen — verify with `python3 plugin/tests/run.py test_genesis -k Memo`
## Non-goals
## Approach (options → choice → why)
1) Pass parsed events down every call chain: invasive, fails if a chain misses a caller. 2) Use what exists: memoise in core.ledger_events, likely outcome: shared dicts mutated by other callers. 3) Do less: memoise only in rune._events keyed by file path/mtime/size; likely outcome: step drops to one scan. Choice 3 (80%): smallest, rune callers read-only.
## Risks and rollback
## Execution prompt
## Steps
1. [x] add a test pinning identical step output and one scan; memoise rune._events
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k GenesisStepMemo` → exit 0 · Ran 1 tests in 16.3s (1 jobs, 16 at a time; slowest: GenesisStepMemo 0s) / OK [ran] [tree 5613569bfc46] [world 2f1906870a] (2026-11-06T08:58:19Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree 5613569bfc46] [world 2f1906870a] (2026-11-06T08:58:22Z)
- (step 1) `python3 plugin/tests/run.py -k GenesisStepMemo` → exit 0 · Ran 1 tests in 27.8s (1 jobs, 16 at a time; slowest: GenesisStepMemo 0s) / OK [ran] [tree 8257f404ecc7] [world 2f1906870a] (2026-11-06T09:13:09Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_genesis test_left_out test_models test_moons_scale test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [22.52s] [ran] [tree 8257f404ecc7] [world 2f1906870a] (2026-11-06T09:14:40Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 306a891ce42f] (2026-11-06T10:45:19Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 221 tests in 12.1s (25 jobs, 16 at a time; slowest: GenerationReview 10s, ProofBeforePresentation 9s, GenesisExport 7s) / FAILED (1 classes: test_genesis.GenesisStepMemo) (start tree + this task's tests) [ran] [tree 306a891ce42f] [world 2f1906870a] (2026-11-06T10:45:47Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 221 tests in 13.5s (25 jobs, 16 at a time; slowest: GenerationReview 13s, ProofBeforePresentation 13s, GenesisSweep 7s) / OK [ran] [tree 306a891ce42f] [world 2f1906870a] (2026-11-06T10:45:47Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis -k Memo` → exit 0 · Ran 1 tests in 0.5s (1 jobs, 16 at a time; slowest: GenesisStepMemo 0s) / OK [ran] [tree 306a891ce42f] [world 2f1906870a] (2026-11-06T10:45:49Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 306a891ce42f] (2026-11-06T10:45:49Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 306a891ce42f] (2026-11-06T10:45:49Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 306a891ce42f] (2026-11-06T10:45:49Z)
## Log
- 2026-11-06T06:21:36Z created
- 2026-11-06T08:56:37Z planned: it has criteria and steps
- 2026-11-06T08:56:53Z focused
- 2026-11-06T08:56:54Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T10:43:57Z criterion 1 verify: `python3 plugin/tests/run.py plugin/tests/test_genesis.py -k Memo` → `python3 plugin/tests/run.py test_genesis -k Memo`
- 2026-11-06T10:45:16Z merged worktree-agent-acf088c99b88ed4c7 (2 file(s))
- 2026-11-06T10:45:16Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acf088c99b88ed4c7
- 2026-11-06T10:45:17Z focused
- 2026-11-06T10:45:18Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/rune.py', 'plugin/tests/test_genesis.py']
- 2026-11-06T10:45:19Z scope: widened at merge to the reviewed lane's own diff (a76c8187e), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T10:46:23Z done
- 2026-11-06T10:46:25Z committed f84d5ed2f (1 file)
- 2026-11-06T14:24:46Z not reverted: test_check_paths.CheckSkip, test_claims.Claims, test_close_gates.CloseGates already fail on a76c8187e's first parent
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-10-31: [costly] Tower filing waits for the user's call on the cold-read rule: Missions 5-8's files and the Mission 3-4 critiques stay unfiled after 4-12 pu…
- similar past tasks were L: consider --tier L
## Measurements
27-tower rune.step loop: 3.05 s -> 0.27 s, ledger scans 56 -> 3 (lane timing on the same state; output sha256 unchanged)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/sampo/rune.py
- CHANGELOG.md
