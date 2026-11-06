---
id: T-1184
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T12:38:39Z
updated: 2026-10-16T12:59:53Z
base: a42fb5527315733bb300c3d1f69e404db2db08ae
base_tree: 0f4314c87c5ca5c86570f4eeb9140a0c91e37ca4
plan0_at: 2026-10-16T12:39:33Z
plan0_scope: []
verified: strong
---
# `fm doctor --fix` applies only the findings that already have a safe repair (regenerate st
## Raw request
> FEATURE: `fm doctor --fix` applies only the findings that already have a safe repair (regenerate status views, the --repair and --restore-state moves) and lists every finding it left for a person.
> DONE-WHEN: a new test in plugin/tests/test_doctor.py seeds a stale status view and a truncated brief, runs `fm doctor --fix`, and sees the view regenerated and the second finding listed as unfixed.
## Interpretation
fm doctor lists problems; some have a safe, mechanical repair already (regenerate STATE/INBOX views, --repair for crash-truncated git objects, --restore-state for fallback state). fm doctor --fix applies exactly those and lists every remaining finding as needing a person (with the command or reason), so a weak agent or the drive can repair without judgment calls.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm doctor --fix regenerates a stale STATE view and reports it fixed, lists a finding with no repair as left for a person, and changes nothing a plain fm doctor run wouldn't suggest — verify with `python3 plugin/tests/run.py test_doctor_fix`
## Non-goals
## Approach (options → choice → why)
Options: (a) a FIXERS table in fmdoctor mapping a Result name (briefs/STATE drift, git objects, state dir fallback, …) to an existing repair function; --fix runs the doctor, applies fixers for FAIL/WARN results that have one, re-runs those checks and prints fixed/left; (b) a separate fm repair verb (duplicates doctor's knowledge); (c) auto-fix inside every doctor run (surprising writes). Choice: (a); nothing irreversible: only repairs the existing flags already perform.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_doctor_fix.py)
2. [x] FIXERS table and --fix in fmdoctor
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor_fix` → ✗ exit 1 · Ran 3 tests in 2.4s (1 classes, 16 at a time; slowest: Fix 1s) / FAILED (1 classes) [ran] [tree bb8c9b21f566] (2026-10-16T12:40:07Z)
- (step 2) `python3 plugin/tests/run.py test_doctor_fix` → exit 0 · Ran 3 tests in 2.0s (1 classes, 16 at a time; slowest: Fix 2s) / OK [ran] [tree 44726bc10949] (2026-10-16T12:40:25Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor_fix test_doctor` → exit 0 · Ran 50 tests in 22.4s (18 classes, 16 at a time; slowest: Command 22s, ViewsRepair 16s, Fix 1s) / OK [ran] [tree 29febc121320] (2026-10-16T12:52:35Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor_fix` → exit 0 · Ran 3 tests in 5.8s (1 classes, 16 at a time; slowest: Fix 4s) / OK [ran] [tree 0c815e48ca75] (2026-10-16T12:52:57Z)
- (audit intent) `self: reviewed the merged diff: FIXERS maps three result names to repairs the existing flags already do (regen_views, the git-object quarantine, restore_default_state), each rechecked; anything without a fixer, a fixer error or a failed recheck is listed for a person; PASS results untouched` → a weak agent or the drive can repair without a judgment call [tree 0c815e48ca75] (2026-10-16T12:52:57Z)
- (audit adversary) `self: reviewed the merged diff: FIXERS maps three result names to repairs the existing flags already do (regen_views, the git-object quarantine, restore_default_state), each rechecked; anything without a fixer, a fixer error or a failed recheck is listed for a person; PASS results untouched` → only repairs that already existed as flags; nothing deletes or rewrites briefs [tree 0c815e48ca75] (2026-10-16T12:52:57Z)
- (audit edge) `self: reviewed the merged diff: FIXERS maps three result names to repairs the existing flags already do (regen_views, the git-object quarantine, restore_default_state), each rechecked; anything without a fixer, a fixer error or a failed recheck is listed for a person; PASS results untouched` → FOREMAN_STATE set: state dir fix is a no-op and listed as left; a second run finds nothing [tree 0c815e48ca75] (2026-10-16T12:52:57Z)
- (audit operator) `self: reviewed the merged diff: FIXERS maps three result names to repairs the existing flags already do (regen_views, the git-object quarantine, restore_default_state), each rechecked; anything without a fixer, a fixer error or a failed recheck is listed for a person; PASS results untouched` → Fixed / Left for a person lists; exit 1 when anything is left [tree 0c815e48ca75] (2026-10-16T12:52:57Z)
- (audit maintainer) `self: reviewed the merged diff: FIXERS maps three result names to repairs the existing flags already do (regen_views, the git-object quarantine, restore_default_state), each rechecked; anything without a fixer, a fixer error or a failed recheck is listed for a person; PASS results untouched` → one table to extend [tree 0c815e48ca75] (2026-10-16T12:52:57Z)
## Log
- 2026-10-16T12:38:39Z created
- 2026-10-16T12:39:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1184.builder.md
- 2026-10-16T12:39:33Z focused
- 2026-10-16T12:52:01Z merged worktree-agent-ae9be4d67bd022c45 (3 file(s))
- 2026-10-16T12:52:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae9be4d67bd022c45
- 2026-10-16T12:52:07Z focused
- 2026-10-16T12:52:47Z scope: the views hint in fmdoctor now points at --fix (builder's note); CHANGELOG line
- 2026-10-16T12:59:52Z done
- 2026-10-16T12:59:53Z committed 76be1cb9 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-pass-1: Source: research/brainstorm-20261004-013651 (4 lenses × 3 rounds, past the four earlier idea lists; 132 new titles). Pack: the user's words, …
- T-0268 [FEATURE M, done, 3 steps] Repo integrity in fm doctor: empty git objects and truncated state, fm doctor --repair — lesson: A health check that is also a gate mus…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- the similar finished task took 3 steps
## Lessons
- a doctor's repair should be a table of finding -> existing repair + recheck, never a new repair path
## Plan gaps
- failed first: step 1 Failing tests (test_doctor_fix.py)
## Files touched
- plugin/tests/test_doctor_fix.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmcli.py
- CHANGELOG.md
