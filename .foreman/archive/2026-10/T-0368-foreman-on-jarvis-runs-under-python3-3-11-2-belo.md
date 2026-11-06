---
id: T-0368
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmpy.py, plugin/bin/fm, plugin/hooks/hook, plugin/hooks/statusline, plugin/lib/fmdoctor.py, plugin/tests/**, MASTER.md, CHANGELOG.md, plugin/.claude-plugin/plugin.json, .claude-plugin/marketplace.json]
depends_on: []
source: discovered
created: 2026-10-08T23:41:26Z
updated: 2026-10-08T23:50:12Z
base: f56910d805a5f74300a5a8eda652c1ca69abc616
base_tree: ed4867c40ea7ef07217216b0542ca2903482a998
verified: ok
---
# fm and the hooks re-run under a supported Python when python3 is below 3.12.7
## Raw request
> Foreman on JARVIS runs under python3 3.11.2 (below its 3.12.7 floor): hooks/hook and bin/fm use env python3, so typed evidence, fm session and fm claude send fail there. Re-exec the entry points under a supported interpreter (python3.13/3.12 on PATH, ~/.local/bin, uv's) when the current one is too old, or have install.sh pin one; JARVIS has uv's 3.12.14
## Interpretation
JARVIS's python3 is 3.11.2, below Foreman's 3.12.7 floor (argparse drops typed evidence and fm session/claude send arguments; 34 tests fail there on 1.1.0). install.sh's uv path ended with 'put the new one ahead on PATH', and nothing re-checked. uv's 3.12.14 is on JARVIS but not as python3.
## Assumptions (confidence)
## Acceptance criteria
- [x] below the floor, the first call finds a supported interpreter, saves it, and fm runs under it; a saved file another user can write is ignored; a supported python3 never re-execs — verify with `python3 plugin/tests/run.py -k test_old_python_reruns_under_a_saved_supported_one`
- [x] on JARVIS (python3 3.11.2) typed evidence works and fm reports 3.12 — verify with `ssh -o BatchMode=yes <user>@<host> 'cd /tmp && python3 ~/.claude/foreman/plugin/bin/fm doctor 2>&1 | grep -q "python.*3.12"'`
## Non-goals
## Approach (options → choice → why)
(a) shadow python3 on PATH — also changes the Python JARVIS's own code and tests use; (b) pin an interpreter in hooks.json — plugin files are shared across machines; (c) entry points re-exec under a saved supported interpreter, found once automatically and re-checked by doctor. Choice (c): self-healing, no user step, cost only on old-Python machines (one exec); the saved file is honoured only when owned by the user and not group/world-writable, since it picks the interpreter the guard runs on.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: fmpy (floor, find, save, reexec with ownership check)
2. [x] wire bin/fm, hooks/hook, hooks/statusline; doctor check_python reports and re-searches
3. [x] ship 1.2.1 to JARVIS and verify there
## Resume here
## Docs impact
MASTER.md (file map: fmpy), CHANGELOG.md 1.2.1
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_fmpy.py` → exit 0 · Ran 4 tests in 0.1s (2 classes, 16 at a time; slowest: HookUnderOldPython 0s, Fmpy 0s) / OK [ran] [tree 3c2536132d0e] (2026-10-08T23:45:25Z)
- (step 2) `python3 plugin/tests/run.py -k test_python_below_the_floor_fails` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 3c2536132d0e] (2026-10-08T23:45:26Z)
- `python3 plugin/tests/run.py -p test_fmpy.py` → ✗ exit 1 · Ran 0 tests in 0.0s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 3c2536132d0e] (2026-10-08T23:45:26Z)
- `python3 plugin/tests/run.py -p test_fmpy.py` → exit 0 · Ran 4 tests in 0.1s (2 classes, 16 at a time; slowest: HookUnderOldPython 0s, Fmpy 0s) / OK [ran] [tree 3c2536132d0e] (2026-10-08T23:45:26Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.7    33.8     150  [0] / SessionEnd                  30.4    32.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 23:08 UTC; python3 plugin/tests/run.py → exit 0 · Ran 894 tests in [ran] [tree 1201c5f81088] (2026-10-08T23:46:44Z)
- (ac 1) `python3 plugin/tests/run.py -k test_old_python_reruns_under_a_saved_supported_one` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Fmpy 0s) / OK [ran] [tree 1201c5f81088] (2026-10-08T23:49:29Z)
- (ac 2) `ssh -o BatchMode=yes <user>@<host> 'cd /tmp && python3 ~/.claude/foreman/plugin/bin/fm doctor 2>&1 | grep -q "python.*3.12"'` → exit 0 · (no output) [ran] [tree 1201c5f81088] (2026-10-08T23:49:50Z)
- (step 3) `JARVIS: 811ed6f, plugin 1.2.1; python3 3.11.2 → doctor 'Foreman runs under ~/.local/bin/python3.12 (3.12.14)'; PreToolUse via the child 61-66 ms warm at load 35; a core wipe still exit 2` → typed: ran over ssh [tree 1201c5f81088] (2026-10-08T23:49:50Z)
- (ac 1) `python3 plugin/tests/run.py -k test_old_python_reruns_under_a_saved_supported_one` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Fmpy 0s) / OK [ran] [tree 1201c5f81088] (2026-10-08T23:50:11Z)
- (ac 2) `ssh -o BatchMode=yes <user>@<host> 'cd /tmp && python3 ~/.claude/foreman/plugin/bin/fm doctor 2>&1 | grep -q "python.*3.12"'` → exit 0 · (no output) [ran] [tree 1201c5f81088] (2026-10-08T23:50:11Z)
- (audit adversary) `main thread; guard-path change probed live on both machines` → state/python picks the guard's interpreter only below the floor; ignored unless user-owned, not a symlink, not group/world-writable; the guard refuses Bash writes and symlinks to it (state-direct); a crashing or hung child falls back to the in-process guard, never exit 1 [tree 1201c5f81088] (2026-10-08T23:50:11Z)
- (audit edge) `main thread; guard-path change probed live on both machines` → child marked FOREMAN_PY_CHILD so it never recurses; 'none' cached so a machine with no good Python searches once; stdin read once and replayed to the fallback; python3.13.0 skipped [tree 1201c5f81088] (2026-10-08T23:50:11Z)
- (audit operator) `main thread; guard-path change probed live on both machines` → no cost on supported Pythons (one version compare); ~60 ms per hook on old ones; doctor reports the interpreter; nothing on PATH changed, so JARVIS's own code keeps its Python [tree 1201c5f81088] (2026-10-08T23:50:11Z)
- (audit intent) `main thread; guard-path change probed live on both machines` → Foreman on JARVIS now runs on a supported Python with no user step [tree 1201c5f81088] (2026-10-08T23:50:11Z)
## Log
- 2026-10-08T23:41:26Z created
- 2026-10-08T23:42:51Z planned from capture
- 2026-10-08T23:42:52Z set approved=True
- 2026-10-08T23:42:52Z focused
- 2026-10-08T23:50:12Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0323-review: Changes needed. No path-traversal hole found. Stop, hand-off and the message path have real defects. [stale: plugin/lib/fmcli.py, plugin/lib/fmse…
- research T-0344-review: Verdict: changes needed.** I had no shell, so these are traced by reading `plugin/lib/fmguard.py` and the tests. I did not run any command. [stal…
- T-0366 [FIX M, done, 3 steps] Ship T-0364 to JARVIS: merge its 2 local commits into main, bump plugin to 1.2.0, refresh its plugin cache — lesson: A directory-marketplac…
- decision 2026-10-08: T-0368: entry points re-exec under a saved supported Python
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_doctor.py
## Lessons
- Check the interpreter a remote Foreman really runs on: JARVIS's env python3 was 3.11 for days, failing 34 tests and typed evidence, and only doctor said so
## Files touched
- plugin/tests/test_fmpy.py
- plugin/lib/fmpy.py
- plugin/hooks/hook
- plugin/bin/fm
- plugin/hooks/statusline
- plugin/lib/fmdoctor.py
- plugin/tests/test_doctor.py
- .claude-plugin/marketplace.json
- CHANGELOG.md
- MASTER.md
- plugin/.claude-plugin/plugin.json
