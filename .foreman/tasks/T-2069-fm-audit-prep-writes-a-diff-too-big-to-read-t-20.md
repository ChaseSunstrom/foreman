---
id: T-2069
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-30T00:29:10Z
updated: 2026-10-30T01:20:59Z
base: 06444fa87f77e105fbf93faf3f200f411cbdf1fb
base_tree: f17b898cc90580af6d14a55a9bd9256662b23591
plan0_at: 2026-10-30T00:38:16Z
plan0_scope: []
verified: strong
---
# Audit diffs list a generated file (a changed line over 4000 chars: recordings, minified) by counts, not its text
## Raw request
> fm audit prep writes a diff too big to Read (T-2040.diff 3.1 MB): page or trim generated/binary hunks so a reviewer can read it
## Interpretation
T-2040's audit diff was 27 MB (demo/live.cast frames are 20 KB lines; changed lines always stay whole), too big for any Read: the reviewer got nothing. No reviewer can read a 20 KB line; listing such a file by its +/- counts, like lockfiles, keeps the review on the code.
## Assumptions (confidence)
## Acceptance criteria
- [x] a file with a changed line over 4000 chars is one counts line in the reviewer's diff; short changed lines still stay whole — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_audit`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_audit.CompactDiff: a demo/live.cast block with a 20000-char +line becomes 'generated or minified … left out'
2. [x] _compact_diff: a changed line over GENERATED_LINE marks the file as generated
## Resume here
<!-- auto -->
- 2026-10-30T00:52:11Z steps 2/2 done
- git: foreman/build; 1 uncommitted: CHANGELOG.md
- touched since last checkpoint: .claude/worktrees/agent-ade7380b9617375bb/plugin/tests/test_audit.py, .claude/worktrees/agent-ade7380b9617375bb/plugin/lib/fmcli.py, CHANGELOG.md
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_audit` → exit 0 · Ran 36 tests in 16.4s (17 classes, 16 at a time; slowest: AuditRun 16s, DesignLens 12s, ImportCards 7s) / OK [ran] [tree 1b2979ecf0cf] (2026-10-30T00:39:15Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_cli` → exit 0 · Ran 168 tests in 69.2s (52 classes, 16 at a time; slowest: TaskLifecycle 65s, CaptureAndIntake 33s, StateViews 31s) / OK [ran] [tree 1b2979ecf0cf] (2026-10-30T00:40:26Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_audit` → exit 0 · Ran 36 tests in 15.7s (17 classes, 16 at a time; slowest: AuditRun 15s, DesignLens 11s, ImportCards 6s) / OK [ran] [tree 1b2979ecf0cf] (2026-10-30T00:40:46Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_audit` → exit 0 · Ran 36 tests in 16.0s (17 classes, 16 at a time; slowest: AuditRun 15s, DesignLens 11s, ImportCards 7s) / OK [ran] [tree 430fcac1f7f2] (2026-10-30T00:51:24Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_audit` → exit 0 · Ran 36 tests in 17.8s (17 classes, 16 at a time; slowest: AuditRun 17s, DesignLens 12s, ImportCards 8s) / OK [ran] [tree dbdbec8077d6] (2026-10-30T00:52:17Z)
- (audit edge) `self: diff read; only _compact_diff's classifier changed; short changed lines stay whole (test); T-2055's audit brief came out at 14.5 KB with live.cast/svg listed by counts` → a source file with one 4000+ char line (a data literal) is listed by counts; the reviewer still sees its name and counts and can Read it [tree dbdbec8077d6] (2026-10-30T00:52:17Z)
- (audit self) `self: diff read; only _compact_diff's classifier changed; short changed lines stay whole (test); T-2055's audit brief came out at 14.5 KB with live.cast/svg listed by counts` → no findings [tree dbdbec8077d6] (2026-10-30T00:52:17Z)
## Log
- 2026-10-30T00:29:10Z created
- 2026-10-30T00:30:54Z planned from capture
- 2026-10-30T00:38:01Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2069.builder.md
- 2026-10-30T00:38:16Z focused
- 2026-10-30T00:45:16Z merged worktree-agent-ade7380b9617375bb (2 file(s))
- 2026-10-30T00:45:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ade7380b9617375bb
- 2026-10-30T00:51:05Z focused
- 2026-10-30T00:53:35Z done
- 2026-10-30T00:53:42Z committed 5f65f80a (1 file)
- 2026-10-30T00:54:29Z guard authorization added: publish
- 2026-10-30T01:20:59Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0717-tool-result-sizes: Measured with scratchpad/sizes.py over 64,393 tool results (~31.7M tokens, chars/4).
- T-2040 [FEATURE L, done, 6 steps] Clean up and redesign the whole website (site/): fully modern, more animated, better… — lesson: A recorded video of a themed terminal s…
- research T-2040-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I couldn't run the tests here, so the …
- decision 2026-10-22: T-1508: keep the 2,000-character skill-listing budget; make room by trimming the longest Foreman skill descriptions, not by raising the cap
- similar past tasks were L: consider --tier L
- the similar finished task took 6 steps
## Measurements
T-2055 reviewer brief: ~3.4 MB of cast/svg diff text → 14,520 bytes
## Lessons
- classify generated files by line length, not extension: recordings and minified bundles share no suffix
## Files touched
- plugin/tests/test_audit.py
- plugin/lib/fmcli.py
- CHANGELOG.md
