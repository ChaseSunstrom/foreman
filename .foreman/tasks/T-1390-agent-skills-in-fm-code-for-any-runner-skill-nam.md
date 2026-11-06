---
id: T-1390
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmlib.py, plugin/tests/test_code_skills.py, CHANGELOG.md, README.md]
depends_on: [T-2742]
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-11-03T01:00:24Z
inferred_deps: [T-1382]
inferred_why: T-1382: named in its request
---
# Agent Skills for any fm code runner: listed in the plan, loaded on demand, scripts through the guard
## Raw request
> FEATURE: Agent Skills in fm code for any runner: skill names and descriptions in the planner prompt, a skill action loads one SKILL.md body (references on demand), scripts/ run only through the guard, a per-model token budget (S3, A16 A1 B3)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a fake non-Claude model that calls the skill action receives the body and the journal records it; an unknown name returns an error; a skill script with a planted curl is refused by the guard
## Interpretation
fm code's planner and worker models other than Claude never see Agent Skills; give every runner the format's progressive disclosure: names and descriptions up front within a token budget, a body on request, references on demand, and scripts only through the guard.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a fake non-Claude model that calls the skill action gets the body inside the envelope and the journal records the load; an unknown name returns an error naming near matches — verify with `cd plugin/tests && python3 -m unittest test_code_skills.Skills.test_load_and_unknown`
- [ ] a skill script with a planted curl is refused by the guard when a step runs it; a ref outside the skill folder is refused — verify with `cd plugin/tests && python3 -m unittest test_code_skills.Skills.test_scripts_and_refs_confined`
- [ ] the listing stays within the model's skill budget and leaves out ideas-only and source-available bodies — verify with `cd plugin/tests && python3 -m unittest test_code_skills.Skills.test_budget_and_classes`
## Non-goals
## Approach (options → choice → why)
Progressive disclosure as the Agent Skills format defines it: the planner prompt lists skill name + description (from the project's installed plugins and T-1389's open-class lib entries; ideas-only and source-available bodies are never loaded), capped by a per-model token budget (the model profile's context, fraction ~5%); a new slot action `skill` with {name} returns that SKILL.md body inside the run's data envelope (T-1394 fence: it is third-party text) and records the load in the journal; `skill` with {name, ref} returns one file under the skill's folder (confined: realpath inside the folder, regular file, size-capped); a skill's scripts/ never run directly — a step that wants one goes through the ordinary command path, so the guard judges it like any command. Options: inline all bodies (blows the budget) → rejected; Claude-only native skills (doesn't serve other runners) → rejected. Unknown name → an error result naming the nearest names.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing tests  <- CURRENT
2. [ ] listing with budget
3. [ ] skill action: body and refs, fenced, journaled
4. [ ] scripts only via the guarded command path
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-22T16:40:12Z planned from capture
- 2026-10-22T16:40:15Z blocked: waits for T-1401's lane (fmcode.py)
- 2026-11-03T00:36:17Z unblocked: their named blockers (T-1214, T-1316, T-1401) closed weeks ago; the blocked-pile line found them (T-2683)
- 2026-11-03T00:46:39Z set depends_on=['T-1476']
- 2026-11-03T01:00:24Z set depends_on=['T-2742']
## Follow-ups captured
