---
id: T-0170
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-10-03T08:54:00Z
updated: 2026-10-03T09:13:09Z
base: 6fdf4c686f9ea47e1230d2b6b2a64c634bee3116
base_tree: c3a3299fe1f6c6010197225206fe1dfe8cd401e3
verified: strong
---
# Guard: 'driving Foreman's modules' reads real Python imports, not text that mentions them
## Raw request
> Guard: 'interpreter code driving Foreman's modules' should test real Python imports (ast Import/ImportFrom, __import__/import_module with a constant fm name) and fall back to the regex when parsing fails or exec/eval/compile/getattr appear; text that merely mentions import fmx stays allowed
## Interpretation
The check fires when the text 'import fm…' and a writer name both appear anywhere in a command, so a python heredoc whose strings merely mention them (an edit script that writes Foreman's own source) was blocked as driving Foreman's modules. Make it read real imports where it can prove them, and keep today's text match everywhere else.
## Assumptions (confidence)
## Acceptance criteria
- [x] A python heredoc whose strings mention import fmx and write_atomic isn't 'driving Foreman's modules'; a real import plus a writer, exec of such text, a syntax error, -c code and a cat heredoc later run with python3 all still are — verify with `python3 plugin/tests/run.py -k test_driving_foremans_modules`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) narrow the regex (e.g. require line starts): strings with newlines still fool it, and it can't see dynamic imports; (b) parse quoted heredocs fed straight to python with ast: a real Import/ImportFrom of an fm module plus a writer name blocks; exec, eval, compile, getattr, __import__, importlib or a syntax error falls back to the text match, and fm import text anywhere outside those parsed bodies (-c code, data heredocs, the shell) decides as today. Choice: (b): it only ever relaxes what it can prove, so every case it can't read stays blocked.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests
2. [x] _drives_fm with ast and the fallbacks
3. [x] CHANGELOG and MASTER
## Resume here
## Docs impact
MASTER (guard limits sentence) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_driving_foremans_modules` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) [ran] [tree 38fe257b0cac] (2026-10-03T09:08:01Z)
- (step 1) `python3 plugin/tests/run.py -k test_driving_foremans_modules` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) [ran] [tree 61fca0d8deaf] (2026-10-03T09:08:20Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → ✗ exit 1 · Ran 49 tests in 1.1s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, GitDestructive 0s) / FAILED (1 classes) [ran] [tree 61fca0d8deaf] (2026-10-03T09:08:21Z)
- (step 1) `python3 plugin/tests/run.py -k test_driving_foremans_modules` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 41a46778a6a8] (2026-10-03T09:08:53Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 49 tests in 1.1s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, GitDestructive 0s) / OK [ran] [tree 41a46778a6a8] (2026-10-03T09:08:54Z)
- (step 3) `grep -q T-0170 MASTER.md && grep -q T-0170 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 53d98c199183] (2026-10-03T09:09:43Z)
- (step 2) `python3 plugin/tests/run.py -k test_guard` → exit 0 · Ran 49 tests in 1.1s (18 classes, 16 at a time; slowest: GuardAgainstBash 1s, PluginChanges 0s, GitDestructive 0s) / OK [ran] [tree a96088998086] (2026-10-03T09:12:06Z)
- (step 3) `grep -q T-0170 MASTER.md && grep -q T-0170 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 5901b52e9db1] (2026-10-03T09:12:58Z)
- (ac 1) `python3 plugin/tests/run.py -k test_driving_foremans_modules` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 5901b52e9db1] (2026-10-03T09:13:09Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 09:12 UTC); cached (fm check --fresh reruns) [ran] [tree 5901b52e9db1] (2026-10-03T09:13:09Z)
- (audit intent) `Reviewer declined the adversary lens (it wouldn't construct bypasses); done in the main thread instead, defensively: the relaxation only passes parsed code that can't run what its strings hold. Six must-block forms plus five ways strings can still run (os.system, subprocess, a module it wrote then imports, pickle, dunder walking) are tests and block; heredoc parsing ends a body at or before bash does, so a mismatch only moves lines into the text-checked rest. Also closed an older gap: a writer imported under an alias.` → an edit script whose strings mention Foreman's modules is no longer 'driving' them (that block isn't covered by the standing core yes, which is why it kept stopping work); its writes still go through the core-path check [tree 5901b52e9db1] (2026-10-03T09:13:09Z)
- (audit adversary) `Reviewer declined the adversary lens (it wouldn't construct bypasses); done in the main thread instead, defensively: the relaxation only passes parsed code that can't run what its strings hold. Six must-block forms plus five ways strings can still run (os.system, subprocess, a module it wrote then imports, pickle, dunder walking) are tests and block; heredoc parsing ends a body at or before bash does, so a mismatch only moves lines into the text-checked rest. Also closed an older gap: a writer imported under an alias.` → relaxes only provably inert code: a fixed import allowlist, no exec/eval/getattr/process functions, no dunder access; everything else (other interpreters, -c, data heredocs, options before -, two heredocs on a line) is read as text as before; string-built imports were and stay a documented speed-bump limit [tree 5901b52e9db1] (2026-10-03T09:13:09Z)
## Log
- 2026-10-03T08:54:00Z created
- 2026-10-03T09:07:55Z planned from capture
- 2026-10-03T09:07:55Z focused
- 2026-10-03T09:13:09Z done
- 2026-10-03T09:13:09Z committed 3995245 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research t0036-maintainer: MEDIUM** — `~/.claude/foreman/plugin/lib/fmhooks.py:341-364` (`_pin_problem`) and `~/.claude/foreman/plugin/lib/fmguard.py…
- T-0144 [SECURITY L, done, 3 steps] Guard: leave out only real top-level fm --run arguments from the interpreter claude-check (a fake --run in a heredoc or -c body hid co…
- research t0016-adversary-r3: hemeral_5m_input_tokens":21309,"ephemeral_1h_input_tokens":0},"output_tokens":5,"service_tier":"standard","inference_geo":"not_available"},"…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Relax a guard by proving the safe case, not by listing the unsafe ones: an allowlist of imports plus a ban on exec-like calls is small enough to reason about; a blocklist of tricks never is.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
