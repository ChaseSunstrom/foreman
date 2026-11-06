---
id: T-1885
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/**, plugin/tests/test_playbook_route.py, plugin/tests/test_playbook_check.py, CHANGELOG.md, MASTER.md]
depends_on: [T-1881]
source: discovered
created: 2026-10-29T00:18:41Z
updated: 2026-10-29T05:06:53Z
base: a263822937326fc2401f83109234f2a561b4bd89
base_tree: 44b8c809dba07afeea44ed6bce3868f28df635f5
plan0_at: 2026-10-29T04:36:37Z
plan0_scope: [plugin/skills/playbooks/**, plugin/tests/test_playbook_route.py, plugin/tests/test_playbook_check.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Grow the playbook library with real books: T-1803 built routing for 10k+ books but the lib
## Raw request
> Grow the playbook library with real books: T-1803 built routing for 10k+ books but the library is still 82 — mine finished tasks (fm playbooks mine/draft) into new, deduped, routed books, keep only ones that route and get used
## Interpretation
Routing 600 finished tasks found six kinds of work with no book (or a wrong one): command-guard rules, CLI argument errors, benchmark statistics, shipping a branch to main, regex backtracking, surface parity. Write those six books from the tasks that did the work, route them, and prove routing on held-out real titles.
## Assumptions (confidence)
## Acceptance criteria
- [x] Six mined books route their kind of task in the top 3 on held-out real titles; the labelled routing test keeps its thresholds — verify with `python3 plugin/tests/run.py test_playbook_route`
- [x] SKILL.md stays under its budget, every book is listed, no dead index line — verify with `python3 plugin/tests/run.py test_playbook_check`
## Non-goals
## Approach (options → choice → why)
Options: (a) fm playbooks draft per gap, then hand-edit; (b) write each from the mined tasks directly; (c) one generic book per stage. Chose (b): the drafts were read and the books are short, so writing them is cheaper than editing drafts; (c) routes badly. perf and security get an INDEX.md so SKILL.md has room.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Routing test for the six kinds on held-out titles (red)
2. [x] Six books, perf/security INDEX.md, SKILL.md and release/INDEX.md lines (green)
3. [x] CHANGELOG and MASTER
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -j 2 test_playbook_route test_playbook_check` → exit 0 · Ran 60 tests in 5.3s (12 classes, 2 at a time; slowest: Snippets 2s, Coverage 2s, Cli 2s) / OK [ran] [tree 053a4704863a] (2026-10-29T05:06:16Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_check` → exit 0 · Ran 36 tests in 2.5s (10 classes, 16 at a time; slowest: Snippets 2s, Coverage 2s, Repo 1s) / OK [ran] [tree 053a4704863a] (2026-10-29T05:06:34Z)
- (step 3) `grep -q T-1885 CHANGELOG.md && grep -q T-1885 MASTER.md` → exit 0 · (no output) [ran] [tree 053a4704863a] (2026-10-29T05:06:35Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_route` → exit 0 · Ran 24 tests in 2.3s (2 classes, 16 at a time; slowest: Cli 2s, Rank 1s) / OK [ran] [tree 053a4704863a] (2026-10-29T05:06:50Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_check` → exit 0 · Ran 36 tests in 2.5s (10 classes, 16 at a time; slowest: Snippets 2s, Coverage 2s, Repo 1s) / OK [ran] [tree 053a4704863a] (2026-10-29T05:06:50Z)
- (audit intent) `fm-reviewer pass on the lane: 2 medium + nits, fixed in cf500840; criteria re-run on the merged tree` → six books cover the unrouted kinds, held-out titles route top 3 [tree 053a4704863a] (2026-10-29T05:06:50Z)
- (audit edge) `fm-reviewer pass on the lane: 2 medium + nits, fixed in cf500840; criteria re-run on the merged tree` → SKILL.md budget held by stage INDEX.md for perf and security [tree 053a4704863a] (2026-10-29T05:06:50Z)
- (audit adversary) `fm-reviewer pass on the lane: 2 medium + nits, fixed in cf500840; criteria re-run on the merged tree` → read security/command-guard.md for advice that weakens the guard: it says refuse what the parser can't read, block case beside every allow, grants stay user-only; nothing to exploit (docs only, no code path) [tree 053a4704863a] (2026-10-29T05:06:50Z)
## Log
- 2026-10-29T00:18:41Z created
- 2026-10-29T00:49:20Z set scope=['plugin/skills/playbooks/**', 'plugin/tests/test_playbook_route.py', 'plugin/tests/test_playbook_check.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-29T00:53:52Z set status=planned
- 2026-10-29T01:18:55Z plan re-read: only CHANGELOG.md moved; drafts re-applied clean in a trial tree with all queued drafts, tests green
- 2026-10-29T02:55:57Z set depends_on=['T-1881']
- 2026-10-29T04:36:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1885.builder.md
- 2026-10-29T04:36:36Z focused
- 2026-10-29T05:05:46Z merged worktree-agent-ae88a5539589fcd66 (12 file(s))
- 2026-10-29T05:05:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae88a5539589fcd66
- 2026-10-29T05:05:51Z focused
- 2026-10-29T05:06:51Z done
- 2026-10-29T05:06:53Z committed 489db69c (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1803 [FEATURE L, done, 3 steps] Playbook library at 10,000+ scale, all routed, none listed (user: 'tens of thousands of sk — lesson: A regex that reads a command's arg…
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1838 [FEATURE M, done, 3 steps] Fm playbooks route: top-1 missed on 3 of 3 real task titles (e.g. a stop-hook bug → strate — lesson: bm25 in FTS5 scores 0 for a word i…
- decision 2026-10-28: T-1838 step 3: the per-turn hint still does not name the top routed book
- similar finished tasks took 3–5 steps
## Preflight
Changed in scope since this was planned (2026-10-29): CHANGELOG.md, MASTER.md, plugin/skills/playbooks/SKILL.md, plugin/skills/playbooks/references/fix/cli-errors.md, plugin/skills/playbooks/references/perf/INDEX.md, plugin/skills/playbooks/references/p…; re-ground the plan against them before editing
## Lessons
- Mining finished-task titles by kind finds missing playbooks faster than brainstorming them
## Files touched
- plugin/tests/test_playbook_route.py
- plugin/skills/playbooks/references/fix/cli-errors.md
- plugin/skills/playbooks/references/perf/INDEX.md
- plugin/skills/playbooks/references/perf/benchmark-statistics.md
- plugin/skills/playbooks/references/perf/regex-backtracking.md
- plugin/skills/playbooks/references/release/ship-to-main.md
- plugin/skills/playbooks/references/review/surface-parity.md
- plugin/skills/playbooks/references/security/INDEX.md
- plugin/skills/playbooks/references/security/command-guard.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/release/INDEX.md
- MASTER.md
- CHANGELOG.md
