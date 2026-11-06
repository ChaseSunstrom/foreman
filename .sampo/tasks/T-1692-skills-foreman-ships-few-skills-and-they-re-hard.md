---
id: T-1692
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-22T22:26:07Z
updated: 2026-10-23T02:19:33Z
group: skills and routing
base: 5f30c5f91834a2c57ca7760c8b13ddb90fc35489
base_tree: 5622f090d89b075ee92aaa1b18bde0c0a73d2288
plan0_at: 2026-10-23T02:18:45Z
plan0_scope: []
verified: strong
---
# Skills: why Foreman's skills went unused, and the slate that fixes it
## Raw request
> Skills: Foreman ships few skills and they're hardly used: find out why, then super-improve (more skills, better triggering, real use)
## Interpretation
Skills were hardly used because hooks hand the exact fm command each turn, descriptions spoke Foreman jargon, the listing was capped, and playbooks hid behind one skill.
## Assumptions (confidence)
## Acceptance criteria
- [x] the cause is recorded and every slate task (T-1697..T-1705) is done — verify with `fm task show T-1705`
## Non-goals
## Approach (options → choice → why)
Hooks name the skill to load; task-worded descriptions with a lint and a trigger eval; listing room freed; four job skills; fm which; honest usage counts with a doctor warning.
## Risks and rollback
## Execution prompt
## Steps
1. [x] diagnose with fm usage data
2. [x] slate T-1697..T-1705 built and merged
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/bin/fm usage --days 1` → exit 0 · named, not loaded: directions ×1 / Next followed: 2 of 9; most often not: fm friction ×2, fm focus ×2, fm task audit ×1 [ran] [tree 5622f090d89b] (2026-10-23T02:18:47Z)
- (step 2) `python3 plugin/bin/fm usage --days 1` → exit 0 · named, not loaded: directions ×1 / Next followed: 2 of 9; most often not: fm friction ×2, fm focus ×2, fm task audit ×1 [ran] [tree 5622f090d89b] (2026-10-23T02:18:48Z)
- (ac 1) `fm task show T-1705` → exit 0 · - plugin/skills/status/SKILL.md / - plugin/tests/test_doctor.py [ran] [tree 5622f090d89b] (2026-10-23T02:18:49Z)
- (ac 1) `fm task show T-1705` → exit 0 · - plugin/skills/status/SKILL.md / - plugin/tests/test_doctor.py [ran] [tree 46a9a0b16098] (2026-10-23T02:19:01Z)
- (audit intent) `self: every slate task closed with its own review; the cause and the built slate are in the Decision` → the user asked why skills were few and unused and to super-improve them: the cause is answered with fm usage data and nine tasks built, reviewed and merged [tree 46a9a0b16098] (2026-10-23T02:19:01Z)
- (audit operator) `self: every slate task closed with its own review; the cause and the built slate are in the Decision` → fm usage already shows named-not-loaded (directions ×1 today), so the next audit can tell offered-and-ignored from never-offered [tree 46a9a0b16098] (2026-10-23T02:19:01Z)
## Log
- 2026-10-22T22:26:07Z created
- 2026-10-23T02:18:35Z planned from capture
- 2026-10-23T02:18:44Z focused
- 2026-10-23T02:19:33Z done
## Follow-ups captured
## Decision
Cause: hooks handed Claude the exact fm command each turn, so it never loaded the skill describing the step; descriptions used Foreman jargon or user words a long autonomous run never contains; the listing cap kept the count low; 82 playbooks hid behind one skill. Built: hooks name the skill to load once a session (T-1697); task-worded descriptions with a doctor lint (T-1698) and a static trigger eval (T-1704); tidy/doctor made user-only to free listing room (T-1705) and the cap raised to 2,200 (decision); job skills ui-design, debug-test, release and research (T-1700, T-1701), loaded by the design/UI, FIX and RESEARCH hints; fm which routes a task in plain words (T-1699); fm usage counts named-not-loaded skills (T-1702) and doctor warns on them (T-1703).
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- research mission-20261022-172631: Request: I also know there arent a lot of skills with foreman? and they are also hardly used? why? super improve!!!
- decision 2026-10-22: Skills fix: make the hooks name the skill and rewrite descriptions in task terms before adding skills; keep the 2,000-character listing cap and free…
- research mission-20261022-172631.pack: I also know there arent a lot of skills with foreman? and they are also hardly used? why? super improve!!!
## Lessons
- Hooks that hand the exact command make skills invisible; name the skill in the hint instead
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmdesign.py
- plugin/tests/fixtures/design-surfaces/DESIGN.md
- plugin/tests/test_design_surfaces.py
