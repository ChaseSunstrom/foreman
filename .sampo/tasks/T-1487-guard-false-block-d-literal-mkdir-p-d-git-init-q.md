---
id: T-1487
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T17:33:47Z
updated: 2026-10-23T05:05:44Z
group: guard corpus and false blocks
done_in: T-1727
---
# Guard false block: D=/literal; mkdir -p $D && git init -q $D && printf … > $D/p.sh is refu
## Raw request
> Guard false block: D=/literal; mkdir -p $D && git init -q $D && printf … > $D/p.sh is refused as a tree write over protected core: with ; mixed with && the env is None, $D is unresolved and the guess falls back to cwd (fmguard.py:2382-2394, 2700-2705, 1880-1884). Make it resolve, add the forms to test_guard_diff FORMS (and keep D=~ … git init blocked), and say '$D unresolved' instead of 'git init writes its folder'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] D=/literal; mkdir -p $D && git init -q $D && printf … > $D/p.sh resolves $D and passes outside core; D=~ … git init $D still refuses; the message says '$D unresolved' when it can't resolve — verify with `cd plugin/tests && python3 -m unittest test_guard_diff test_guard.GitInitTarget`
## Non-goals
## Approach (options → choice → why)
Options: special-case git init; chosen: make _prefix_vars carry a literal assignment across ; as well as && (bash runs them in order in the same shell), and word the unresolved-target message by cause.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] resolve the variable across ; and &&
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-22T17:33:47Z created
- 2026-10-22T18:13:50Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'plugin/tests/test_guard_diff.py', 'CHANGELOG.md']
- 2026-10-23T03:33:02Z batched into T-1727
- 2026-10-23T05:05:44Z done in T-1727 (batch)
## Follow-ups captured
