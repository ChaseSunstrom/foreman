---
name: ideation-to-briefs
title: Ideation to briefs
area: practice
tags: [planning, briefs, tasks, acceptance-criteria, handoff]
detect: []
related: [grounding-ideas, value-effort-scoring, scope-cutting, brainstorming-lenses]
---
Turn a chosen idea into an executable task: outcome, criteria with verify commands, steps, scope and non-goals, ordered in the queue.

## Verify
- `fm queue`: the new tasks appear in the intended order.
- `fm task new --help`: shows `--ac "<done when> :: <verify cmd>"` and `--step`.
- `fm check`: runs the criteria commands; each fails now (test first) and passes at the end.

## Test first
A brief is ready when every criterion has a command that fails today.
```markdown
Title: <verb + outcome>
AC: 1. `pytest tests/test_export.py::test_csv_header -q` fails now with "no such function export_csv"
Steps: 1. add failing test 2. implement 3. gate
Scope: src/export.py, tests/test_export.py   Non-goals: XLSX
Pass = running each AC command on the current tree fails for the stated reason.
```

## Do
- Write the outcome in one sentence a user would recognise.
- Convert each wanted behaviour into a criterion plus a command; run it to see it fail.
- Name the files in scope from grounding; list non-goals to stop drift.
- Size the tier honestly (small, several files, cross-cutting) and split anything larger than one sitting.
- Put dependencies between tasks explicitly, and order by value, risk and unblock count.
- Add a verification step and any audit the tier requires.
- Create it with `fm task new "<title>" --type T --tier S --ac "<criterion> :: <command>" --step "<step>"`.

## Avoid
- Criteria that restate the idea ("works well"): replace with a command and an expected output.
- Briefs with no file evidence: ground first or the steps are guesses.
- One giant task for the whole list: one outcome per task.
- Criteria that pass before the work: a green-from-the-start check proves nothing; make it fail first.
- Missing non-goals: scope grows unless the boundary is written.

## Review
- [ ] Outcome is one sentence.
- [ ] Every criterion has a command that failed beforehand.
- [ ] Scope files and non-goals are listed.
- [ ] Tier and dependencies are set.
- [ ] Queue order was checked with `fm queue`.
