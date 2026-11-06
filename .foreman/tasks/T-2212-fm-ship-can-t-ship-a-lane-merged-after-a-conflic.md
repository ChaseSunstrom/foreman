---
id: T-2212
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T20:46:09Z
updated: 2026-10-30T21:30:22Z
base: e231e196f7f1a26556527929f51b9a834e7d3edb
base_tree: 72286c1ccbcc907e151309db6c2c2330c953afd4
plan0_at: 2026-10-30T21:20:17Z
plan0_scope: []
verified: strong
---
# fm ship can't ship a lane merged after a conflict resolution: it cherry-picks the lane's…
## Raw request
> fm ship can't ship a lane merged after a conflict resolution: it cherry-picks the lane's own commits onto origin/main, and the first one conflicts because the resolution lives only in the merge commit; it should squash last-shipped..HEAD onto origin/main (done by hand for T-2203 + T-2123)
## Interpretation
fm ship replays a branch's own first-parent history (T-2054) only when origin main is exactly where the last ship left it. When main moved since then only in files the branch never touches (the site's auto-published Genesis data), it falls back to git cherry, cherry-picks a merged lane's commits one by one, and the first conflicts because the merge's resolution isn't in any of them. Relax the condition: replay first-parent steps when the files main changed since the last ship don't overlap the files the branch changed since it.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ship with no commits named ships a lane merged after a conflict resolution when origin main moved since the last ship only in other files, and still refuses (nothing pushed) when main touched the same files — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
Options: (A) relax T-2054's condition to 'no overlap between main's files since the last ship and the branch's files since it'; (B) squash last..HEAD into one commit onto main (loses per-task commits on main); (C) rebase the branch onto main locally first (rewrites local history). Choice A: smallest change, keeps one commit per step, and an overlap still falls back to today's behaviour.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: lane merged with a conflict resolution, main moved in an unrelated file; fix the replay condition
## Resume here
## Docs impact
MASTER fmrelease line, CHANGELOG.
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_ship 2>&1 | tail -15` → ✗ exit 1 · Ran 19 tests in 13.2s (1 classes, 16 at a time; slowest: Ship 12s) / FAILED (1 classes) [ran] [tree 8039db0e0ef9] (2026-10-30T21:20:42Z)
- (ac 1) `python3 plugin/tests/run.py test_ship 2>&1 | tail -6` → exit 0 · Ran 19 tests in 12.3s (1 classes, 16 at a time; slowest: Ship 12s) / OK [ran] [tree a77d706a9690] (2026-10-30T21:20:59Z)
- (step 1) `python3 plugin/tests/run.py test_ship 2>&1 | tail -6` → exit 0 · Ran 19 tests in 12.3s (1 classes, 16 at a time; slowest: Ship 12s) / OK [ran] [tree a77d706a9690] (2026-10-30T21:20:59Z)
- (step 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 19 tests in 19.6s (1 classes, 16 at a time; slowest: Ship 19s) / OK [ran] [tree a77d706a9690] (2026-10-30T21:21:22Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_release test_ship && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.32s] [ran] [tree a77d706a9690] (2026-10-30T21:21:47Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 19 tests in 12.3s (1 classes, 16 at a time; slowest: Ship 12s) / OK [ran] [tree 144c01092bf6] (2026-10-30T21:29:05Z)
- (step 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 19 tests in 12.3s (1 classes, 16 at a time; slowest: Ship 12s) / OK [ran] [tree 144c01092bf6] (2026-10-30T21:29:17Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 19 tests in 12.3s (1 classes, 16 at a time; slowest: Ship 12s) / OK [ran] [tree f0d5aac4d6e8] (2026-10-30T21:29:53Z)
- (audit intent) `lead review of the builder's branch (diff read in full): the replay condition now compares the file sets main and the branch changed since the last ship; an overlap keeps the old cherry fallback; a non-descendant main makes the diff large and falls back; idempotent after a push` → a lane merged after a conflict ships with no commits named when main moved only in other files (red before the fix, green now) [tree f0d5aac4d6e8] (2026-10-30T21:29:53Z)
- (audit edge) `lead review of the builder's branch (diff read in full): the replay condition now compares the file sets main and the branch changed since the last ship; an overlap keeps the old cherry fallback; a non-descendant main makes the diff large and falls back; idempotent after a push` → main touching the branch's files still refuses with nothing pushed; a rebased or force-pushed main falls back to git cherry [tree f0d5aac4d6e8] (2026-10-30T21:29:53Z)
## Log
- 2026-10-30T20:46:09Z created
- 2026-10-30T21:19:54Z planned: it has criteria and steps
- 2026-10-30T21:19:55Z set approved=True
- 2026-10-30T21:20:03Z criterion 1 verify: `python3 plugin/tests/run.py test_release` → `python3 plugin/tests/run.py test_ship`
- 2026-10-30T21:20:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2212.builder.md
- 2026-10-30T21:20:16Z focused
- 2026-10-30T21:28:46Z merged worktree-agent-a3d150decc0adf378 (2 file(s))
- 2026-10-30T21:28:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3d150decc0adf378
- 2026-10-30T21:28:52Z focused
- 2026-10-30T21:29:32Z scope: fmrelease replay condition + test_ship; builder lane reviewed by me (diff read: file-set overlap check, overlap keeps the old fallback)
- 2026-10-30T21:30:20Z done
- 2026-10-30T21:30:22Z committed e930a846 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2054 [FIX S, done, 2 steps] fm ship replays merged builder lanes: picks the branch's first-parent chain after the last ship (merges with -m 1) when main still matches …
- research T-2090-review: Verdict** — changes needed (two MEDIUM, both fixable in a few lines). I couldn't run the tests, since I only had read tools, so everything below …
- decision 2026-10-30: [outward] Turn on fm genesis live for the Foreman repo: tower changes push site/genesis data to origin main automatically
- similar finished tasks took 2–2 steps
## Why not caught
the T-2054 test kept origin main still after the last ship; the live repo's main moves on its own (site auto-publish)
## Lessons
- Replay a merged branch by its first-parent steps whenever main's own changes since the last ship don't touch the branch's files; exact equality was stricter than safety needs
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
- MASTER.md
