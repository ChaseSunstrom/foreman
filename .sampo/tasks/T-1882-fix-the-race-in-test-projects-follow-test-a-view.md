---
id: T-1882
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T00:07:35Z
updated: 2026-10-29T00:35:28Z
base: 418adf5d361361b0a52d282e53b91f5433a46421
base_tree: 1a163adeedb16faa26c3702adf328116e5692a12
plan0_at: 2026-10-29T00:25:59Z
plan0_scope: []
verified: strong
---
# Fix the race in test_projects.Follow.test_a_view_line_each_time_the_project_changes (flaky
## Raw request
> Fix the race in test_projects.Follow.test_a_view_line_each_time_the_project_changes (flaky twice in fm check: failed, passed on rerun)
## Interpretation
fmwatch._follow (shared by fm ui, fm projects, fm sessions and fm claude --follow) takes its file-time snapshot after build() and print. A change that lands in that gap (the reader acts on the printed line while the follower is descheduled) is already in the snapshot, so the next line waits for the 30 s refresh. Fix: snapshot before each build, so any change from then on triggers a rebuild.
## Assumptions (confidence)
## Acceptance criteria
- [x] a change that lands while the view is built shows up on the next line, not after the refresh — verify with `python3 plugin/tests/run.py test_projects`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a build that changes its own source right after reading it
2. [x] snapshot before build in _follow; green
## Resume here
<!-- auto -->
- 2026-10-29T00:28:18Z steps 2/2 done
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmwatch.py, plugin/tests/test_projects.py
- touched since last checkpoint: plugin/tests/test_projects.py, plugin/lib/fmwatch.py, CHANGELOG.md
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k change_while_the_view test_projects` → red as expected (exit 1) · Ran 7 tests in 4.6s (5 classes, 16 at a time; slowest: Follow 4s, Projects 2s, VersionSkew 1s) / FAILED (1 classes) [ran] [tree a9a826ac2fc3] (2026-10-29T00:26:06Z)
- (step 2) `python3 plugin/tests/run.py test_projects` → exit 0 · Ran 7 tests in 1.9s (5 classes, 16 at a time; slowest: Projects 1s, Follow 1s, VersionSkew 1s) / OK [ran] [tree 3c827dd15a5f] (2026-10-29T00:26:13Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmwatch.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.3    44.2     150  [0] / SessionEnd                  36.7    39.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree 590f48ba080d] (2026-10-29T00:34:23Z)
- (ac 1) `python3 plugin/tests/run.py test_projects` → exit 0 · Ran 7 tests in 1.0s (5 classes, 16 at a time; slowest: Projects 1s, Follow 1s, VersionSkew 0s) / OK [ran] [tree 590f48ba080d] (2026-10-29T00:34:41Z)
- (audit intent) `self-review, S tier: the snapshot moves before the build in the one shared _follow loop` → a change made while a line is built or printed shows on the next line; the new test fails on the old order [tree 590f48ba080d] (2026-10-29T00:34:41Z)
- (audit adversary) `self-review, S tier: the snapshot moves before the build in the one shared _follow loop` → no new inputs; the same paths are watched, the same JSON printed [tree 590f48ba080d] (2026-10-29T00:34:41Z)
- (audit edge) `self-review, S tier: the snapshot moves before the build in the one shared _follow loop` → paths that change between builds cost one extra rebuild; BrokenPipe and KeyboardInterrupt still end it quietly [tree 590f48ba080d] (2026-10-29T00:34:41Z)
- (audit self) `self-review, S tier: the snapshot moves before the build in the one shared _follow loop` → no findings [tree 590f48ba080d] (2026-10-29T00:34:41Z)
- `python3 plugin/tests/run.py test_projects` → ✗ exit 1 · Ran 7 tests in 4.8s (5 classes, 16 at a time; slowest: Follow 4s, Projects 1s, VersionSkew 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 590f48ba080d] (2026-10-29T00:35:07Z)
- `python3 plugin/tests/run.py test_projects` → exit 0 · Ran 7 tests in 1.1s (5 classes, 16 at a time; slowest: Projects 1s, Follow 1s, VersionSkew 1s) / OK [ran] [tree 590f48ba080d] (2026-10-29T00:35:07Z)
- (audit intent) `self-review, S tier: the snapshot moves before the build in the one shared _follow loop` → a change made while a line is built or printed shows on the next line; the new test fails on the old order [tree 590f48ba080d] (2026-10-29T00:35:12Z)
- (audit adversary) `self-review, S tier: the snapshot moves before the build in the one shared _follow loop` → no new inputs; the same paths are watched, the same JSON printed [tree 590f48ba080d] (2026-10-29T00:35:12Z)
- (audit edge) `self-review, S tier: the snapshot moves before the build in the one shared _follow loop` → paths that change between builds cost one extra rebuild; BrokenPipe and KeyboardInterrupt still end it quietly [tree 590f48ba080d] (2026-10-29T00:35:12Z)
- (audit self) `self-review, S tier: the snapshot moves before the build in the one shared _follow loop` → no findings [tree 590f48ba080d] (2026-10-29T00:35:12Z)
## Log
- 2026-10-29T00:07:35Z created
- 2026-10-29T00:21:59Z set type=FIX, tier=S
- 2026-10-29T00:25:59Z focused
- 2026-10-29T00:35:27Z done
- 2026-10-29T00:35:28Z committed 2db04662 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1789 [FIX S, done, 2 steps] Flaky: test_session.Session.test_review_fixes failed on a tree then passed on the same tre — lesson: When a flake leaves no text, read the …
- research wave2-plan-ab508671842de9f2d: === T-1069 [stale: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts…
- playbook Flaky tests (fm playbooks show fix/flaky-tests)
- decision 2026-10-09: T-0476 quarantine skipped: fm check keeps treating a gate flaky 2+ times as failing
- the similar finished task took 2 steps
- start here (files T-1789 touched): plugin/lib/fmcore.py, plugin/lib/fmsession.py, plugin/tests/test_gate_friction.py, plugin/tests/test_session.py, CHANGELOG.md
## Lessons
- snapshot what you watch before you read it, not after
## Files touched
- plugin/tests/test_projects.py
- plugin/lib/fmwatch.py
- CHANGELOG.md
