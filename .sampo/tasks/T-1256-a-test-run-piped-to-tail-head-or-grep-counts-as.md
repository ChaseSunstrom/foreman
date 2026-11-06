---
id: T-1256
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_bookkeeping.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-20T14:01:16Z
updated: 2026-10-20T14:44:34Z
base: 692359cfd7f237473a41cacf3b2ff3ac6d6095a3
base_tree: 8090f1136eb897d6f76d9f2a196948d4b0528127
plan0_at: 2026-10-20T14:40:24Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_bookkeeping.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# A test run piped to tail, head or grep counts as the criterion's or step's evidence when i
## Raw request
> PERF: A test run piped to tail, head or grep counts as the criterion's or step's evidence when its output carries the runner's own pass or fail summary (the long-session agent piped every run, then spent 5-12 fm task evidence calls)
> CONTEXT: brainstorm 2026-10-20 (research brainstorm-20261020), T-1252; Claude Code 2.1.304 re-sends the skill list after each compaction
## Interpretation
A test run piped to tail, head or grep (often with 2>&1) is the same check as the verify or runner it wraps. Its exit code is the filter's, so it counts only when the output carries the runner's own pass summary (unittest OK, pytest N passed in, jest Tests: N passed, cargo test result: ok, go ok/PASS, mocha N passing), and a failure summary records a failure. Long sessions piped every run and then spent 5 to 12 calls on fm task evidence.
## Assumptions (confidence)
## Acceptance criteria
- [x] a criterion's verify or a same-runner test run piped to tail, head or grep (2>&1 included) records evidence when its output carries the runner's own pass summary; a failure summary or no summary records none — verify with `python3 plugin/tests/run.py test_bookkeeping`
## Non-goals
## Approach (options → choice → why)
Options: (a) strip a trailing tail/head/grep filter, then judge the run by its output's summary; (b) ask agents not to pipe (a note, costs context, ignored under pressure); (c) set pipefail through a hook (can't change the Bash tool's shell). Choice: (a), in _auto_evidence and _runner, with fmcore holding the pass-summary pattern beside the failure one.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in test_bookkeeping: piped verify with a pass summary is evidence; with a failure or no summary it isn't; a piped same-runner run verifies the step
2. [x] Strip a trailing output filter in fmhooks (_auto_evidence, _runner), require fmcore's pass summary for piped runs, changelog
## Resume here
## Docs impact
MASTER auto-evidence paragraph and CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bookkeeping` → ✗ exit 1 · Ran 13 tests in 3.1s (8 classes, 16 at a time; slowest: StepEvidence 3s, CommitOwnFiles 2s, CommitAfterFocus 2s) / FAILED (1 classes) [ran] [tree 3eb1a617e061] (2026-10-20T14:40:28Z)
- (step 2) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 13 tests in 3.1s (8 classes, 16 at a time; slowest: StepEvidence 3s, CommitOwnFiles 2s, CommitAfterFocus 2s) / OK [ran] [tree 19443283ec86] (2026-10-20T14:41:15Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 13 tests in 3.2s (8 classes, 16 at a time; slowest: StepEvidence 3s, CommitOwnFiles 2s, CommitAfterFocus 2s) / OK [ran] [tree f370fc20ef43] (2026-10-20T14:43:25Z)
- `python3 plugin/tests/run.py test_bookkeeping test_hooks` → exit 0 · Ran 199 tests in 37.8s (29 classes, 16 at a time; slowest: Stop 38s, PreToolUse 22s, NoTaskGate 22s) / OK [ran] [tree f370fc20ef43] (2026-10-20T14:43:25Z)
- (audit intent) `self review of the filter stripping and the summary patterns against each runner's real summary lines, including mixed pass and fail lines` → a piped check now counts by its output, so a session that pipes every run no longer pays a second call per step; the fewer calls are what the long-session premium was made of [tree f370fc20ef43] (2026-10-20T14:43:25Z)
- (audit adversary) `self review of the filter stripping and the summary patterns against each runner's real summary lines, including mixed pass and fail lines` → a pipe can't fake a pass by its exit: tail's 0 counts only with the runner's own summary and no failure summary; a grep that keeps only an OK line from a failed run would pass, which is the agent filtering its own evidence, the same as before with any output it chose to show [tree f370fc20ef43] (2026-10-20T14:43:25Z)
- (audit edge) `self review of the filter stripping and the summary patterns against each runner's real summary lines, including mixed pass and fail lines` → a grep pattern with a quoted | is stripped as one filter; several filters in a row are all stripped; a verify that itself contains a pipe still matches exactly; pytest -q's bare '4 passed' without its timing isn't taken as a summary [tree f370fc20ef43] (2026-10-20T14:43:25Z)
## Log
- 2026-10-20T14:01:16Z created
- 2026-10-20T14:17:18Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_bookkeeping.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-20T14:40:24Z focused
- 2026-10-20T14:44:33Z done
- 2026-10-20T14:44:34Z committed 3e6d5468 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Measurements
Manual fm task evidence calls a piped test run needs before its step or criterion counts: 1 before → 0 after (test_bookkeeping replays a piped verify and a piped same-runner run; both were refused before the change, step 1's red run). In the long benchmark transcripts the agent piped every run and made 5 to 12 such calls a session; a new long duel will show the after figure there (not run yet, to save usage).
## Lessons
- Count a run by its output's summary when its exit code belongs to a filter; a pipe to tail is how agents keep output short, so evidence has to survive it
## Plan gaps
- failed first: step 1 Failing tests in test_bookkeeping: piped verify with a pass summary is evidence; with a failure or …
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
