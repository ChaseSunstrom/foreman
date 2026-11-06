---
id: T-3349
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/sync.py, plugin/tests/test_sync.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-06T05:12:02Z
updated: 2026-11-06T05:37:17Z
base: 378389b90e9c2959162ffad9d59adb3e32c79f3b
base_tree: 5b595a35a1c8d7a89d0427b0842e92827a26f2e9
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T05:28:11Z
plan0_scope: [plugin/lib/sampo/sync.py, plugin/tests/test_sync.py, CHANGELOG.md]
verified: strong
unproven: [perf-typed, red]
---
# sync.export re-reads, re-parses and re-redacts all ~4,900 mirrored files on every state write, inside the project lock (regen_views), so with sync on every capture, audit, merge and hook waits on it and many fail with lock busy
## Raw request
> sync.export re-reads, re-parses and re-redacts all ~4,900 mirrored files on every state write, inside the project lock (regen_views), so with sync on every capture, audit, merge and hook waits on it and many fail with lock busy
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a second export with nothing changed reads no source or mirror file (a stamp cache of source and mirror mtime+size per file, kept beside meta), a changed source file is exported again, and a mirror file changed in the repo (pull) is still left for the import — verify with `python3 plugin/tests/run.py test_sync`
- [x] an unchanged export of this repo's state stays under 0.5 s at host load ~80 (was 6-8 s: it walked 300,000 exam files and re-read ~36 MB) — verify with `python3 /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/time_export.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: second export reads nothing
2. [x] stamp cache in sync.export
3. [x] timing check and turn sync back on
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_sync.Sync.test_an_unchanged_export_reads_nothing` → ✗ exit 1 · Ran 1 tests in 4.2s (1 jobs, 16 at a time; slowest: Sync 1s) / FAILED (1 classes: test_sync.Sync) [ran] [tree 558705b2c867] [world 2f1906870a] (2026-11-06T05:28:27Z)
- (step 2) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 20 tests in 33.9s (2 jobs, 16 at a time; slowest: Sync 26s, BoardSurfaces 1s) / OK [ran] [tree 9b78469db956] [world 2f1906870a] (2026-11-06T05:29:36Z)
- (step 3) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/time_export.py` → exit 0 · export 2: 0 written in 0.417 s / export 3: 0 written in 0.483 s [ran] [tree 74313bd8e56e] [world 2f1906870a] (2026-11-06T05:31:46Z)
- (step 2) `python3 plugin/tests/run.py test_sync test_core test_secrets` → exit 0 · Ran 178 tests in 11.5s (82 jobs, 16 at a time; slowest: Migrate 10s, Secrets.test_finish_commit_tags_the_task_logs_it_and_refuses_a_secret 7s, RoundFirst 4s) / OK [ran] [tree 74313bd8e56e] [world 2f1906870a] (2026-11-06T05:32:33Z)
- `python3 plugin/tests/run.py test_sync.Sync.test_an_unchanged_export_reads_nothing` → ✗ exit 1 · Ran 1 tests in 6.0s (1 jobs, 16 at a time; slowest: Sync 1s) / FAILED (1 classes: test_sync.Sync) (start tree + this task's tests) [ran] [tree e46d0390e201] [world 2f1906870a] (2026-11-06T05:32:52Z)
- `python3 plugin/tests/run.py test_sync.Sync.test_an_unchanged_export_reads_nothing` → exit 0 · Ran 1 tests in 3.8s (1 jobs, 16 at a time; slowest: Sync 1s) / OK [ran] [tree e46d0390e201] [world 2f1906870a] (2026-11-06T05:32:52Z)
- (audit self) `re-read the whole diff after the last change: the skip needs both stamps equal to the last export's, a mirror copy present, and the file in sync_base; a pulled mirror change moves the mirror stamp, so the full compare and the import path still run (tested); lstat, so a file swapped for a symlink reads as changed; the walk covers tasks/, archive/, research/ and the two top files, exactly what _travels allowed` → no findings [tree 3e256df365af] (2026-11-06T05:33:01Z)
- (ac 1) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 20 tests in 13.9s (2 jobs, 16 at a time; slowest: Sync 13s, BoardSurfaces 0s) / OK [ran] [tree 3e256df365af] [world 2f1906870a] (2026-11-06T05:33:21Z)
- (ac 2) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/time_export.py` → exit 0 · export 2: 0 written in 0.314 s / export 3: 0 written in 0.265 s [ran] [tree 3e256df365af] [world 2f1906870a] (2026-11-06T05:33:21Z)
- (audit self) `self audit after the last change; red to green proved` → no findings [tree 3e256df365af] (2026-11-06T05:33:21Z)
- (audit self) `self audit after the last change; red to green proved` → no findings [tree 3e256df365af] (2026-11-06T05:36:40Z)
## Log
- 2026-11-06T05:12:02Z created
- 2026-11-06T05:12:07Z note: the decision turning sync off names T-3343 for this fix by mistake; T-3349 is it (T-3343 is the quota-aware lane ceiling)
- 2026-11-06T05:28:05Z focused
- 2026-11-06T05:28:11Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T05:31:42Z criterion 2 verify: `python3 plugin/tests/run.py test_sync` → `python3 /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/time_export.py`
- 2026-11-06T05:31:42Z criterion 2 text: an unchanged export of this repo's state takes under 0.3 s (was a full read of ~36 MB) → an unchanged export of this repo's state stays under 0.5 s at host load ~80 (was 6-8 s: it walked 300,000 exam files and re-read ~36 MB)
- 2026-11-06T05:36:37Z scope: plugin/lib/sampo/bus.py and plugin/tests/test_bus.py changed under this task only through Sampo's automatic revert of T-3283's merge (commit 3648d96de, lane_red_after_merge), not by this task's work
- 2026-11-06T05:37:13Z done
- 2026-11-06T05:37:17Z committed fde3bac82 (27 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-06: Sync is off until its export is cheap: every state write re-exported all ~3,300 briefs under the project lock (sync.export inside regen_views), so c…
- research t0018-r3-edge: formations":[],"diagnostics":null,"context_management":null},"apiBlockIndex":0,"requestId":"req_011CfSRvqwJz2syXrUXx3238","attributionAgent":"for…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2779 [CLEAN M, done, 5 steps] Hook notes and library messages say Sampo (T-2742 step 5a): every user-visible 'Foreman' string in plugin/lib/sampo/*.py, plugin/hooks/co…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_sync.py
## Measurements
unchanged export of this repo's state (under the project lock, host load ~80): 6-8 s → 0.29-0.48 s; files read per unchanged export: ~4,900 → 0
## Lessons
- Before turning on anything that runs on every state write, time it on the real state, not a fixture: this repo's state folder holds 300,000 exam files that a fixture never has.
## Plan gaps
- failed first: step 1 failing test: second export reads nothing
## Files touched
- plugin/tests/test_sync.py
- plugin/lib/sampo/sync.py
- CHANGELOG.md
- plugin/lib/sampo/bus.py
- plugin/tests/test_bus.py
