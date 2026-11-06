---
id: T-0176
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py,plugin/tests/test_guard.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: self
created: 2026-10-03T09:33:19Z
updated: 2026-10-03T18:41:33Z
base: eab96c63fb9536ea81ab20c4c8489a50cf6c7709
base_tree: f8c9524cf7de5e6cd3296cf5f5f905299a4908b1
verified: strong
---
# Guard: a python heredoc that provably writes only through open() counts only those files as written
## Raw request
> Guard interpreter writes: when a python heredoc provably writes only through open() on literal paths (no os/shutil/pathlib/subprocess, nothing dynamic), only those paths count as write targets, not every quoted string — evidence: T-0174 probe blocked because a replace() string mentioned .foreman
## Interpretation
Self item from T-0174's friction: an edit script fed to python whose replace() strings mention the mirror folder, and that writes only its own file, is blocked state-direct, because every quoted path in interpreter code counts as a write target. Relax it only where provable.
## Assumptions (confidence)
## Acceptance criteria
- [x] an edit script that provably writes one file counts only that file — verify with `python3 plugin/tests/run.py -k test_a_provable_python_edit_counts_only_its_open_targets`
## Non-goals
## Approach (options → choice → why)
A: for quoted heredocs fed straight to python (T-0170 units) with no other interpreter code around them, parse each; when it imports nothing beyond whitelisted pure functions of re, json, textwrap and sys (used only as module.attr from that list), calls nothing dynamic (the T-0170 list plus breakpoint and help), touches no dunder or frame attribute, never rebinds or passes the builtin open, and every write-mode open names a literal or a module-level name bound once to one, then builtin open is the only thing that can write and its paths are the targets. Anything else keeps the coarse rule. B (rejected): enumerate os, shutil and pathlib writers: module objects are reachable through other modules' attributes and os.replace has the same shape as str.replace, so it can't be proved.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] parse and prove the targets
3. [x] gates, docs, audit
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (guard limits: proved python writes)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_provable_python_edit_counts_only_its_open_targets` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) [ran] [tree d65cf0fed9e0] (2026-10-03T10:00:08Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_provable_python_edit_counts_only_its_open_targets` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes) [ran] [tree ef5656a65261] (2026-10-03T10:01:08Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_provable_python_edit_counts_only_its_open_targets` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 4f63786cb298] (2026-10-03T10:01:21Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    33.1     150  [0] / SessionEnd                  27.9    29.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:15 UTC; python3 plugin/tests/run.py → e [ran] [tree 4f63786cb298] (2026-10-03T10:02:03Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_provable_python_edit_counts_only_its_open_targets` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 0b3f4555925c] (2026-10-03T10:05:52Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.3    32.7     150  [0] / SessionEnd                  28.2    30.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:15 UTC; python3 plugin/tests/run.py → e [ran] [tree 0b3f4555925c] (2026-10-03T10:06:34Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_provable_python_edit_counts_only_its_open_targets` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 0b3f4555925c] (2026-10-03T18:41:33Z)
- (audit intent) `one fm-reviewer adversary pass plus the automated security review; every finding fixed or documented, with unit asserts that the proof refuses each attack script` → the friction (an edit script whose replace() strings name the mirror or a credential file, writing only its own file) is allowed; a proved script's open() targets are still classified [tree 0b3f4555925c] (2026-10-03T18:41:33Z)
- (audit adversary) `one fm-reviewer adversary pass plus the automated security review; every finding fixed or documented, with unit asserts that the proof refuses each attack script` → reviews found locals() reaching builtins.open or rebinding a trusted name, type(file) giving FileIO, module members passed on, PYTHONPATH on a continued line, a same-named module in the current folder, and mkdir -p assumed to succeed — fixed by an allowlist of plain builtins, refusing .open attributes, dunder strings and frame attributes, calling module members only directly, refusing python path settings and continued lines, checking searched folders for shadow modules, and counting mkdir -p only where it can be made; a union with the coarse targets was declined (those are exactly the false blocks removed). Remaining limit: obfuscated writes the coarse write-API test doesn't see (aliasing open, type() tricks) are allowed as before, now documented [tree 0b3f4555925c] (2026-10-03T18:41:33Z)
## Log
- 2026-10-03T09:33:19Z created
- 2026-10-03T09:59:58Z planned from capture
- 2026-10-03T09:59:58Z focused
- 2026-10-03T10:05:52Z review fixes (fm-reviewer + automated security review): builtins by allowlist (type/locals/object/super… out), no .open attribute or dunder string, module members only called directly or named as flags/exceptions, sys stdin/stdout/stderr dropped, PYTHONPATH-like settings and continued lines refuse the proof, a same-named module in a searched folder refuses it; mkdir -p counts for a cd only where it can be made
- 2026-10-03T18:41:33Z done
- 2026-10-03T18:41:33Z committed 83b91e8 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0170 [FIX M, done, 3 steps] Guard: 'driving Foreman's modules' reads real Python imports, not text that mentions them — lesson: Relax a guard by proving the safe case,…
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Prove a relaxation by allowlist, not denylist: every denylist the reviews probed (dynamic names, dunders, module attributes) had a hole (locals(), type(), a planted json.py) that an allowlist of plain builtins closes by construction.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- MASTER.md
- CHANGELOG.md
