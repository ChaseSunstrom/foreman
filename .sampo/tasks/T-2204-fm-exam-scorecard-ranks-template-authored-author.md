---
id: T-2204
type: FIX
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T19:46:41Z
updated: 2026-10-30T21:03:13Z
base: 78aed46aac462abb71bf1d5354d471b4e21dd26b
base_tree: bc9189184357dd45ed36a6da3b5095f1e9409442
plan0_at: 2026-10-30T20:41:16Z
plan0_scope: []
verified: strong
---
# fm exam scorecard ranks template-authored (--author self) held-out scenarios:…
## Raw request
> fm exam scorecard ranks template-authored (--author self) held-out scenarios: _scorecard's newest() has no author filter, while the exam Mission says self-authored scenarios never rank (their templates are learnable). Count only child-authored held-out scenarios for kinds in fmexam.CHILD_KINDS; decide and say how kinds the child can't author yet are scored
## Interpretation
The capability scorecard (fmgenesis scorecard, the done gate for gen-0's 'every §2 capability passes its held-out exam') counts every held-out scenario, template-authored ones included, though the exam Mission says template scenarios never rank because their templates are learnable. Only 6 of 15 kinds (bug, vuln, none, rank, goal, resume) have an outside (child) author today, so filtering alone leaves the other kinds' capabilities unable to pass; the honest gate needs the filter plus a wider child author.
## Assumptions (confidence)
## Acceptance criteria
- [x] the scorecard counts only child-authored held-out scenarios; a capability with no child-authorable kind shows 'no outside author', never pass — verify with `python3 plugin/tests/run.py test_genesis test_exam`
- [x] fm exam gen --author child authors slow and dep scenarios that pass the exam of the exam (untested, docs, flaky and clean need new scenario shapes: T-2211) — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
Complete version: (a) fm exam grade records each answered scenario's author in the exam line (authors: {id: child|self}); (b) the scorecard counts a held-out scenario only when it is child-authored; older lines without authors count as self; a capability whose kinds have no child author yet shows 'no outside author' (not pass) with the kinds named; (c) widen fmexam.CHILD_KINDS kind by kind (untested, slow, docs, flaky, dep, clean first), each kept only if the exam of the exam passes on the child's plants; (d) scorecard, Genesis line, MCP and site show the new state. Options: weight self-authored scenarios lower (still learnable, still gameable), drop the filter and rely on seeds (Design forbids), hold the scorecard until all kinds have a child (blocks every signal), filter + widen (chosen). Build vs reuse: the child author path (fm exam gen --author child), _scorecard rows, exam.jsonl lines.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: scorecard author filter tests and per-kind child author tests
2. [x] grade records authors; scorecard filters and names 'no outside author'
3. [x] widen CHILD_KINDS kind by kind with exam-of-the-exam checks
4. [x] surfaces (Genesis line, MCP, site) and docs
## Resume here
<!-- auto -->
- 2026-10-30T20:53:50Z steps 4/4 done
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, site/genesis/genesis.js, site/genesis/index.html
- touched since last checkpoint: plugin/tests/test_genesis.py, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, site/genesis/index.html, site/genesis/genesis.js, CHANGELOG.md, MASTER.md
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md ~/.claude/foreman/site/genesis/index.html ~/.claude/foreman/site/genesis/genesis.js
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisDraft.test_the_scorecard_counts_only_an_outside_authors_held_out_scenarios test_exam.ExamAuthors.test_children_author_slow_and_dep_scenarios_too test_exam.ExamGen.test_a_graded_held_out_run_lands_on_the_capability_scorecard` → red as expected (exit 1) · Ran 3 tests in 3.1s (3 classes, 16 at a time; slowest: ExamGen 3s, ExamAuthors 0s, GenesisDraft 0s) / FAILED (3 classes) [ran] [tree 7c151dff10b9] (2026-10-30T20:44:09Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 124 tests in 36.5s (23 classes, 16 at a time; slowest: ExamAuthors 36s, ExamGen 22s, GenesisCheck 13s) / OK [ran] [tree 48b904270dba] (2026-10-30T20:47:49Z)
- (step 3) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 10 tests in 32.6s (1 classes, 16 at a time; slowest: ExamAuthors 32s) / OK [ran] [tree 48b904270dba] (2026-10-30T20:48:56Z)
- (step 4) `python3 plugin/tests/run.py test_site test_site_build test_mcp test_genesis` → exit 0 · Ran 141 tests in 7.4s (32 classes, 16 at a time; slowest: GenesisCheck 7s, GenesisSweep 6s, GenesisLive 5s) / OK [ran] [tree 48b904270dba] (2026-10-30T20:49:04Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 124 tests in 36.5s (23 classes, 16 at a time; slowest: ExamAuthors 36s, ExamGen 21s, GenesisCheck 13s) / OK [ran] [tree 48b904270dba] (2026-10-30T20:49:46Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 31 tests in 36.1s (10 classes, 16 at a time; slowest: ExamAuthors 36s, ExamGen 22s, ExamRust 12s) / OK [ran] [tree 48b904270dba] (2026-10-30T20:50:23Z)
- `python3 plugin/tests/run.py test_genesis test_exam` → ✗ exit 1 · Ran 124 tests in 22.4s (23 classes, 16 at a time; slowest: ExamGen 21s, ExamAuthors 15s, GenesisCheck 13s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 48b904270dba] (2026-10-30T20:51:22Z)
- `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 124 tests in 36.6s (23 classes, 16 at a time; slowest: ExamAuthors 36s, ExamGen 22s, GenesisCheck 13s) / OK [ran] [tree 48b904270dba] (2026-10-30T20:51:22Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 125 tests in 36.4s (23 classes, 16 at a time; slowest: ExamAuthors 36s, ExamGen 21s, GenesisCheck 13s) / OK [ran] [tree 48b50a5bb1a7] (2026-10-30T20:59:31Z)
- (ac 2) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 10 tests in 32.6s (1 classes, 16 at a time; slowest: ExamAuthors 32s) / OK [ran] [tree 48b50a5bb1a7] (2026-10-30T21:00:04Z)
- (step 4) `python3 plugin/tests/run.py test_site test_site_build test_mcp test_genesis test_cli` → exit 0 · Ran 278 tests in 21.0s (70 classes, 16 at a time; slowest: TaskLifecycle 21s, CaptureAndIntake 10s, GenesisCheck 9s) / OK [ran] [tree 48b50a5bb1a7] (2026-10-30T21:00:25Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 125 tests in 36.5s (23 classes, 16 at a time; slowest: ExamAuthors 36s, ExamGen 22s, GenesisCheck 13s) / OK [ran] [tree 48b50a5bb1a7] (2026-10-30T21:02:22Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 31 tests in 36.3s (10 classes, 16 at a time; slowest: ExamAuthors 36s, ExamGen 22s, ExamRust 12s) / OK [ran] [tree 48b50a5bb1a7] (2026-10-30T21:02:22Z)
- (audit intent) `one foreman:fm-reviewer pass over six lenses (research/T-2204-review.md): 4 MEDIUM + 4 LOW fixed test-first (partial state, no erasure by template runs, forged ids ignored, dep prompt, #13 why, docstring/naming, help, site marker), 1 LOW skipped and 3 accepted with reasons` → only outside-authored held-out scenarios decide; a capability partly without an outside author is partial, never pass [tree 48b50a5bb1a7] (2026-10-30T21:02:22Z)
- (audit adversary) `one foreman:fm-reviewer pass over six lenses (research/T-2204-review.md): 4 MEDIUM + 4 LOW fixed test-first (partial state, no erasure by template runs, forged ids ignored, dep prompt, #13 why, docstring/naming, help, site marker), 1 LOW skipped and 3 accepted with reasons` → exam.jsonl is state-direct guarded and child ids of kinds no child writes are ignored [tree 48b50a5bb1a7] (2026-10-30T21:02:22Z)
- (audit edge) `one foreman:fm-reviewer pass over six lenses (research/T-2204-review.md): 4 MEDIUM + 4 LOW fixed test-first (partial state, no erasure by template runs, forged ids ignored, dep prompt, #13 why, docstring/naming, help, site marker), 1 LOW skipped and 3 accepted with reasons` → a later template run never erases a child result; pre-T-2204 lines read as template-written [tree 48b50a5bb1a7] (2026-10-30T21:02:22Z)
- (audit operator) `one foreman:fm-reviewer pass over six lenses (research/T-2204-review.md): 4 MEDIUM + 4 LOW fixed test-first (partial state, no erasure by template runs, forged ids ignored, dep prompt, #13 why, docstring/naming, help, site marker), 1 LOW skipped and 3 accepted with reasons` → about a third more child calls per full gen, off the hot path [tree 48b50a5bb1a7] (2026-10-30T21:02:22Z)
- (audit maintainer) `one foreman:fm-reviewer pass over six lenses (research/T-2204-review.md): 4 MEDIUM + 4 LOW fixed test-first (partial state, no erasure by template runs, forged ids ignored, dep prompt, #13 why, docstring/naming, help, site marker), 1 LOW skipped and 3 accepted with reasons` → one answered.child list, selfmade per row and overall, why per row [tree 48b50a5bb1a7] (2026-10-30T21:02:22Z)
- (audit design) `one foreman:fm-reviewer pass over six lenses (research/T-2204-review.md): 4 MEDIUM + 4 LOW fixed test-first (partial state, no erasure by template runs, forged ids ignored, dep prompt, #13 why, docstring/naming, help, site marker), 1 LOW skipped and 3 accepted with reasons` → the site marks template-written exam rows only when the line names its author [tree 48b50a5bb1a7] (2026-10-30T21:02:22Z)
## Log
- 2026-10-30T19:46:41Z created
- 2026-10-30T19:58:24Z planned: it has criteria and steps
- 2026-10-30T19:58:24Z set approved=True
- 2026-10-30T19:58:24Z approved under the user's standing yes: "I approve all changes btw, you don't need to ask for my approval"
- 2026-10-30T20:41:15Z focused
- 2026-10-30T20:42:09Z criterion 2 text: fm exam gen --author child authors untested, slow, docs, flaky, dep and clean scenarios that pass the exam of the exam → fm exam gen --author child authors slow and dep scenarios that pass the exam of the exam (untested, docs, flaky and clean need new scenario shapes: T-2211)
- 2026-10-30T20:42:10Z scope: slow and dep reuse the bug/vuln plant path (one function and its test); untested, docs, flaky and clean each need a new item shape and C header handling, so they're T-2211
- 2026-10-30T20:51:20Z scope: fmexam (grade's answered.child, CHILD_KINDS slow/dep, scorecard text), fmgenesis (scorecard filter, _exam_count), site/genesis (exam rows marked, page text), MASTER/CHANGELOG, test_exam/test_genesis; decision: answered.child list instead of an authors map (one list, the only thing the scorecard reads)
- 2026-10-30T21:03:11Z done
- 2026-10-30T21:03:13Z committed d9201d33 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- research T-2126-review: Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
- the similar finished task took 5 steps
## Why not caught
the scorecard tests fed hand-built exam lines with no author, so nothing distinguished a template result from an outside one
## Lessons
- A score that decides done must not be computed from scenarios the scored system wrote: tag every result with who authored it, count only outside authors, and make a partly-covered capability say partial instead of passing on the part it has
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- site/genesis/genesis.js
- site/genesis/index.html
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
