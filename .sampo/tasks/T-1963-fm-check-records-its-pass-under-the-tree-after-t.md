---
id: T-1963
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T10:21:56Z
updated: 2026-10-29T10:41:25Z
base: ea0663cd7f245311f2e1471c89db3eed78d0f931
base_tree: e85e4d01927f03756eb7246b366eac57a4c08ce5
plan0_at: 2026-10-29T10:26:49Z
plan0_scope: []
verified: strong
---
# Fm check records its pass under the tree after the run (fmcli _cmd_check: tree = after or
## Raw request
> FIX: fm check records its pass under the tree after the run (fmcli _cmd_check: tree = after or tree), so an edit made while the gates ran gets a cached pass and fresh evidence it never earned; record the tested (before) tree when the tree changed mid-run, and have the Edit/Write hook note when a full fm check is running on this project (gates_running or the gate lock), since I edited mid-gates on T-1962
## Interpretation
A pass must describe the tree it tested. Today _cmd_check sets tree = after, so a mid-run edit (mine on T-1962) gets a cached pass and fresh evidence it never earned.
## Assumptions (confidence)
## Acceptance criteria
- [x] after a gate changes the tree, the next fm check reruns instead of reporting a cached pass — verify with `python3 plugin/tests/run.py test_round_f`
- [x] an Edit while a full fm check runs gets a note naming it — verify with `python3 plugin/tests/run.py test_round_f -k during`
## Non-goals
## Approach (options → choice → why)
Chosen: delete 'tree = after or tree' (when nothing changed, after == tree; when something did, the tested tree is the before one, so the cache and evidence go stale against the edited tree, which is correct); set gates_running on every full run so the PreToolUse hook can note an edit made meanwhile. Rejected: blocking edits during gates (ambient runs and long suites would stall work); a separate running-check marker file (meta gates_running already exists, T-1176); re-hashing after each gate (cost for no extra truth).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a gate that changes the tree leaves no cached pass for the changed tree
2. [x] fm check keeps the tested (before) tree when the tree changed mid-run
3. [x] every full fm check sets gates_running; the Edit/Write hook notes it once
## Resume here
<!-- auto -->
- 2026-10-29T10:30:27Z step 2/3: fm check keeps the tested (before) tree when the tree changed mid-run
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_check_paths.py, plugin/tests/test_round_f.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/tests/test_round_f.py, plugin/lib/fmhooks.py, CHANGELOG.md, MASTER.md, plugin/tests/test_check_paths.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_round_f` → ✗ exit 1 · Ran 14 tests in 4.9s (1 classes, 16 at a time; slowest: RoundF 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 403b3a553e55] (2026-10-29T10:28:08Z)
- `python3 plugin/tests/run.py test_round_f` → ✗ exit 1 · Ran 14 tests in 4.1s (1 classes, 16 at a time; slowest: RoundF 4s) / FAILED (1 classes) [ran] [tree 403b3a553e55] (2026-10-29T10:28:08Z)
- `python3 plugin/tests/run.py test_round_f` → ✗ exit 1 · Ran 14 tests in 5.0s (1 classes, 16 at a time; slowest: RoundF 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree be982b8f5828] (2026-10-29T10:28:27Z)
- `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 14 tests in 4.3s (1 classes, 16 at a time; slowest: RoundF 4s) / OK [ran] [tree be982b8f5828] (2026-10-29T10:28:27Z)
- (step 1) `python3 plugin/tests/run.py test_round_f -k changed` → exit 0 · Ran 75 tests in 5.7s (56 classes, 16 at a time; slowest: RoundF 5s, Reopen 3s, Recall 3s) / OK [ran] [tree bf77c8f39e2f] (2026-10-29T10:29:49Z)
- (step 2) `python3 plugin/tests/run.py test_round_f test_check_paths` → ✗ exit 1 · Ran 25 tests in 6.7s (4 classes, 16 at a time; slowest: CheckSkip 6s, RoundF 4s, CheckPaths 2s) / FAILED (1 classes) [ran] [tree bf77c8f39e2f] (2026-10-29T10:29:56Z)
- (step 3) `python3 plugin/tests/run.py test_round_f test_drive -k during` → exit 0 · Ran 44 tests in 12.9s (14 classes, 16 at a time; slowest: Stop 13s, DriveSide 4s, RoundF 4s) / OK [ran] [tree bf77c8f39e2f] (2026-10-29T10:30:10Z)
- (step 2) `python3 plugin/tests/run.py test_round_f test_check_paths` → exit 0 · Ran 25 tests in 6.6s (4 classes, 16 at a time; slowest: CheckSkip 6s, RoundF 4s, CheckPaths 2s) / OK [ran] [tree f08b72ce2f95] (2026-10-29T10:32:07Z)
- (step 2) `python3 plugin/tests/run.py test_round_f test_check_paths` → exit 0 · Ran 25 tests in 9.8s (4 classes, 16 at a time; slowest: CheckSkip 9s, RoundF 7s, CheckPaths 4s) / OK [ran] [tree 53f59661335e] (2026-10-29T10:33:56Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn,; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                39.9    43.4     150  [0] / SessionEnd                  34.3    37.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 53f59661335e] (2026-10-29T10:40:03Z)
- (ac 1) `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 14 tests in 4.4s (1 classes, 16 at a time; slowest: RoundF 4s) / OK [ran] [tree 53f59661335e] (2026-10-29T10:40:30Z)
- (ac 2) `python3 plugin/tests/run.py test_round_f -k during` → exit 0 · Ran 23 tests in 4.3s (10 classes, 16 at a time; slowest: RoundF 4s, Durable 2s, LoopReview 1s) / OK [ran] [tree 53f59661335e] (2026-10-29T10:40:30Z)
- `python3 plugin/tests/run.py test_round_f test_check_paths` → exit 0 · Ran 25 tests in 6.6s (4 classes, 16 at a time; slowest: CheckSkip 6s, RoundF 4s, CheckPaths 2s) / OK [ran] [tree 53f59661335e] (2026-10-29T10:40:30Z)
- (audit edge) `self: a writing gate's change no longer earns a cached pass (stamp-gate test: the 2nd check reruns, the 3rd is cached); this repo's own gates never change the tree (0 'changed during the gates' across 15 runs), so caching here is unaffected; the edit note fires only for files inside the project while a live full run on this tree is marked` → an edit outside the project, a dead pid, and another tree's run (fm ship's scratch) get no note; a marker without root (older) still notes [tree 53f59661335e] (2026-10-29T10:40:30Z)
- (audit adversary) `self: a writing gate's change no longer earns a cached pass (stamp-gate test: the 2nd check reruns, the 3rd is cached); this repo's own gates never change the tree (0 'changed during the gates' across 15 runs), so caching here is unaffected; the edit note fires only for files inside the project while a live full run on this tree is marked` → a gate that writes under another gate's paths can't launder the write into a skip; that gate reruns until it has seen the written tree [tree 53f59661335e] (2026-10-29T10:40:30Z)
- (audit self) `self: a writing gate's change no longer earns a cached pass (stamp-gate test: the 2nd check reruns, the 3rd is cached); this repo's own gates never change the tree (0 'changed during the gates' across 15 runs), so caching here is unaffected; the edit note fires only for files inside the project while a live full run on this tree is marked` → no findings [tree 53f59661335e] (2026-10-29T10:40:30Z)
## Log
- 2026-10-29T10:21:56Z created
- 2026-10-29T10:22:35Z set tier=S
- 2026-10-29T10:22:36Z planned: it has criteria and steps
- 2026-10-29T10:26:48Z focused
- 2026-10-29T10:32:07Z steer: test_check_paths' writing-gate case now expects gate 1 to rerun each time another gate writes under its paths (it never saw that write)
- 2026-10-29T10:33:56Z steer: the note ignores edits outside the project (a scratchpad write set it off while dogfooding)
- 2026-10-29T10:41:23Z done
- 2026-10-29T10:41:25Z committed 9cd7e447 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0126-review: Verdict:** changes needed. Two gates can be skipped when a covered file changed (renames, and the wrapped-around skip chain). One skipped pass is…
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- T-1924 [PERFORMANCE M, done, 1 steps] Guard: repeated 'cd X; …; cd ..' in a ; line grows its folder sets exponentially (_moved/_ — lesson: Tails after a substitution wer…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar past tasks were M: consider --tier M
- similar finished tasks took 1–4 steps
## Plan gaps
- failed first: step 2 fm check keeps the tested (before) tree when the tree changed mid-run
## Files touched
- plugin/tests/test_round_f.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_check_paths.py
