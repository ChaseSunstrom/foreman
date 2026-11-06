---
id: T-1188
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T12:38:39Z
updated: 2026-10-16T13:55:32Z
base: b14666cd8795b68b486c985ec3f773279ca24278
base_tree: 1dd8c405acfb3f996bdde3e3d7b60040bac543bd
plan0_at: 2026-10-16T13:08:04Z
plan0_scope: []
verified: strong
---
# `fm release VERSION` chains release-check, canary, the release.py steps and `fm round clos
## Raw request
> FEATURE: `fm release VERSION` chains release-check, canary, the release.py steps and `fm round close` as named steps, writes a checkpoint after each, and `--resume` continues from the first unfinished step; `--dry-run` only prints the plan.
> DONE-WHEN: plugin/tests/test_release.py runs `fm release 9.9.9 --dry-run` in a temp repo and lists every step, and a run stopped after step 2 continues from step 3 with `--resume`.
## Interpretation
Releasing is an 8-step ritual done by hand. fm release VERSION [--ui VERSION] [--push] [--dry-run] [--resume] runs it as named steps with a checkpoint after each: clean tree; full fm check; bump plugin.json, both marketplace.json entries, and the foreman-ui version when mods/foreman-ui changed since the last release commit; CHANGELOG 'Unreleased' heading; commit 'Foreman VERSION' with the Foreman-Task trailer; fm release-check; with --push, merge into origin's main from a temporary worktree (--no-ff) and push, behind the active task's publish grant (spent by the push). --resume continues from the first unfinished step; --dry-run prints the plan.
## Assumptions (confidence)
## Acceptance criteria
- [x] in a temp repo shaped like Foreman's, fm release 9.9.9 --dry-run lists every step; a run stopped after step 2 continues from step 3 with --resume; --push without the publish grant refuses before any change — verify with `python3 plugin/tests/run.py test_release`
## Non-goals
## Approach (options → choice → why)
Options: (a) a new fmrelease module reusing release.py's helpers (import it from the repo root when present) and fm's own check/release-check, state in meta release={version, done:[steps]}; (b) extend release.py only (not on PATH as fm, no checkpoints in fm state); (c) a workflow (needs user opt-in). Choice: (a); refuse outside Foreman's own repo (no release.py).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_release.py) on a temp repo with --no-check style stubs for the gates
2. [x] fmrelease: steps, checkpoints, resume, dry-run, publish-grant push
3. [x] Review fixes: push merges the recorded release commit; stubbed gates push only to a local remote; same-version rerun resumes; failed check then resume; dry-run --abandon changes nothing; corrupt release.json abandons; remote can't be an option; commit only its files; round and grant spend idempotent; release.py passes other flags through
## Resume here
<!-- auto -->
- 2026-10-16T13:45:11Z steps 2/2 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: .claude/worktrees/agent-ab0b16b059fab10d2/plugin/tests/test_release_py.py, .claude/worktrees/agent-ab0b16b059fab10d2/release.py, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/lib/fmrelease.py, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/tests/test_release.py, .claude/worktrees/agent-ab0b16b059fab10d2/CHANGELOG.md, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/lib/fmcli.py, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/lib/fmcore.py, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/lib/fmhooks.py, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/lib/fmreplay.py, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/lib/fmtidy.py, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/tests/bench_hooks.py, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/tests/fixtures/hook_payloads.json, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/tests/test_guard_cases.py, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/tests/test_guard_mine.py, .claude/worktrees/agent-ab0b16b059fab10d2/plugin/tests/test_until_conditions.py
## Docs impact
plugin/skills/playbooks/references/release/release-and-changelog.md, README.md, MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_release` → ✗ exit 1 · Ran 8 tests in 41.3s (3 classes, 16 at a time; slowest: BoardVerbs 39s, Release 6s, ClaimsReview 4s) / FAILED (1 classes) [ran] [tree 5001da090da1] (2026-10-16T13:10:10Z)
- (step 1) `python3 plugin/tests/run.py -k Release` → exit 0 · Ran 6 tests in 13.4s (1 classes, 16 at a time; slowest: Release 12s) / OK [ran] [tree abd16163f3da] (2026-10-16T13:13:29Z)
- (step 2) `python3 plugin/tests/run.py -k Release` → exit 0 · Ran 6 tests in 11.6s (1 classes, 16 at a time; slowest: Release 11s) / OK [ran] [tree abd16163f3da] (2026-10-16T13:13:42Z)
- (step 3) `python3 plugin/tests/run.py test_release test_release_py` → exit 0 · Ran 27 tests in 38.6s (5 classes, 16 at a time; slowest: Release 38s, BoardVerbs 37s, Release 6s) / OK [ran] [tree 980ae68ee316] (2026-10-16T13:52:17Z)
- (ac 1) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 27 tests in 30.1s (5 classes, 16 at a time; slowest: Release 29s, BoardVerbs 28s, Release 6s) / OK [ran] [tree 980ae68ee316] (2026-10-16T13:53:10Z)
- `python3 plugin/tests/run.py test_release test_release_py test_board_verbs` → exit 0 · Ran 32 tests in 21.0s (5 classes, 16 at a time; slowest: BoardVerbs 21s, Release 15s, Release 3s) / OK [ran] [tree 980ae68ee316] (2026-10-16T13:53:10Z)
- (audit intent) `fm-reviewer five-lens pass over fmrelease.py, release.py and the tests; 2 MEDIUM and 9 LOW findings, all fixed test-first in step 3 except the shared spend helper with fmpr (left: two 15-line functions, captured as maintainer note)` → dry-run lists all 9 steps; a stop at any step resumes there (tested at check, bump and release-check); --push without the grant refuses before any change [tree 980ae68ee316] (2026-10-16T13:53:10Z)
- (audit adversary) `fm-reviewer five-lens pass over fmrelease.py, release.py and the tests; 2 MEDIUM and 9 LOW findings, all fixed test-first in step 3 except the shared spend helper with fmpr (left: two 15-line functions, captured as maintainer note)` → push merges the recorded release sha, not HEAD; the FOREMAN_RELEASE_FM stub can only push to a local path remote; a --remote starting with - is refused; the grant is rechecked under the lock before it is spent [tree 980ae68ee316] (2026-10-16T13:53:10Z)
- (audit edge) `fm-reviewer five-lens pass over fmrelease.py, release.py and the tests; 2 MEDIUM and 9 LOW findings, all fixed test-first in step 3 except the shared spend helper with fmpr (left: two 15-line functions, captured as maintainer note)` → same-version rerun after the bump auto-resumes; --abandon --dry-run changes nothing; a corrupt release.json is a one-line error and --abandon clears it; staged files between runs stay out of the release commit; round close skips when HEAD is already tagged [tree 980ae68ee316] (2026-10-16T13:53:10Z)
- (audit operator) `fm-reviewer five-lens pass over fmrelease.py, release.py and the tests; 2 MEDIUM and 9 LOW findings, all fixed test-first in step 3 except the shared spend helper with fmpr (left: two 15-line functions, captured as maintainer note)` → each step prints step N/9 and a stop names the --resume command; release.py forwards --resume, --ui, --dry-run [tree 980ae68ee316] (2026-10-16T13:53:10Z)
- (audit maintainer) `fm-reviewer five-lens pass over fmrelease.py, release.py and the tests; 2 MEDIUM and 9 LOW findings, all fixed test-first in step 3 except the shared spend helper with fmpr (left: two 15-line functions, captured as maintainer note)` → version and changelog writes are atomic like the marketplace one; one module, steps as a table [tree 980ae68ee316] (2026-10-16T13:53:10Z)
- `python3 plugin/tests/run.py test_release test_release_py test_board_verbs` → exit 0 · Ran 32 tests in 15.3s (5 classes, 16 at a time; slowest: BoardVerbs 15s, Release 11s, Release 2s) / OK [ran] [tree 980ae68ee316] (2026-10-16T13:54:35Z)
- (audit intent) `fm-reviewer five-lens pass over fmrelease.py, release.py and the tests; 2 MEDIUM and 9 LOW findings, all fixed test-first in step 3 except a shared grant-spend helper with fmpr (two short functions, left as is)` → dry-run lists all 9 steps; a stop at any step resumes there (tested at check, bump and release-check); --push without the grant refuses before any change [tree 980ae68ee316] (2026-10-16T13:54:35Z)
- (audit adversary) `fm-reviewer five-lens pass over fmrelease.py, release.py and the tests; 2 MEDIUM and 9 LOW findings, all fixed test-first in step 3 except a shared grant-spend helper with fmpr (two short functions, left as is)` → push merges the recorded release sha, not HEAD; the FOREMAN_RELEASE_FM stub can only push to a local path remote; a --remote starting with - is refused; the grant is rechecked under the lock before it is spent [tree 980ae68ee316] (2026-10-16T13:54:35Z)
- (audit edge) `fm-reviewer five-lens pass over fmrelease.py, release.py and the tests; 2 MEDIUM and 9 LOW findings, all fixed test-first in step 3 except a shared grant-spend helper with fmpr (two short functions, left as is)` → same-version rerun after the bump auto-resumes; --abandon --dry-run changes nothing; a corrupt release.json is a one-line error and --abandon clears it; staged files between runs stay out of the release commit; round close skips when HEAD is already tagged [tree 980ae68ee316] (2026-10-16T13:54:35Z)
- (audit operator) `fm-reviewer five-lens pass over fmrelease.py, release.py and the tests; 2 MEDIUM and 9 LOW findings, all fixed test-first in step 3 except a shared grant-spend helper with fmpr (two short functions, left as is)` → each step prints step N/9 and a stop names the --resume command; release.py forwards --resume, --ui, --dry-run [tree 980ae68ee316] (2026-10-16T13:54:35Z)
- (audit maintainer) `fm-reviewer five-lens pass over fmrelease.py, release.py and the tests; 2 MEDIUM and 9 LOW findings, all fixed test-first in step 3 except a shared grant-spend helper with fmpr (two short functions, left as is)` → version and changelog writes are atomic like the marketplace one; one module, steps as a table [tree 980ae68ee316] (2026-10-16T13:54:35Z)
## Log
- 2026-10-16T12:38:39Z created
- 2026-10-16T13:07:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1188.builder.md
- 2026-10-16T13:08:03Z focused
- 2026-10-16T13:44:09Z merged worktree-agent-ab0b16b059fab10d2 (8 file(s))
- 2026-10-16T13:44:40Z merged worktree-agent-ab0b16b059fab10d2 (0 file(s))
- 2026-10-16T13:44:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab0b16b059fab10d2
- 2026-10-16T13:44:55Z focused
- 2026-10-16T13:45:12Z paused: focus moved to T-1185
- 2026-10-16T13:48:46Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T13:48:46Z focused
- 2026-10-16T13:52:18Z scope: CHANGELOG line; release.py passthrough
- 2026-10-16T13:55:30Z done
- 2026-10-16T13:55:32Z committed b8fa1cb1 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0960 [FEATURE M, done, 3 steps] New verbs: fm oops, fm round close, fm show, fm release-check, fm sensitive suggest, fm outcomes --readme — lesson: A restore verb's me…
- playbook Release and changelog (skills/playbooks/references/release/release-and-changelog.md)
- T-0678 [FEATURE M, done, 3 steps] Milestone: Features — Releases and delivery — lesson: A release done by hand four times in a day is a script; the script is the checkli…
- decision 2026-10-15: Release as 1.2.28 via release.py --push, not a raw push
- similar finished tasks took 3–3 steps
- start here (files T-0960 touched): plugin/tests/test_board_verbs.py, plugin/lib/fmcli.py, plugin/lib/fmoutcomes.py, plugin/lib/fmdemo.py, MASTER.md, README.md
## Lessons
- A deferred step that acts on HEAD must act on the commit the gates saw: record the sha at the step that made it
## Plan gaps
- added late: Review fixes: push merges the recorded release commit; stubbed gates push only to a local remote; same-version rerun re…
- failed first: step 1 Failing tests (test_release.py) on a temp repo with --no-check style stubs for the gates
## Files touched
- plugin/tests/test_release.py
- plugin/lib/fmrelease.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/tests/test_release_py.py
- release.py
- CHANGELOG.md
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmreplay.py
- plugin/lib/fmtidy.py
- plugin/tests/bench_hooks.py
- plugin/tests/fixtures/hook_payloads.json
- plugin/tests/test_guard_cases.py
- plugin/tests/test_guard_mine.py
- plugin/tests/test_until_conditions.py
- plugin/tests/test_verify_check.py
- README.md
- plugin/skills/playbooks/references/release/release-and-changelog.md
