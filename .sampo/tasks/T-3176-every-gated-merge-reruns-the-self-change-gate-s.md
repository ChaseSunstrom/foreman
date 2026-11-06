---
id: T-3176
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T08:02:22Z
updated: 2026-11-05T10:29:38Z
builder_model: haiku
base: 8e47727c05cbb5e9c5fce9df31ee0b363085521d
base_tree: 595fbc3ad18ff95fa65d9967933052c16df90594
plan0_at: 2026-11-05T09:38:51Z
plan0_scope: []
builder_returned: 2026-11-05T09:49:12Z
lane_stop: merged 2026-11-05T10:28:21Z
verified: strong
unproven: [perf-typed]
---
# A gated merge benches the base tree once per base commit: the self-change gate caches the base side's bench and guard replay by the base tree's content hash, so back-to-back merges onto one main skip the 2-4 min base half
## Raw request
> Every gated merge reruns the self-change gate's base bench and guard replay (2-4 min) although the base is the same commit each time: cache them by the base tree's hash (selfgate.py ponytail note; T-3171 found)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] selfgate runs the base tree's bench and guard replay once per base tree hash and reuses the result (stored with the hash, the bench settings and the machine) on the next gate against the same base; a changed base, changed bench settings or a cache older than a day reruns it; the branch side always runs fresh — verify with `python3 plugin/tests/run.py test_selfgate`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: a second gate on the same base skips the base bench; a changed base or settings reruns it
2. [x] the cache in selfgate
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_selfgate 2>&1 | tail -5` → ✗ exit 1 · Ran 29 tests in 3.7s (7 classes, 16 at a time; slowest: GateEndToEnd 1s, LoadedWallCheck 1s, AaFixtures 0s) / FAILED (1 classes: test_selfgate.BaseCache) [ran] [tree b58812bebc1a] [world 2f1906870a] (2026-11-05T09:39:37Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate 2>&1 | tail -8` → ✗ exit 1 · Ran 29 tests in 3.1s (7 classes, 16 at a time; slowest: LoadedWallCheck 1s, AaFixtures 1s, MedianCpu 1s) / FAILED (1 classes: test_selfgate.BaseCache) [ran] [tree 9b0d45e32858] [world 2f1906870a] (2026-11-05T09:42:12Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate 2>&1 | grep -B3 -A14 "^FAIL:"` → ✗ exit 1 · Ran 6 tests in 0.009s / FAILED (failures=1) [ran] [tree 9b0d45e32858] [world 2f1906870a] (2026-11-05T09:42:26Z)
- (step 2) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 29 tests in 1.9s (7 classes, 16 at a time; slowest: GateEndToEnd 1s, BaseCache 1s, WhichDiffsAreTimed 1s) / OK [ran] [tree 2f0a5ef6318c] [world 2f1906870a] (2026-11-05T09:44:16Z)
- (step 1) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 29 tests in 2.3s (7 classes, 16 at a time; slowest: GateEndToEnd 1s, MedianCpu 1s, BaseCache 1s) / OK [ran] [tree 2f0a5ef6318c] [world 2f1906870a] (2026-11-05T09:44:18Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan test_selfgate && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [32.08s] [ran] [tree 2f0a5ef6318c] [world 2f1906870a] (2026-11-05T09:46:12Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate 2>&1 | grep -A12 "^FAIL\|^ERROR\|^OK\|^Ran" | head -50` → exit 0 · Ran 34 tests in 0.5s (7 classes, 16 at a time; slowest: GateEndToEnd 0s, WhichDiffsAreTimed 0s, BaseCache 0s) / OK [ran] [tree 0a456409b755] [world 2f1906870a] (2026-11-05T09:48:06Z)
- (step 2) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 34 tests in 1.6s (7 classes, 16 at a time; slowest: GateEndToEnd 1s, AaFixtures 0s, LoadedWallCheck 0s) / OK [ran] [tree 0a456409b755] [world 2f1906870a] (2026-11-05T09:48:16Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan test_selfgate && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [24.43s] [ran] [tree 0a456409b755] [world 2f1906870a] (2026-11-05T09:49:00Z)
- (step 1) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 34 tests in 0.5s (7 classes, 16 at a time; slowest: GateEndToEnd 0s, BaseCache 0s, Interleaved 0s) / OK [ran] [tree ec6de35a90fe] [world 2f1906870a] (2026-11-05T10:28:35Z)
- `python3 plugin/tests/run.py test_selfgate.BaseCache` → ✗ exit 1 · Ran 11 tests in 1.7s (1 classes, 16 at a time; slowest: BaseCache 0s) / FAILED (1 classes: test_selfgate.BaseCache) (start tree + this task's tests) [ran] [tree ec6de35a90fe] [world 2f1906870a] (2026-11-05T10:28:40Z)
- `python3 plugin/tests/run.py test_selfgate.BaseCache` → exit 0 · Ran 11 tests in 0.4s (1 classes, 16 at a time; slowest: BaseCache 0s) / OK [ran] [tree ec6de35a90fe] [world 2f1906870a] (2026-11-05T10:28:40Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T10:28:35Z [ran] [tree ec6de35a90fe] [world 2f1906870a] (2026-11-05T10:29:16Z)
- (audit adversary) `self: read the merged selfgate cache (key over base content+bench settings+machine, HMAC-SHA256 under a 0600 O_EXCL/O_NOFOLLOW key, compare_digest, day TTL, load band 1.5x); 34 selfgate tests incl. forged cache, other-key cache, private files` → forged or other-key cache reruns the base half (tests); remaining hole: the key path follows SAMPO_/FOREMAN_SECRETS, so an env-redirected merge could forge it -> captured T-3192 [tree ec6de35a90fe] (2026-11-05T10:29:16Z)
- (audit edge) `self: read the merged selfgate cache (key over base content+bench settings+machine, HMAC-SHA256 under a 0600 O_EXCL/O_NOFOLLOW key, compare_digest, day TTL, load band 1.5x); 34 selfgate tests incl. forged cache, other-key cache, private files` → changed base, settings, stale (>1 day) or load outside 1.5x reruns the bench; replay verdicts kept across load [tree ec6de35a90fe] (2026-11-05T10:29:16Z)
- (audit self) `self: read the merged selfgate cache (key over base content+bench settings+machine, HMAC-SHA256 under a 0600 O_EXCL/O_NOFOLLOW key, compare_digest, day TTL, load band 1.5x); 34 selfgate tests incl. forged cache, other-key cache, private files` → no findings [tree ec6de35a90fe] (2026-11-05T10:29:16Z)
## Log
- 2026-11-05T08:02:22Z created
- 2026-11-05T08:02:34Z planned from capture
- 2026-11-05T08:02:35Z set approved=True
- 2026-11-05T08:29:12Z blocked: planned and approved; goes to a builder when host load lets a lane in (refused at 42); not built in the main checkout, which stays quiet so the queued merges (T-3108, T-3053 chain, T-3174...) land
- 2026-11-05T09:38:26Z unblocked
- 2026-11-05T09:38:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3176.builder.md
- 2026-11-05T09:38:49Z focused
- 2026-11-05T10:28:21Z merged worktree-agent-a75439e5fc1732e5e (2 file(s))
- 2026-11-05T10:28:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a75439e5fc1732e5e
- 2026-11-05T10:28:33Z focused
- 2026-11-05T10:29:38Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3139 [PERFORMANCE M, active, 2 steps] Fast merges part 1: the bench records which modules each hook really imports, and the self-change gate times hooks only when a di…
- research T-2352-review: T-2352 review (fm-reviewer, one pass): changes needed; fixed before close (tests added after the fixes, so not seen red first).
- T-3138 [PERFORMANCE L, blocked, 4 steps] Fast merges: seconds-to-minutes instead of an hour, still proven: a runtime map of what each hook loads, content-hashed test res…
- decision 2026-11-02: [costly] Release 1.2.51: its push step conflicted because fm ship cherry-picks left foreman/build and main with diverged histories (merge base 2026-…
## Measurements
base half per gate on an unchanged base: rerun every gate (2-4 min) -> skipped on a cache hit (BaseCache tests); live timing owed on the next two merges onto one base
## Lessons
- a cache that can let a change pass a gate needs a MAC under a key the guarded agent can't read, and the key's path must not follow env
## Files touched
- plugin/tests/test_selfgate.py
- plugin/lib/sampo/selfgate.py
