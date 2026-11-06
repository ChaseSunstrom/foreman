---
id: T-1911
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/run.py, plugin/tests/test_ci_annotations.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T04:21:26Z
updated: 2026-10-29T04:57:52Z
base: bda2bda0f53de20635947e16da186e09c4d13e7f
base_tree: 0ee62b57f12dea6398c0e98ff12a53bb03a9fb4e
plan0_at: 2026-10-29T04:35:40Z
plan0_scope: [plugin/tests/run.py, plugin/tests/test_ci_annotations.py, CHANGELOG.md]
verified: strong
---
# MacOS CI shard 2 exits 1 with no ::error annotation (only run.py's notice), so its failure
## Raw request
> FIX: macOS CI shard 2 exits 1 with no ::error annotation (only run.py's notice), so its failure is invisible without logs: run.py should end a failed CI run with one short ::error naming every failed class and its return code, cap each annotation line's length, and annotate an uncaught exception in main
## Interpretation
A failed CI run must always leave a public ::error naming what failed: one summary error naming each failed class and its exit code, annotation lines capped, 'no output' for a silent class, and run.py's own crash annotated.
## Assumptions (confidence)
## Acceptance criteria
- [x] a failed run names every failed class in one error; a silent class says no output; long lines are cut — verify with `python3 plugin/tests/run.py test_ci_annotations`
## Non-goals
## Approach (options → choice → why)
Complete: every failed CI run names its failures publicly. (A) a summary ::error in summary_notes plus caps — chosen, smallest; (B) upload the log as an artifact — rejected, still needs a login; (C) GitHub step summary markdown — rejected, also needs the run page.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] summary error, capped lines, no-output fallback, crash annotation
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ci_annotations` → exit 0 · Ran 6 tests in 0.3s (2 classes, 16 at a time; slowest: Annotations 0s, SummaryNotes 0s) / OK [ran] [tree 4fa80d0638a7] (2026-10-29T04:56:47Z)
- `python3 plugin/tests/run.py test_ci_annotations` → exit 0 · Ran 6 tests in 1.1s (2 classes, 16 at a time; slowest: SummaryNotes 0s, Annotations 0s) / OK (start tree + this task's tests) [ran] [tree 4fa80d0638a7] (2026-10-29T04:56:49Z)
- `python3 plugin/tests/run.py test_ci_annotations` → exit 0 · Ran 6 tests in 0.3s (2 classes, 16 at a time; slowest: Annotations 0s, SummaryNotes 0s) / OK [ran] [tree 4fa80d0638a7] (2026-10-29T04:56:49Z)
- (step 1) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/try4/plugin/tests/run.py test_ci_annotations` → red as expected (exit 1) · Ran 6 tests in 0.4s (2 classes, 16 at a time; slowest: Annotations 0s, SummaryNotes 0s) / FAILED (2 classes) [ran] [tree 4fa80d0638a7] (2026-10-29T04:57:25Z)
- (step 1) `python3 plugin/tests/run.py test_ci_annotations` → exit 0 · Ran 6 tests in 0.3s (2 classes, 16 at a time; slowest: SummaryNotes 0s, Annotations 0s) / OK [ran] [tree 4fa80d0638a7] (2026-10-29T04:57:30Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_annotations` → exit 0 · Ran 6 tests in 0.3s (2 classes, 16 at a time; slowest: Annotations 0s, SummaryNotes 0s) / OK [ran] [tree 4fa80d0638a7] (2026-10-29T04:57:44Z)
- (step 2) `python3 plugin/tests/run.py test_ci_annotations` → exit 0 · Ran 6 tests in 0.3s (2 classes, 16 at a time; slowest: Annotations 0s, SummaryNotes 0s) / OK [ran] [tree 4fa80d0638a7] (2026-10-29T04:57:44Z)
- (step 3) `python3 plugin/tests/run.py test_ci_annotations` → exit 0 · Ran 6 tests in 0.3s (2 classes, 16 at a time; slowest: Annotations 0s, SummaryNotes 0s) / OK [ran] [tree 4fa80d0638a7] (2026-10-29T04:57:44Z)
- (audit edge) `builder self-review + main-thread read of the diff: annotations stay plain text, lines cut, summary names failed classes` → a class with no output says no output; a crash in run.py itself is annotated (test) [tree 4fa80d0638a7] (2026-10-29T04:57:44Z)
- (audit operator) `builder self-review + main-thread read of the diff: annotations stay plain text, lines cut, summary names failed classes` → a red CI run now names its failing classes without a login [tree 4fa80d0638a7] (2026-10-29T04:57:44Z)
- (audit self) `builder self-review + main-thread read of the diff: annotations stay plain text, lines cut, summary names failed classes` → no findings [tree 4fa80d0638a7] (2026-10-29T04:57:44Z)
## Log
- 2026-10-29T04:21:26Z created
- 2026-10-29T04:23:30Z set tier=S, scope=['plugin/tests/run.py', 'plugin/tests/test_ci_annotations.py', 'CHANGELOG.md']
- 2026-10-29T04:23:30Z planned: it has criteria and steps
- 2026-10-29T04:35:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1911.builder.md
- 2026-10-29T04:35:39Z focused
- 2026-10-29T04:56:34Z merged worktree-agent-a7f874f7905f57f41 (2 file(s))
- 2026-10-29T04:56:36Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7f874f7905f57f41
- 2026-10-29T04:56:37Z focused
- 2026-10-29T04:57:50Z done
- 2026-10-29T04:57:52Z committed 03e0f7a1 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1809 [FIX M, done, 4 steps] CI's macOS job names what makes it time out: run.py --deadline stops below each job's cap, killing and naming running classes; slowest clas…
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- research T-1551-review: Verdict: changes needed.** There are two ways to crash `fm lsp` with crafted input, and one test that cannot fail. I could not run anything (read…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
## Regression test
test_ci_annotations: red on the start tree's run.py (evidence: try4 at bda2bda0 with only the new test), green now; fm task prove can't show it because it carries run.py itself (T-1919)
## Lessons
- A runner's failure report must name what failed; an exit code alone needs a login to read
## Files touched
- plugin/tests/test_ci_annotations.py
- plugin/tests/run.py
- CHANGELOG.md
