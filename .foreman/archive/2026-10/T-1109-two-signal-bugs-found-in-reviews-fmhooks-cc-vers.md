---
id: T-1109
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmrecall.py, plugin/tests/test_recall.py, plugin/tests/test_hooks.py]
depends_on: []
source: discovered
created: 2026-10-16T05:08:39Z
updated: 2026-10-16T05:34:48Z
base: 84f827f2104329ddf41de7ce7dd2b3001030e098
base_tree: f5d869d3ec23ab7b8e8188dd85ec5b874a6dd42d
verified: strong
---
# Two signal bugs found in reviews: fmhooks._cc_version caches the Claude Code version for 2
## Raw request
> Two signal bugs found in reviews: fmhooks._cc_version caches the Claude Code version for 24 h (doctor says 'claude update' after an update; refresh on the binary's mtime/ctime change); fmrecall.failure_signature zeroes digits but keeps hex letters, so worktree/agent names (agent-a0bd0ad0edc0) make the same failure look new every time and repeats never group
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] failure_signature gives the same signature for the same error in differently named worktrees/agents (hex ids), and keeps words without digits — verify with `python3 plugin/tests/run.py test_recall`
- [x] _cc_version re-reads claude --version when the claude binary is newer than the cached version file — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests for both
2. [x] Zero hex ids in signatures; refresh the version cache on a newer binary
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_recall test_hooks` → ✗ exit 1 · Ran 169 tests in 54.8s (25 classes, 16 at a time; slowest: Stop 55s, PreToolUse 36s, Recall 34s) / FAILED (2 classes) [ran] [tree 437f7047c38d] (2026-10-16T05:31:40Z)
- (step 2) `python3 plugin/tests/run.py test_recall test_hooks test_fixes test_doctor` → exit 0 · Ran 228 tests in 43.8s (42 classes, 16 at a time; slowest: Stop 44s, Command 28s, PreToolUse 27s) / OK [ran] [tree ca49962902a3] (2026-10-16T05:32:31Z)
- (ac 1) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 14 tests in 21.8s (5 classes, 16 at a time; slowest: Recall 22s, RedGreen 2s, Memory 1s) / OK [ran] [tree a49406a7bdc7] (2026-10-16T05:34:47Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 155 tests in 71.8s (20 classes, 16 at a time; slowest: Stop 72s, PreToolUse 47s, PromptApprovals 35s) / OK [ran] [tree a49406a7bdc7] (2026-10-16T05:34:47Z)
- (step 1) `python3 plugin/tests/run.py test_recall test_hooks` → exit 0 · Ran 169 tests in 34.5s (25 classes, 16 at a time; slowest: Stop 34s, PreToolUse 18s, Recall 17s) / OK [ran] [tree a49406a7bdc7] (2026-10-16T05:34:47Z)
- (audit self) `self: both changes tested red then green; the hex rule needs a digit and 5+ chars so plain words stay` → no findings [tree a49406a7bdc7] (2026-10-16T05:34:47Z)
## Log
- 2026-10-16T05:08:39Z created
- 2026-10-16T05:30:10Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmrecall.py', 'plugin/tests/test_recall.py', 'plugin/tests/test_doctor.py']
- 2026-10-16T05:30:33Z focused
- 2026-10-16T05:30:44Z set scope=['plugin/lib/fmhooks.py', 'plugin/lib/fmrecall.py', 'plugin/tests/test_recall.py', 'plugin/tests/test_hooks.py']
- 2026-10-16T05:31:47Z criterion 2 verify: `python3 plugin/tests/run.py test_doctor` → `python3 plugin/tests/run.py test_hooks`
- 2026-10-16T05:32:38Z scope: CHANGELOG.md — release note
- 2026-10-16T05:34:47Z done
- 2026-10-16T05:34:48Z committed 342cc76 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- research T-1076-review: Verdict: approve with nits.** The code is correct on the paths I traced. None of these findings is HIGH. I did not run the tests, and I could not…
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
- likely tests for the scope: plugin/tests/test_hooks.py, plugin/tests/test_recall.py
## Lessons
- A cache of another program's version should key on that program's file, not only on the clock
## Plan gaps
- failed first: step 1 Failing tests for both
## Files touched
- plugin/tests/test_hooks.py
- plugin/tests/test_recall.py
- plugin/lib/fmhooks.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
