---
id: T-2215
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T21:00:44Z
updated: 2026-10-30T22:44:41Z
base: f2447e58ca72dcf528c603088a90a68fb2ba1aa3
base_tree: b781ff25fcda128c639f002c54bd3aac42a7046f
plan0_at: 2026-10-30T22:26:21Z
plan0_scope: []
verified: strong
---
# fm genesis spec --author child: #13's G-line/G-none/G-sweep/G-tower projects rendered…
## Raw request
> fm genesis spec --author child: #13's G-line/G-none/G-sweep/G-tower projects rendered from child-authored fm exam gen scenarios, with answered.child on draft-genesis lines, so #13 can leave 'no outside author' (T-2204 review)
## Interpretation
#13 (Genesis as a feature) reads 'no outside author' because fm genesis exam's G-scenarios are all Foreman's: the project's planted defect comes from fmexam's template and G-line's planted MUST/NEVER lines from a fixed pool of three each, both memorizable. fm genesis exam --author child makes each G-scenario's project defect child-planted (fmexam's child author for that defect kind) and G-line's MUST/NEVER lines child-written; draft lines carry answered.child, and the scorecard counts them for #13.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis exam --author child renders G-scenarios whose project defect and G-line MUST/NEVER lines a child wrote, graded as before, and its lines carry answered.child — verify with `python3 plugin/tests/run.py test_genesis`
- [x] the scorecard counts #13's child-authored draft results and stops reading 'no outside author' for it — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Options: (A) reuse fmexam's per-kind child authors to plant each G project's defect (render(tmp, s, plant)) and add one small prompt for G-line's MUST/NEVER pair (validated: the prefix, length, not a PLANT line, not in the README already); (B) a child writes the whole project (unbounded, hard to validate); (C) leave #13 to the long-horizon tier only (then #13 can never pass the held-out exam DONE-WHEN names). Choice A: same gate (the checklist and the planted lines decide), outside-authored inputs.
## Risks and rollback
A child MUST/NEVER line a draft can't reasonably infer from the project makes every arm miss it: the line must name something the README or code shows. Rollback: --author self stays the default.
## Execution prompt
## Steps
1. [x] red: child G-scenarios with a stub child; scorecard row for #13
2. [x] fm genesis exam --author child: child plants and G-line lines
3. [x] scorecard: draft-genesis outside authors
4. [x] docs: MASTER, CHANGELOG, site
## Resume here
<!-- auto -->
- 2026-10-30T22:32:23Z steps 4/4 done
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, site/genesis/index.html
- touched since last checkpoint: plugin/lib/fmexam.py, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, CHANGELOG.md, MASTER.md, site/genesis/index.html
## Docs impact
MASTER.md, CHANGELOG.md, site/genesis/index.html
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisExam test_genesis.GenesisDraft` → red as expected (exit 1) · Ran 23 tests in 3.1s (2 classes, 16 at a time; slowest: GenesisDraft 3s, GenesisExam 2s) / FAILED (2 classes) [ran] [tree 7f8bfd8f9bef] (2026-10-30T22:26:25Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisExam test_genesis.GenesisDraft` → exit 0 · Ran 23 tests in 3.3s (2 classes, 16 at a time; slowest: GenesisDraft 3s, GenesisExam 2s) / OK [ran] [tree 393a17eef78b] (2026-10-30T22:29:06Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 133 tests in 68.6s (23 classes, 16 at a time; slowest: ExamAuthors 68s, ExamGen 53s, ExamRust 17s) / OK [ran] [tree 393a17eef78b] (2026-10-30T22:30:15Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_site` → exit 0 · Ran 107 tests in 8.3s (32 classes, 16 at a time; slowest: Fences 8s, Header 5s, Landing 2s) / OK [ran] [tree 393a17eef78b] (2026-10-30T22:30:24Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_site` → exit 0 · Ran 107 tests in 8.3s (32 classes, 16 at a time; slowest: Fences 8s, Header 5s, Landing 2s) / OK [ran] [tree 0fa3188f9414] (2026-10-30T22:30:47Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GenesisExam test_genesis.GenesisDraft` → exit 0 · Ran 23 tests in 3.3s (2 classes, 16 at a time; slowest: GenesisDraft 3s, GenesisExam 2s) / OK [ran] [tree 0fa3188f9414] (2026-10-30T22:30:58Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 97 tests in 6.3s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree 0fa3188f9414] (2026-10-30T22:31:04Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisExam test_genesis.GenesisDraft` → red as expected (exit 1) · Ran 24 tests in 3.3s (2 classes, 16 at a time; slowest: GenesisDraft 3s, GenesisExam 3s) / FAILED (1 classes) [ran] [tree dbc0ab45d69f] (2026-10-30T22:38:14Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisExam test_genesis.GenesisDraft` → exit 0 · Ran 24 tests in 3.2s (2 classes, 16 at a time; slowest: GenesisDraft 3s, GenesisExam 3s) / OK [ran] [tree 8bfee743fb63] (2026-10-30T22:38:27Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 98 tests in 6.1s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree 3c921f6666e7] (2026-10-30T22:39:54Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 98 tests in 6.1s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree 3c921f6666e7] (2026-10-30T22:39:54Z)
- (audit intent) `one fm-reviewer five-lens pass (research/T-2215-review.md); 4 fixed test-first, 1 captured (T-2225)` → child plant reached no grade; now the child writes the README and G-line lines the drafts read [tree 3c921f6666e7] (2026-10-30T22:39:54Z)
- (audit edge) `one fm-reviewer five-lens pass (research/T-2215-review.md); 4 fixed test-first, 1 captured (T-2225)` → cached per run/scenario so arms grade the same input; failed child keeps the template whole [tree 3c921f6666e7] (2026-10-30T22:39:54Z)
- (audit adversary) `one fm-reviewer five-lens pass (research/T-2215-review.md); 4 fixed test-first, 1 captured (T-2225)` → none; lines c.plain'd, README via facts' defang/redact, cache re-vetted on load [tree 3c921f6666e7] (2026-10-30T22:39:54Z)
- (audit operator) `one fm-reviewer five-lens pass (research/T-2215-review.md); 4 fixed test-first, 1 captured (T-2225)` → spend under the project, model stamped, child count in r and summary [tree 3c921f6666e7] (2026-10-30T22:39:54Z)
- (audit maintainer) `one fm-reviewer five-lens pass (research/T-2215-review.md); 4 fixed test-first, 1 captured (T-2225)` → fallback and cross-arm reuse tested [tree 3c921f6666e7] (2026-10-30T22:39:54Z)
## Log
- 2026-10-30T21:00:44Z created
- 2026-10-30T22:21:16Z planned: it has criteria and steps
- 2026-10-30T22:21:17Z set approved=True
- 2026-10-30T22:21:17Z approved on the user's yes 2026-10-30: 'I approve all changes btw, you don't need to ask for my approval'
- 2026-10-30T22:26:20Z focused
- 2026-10-30T22:31:04Z scope: fmgenesis (exam author/model/langs, LINES, _child_lines, scorecard draft-genesis outside), fmexam.child (factored out of _authored), fmcli genesis --author/--model/--lang, test_genesis, MASTER/CHANGELOG/site
- 2026-10-30T22:38:10Z review: the child's code plant reached no grade (drafts read only README + request); reworked: the child writes the README and G-line's lines, cached per run/scenario so arms grade the same input; spend under project, model stamped, child count in r. G-tower stays fm exam's genesis session arm (not this task's scope).
- 2026-10-30T22:41:11Z done
- 2026-10-30T22:41:13Z committed eec15541 (7 files)
- 2026-10-30T22:41:29Z guard authorization added: publish
- 2026-10-30T22:44:41Z publish grant used by fm ship
## Follow-ups captured
## Build vs reuse
Reuses fmexam's _author/_author_shaped/_author_key dispatch and render(plant), fmideas.run_child, the draft grader (_misses), exam_line's answered dict, and the scorecard's outside-author rule (T-2204).
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2099 [FEATURE M, done, 5 steps] fm genesis draft/spec — gen-0 from a line or nothing; per-project spec with a held-out… — lesson: cover() tag words counted as shared w…
- research T-2126-review: Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which…
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
## Lessons
- An 'outside author' counts only for what the graded arm reads; check the input path before crediting authorship
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- site/genesis/index.html
