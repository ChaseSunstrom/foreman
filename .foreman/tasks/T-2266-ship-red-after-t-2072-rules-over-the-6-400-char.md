---
id: T-2266
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T04:31:31Z
updated: 2026-10-31T04:35:15Z
base: 08db5b40c56598e32f8bcd9bd015afd5b9ea4728
base_tree: 4839ace78394814b5dc8c6816e3fae23fcf41d19
plan0_at: 2026-10-31T04:31:32Z
plan0_scope: []
verified: strong
---
# Ship red after T-2072: rules over the 6,400-char always-on budget and a 20-skill count cap the user's 'many more skills' request supersedes
## Raw request
> Ship red after T-2072: rules over the 6,400-char always-on budget and a 20-skill count cap the user's 'many more skills' request supersedes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_doctor footprint and test_playbook_use cap pass; the 2,200-char listing test still holds — verify with `python3 plugin/tests/run.py test_doctor test_playbook_use test_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] drop the four plain-word pairs from the rules (skills fire from descriptions and stage routes); count cap → the listing's char budget; resync eval prompts; changelog
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_doctor test_playbook_use test_board_verbs` → ✗ exit 1 · Ran 94 tests in 9.4s (30 classes, 16 at a time; slowest: BoardVerbs 8s, Use 6s, ViewsRepair 6s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree d2839a4036d0] (2026-10-31T04:34:04Z)
- `python3 plugin/tests/run.py test_doctor test_playbook_use test_board_verbs` → exit 0 · Ran 94 tests in 8.5s (30 classes, 16 at a time; slowest: BoardVerbs 8s, ViewsRepair 6s, Use 6s) / OK [ran] [tree d2839a4036d0] (2026-10-31T04:34:04Z)
- (step 1) `python3 plugin/tests/run.py test_doctor test_playbook_use test_docs test_which test_board_verbs` → exit 0 · Ran 193 tests in 9.0s (55 classes, 16 at a time; slowest: BoardVerbs 9s, Fences 8s, Use 6s) / OK [ran] [tree d2839a4036d0] (2026-10-31T04:34:24Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor test_playbook_use test_docs` → exit 0 · Ran 168 tests in 8.6s (51 classes, 16 at a time; slowest: Fences 8s, Use 6s, ViewsRepair 6s) / OK [ran] [tree d2839a4036d0] (2026-10-31T04:34:43Z)
- (audit intent) `self: footprint back under 6,400 rules chars, the skill-count cap replaced by the listing's 2,200-char budget the user named, two skills renamed off their playbooks' names; full ship suite failures were exactly these three classes` → the user asked for many more skills within the listing budget (T-2072), so the binding budget is characters, not a count; the always-on rules budget stays untouched [tree d2839a4036d0] (2026-10-31T04:34:43Z)
- (audit adversary) `self: footprint back under 6,400 rules chars, the skill-count cap replaced by the listing's 2,200-char budget the user named, two skills renamed off their playbooks' names; full ship suite failures were exactly these three classes` → the guard eval prompts changed only by the resynced rules line (four plain-word pairs removed); security-audit's body is byte-identical to the reviewed security-review (local proofs only, never loosen the guard); no guard code touched [tree d2839a4036d0] (2026-10-31T04:34:43Z)
- (audit edge) `self: footprint back under 6,400 rules chars, the skill-count cap replaced by the listing's 2,200-char budget the user named, two skills renamed off their playbooks' names; full ship suite failures were exactly these three classes` → security-review also shadowed Claude Code's built-in /security-review; security-audit and write-docs collide with no playbook stem (test_playbook_use) [tree d2839a4036d0] (2026-10-31T04:34:43Z)
- (audit maintainer) `self: footprint back under 6,400 rules chars, the skill-count cap replaced by the listing's 2,200-char budget the user named, two skills renamed off their playbooks' names; full ship suite failures were exactly these three classes` → the skills still load from their descriptions and the SECURITY/PERFORMANCE/CLEAN stage routes; no plain-word duplicate in the always-on rules [tree d2839a4036d0] (2026-10-31T04:34:43Z)
- (audit self) `self: footprint back under 6,400 rules chars, the skill-count cap replaced by the listing's 2,200-char budget the user named, two skills renamed off their playbooks' names; full ship suite failures were exactly these three classes` → no findings [tree d2839a4036d0] (2026-10-31T04:34:43Z)
## Log
- 2026-10-31T04:31:31Z created
- 2026-10-31T04:31:31Z focused
- 2026-10-31T04:34:24Z scope: plugin/rules/foreman.md, plugin/evals/*/prompt.md (resynced), plugin/tests/test_playbook_use.py, plugin/skills/{security-audit,write-docs}/SKILL.md (renamed from security-review, docs), plugin/lib/fmcore.py (stage route), plugin/tests/{test_docs.py,fixtures/skill_triggers.json}, MASTER.md, CHANGELOG.md
- 2026-10-31T04:35:06Z done
- 2026-10-31T04:35:08Z committed 6e2e8061 (14 files)
- 2026-10-31T04:35:15Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Context Budget (fm playbooks show context/context-budget)
- T-0045 [FEATURE M, done, 0 steps] FIX tasks need red→green proof — a failing then passing recorded run of the same command,
- T-2109 [CLEAN S, done, 1 steps] CLEAN S: friction repeat detector skips SessionStart/UserPromptSubmit…
- decision 2026-10-22: Skill listing cap 2,000 → 2,200 characters for the four job skills (ui-design, debug-test, release, research)
- similar finished tasks took 0–1 steps
- start here (files T-2109 touched): CHANGELOG.md, MASTER.md, plugin/lib/fmfriction.py
## Why not caught
the builder ran test_docs test_which test_cli test_core test_hooks, not test_doctor/test_playbook_use; fm check before merge would have
## Lessons
- A lane's own test run isn't the suite: budget tests live in other modules (test_doctor footprint, test_playbook_use cap), so a lane changing always-on text must run fm check, not only its named tests
## Files touched
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/tests/test_playbook_use.py
- plugin/skills/write-docs/SKILL.md
- plugin/skills/security-audit/SKILL.md
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcore.py
- plugin/tests/fixtures/skill_triggers.json
- plugin/tests/test_docs.py
