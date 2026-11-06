---
id: T-1698
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/skills, plugin/lib/fmdoctor.py, plugin/tests/test_docs.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T22:36:23Z
updated: 2026-10-22T23:17:26Z
lane_branch: worktree-agent-af7602f15e97c03f9
base: e457cf0cb8ed0fa1892980c6b98a471b1225a064
base_tree: 5dd56ce71a39c7b579da5d9b3ba8424e97501cfe
plan0_at: 2026-10-22T22:58:32Z
plan0_scope: [plugin/skills, plugin/lib/fmdoctor.py, plugin/tests/test_docs.py, CHANGELOG.md]
verified: ok
---
# Skill descriptions in task terms, and fm doctor's skills lint (Foreman jargon, overlapping descriptions)
## Raw request
> Skill descriptions in task terms, and fm doctor's skills lint (Foreman jargon, overlapping descriptions)
## Interpretation
Claude Code shows the model only each skill's name and description; Foreman's say 'Use when STATE says…' instead of what the person is doing. Rewrite all 13 in task terms ('Use whenever you are about to …'), and add a lint to fm doctor so they stay that way.
## Assumptions (confidence)
## Acceptance criteria
- [x] no model-invocable description leans on Foreman jargon (STATE, STATUS, RESUME, brief) without task words, and the lint flags two descriptions sharing over 60% of their words; the listing stays within its budget — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
Options: an LLM description optimiser run overnight (cost, drift); A/B tests (needs live runs); a hand rewrite plus a static lint. Choice: the rewrite and lint now; the static trigger eval (another task) guards it.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing lint test
2. [x] rewrite the descriptions
3. [x] doctor lint
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_docs 2>&1 | grep -A8 "stays_small" | head -12` → ✗ exit 1 · Ran 8 tests in 0.054s / FAILED (failures=1) [ran] [tree 3143be65c37e] (2026-10-22T23:00:06Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 123 tests in 8.5s (36 classes, 16 at a time; slowest: Fences 8s, Command 2s, TaskLifecycle 2s) / OK [ran] [tree 54d7f710c1b6] (2026-10-22T23:14:15Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 123 tests in 8.4s (36 classes, 16 at a time; slowest: Fences 8s, Command 2s, ViewsRepair 1s) / OK [ran] [tree 54d7f710c1b6] (2026-10-22T23:14:30Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 123 tests in 8.5s (36 classes, 16 at a time; slowest: Fences 8s, Command 2s, TaskLifecycle 2s) / OK [ran] [tree 54d7f710c1b6] (2026-10-22T23:14:39Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_doctor` → exit 0 · Ran 123 tests in 8.5s (36 classes, 16 at a time; slowest: Fences 8s, Command 2s, TaskLifecycle 2s) / OK [ran] [tree 54d7f710c1b6] (2026-10-22T23:14:48Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 63 tests in 8.5s (15 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 54d7f710c1b6] (2026-10-22T23:14:57Z)
- (audit self) `self: read all 12 description rewrites (task wording, no STATE/STATUS/RESUME/brief, listing ≤ 2000) and the fmdoctor lint (skips user-only skills, whole-word jargon, >60% word overlap)` → descriptions now say what Claude is about to do; doctor's lint keeps them that way; tidy/doctor user-only from T-1705 kept on merge [tree 54d7f710c1b6] (2026-10-22T23:14:57Z)
- (audit self) `self: read all 12 description rewrites (task wording, no STATE/STATUS/RESUME/brief, listing ≤ 2000) and the fmdoctor lint (skips user-only skills, whole-word jargon, >60% word overlap)` → descriptions now say what Claude is about to do; doctor's lint keeps them that way; tidy/doctor user-only from T-1705 kept on merge [tree 54d7f710c1b6] (2026-10-22T23:17:22Z)
## Log
- 2026-10-22T22:36:23Z created
- 2026-10-22T22:36:25Z set scope=['plugin/skills', 'plugin/lib/fmdoctor.py', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-22T22:36:28Z from T-1692 (skills hardly used; brainstorm-skills-20261022)
- 2026-10-22T22:58:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1698.builder.md
- 2026-10-22T22:58:31Z focused
- 2026-10-22T23:12:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af7602f15e97c03f9 (branch worktree-agent-af7602f15e97c03f9 kept: not merged)
- 2026-10-22T23:13:31Z focused
- 2026-10-22T23:14:02Z merged worktree-agent-af7602f15e97c03f9 (14 file(s))
- 2026-10-22T23:17:21Z scope: plugin/tests/test_doctor.py holds check_frontmatter's tests, where the description lint is tested
- 2026-10-22T23:17:26Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- research mission-20261022-172631: Request: I also know there arent a lot of skills with foreman? and they are also hardly used? why? super improve!!!
- research T-1621-review: Verdict:** approve with nits. I read the diff and the worktree code but ran no tests. Two MEDIUM items are worth fixing before merge. [stale: plu…
- decision 2026-10-22: Skills fix: make the hooks name the skill and rewrite descriptions in task terms before adding skills; keep the 2,000-character listing cap and free…
- likely tests for the scope: plugin/tests/test_doctor.py
## Behaviour lock
none: the lane didn't record a pre-edit run. The change is text in description lines plus a new doctor lint (intended new behaviour); test_docs and test_doctor (123 tests) are green on the merged tree, and the listing-budget and frontmatter tests guard what existed.
## Lessons
- Skill descriptions trigger on the model's situation, not user keywords: write 'Use whenever you are about to …'
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/directions/SKILL.md
- plugin/skills/doctor/SKILL.md
- plugin/skills/improve/SKILL.md
- plugin/skills/intake/SKILL.md
- plugin/skills/library/SKILL.md
- plugin/skills/next/SKILL.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/reflect/SKILL.md
- plugin/skills/resume/SKILL.md
- plugin/skills/status/SKILL.md
- plugin/skills/tidy/SKILL.md
