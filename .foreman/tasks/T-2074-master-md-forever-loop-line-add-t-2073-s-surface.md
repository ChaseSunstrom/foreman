---
id: T-2074
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T00:58:12Z
updated: 2026-10-31T01:01:10Z
base: 0b67a8153fe0a108e6e5e397eef9f65fd6227499
base_tree: c6c53d658ae86ab6ef5803934930d8117602c73d
plan0_at: 2026-10-31T00:55:27Z
plan0_scope: []
verified: ok
---
# MASTER.md forever-loop line: add T-2073's surface lag (FACES, lag(), LAG_MIN, the…
## Raw request
> MASTER.md forever-loop line: add T-2073's surface lag (FACES, lag(), LAG_MIN, the brief's Surfaces section) once T-2053's restructure has merged
## Interpretation
MASTER.md's forever-loop line doesn't mention T-2073's surface lag. The names in the request (FACES, LAG_MIN, a brief Surfaces section) are from an earlier design; what shipped is fmloop.lag(p): files recent work would normally have brought along but didn't, learned from the repo's git history (fmmap.drift), printed in fm loop round's Surfaces line (defanged, one line each, 'unknown' without git).
## Assumptions (confidence)
## Acceptance criteria
- [x] MASTER.md's forever-loop line names lag(p), fmmap.drift and where fm loop round prints it — verify with `grep -q 'T-2073' MASTER.md && grep -q 'fmmap.drift' MASTER.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] add the T-2073 clause to MASTER's forever-loop line
## Resume here
## Docs impact
MASTER.md forever-loop line
## Verification evidence
- (step 1) `grep -q 'T-2073' MASTER.md && grep -q 'fmmap.drift' MASTER.md` → exit 0 · (no output) [ran] [tree 8ea837478687] (2026-10-31T00:55:29Z)
- (ac 1) `grep -q 'T-2073' MASTER.md && grep -q 'fmmap.drift' MASTER.md` → exit 0 · (no output) [ran] [tree 8ea837478687] (2026-10-31T00:55:29Z)
- (ac 1) `grep -q 'T-2073' MASTER.md && grep -q 'fmmap.drift' MASTER.md` → exit 0 · (no output) [ran] [tree 8ea837478687] (2026-10-31T00:55:41Z)
- (audit self) `self: the line matches fmloop.lag and its caller (fmloop.py:117-122), not the request's earlier-design names` → no findings [tree 8ea837478687] (2026-10-31T00:55:41Z)
## Log
- 2026-10-30T00:58:12Z created
- 2026-10-31T00:55:25Z set tier=S, type=CLEAN
- 2026-10-31T00:55:26Z planned: it has criteria and steps
- 2026-10-31T00:55:26Z focused
- 2026-10-31T00:55:56Z done
- 2026-10-31T00:55:59Z committed 35040aae (1 file)
- 2026-10-31T01:01:10Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1873 [FEATURE M, done, 3 steps] Fm scene gallery: every built-in scene on one contact sheet, each with a one-line caption — lesson: A playbook has a token ceiling (tes…
- T-2005 [FIX S, done, 2 steps] run.py suggests the test a -k meant, the loop's main-thread round sweeps every lens — lesson: A miss message that names the filter is half …
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- decision 2026-10-16: Recommendation: build the 9 grounded items T-1180..T-1188 with builders; the worktree-fm re-exec idea is skipped (unreviewed lane code would write r…
## Behaviour lock
none: docs only (one MASTER.md line), no code changed
## Lessons
- A doc follow-up written before the code lands can name a design that changed: write it from the shipped code
## Files touched
- MASTER.md
