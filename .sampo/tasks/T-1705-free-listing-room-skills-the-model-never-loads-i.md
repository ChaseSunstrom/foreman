---
id: T-1705
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/skills, plugin/tests/test_docs.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T22:36:45Z
updated: 2026-10-22T23:18:48Z
base: 9778a0116957a8a16196adf325d942ad52e7d086
base_tree: e88eff9f13e444fc7f301995093d927fd98b44dd
plan0_at: 2026-10-22T22:58:59Z
plan0_scope: [plugin/skills, plugin/tests/test_docs.py, CHANGELOG.md]
verified: strong
---
# Free listing room: skills the model never loads itself (the hook already gives the fm command) become user-only slash commands
## Raw request
> Free listing room: skills the model never loads itself (the hook already gives the fm command) become user-only slash commands
## Interpretation
Foreman holds its skill listing to 2,000 characters (T-1253/T-1508: Claude Code resends it after every compaction). Skills the model never needs to load itself (the hook hands it the fm command: tidy, improve) can be user-only, freeing room for the new job skills without raising the cap.
## Assumptions (confidence)
## Acceptance criteria
- [x] the listing total drops by at least 250 characters; every skill a hook tells the model to load stays model-invocable — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
Options: raise the cap (rejected in T-1508); merge skills (churn); demote the user-triggered ones. Choice: demote only those no hook asks the model to load.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] frontmatter and USER_ONLY
## Resume here
## Docs impact
plugin/rules/foreman.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 63 tests in 9.1s (15 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree 54d7f710c1b6] (2026-10-22T23:17:46Z)
- (step 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 63 tests in 9.3s (15 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 54d7f710c1b6] (2026-10-22T23:17:56Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_rules test_evals` → ✗ exit 1 · run.py: no test matches test_evals [ran] [tree 54d7f710c1b6] (2026-10-22T23:17:57Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 63 tests in 8.7s (15 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree 54d7f710c1b6] (2026-10-22T23:18:24Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 63 tests in 9.1s (15 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree 54d7f710c1b6] (2026-10-22T23:18:34Z)
- (audit self) `self: tidy and doctor user-only (improve kept model-invocable after checking the rules map plain words to it); rules map clean up / is foreman ok? to fm tidy / fm doctor; a new test holds every rules-mapped /foreman:X model-invocable` → ~270 listing characters freed for job skills; no hook or rules mapping points the model at a skill it can't load [tree 54d7f710c1b6] (2026-10-22T23:18:34Z)
- (audit adversary) `self: tidy and doctor user-only (improve kept model-invocable after checking the rules map plain words to it); rules map clean up / is foreman ok? to fm tidy / fm doctor; a new test holds every rules-mapped /foreman:X model-invocable` → no capability widened: the change only removes two skills from model invocation; the user can still type /foreman:tidy and /foreman:doctor [tree 54d7f710c1b6] (2026-10-22T23:18:34Z)
## Log
- 2026-10-22T22:36:45Z created
- 2026-10-22T22:36:45Z set scope=['plugin/skills', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-22T22:36:46Z from T-1692 (skills hardly used; brainstorm-skills-20261022)
- 2026-10-22T22:58:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1705.builder.md
- 2026-10-22T22:58:58Z focused
- 2026-10-22T23:13:23Z merged worktree-agent-ae0931dc193e0d13f (9 file(s))
- 2026-10-22T23:13:23Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae0931dc193e0d13f
- 2026-10-22T23:17:37Z focused
- 2026-10-22T23:18:24Z scope: plugin/rules/foreman.md and plugin/evals (rules now map clean up / is foreman ok? to fm tidy / fm doctor; eval prompts embed the rules)
- 2026-10-22T23:18:48Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-22: Skills fix: make the hooks name the skill and rewrite descriptions in task terms before adding skills; keep the 2,000-character listing cap and free…
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- research T-1472-review: Verdict:** changes needed. The commands/hooks listing meets both acceptance criteria on a read of the code. The note's delivery channel and its 1…
## Behaviour lock
none: the lane didn't record a pre-edit run. Three frontmatter keys, one rules line and the synced eval prompts; test_docs (listing budget, USER_ONLY, rules budget, eval-sync, every rules-mapped skill model-invocable) is green on the merged tree.
## Lessons
- Before making a skill user-only, grep the rules file for plain-word mappings to it: the model can't load a user-only skill
## Files touched
- plugin/tests/test_docs.py
- plugin/skills/tidy/SKILL.md
- plugin/skills/improve/SKILL.md
- plugin/skills/doctor/SKILL.md
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmdoctor.py
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/directions/SKILL.md
- plugin/skills/intake/SKILL.md
- plugin/skills/library/SKILL.md
- plugin/skills/next/SKILL.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/reflect/SKILL.md
- plugin/skills/resume/SKILL.md
- plugin/skills/status/SKILL.md
- plugin/tests/test_doctor.py
