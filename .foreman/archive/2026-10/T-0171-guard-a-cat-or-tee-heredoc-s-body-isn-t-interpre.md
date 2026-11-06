---
id: T-0171
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-10-03T08:54:00Z
updated: 2026-10-03T09:04:22Z
base: 3c27f97c493e6189925d80b0799f4fb7cf303596
base_tree: c7649778931a18f00a74b8ee65fbe0398cc112b6
verified: strong
---
# Guard: a quoted cat/tee heredoc's body is data, not interpreter code, for the interpreter gate
## Raw request
> Guard: a cat or tee heredoc's body isn't interpreter code: run the interpreter gate on the shell text only for those (redirect targets are still checked)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Writing a file with a quoted cat heredoc that mentions python and a credential path is allowed; the same body piped into python3, an unquoted heredoc with a substitution, and every differential form stay blocked — verify with `python3 plugin/tests/run.py -k test_guard`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red rows
2. [x] _drop_data_heredocs in the interpreter gate
3. [x] CHANGELOG; MASTER wording fix from T-0167
## Resume here
## Docs impact
MASTER (guard limits sentence; T-0167 wording) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_quoted_cat_heredoc` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 9995a97c625b] (2026-10-03T09:02:52Z)
- (step 1) `python3 plugin/tests/run.py -k test_a_quoted_cat_heredoc` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) [ran] [tree 1c56f2843016] (2026-10-03T09:03:12Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 47 tests in 1.0s (17 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, GitDestructive 0s) / OK [ran] [tree b8fa794dc4a3] (2026-10-03T09:03:21Z)
- (step 1) `python3 plugin/tests/run.py -k test_a_quoted_cat_heredoc` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree c025d7b27fcb] (2026-10-03T09:03:34Z)
- (step 3) `grep -q T-0171 CHANGELOG.md && grep -q 'doubled slash' MASTER.md` → exit 0 · (no output) [ran] [tree c025d7b27fcb] (2026-10-03T09:04:14Z)
- (ac 1) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 47 tests in 1.0s (17 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, PreToolUse 0s) / OK [ran] [tree c025d7b27fcb] (2026-10-03T09:04:22Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 09:04 UTC); cached (fm check --fresh reruns) [ran] [tree c025d7b27fcb] (2026-10-03T09:04:22Z)
- (audit adversary) `self: red→green on the same test command; the probe showed the false positive needs python named as a command in the body (shebang, a command line) plus a quoted protected path; only the interpreter gate drops the body, and only for quoted cat/tee heredocs with no pipe, substitution, ; or & on their line; the rest of the scan still reads the whole command` → piped (cat <<'E' | python3), chained (&& python3 f), unquoted (bodies expand) and real interpreter heredocs keep their bodies and stay blocked (tests); running the written file later is a separate command the guard reads on its own; the bash differential test passes [tree c025d7b27fcb] (2026-10-03T09:04:22Z)
- (audit self) `self: red→green on the same test command; the probe showed the false positive needs python named as a command in the body (shebang, a command line) plus a quoted protected path; only the interpreter gate drops the body, and only for quoted cat/tee heredocs with no pipe, substitution, ; or & on their line; the rest of the scan still reads the whole command` → no findings [tree c025d7b27fcb] (2026-10-03T09:04:22Z)
## Log
- 2026-10-03T08:54:00Z created
- 2026-10-03T09:02:32Z planned from capture
- 2026-10-03T09:02:32Z focused
- 2026-10-03T09:04:22Z done
- 2026-10-03T09:04:22Z committed 8fb3cb7 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research T-0158-review: Verdict: changes needed.** I found four verified bypasses and one regression. I could not run code here (read-only), so every trace is by hand ag…
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- T-0144 [SECURITY L, done, 3 steps] Guard: leave out only real top-level fm --run arguments from the interpreter claude-check (a fake --run in a heredoc or -c body hid co…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Ground a reviewer's proposed false positive with a probe before fixing it: the first body I wrote wasn't blocked at all; the real trigger was python named as a command in written text.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
