---
id: T-3132
type: SECURITY
tier: S
status: planned
priority: normal
scope: [plugin/tests/bench_hooks.py, plugin/tests/test_bench_hooks.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T03:51:02Z
updated: 2026-11-06T03:52:34Z
group: hook bench gate
---
# The hook bench never imports the tree's own code into its timing process: the script budget comes from a child, so a branch can't patch the clock that judges it
## Raw request
> self-change gate: bench_hooks imports the branch's fmguard in its own process, so branch code could patch resource.getrusage or statistics.median and fake its own timings (pre-existing, review of T-3131); bench in a subprocess that loads only the base's harness
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] bench_hooks.py imports nothing from the benched tree's plugin/lib in its own process; fmguard._script_budget() is read by a child python (-I) and parsed, with the old default when the child fails; a branch fmguard that patches resource.getrusage at import changes no timing the bench reports — verify with `python3 plugin/tests/run.py test_bench_hooks test_selfgate`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: a fixture tree whose fmguard patches resource.getrusage at import; the bench's reported CPU times are unaffected and no plugin/lib module is in sys.modules after import  <- CURRENT
2. [ ] the child read of the script budget in bench_hooks
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T03:51:02Z created
- 2026-11-05T03:51:16Z planned from capture
- 2026-11-05T03:51:16Z set approved=True
- 2026-11-05T03:51:17Z set scope=['plugin/tests/bench_hooks.py', 'plugin/tests/test_bench_hooks.py', 'CHANGELOG.md']
- 2026-11-05T03:51:17Z blocked: approved; right after T-3131 closes (the same files' neighbourhood), main thread or a builder
- 2026-11-06T03:52:34Z unblocked
## Follow-ups captured
