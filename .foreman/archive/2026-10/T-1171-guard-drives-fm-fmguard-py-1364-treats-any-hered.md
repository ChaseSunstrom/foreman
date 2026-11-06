---
id: T-1171
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-16T10:48:14Z
updated: 2026-10-16T11:27:17Z
base: ea0244a4aa9d1433cd6364ea0ea8af93395c12cb
base_tree: c37cfbfee70a7097dbf4497e17221ff50b364005
plan0_at: 2026-10-16T11:21:23Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Guard: _drives_fm (fmguard.py:1364) treats any heredoc that doesn't parse, and fm-import t
## Raw request
> Guard: _drives_fm (fmguard.py:1364) treats any heredoc that doesn't parse, and fm-import text outside quoted python - bodies, as driving fm (18 false blocks): parse python3 - <<'EOF' bodies after a ; or cd, and flag only a real import fm* plus a mutating call
## Interpretation
Grounded on the 31 real refusals of this rule in four days of transcripts (full commands): 12 wrote a test with cat <<'EOF' and ran the tests in the same command; the rest ran python code importing fm modules for real. None was data-only. Since writing the file alone and running the tests alone each pass, the guard stays as it is and the refusal says to split, so the next try is right the first time.
## Assumptions (confidence)
## Acceptance criteria
- [x] a quoted heredoc written to a file with cat or tee and nothing run is not 'driving Foreman'; the same with python3/bash/source/eval/xargs/$( after it, an unquoted delimiter, or a python heredoc stays blocked — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
Options: (a) in _drives_fm, return False early when _data_only_writes(cmd): every heredoc starter line is cat/tee to a file with a quoted delimiter, and the shell text without bodies has no interpreter word, no $( or backtick; (b) parse python bodies after ';' (finding 1): no gain, those bodies import fm for real; (c) record labelled cases first (T-1162). Choice: (a); why: smallest relaxation that is provably data (quoted delimiter = no expansion; nothing runs it in the same command). Adversary: write-then-run (python3 x.py, bash x, source, run.py) stays blocked because an interpreter word appears.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in test_guard (driving: data-only writes allowed, every run form blocked)
2. [x] _data_only_writes in fmguard and the early return; message names the split
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 119 tests in 5.2s (50 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, GuardTry 1s) / FAILED (1 classes) [ran] [tree 739d474aacb8] (2026-10-16T11:21:49Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_try` → ✗ exit 1 · Ran 119 tests in 5.3s (50 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, GuardTry 1s) / FAILED (1 classes) [ran] [tree ce6c9373ba98] (2026-10-16T11:22:29Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_try` → ✗ exit 1 · Ran 119 tests in 5.8s (50 classes, 16 at a time; slowest: GuardAgainstBash 6s, Hook 2s, GuardTry 1s) / FAILED (1 classes) [ran] [tree 9c3c8e1b873d] (2026-10-16T11:23:07Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_try` → ✗ exit 1 · Ran 119 tests in 5.8s (50 classes, 16 at a time; slowest: GuardAgainstBash 6s, Hook 2s, GuardTry 1s) / FAILED (1 classes) [ran] [tree c5a866aa27d6] (2026-10-16T11:23:25Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_try` → ✗ exit 1 · Ran 119 tests in 6.0s (50 classes, 16 at a time; slowest: GuardAgainstBash 6s, Hook 2s, GuardTry 1s) / FAILED (1 classes) [ran] [tree 34be267ea1b9] (2026-10-16T11:23:42Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_try` → exit 0 · Ran 119 tests in 15.2s (50 classes, 16 at a time; slowest: GuardAgainstBash 15s, Hook 5s, GuardTry 3s) / OK [ran] [tree 635314f73e77] (2026-10-16T11:25:32Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 119 tests in 27.7s (50 classes, 16 at a time; slowest: GuardAgainstBash 27s, Hook 9s, GuardTry 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 38802f16c0de] (2026-10-16T11:26:26Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 119 tests in 9.8s (50 classes, 16 at a time; slowest: GuardAgainstBash 10s, Hook 5s, GuardTry 2s) / OK [ran] [tree 38802f16c0de] (2026-10-16T11:26:26Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 119 tests in 5.4s (50 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, GuardTry 1s) / OK [ran] [tree 38802f16c0de] (2026-10-16T11:26:37Z)
- `python3 plugin/tests/run.py test_guard test_guard_diff` → exit 0 · Ran 119 tests in 5.3s (50 classes, 16 at a time; slowest: GuardAgainstBash 5s, Hook 2s, GuardTry 1s) / OK [ran] [tree 38802f16c0de] (2026-10-16T11:26:37Z)
- (audit intent) `self: mined all 31 refusals from transcripts with full text; a relaxation for data-only cat writes was built, then reverted when the untruncated commands showed it would have helped none; only the refusal text changed (no verdict changes); tests pin the hint, the two halves passing and the run forms still refused` → the next attempt after this refusal succeeds first time [tree 38802f16c0de] (2026-10-16T11:26:37Z)
- (audit adversary) `self: mined all 31 refusals from transcripts with full text; a relaxation for data-only cat writes was built, then reverted when the untruncated commands showed it would have helped none; only the refusal text changed (no verdict changes); tests pin the hint, the two halves passing and the run forms still refused` → no verdict changed (fmguard diff is message-only); write-then-run forms (python3 x.py, env python3, cat|python3, python heredoc) still refused [tree 38802f16c0de] (2026-10-16T11:26:37Z)
- (audit edge) `self: mined all 31 refusals from transcripts with full text; a relaxation for data-only cat writes was built, then reverted when the untruncated commands showed it would have helped none; only the refusal text changed (no verdict changes); tests pin the hint, the two halves passing and the run forms still refused` → the hint appears only when a cat/tee heredoc is in the command; the cd; hint still combines [tree 38802f16c0de] (2026-10-16T11:26:37Z)
- (audit operator) `self: mined all 31 refusals from transcripts with full text; a relaxation for data-only cat writes was built, then reverted when the untruncated commands showed it would have helped none; only the refusal text changed (no verdict changes); tests pin the hint, the two halves passing and the run forms still refused` → one clause added to an existing message [tree 38802f16c0de] (2026-10-16T11:26:37Z)
- (audit maintainer) `self: mined all 31 refusals from transcripts with full text; a relaxation for data-only cat writes was built, then reverted when the untruncated commands showed it would have helped none; only the refusal text changed (no verdict changes); tests pin the hint, the two halves passing and the run forms still refused` → comment cites the mined counts [tree 38802f16c0de] (2026-10-16T11:26:37Z)
## Log
- 2026-10-16T10:48:14Z created
- 2026-10-16T11:21:21Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-10-16T11:21:22Z steer: grounded on 31 mined refusals; relax only data-only cat/tee heredoc writes
- 2026-10-16T11:21:22Z focused
- 2026-10-16T11:23:25Z tried: `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_try` ×3 on step 2, failing the same way
- 2026-10-16T11:23:42Z tried: `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_try` ×4 on step 2, failing the same way
- 2026-10-16T11:25:47Z steer: a data-only relaxation was built and reverted: on full (untruncated) commands it would have prevented 0 of 31 refusals; the message names the split instead
- 2026-10-16T11:27:16Z done
- 2026-10-16T11:27:17Z committed feeb84a (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0761 [FIX S, dropped, 2 steps] Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- the similar finished task took 2 steps
- start here (files T-0774 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
the friction digest counts refusals but not their commands; mining transcripts gave the real shapes
## Lessons
- mine full commands before relaxing a guard rule: a 1,500-char cut made write+run commands look like data-only writes
## Plan gaps
- failed first: step 1 Failing test in test_guard (driving: data-only writes allowed, every run form blocked)
- failed first: step 2 _data_only_writes in fmguard and the early return; message names the split
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
