---
id: T-2217
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T21:15:59Z
updated: 2026-10-30T22:09:31Z
base: 36a26d0b0a286aa04902ecd1314933c50db07e0b
base_tree: eac7a6485a5af54c373a70139c7e29802d6142ba
plan0_at: 2026-10-30T21:34:53Z
plan0_scope: []
verified: strong
---
# Child-authored vague, ambiguous and missing-tool exam scenarios (the request-shape…
## Raw request
> Child-authored vague, ambiguous and missing-tool exam scenarios (the request-shape kinds): the child writes the request and the readings or missing-tool pattern a good answer names, validated and gated by fm exam check, so #4 and #8 stop reading partial and #5 leaves 'no outside author'
## Interpretation
The request-shape exam kinds (vague, ambiguous, missing-tool) are still written only by Foreman's templates, so #4 and #8 read partial and #5 'no outside author'. A tool-less child writes each: the request in plain words plus the regexes a good answer must match (readings for vague and ambiguous, the missing tool for missing-tool), validated so echoing the request never scores, and gated by fm exam check.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen --author child authors vague, ambiguous and missing-tool scenarios that pass fm exam check; the oracle closes each, and an answer that only repeats the request matches no reading — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
Options: (A) extend SHAPED with three reply shapes: vague {request, readings[2-3]} on the template's slow plant; ambiguous {function, request, readings[2]}; missing-tool {request, missing[1-2], says}, each regex compiled, no quantified group, not matching the request itself, and distinct from the others. (B) let the child also plant the code for vague (a one-function plant plus readings): more authorship but two child calls per scenario. (C) leave them template-written and drop them from the capabilities' Exam lines: shrinks the frame, which the user's steer forbids. Choice A: one call each, the parts the kinds test (reading the request) are outside-authored; vague keeps the template's slow plant, noted as mixed authorship like none.
## Risks and rollback
A reading regex too broad (.*) scores any answer: rejected when it matches the request or another reading. Rollback: drop the three from CHILD_KINDS.
## Execution prompt
## Steps
1. [x] red: stub replies for the three kinds, an echo answer, malformed replies
2. [x] SHAPED vague/ambiguous/missing-tool and their render
3. [x] docs: MASTER, CHANGELOG
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md ~/.claude/foreman/site/genesis/index.html
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamAuthors.test_children_write_the_vague_ambiguous_and_missing_tool_requests` → red as expected (exit 1) · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: ExamAuthors 0s) / FAILED (1 classes) [ran] [tree 49f5de58c061] (2026-10-30T21:35:01Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 129 tests in 62.9s (23 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 22s, GenesisCheck 13s) / OK [ran] [tree 013c3bc68383] (2026-10-30T21:42:03Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_site` → exit 0 · Ran 107 tests in 8.3s (32 classes, 16 at a time; slowest: Fences 8s, Header 5s, Landing 2s) / OK [ran] [tree 013c3bc68383] (2026-10-30T21:42:19Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 34 tests in 63.0s (10 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 22s, ExamRust 12s) / OK [ran] [tree 013c3bc68383] (2026-10-30T21:43:26Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 34 tests in 63.5s (10 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 22s, ExamRust 12s) / OK [ran] [tree 35a4cec706b0] (2026-10-30T21:50:43Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 129 tests in 63.9s (23 classes, 16 at a time; slowest: ExamAuthors 64s, ExamGen 22s, GenesisCheck 13s) / OK [ran] [tree 35a4cec706b0] (2026-10-30T21:51:47Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 34 tests in 63.4s (10 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 22s, ExamRust 12s) / OK [ran] [tree 35a4cec706b0] (2026-10-30T21:54:33Z)
- `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 129 tests in 63.3s (23 classes, 16 at a time; slowest: ExamAuthors 63s, ExamGen 22s, GenesisCheck 13s) / OK [ran] [tree 35a4cec706b0] (2026-10-30T21:54:33Z)
- (audit intent) `one foreman:fm-reviewer pass over six lenses (research/T-2217-review.md): 3 MEDIUM + 6 LOW fixed test-first (example answers for the oracle, regexes refused when the module or a filler answer meets them, vague tied to its slow plant, 2 readings, overflow and ? in the guard, docstring, guard-branch tests)` → every exam kind has an outside author; the oracle closes each child request scenario by saying its example answer; a capability ungraded on some kind is partial [tree 35a4cec706b0] (2026-10-30T21:54:33Z)
- (audit adversary) `one foreman:fm-reviewer pass over six lenses (research/T-2217-review.md): 3 MEDIUM + 6 LOW fixed test-first (example answers for the oracle, regexes refused when the module or a filler answer meets them, vague tied to its slow plant, 2 readings, overflow and ? in the guard, docstring, guard-branch tests)` → a child regex that the module, its tests, README or a filler answer would meet is refused, so no lazy answer scores [tree 35a4cec706b0] (2026-10-30T21:54:33Z)
- (audit edge) `one foreman:fm-reviewer pass over six lenses (research/T-2217-review.md): 3 MEDIUM + 6 LOW fixed test-first (example answers for the oracle, regexes refused when the module or a filler answer meets them, vague tied to its slow plant, 2 readings, overflow and ? in the guard, docstring, guard-branch tests)` → \b, classes and groups in readings no longer break the oracle; overflow at compile is caught [tree 35a4cec706b0] (2026-10-30T21:54:33Z)
- (audit operator) `one foreman:fm-reviewer pass over six lenses (research/T-2217-review.md): 3 MEDIUM + 6 LOW fixed test-first (example answers for the oracle, regexes refused when the module or a filler answer meets them, vague tied to its slow plant, 2 readings, overflow and ? in the guard, docstring, guard-branch tests)` → one child call per scenario [tree 35a4cec706b0] (2026-10-30T21:54:33Z)
- (audit maintainer) `one foreman:fm-reviewer pass over six lenses (research/T-2217-review.md): 3 MEDIUM + 6 LOW fixed test-first (example answers for the oracle, regexes refused when the module or a filler answer meets them, vague tied to its slow plant, 2 readings, overflow and ? in the guard, docstring, guard-branch tests)` → patched CHILD_KINDS in tests say why; the CLI assertions check the real table [tree 35a4cec706b0] (2026-10-30T21:54:33Z)
- (audit design) `one foreman:fm-reviewer pass over six lenses (research/T-2217-review.md): 3 MEDIUM + 6 LOW fixed test-first (example answers for the oracle, regexes refused when the module or a filler answer meets them, vague tied to its slow plant, 2 readings, overflow and ? in the guard, docstring, guard-branch tests)` → the site's exam text lists every kind the outside author writes [tree 35a4cec706b0] (2026-10-30T21:54:33Z)
## Log
- 2026-10-30T21:15:59Z created
- 2026-10-30T21:17:13Z planned: it has criteria and steps
- 2026-10-30T21:17:14Z set approved=True
- 2026-10-30T21:17:14Z approved on the user's yes 2026-10-30: 'I approve all changes btw, you don't need to ask for my approval'
- 2026-10-30T21:34:53Z focused
- 2026-10-30T21:42:19Z scope: fmexam (ASKS, SHAPED request prompts, _guard, _author_shaped, _shaped delegation, render readings/missing), fmgenesis (per-kind partial), test_exam/test_genesis, MASTER/CHANGELOG/site
- 2026-10-30T21:55:48Z done
- 2026-10-30T21:55:50Z committed c3be730d (7 files)
- 2026-10-30T22:06:54Z guard authorization added: publish
- 2026-10-30T22:09:31Z publish grant used by fm ship
## Follow-ups captured
## Build vs reuse
Reuses T-2211's SHAPED/_author_shaped/_regex and _shaped dispatch, render's readings/missing keys and grade's readings_hit/missing_hit, fm exam check as the gate.
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- T-2149 [FEATURE M, done, 1 steps] #4 exam: the child writes the whole contents key (4-6 items, tests and README patterns),… — lesson: A child-written regex is untrusted …
- T-2216 [FEATURE L, planned, 6 steps] Exam kinds for gen-0 #2 Exhaustive thinking, #9 Orchestration and #11 Self-triggering,…
- decision 2026-10-30: [revisited: weakness-finding uses signals] [cites: user steer 2026-10-30] [check: python3 plugin/tests/run.py test_exam.ExamAuthors] Standing rule: …
- the similar finished task took 1 steps
- start here (files T-2149 touched): plugin/tests/test_exam.py, plugin/lib/fmexam.py, CHANGELOG.md, MASTER.md
## Why not caught
the stub's readings were plain alternations, which the old split happened to survive; nothing fed a \b or a class
## Lessons
- A grader must never reverse-engineer an answer from its own pattern: have the author supply an example that the patterns are checked against, and refuse any pattern a lazy or filler answer would meet
## Files touched
- plugin/lib/fmexam.py
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- site/genesis/index.html
