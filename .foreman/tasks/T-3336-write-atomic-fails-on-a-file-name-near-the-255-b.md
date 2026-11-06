---
id: T-3336
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/core.py, plugin/tests/test_core.py, CHANGELOG.md, plugin/lib/sampo/secrets.py, plugin/tests/test_secrets.py]
depends_on: []
source: discovered
created: 2026-11-06T04:44:37Z
updated: 2026-11-06T05:03:37Z
base: a6a471ef6fa5fded57eb011ae2e37df8c93c003f
base_tree: c00f587f3487ccb8e918e1520ddefba67ef52542
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T04:44:47Z
plan0_scope: [plugin/lib/sampo/core.py, plugin/tests/test_core.py, CHANGELOG.md]
verified: strong
unproven: [red]
---
# write_atomic fails on a file name near the 255-byte limit: its temp name is '.' + the whole name + 8 random chars + '.tmp', so sampo sync on refused (Errno 36) on a long brainstorm file and stayed off
## Raw request
> write_atomic fails on a file name near the 255-byte limit: its temp name is '.' + the whole name + 8 random chars + '.tmp', so sampo sync on refused (Errno 36) on a long brainstorm file and stayed off
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] write_atomic writes a file whose name is 250 bytes long, and leaves no temp file behind — verify with `python3 plugin/tests/run.py test_core`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with a 250-byte name
2. [x] cap the temp prefix in write_atomic
3. [x] URL passwords that are placeholders don't block a commit (test first)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core.WritesAndLocks` → ✗ exit 1 · Ran 3 tests in 3.6s (1 jobs, 16 at a time; slowest: WritesAndLocks 2s) / FAILED (1 classes: test_core.WritesAndLocks) [ran] [tree bbf4005a5de0] [world 2f1906870a] (2026-11-06T04:45:09Z)
- (step 2) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 145 tests in 9.6s (49 jobs, 16 at a time; slowest: Migrate 8s, RoundFirst 5s, PreToolUse 4s) / OK [ran] [tree da54ab8736ea] [world 2f1906870a] (2026-11-06T04:45:29Z)
- (step 2) `python3 plugin/tests/run.py test_core test_sync` → exit 0 · Ran 164 tests in 11.5s (70 jobs, 16 at a time; slowest: Migrate 9s, ConfidenceRoutes.test_an_assumption_under_the_bar_is_refused_until_a_verified_check_a_cold_reader_agrees_with 4s, PreToolUse 4s) / O [ran] [tree 9663420fefbe] [world 2f1906870a] (2026-11-06T04:45:54Z)
- `python3 plugin/tests/run.py test_core.WritesAndLocks` → ✗ exit 1 · Ran 3 tests in 8.2s (1 jobs, 16 at a time; slowest: WritesAndLocks 2s) / FAILED (1 classes: test_core.WritesAndLocks) (start tree + this task's tests) [ran] [tree f496bfb3c29c] [world 2f1906870a] (2026-11-06T04:46:22Z)
- `python3 plugin/tests/run.py test_core.WritesAndLocks` → exit 0 · Ran 3 tests in 3.0s (1 jobs, 16 at a time; slowest: WritesAndLocks 2s) / OK [ran] [tree f496bfb3c29c] [world 2f1906870a] (2026-11-06T04:46:22Z)
- (audit self) `read the diff: one shared helper, every caller benefits; edge: multi-byte names (4-byte chars) checked by the é case, 40 chars ≤160 bytes; the planted-symlink protection (mkstemp O_EXCL) is unchanged` → no findings [tree f496bfb3c29c] (2026-11-06T04:46:23Z)
- (ac 1) `python3 plugin/tests/run.py test_core` → exit 0 · Ran 145 tests in 9.7s (51 jobs, 16 at a time; slowest: Migrate 8s, PreToolUse 4s, ConfidenceRoutes.test_an_assumption_under_the_bar_is_refused_until_a_verified_check_a_cold_reader_agrees_with 3s) / OK [ran] [tree f496bfb3c29c] [world 2f1906870a] (2026-11-06T04:46:42Z)
- (audit self) `self audit after the last change; red to green proved` → no findings [tree f496bfb3c29c] (2026-11-06T04:46:42Z)
- (step 3) `python3 plugin/tests/run.py test_secrets` → ✗ exit 1 · Ran 12 tests in 11.4s (5 jobs, 16 at a time; slowest: Secrets 10s, KnownFixes 1s, Session 1s) / FAILED (1 classes: test_secrets.Secrets) [ran] [tree c11f5a964804] [world 2f1906870a] (2026-11-06T04:51:12Z)
- (step 3) `python3 plugin/tests/run.py test_secrets test_core` → exit 0 · Ran 157 tests in 10.0s (61 jobs, 16 at a time; slowest: Migrate 8s, RoundFirst 6s, Secrets.test_finish_commit_tags_the_task_logs_it_and_refuses_a_secret 5s) / OK [ran] [tree 46394710365e] [world 2f1906870a] (2026-11-06T04:51:54Z)
- (step 3) `python3 plugin/tests/run.py test_secrets test_core test_find` → exit 0 · Ran 281 tests in 34.0s (142 jobs, 16 at a time; slowest: FindRenders 33s, Migrate 9s, FindBlindSpots.test_a_new_day_files_the_next_unfiled_record_not_the_same_one 7s) / OK [ran] [tree 886a03a3964a] [world 2f1906870a] (2026-11-06T04:53:46Z)
- (audit self) `re-read the whole diff after the last change: write_atomic prefix cut at 40 chars (≤160 bytes); URL passwords skipped only when the whole password is a placeholder word or matches the shared PLACEHOLDER rule; ISO dates skipped only on a full match, not for tokens; real values in the same shapes still flagged (tests)` → no findings [tree d45bde23ebc9] (2026-11-06T04:55:03Z)
- (audit adversary) `could a real credential now pass? only if its entire value is one of 7 words, a PLACEHOLDER match (the existing rule for literals), or a full ISO date; a real password embedding 'pass' (Zq8Lm2Xv9Rpass) still flags (test)` → none [tree d45bde23ebc9] (2026-11-06T04:55:17Z)
- `python3 plugin/tests/run.py test_secrets test_core.WritesAndLocks` → ✗ exit 1 · Ran 16 tests in 12.8s (6 jobs, 16 at a time; slowest: Secrets 9s, WritesAndLocks 2s, KnownFixes 1s) / FAILED (2 classes: test_secrets.Secrets, test_core.WritesAndLocks) (start tree + this task's tests) [ran] [tree d45bde23ebc9] [world 2f1906870a] (2026-11-06T04:55:55Z)
- `python3 plugin/tests/run.py test_secrets test_core.WritesAndLocks` → exit 0 · Ran 16 tests in 6.0s (14 jobs, 16 at a time; slowest: Secrets.test_finish_commit_tags_the_task_logs_it_and_refuses_a_secret 5s, Secrets.test_finish_commit_takes_paths_literally_and_leaves_out_an_ignor [ran] [tree d45bde23ebc9] [world 2f1906870a] (2026-11-06T04:55:55Z)
- (audit self) `self and adversary recorded after the last change; red to green proved for both fixes` → no findings [tree d45bde23ebc9] (2026-11-06T04:56:26Z)
- (step 3) `python3 plugin/tests/run.py test_secrets test_core` → exit 0 · Ran 158 tests in 10.6s (62 jobs, 16 at a time; slowest: Migrate 9s, Secrets.test_finish_commit_tags_the_task_logs_it_and_refuses_a_secret 6s, RoundFirst 3s) / OK [ran] [tree 8f7fc6ecdfbe] [world 2f1906870a] (2026-11-06T04:59:16Z)
- (audit self) `re-read after marking the three test lines that hold sample URL credentials with the allowlist pragma (detect-secrets convention); no code change` → no findings [tree 8f7fc6ecdfbe] (2026-11-06T04:59:35Z)
- (audit adversary) `the pragma only exempts those test lines; scanner rules unchanged since the last adversary pass` → none [tree 8f7fc6ecdfbe] (2026-11-06T05:00:09Z)
- (audit self) `self and adversary recorded after the last change; red to green proved for both fixes` → no findings [tree 8f7fc6ecdfbe] (2026-11-06T05:00:40Z)
## Log
- 2026-11-06T04:44:37Z created
- 2026-11-06T04:44:40Z focused
- 2026-11-06T04:44:47Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T04:49:37Z set scope=['plugin/lib/sampo/core.py', 'plugin/tests/test_core.py', 'CHANGELOG.md', 'plugin/lib/sampo/secrets.py', 'plugin/tests/test_secrets.py']
- 2026-11-06T04:50:00Z scope: the close's commit scan refused .foreman/research/T-1859-review.md:12, a review quoting https://user:[REDACTED]@host as an example; the URL-password pattern never asked is_placeholder, so placeholder URL passwords (pass, password, example…) block every commit of the mirror. Fixed here because it blocks this close
- 2026-11-06T05:02:01Z done
- 2026-11-06T05:03:37Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-2776 [CLEAN S, done, 1 steps] fm bench duel --ablate stops offering gate-pipe: T-2765 made the gate-pipe note a guard deny, which is never ablatable, so the name leave…
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_verify_alias.py
## Lessons
- Turning on sync is the first time every state file meets the commit scanner: run sampo secrets over .foreman first and fix scanner false positives at the rule (placeholder URL passwords, ISO dates), never per file; mark test lines holding sample credentials with the allowlist pragma.
## Plan gaps
- added late: URL passwords that are placeholders don't block a commit (test first)
- failed first: step 1 failing test with a 250-byte name
- failed first: step 3 URL passwords that are placeholders don't block a commit (test first)
## Files touched
- plugin/tests/test_core.py
- plugin/lib/sampo/core.py
- CHANGELOG.md
- plugin/tests/test_secrets.py
- plugin/lib/sampo/secrets.py
