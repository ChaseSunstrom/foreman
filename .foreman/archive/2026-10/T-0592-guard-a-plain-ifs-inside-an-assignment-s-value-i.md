---
id: T-0592
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:17:12Z
updated: 2026-10-09T15:18:06Z
base: 0afd44adc2347c7857fb0c381f3eebeb039d9e7e
base_tree: 8ece48961a4fa7efa119d7bf496959dbe555806d
verified: strong
---
# Guard: a plain IFS inside an assignment's value is refused, not rewritten
## Raw request
> Guard: a plain IFS inside an assignment's value is refused, not rewritten
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] IFS in an unquoted assignment value is refused; quoted values pass — verify with `python3 plugin/tests/run.py -k IfsInValue`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: IfsInValue rows
2. [x] _ifs_unreadable refuses an unquoted assignment value with a plain IFS
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k IfsInValue` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: IfsInValue 0s) / FAILED (1 classes) [ran] [tree 63f026bfeab4] (2026-10-09T15:17:16Z)
- (step 2) `python3 plugin/tests/run.py -k IfsInValue` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: IfsInValue 0s) / OK [ran] [tree 48435ca99ec7] (2026-10-09T15:18:05Z)
- (ac 1) `python3 plugin/tests/run.py -k IfsInValue` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: IfsInValue 0s) / OK [ran] [tree 48435ca99ec7] (2026-10-09T15:18:06Z)
- (audit adversary) `self: rows for a scalar, an exported and an array-element value refuse; a quoted value passes; suites green; replay 0/0` → the refusal is appended with the line's other findings (rm-outside also reported), so allowing system lets nothing else through [tree 48435ca99ec7] (2026-10-09T15:18:06Z)
- (audit self) `self: rows for a scalar, an exported and an array-element value refuse; a quoted value passes; suites green; replay 0/0` → no findings [tree 48435ca99ec7] (2026-10-09T15:18:06Z)
## Log
- 2026-10-09T15:17:12Z created
- 2026-10-09T15:17:12Z focused
- 2026-10-09T15:18:06Z done
- 2026-10-09T15:18:06Z committed bdbdc25 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0590 [SECURITY M, done, 2 steps] Guard: IFS review round 2 — eval/source/quoted IFS sets, # after a rewritten IFS, quoted spans, read across a newline — lesson: a text…
- T-0585 [SECURITY M, done, 2 steps] Guard: IFS set by any name form, or expanded with an operator, is refused instead of erased — lesson: a guard rewrite that maps a fami…
- T-0411 [FEATURE M, done, 3 steps] FEATURE: the guard reads a for loop over literal words (for w in agent-a agent-b; do … $w — lesson: A text rewrite ahead of the guard m…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar past tasks were M: consider --tier M
## Lessons
- an assignment value is one word to bash whatever it expands to; never insert separators into it
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/lib/fmguard.py
- CHANGELOG.md
