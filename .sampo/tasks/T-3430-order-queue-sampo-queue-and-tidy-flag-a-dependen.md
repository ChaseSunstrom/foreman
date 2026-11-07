---
id: T-3430
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/core.py, plugin/lib/sampo/tidy.py, plugin/lib/sampo/cli.py, plugin/tests/test_core.py, plugin/tests/test_visibility.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: discovered
created: 2026-11-06T11:17:37Z
updated: 2026-11-06T16:29:47Z
base: b61801502ce5693a2fe1122f4926d2dcf7a0feae
base_tree: 94e4bcdb7a597b91e2201fd7391f50556cd176e2
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T11:18:50Z
plan0_scope: [plugin/lib/sampo/core.py, plugin/lib/sampo/tidy.py, plugin/lib/sampo/cli.py, plugin/tests/test_core.py]
builder_returned: 2026-11-06T11:37:52Z
lane_stop: merged 2026-11-06T12:56:33Z
verified: strong
unproven: [meaning]
lane_verified: a9301d00a4461b49ce5d05093c4df5327311e361
---
# order_queue (sampo queue) and tidy flag a dependency on an archived (closed) task as…
## Raw request
> FIX: order_queue (sampo queue) and tidy flag a dependency on an archived (closed) task as dangling or unknown because they load briefs without the archive; treat archived ids as satisfied dependencies (T-3420 review)
## Interpretation
Archived deps are satisfied; pass archived ids (file names only) to order_queue.
## Assumptions (confidence)
## Acceptance criteria
- [x] archived dep queued unblocked, unknown still flagged — verify with `python3 plugin/tests/run.py test_core.Queue`
## Non-goals
## Approach (options → choice → why)
core.archived_ids(p) lists archive file names via _BRIEF_FILE; order_queue(briefs, archived=()) skips dangling for them; tidy and cmd_queue pass it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] archived ids in order_queue, tidy, queue view
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_core.Queue` → exit 0 · Ran 8 tests in 1.5s (1 jobs, 16 at a time; slowest: Queue 0s) / OK [ran] [tree e85650ac4590] [world 2f1906870a] (2026-11-06T11:19:09Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_tidy test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [14.58s] [ran] [tree e85650ac4590] [world 2f1906870a] (2026-11-06T11:19:50Z)
- (step 1) `python3 plugin/tests/run.py test_visibility.Progress test_core.Queue` → exit 0 · Ran 14 tests in 11.2s (2 jobs, 16 at a time; slowest: Progress 3s, Queue 0s) / OK [ran] [tree 88e6f394c4b5] [world 2f1906870a] (2026-11-06T11:36:41Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_tidy test_verify_alias test_verify_unittest_form test_visibility && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [15.43s] [ran] [tree 88e6f394c4b5] [world 2f1906870a] (2026-11-06T11:37:45Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 60cc54bf8755] (2026-11-06T12:56:38Z)
- `python3 plugin/tests/run.py test_core test_visibility` → ✗ exit 1 · Ran 164 tests in 39.2s (34 jobs, 16 at a time; slowest: ConfidenceRoutes 4s, Migrate 3s, Progress 2s) / FAILED (2 classes: test_core.Queue, test_visibility.Progress) (start tree + this task's tests) [ran] [tree 60cc54bf8755] [world 2f1906870a] (2026-11-06T12:58:02Z)
- `python3 plugin/tests/run.py test_core test_visibility` → exit 0 · Ran 164 tests in 39.2s (38 jobs, 16 at a time; slowest: ConfidenceRoutes 4s, Progress 3s, Migrate 2s) / OK [ran] [tree 60cc54bf8755] [world 2f1906870a] (2026-11-06T12:58:02Z)
- (ac 1) `python3 plugin/tests/run.py test_core.Queue` → exit 0 · Ran 8 tests in 27.4s (1 jobs, 16 at a time; slowest: Queue 0s) / OK [ran] [tree 60cc54bf8755] [world 2f1906870a] (2026-11-06T12:58:34Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 60cc54bf8755] (2026-11-06T12:58:34Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 60cc54bf8755] (2026-11-06T12:58:34Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 60cc54bf8755] (2026-11-06T12:58:34Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 60cc54bf8755] (2026-11-06T12:58:34Z)
## Log
- 2026-11-06T11:17:37Z created
- 2026-11-06T11:18:33Z set tier=S
- 2026-11-06T11:18:40Z set scope=['plugin/lib/sampo/core.py', 'plugin/lib/sampo/tidy.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_core.py']
- 2026-11-06T11:18:48Z planned: it has criteria and steps
- 2026-11-06T11:18:49Z focused
- 2026-11-06T11:18:50Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T11:36:23Z set scope=['plugin/lib/sampo/core.py', 'plugin/lib/sampo/tidy.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_core.py', 'plugin/tests/test_visibility.py']
- 2026-11-06T12:56:33Z merged worktree-agent-ad0433a3815236ca9 (5 file(s))
- 2026-11-06T12:56:34Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad0433a3815236ca9
- 2026-11-06T12:56:34Z focused
- 2026-11-06T12:56:38Z set scope=['plugin/lib/sampo/core.py', 'plugin/lib/sampo/tidy.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_core.py', 'plugin/tests/test_visibility.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T12:56:38Z scope: widened at merge to the reviewed lane's own diff (a9301d00a), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T13:00:36Z done
- 2026-11-06T13:00:55Z committed 4a071f512 (1 file)
- 2026-11-06T16:29:47Z verified: the full suite is green on 1078ed22d, which contains a9301d00a
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- T-2334 [FIX M, done, 2 steps] A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit — lesson: A timeout is not …
- T-3372 [FIX M, done, 1 steps] Sampo task ac ID list silently adds a criterion named 'list' (T-3266 builder); unknown… — lesson: none: a reviewed builder lane; its lesson…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_affected_hubs.py, plugin/tests/test_affected_symbols.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_mint.py, p…
## Preflight
Changed in scope since this was planned (2026-11-06): plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/tidy.py, plugin/tests/test_core.py, plugin/tests/test_visibility.py; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/test_core.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/tidy.py
- plugin/lib/sampo/cli.py
- plugin/tests/test_visibility.py
- CHANGELOG.md
