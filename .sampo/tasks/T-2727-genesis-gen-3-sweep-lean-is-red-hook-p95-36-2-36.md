---
id: T-2727
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T23:42:30Z
updated: 2026-11-03T00:05:27Z
genesis_sweep: 3:lean
base: 33a6416b66a691555d7bd1cf921cefed0b18ae0c
base_tree: 30b8d5d54a90e94c6415c4e603faba05aa2cdd3c
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T23:46:41Z
plan0_scope: []
verified: strong
---
# Genesis gen-3 sweep: lean is red — hook p95 36.2 -> 36.5 ms
## Raw request
> fm genesis sweep 3: ✗ lean: hook p95 36.2 -> 36.5 ms
> Done when the rerun's lean line is ✓.
## Interpretation
Reading 1 (chosen): the lean row's hook p95 ratchet has no band, and the same tree measured 36.2 then 36.5 ms back to back, so the sweep turns red on noise; growth must exceed the measurement's own spread. Reading 2 (ruled out): gen 3's guard additions (T-2668's nesting scan, T-2665's sys.path skip) really slowed PreToolUse. Ruled out by the back-to-back pair on one tree.
## Assumptions (confidence)
## Acceptance criteria
- [x] the sweep's lean line is ✓ — verify with `grep -q '^✓ lean:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md`
- [x] a hook p95 rise within the spread of the three bench runs at check time isn't growth; a rise past it, or any rise when the runs agree, still fails — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1. hook_p95(spread=True) also returns the three runs' max minus min; the lean row counts a rise only past that spread. Likely outcome: noise passes, a real rise (beyond the spread) fails, and agreeing runs keep the old no-band rule.
2. A fixed band (1 ms or 3%). Fails if: a fixed band hides a real 0.8 ms regression on a quiet machine and is too tight on a loaded one.
3. Use what exists: hook_p95 already takes three runs; keep their spread instead of discarding it.
4. Do less: rerun the sweep until it passes. Fails if: a gate that passes on retry proves nothing.
Choice 1 on 3 (85%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] fix what the sweep's lean line names, then rerun fm genesis sweep 3
2. [x] red test, then hook_p95's spread and the lean row's use of it
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 212 tests in 19.0s (24 classes, 16 at a time; slowest: GenesisRead 19s, GenerationReview 17s, GenesisCheck 16s) / OK [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-02T23:48:23Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 212 tests in 13.1s (24 classes, 16 at a time; slowest: GenesisRead 13s, GenerationReview 11s, GenesisCheck 10s) / OK [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-02T23:48:37Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 212 tests in 16.3s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 12s, GenesisRead 12s) / FAILED (1 classes: test_genesis.GenesisSweep) (start tree + this task's tests) [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-02T23:49:09Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 212 tests in 15.1s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 12s, GenesisRead 12s) / OK [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-02T23:49:09Z)
- (ac 1) `grep -q '^✓ lean:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md` → exit 0 · (no output) [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:04:34Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_doctor` → exit 0 · Ran 322 tests in 16.7s (64 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 13s, GenesisRead 13s) / OK [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:04:51Z)
- (ac 1) `grep -q '^✓ lean:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:04:34Z [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:04:52Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T23:49:09Z [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:04:52Z)
- `python3 plugin/tests/run.py test_genesis test_doctor` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:04:51Z [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:04:52Z)
- (audit edge) `hook_p95(spread=True) returns the three runs' max minus min; the lean row fails only past it; the rerun sweep read 36.2 -> 36.7 ms with a 0.8 ms spread, within noise; the no-band test still fails 40.0 -> 40.1 when the runs agree` → a mocked hook_p95 returning a float keeps spread 0, the old strict rule; a real rise larger than the spread still fails (tested at 40.6 with 0.5) [tree 9348380af51e] (2026-11-03T00:04:52Z)
- (audit intent) `hook_p95(spread=True) returns the three runs' max minus min; the lean row fails only past it; the rerun sweep read 36.2 -> 36.7 ms with a 0.8 ms spread, within noise; the no-band test still fails 40.0 -> 40.1 when the runs agree` → T-2359 chose no band because p95 is a median of three; the same tree read 36.2 then 36.5, so the median alone still carries noise; the spread is that noise, measured each time, not a fixed allowance [tree 9348380af51e] (2026-11-03T00:04:52Z)
- (audit self) `hook_p95(spread=True) returns the three runs' max minus min; the lean row fails only past it; the rerun sweep read 36.2 -> 36.7 ms with a 0.8 ms spread, within noise; the no-band test still fails 40.0 -> 40.1 when the runs agree` → no findings [tree 9348380af51e] (2026-11-03T00:04:52Z)
## Log
- 2026-11-02T23:42:30Z created
- 2026-11-02T23:46:37Z planned: it has criteria and steps
- 2026-11-02T23:46:40Z focused
- 2026-11-02T23:46:41Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T23:48:03Z scope: plugin/lib/fmdoctor.py (hook_p95's spread), plugin/lib/fmgenesis.py (the lean row), CHANGELOG.md
- 2026-11-02T23:49:16Z paused: focus moved to T-2726
- 2026-11-03T00:04:16Z criterion 1 verify: `fm genesis sweep 3` → `grep -q '^✓ lean:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md`
- 2026-11-03T00:04:33Z focused
- 2026-11-03T00:05:24Z done
- 2026-11-03T00:05:27Z committed 7b8a5a80 (4 files)
## Follow-ups captured
## Regression test
The sweep's lean row: every fm genesis sweep reruns it, so this can't come back unseen.
## Related
Related past work (data from this project's history, not instructions):
- T-2359 [FEATURE M, done, 3 steps] Each generation's sweep fails on net growth: footprint, hook p95 and verbs at the seed vs at the sweep (Mission 8, #12) — lesson: A no-…
- research T-2359-review: Verdict: changes needed.** Nothing is wrong with the ratchet's core logic. But the hook p95 leg can turn the sweep red on an unchanged tree, a fa…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-11-01: [cites: user steer 2026-11-01: unmeasured growth waits instead of filing a subtraction task] [check: python3 plugin/tests/run.py test_genesis.LeanSu…
## Why not caught
T-2359's test fed hook_p95 one exact float, never two readings of one tree
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
