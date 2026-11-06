---
id: T-3292
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/recipe.py, plugin/tests/test_recipe.py, plugin/lib/sampo/lanes.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:35:52Z
updated: 2026-11-06T02:36:11Z
builder: 2026-11-06T02:36:11Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
---
# Moon C-006005: a builder brief cites a recipe from the nearest closed task (files touched, each step with the command that passed it, its lesson)
## Raw request
> Moon C-006005: a builder brief cites a recipe from the nearest closed task (files touched, each step with the command that passed it, its lesson)
## Interpretation
Reading 1 (chosen): a closed Sampo task is the recorded session; recipe.py turns it into a replayable recipe (files touched, each step with its passing evidence command, lesson) and builder_brief cites the nearest one so a lane starts from how a similar change was made. Reading 2 (ruled out): recording raw agent transcripts for video-like replay, because transcripts are large, unstructured and already in state/agent-sessions; the structured task already holds what a builder needs. Exists: fm recall ranks past briefs and lessons (recall.py:192) and Files touched is stored at close (cli.py:937), but no builder brief cites a precedent (lanes.py:1736 builds sections from the task alone). Partial: recall exists, this adds the recipe and the brief registration.
## Assumptions (confidence)
## Acceptance criteria
- [ ] recipe.recipe(b) renders a closed task as steps with their passing evidence commands, files touched and lesson, and omits failed or typed-only runs — verify with `python3 plugin/tests/run.py test_recipe`
- [ ] recipe.nearest(p, b) picks the closest closed task of the same type by word overlap and returns None below a floor — verify with `python3 plugin/tests/run.py test_recipe`
- [ ] sampo lane brief output file holds a Precedent recipe section when a close match exists and none otherwise — verify with `python3 plugin/tests/run.py test_recipe`
## Non-goals
## Approach (options → choice → why)
1. New recipe.py with nearest (Jaccard over recall._tokens of title plus Interpretation, same type, closed, floor 0.25) and recipe (render), one call from lanes.builder_brief. Likely outcome: small diff, one lane-file line, parallel lanes safe.
2. Reuse recall.recall() ranking (BM25) and render its top hit. Likely outcome: heavier, ranks decisions and playbooks too, needs filtering to done briefs; slower per brief.
3. Add a sampo recipe CLI verb as well. fails if: it touches cli.py, a big hot file, and collides with other lanes.
4. Do less: only cite the nearest task id and title in the brief. Likely outcome: little value, the builder still has to dig.

Choice 1 (85%): isolated module, stdlib only, one small registration. Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests for recipe() and nearest() in plugin/tests/test_recipe.py  <- CURRENT
2. [ ] plugin/lib/sampo/recipe.py: nearest via recall._tokens Jaccard, recipe via Steps, evidence, Files touched, Lessons
3. [ ] register in lanes.builder_brief as a Precedent section (capped 1500 chars) and CHANGELOG
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T02:35:52Z created
- 2026-11-06T02:36:06Z set scope=['plugin/lib/sampo/recipe.py', 'plugin/tests/test_recipe.py', 'plugin/lib/sampo/lanes.py', 'CHANGELOG.md']
- 2026-11-06T02:36:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3292.builder.md
## Follow-ups captured
