---
id: T-1749
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmsync.py, plugin/lib/fmhome.py, plugin/tests/test_sync.py, plugin/tests/test_portability.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T04:51:07Z
updated: 2026-10-23T05:12:52Z
base: b21f5582b0ef83a033b481e093a89b07db25972e
base_tree: 79f2bffd493dd890388696632ed1b31501594204
plan0_at: 2026-10-23T05:09:37Z
plan0_scope: [plugin/lib/fmsync.py, plugin/lib/fmhome.py, plugin/tests/test_sync.py, plugin/tests/test_portability.py, CHANGELOG.md]
verified: strong
---
# Fm sync import has the gaps fm home import closed: it keeps lease marks (lane, builder, co
## Raw request
> fm sync import has the gaps fm home import closed: it keeps lease marks (lane, builder, cost_cap), never sets confirm on open pulled briefs, and keeps check_run/evidence events; share fmhome's brief and ledger cleaning
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm sync import drops lease marks (lane, lane_branch, builder, builder_proc, cost_cap, cap_hit), sets confirm on open pulled briefs and drops check_run/evidence/ledger_damage_ack events, sharing fm home's cleaning — verify with `python3 plugin/tests/run.py test_sync`
## Non-goals
## Approach (options → choice → why)
Move fmhome._brief's lease/focus/confirm logic and _jsonl's event filter into one place both use (fmsync, since fmhome already imports it); keep fm sync's existing demotion of active/verifying. Test-first in test_sync.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests for each gap
2. [x] share fmhome's brief and ledger cleaning with fmsync
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_sync` → red as expected (exit 1) · Ran 19 tests in 12.5s (2 classes, 16 at a time; slowest: Sync 12s, BoardSurfaces 0s) / FAILED (1 classes) [ran] [tree 7ea3c05e8781] (2026-10-23T05:10:29Z)
- (step 2) `python3 plugin/tests/run.py test_sync test_portability test_followups test_board_surfaces` → exit 0 · Ran 49 tests in 12.6s (7 classes, 16 at a time; slowest: Sync 12s, Home 9s, BoardSurfaces 2s) / OK [ran] [tree 6e0469b55160] (2026-10-23T05:11:35Z)
- (step 1) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 19 tests in 12.7s (2 classes, 16 at a time; slowest: Sync 12s, BoardSurfaces 0s) / OK [ran] [tree 6e0469b55160] (2026-10-23T05:11:48Z)
- (ac 1) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 19 tests in 12.7s (2 classes, 16 at a time; slowest: Sync 12s, BoardSurfaces 0s) / OK [ran] [tree 6e0469b55160] (2026-10-23T05:12:02Z)
- (ac 1) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 19 tests in 12.6s (2 classes, 16 at a time; slowest: Sync 12s, BoardSurfaces 0s) / OK [ran] [tree da6b41bf9284] (2026-10-23T05:12:36Z)
- (audit adversary) `self: one settle(b, new) in fmsync used by fm sync import and fm home import (fmhome's copy removed): active/verifying become planned unless this machine has it active, lease marks dropped, a new open brief gets confirm; on an update the local copy's grants, lease marks and confirm are carried over so this machine's own work isn't disturbed; the ledger doesn't travel through sync, so the forged check_run concern doesn't apply there` → a cloned repo's .foreman/tasks can no longer plant an open task the drive works as if the user asked: it waits for fm ask ID confirm; another machine's lane or builder marks can't make a task look leased here [tree da6b41bf9284] (2026-10-23T05:12:36Z)
- (audit edge) `self: one settle(b, new) in fmsync used by fm sync import and fm home import (fmhome's copy removed): active/verifying become planned unless this machine has it active, lease marks dropped, a new open brief gets confirm; on an update the local copy's grants, lease marks and confirm are carried over so this machine's own work isn't disturbed; the ledger doesn't travel through sync, so the forged check_run concern doesn't apply there` → the user's own tasks pulled onto a new machine also wait for one confirm each (deliberate friction); a task already here keeps its own confirm state [tree da6b41bf9284] (2026-10-23T05:12:36Z)
- (audit self) `self: one settle(b, new) in fmsync used by fm sync import and fm home import (fmhome's copy removed): active/verifying become planned unless this machine has it active, lease marks dropped, a new open brief gets confirm; on an update the local copy's grants, lease marks and confirm are carried over so this machine's own work isn't disturbed; the ledger doesn't travel through sync, so the forged check_run concern doesn't apply there` → no findings [tree da6b41bf9284] (2026-10-23T05:12:36Z)
## Log
- 2026-10-23T04:51:07Z created
- 2026-10-23T05:06:30Z set scope=['plugin/lib/fmsync.py', 'plugin/lib/fmhome.py', 'plugin/tests/test_sync.py', 'plugin/tests/test_portability.py', 'CHANGELOG.md']
- 2026-10-23T05:09:37Z focused
- 2026-10-23T05:12:50Z done
- 2026-10-23T05:12:52Z committed 536968c1 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1752 [FIX M, planned, 3 steps] Workflow output fixes: check --affected --evidence records evidence, lease take lists only its own, a confirm gap says …
- T-1731 [FIX M, done, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski… — lesson: Skip a t…
- T-1665 [FEATURE M, done, 3 steps] fm home export and import: a tarball of Foreman's state without secrets, checked on import into an empty home — lesson: Importing state…
- decision 2026-09-26: fm sync keeps the automatic import at session start and before fm commands: imported content can't grant, mark runs, count as audits or take focus, …
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_sync.py
## Why not caught
fm sync's adversary audits covered grants, marks and audits, not the confirm gate or lease marks; fm home's review found them first
## Lessons
- Anything a repo can carry into Foreman's state is untrusted input: it waits for the user's yes
## Files touched
- plugin/tests/test_sync.py
- plugin/lib/fmsync.py
- plugin/lib/fmhome.py
- CHANGELOG.md
