---
id: T-2267
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T04:35:15Z
updated: 2026-10-31T04:40:58Z
base: 6e2e80616eb49075972285f206ee8c87fbb150b9
base_tree: d2839a4036d0be81a15b353d3b872311f2ab9272
plan0_at: 2026-10-31T04:37:39Z
plan0_scope: []
verified: strong
---
# fm task finish for a lane-merged task runs the always-on budget checks (test_doctor…
## Raw request
> fm task finish for a lane-merged task runs the always-on budget checks (test_doctor footprint, test_playbook_use cap, test_docs listing) when its diff touches rules, skills, agents or commands: T-2072 merged green on its own tests and broke ship63 on budgets in other modules (T-2266)
## Interpretation
T-2072 merged green on its own tests and broke ship63 on budget tests in other modules: the project map links a test to a folder it names only at the top level (T-2086), and in this repo every folder sits under plugin/, so test_doctor naming "rules" and test_playbook_use naming "skills" link nothing, and neither fm impact nor the close's linked tests ran them.
## Assumptions (confidence)
## Acceptance criteria
- [x] a test that names a folder beside its own (plugin/tests/test_x.py naming "skills" or "rules") is linked to plugin/skills/ or plugin/rules/ when that folder is mostly non-code, so fm impact and the close's linked tests include it; a mostly-code sibling (plugin/lib) links by file name only — verify with `python3 plugin/tests/run.py test_map`
## Non-goals
## Approach (options → choice → why)
1) _folders also links folders beside the test's own folder (plugin/skills beside plugin/tests) that the test names, when their files are mostly non-code (measured from the file list, no hardcoded names): skills, rules, agents, commands get linked; plugin/lib (109 of 115 code) links by file name as before, so a lib edit doesn't pull in 52 tests. 2) run the whole suite at every lane merge — rejected: 3 minutes per merge, and ship already does it. 3) a hardcoded budget-test list — rejected (learn from data). Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_map, then fmmap._folders links non-code sibling folders
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_map` → ✗ exit 1 · Ran 8 tests in 2.734s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 62d295c70b2e] (2026-10-31T04:39:20Z)
- `cd plugin/tests && python3 -m unittest -q test_map` → exit 0 · Ran 8 tests in 2.716s / OK [ran] [tree 62d295c70b2e] (2026-10-31T04:39:20Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_map test_docs test_playbook_use test_doctor` → exit 0 · Ran 138 tests in 22.485s / OK [ran] [tree 62d295c70b2e] (2026-10-31T04:39:42Z)
- (ac 1) `python3 plugin/tests/run.py test_map` → exit 0 · Ran 10 tests in 6.7s (3 classes, 16 at a time; slowest: Map 6s, Cold 1s, RoundG 1s) / OK [ran] [tree 3c6276226e3c] (2026-10-31T04:40:01Z)
- (audit intent) `self: on the real repo a rules edit now links test_doctor and test_docs, a skill edit links test_playbook_use, test_docs and test_doctor (43 tests), a lib edit still links by name only; map VERSION bumped so cached maps rebuild` → the three budget tests that broke ship63/64 are now linked to the files whose edits break them, learned from the file mix, not a list (test_map red-to-green proven) [tree 3c6276226e3c] (2026-10-31T04:40:01Z)
- (audit edge) `self: on the real repo a rules edit now links test_doctor and test_docs, a skill edit links test_playbook_use, test_docs and test_doctor (43 tests), a lib edit still links by name only; map VERSION bumped so cached maps rebuild` → a test at the top level (tests/x.py) has no sibling folders; the test's own folder is excluded; a folder with equal code and non-code counts doesn't link [tree 3c6276226e3c] (2026-10-31T04:40:01Z)
- (audit operator) `self: on the real repo a rules edit now links test_doctor and test_docs, a skill edit links test_playbook_use, test_docs and test_doctor (43 tests), a lib edit still links by name only; map VERSION bumped so cached maps rebuild` → a skill edit's linked run grows to 43 modules (parallel, under a minute); a lib edit is unchanged [tree 3c6276226e3c] (2026-10-31T04:40:01Z)
- (audit self) `self: on the real repo a rules edit now links test_doctor and test_docs, a skill edit links test_playbook_use, test_docs and test_doctor (43 tests), a lib edit still links by name only; map VERSION bumped so cached maps rebuild` → no findings [tree 3c6276226e3c] (2026-10-31T04:40:01Z)
## Log
- 2026-10-31T04:35:15Z created
- 2026-10-31T04:37:31Z planned: it has criteria and steps
- 2026-10-31T04:37:38Z set tier=S
- 2026-10-31T04:37:39Z focused
- 2026-10-31T04:39:43Z scope: plugin/lib/fmmap.py, plugin/tests/test_map.py, CHANGELOG.md; plus plugin/skills/docs/SKILL.md and plugin/skills/security-review/SKILL.md, T-2266's deletions its commit left unstaged (T-2268)
- 2026-10-31T04:40:23Z done
- 2026-10-31T04:40:25Z committed d6250929 (3 files)
- 2026-10-31T04:40:58Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2266 [FIX S, done, 1 steps] Ship red after T-2072: rules over the 6,400-char always-on budget and a 20-skill count cap the user's 'many more skills' request supersedes…
- T-2086 [FIX S, done, 3 steps] T-2080's close passed its gates but fm ship's scratch-tree run failed…
- T-1785 [FEATURE M, done, 3 steps] Site gallery: every design playbook (references/ui/*.md) has a reproducible example page b — lesson: Files added under skills/playbooks…
- decision 2026-10-30: [revisited: The user's standing intent (on top of every earlier steer] [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pytho…
- similar finished tasks took 1–3 steps
## Lessons
- A folder link heuristic tuned on one repo layout (top-level folders) silently misses a nested one (plugin/*): test the link on the repo it runs in
## Files touched
- plugin/tests/test_map.py
- plugin/lib/fmmap.py
- CHANGELOG.md
