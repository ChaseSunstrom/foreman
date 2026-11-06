---
id: T-1274
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T14:56:40Z
updated: 2026-10-20T17:01:00Z
base: 0206ac8cf90462420c3f826f1be7a4cfe91e67c3
base_tree: c999e06fded006ea8c6410043739753b8ef81bbc
plan0_at: 2026-10-20T16:55:48Z
plan0_scope: []
verified: strong
---
# Edit-time lesson note: at most 200 characters, shorter wording ('T-x's lesson for this file: …')
## Raw request
> Edit-time recall note 'T-x (done) also changed this file; its lesson: …' was 12 KB over 64 edits in one session: once per file per session, and the lesson cut to one short clause
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the tripwire note names the task and its lesson in at most 200 characters — verify with `python3 plugin/tests/run.py test_memory test_learning test_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a long lesson's note fits 200 characters and keeps the task id
2. [x] Shorten the note in fmhooks._tripwire_note, measurements, changelog
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_memory test_learning test_friction 2>&1 | tail -15` → ✗ exit 1 · Ran 32 tests in 15.1s (14 classes, 16 at a time; slowest: Memory 14s, Friction 12s, Playbook 2s) / FAILED (1 classes) [ran] [tree 90387f37bb0a] (2026-10-20T16:56:14Z)
- (ac 1) `python3 plugin/tests/run.py test_memory test_learning test_friction` → exit 0 · Ran 32 tests in 6.9s (14 classes, 16 at a time; slowest: Memory 7s, Friction 6s, Playbook 1s) / OK [ran] [tree 71ba8e676b9c] (2026-10-20T16:58:46Z)
- (step 1) `python3 plugin/tests/run.py test_memory test_learning test_friction` → exit 0 · Ran 32 tests in 6.9s (14 classes, 16 at a time; slowest: Memory 7s, Friction 6s, Playbook 1s) / OK [ran] [tree 71ba8e676b9c] (2026-10-20T16:58:46Z)
- (step 2) `python3 plugin/tests/run.py test_memory test_learning test_friction` → exit 0 · Ran 32 tests in 6.9s (14 classes, 16 at a time; slowest: Memory 7s, Friction 6s, Playbook 1s) / OK [ran] [tree 71ba8e676b9c] (2026-10-20T16:58:46Z)
- (audit intent) `main session read the builder's one-line change and its test; criteria re-run here after the merge` → Foreman's per-file lesson notes cost less context while still naming the task and its lesson [tree 71ba8e676b9c] (2026-10-20T16:58:46Z)
- (audit edge) `main session read the builder's one-line change and its test; criteria re-run here after the merge` → the task id comes first, so the 200-character cut only ever trims the lesson's end; an empty lesson gives a shorter note; the once-per-file-per-context rule is unchanged [tree 71ba8e676b9c] (2026-10-20T16:58:46Z)
- (audit self) `main session read the builder's one-line change and its test; criteria re-run here after the merge` → no findings [tree 71ba8e676b9c] (2026-10-20T16:58:46Z)
- `python3 plugin/tests/run.py test_memory test_learning test_friction` → exit 0 · Ran 32 tests in 6.9s (14 classes, 16 at a time; slowest: Memory 7s, Friction 6s, Playbook 1s) / OK [ran] [tree 71ba8e676b9c] (2026-10-20T16:59:57Z)
- (audit intent) `main session read the builder's one-line change and its test; criteria re-run here after the merge` → Foreman's per-file lesson notes cost less context while still naming the task and its lesson [tree 71ba8e676b9c] (2026-10-20T16:59:57Z)
- (audit edge) `main session read the builder's one-line change and its test; criteria re-run here after the merge` → the task id comes first, so the 200-character cut only ever trims the lesson's end; an empty lesson gives a shorter note; the once-per-file-per-context rule is unchanged [tree 71ba8e676b9c] (2026-10-20T16:59:57Z)
- (audit self) `main session read the builder's one-line change and its test; criteria re-run here after the merge` → no findings [tree 71ba8e676b9c] (2026-10-20T16:59:57Z)
## Log
- 2026-10-20T14:56:40Z created
- 2026-10-20T16:52:54Z planned from capture
- 2026-10-20T16:52:59Z criterion 1 verify: `python3 plugin/tests/run.py test_recall` → `python3 plugin/tests/run.py test_memory test_learning test_friction`
- 2026-10-20T16:55:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1274.builder.md
- 2026-10-20T16:55:47Z focused
- 2026-10-20T16:58:27Z merged worktree-agent-a369e4adc3bb227bb (2 file(s))
- 2026-10-20T16:58:27Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a369e4adc3bb227bb
- 2026-10-20T16:58:38Z focused
- 2026-10-20T17:00:59Z done
- 2026-10-20T17:01:00Z committed 1851c52e (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1242 [FEATURE L, done, 3 steps] Marathon showcase: a long unattended run that keeps finishing work across forced compactions, Foreman vs plain Claude Code, cheap (Haik…
- research T-1032-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** changes needed. Two MEDIUM findings should be fixed befor…
- T-0707 [FEATURE M, done, 4 steps] Frontier 07 — Knowledge graph — lesson: Retrieval for a new task works best through past tasks: words match titles far better than path…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
## Measurements
Lesson note length cap: 320 → 200 characters; fixed frame 49 → 33 characters ('(done) also changed this file; its lesson:' → ''s lesson for this file:'), from the code; in the measured long session 64 notes averaged about 190 characters (12 KB), so long ones now save up to 120 characters each
## Lessons
- none: a wording cut with its bound tested; nothing new to carry forward
## Files touched
- plugin/tests/test_memory.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- plugin/lib/fmambient.py
- plugin/tests/test_ambient.py
