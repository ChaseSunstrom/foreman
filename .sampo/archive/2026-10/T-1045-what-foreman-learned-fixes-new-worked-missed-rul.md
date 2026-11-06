---
id: T-1045
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcost.py, plugin/lib/fmfixes.py, plugin/tests/test_learning.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx]
depends_on: []
source: followup
created: 2026-10-16T03:42:08Z
updated: 2026-10-16T08:42:56Z
base: ba44cb57bd9ec60b95c9fdb88626ee12db1df296
base_tree: b372fefe70a54d8a98ec2d7212dfa1e6445033f1
plan0_at: 2026-10-16T08:29:23Z
plan0_scope: [plugin/lib/fmcost.py, plugin/lib/fmfixes.py, plugin/tests/test_learning.py, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/types/index.d.ts, mods/foreman-ui/tests/foreman-ui.test.tsx]
verified: strong
---
# What Foreman learned: fixes new/worked/missed, rules from corrections, interventions per c
## Raw request
> What Foreman learned: fixes new/worked/missed, rules from corrections, interventions per closed task, in fm digest and as the pane's idle line (T-1029 C2, C12, C9)
## Interpretation
Show what Foreman learned in the window: known fixes added, applied and worked or missed, rules proposed from corrections, interventions (corrections plus guard denies) per closed task. It goes in fm digest (text and JSON) and as the pane's dim idle line.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm digest` prints "Learned:" with fixes new/worked/missed, rules and interventions per task — verify with `python3 plugin/tests/run.py test_learning test_fixes`
- [x] the pane shows it when idle — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
- [x] the pane shows the learned line when idle — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
Count from what is already recorded (fmfixes stats and records, ledger correction and rule events, done briefs). No new state. One helper feeds both the digest and fm ui's view key 'learned'; the mod renders it when nothing is running. Options considered: a separate fm learned command (more surface), or the digest only (the user asked for the pane too).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: seed fixes.md plus stats (worked 2, misses 1) with `correction` ledger events on a done task, then `fm digest --json` has `learned` with `fixes_new`, `worked`, `missed`, `interventions_per_task`; the text contains "per closed task".
2. [x] `fmfixes.learned(p, since)` (counts from stats `last` and records) plus an interventions helper in fmcost; add to `cmd_digest` output and the JSON.
3. [x] Render `v.learned` as the dim idle line in `register.tsx` (the field is added to the pane's view type). The pane's data source was not traced, so the builder must find where `FmView` is filled.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_fixes` → ✗ exit 1 · Ran 15 tests in 8.0s (1 classes, 16 at a time; slowest: KnownFixes 7s) / FAILED (1 classes) [ran] [tree f608443cc274] (2026-10-16T08:30:16Z)
- (step 2) `python3 plugin/tests/run.py test_fixes test_learning` → exit 0 · Ran 25 tests in 7.1s (11 classes, 16 at a time; slowest: KnownFixes 7s, Playbook 2s, Retire 2s) / OK [ran] [tree fc0f2e96d820] (2026-10-16T08:30:52Z)
- (step 3) `python3 plugin/tests/run.py test_ui test_board_surfaces` → exit 0 · Ran 30 tests in 11.4s (7 classes, 16 at a time; slowest: UiView 11s, BoardSurfaces 2s, UiSkills 1s) / OK [ran] [tree 90bce41c6b0b] (2026-10-16T08:32:15Z)
- (step 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 119 tests across 1 file. [13.86s] [ran] [tree 503e1a4e4dd0] (2026-10-16T08:37:49Z)
- (step 1) `python3 plugin/tests/run.py test_fixes test_learning test_ui test_board_surfaces` → exit 0 · Ran 55 tests in 26.3s (18 classes, 16 at a time; slowest: UiView 26s, KnownFixes 16s, BoardSurfaces 6s) / OK [ran] [tree 1d49809a6d6b] (2026-10-16T08:41:17Z)
- (ac 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 120 tests across 2 files. [11.22s] [ran] [tree b15f6fd04fab] (2026-10-16T08:42:02Z)
- (ac 1) `python3 plugin/tests/run.py test_learning test_fixes` → exit 0 · Ran 25 tests in 5.5s (11 classes, 16 at a time; slowest: KnownFixes 5s, Playbook 1s, Retire 1s) / OK [ran] [tree b15f6fd04fab] (2026-10-16T08:42:25Z)
- (ac 2) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 120 tests across 2 files. [11.11s] [ran] [tree b15f6fd04fab] (2026-10-16T08:42:25Z)
- (ac 3) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 120 tests across 2 files. [11.11s] [ran] [tree b15f6fd04fab] (2026-10-16T08:42:25Z)
- `python3 plugin/tests/run.py test_fixes test_learning` → exit 0 · Ran 25 tests in 5.5s (11 classes, 16 at a time; slowest: KnownFixes 5s, Playbook 1s, Retire 1s) / OK [ran] [tree b15f6fd04fab] (2026-10-16T08:42:25Z)
- (audit intent) `self review of the branch: counting from recorded state only; the pane line cost about 470 ms per poll → cached 120 s in state, warm fm ui back to about 0.3 s (measured 5 runs each); the idle block grows to 3 rows only when the line exists and nothing runs; the criterion's npm test never existed → fixed to the mod harness, 120/120` → digest and pane say what was learned [tree b15f6fd04fab] (2026-10-16T08:42:25Z)
- (audit adversary) `self review of the branch: counting from recorded state only; the pane line cost about 470 ms per poll → cached 120 s in state, warm fm ui back to about 0.3 s (measured 5 runs each); the idle block grows to 3 rows only when the line exists and nothing runs; the criterion's npm test never existed → fixed to the mod harness, 120/120` → read-only counts; the cache file is Foreman state written by fm itself [tree b15f6fd04fab] (2026-10-16T08:42:25Z)
- (audit edge) `self review of the branch: counting from recorded state only; the pane line cost about 470 ms per poll → cached 120 s in state, warm fm ui back to about 0.3 s (measured 5 runs each); the idle block grows to 3 rows only when the line exists and nothing runs; the criterion's npm test never existed → fixed to the mod harness, 120/120` → no closed task in the window says so instead of dividing by zero [tree b15f6fd04fab] (2026-10-16T08:42:25Z)
- (audit operator) `self review of the branch: counting from recorded state only; the pane line cost about 470 ms per poll → cached 120 s in state, warm fm ui back to about 0.3 s (measured 5 runs each); the idle block grows to 3 rows only when the line exists and nothing runs; the criterion's npm test never existed → fixed to the mod harness, 120/120` → one line idle, the digest's Learned block [tree b15f6fd04fab] (2026-10-16T08:42:25Z)
- (audit maintainer) `self review of the branch: counting from recorded state only; the pane line cost about 470 ms per poll → cached 120 s in state, warm fm ui back to about 0.3 s (measured 5 runs each); the idle block grows to 3 rows only when the line exists and nothing runs; the criterion's npm test never existed → fixed to the mod harness, 120/120` → fmfixes.learned and fmcost.learned feed both [tree b15f6fd04fab] (2026-10-16T08:42:25Z)
## Log
- 2026-10-16T03:42:08Z created
- 2026-10-16T04:22:55Z set scope=['plugin/lib/fmcost.py', 'plugin/lib/fmfixes.py', 'plugin/tests/test_learning.py', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/types/index.d.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx']
- 2026-10-16T04:22:55Z set tier=M
- 2026-10-16T08:29:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1045.builder.md
- 2026-10-16T08:29:22Z focused
- 2026-10-16T08:39:29Z criterion 2 verify: `cd mods/foreman-ui && npm test` → `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
- 2026-10-16T08:40:40Z merged worktree-agent-af638a65d5fc8abf7 (8 file(s))
- 2026-10-16T08:40:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af638a65d5fc8abf7
- 2026-10-16T08:40:48Z focused
- 2026-10-16T08:42:02Z scope: plugin/lib/fmwatch.py, plugin/lib/ui-demo.json, plugin/tests/test_fixes.py, mods/foreman-ui (types, register.tsx) — the pane line and its cache; CHANGELOG.md, MASTER.md — docs (with T-1050's lines)
- 2026-10-16T08:42:56Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- decision 2026-10-15: Size legend removed from the pane (T-0909)
- similar finished tasks took 5–6 steps
- likely tests for the scope: plugin/tests/test_fixes.py
## Preflight
Changed in scope since this was planned (2026-10-16): mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/fmcost.py, plugin/lib/fmfixes.py; re-ground the plan against them before editing
## Lessons
- Anything added to a per-poll view needs a timing before and after; a fresh process per poll defeats in-process memos
## Plan gaps
- failed first: step 1 Failing tests: seed fixes.md plus stats (worked 2, misses 1) with `correction` ledger events on a d…
## Files touched
- plugin/tests/test_fixes.py
- plugin/lib/fmfixes.py
- plugin/lib/fmcost.py
- plugin/lib/fmwatch.py
- mods/foreman-ui/types/index.d.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/lib/ui-demo.json
- CHANGELOG.md
- MASTER.md
