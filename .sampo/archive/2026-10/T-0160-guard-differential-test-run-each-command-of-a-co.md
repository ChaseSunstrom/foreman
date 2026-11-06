---
id: T-0160
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/tests/test_guard_diff.py, plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-10-03T07:19:59Z
updated: 2026-10-03T07:22:44Z
base: 11af2a100a4ee8c01de84e42a2fa2d1505cbb179
base_tree: 71b791d474ce6dfc08372041cbf1bcc394524500
verified: ok
---
# Guard differential test: real bash in a bubblewrap sandbox with logging stand-ins finds what check_bash misses
## Raw request
> Guard differential test: run each command of a corpus (the guard tests plus generated mutations: keywords, substitutions, quoting, heredocs, comments, variables) in real bash with logging stand-ins for rm, git, claude, curl on a temp PATH and HOME; any dangerous call the stand-ins log that check_bash didn't block is a bypass — finds the class of gaps hand-tracing found four of today
## Interpretation
Hand-tracing found four guard bypasses today (comments, keywords, quoted backticks, fm blanking); reviews keep finding more. A test that executes each form in real bash and compares with the guard's verdict finds the class mechanically.
## Assumptions (confidence)
## Acceptance criteria
- [x] every corpus form that runs a dangerous call in real bash is blocked by check_bash, and the corpus is not vacuous (each payload's plain form logs) — verify with `python3 plugin/tests/run.py -p test_guard_diff.py`
## Non-goals
## Approach (options → choice → why)
A) bubblewrap (read-only /, tmpfs /home, no network) + stand-in rm/git/claude first on PATH that log their argv; ~40 shell forms × 3 payloads; a dangerous logged call with no guard finding fails the test, listing each bypass; skipped where bwrap is missing. B) a pure-Python shell model: it would share the guard's blind spots. Choice A; obfuscation the guard doesn't claim to handle (computed command names) stays out of the corpus.
## Risks and rollback
## Execution prompt
## Steps
1. [x] the harness and corpus (red where the guard misses)
2. [x] fix what it finds, or record a limit
3. [x] docs: MASTER guard paragraph, CHANGELOG
## Resume here
## Docs impact
MASTER guard paragraph; CHANGELOG; RSI brief
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_guard_diff.py` → first run red: 5 runner forms × 3 payloads bypassed (setsid, trap, find -exec, flock, script -c); ~40 others blocked (2026-10-03T07:22:43Z)
- (step 2) `test_guard_diff.py + test_guard.py` → both OK after reading trap/script -c/find -exec and stripping setsid/flock/busybox (2026-10-03T07:22:43Z)
- (step 3) `fm check` → 553 tests OK (the differential test runs in the gate, <1 s) (2026-10-03T07:22:43Z)
- (ac 1) `python3 plugin/tests/run.py -p test_guard_diff.py` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree dc996a4de818] (2026-10-03T07:22:44Z)
- (audit intent) `self-review of the harness and the five fixes` → a mechanical check that the guard matches what bash really runs; it found a new class (runners) on its first run, fixed in the same task; the RSI brief now feeds it forms [tree dc996a4de818] (2026-10-03T07:22:44Z)
- (audit adversary) `self-review of the harness and the five fixes` → the sandbox is read-only except a temp tree and a tmpfs /home, no network, so a missed stand-in can't harm the machine; the stand-ins shadow rm/git/claude on PATH (absolute paths would bypass them, so the corpus avoids them); the test asserts it isn't vacuous (more dangerous runs than forms). Known out-of-scope: computed command names and variables (documented guard limit) [tree dc996a4de818] (2026-10-03T07:22:44Z)
## Log
- 2026-10-03T07:19:59Z created
- 2026-10-03T07:20:49Z planned from capture
- 2026-10-03T07:20:49Z focused
- 2026-10-03T07:21:53Z scope: plugin/lib/fmfriction.py — the RSI brief now asks for new differential-test forms (one sentence)
- 2026-10-03T07:22:44Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0144-review: Verdict:** changes needed. This is one MEDIUM finding in the guard, plus LOW cosmetic gaps in `clean()`. I had no execution tool, so every case b…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research T-0158-review: Verdict: changes needed.** I found four verified bypasses and one regression. I could not run code here (read-only), so every trace is by hand ag…
- T-0158 [SECURITY M, done, 3 steps] Guard: one quote-aware reader for command substitutions (nested, quoted, backticks) — lesson: Patch a text scanner one bypass at a tim…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Test a text-based guard against the real interpreter: the differential found in 0.6 s what reviews found one at a time
## Files touched
- plugin/tests/test_guard_diff.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmfriction.py
- plugin/lib/fmguard.py
