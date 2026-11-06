---
id: T-0370
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-10-08T23:55:43Z
updated: 2026-10-09T00:30:25Z
base: e6687b769c0e8f1e6ac9180bdbfcf479aecccc44
base_tree: a705a7ee522399669ace08ba905778b1e8a55f04
verified: strong
---
# Guard: a $(…) substitution no longer turns off variable tracking, so a literal S=/tmp/… stays known
## Raw request
> Guard: an unresolved variable write target is guessed from every word in the command (fmguard.py:1402-1420), so a state path that only appears as an ls argument yields a state-direct block that can't be granted; guess only from the variable's own assignment (recon, low confidence: full command not in the digest)
## Interpretation
6 real blocks (2026-10-03..07, foreman, nixie, volt): f=$(ls <state>/…); …; S=/tmp/…/scratchpad; … > $S/file. _straight_line (fmguard.py:1143) counts the ( ) of $(…) as branching (_BRANCHY), so raw=None, env=None: no variable is tracked, $S is unknown and guessed from the ls argument (a state path) → state-direct, which can't be granted.
## Assumptions (confidence)
## Acceptance criteria
- [x] f=$(ls <state>); …; S=/tmp/…; echo > $S/x passes, and a variable set from a substitution, or a write through it, still blocks — verify with `python3 plugin/tests/run.py -k test_a_substitution_keeps_literal_variables_known`
## Non-goals
## Approach (options → choice → why)
(a) guess only from the variable's own assignment — needs the tracking that's off here anyway; (b) mask $(…)/`…` before the branch check: a substitution runs in a subshell, can't skip later commands or set this shell's variables, and its body is checked as a command of its own (T-0158); assignments from it stay unknown (_PART); len(raw)==len(cmds) still turns tracking off if the split disagrees; (c) leave it. Choice (b).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: the six real shapes pass; substitution-set variables stay unknown
2. [x] guard suite + fm replay corpus
## Resume here
<!-- auto -->
- 2026-10-09T00:21:46Z step 1/2: test-first: the six real shapes pass; substitution-set variables stay unknown
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py
- touched since last checkpoint: CHANGELOG.md, plugin/tests/test_guard.py, plugin/lib/fmguard.py
## Docs impact
CHANGELOG.md (T-0370, T-0374)
## Verification evidence
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: fm replay → ✗ exit 1 · 0 newly allowed (possible bypasses) / 2919 new to the corpus · fm replay --accept takes these verdicts as the baseline [ran] [tree d18c474b7aff] (2026-10-09T00:15:24Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.0    35.2     150  [0] / SessionEnd                  30.7    34.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 23:08 UTC; python3 plugin/tests/run.py → exit 0 · Ran 896 tests in [ran] [tree 4e928a51acd2] (2026-10-09T00:18:34Z)
- `python3 plugin/tests/run.py -k test_a_substitution_keeps_literal_variables_known` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree aa1623135cee] (2026-10-09T00:18:52Z)
- `python3 plugin/tests/run.py -k test_a_substitution_keeps_literal_variables_known` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree aa1623135cee] (2026-10-09T00:18:52Z)
- (step 1) `python3 plugin/tests/run.py -k test_a_substitution_keeps_literal_variables_known` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree 2728a8f5f003] (2026-10-09T00:23:42Z)
- (step 2) `python3 plugin/tests/run.py -p test_guard_diff.py` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree 2728a8f5f003] (2026-10-09T00:23:44Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: claude plugin test mods/foreman-ui → ✗ exit 1 · 1 fail / Ran 62 tests across 1 file. [3.08s] (pre-existing: it also failed before this task); fm replay → ✗ exit 1 · 0 newly allowed (possible bypasses) / 2919 new to the corpus · fm replay --accept takes these verdicts as the baseline (pre-existing: it also failed before this task) [ran] [tree 2728a8f5f003] (2026-10-09T00:25:13Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.6    33.4     150  [0] / SessionEnd                  29.7    31.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 62 tests across 1 file. [3.05s]; python3 plugin/tests/run.py → exit 0 · Ran 897 tests in 36.6s (221 classes, 16 at a time [ran] [tree 6c809bfbd73e] (2026-10-09T00:30:11Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_substitution_keeps_literal_variables_known` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree 6c809bfbd73e] (2026-10-09T00:30:25Z)
- (audit adversary) `adversary: real-bash differential (bubblewrap) on 16 new forms — each that runs rm -rf / or ~ is blocked, the friction shape runs a scratch rm and is allowed; replay 5000 commands 0 newly allowed / 0 newly blocked; the fm-reviewer pass was cut short by its safety classifier, the automated security review's printf finding fixed test-first` → masking only plain substitution bodies (no quote, escape, comment, heredoc, case); a value is never trusted before its own assignment; unset or unknown parts are tried empty; printf counts as a setter when its first word may become -v ($, backtick, a glob/brace after a -v prefix) [tree 6c809bfbd73e] (2026-10-09T00:30:25Z)
- (audit edge) `adversary: real-bash differential (bubblewrap) on 16 new forms — each that runs rm -rf / or ~ is blocked, the friction shape runs a scratch rm and is allowed; replay 5000 commands 0 newly allowed / 0 newly blocked; the fm-reviewer pass was cut short by its safety classifier, the automated security review's printf finding fixed test-first` → nested substitutions unwind innermost first; $((…)) stays a branch; a tail's head is blank, not a command; a format that starts with [ stays conservative (quotes are gone after tokenizing) [tree 6c809bfbd73e] (2026-10-09T00:30:25Z)
- (audit intent) `adversary: real-bash differential (bubblewrap) on 16 new forms — each that runs rm -rf / or ~ is blocked, the friction shape runs a scratch rm and is allowed; replay 5000 commands 0 newly allowed / 0 newly blocked; the fm-reviewer pass was cut short by its safety classifier, the automated security review's printf finding fixed test-first` → the 6 real state-direct false blocks pass; the unset-variable write to the guard file (found on the way) now blocks [tree 6c809bfbd73e] (2026-10-09T00:30:25Z)
- (audit operator) `adversary: real-bash differential (bubblewrap) on 16 new forms — each that runs rm -rf / or ~ is blocked, the friction shape runs a scratch rm and is allowed; replay 5000 commands 0 newly allowed / 0 newly blocked; the fm-reviewer pass was cut short by its safety classifier, the automated security review's printf finding fixed test-first` → guard latency unchanged (bench green); foreman-ui test fixed for Claude Code 2.1.295's compaction shape [tree 6c809bfbd73e] (2026-10-09T00:30:25Z)
## Log
- 2026-10-08T23:55:43Z created
- 2026-10-09T00:03:06Z planned from capture
- 2026-10-09T00:03:07Z set approved=True
- 2026-10-09T00:03:07Z focused
- 2026-10-09T00:07:20Z user updated Claude Code to 2.1.295
- 2026-10-09T00:11:17Z hypothesis: the backtick case fails because its tail starts 'ls …`; …' and the tail-head mask only ends at ')'
- 2026-10-09T00:11:44Z hypothesis 1 false (no backtick tail); cause: env tracking starts, dies at the backtick word, and fixed=pre is only set when tracking was off from the start
- 2026-10-09T00:12:25Z steer(self): prefix values were trusted before their own assignment (echo > $S/<guard>; S=/tmp/x passes): drop a name referenced before it is set; backtick case dropped (no real block used backticks)
- 2026-10-09T00:13:18Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-09T00:13:18Z scope: + T-0374's fix (unknown variables can be empty), same function and the same test
- 2026-10-09T00:21:46Z waiting on the adversary review; all gates green incl. replay (0 newly allowed/blocked); printf computed-first-word fix added after the automated security review
- 2026-10-09T00:21:46Z paused: focus moved to T-0373
- 2026-10-09T00:22:35Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-09T00:22:35Z focused
- 2026-10-09T00:23:41Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'plugin/tests/test_guard_diff.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-09T00:23:42Z scope: + test_guard_diff.py — the adversary pass runs the new cases under real bash in bubblewrap
- 2026-10-09T00:28:57Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'plugin/tests/test_guard_diff.py', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-09T00:28:57Z scope: + foreman-ui.test.tsx — Claude Code 2.1.295 refuses a compaction stand-in with no messages (needs text + toolUses); the gate's mod test failed before this task
- 2026-10-09T00:30:25Z done
- 2026-10-09T00:30:25Z committed 8734dbf (5 path(s))
- 2026-10-09T00:30:25Z includes T-0374: SECURITY: a write through a variable that is never set (echo x > $NOPE~/.claude/
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-20261008: 1. **Answer.** I could ground one improvement fully (the pipe-shell false block) and one partly (state-direct from guessed variable targets).…
- T-0183 [FIX M, done, 3 steps] Guard: unknown-target guesses come from the command's own words, pair up across unknown parts, and know a literal set once before any branc…
- T-0190 [FIX M, done, 3 steps] Guard: guesses never use a variable's own name; rm targets use literals set once before a branch — lesson: A replay gate turns a guard chan…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- similar finished tasks took 3–3 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- Before widening what the guard trusts, run the new trust under real bash with adversarial neighbours: each widening I tried (substitution masking, prefix values, printf) had a bypass that only a differential run made concrete
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- plugin/tests/test_guard_diff.py
- mods/foreman-ui/tests/foreman-ui.test.tsx
