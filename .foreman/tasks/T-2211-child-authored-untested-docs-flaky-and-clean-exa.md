---
id: T-2211
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T20:41:17Z
updated: 2026-10-30T21:28:15Z
base: f37ac44ec501e39f395c4edede9f896137b4bde2
base_tree: fa62982d6af2a91de3f3580c28b97e7f7661ad81
plan0_at: 2026-10-30T21:08:59Z
plan0_scope: []
verified: strong
---
# Child-authored untested, docs, flaky and clean exam scenarios: each needs a new item…
## Raw request
> Child-authored untested, docs, flaky and clean exam scenarios: each needs a new item shape (a new function with its test held back; a README line the code contradicts with must/never patterns; a nondeterministic test with its never pattern; a new function and test both present), C needs a header prototype; each passes fm exam check (T-2204 split)
## Interpretation
So every §2 capability can pass on outside-authored scenarios (T-2204 counts only those), the tool-less child must also author untested, docs, flaky and clean scenarios. Each needs its own reply shape, validated, rendered for all six languages where it can be, and passing fm exam check (each hidden check fails on the planted repo and passes on the clean render).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen --author child authors untested, docs, flaky and clean scenarios that pass fm exam check, with the oracle closing each and empty closing only clean — verify with `python3 plugin/tests/run.py test_exam`
- [x] a malformed child reply for each new kind (missing field, a regex that fails to compile or matches both lines, a name that collides) drops that scenario with its reason instead of rendering it — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
Options: (A) one 'extra' function mechanism: the child writes a NEW function and its test (untested: the test held back from the repo; clean: both present, no defect), plus a docs reply (a README line the code contradicts, its corrected line, must/never regexes) and a flaky reply (a nondeterministic test of a BASE function, its fixed body, a never regex); C gets the prototype from the function's first line. (B) reuse AUTHOR_KEY items only (test/readme items) — no new code, but untested would only pick among six template functions and docs would only add missing lines, not contradict code: too thin to stop memorizing the template. (C) child edits whole files — unbounded, hard to validate. Choice A: new code paths per kind, each validated before render and gated by fm exam check; a scenario a language can't express is dropped and counted (gen's dropped list).
## Risks and rollback
A child regex that matches both the wrong and the right README line would make a check that never fails: validated before render and by fm exam check. A flaky test that fails every time breaks the clean suite: check catches it. Rollback: drop the kinds from CHILD_KINDS; template scenarios are untouched.
## Execution prompt
## Steps
1. [x] red: stub child replies per kind and malformed ones
2. [x] extra-function mechanism (untested, clean) incl. C prototypes
3. [x] docs and flaky reply shapes
4. [x] docs: MASTER, CHANGELOG, site exam text
## Resume here
<!-- auto -->
- 2026-10-30T21:19:02Z steps 4/4 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmexam.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, site/genesis/index.html
- touched since last checkpoint: plugin/lib/fmexam.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, CHANGELOG.md, MASTER.md, site/genesis/index.html
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md ~/.claude/foreman/site/genesis/index.html
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamAuthors.test_children_author_untested_docs_flaky_and_clean_scenarios test_exam.ExamAuthors.test_a_new_function_is_exported_and_declared_where_the_language_needs_it` → red as expected (exit 1) · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: ExamAuthors 0s) / FAILED (1 classes) [ran] [tree 4c1ed02e0860] (2026-10-30T21:09:13Z)
- (step 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 33 tests in 51.6s (10 classes, 16 at a time; slowest: ExamAuthors 51s, ExamGen 22s, ExamRust 12s) / OK [ran] [tree c7600d1f8da5] (2026-10-30T21:13:10Z)
- (step 3) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 12 tests in 48.3s (1 classes, 16 at a time; slowest: ExamAuthors 48s) / OK [ran] [tree c7600d1f8da5] (2026-10-30T21:14:04Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_site test_genesis` → exit 0 · Ran 201 tests in 8.6s (44 classes, 16 at a time; slowest: Fences 8s, GenesisCheck 7s, GenesisSweep 5s) / OK [ran] [tree c7600d1f8da5] (2026-10-30T21:14:13Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 33 tests in 51.3s (10 classes, 16 at a time; slowest: ExamAuthors 51s, ExamGen 22s, ExamRust 12s) / OK [ran] [tree c7600d1f8da5] (2026-10-30T21:15:05Z)
- (ac 2) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 12 tests in 48.3s (1 classes, 16 at a time; slowest: ExamAuthors 48s) / OK [ran] [tree c7600d1f8da5] (2026-10-30T21:15:53Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 33 tests in 51.6s (10 classes, 16 at a time; slowest: ExamAuthors 51s, ExamGen 22s, ExamRust 12s) / OK [ran] [tree 72286c1ccbcc] (2026-10-30T21:24:02Z)
- (ac 2) `python3 plugin/tests/run.py test_exam.ExamAuthors` → exit 0 · Ran 12 tests in 48.3s (1 classes, 16 at a time; slowest: ExamAuthors 48s) / OK [ran] [tree 72286c1ccbcc] (2026-10-30T21:25:01Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 33 tests in 51.5s (10 classes, 16 at a time; slowest: ExamAuthors 51s, ExamGen 22s, ExamRust 12s) / OK [ran] [tree 72286c1ccbcc] (2026-10-30T21:27:09Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 33 tests in 51.5s (10 classes, 16 at a time; slowest: ExamAuthors 51s, ExamGen 22s, ExamRust 12s) / OK [ran] [tree 72286c1ccbcc] (2026-10-30T21:27:09Z)
- `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 128 tests in 51.2s (23 classes, 16 at a time; slowest: ExamAuthors 51s, ExamGen 22s, GenesisCheck 14s) / OK [ran] [tree 72286c1ccbcc] (2026-10-30T21:27:09Z)
- (audit intent) `one foreman:fm-reviewer pass over six lenses (research/T-2211-review.md): 3 MEDIUM + 4 LOW fixed test-first (open-ended-repeat guard, validation against the clean suite's tests, C signature, Rust pub, flaky beside the original and run twice, ASCII names, regex drop tests), 1 LOW accepted` → untested, clean, docs and flaky now have outside-authored scenarios gated by fm exam check; the oracle closes each, empty only clean [tree 72286c1ccbcc] (2026-10-30T21:27:09Z)
- (audit adversary) `one foreman:fm-reviewer pass over six lenses (research/T-2211-review.md): 3 MEDIUM + 4 LOW fixed test-first (open-ended-repeat guard, validation against the clean suite's tests, C signature, Rust pub, flaky beside the original and run twice, ASCII names, regex drop tests), 1 LOW accepted` → child regexes are refused with a repeated group or more than two open-ended repeats; child code runs only through _run with credentials stripped [tree 72286c1ccbcc] (2026-10-30T21:27:09Z)
- (audit edge) `one foreman:fm-reviewer pass over six lenses (research/T-2211-review.md): 3 MEDIUM + 4 LOW fixed test-first (open-ended-repeat guard, validation against the clean suite's tests, C signature, Rust pub, flaky beside the original and run twice, ASCII names, regex drop tests), 1 LOW accepted` → a C source with no plain signature, a non-pub Rust fn, a never regex that matches the clean suite and a flaky fixed body are each caught [tree 72286c1ccbcc] (2026-10-30T21:27:09Z)
- (audit operator) `one foreman:fm-reviewer pass over six lenses (research/T-2211-review.md): 3 MEDIUM + 4 LOW fixed test-first (open-ended-repeat guard, validation against the clean suite's tests, C signature, Rust pub, flaky beside the original and run twice, ASCII names, regex drop tests), 1 LOW accepted` → one child call per scenario, dropped ones counted in gen's dropped list [tree 72286c1ccbcc] (2026-10-30T21:27:09Z)
- (audit maintainer) `one foreman:fm-reviewer pass over six lenses (research/T-2211-review.md): 3 MEDIUM + 4 LOW fixed test-first (open-ended-repeat guard, validation against the clean suite's tests, C signature, Rust pub, flaky beside the original and run twice, ASCII names, regex drop tests), 1 LOW accepted` → one SHAPED table and two functions; the render reuses _write/_tests/_app [tree 72286c1ccbcc] (2026-10-30T21:27:09Z)
- (audit design) `one foreman:fm-reviewer pass over six lenses (research/T-2211-review.md): 3 MEDIUM + 4 LOW fixed test-first (open-ended-repeat guard, validation against the clean suite's tests, C signature, Rust pub, flaky beside the original and run twice, ASCII names, regex drop tests), 1 LOW accepted` → the site's exam text names what the outside author writes [tree 72286c1ccbcc] (2026-10-30T21:27:09Z)
## Log
- 2026-10-30T20:41:17Z created
- 2026-10-30T20:54:28Z planned: it has criteria and steps
- 2026-10-30T20:54:36Z approved on the user's yes 2026-10-30: 'I approve all changes btw, you don't need to ask for my approval'
- 2026-10-30T20:54:41Z set approved=True
- 2026-10-30T21:08:58Z focused
- 2026-10-30T21:15:23Z scope: fmexam (SHAPED prompts, _regex, _author_shaped, _shaped, render/_authored dispatch, CHILD_KINDS), test_exam (stub + tests), test_genesis (partial test retargeted to missing-tool), MASTER/CHANGELOG, site/genesis/index.html
- 2026-10-30T21:28:13Z done
- 2026-10-30T21:28:15Z committed e231e196 (6 files)
## Follow-ups captured
## Build vs reuse
Reuses fmexam's child author (fmideas.run_child, _json, _body), render/_template's planted/clean/hidden layout, the static check type (must/never regexes over test or readme files), _check_one (fm exam check) as the gate, and gen's dropped list; new code is only the per-kind reply validation and the extra-function slot in _app.
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- T-2121 [FEATURE L, done, 2 steps] fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (…
- T-2079 [FEATURE L, done, 6 steps] fm exam: generated multi-language exam with hidden keys, holdout third, finders and claude arms, scores to exam.jsonl — lesson: A claud…
- decision 2026-10-30: [cites: T-2149] #4 exam keys reuse the defect machinery: the child writes one key item (its gap), the goal text is the template's, resume's done ite…
- similar finished tasks took 2–6 steps
## Why not caught
the first stub replies were well-formed Python only; no test fed a brace-first C source, a non-pub Rust fn or a never regex that also hits a regression test
## Lessons
- When a model writes code and patterns that a grader later runs, validate them against exactly what the grader will see (the full clean suite, the language's export and declaration rules), and bound regex cost before the first match
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- plugin/tests/test_genesis.py
- CHANGELOG.md
- MASTER.md
- site/genesis/index.html
