---
id: T-3118
type: PERFORMANCE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T03:13:12Z
updated: 2026-11-05T03:22:30Z
---
# Merge speed: the self-change gate's paired timing bench (selfgate._benched: any plugin/…
## Raw request
> merge speed: the self-change gate's paired timing bench (selfgate._benched: any plugin/ file but tests and .md) runs for branches no hook can load (plugin/web/live/*.js, CLI-only modules), and it is what makes every merge wait for a quiet machine; bench only files on the hook path: the import closure of plugin/hooks' entry points plus the files hooks read and CHANGELOG.md; everything else merges without the bench or the quiet wait
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:13:12Z created
- 2026-11-05T03:22:30Z dropped: premise false, measured: hooks can lazily reach 131 of 132 sampo modules (scratchpad hookreach.py), so a hook-path filter skips almost nothing; and the bench already times CPU (T-2363), so load barely skews it. The merge wait was my merge script's own quiet window (LOAD 9 to 12), set after three holds; folded into T-3091 (are the holds real?)
## Follow-ups captured
