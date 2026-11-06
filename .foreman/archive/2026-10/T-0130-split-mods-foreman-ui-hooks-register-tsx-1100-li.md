---
id: T-0130
type: CLEAN
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/**, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-10-03T04:44:02Z
updated: 2026-10-03T08:34:38Z
base: 44f216361fdac559cdf7ac5d6fff27f3da0eecb9
base_tree: b8e708994e1ab2b17072e3ce1b2e02be936e8693
verified: strong
---
# Split the mod: transcript rows into rows.tsx, shared atoms/constants/settings into state.ts
## Raw request
> Split mods/foreman-ui/hooks/register.tsx (~1100 lines) into band, pane, rows and state modules so a change reads one small file
## Interpretation
register.tsx is 1637 lines; every edit to a transcript row means reading around the band and pane. Move the pure row renderers (shell, edit, agent rows, diffs, meters, sparklines, mascot) to rows.tsx and the atoms, constants, shared maps and three settings to state.ts, with no behaviour change.
## Assumptions (confidence)
## Acceptance criteria
- [x] Behaviour lock: the mod's 57 tests pass before and after, and claude plugin validate accepts it — verify with `claude plugin test mods/foreman-ui && claude plugin validate mods/foreman-ui`
- [x] register.tsx loses the row renderers (under 1350 lines) — verify with `python3 -c "import sys; sys.exit(sum(1 for _ in open('mods/foreman-ui/hooks/register.tsx')) >= 1350)"`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) split everything (band, pane, helpers) behind one shared mutable-state object, renaming 17 module variables across 1600 lines; (b) move only what has no mutable state: the rows (they read three settings, which become a cfg object, and two maps) and the constants they share. Choice: (b): a mechanical, verifiable cut with no import cycle; the band and pane follow when next edited (captured).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Lock: tests and validate before
2. [x] Scripted move with generated imports
3. [x] Sync the dev copy; CHANGELOG and MASTER
## Resume here
## Docs impact
MASTER (foreman-ui modules line) and CHANGELOG.
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui && claude plugin validate mods/foreman-ui` → exit 0 · ❯ ./register.tsx state reads: foreman-ui.agents, foreman-ui.away, foreman-ui.beat, foreman-ui.ctx, foreman-ui.error, foreman-ui.files, foreman-ui.frame, foreman-ui.resumed, foreman-ui.shells, foreman- [ran] [tree b8e708994e1a] (2026-10-03T08:31:52Z)
- (step 2) `claude plugin test mods/foreman-ui && claude plugin validate mods/foreman-ui` → exit 0 · ❯ ./register.tsx state reads: foreman-ui.agents, foreman-ui.away, foreman-ui.beat, foreman-ui.ctx, foreman-ui.error, foreman-ui.files, foreman-ui.frame, foreman-ui.resumed, foreman-ui.shells, foreman- [ran] [tree 1717ad9267f1] (2026-10-03T08:34:28Z)
- (step 3) `cmp mods/foreman-ui/hooks/rows.tsx ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui/hooks/rows.tsx && grep -q T-0130 MASTER.md` → exit 0 · (no output) [ran] [tree 1717ad9267f1] (2026-10-03T08:34:29Z)
- (ac 1) `claude plugin test mods/foreman-ui && claude plugin validate mods/foreman-ui` → exit 0 · ❯ ./register.tsx state reads: foreman-ui.agents, foreman-ui.away, foreman-ui.beat, foreman-ui.ctx, foreman-ui.error, foreman-ui.files, foreman-ui.frame, foreman-ui.resumed, foreman-ui.shells, foreman- [ran] [tree 1717ad9267f1] (2026-10-03T08:34:38Z)
- (ac 2) `python3 -c "import sys; sys.exit(sum(1 for _ in open('mods/foreman-ui/hooks/register.tsx')) >= 1350)"` → exit 0 · (no output) [ran] [tree 1717ad9267f1] (2026-10-03T08:34:38Z)
- (ac 3) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:34 UTC); cached (fm check --fresh reruns) [ran] [tree 1717ad9267f1] (2026-10-03T08:34:38Z)
- (audit intent) `self (mechanical move, scripted): the behaviour lock (57 mod tests, claude plugin validate) passed before and after; leftover bare names checked (only a comment); the dev copy synced. The two engine rules found on the way ($ not across imports, atoms only in their declaring file) are in MASTER and shaped the follow-up T-0166.` → register.tsx 1637 → 1323 lines; the transcript rows (most-edited code this week) now live in a 300-line file; no behaviour changed [tree 1717ad9267f1] (2026-10-03T08:34:38Z)
- (audit maintainer) `self (mechanical move, scripted): the behaviour lock (57 mod tests, claude plugin validate) passed before and after; leftover bare names checked (only a comment); the dev copy synced. The two engine rules found on the way ($ not across imports, atoms only in their declaring file) are in MASTER and shaped the follow-up T-0166.` → rows take the resolved element table instead of $, so the next reader sees why; atoms stay with their readers; state.ts holds only constants, two maps and cfg, so there is no import cycle [tree 1717ad9267f1] (2026-10-03T08:34:38Z)
## Log
- 2026-10-03T04:44:02Z created
- 2026-10-03T08:31:40Z planned from capture
- 2026-10-03T08:31:40Z focused
- 2026-10-03T08:34:38Z done
- 2026-10-03T08:34:38Z committed 4c87037 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- likely tests for the scope: plugin/tests/test_shot.py
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/tools/shot.py, mods/foreman-ui/types/index.d.ts; re-ground the plan against them before editing
## Behaviour lock
claude plugin test mods/foreman-ui (57 tests) and claude plugin validate mods/foreman-ui, before and after the move; no test is edited.
## Lessons
- Before splitting a mod, read the validator's rules: the engine's static scan of $ and atoms decides where a function may live, not just the import graph.
## Files touched
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/rows.tsx
- mods/foreman-ui/hooks/state.ts
- CHANGELOG.md
- MASTER.md
