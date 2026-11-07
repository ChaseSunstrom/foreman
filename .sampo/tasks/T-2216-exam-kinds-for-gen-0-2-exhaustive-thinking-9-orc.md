---
id: T-2216
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T21:15:59Z
updated: 2026-10-30T22:21:09Z
base: c3be730de7735536bae694506dc0d5a0fc09420a
base_tree: 35a4cec706b0ff50c05e00841294c6a21f58a0ba
plan0_at: 2026-10-30T21:56:35Z
plan0_scope: []
verified: strong
---
# Exam kinds for gen-0 #2 Exhaustive thinking, #9 Orchestration and #11 Self-triggering,…
## Raw request
> Exam kinds for gen-0 #2 Exhaustive thinking, #9 Orchestration and #11 Self-triggering, which the scorecard shows as 'no exam kind' so DONE-WHEN can never be met: a scenario shape fm exam can grade for each (a request with several readings and approaches that must be listed; a multi-part request whose parts belong on lanes with the cheapest model; work that needs a schedule or watcher queued for one yes), child-authorable, and KIND_WORDS so the capability maps to it
## Interpretation
Three gen-0 §2 capabilities have no exam kind, so the scorecard can't pass them and DONE-WHEN is unreachable. Each needs a held-out scenario fm exam can grade from the repo and the answer alone: #2 'exists' (the request asks for something the module already does: a good answer names the existing function and adds no duplicate; scored by a reading and a static never-check on a duplicate), #9 'parts' (three independent defects in three files, request names all three: all fixed and each part's finding names its file; the session arm records lanes/subagents used and cost, scored per part), #11 'trigger' (a request to re-run the checks on a schedule or on change: a good answer writes a trigger spec in the repo — a CI schedule or watcher config — and claims done only with it queued, never installed; scored statically). Each child-authorable via SHAPED, and KIND_WORDS maps the capability lines to them.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen renders exists, parts and trigger scenarios (template and child) that pass fm exam check; the oracle closes each and empty closes none — verify with `python3 plugin/tests/run.py test_exam`
- [x] the scorecard maps gen-0 #2, #9 and #11 to exists, parts and trigger (no capability reads 'no exam kind') — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Options: (A) three new KINDS graded by existing machinery (readings, static must/never checks, run checks), each with a template render and a SHAPED child reply. (B) grade orchestration and exhaustiveness from session transcripts (tool calls, Agent spawns): richer, but only session arms have transcripts and it grades process, not outcome. (C) map #2/#9/#11 to existing kinds (ambiguous, none, clean): fast, but they don't test the capability. Choice A, with B's transcript signal recorded as a note on session lines for #9 (not scored) so the end-of-run exam can read it.
## Risks and rollback
A trigger kind could tempt an arm to install a timer: the scenario's done_ok requires it queued only, and the guard already blocks installs. Rollback: remove the kinds from KINDS; old runs keep their keys.
## Execution prompt
## Steps
1. [x] red: render/check/oracle/empty per kind; KIND_WORDS mapping
2. [x] exists kind
3. [x] parts kind
4. [x] trigger kind
5. [x] child shapes for the three
6. [x] docs: MASTER, CHANGELOG, site exam text
## Resume here
<!-- auto -->
- 2026-10-30T22:08:37Z steps 6/6 done
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, site/genesis/index.html
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2216_test.edit, plugin/tests/test_genesis.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2216_code.edit, plugin/lib/fmgenesis.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2216_child_test.edit, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2216_child_code.edit, plugin/lib/fmexam.py, plugin/tests/test_exam.py, CHANGELOG.md, MASTER.md, site/genesis/index.html
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md ~/.claude/foreman/site/genesis/index.html
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamGen.test_exists_parts_and_trigger_scenarios_render_check_and_grade test_genesis.GenesisDraft.test_exhaustive_thinking_orchestration_and_self_triggering_have_exam_kinds` → red as expected (exit 1) · Ran 2 tests in 0.4s (2 classes, 16 at a time; slowest: ExamGen 0s, GenesisDraft 0s) / FAILED (2 classes) [ran] [tree 4c4480834de4] (2026-10-30T21:57:37Z)
- (step 2) `python3 plugin/tests/run.py test_exam.ExamGen.test_exists_parts_and_trigger_scenarios_render_check_and_grade test_genesis.GenesisDraft.test_exhaustive_thinking_orchestration_and_self_triggering_have_exam_kinds` → exit 0 · Ran 2 tests in 21.0s (2 classes, 16 at a time; slowest: ExamGen 21s, GenesisDraft 0s) / OK [ran] [tree 687ba354ef6a] (2026-10-30T22:00:48Z)
- (step 3) `python3 plugin/tests/run.py test_exam.ExamGen.test_exists_parts_and_trigger_scenarios_render_check_and_grade test_genesis.GenesisDraft.test_exhaustive_thinking_orchestration_and_self_triggering_have_exam_kinds` → exit 0 · Ran 2 tests in 21.0s (2 classes, 16 at a time; slowest: ExamGen 21s, GenesisDraft 0s) / OK [ran] [tree 687ba354ef6a] (2026-10-30T22:01:09Z)
- (step 4) `python3 plugin/tests/run.py test_exam.ExamGen.test_exists_parts_and_trigger_scenarios_render_check_and_grade test_genesis.GenesisDraft.test_exhaustive_thinking_orchestration_and_self_triggering_have_exam_kinds` → exit 0 · Ran 2 tests in 21.0s (2 classes, 16 at a time; slowest: ExamGen 21s, GenesisDraft 0s) / OK [ran] [tree 687ba354ef6a] (2026-10-30T22:01:31Z)
- (step 5) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 14 tests in 60.7s (1 classes, 16 at a time; slowest: ExamAuthors 60s) / OK [ran] [tree a726f67fc293] (2026-10-30T22:05:05Z)
- (step 6) `python3 plugin/tests/run.py test_docs test_site` → exit 0 · Ran 107 tests in 8.4s (32 classes, 16 at a time; slowest: Fences 8s, Header 5s, Landing 2s) / OK [ran] [tree a726f67fc293] (2026-10-30T22:05:14Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 36 tests in 68.2s (10 classes, 16 at a time; slowest: ExamAuthors 68s, ExamGen 44s, ExamRust 16s) / OK [ran] [tree a726f67fc293] (2026-10-30T22:06:28Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 96 tests in 6.2s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree a726f67fc293] (2026-10-30T22:06:35Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 36 tests in 67.6s (10 classes, 16 at a time; slowest: ExamAuthors 67s, ExamGen 55s, ExamRust 16s) / OK [ran] [tree 3d61c2143187] (2026-10-30T22:16:33Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 96 tests in 6.2s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisLive 4s, GenesisSweep 4s) / OK [ran] [tree 3d61c2143187] (2026-10-30T22:16:39Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 36 tests in 68.0s (10 classes, 16 at a time; slowest: ExamAuthors 68s, ExamGen 54s, ExamRust 16s) / OK [ran] [tree 3d61c2143187] (2026-10-30T22:19:49Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 96 tests in 6.2s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree 3d61c2143187] (2026-10-30T22:19:49Z)
- `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 132 tests in 67.3s (23 classes, 16 at a time; slowest: ExamAuthors 67s, ExamGen 53s, ExamRust 16s) / OK [ran] [tree 3d61c2143187] (2026-10-30T22:19:49Z)
- (audit intent) `one foreman:fm-reviewer pass over six lenses (research/T-2216-review.md): 1 HIGH + 5 MEDIUM + 1 LOW fixed test-first (duplicate check for exists, trigger files only, anchored kind words, proxy note for #9, findings matching, safe static scan), 2 LOW accepted` → #2, #9 and #11 now have exam kinds; exists fails an answer that adds a copy, and #9's row says its kind is a proxy [tree 3d61c2143187] (2026-10-30T22:19:49Z)
- (audit adversary) `one foreman:fm-reviewer pass over six lenses (research/T-2216-review.md): 1 HIGH + 5 MEDIUM + 1 LOW fixed test-first (duplicate check for exists, trigger files only, anchored kind words, proxy note for #9, findings matching, safe static scan), 2 LOW accepted` → a trigger counts only in a CI workflow, timer, service or crontab that schedules a test command [tree 3d61c2143187] (2026-10-30T22:19:49Z)
- (audit edge) `one foreman:fm-reviewer pass over six lenses (research/T-2216-review.md): 1 HIGH + 5 MEDIUM + 1 LOW fixed test-first (duplicate check for exists, trigger files only, anchored kind words, proxy note for #9, findings matching, safe static scan), 2 LOW accepted` → the static scan skips links, FIFOs and virtualenvs [tree 3d61c2143187] (2026-10-30T22:19:49Z)
- (audit operator) `one foreman:fm-reviewer pass over six lenses (research/T-2216-review.md): 1 HIGH + 5 MEDIUM + 1 LOW fixed test-first (duplicate check for exists, trigger files only, anchored kind words, proxy note for #9, findings matching, safe static scan), 2 LOW accepted` → a default fm exam gen renders 18 kinds, about a fifth more [tree 3d61c2143187] (2026-10-30T22:19:49Z)
- (audit maintainer) `one foreman:fm-reviewer pass over six lenses (research/T-2216-review.md): 1 HIGH + 5 MEDIUM + 1 LOW fixed test-first (duplicate check for exists, trigger files only, anchored kind words, proxy note for #9, findings matching, safe static scan), 2 LOW accepted` → capability words are anchored and tested on gen-0's own lines and user-style lines [tree 3d61c2143187] (2026-10-30T22:19:49Z)
- (audit design) `one foreman:fm-reviewer pass over six lenses (research/T-2216-review.md): 1 HIGH + 5 MEDIUM + 1 LOW fixed test-first (duplicate check for exists, trigger files only, anchored kind words, proxy note for #9, findings matching, safe static scan), 2 LOW accepted` → the site's exam text lists the new kinds [tree 3d61c2143187] (2026-10-30T22:19:49Z)
## Log
- 2026-10-30T21:15:59Z created
- 2026-10-30T21:18:52Z planned: it has criteria and steps
- 2026-10-30T21:18:54Z set approved=True
- 2026-10-30T21:18:54Z approved on the user's yes 2026-10-30: 'I approve all changes btw, you don't need to ask for my approval'
- 2026-10-30T21:56:34Z focused
- 2026-10-30T22:06:35Z scope: fmexam (KINDS, REQUESTS, TEXTS, TRIGGER, NIGHTLY, VARIANT/DEFECTS, _write subdirs, _template trigger, _static any, readings, SHAPED exists/trigger/parts, _author_shaped, _shaped), fmgenesis KIND_WORDS, tests, MASTER/CHANGELOG/site
- 2026-10-30T22:21:07Z done
- 2026-10-30T22:21:09Z committed 808e2aa0 (7 files)
## Follow-ups captured
## Build vs reuse
Reuses fmexam's KINDS/REQUESTS/render/_template, the static and run check types, readings/missing grading, SHAPED/_author_shaped for child replies, and fmgenesis KIND_WORDS/_kinds for the capability map.
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- research T-2126-review: Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which…
- decision 2026-10-30: The Genesis line and the exam_scorecard MCP tool show the held-out scorecard to sessions: aggregate N/M pass on the shared line, per-capability coun…
- the similar finished task took 4 steps
## Why not caught
the first tests only fed the oracle's clean answer; no answer added a copy or wrote a schedule into the README
## Lessons
- An exam kind must test the capability, not a phrase: check the behaviour a lazy answer would get wrong (a copy added, a schedule written in prose), and where the grader can't see the capability, say proxy on the row instead of letting it pass silently
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- site/genesis/index.html
