---
id: T-1074
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmap.py, plugin/lib/fmoutcomes.py, plugin/tests/test_map.py, plugin/tests/test_audit.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T05:39:39Z
base: 4ea8e9900645461807bb0179155a057a1f5ea505
base_tree: bf9462183fd08a14c51fb19205ad1ba0832c61bf
verified: strong
---
# Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a
## Raw request
> FEATURE: Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and audit prep of a task that touches them (wild C18)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
A file that keeps being fixed after edits (git fix/revert commits touching it) is flagged at `fm task focus` (the plan record) and in `fm audit prep` pre-audit findings for any task whose scope or diff touches it (wild C18, "hotspots x2"). Already covered: the task-outcome atlas flags files where finished tasks needed a later fix, shown only at focus (`fmoutcomes.py:203` `caution`, called `fmcli.py:2206`); the map's "hot" is plain churn (`fmmap.py:71`) and the tour's "hot file" risk reason (`fmmap.py:368`). Missing: a git-history fix-after-edit count, and any mention in audit prep.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm map --json` lists `fixy`, and `fm task focus` prints "Hotspot:" for a scoped file in it — verify with `python3 plugin/tests/run.py test_map`
- [x] `fm audit prep` pre-audit lists "hotspot" for a diff touching it — verify with `python3 plugin/tests/run.py test_audit`
## Non-goals
## Approach (options → choice → why)
(a) extend `fmoutcomes.caution` only, which gets no signal from untracked history; (b) new module, which is overkill; (c) add `fixy` to `fmmap.build` (files in ≥3 commits with fix/revert/bug subjects in 180 days, VERSION 8→9), print it from `caution` and from `pre_audit`. Choose (c): the map is cached and both callers already load it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: in a temp repo make 3 "fix:" commits touching a.py and 1 touching b.py; assert `m["fixy"]` has a.py only; focus on a task scoped to a.py prints "Hotspot: a.py"; pre_audit on a diff with a.py returns a line containing "hotspot"; b.py does not.
2. [x] `fmmap._fixy(root, files)` using one `git log --name-only --format=%x00%s`, regex `\b(fix|revert|bug|hotfix)`; store in build(); bump VERSION.
3. [x] Add the hotspot line to `fmoutcomes.caution` (take the map via `fmmap.load`) and to `fmmap.pre_audit` next to the `pairs` block (`fmmap.py:555`).
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_map` → ✗ exit 1 · Ran 8 tests in 2.0s (3 classes, 16 at a time; slowest: Map 2s, Cold 0s, RoundG 0s) / FAILED (1 classes) [ran] [tree f977832cdb22] (2026-10-16T05:27:22Z)
- (step 2) `python3 plugin/tests/run.py test_map` → exit 0 · Ran 8 tests in 2.7s (3 classes, 16 at a time; slowest: Map 2s, Cold 1s, RoundG 0s) / OK [ran] [tree 69504e40b3fc] (2026-10-16T05:28:04Z)
- (step 3) `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 20 tests in 3.0s (15 classes, 16 at a time; slowest: ImportCards 3s, TaskLifecycle 2s, RoundFiveWorkflow 1s) / OK [ran] [tree 69504e40b3fc] (2026-10-16T05:28:07Z)
- (ac 1) `python3 plugin/tests/run.py test_map` → exit 0 · Ran 8 tests in 2.2s (3 classes, 16 at a time; slowest: Map 2s, Cold 0s, RoundG 0s) / OK [ran] [tree 69456129a3ed] (2026-10-16T05:39:38Z)
- (ac 2) `python3 plugin/tests/run.py test_audit` → exit 0 · Ran 20 tests in 2.3s (15 classes, 16 at a time; slowest: ImportCards 2s, TaskLifecycle 1s, RoundFiveWorkflow 1s) / OK [ran] [tree 69456129a3ed] (2026-10-16T05:39:38Z)
- `python3 plugin/tests/run.py test_map test_audit test_outcomes` → exit 0 · Ran 43 tests in 9.3s (26 classes, 16 at a time; slowest: Survival 9s, Map 3s, ImportCards 3s) / OK [ran] [tree 69456129a3ed] (2026-10-16T05:39:38Z)
- (audit intent) `review: one fm-reviewer pass (combined with T-1079/T-1072); 4 findings fixed by the builder test-first` → plans name the files that keep getting fixed, at focus and in the audit brief [tree 69456129a3ed] (2026-10-16T05:39:38Z)
- (audit adversary) `review: one fm-reviewer pass (combined with T-1079/T-1072); 4 findings fixed by the builder test-first` → file paths from git log go through plain() in read(); no untrusted text otherwise [tree 69456129a3ed] (2026-10-16T05:39:38Z)
- (audit edge) `review: one fm-reviewer pass (combined with T-1079/T-1072); 4 findings fixed by the builder test-first` → sweeping commits (>20 files) skipped; fixture/fixup don't match; empty scope or no git returns before loading the map [tree 69456129a3ed] (2026-10-16T05:39:38Z)
- (audit operator) `review: one fm-reviewer pass (combined with T-1079/T-1072); 4 findings fixed by the builder test-first` → one extra git log per map build; capped at 50 files ordered by count [tree 69456129a3ed] (2026-10-16T05:39:38Z)
- (audit maintainer) `review: one fm-reviewer pass (combined with T-1079/T-1072); 4 findings fixed by the builder test-first` → fixy is a {file: n} dict in map.json (VERSION 9); caution returns multi-line text, its one caller filters and joins [tree 69456129a3ed] (2026-10-16T05:39:38Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:50Z set scope=['plugin/lib/fmmap.py', 'plugin/lib/fmoutcomes.py', 'plugin/tests/test_map.py', 'plugin/tests/test_audit.py']
- 2026-10-16T04:22:50Z set tier=M
- 2026-10-16T05:26:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1074.builder.md
- 2026-10-16T05:26:58Z focused
- 2026-10-16T05:39:16Z merged worktree-agent-aaf4d66c59a0a2c13 (4 file(s))
- 2026-10-16T05:39:16Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aaf4d66c59a0a2c13
- 2026-10-16T05:39:16Z focused
- 2026-10-16T05:39:24Z scope: CHANGELOG.md — release note
- 2026-10-16T05:39:39Z done
- 2026-10-16T05:39:39Z committed a79ee93 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_map.py, plugin/tests/test_outcomes.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmmap.py, plugin/lib/fmoutcomes.py, plugin/tests/test_audit.py, plugin/tests/test_map.py; re-ground the plan against them before editing
## Lessons
- A history signal needs a cap on sweeping commits, or a lint pass makes every file look hot
## Plan gaps
- failed first: step 1 Failing tests: in a temp repo make 3 "fix:" commits touching a.py and 1 touching b.py; assert `m["f…
## Files touched
- plugin/tests/test_map.py
- plugin/tests/test_audit.py
- plugin/lib/fmmap.py
- plugin/lib/fmoutcomes.py
- CHANGELOG.md
