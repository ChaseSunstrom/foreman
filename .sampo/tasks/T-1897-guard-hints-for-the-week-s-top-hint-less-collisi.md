---
id: T-1897
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/lib/fmrisk.py, plugin/tests/test_safety.py, plugin/tests/test_risk.py, CHANGELOG.md]
depends_on: [T-1885]
source: discovered
created: 2026-10-29T02:37:42Z
updated: 2026-10-29T05:14:50Z
base: 489db69c23560350f60dccddf353818ed4021bb1
base_tree: 053a4704863a5788f946ca15854b707ef6b62d89
plan0_at: 2026-10-29T04:38:30Z
plan0_scope: [plugin/lib/fmguard.py, plugin/lib/fmrisk.py, plugin/tests/test_safety.py, plugin/tests/test_risk.py, CHANGELOG.md]
verified: strong
---
# Guard hints for tree writes over Foreman and edits with no task; readable rule names
## Raw request
> Guard hints for the week's top hint-less collisions: core tree write over plugin/ (21× in 7 days, what passes: git in a worktree or fm edit), core:interpreter-code (17×), brief:path-py (6×); also name rules readably (core:a-tree-write-over)
## Interpretation
The week's most-hit guard blocks carry no hint of what passes: add one to the core tree-write block (fm edit, or git in a scratch worktree) and to fm risk's brief block (how to start a task); rule names drop filler words and read contractions as words.
## Assumptions (confidence)
## Acceptance criteria
- [x] a core tree-write block hints fm edit or a scratch worktree; fm risk says how to start a task for a brief block; rule names drop filler and read contractions as words — verify with `python3 plugin/tests/run.py -j 2 test_safety test_risk`
## Non-goals
A hint for core:interpreter-code (its detail already says what passes). Renaming stored ledger rules (old names age out of the 7-day window).
## Approach (options → choice → why)
Hint text on the block's detail and in fm risk's rule list; a rule-name normalizer in fmrisk. Alternatives: a docs page only (agents don't read it at the block), loosening the block (never weaken the guard).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: rule names, tree-write hint, brief rewrite
2. [x] Implement rule_id filler and quote fix, _hint core tree write, fmrisk brief rewrite
3. [x] Docs: CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-29T05:10:10Z steps 3/3 done
- git: foreman/build; 1 uncommitted: CHANGELOG.md
- touched since last checkpoint: .claude/worktrees/agent-a3819c7350f17e7af/plugin/tests/test_risk.py, .claude/worktrees/agent-a3819c7350f17e7af/plugin/tests/test_safety.py, .claude/worktrees/agent-a3819c7350f17e7af/CHANGELOG.md, .claude/worktrees/agent-a3819c7350f17e7af/plugin/lib/fmguard.py, .claude/worktrees/agent-a3819c7350f17e7af/plugin/lib/fmrisk.py, CHANGELOG.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1919.txt
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -j 2 test_safety test_risk` → exit 0 · Ran 34 tests in 7.0s (9 classes, 2 at a time; slowest: SafetyGate 4s, Risk 3s, ReleaseGate 3s) / OK [ran] [tree d4c5c53c1fd3] (2026-10-29T05:07:27Z)
- (step 2) `python3 plugin/tests/run.py -j 4 test_safety test_risk test_guard test_replay test_recall` → exit 0 · Ran 355 tests in 21.6s (105 classes, 4 at a time; slowest: Recall 16s, Mutation 7s, OtherProjects 6s) / OK [ran] [tree d4c5c53c1fd3] (2026-10-29T05:08:05Z)
- (step 3) `grep -q T-1897 CHANGELOG.md` → exit 0 · (no output) [ran] [tree d4c5c53c1fd3] (2026-10-29T05:08:05Z)
- (ac 1) `python3 plugin/tests/run.py -j 2 test_safety test_risk 2>&1 | tail -15` → ✗ exit 1 · FAILED (2 classes) / ✗ exit 1 (10.0 s; last 37 of 37 lines) [ran] [tree cadc856958b8] (2026-10-29T05:12:40Z)
- (step 2) `python3 plugin/tests/run.py -j 4 test_safety test_risk test_guard test_replay test_recall` → exit 0 · Ran 356 tests in 24.2s (105 classes, 4 at a time; slowest: Recall 16s, Mutation 7s, OtherProjects 6s) / OK [ran] [tree 47687e0a4155] (2026-10-29T05:14:12Z)
- (ac 1) `python3 plugin/tests/run.py -j 2 test_safety test_risk` → exit 0 · Ran 35 tests in 7.2s (9 classes, 2 at a time; slowest: SafetyGate 4s, Risk 3s, ReleaseGate 3s) / OK [ran] [tree 420efebfc1e4] (2026-10-29T05:14:38Z)
- (audit intent) `one fm-reviewer pass over the lane diff: 2 MEDIUM, 4 LOW; fixed the hint gaps and wording test-first, accepted the rest` → the week's top two hint-less rules (tree-write-over, interpreter-code) now carry a hint; test_safety pins both [tree 420efebfc1e4] (2026-10-29T05:14:38Z)
- (audit adversary) `one fm-reviewer pass over the lane diff: 2 MEDIUM, 4 LOW; fixed the hint gaps and wording test-first, accepted the rest` → hints and rule names only; no block is weakened or skipped, test_guard and fm replay green [tree 420efebfc1e4] (2026-10-29T05:14:38Z)
- (audit edge) `one fm-reviewer pass over the lane diff: 2 MEDIUM, 4 LOW; fixed the hint gaps and wording test-first, accepted the rest` → old ledger rows keep the old rule names, so a week of counts splits between core:a-tree-write-over and core:tree-write-over; accepted, it ages out [tree 420efebfc1e4] (2026-10-29T05:14:38Z)
- (audit operator) `one fm-reviewer pass over the lane diff: 2 MEDIUM, 4 LOW; fixed the hint gaps and wording test-first, accepted the rest` → the tree-write hint leads with the scratch-worktree route and names the standing core yes; the brief fallback gives the full fm task new form [tree 420efebfc1e4] (2026-10-29T05:14:38Z)
- (audit maintainer) `one fm-reviewer pass over the lane diff: 2 MEDIUM, 4 LOW; fixed the hint gaps and wording test-first, accepted the rest` → one _hint branch per rule beside the others; fmrisk reuses fmguard._hint [tree 420efebfc1e4] (2026-10-29T05:14:38Z)
## Log
- 2026-10-29T02:37:42Z created
- 2026-10-29T02:54:38Z set title=Guard hints for tree writes over Foreman and edits with no task; readable rule names, scope=['plugin/lib/fmguard.py', 'plugin/lib/fmrisk.py', 'plugin/tests/test_safety.py', 'plugin/tests/test_risk.py', 'CHANGELOG.md']
- 2026-10-29T02:54:39Z planned: it has criteria and steps
- 2026-10-29T02:55:58Z set depends_on=['T-1885']
- 2026-10-29T04:38:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1897.builder.md
- 2026-10-29T04:38:29Z focused
- 2026-10-29T05:07:09Z merged worktree-agent-a3819c7350f17e7af (4 file(s))
- 2026-10-29T05:07:12Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3819c7350f17e7af
- 2026-10-29T05:07:14Z focused
- 2026-10-29T05:14:49Z done
- 2026-10-29T05:14:50Z committed 4fc45cd5 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1875-review: Approve with nits. The feature meets the acceptance criterion in code. I did not run the tests, because I only had read tools. There are no HIGH …
- T-1875 [FEATURE M, done, 3 steps] Fm risk lists the week's guard collisions by rule with the rewrite that passes, and Sessio — lesson: A new SessionStart line has to ear…
- T-1851 [FEATURE M, done, 2 steps] 3D showpiece: terrain, a heightfield of churn or cost over time (from T-1655) — lesson: A collision fallback name needs its own loop: o…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_guard.py, plugin/tests/test_risk.py
## Preflight
Changed in scope since this was planned (2026-10-29): CHANGELOG.md, plugin/lib/fmguard.py, plugin/lib/fmrisk.py, plugin/tests/test_risk.py, plugin/tests/test_safety.py; re-ground the plan against them before editing
## Lessons
- A hint that sends Claude to a second guarded route must name that route's grant, or it trades one block for another
## Files touched
- plugin/tests/test_risk.py
- plugin/tests/test_safety.py
- CHANGELOG.md
- plugin/lib/fmguard.py
- plugin/lib/fmrisk.py
