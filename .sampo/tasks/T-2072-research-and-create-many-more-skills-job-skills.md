---
id: T-2072
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T00:50:57Z
updated: 2026-10-31T04:17:14Z
inferred_deps: [T-2070]
inferred_why: T-2070: skills wrap playbooks, so playbooks come first
base: 81fac4cf37574a9bfa4b3222b0c8d34de051f8c5
base_tree: 4c85c5db575ee3b56ce6ad06de57a8fa566b6254
plan0_at: 2026-10-31T03:32:30Z
plan0_scope: []
verified: strong
---
# Research and create many more skills (job skills that wrap playbooks and fm verbs), use…
## Raw request
> FEATURE: research and create many more skills (job skills that wrap playbooks and fm verbs), use them, within the skill-listing budget
## Interpretation
Sessions do recurring jobs (refactor, performance, security review, docs, dependency upgrades, migrations, incident response…) that have playbooks and fm verbs but no job skill, so the model rarely loads the right procedure. Add job skills chosen from this project's own data (fm repeats, the stage words in plugin/skills/routing.json, ledger task types and the playbook stages most used), each a short 'Use whenever …' description that fires on task words and a body that wraps real playbooks and fm verbs — and make every skill actually used: the rules' plain-word map and fm which route to them. All within the 2,200-character listing budget (test_docs), tightening existing descriptions where needed.
## Assumptions (confidence)
## Acceptance criteria
- [x] at least four new model-invocable job skills, chosen from measured data (the brief names the data), each short, starting 'Use whenever', wrapping real playbooks and fm verbs; the listing stays within 2,200 characters; each wins the description-overlap test for its own plain request — verify with `python3 plugin/tests/run.py test_docs test_which`
## Non-goals
## Approach (options → choice → why)
Options: (1) a few model-invocable job skills from measured gaps, budget kept by tightening descriptions (chosen: the model can load them; data picks them); (2) many user-only skills (free in the listing, but the model can't use them); (3) one dispatcher skill (an extra hop, and its description can't fire on every job's words). Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] measure: fm repeats, routing.json stage words, task types and playbook stages in this project's ledger; pick the jobs with no skill
2. [x] red tests: test_docs job-skill and overlap entries for the new skills; listing budget
3. [x] write the skills (and tighten old descriptions to fit); route plain words to them in the rules map if one fits
4. [x] docs (MASTER skills line, CHANGELOG, README skills list)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/rules/foreman.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_docs test_which 2>&1 | grep -vE "^\s*$" | tail -25` → ✗ exit 1 · Ran 99 tests in 9.9s (25 classes, 16 at a time; slowest: Fences 9s, Which 5s, TaskLifecycle 2s) / FAILED (1 classes) [ran] [tree 8845d55b619f] (2026-10-31T03:43:15Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_which 2>&1 | grep -E "^(FAIL|ERROR)|^AssertionError|^ : |^OK|Ran|FAILED"` → ✗ exit 1 · Ran 99 tests in 10.6s (25 classes, 16 at a time; slowest: Fences 10s, Which 4s, TaskLifecycle 2s) / FAILED (1 classes) [ran] [tree 76c34e7c9e38] (2026-10-31T03:44:14Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_which 2>&1 | grep -E "^(FAIL|ERROR)|^AssertionError|^ : |^OK|Ran|FAILED"` → ✗ exit 1 · Ran 99 tests in 9.9s (25 classes, 16 at a time; slowest: Fences 10s, Which 3s, TaskLifecycle 1s) / FAILED (1 classes) [ran] [tree 2702a291e9ef] (2026-10-31T03:44:44Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_which 2>&1 | grep -E "^(FAIL|ERROR)|^AssertionError|^ : |^OK|Ran|FAILED"` → exit 0 · Ran 99 tests in 10.4s (25 classes, 16 at a time; slowest: Fences 10s, Which 5s, TaskLifecycle 2s) / OK [ran] [tree d828fbecc976] (2026-10-31T03:45:03Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_which` → exit 0 · Ran 99 tests in 8.4s (25 classes, 16 at a time; slowest: Fences 8s, Which 3s, TaskLifecycle 1s) / OK [ran] [tree bb9caaa94814] (2026-10-31T04:15:37Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_which` → exit 0 · Ran 99 tests in 8.4s (25 classes, 16 at a time; slowest: Fences 8s, Which 3s, TaskLifecycle 1s) / OK [ran] [tree 9fed4e52e6d1] (2026-10-31T04:16:22Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_which` → exit 0 · Ran 99 tests in 8.6s (25 classes, 16 at a time; slowest: Fences 8s, Which 3s, TaskLifecycle 1s) / OK [ran] [tree 9fed4e52e6d1] (2026-10-31T04:16:31Z)
- (step 4) `grep -c 'T-2072' CHANGELOG.md && grep -c 'foreman:security-review' MASTER.md` → exit 0 · 1 / 1 [ran] [tree 9fed4e52e6d1] (2026-10-31T04:16:31Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_which` → exit 0 · Ran 99 tests in 8.4s (25 classes, 16 at a time; slowest: Fences 8s, Which 3s, TaskLifecycle 1s) / OK [ran] [tree 9fed4e52e6d1] (2026-10-31T04:16:47Z)
- (audit intent) `self + one fm-reviewer pass (6 findings, all fixed: trigger words, improve description, security-review safety lines, separate rules pairs, review.js whenToUse, per-skill cap); spot-checked every playbook path and verb the new skills name exists` → four job skills chosen from the ledger's stage words, each 'Use whenever', wins its own plain request in the trigger fixtures; listing 2184/2200 chars (test_docs, test_which green) [tree 9fed4e52e6d1] (2026-10-31T04:16:47Z)
- (audit adversary) `self + one fm-reviewer pass (6 findings, all fixed: trigger words, improve description, security-review safety lines, separate rules pairs, review.js whenToUse, per-skill cap); spot-checked every playbook path and verb the new skills name exists` → security-review says proofs are local tests only, no live systems, no running untrusted code, never loosen the guard (rule changes via fm ask core), synthetic secrets only; the guard eval prompts changed only by the synced rules line (four new plain-word pairs), no guard text touched [tree 9fed4e52e6d1] (2026-10-31T04:16:47Z)
- (audit edge) `self + one fm-reviewer pass (6 findings, all fixed: trigger words, improve description, security-review safety lines, separate rules pairs, review.js whenToUse, per-skill cap); spot-checked every playbook path and verb the new skills name exists` → 'debug this' no longer ties with library; 'which sorting library' doesn't hit security-review; per-skill cap 125 chars [tree 9fed4e52e6d1] (2026-10-31T04:16:47Z)
- (audit maintainer) `self + one fm-reviewer pass (6 findings, all fixed: trigger words, improve description, security-review safety lines, separate rules pairs, review.js whenToUse, per-skill cap); spot-checked every playbook path and verb the new skills name exists` → stage routes name the job skill first and keep the playbooks name for fm playbooks route [tree 9fed4e52e6d1] (2026-10-31T04:16:47Z)
## Log
- 2026-10-30T00:50:57Z created
- 2026-10-30T00:51:38Z steer: skills aren't loaded until needed, but they must actually be used/available (lazy: no listing cost per skill; a router or prompt-matched hint brings the right one)
- 2026-10-31T03:32:08Z set type=FEATURE, tier=M
- 2026-10-31T03:32:08Z planned: it has criteria and steps
- 2026-10-31T03:32:09Z set approved=True
- 2026-10-31T03:32:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2072.builder.md
- 2026-10-31T03:32:29Z focused
- 2026-10-31T03:40:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a992b49f2d0ee577d; dropped: the builder's worktree never finished creating; moved aside, pruned
- 2026-10-31T03:40:56Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2072.builder.md
- 2026-10-31T03:41:21Z focused
- 2026-10-31T04:14:58Z merged worktree-agent-a57f6b8442dad500a (30 file(s))
- 2026-10-31T04:14:59Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a57f6b8442dad500a
- 2026-10-31T04:14:59Z focused
- 2026-10-31T04:15:59Z scope: plugin/skills/{security-review,performance,refactor,docs}/SKILL.md (new), 15 skill descriptions trimmed, plugin/rules/foreman.md, plugin/lib/fmcore.py (stage routes), plugin/evals/*/prompt.md (synced rules), plugin/workflows/{ideas,review}.js, plugin/tests/{test_docs.py,fixtures/skill_triggers.json}, MASTER.md, CHANGELOG.md; README has no skills list (step 4's README part: none)
- 2026-10-31T04:17:12Z done
- 2026-10-31T04:17:14Z committed 634388b4 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- T-1697 [FEATURE M, done, 3 steps] Hooks name the Foreman skill to load: Next lines and stage notes say which skill (or playbook) fits, within the prompt budget — lesson:…
- playbook Living Docs Governance (fm playbooks show context/living-docs)
- decision 2026-10-28: T-1803 step 3: the next-step hint does not name the top routed book
- the similar finished task took 3 steps
## Lessons
- A skill listing has a fixed character budget: each new description costs words taken from older ones, so trigger fixtures must cover the old skills too
## Files touched
- plugin/tests/test_docs.py
- plugin/tests/fixtures/skill_triggers.json
- plugin/skills/refactor/SKILL.md
- plugin/skills/performance/SKILL.md
- plugin/skills/security-review/SKILL.md
- plugin/skills/docs/SKILL.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/improve/SKILL.md
- plugin/skills/library/SKILL.md
- plugin/skills/resume/SKILL.md
- plugin/skills/next/SKILL.md
- plugin/skills/intake/SKILL.md
- plugin/skills/research/SKILL.md
- plugin/skills/release/SKILL.md
- plugin/skills/debug-test/SKILL.md
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/ui-design/SKILL.md
- plugin/workflows/review.js
- plugin/workflows/ideas.js
- plugin/skills/reflect/SKILL.md
- plugin/skills/directions/SKILL.md
- plugin/skills/status/SKILL.md
- plugin/lib/fmcore.py
- plugin/rules/foreman.md
- MASTER.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
