---
id: T-1702
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcost.py, plugin/lib/fmhooks.py, plugin/tests/test_cost.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T22:36:38Z
updated: 2026-10-22T23:37:51Z
base: 889cef16c7faa137f4304cb1314c772717bd9042
base_tree: 7a8c275db192c6f9bbae819b88a8fd0613c1e70e
plan0_at: 2026-10-22T22:58:43Z
plan0_scope: [plugin/lib/fmcost.py, plugin/lib/fmhooks.py, plugin/tests/test_cost.py, CHANGELOG.md]
verified: strong
---
# fm usage counts skills honestly: hook-named skills, slash commands and subagent playbook reads, and lists skills named but not loaded
## Raw request
> fm usage counts skills honestly: hook-named skills, slash commands and subagent playbook reads, and lists skills named but not loaded
## Interpretation
fm usage counts only Skill tool events and the main session's playbook reads, so '12 of 13 never used' may undercount slash commands and subagent reads, and it can't tell 'never offered' from 'offered and ignored'. A skill_named event from the hooks makes misses visible.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fixture where the hook named /foreman:X and the model ran fm without loading X reports 'named, not loaded: X'; user-typed /foreman:x and subagent reads count — verify with `python3 plugin/tests/run.py test_cost`
## Non-goals
## Approach (options → choice → why)
Options: mine transcripts on demand (slow); log at the source (hooks know what they named). Choice: log at the source, compare in fm usage.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] skill_named events and counting
3. [x] named-not-loaded report
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_cost 2>&1 | tail -15` → ✗ exit 1 · Ran 16 tests in 15.2s (7 classes, 16 at a time; slowest: TaskCostCap 14s, SkillUsage 1s, CostForecast 1s) / FAILED (1 classes) [ran] [tree e797e23ed0cc] (2026-10-22T23:01:37Z)
- (step 1) `python3 plugin/tests/run.py test_cost` → ✗ exit 1 · Ran 16 tests in 16.5s (7 classes, 16 at a time; slowest: TaskCostCap 16s, CostForecast 2s, SkillUsage 2s) / FAILED (1 classes) [ran] [tree e797e23ed0cc] (2026-10-22T23:01:56Z)
- (ac 1) `python3 plugin/tests/run.py test_cost 2>&1 | tail -3` → exit 0 · Ran 16 tests in 6.9s (7 classes, 16 at a time; slowest: TaskCostCap 7s, SkillUsage 1s, CostForecast 1s) / OK [ran] [tree fdaff9da4b2a] (2026-10-22T23:03:16Z)
- (step 2) `python3 plugin/tests/run.py test_cost` → exit 0 · Ran 16 tests in 7.0s (7 classes, 16 at a time; slowest: TaskCostCap 7s, SkillUsage 1s, CostForecast 1s) / OK [ran] [tree fdaff9da4b2a] (2026-10-22T23:03:27Z)
- (step 3) `python3 plugin/tests/run.py test_cost` → exit 0 · Ran 16 tests in 6.7s (7 classes, 16 at a time; slowest: TaskCostCap 6s, SkillUsage 1s, CostForecast 1s) / OK [ran] [tree fdaff9da4b2a] (2026-10-22T23:03:34Z)
- (step 1) `python3 plugin/tests/run.py test_cost` → ✗ exit 1 · Ran 18 tests in 7.6s (7 classes, 16 at a time; slowest: TaskCostCap 7s, SkillUsage 2s, CostForecast 1s) / FAILED (1 classes) [ran] [tree e8a707fb8f3d] (2026-10-22T23:19:19Z)
- (step 2) `python3 plugin/tests/run.py test_cost` → exit 0 · Ran 18 tests in 9.1s (7 classes, 16 at a time; slowest: TaskCostCap 9s, SkillUsage 3s, CostForecast 1s) / OK [ran] [tree b790d8c83030] (2026-10-22T23:20:04Z)
- (step 3) `python3 plugin/tests/run.py test_cost` → exit 0 · Ran 18 tests in 11.4s (7 classes, 16 at a time; slowest: TaskCostCap 11s, SkillUsage 5s, CostForecast 2s) / OK [ran] [tree b790d8c83030] (2026-10-22T23:20:15Z)
- (ac 1) `python3 plugin/tests/run.py test_cost test_hooks` → exit 0 · Ran 219 tests in 81.3s (31 classes, 16 at a time; slowest: Stop 81s, NoTaskGate 42s, PreToolUse 32s) / OK [ran] [tree 49352ce99102] (2026-10-22T23:36:20Z)
- (ac 1) `python3 plugin/tests/run.py test_cost` → exit 0 · Ran 18 tests in 6.4s (7 classes, 16 at a time; slowest: TaskCostCap 6s, SkillUsage 2s, CostForecast 1s) / OK [ran] [tree 49352ce99102] (2026-10-22T23:36:39Z)
- (audit intent) `fm-reviewer full pass; HIGH (T-1697's 'load: Skill foreman:x' hints not matched) and two MEDIUMs (Stop reasons unlogged; non-skills like /foreman:review counted) fixed test-first after merging build; LOW name-length cap with a lookahead` → fm usage reports named-not-loaded skills, counts typed /foreman:x and lane playbook reads, so 'never used' can be told from 'offered and ignored' [tree 49352ce99102] (2026-10-22T23:36:39Z)
- (audit adversary) `fm-reviewer full pass; HIGH (T-1697's 'load: Skill foreman:x' hints not matched) and two MEDIUMs (Stop reasons unlogged; non-skills like /foreman:review counted) fixed test-first after merging build; LOW name-length cap with a lookahead` → names capped at 40 chars with a lookahead (a 100k-char typed name is never logged); users set no other event field; _skill_named swallows its own errors so a hook can't trip its breaker [tree 49352ce99102] (2026-10-22T23:36:39Z)
- (audit edge) `fm-reviewer full pass; HIGH (T-1697's 'load: Skill foreman:x' hints not matched) and two MEDIUMs (Stop reasons unlogged; non-skills like /foreman:review counted) fixed test-first after merging build; LOW name-length cap with a lookahead` → both spellings (/foreman:x and Skill foreman:x) matched; Stop and SubagentStop reasons logged; only real skills counted [tree 49352ce99102] (2026-10-22T23:36:39Z)
- (audit operator) `fm-reviewer full pass; HIGH (T-1697's 'load: Skill foreman:x' hints not matched) and two MEDIUMs (Stop reasons unlogged; non-skills like /foreman:review counted) fixed test-first after merging build; LOW name-length cap with a lookahead` → hook output size unchanged (events only); at most one event per injected note naming a skill [tree 49352ce99102] (2026-10-22T23:36:39Z)
## Log
- 2026-10-22T22:36:38Z created
- 2026-10-22T22:36:39Z set scope=['plugin/lib/fmcost.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_cost.py', 'CHANGELOG.md']
- 2026-10-22T22:36:40Z from T-1692 (skills hardly used; brainstorm-skills-20261022)
- 2026-10-22T22:58:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1702.builder.md
- 2026-10-22T22:58:42Z focused
- 2026-10-22T23:34:55Z merged worktree-agent-a82ead3cfc502e305 (4 file(s))
- 2026-10-22T23:34:55Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a82ead3cfc502e305
- 2026-10-22T23:34:58Z focused
- 2026-10-22T23:37:51Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- research T-1472-review: Verdict:** changes needed. The commands/hooks listing meets both acceptance criteria on a read of the code. The note's delivery channel and its 1…
- decision 2026-10-22: Skills fix: make the hooks name the skill and rewrite descriptions in task terms before adding skills; keep the 2,000-character listing cap and free…
- likely tests for the scope: plugin/tests/test_cost.py, plugin/tests/test_hooks.py
## Why not caught
none: the two lanes ran in parallel; the review caught the wording mismatch before merge
## Lessons
- When two lanes change the same contract (hint wording and its counter), the later one must merge the earlier before review, or its tests pass against the old wording
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_cost.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcost.py
- CHANGELOG.md
