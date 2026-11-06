---
id: T-2031
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T19:03:58Z
updated: 2026-10-29T19:36:32Z
base: ec750401d0d6cbcc60e139dd43dc19b68a7208f7
base_tree: b6220bd4ab74c2f1e741282622e907ca848c5660
plan0_at: 2026-10-29T19:08:13Z
plan0_scope: []
verified: strong
---
# Fast active scan reads a small closed-keys file, not the 700 KB brief index
## Raw request
> Fast active scan reads a small closed-keys file, not the 700 KB brief index
## Interpretation
active_brief_fast runs on every PreToolUse (and 14 other hook paths). It json.loads the whole 716 KB briefs-index.json (4.1 ms) only to learn which file keys are closed. A keys-only file written beside the index answers that in a fraction of the time.
## Assumptions (confidence)
## Acceptance criteria
- [x] active_brief_fast skips closed briefs from briefs-closed.json without opening briefs-index.json, and a corrupt or stale one stays correct — verify with `python3 plugin/tests/run.py test_core -k brief_index`
## Non-goals
## Approach (options → choice → why)
(a) chosen: load_briefs writes briefs-closed.json ({name: [ino, mtime_ns, size]}) whenever it writes the index or the keys file is missing; active_brief_fast reads it, falling back to the index when it is missing or unreadable. A stale keys file stays correct: a key only matches an unchanged closed file. (b) rejected: split meta out of the index into per-brief files (more files, more stats). (c) rejected: a pickle or marshal cache (never unpickle from a state dir; marshal ties to the Python version).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: the fast scan opens no briefs-index.json once the keys file exists
2. [x] Write the keys file beside the index and read it in active_brief_fast; A/B PreToolUse
## Resume here
## Docs impact
CHANGELOG line; no other docs name the brief index
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core -k fast_scan_reads_only` → ✗ exit 1 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: BriefIndex 1s) / FAILED (1 classes) [ran] [tree 15bee090452d] (2026-10-29T19:08:33Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k brief_index 2>&1 | tail -12` → exit 0 · Ran 6 tests in 3.2s (1 classes, 16 at a time; slowest: BriefIndex 3s) / OK [ran] [tree 99a053594cfa] (2026-10-29T19:08:46Z)
- (step 2) `python3 plugin/tests/run.py test_core -k brief_index` → exit 0 · Ran 6 tests in 3.6s (1 classes, 16 at a time; slowest: BriefIndex 3s) / OK [ran] [tree a3ccdaa93487] (2026-10-29T19:09:41Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcore.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.7    32.1     150  [0] / SessionEnd                  25.2    27.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree a3ccdaa93487] (2026-10-29T19:35:58Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k brief_index` → exit 0 · Ran 6 tests in 2.3s (1 classes, 16 at a time; slowest: BriefIndex 2s) / OK [ran] [tree cfb7f0ea3eb3] (2026-10-29T19:36:25Z)
- (step 1) `python3 plugin/tests/run.py test_core -k fast_scan_reads_only` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: BriefIndex 0s) / OK [ran] [tree cfb7f0ea3eb3] (2026-10-29T19:36:25Z)
- (audit intent) `self-review of the fmcore diff and the new test (risk budget spent: no subagents)` → active_brief_fast skips closed briefs from a keys-only file and never opens the 700 KB index once it exists [tree cfb7f0ea3eb3] (2026-10-29T19:36:25Z)
- (audit edge) `self-review of the fmcore diff and the new test (risk budget spent: no subagents)` → a crash between the index and keys writes leaves the keys file older; a key matches only an unchanged closed file, so it is slower, never wrong; a corrupt or missing keys file falls back to the index and a missing one is rewritten on the next load [tree cfb7f0ea3eb3] (2026-10-29T19:36:25Z)
- (audit maintainer) `self-review of the fmcore diff and the new test (risk budget spent: no subagents)` → one name parameter on _brief_index, no new reader; fm sync copies only tasks/ and archive/, so the cache stays local [tree cfb7f0ea3eb3] (2026-10-29T19:36:25Z)
- (audit self) `self-review of the fmcore diff and the new test (risk budget spent: no subagents)` → no findings [tree cfb7f0ea3eb3] (2026-10-29T19:36:25Z)
## Log
- 2026-10-29T19:03:58Z created
- 2026-10-29T19:08:12Z focused
- 2026-10-29T19:36:30Z done
- 2026-10-29T19:36:32Z committed cbf20bd3 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2022 [PERFORMANCE M, done, 2 steps] load_briefs reads closed briefs from a stat-checked index: a hook stops opening ~1150 done briefs — lesson: A stat-checked JSON ind…
- T-1262 [FEATURE S, done, 2 steps] Guard asks through a mod tool.check with decider person, so only a person's dialog answer — lesson: Claude Code 2.1.309 has no tool.che…
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
## Measurements
PreToolUse min 39 -> 36 ms, median 40 -> 37 ms (hook_t, 15 runs x2, idle machine, real 1,204-brief state)
## Lessons
- Time A/B hook runs only on an idle machine: the same pair read 61 -> 55 ms while a ship's suite ran and 39 -> 36 ms idle
## Plan gaps
- failed first: step 1 Red test: the fast scan opens no briefs-index.json once the keys file exists
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- CHANGELOG.md
