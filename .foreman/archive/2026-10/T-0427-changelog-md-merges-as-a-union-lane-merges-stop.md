---
id: T-0427
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T14:02:15Z
updated: 2026-10-09T14:02:27Z
base: c8fa2518dd8d1eab27d2abb014733b0dca9d870a
base_tree: 3d9d97b19c63d2b888c6750d55b60a559e8c2059
verified: strong
---
# CHANGELOG.md merges as a union (lane merges stop conflicting on it)
## Raw request
> CHANGELOG.md merges as a union (lane merges stop conflicting on it)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane branch and the main line that each add an Unreleased line merge without a conflict — verify with `git -C ~/.claude/foreman check-attr merge CHANGELOG.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] add .gitattributes: CHANGELOG.md merge=union
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git merge-tree --write-tree --name-only HEAD worktree-agent-a0864fcff2994e067` → exit 0 · 3df99b2802ada7ea6f62464cf403a4e5d636ff09 [ran] [tree 0fd86a7b539a] (2026-10-09T14:02:26Z)
- (ac 1) `git -C ~/.claude/foreman check-attr merge CHANGELOG.md` → exit 0 · CHANGELOG.md: merge: union [ran] [tree 0fd86a7b539a] (2026-10-09T14:02:26Z)
- (audit edge) `self: one attribute line; union keeps both sides' lines, which is what a changelog of independent entries wants (order may interleave; a reviewer reads it at release)` → an edit to the same existing line on both sides now keeps both versions instead of conflicting: acceptable for CHANGELOG, which only grows [tree 0fd86a7b539a] (2026-10-09T14:02:26Z)
- (audit self) `self: one attribute line; union keeps both sides' lines, which is what a changelog of independent entries wants (order may interleave; a reviewer reads it at release)` → no findings [tree 0fd86a7b539a] (2026-10-09T14:02:26Z)
## Log
- 2026-10-09T14:02:15Z created
- 2026-10-09T14:02:15Z focused
- 2026-10-09T14:02:26Z done
- 2026-10-09T14:02:27Z committed 692d7d6 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0167 [FEATURE L, done, 5 steps] fm run --parallel N: independent queued tasks at once, each in its own lane, merged back only when gated and clean — lesson: A loop tha…
- T-0186 [FEATURE M, done, 3 steps] fm tidy sweeps stale lanes: a closed task's lane and merged foreman/T-* branches no lane holds — lesson: Cleanup belongs in the command…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Regression test
none as a unit test (a git attribute); before it, the same git merge-tree run reported CONFLICT (content) in CHANGELOG.md for T-0413's and T-0414's branches (both seen this session); after it, exit 0
## Lessons
- When the same conflict recurs on every merge, change the merge rule, not the merges.
## Files touched
- .gitattributes
