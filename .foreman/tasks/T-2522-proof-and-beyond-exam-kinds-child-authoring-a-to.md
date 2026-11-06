---
id: T-2522
type: FEATURE
tier: M
status: dropped
priority: normal
scope: [plugin/lib/fmexam.py, plugin/tests/test_exam.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T01:40:10Z
updated: 2026-11-02T01:55:58Z
---
# Child authoring for the proof and beyond exam kinds
## Raw request
> Proof and beyond exam kinds: child authoring: a tool-less child writes new scenarios (request, hidden check, expected verdict) like the other kinds' authors, each kept only if the base can grade it (from T-2442)
## Interpretation
Reading 1: fm exam gen --author child writes new proof (#6) and beyond (#10) scenarios through _author_shaped, as the shaped kinds already do (CHILD_KINDS gates which kinds a child may author): the child writes the request and the expected verdict; ours stay the hidden check's harness and the grading; an item the base can't grade is dropped. Reading 2: a new authoring path just for these two kinds. Reading 1 fits: _author_shaped already takes a kind's prompt and validates the child's fields.
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm exam gen --author child with the child stubbed writes proof and beyond scenarios with their kind's fields, and drops a malformed or ungradable one (counted in gen's output) — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
1) add proof and beyond to CHILD_KINDS with their shaped prompts (proof: a claim about the module and whether it holds; beyond: a deliverable request whose own run decides), parsed and validated by _author_shaped's field check, and each item graded once on the base before it is kept; fails if: a child's claim can't be checked offline (dropped, counted). 2) use what exists: keep the hand-written proof and beyond items only; fails if: nine per kind need more than the hand-written few, and held-out items must be unseen. 3) do less: proof only; fails if: beyond is the other kind T-2394 left without authors. Choice 1 (75%): the shaped path every recent kind uses.
## Risks and rollback
Risk: a child writes a claim the grader can't settle; the base grade before keeping drops it (T-2523 adds the exam of the exam's check). Risk: authoring spends model calls; gen runs only when asked, and exam runs stay paused until the end of the run (the user's steer). Rollback: revert; hand-written items are untouched.
## Execution prompt
## Steps
1. [ ] red test (ExamAuthors): stub fmideas.run_child to return one good and one malformed proof item and one good beyond item; gen keeps the two good, drops the malformed, and labels each with its kind  <- CURRENT
2. [ ] fmexam: proof and beyond in CHILD_KINDS, their prompts and field checks in _author_shaped, the base grade before keeping; MASTER, CHANGELOG
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-02T01:40:10Z created
- 2026-11-02T01:46:17Z planned from capture
- 2026-11-02T01:46:17Z set approved=True
- 2026-11-02T01:55:58Z dropped: already built: T-2453 (4e0a1989, 2026-11-01) added outside child authors for the proof and beyond kinds (fmexam._author_shaped's T-2453 branch: the child writes the dialect or wording of the request inside our repo, so #6 and #10 can pass the held-out); the T-2394 note that seeded T-2442 predates it
## Follow-ups captured
