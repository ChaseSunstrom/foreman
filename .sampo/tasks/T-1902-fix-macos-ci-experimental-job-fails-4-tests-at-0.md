---
id: T-1902
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_code.py, plugin/tests/test_settings_scopes.py, CHANGELOG.md]
depends_on: [T-1901]
source: discovered
created: 2026-10-29T03:11:02Z
updated: 2026-10-29T03:37:31Z
base: ed4ec4901b7bbf66c1a184e6a41b6d740ef54162
base_tree: 7369195c52bc7bf9804ec4c47e6da3857295b036
plan0_at: 2026-10-29T03:22:03Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_code.py, plugin/tests/test_settings_scopes.py, CHANGELOG.md]
verified: strong
---
# FIX: macOS CI (experimental job) fails 4 tests at 06e55c1 and 48aad3d5: test_settings.Guar
## Raw request
> FIX: macOS CI (experimental job) fails 4 tests at 06e55c1 and 48aad3d5: test_settings.Guard.test_a_builder_lane_writes_nothing_outside_its_worktree (confine says /var/folders/.../tmpX/settings.json is outside worktree /var/folders/.../tmpX — /var vs /private/var symlink, reproducible on Linux with a symlinked tmp), test_settings_scopes.Cli.test_fm_settings_set_scope_project ("this project's" not in ''), test_code.Survivors x2 (runner never registered)
## Interpretation
The experimental macOS CI job fails 4 tests. 1: the guard's builder confine compares a realpath'd target against the lane as named; macOS's temp folder is a link (/var → /private/var), so a write inside the lane reads as outside it. 2: test_settings_scopes reads its pty only after fm exits, and macOS drops what's unread then (T-1828 fixed the other two pty tests with pty_reader). 3–4: test_code's cmdline/alive helpers read /proc, which macOS lacks; the code under test already falls back to ps.
## Assumptions (confidence)
## Acceptance criteria
- [x] a builder's write inside its worktree named through a link passes the guard; the main checkout at its real path stays refused — verify with `python3 plugin/tests/run.py test_guard`
- [x] the Survivors and pty settings tests read processes and terminal output without /proc or a lingering pty buffer — verify with `python3 plugin/tests/run.py test_code test_settings_scopes`
## Non-goals
## Approach (options → choice → why)
Chosen: judge the lane and main at their real paths too (Ctx keeps confine_real beside confine, as it does scratch for T-1249); the tests use pty_reader and fmideas' ps fallbacks. Considered: realpath the lane at the Ctx call sites (three of them, easy to miss one); a per-OS skip on the macOS tests (hides a guard bug a Mac user hits); normalising /private/var specifically (macOS-only, misses other links).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing guard test: a lane and main reached through links
2. [x] confine judges the lane and main at their real paths too
3. [x] test helpers: ps where there's no /proc, pty_reader in test_settings_scopes
4. [x] CHANGELOG line
## Resume here
<!-- auto -->
- 2026-10-29T03:29:07Z steps 4/4 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_code.py, plugin/tests/test_guard.py, plugin/tests/test_settings_scopes.py
- touched since last checkpoint: CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_code.py, plugin/tests/test_settings_scopes.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1904.txt, plugin/tests/test_guard.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1903.txt
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard -k link_is_confined` → red as expected (exit 1) · Ran 292 tests in 15.6s (88 classes, 16 at a time; slowest: Mutation 15s, GuardAgainstBash 14s, Trust 9s) / FAILED (1 classes) [ran] [tree 94d8d0f5b998] (2026-10-29T03:22:25Z)
- (step 2) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 292 tests in 16.9s (88 classes, 16 at a time; slowest: Mutation 16s, GuardAgainstBash 15s, Trust 9s) / OK [ran] [tree a56ec03f61ef] (2026-10-29T03:22:47Z)
- (step 3) `python3 plugin/tests/run.py test_code test_settings_scopes` → exit 0 · Ran 449 tests in 131.6s (97 classes, 16 at a time; slowest: Worker 131s, Fakes 57s, Bench 38s) / OK [ran] [tree 00c2f1042c08] (2026-10-29T03:25:05Z)
- (step 4) `grep -c T-1902 CHANGELOG.md` → exit 0 · 1 [ran] [tree 00c2f1042c08] (2026-10-29T03:25:11Z)
- (step 2) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 292 tests in 8.0s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 80de8a99fed5] (2026-10-29T03:27:13Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmguard.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.3    44.9     150  [0] / SessionEnd                  35.6    37.8     150  [0] (slower: 46.0 s vs a usual 21.2 s); claude plugin test mods/foreman-ui → exit 0 · s [ran] [tree 80de8a99fed5] (2026-10-29T03:31:59Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 292 tests in 7.8s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 80de8a99fed5] (2026-10-29T03:34:16Z)
- (ac 2) `python3 plugin/tests/run.py test_code test_settings_scopes` → exit 0 · Ran 449 tests in 76.8s (97 classes, 16 at a time; slowest: Worker 77s, Fakes 44s, Bench 21s) / OK [ran] [tree 80de8a99fed5] (2026-10-29T03:34:16Z)
- (audit intent) `One fm-reviewer pass over the diff: approve with nits. MEDIUM (the test's lane half didn't depend on the fix) fixed test-first: tightened, shown red with the rlane clause removed, green with it. LOW (test_settings out of the verify command) skipped: it can't fail on Linux; macOS CI confirms after push.` → a builder's worktree reached by a link or its real path counts as its own; main is refused at both [tree 80de8a99fed5] (2026-10-29T03:34:16Z)
- (audit adversary) `One fm-reviewer pass over the diff: approve with nits. MEDIUM (the test's lane half didn't depend on the fix) fixed test-first: tightened, shown red with the rlane clause removed, green with it. LOW (test_settings out of the verify command) skipped: it can't fail on Linux; macOS CI confirms after push.` → no bypass; a lane link pointing outside is still checked at its real path, main by either path stays confined, scratch stays scratch [tree 80de8a99fed5] (2026-10-29T03:34:16Z)
- (audit edge) `One fm-reviewer pass over the diff: approve with nits. MEDIUM (the test's lane half didn't depend on the fix) fixed test-first: tightened, shown red with the rlane clause removed, green with it. LOW (test_settings out of the verify command) skipped: it can't fail on Linux; macOS CI confirms after push.` → no confine set keeps old behaviour; no scratch (fm settings' guard) still allows the lane at both paths [tree 80de8a99fed5] (2026-10-29T03:34:16Z)
- `python3 plugin/tests/run.py test_guard -k real_path_too` → ✗ exit 1 · Ran 292 tests in 8.6s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 80de8a99fed5] (2026-10-29T03:36:02Z)
- `python3 plugin/tests/run.py test_guard -k real_path_too` → exit 0 · Ran 292 tests in 7.8s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree 80de8a99fed5] (2026-10-29T03:36:02Z)
- (audit intent) `One fm-reviewer pass over the diff: approve with nits. MEDIUM (the test's lane half didn't depend on the fix) fixed test-first: tightened, shown red with the rlane clause removed, green with it. LOW (test_settings out of the verify command) skipped: it can't fail on Linux; macOS CI confirms after push.` → a builder's worktree reached by a link or its real path counts as its own; main is refused at both [tree 80de8a99fed5] (2026-10-29T03:36:09Z)
- (audit adversary) `One fm-reviewer pass over the diff: approve with nits. MEDIUM (the test's lane half didn't depend on the fix) fixed test-first: tightened, shown red with the rlane clause removed, green with it. LOW (test_settings out of the verify command) skipped: it can't fail on Linux; macOS CI confirms after push.` → no bypass; a lane link pointing outside is still checked at its real path, main by either path stays confined, scratch stays scratch [tree 80de8a99fed5] (2026-10-29T03:36:09Z)
- (audit edge) `One fm-reviewer pass over the diff: approve with nits. MEDIUM (the test's lane half didn't depend on the fix) fixed test-first: tightened, shown red with the rlane clause removed, green with it. LOW (test_settings out of the verify command) skipped: it can't fail on Linux; macOS CI confirms after push.` → no confine set keeps old behaviour; no scratch (fm settings' guard) still allows the lane at both paths [tree 80de8a99fed5] (2026-10-29T03:36:09Z)
## Log
- 2026-10-29T03:11:02Z created
- 2026-10-29T03:18:59Z set type=FIX, tier=M, scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'plugin/tests/test_code.py', 'plugin/tests/test_settings_scopes.py', 'CHANGELOG.md'], depends_on=['T-1901']
- 2026-10-29T03:19:01Z planned: it has criteria and steps
- 2026-10-29T03:22:01Z focused
- 2026-10-29T03:37:29Z done
- 2026-10-29T03:37:31Z committed 8b4aeed4 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1284-review: Verdict:** approve with nits. I found no way to make the guard treat an outside write as inside a project, or a project or state write as outside…
- T-1249 [FIX M, done, 5 steps] CI macOS (experimental job): tests that assume Linux fail there: /proc/PID/stat reads, /tm — lesson: A failing portability test is often a …
- T-1828 [FIX M, done, 2 steps] FIX: macOS CI job (non-blocking) fails at 3f2538fc: suite hits its 1980 s deadline (test_c — lesson: macOS ptys drop unread output when the…
- decision 2026-10-23: A broken code.toml: fm code config falls back to defaults and names the line; runs keep refusing it
- similar finished tasks took 2–5 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
none: the macOS job is experimental and only CI runs macOS; no Linux test can see a /proc-less or link-temp platform
## Lessons
- On macOS the temp folder is a link: any path the guard compares must be checked as given and as realpath, as scratch already was
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
- plugin/tests/test_code.py
- plugin/tests/test_settings_scopes.py
