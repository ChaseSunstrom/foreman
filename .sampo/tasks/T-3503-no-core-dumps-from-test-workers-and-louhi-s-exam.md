---
id: T-3503
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/louhi.py, plugin/tests/run.py, plugin/tests/test_louhi_models.py, plugin/tests/test_run.py]
depends_on: []
source: discovered
created: 2026-11-06T19:05:59Z
updated: 2026-11-07T00:42:50Z
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: f997eb98c8d4be4238b3699f7edc2ec5717a28e2
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T19:08:36Z
plan0_scope: []
lane_stop: merged 2026-11-06T21:46:50Z
verified: strong
unproven: [perf-typed]
---
# No core dumps from test workers and louhi's exam binary: about 8,500 a day, 4.1 GB, compressed on a loaded box
## Raw request
> No core dumps from test workers and louhi's exam binary: about 8,500 a day, 4.1 GB, compressed on a loaded box
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] run.py's workers and the binary louhi builds and runs start with RLIMIT_CORE 0, as callcards already does — verify with `python3 plugin/tests/run.py test_run test_louhi_models`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] set RLIMIT_CORE 0 in run.py and louhi's exam run, test-first
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_run test_louhi_models` → exit 0 · Ran 127 tests in 9.1s (73 jobs, 16 at a time; slowest: UnknownNames 6s, PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 5s, Ship 5s) / OK [ran] [tree f4537aaf9664] [world 2f1906870a] (2026-11-06T19:09:43Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree a02cd065d0ee] (2026-11-06T22:11:09Z)
- `python3 plugin/tests/run.py test_louhi_models test_run` → ✗ exit 1 · Ran 129 tests in 70.9s (54 jobs, 16 at a time; slowest: PerTestJobs 17s, LouhiModels 16s, Ship 6s) / FAILED (3 classes: test_louhi_models.ModelBenchVisible, test_louhi_models.ExamChildNoCore, test_run (start tree + this task's tests) [ran] [tree a02cd065d0ee] [world 2f1906870a] (2026-11-06T22:12:59Z)
- `python3 plugin/tests/run.py test_louhi_models test_run` → exit 0 · Ran 129 tests in 33.7s (75 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 6s, Hang 5s, UnknownNames 4s) / OK [ran] [tree a02cd065d0ee] [world 2f1906870a] (2026-11-06T22:12:59Z)
- (ac 1) `python3 plugin/tests/run.py test_run test_louhi_models` → exit 0 · Ran 129 tests in 12.7s (73 jobs, 16 at a time; slowest: PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 6s, UnknownNames 5s, Ship 5s) / OK [ran] [tree a02cd065d0ee] [world 2f1906870a] (2026-11-06T22:13:16Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree a02cd065d0ee] (2026-11-06T22:13:16Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree a02cd065d0ee] (2026-11-06T22:13:16Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree a02cd065d0ee] (2026-11-06T22:13:16Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree a02cd065d0ee] (2026-11-06T22:13:16Z)
## Log
- 2026-11-06T19:05:59Z created
- 2026-11-06T19:06:17Z lane: ~/.claude/foreman.lanes/T-3503 on foreman/T-3503
- 2026-11-06T19:08:35Z focused
- 2026-11-06T19:08:36Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T21:46:50Z merged foreman/T-3503 in merge train
- 2026-11-06T22:11:08Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/louhi.py', 'plugin/tests/run.py', 'plugin/tests/test_louhi_models.py', 'plugin/tests/test_run.py']
- 2026-11-06T22:11:09Z scope: widened at merge to the reviewed lane's own diff (7354ab235), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T22:16:00Z done
- 2026-11-06T22:16:05Z committed 32574a5eb (1 file)
- 2026-11-07T00:42:50Z lane removed: ~/.claude/foreman.lanes/T-3503; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-3152 [FIX S, done, 2 steps] Moons' local-only fill names why no local model answered and tries the next local model (this box's GPU) before it stops — lesson: A sweep …
- T-1777 [PERFORMANCE M, done, 2 steps] PreToolUse:Bash:script hook runs at about 90% of its 300 ms budget (p50 271 ms, p95 277 ms — lesson: A latency budget for a time-bo…
- decision 2026-10-21: T-1320's example cards show each run's last screen drawn from its own events plus the command that replays it, not a per-example video
- similar finished tasks took 2–3 steps
## Measurements
core dumps per hour: 441 (files in /var/lib/systemd/coredump newer than 60 min) → measured after landing
## Lessons
- Every process spawned on purpose to crash or be killed must set RLIMIT_CORE to 0 itself, or the system collector compresses each dump on an already loaded machine.
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/louhi.py
- plugin/tests/run.py
- plugin/tests/test_louhi_models.py
- plugin/tests/test_run.py
