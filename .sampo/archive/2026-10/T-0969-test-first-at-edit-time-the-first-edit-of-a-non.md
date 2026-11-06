---
id: T-0969
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-15T22:07:59Z
updated: 2026-10-15T23:06:11Z
base: 9d73e16224e31547fe836a2b2ddcdd2d5b824e20
base_tree: dacbdf4a1b2a4ab576c5ed86d40cd0dc65d2cc12
verified: strong
---
# Test-first at edit time: the first edit of a non-test file in a FIX/FEATURE task with no t
## Raw request
> Test-first at edit time: the first edit of a non-test file in a FIX/FEATURE task with no test changed and no failing run on record gets a one-line note (zero tokens, once per task), from rivals TDD Guard and superpowers (research/T-0964-catalogue.md)
## Interpretation
Test-first at edit time: the first edit of a non-test source file in a FIX or FEATURE task, when the task has changed no test file and recorded no failing run yet, gets one short note to write and run the failing test first. Zero LLM judge (TDD Guard uses one per edit); once per task.
## Assumptions (confidence)
## Acceptance criteria
- [x] In a FIX/FEATURE task with no changed test file and no failing evidence, the first Edit/Write of a non-test source file gets one note naming the test-first step; a test-file edit, a task that already has a failing run or a changed test, a CLEAN/RESEARCH task, a second edit in the same task, and docs/config files get none — verify with `python3 plugin/tests/run.py -k TestFirstNote`
## Non-goals
## Approach (options → choice → why)
Options: a PreToolUse note from facts Foreman already has: the task's type, its evidence (a failed run), and git's changed files since the task base matched against test-path patterns (chosen: zero tokens, once per task, never a block); an LLM judge per edit (tokens, latency); a block (breaks legitimate refactors and docs edits).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing TestFirstNote tests
2. [x] PreToolUse note (fmhooks), test-path patterns shared with existing test detection; docs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k TestFirstNote` → ✗ exit 1 · Ran 5 tests in 3.9s (1 classes, 16 at a time; slowest: TestFirstNote 4s) / FAILED (1 classes) [ran] [tree 4dcf87b4c106] (2026-10-15T22:51:54Z)
- (step 2) `python3 plugin/tests/run.py -k TestFirstNote` → exit 0 · Ran 5 tests in 7.9s (1 classes, 16 at a time; slowest: TestFirstNote 8s) / OK [ran] [tree ea456ce59ad9] (2026-10-15T22:55:02Z)
- (step 1) `python3 plugin/tests/run.py test_first_note test_hooks` → exit 0 · Ran 157 tests in 35.4s (21 classes, 16 at a time; slowest: Stop 35s, PreToolUse 20s, SessionStart 16s) / OK [ran] [tree c864863b937c] (2026-10-15T23:06:00Z)
- (ac 1) `python3 plugin/tests/run.py -k TestFirstNote` → exit 0 · Ran 5 tests in 4.1s (1 classes, 16 at a time; slowest: TestFirstNote 4s) / OK [ran] [tree c864863b937c] (2026-10-15T23:06:05Z)
- (audit intent) `read the merged diff (fmhooks._test_first_note, test_first_note.py, test_hooks note test): FIX/FEATURE only, file tools only, code files only, test files and evidence of a failing run skip it, marker set before the git call so it never repeats; tests pass` → one advisory note on the first source edit with no test written or failing run; never a block [tree c864863b937c] (2026-10-15T23:06:05Z)
- (audit edge) `read the merged diff (fmhooks._test_first_note, test_first_note.py, test_hooks note test): FIX/FEATURE only, file tools only, code files only, test files and evidence of a failing run skip it, marker set before the git call so it never repeats; tests pass` → a test file edit, a non-code file, a task with a ✗ run, a changed test since base, or an S CLEAN/RESEARCH task get no note; a git failure is logged and silent [tree c864863b937c] (2026-10-15T23:06:05Z)
- (audit intent) `read the merged diff (fmhooks._test_first_note, test_first_note.py, test_hooks note test): FIX/FEATURE only, file tools only, code files only, test files and evidence of a failing run skip it, marker set before the git call so it never repeats; tests pass` → one advisory note on the first source edit with no test written or failing run; never a block [tree c864863b937c] (2026-10-15T23:06:11Z)
- (audit edge) `read the merged diff (fmhooks._test_first_note, test_first_note.py, test_hooks note test): FIX/FEATURE only, file tools only, code files only, test files and evidence of a failing run skip it, marker set before the git call so it never repeats; tests pass` → a test file edit, a non-code file, a task with a ✗ run, a changed test since base get no note; a git failure is logged and silent [tree c864863b937c] (2026-10-15T23:06:11Z)
- (audit adversary) `read the merged diff (fmhooks._test_first_note, test_first_note.py, test_hooks note test): FIX/FEATURE only, file tools only, code files only, test files and evidence of a failing run skip it, marker set before the git call so it never repeats; tests pass` → the note only adds context after the guard has ruled; it can't allow or deny a call, and fmguard.py in the range is T-0971's change (closed with its own adversary review) [tree c864863b937c] (2026-10-15T23:06:11Z)
## Log
- 2026-10-15T22:07:59Z created
- 2026-10-15T22:50:06Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0969.builder.md
- 2026-10-15T22:50:17Z focused
- 2026-10-15T22:58:12Z merged worktree-agent-aa29794f770a0fe35 (5 file(s))
- 2026-10-15T22:58:13Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa29794f770a0fe35
- 2026-10-15T23:05:16Z focused
- 2026-10-15T23:06:11Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- research T-0964-catalogue: Sources: research/T-0964-harness.md (claude-code-harness, feature by feature), research/T-0964-workflow.md (ECC,
- T-0671 [FEATURE M, done, 3 steps] Milestone: Features — Autonomy and the user — lesson: A guard-word filter on free text needs the verbs people actually use (push, delet…
- decision 2026-10-15: T-0964: queue 7 of the rival gaps (T-0969..T-0975); keep the LATER ones (PR-per-task flow, best-of-N lanes, diff-comment review page, plan/edit mode…
- similar finished tasks took 3–3 steps
## Lessons
- An edit-time nudge must decide once and mark before any slow call, so a hook never pays for it twice.
## Plan gaps
- failed first: step 1 Failing TestFirstNote tests
## Files touched
- plugin/tests/test_first_note.py
- plugin/lib/fmhooks.py
- plugin/tests/test_hooks.py
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- plugin/tests/test_user_rules.py
