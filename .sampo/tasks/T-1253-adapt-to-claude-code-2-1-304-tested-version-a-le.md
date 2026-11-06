---
id: T-1253
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-20T13:46:48Z
updated: 2026-10-20T13:51:47Z
base: 8e943c4cb8a017aa7da88b7171b83cebd22215fd
base_tree: 77c6a28e6a3d02fa4edfc51da6fd86a19f71353b
plan0_at: 2026-10-20T13:46:53Z
plan0_scope: []
verified: strong
---
# Adapt to Claude Code 2.1.304: tested version, a leaner skill listing (compaction now re-sends it)
## Raw request
> Adapt to Claude Code 2.1.304: tested version, a leaner skill listing (compaction now re-sends it)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] CC_TESTED and README name 2.1.304, Foreman's skill descriptions are shorter and still route — verify with `python3 plugin/tests/run.py test_scout test_skillroute test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Bump the tested version; tighten the longest skill descriptions; build is user-only
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scout test_skillroute test_docs` → exit 0 · Ran 62 tests in 20.2s (16 classes, 16 at a time; slowest: Scout 20s, SkillRoute 2s, ScoutDrive 2s) / OK [ran] [tree 3fea8d053ada] (2026-10-20T13:49:09Z)
- (ac 1) `python3 plugin/tests/run.py test_scout test_skillroute test_docs` → exit 0 · Ran 62 tests in 20.0s (16 classes, 16 at a time; slowest: Scout 20s, SkillRoute 2s, ScoutDrive 2s) / OK [ran] [tree 3fea8d053ada] (2026-10-20T13:49:30Z)
- (audit intent) `self: listing total 2,730 → under 2,000 chars, locked by test_docs.Skills.test_the_listing_foreman_adds_stays_small; each description keeps its trigger words; fm doctor OK on 2.1.304` → Claude Code 2.1.304 re-sends the skill list after each compaction; Foreman's share shrank by ~27% and can't grow back past 2,000 unnoticed [tree 3fea8d053ada] (2026-10-20T13:49:30Z)
- (audit self) `self: listing total 2,730 → under 2,000 chars, locked by test_docs.Skills.test_the_listing_foreman_adds_stays_small; each description keeps its trigger words; fm doctor OK on 2.1.304` → no findings [tree 3fea8d053ada] (2026-10-20T13:49:30Z)
- (audit intent) `self: listing total 2,730 → under 2,000 chars, locked by test_docs.Skills.test_the_listing_foreman_adds_stays_small; each description keeps its trigger words; fm doctor OK on 2.1.304` → Claude Code 2.1.304 re-sends the skill list after each compaction; Foreman's share shrank by ~27% and can't grow back past 2,000 unnoticed [tree 3fea8d053ada] (2026-10-20T13:50:53Z)
- (audit self) `self: listing total 2,730 → under 2,000 chars, locked by test_docs.Skills.test_the_listing_foreman_adds_stays_small; each description keeps its trigger words; fm doctor OK on 2.1.304` → no findings [tree 3fea8d053ada] (2026-10-20T13:50:53Z)
## Log
- 2026-10-20T13:46:48Z created
- 2026-10-20T13:46:53Z focused
- 2026-10-20T13:46:58Z criterion 1 verify: `python3 plugin/tests/run.py test_scout test_skills test_docs` → `python3 plugin/tests/run.py test_scout test_skillroute test_docs`
- 2026-10-20T13:51:46Z done
- 2026-10-20T13:51:47Z committed 61306fef (18 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-0944 [FEATURE M, done, 4 steps] Adopt Claude Code 2.1.296–2.1.301: install it, fix subagent turn.start in the pane, re-verify hooks, move Text bold to weight, record t…
- playbook Strategic Compact Skill (skills/playbooks/references/context/strategic-compact.md)
- decision 2026-10-06: [costly] fm ask grants stay Claude-Code-only on Codex/Gemini/opencode until T-0336 verifies live whether their prompt hooks fire for agent-written s…
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–4 steps
## Behaviour lock
test_docs.Skills: every skill still has valid frontmatter and its user-only flag (build joins capture as user-only); the new listing-budget test was red at 2,730 and green under 2,000; test_skillroute (routing) unchanged and green
## Files touched
- plugin/tests/test_docs.py
- plugin/commands/build.md
- plugin/skills/brainstorm/SKILL.md
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
- plugin/workflows/ideas.js
- plugin/workflows/review.js
- CHANGELOG.md
- README.md
- plugin/lib/fmscout.py
