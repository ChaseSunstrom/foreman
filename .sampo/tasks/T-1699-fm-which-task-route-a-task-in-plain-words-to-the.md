---
id: T-1699
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmwhich.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_which.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T22:36:29Z
updated: 2026-10-23T01:47:32Z
base: 3f61cb43e3b14eb7f2805608ddbf8aa264fa7d73
base_tree: 099cc9ad6fc373d4ec7dbbe80bc0a21b908e07fe
plan0_at: 2026-10-22T23:19:59Z
plan0_scope: [plugin/lib/fmwhich.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_which.py, CHANGELOG.md]
group: skills and routing
verified: strong
---
# fm which TASK: route a task in plain words to the Foreman skill, playbooks and fm verbs that fit
## Raw request
> fm which TASK: route a task in plain words to the Foreman skill, playbooks and fm verbs that fit
## Interpretation
With 13 skills, 82 playbooks and ~100 verbs, nobody can know what exists. fm which ranks skill descriptions, playbook headers and verb help against the task words and prints what to load, each with the command that loads it. The hooks mention it once when a request names no skill.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm which "make a 3D hero with motion" lists the design skill and the ui/scene-3d.md and ui/motion.md playbooks with fm playbooks show lines; an unknown task says so — verify with `python3 plugin/tests/run.py test_which`
## Non-goals
## Approach (options → choice → why)
Options: an embedding index (a model, not stdlib); a long index in a skill (context cost); token ranking with fmplaybooks' tokenizer. Choice: token ranking: stdlib, instant, testable.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] index and ranking
3. [x] hook mention
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_which` → ✗ exit 1 · Ran 8 tests in 3.3s (3 classes, 16 at a time; slowest: Which 2s, Snapshots 1s, Extract 0s) / FAILED (1 classes) [ran] [tree 1774875d0f01] (2026-10-22T23:23:01Z)
- (ac 1) `python3 plugin/tests/run.py test_which 2>&1 | tail -30` → ✗ exit 1 · Ran 8 tests in 4.7s (3 classes, 16 at a time; slowest: Which 4s, Snapshots 1s, Extract 0s) / FAILED (1 classes) [ran] [tree d2e0294202ea] (2026-10-22T23:25:20Z)
- (step 2) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 8 tests in 1.2s (3 classes, 16 at a time; slowest: Which 1s, Snapshots 0s, Extract 0s) / OK [ran] [tree a97ce5d25c11] (2026-10-22T23:27:26Z)
- (step 3) `python3 plugin/tests/run.py test_which test_context_tax test_help` → exit 0 · Ran 15 tests in 4.5s (7 classes, 16 at a time; slowest: ContextTax 4s, Which 3s, PromptApprovals 2s) / OK [ran] [tree a97ce5d25c11] (2026-10-22T23:27:31Z)
- (ac 1) `python3 plugin/tests/run.py test_which 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|FAILED" | head` → ✗ exit 1 · Ran 12 tests in 1.5s (3 classes, 16 at a time; slowest: Which 1s, Snapshots 0s, Extract 0s) / FAILED (1 classes) [ran] [tree 1778b2d5e204] (2026-10-22T23:33:58Z)
- (step 2) `python3 plugin/tests/run.py test_which` → ✗ exit 1 · Ran 12 tests in 1.5s (3 classes, 16 at a time; slowest: Which 1s, Snapshots 0s, Extract 0s) / FAILED (1 classes) [ran] [tree 1778b2d5e204] (2026-10-22T23:34:03Z)
- (step 2) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 12 tests in 1.6s (3 classes, 16 at a time; slowest: Which 1s, Snapshots 0s, Extract 0s) / OK [ran] [tree ee341a092722] (2026-10-22T23:35:18Z)
- (ac 1) `python3 plugin/tests/run.py test_which 2>&1 | grep -E "^(FAIL|ERROR):|^OK|FAILED" | head -4` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree c0bd2dac9b00] (2026-10-23T01:38:05Z)
- (step 2) `python3 plugin/tests/run.py test_which test_recall test_help test_context_tax` → exit 0 · Ran 40 tests in 27.7s (14 classes, 16 at a time; slowest: Recall 28s, OtherProjects 7s, Consolidate 4s) / OK [ran] [tree 17e7e55b1f3e] (2026-10-23T01:38:59Z)
- (ac 1) `python3 plugin/tests/run.py test_which test_recall test_help test_context_tax` → exit 0 · Ran 40 tests in 48.8s (14 classes, 16 at a time; slowest: Recall 48s, OtherProjects 23s, Consolidate 15s) / OK [ran] [tree 17e7e55b1f3e] (2026-10-23T01:43:45Z)
- (ac 1) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 12 tests in 3.0s (3 classes, 16 at a time; slowest: Which 3s, Snapshots 1s, Extract 0s) / OK [ran] [tree 17e7e55b1f3e] (2026-10-23T01:43:57Z)
- (audit intent) `fm-reviewer full pass; fixed test-first: half the task's words must match (oauth-login → Nothing matches), playbooks indexed by header only (600 chars), one shared stemmer in fmrecall with doubled-consonant collapse, Foreman-only verbs not offered, vacuous assert fixed; after T-1700 the real-tree check lists foreman:ui-design unconditionally` → fm which TASK lists the skills, playbooks and fm verbs that fit, each with the call that loads it; '3D hero with motion' → ui-design, ui/scene-3d, ui/motion [tree 17e7e55b1f3e] (2026-10-23T01:43:57Z)
- (audit edge) `fm-reviewer full pass; fixed test-first: half the task's words must match (oauth-login → Nothing matches), playbooks indexed by header only (600 chars), one shared stemmer in fmrecall with doubled-consonant collapse, Foreman-only verbs not offered, vacuous assert fixed; after T-1700 the real-tree check lists foreman:ui-design unconditionally` → no fit → 'Nothing matches', exit 1; a common word alone no longer pulls in noise; quoted YAML descriptions shown without quotes [tree 17e7e55b1f3e] (2026-10-23T01:43:57Z)
- (audit adversary) `fm-reviewer full pass; fixed test-first: half the task's words must match (oauth-login → Nothing matches), playbooks indexed by header only (600 chars), one shared stemmer in fmrecall with doubled-consonant collapse, Foreman-only verbs not offered, vacuous assert fixed; after T-1700 the real-tree check lists foreman:ui-design unconditionally` → reads bounded (regular files, 8,000 chars, 600 for headers); echoed task text cleaned; nothing written but the hook's once-a-session marker [tree 17e7e55b1f3e] (2026-10-23T01:43:57Z)
- (audit operator) `fm-reviewer full pass; fixed test-first: half the task's words must match (oauth-login → Nothing matches), playbooks indexed by header only (600 chars), one shared stemmer in fmrecall with doubled-consonant collapse, Foreman-only verbs not offered, vacuous assert fixed; after T-1700 the real-tree check lists foreman:ui-design unconditionally` → the prompt hook mentions fm which once a session for an untagged request naming no skill, only when it fits the 400-char budget [tree 17e7e55b1f3e] (2026-10-23T01:43:57Z)
## Log
- 2026-10-22T22:36:29Z created
- 2026-10-22T22:36:30Z set scope=['plugin/lib/fmwhich.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_which.py', 'CHANGELOG.md']
- 2026-10-22T22:36:32Z from T-1692 (skills hardly used; brainstorm-skills-20261022)
- 2026-10-22T23:19:10Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1699.builder.md
- 2026-10-22T23:19:58Z focused
- 2026-10-23T01:42:44Z merged worktree-agent-a2ea1fbe42a544035 (7 file(s))
- 2026-10-23T01:42:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2ea1fbe42a544035
- 2026-10-23T01:42:52Z focused
- 2026-10-23T01:43:53Z scope: plugin/lib/fmrecall.py (shared words/stem, verb_docs) and MASTER.md — review items
- 2026-10-23T01:47:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- T-1697 [FEATURE M, done, 3 steps] Hooks name the Foreman skill to load: Next lines and stage notes say which skill (or playbook) fits, within the prompt budget — lesson:…
- T-1622 [FEATURE M, planned, 3 steps] fm playbooks route, blame and preview: a playbook per stage, lines to the tasks that wrote them, the checks a load adds
- decision 2026-10-22: Skills fix: make the hooks name the skill and rewrite descriptions in task terms before adding skills; keep the 2,000-character listing cap and free…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmwhich.py, plugin/tests/test_which.py; re-ground the plan against them before editing
## Lessons
- Relative score floors pass noise when the best match is itself noise; require an absolute share of the query to match
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_which.py
- plugin/lib/fmrecall.py
- plugin/lib/fmwhich.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- plugin/README.md
- plugin/evals/playbooks/verify/tdd-workflow.json
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmshot.py
- plugin/skills/playbooks/SKILL.md
- plugin/skills/ui-design/SKILL.md
- plugin/tests/fixtures/skill_triggers.json
- plugin/tests/test_cost.py
- plugin/tests/test_docs.py
- plugin/tests/test_drive_side.py
- plugin/tests/test_fmshot.py
- plugin/tests/test_hooks.py
- plugin/tests/test_playbook_evals.py
