---
id: T-3056
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: discovered
created: 2026-11-05T00:29:05Z
updated: 2026-11-06T16:29:48Z
base: da5255104c56fd26f565ba4b921968fc16002ebc
base_tree: 1fb5d53a9f8bd834fde7d23f1dce75eb3a9d038e
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T12:46:57Z
plan0_scope: [plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py, CHANGELOG.md]
builder_returned: 2026-11-06T12:53:47Z
lane_stop: merged 2026-11-06T13:18:37Z
verified: strong
lane_verified: 5257ad3eadfb71380afb19a4eb213c1bcc93a3b5
---
# Rune's drift check counts a seed line as drifted only when a second cold read confirms it, and records each read's verdict
## Raw request
> Rune's drift cold read flags a different innocuous seed line on each rerun (gen-4: first 'the exam's train split decides…', fair; then 'Frontier digest … read, never cloned', which agrees with gen-0's NEVER): a single cold read is noisy; count a line as drifted only when two reads agree or a second read confirms it, and record each read's verdict
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis drift N runs a second cold read only when the first names lines, and counts as drifted only the lines both reads name verbatim; a line one read names is listed as unconfirmed (advisory, not a failure); drift.md records each read's verdict; a clean first read costs one call as today — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in test_genesis with a fake child: first read names A, second names B: verdict clean with A and B unconfirmed; both name A: drifted on A; a clean first read makes one call
2. [x] the confirm read in rune.drift and both verdicts in drift.md
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisDrift` → ✗ exit 1 · Ran 16 tests in 39.4s (1 jobs, 16 at a time; slowest: GenesisDrift 4s) / FAILED (1 classes: test_genesis.GenesisDrift) [ran] [tree 494c3bf4c41a] [world 2f1906870a] (2026-11-06T12:47:51Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisDrift` → ✗ exit 1 · Ran 16 tests in 7.9s (1 jobs, 16 at a time; slowest: GenesisDrift 5s) / FAILED (1 classes: test_genesis.GenesisDrift) [ran] [tree 9eb82d0deadd] [world 2f1906870a] (2026-11-06T12:48:32Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisDrift` → exit 0 · Ran 16 tests in 49.5s (1 jobs, 16 at a time; slowest: GenesisDrift 5s) / OK [ran] [tree 06c40b7e62c3] [world 2f1906870a] (2026-11-06T12:49:27Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_genesis test_left_out test_models test_moons_scale test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [20.54s] [ran] [tree 06c40b7e62c3] [world 2f1906870a] (2026-11-06T12:53:05Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree a9cc86cf443c] (2026-11-06T13:18:46Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 224 tests in 72.5s (25 jobs, 16 at a time; slowest: GenerationReview 15s, ProofBeforePresentation 15s, GenesisDrift 11s) / OK [ran] [tree a9cc86cf443c] [world 2f1906870a] (2026-11-06T13:20:05Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree a9cc86cf443c] (2026-11-06T13:20:05Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree a9cc86cf443c] (2026-11-06T13:20:05Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree a9cc86cf443c] (2026-11-06T13:20:05Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree a9cc86cf443c] (2026-11-06T13:20:05Z)
## Log
- 2026-11-05T00:29:05Z created
- 2026-11-05T00:46:17Z recon: rune.py:2984 is one unseeded call; _named (rune.py:2988) only checks the quoted line exists; fix: reply 'DRIFT: <seed line> :: <gen-0 line it breaks>' and ignore hits whose gen-0 part isn't one of gen-0's MUST/NEVER lines
- 2026-11-05T02:57:17Z planned from capture
- 2026-11-05T02:57:18Z set approved=True
- 2026-11-05T02:57:18Z set scope=['plugin/lib/sampo/rune.py', 'plugin/tests/test_genesis.py', 'CHANGELOG.md']
- 2026-11-05T02:57:18Z blocked: planned and approved; waits for a builder slot
- 2026-11-06T03:52:35Z unblocked
- 2026-11-06T12:46:56Z focused
- 2026-11-06T12:46:57Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T13:18:37Z merged worktree-agent-a9762a6657441d2c2 (2 file(s))
- 2026-11-06T13:18:38Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9762a6657441d2c2
- 2026-11-06T13:18:39Z focused
- 2026-11-06T13:18:45Z set scope=['plugin/lib/sampo/rune.py', 'plugin/tests/test_genesis.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T13:18:45Z scope: widened at merge to the reviewed lane's own diff (5257ad3ea), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T13:21:36Z done
- 2026-11-06T13:21:40Z committed 44ae7c50f (1 file)
- 2026-11-06T16:29:48Z verified: the full suite is green on 1078ed22d, which contains 5257ad3ea
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-11-05: [check: python3 plugin/tests/run.py test_genesis] A single model verdict that blocks work is confirmed by a second, independent read before it blocks
- T-2613 [FEATURE M, done, 4 steps] fm exam long grade splits false dones into misses on names the goal never states and real misses — lesson: When an automatic rule repla…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_moons_scale.py, plugin/tests/test_rename_scan.py
## Preflight
Changed in scope since this was planned (2026-11-05): CHANGELOG.md, plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 failing tests in test_genesis with a fake child: first read names A, second names B: verdict clean …
- failed first: step 2 the confirm read in rune.drift and both verdicts in drift.md
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/sampo/rune.py
- CHANGELOG.md
