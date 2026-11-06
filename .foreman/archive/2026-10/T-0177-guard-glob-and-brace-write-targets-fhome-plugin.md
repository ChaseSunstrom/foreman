---
id: T-0177
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py,plugin/tests/test_guard.py,CHANGELOG.md,MASTER.md]
depends_on: []
source: self
created: 2026-10-03T09:52:56Z
updated: 2026-10-03T09:56:01Z
base: a6a51694b213ae7c0d24b827f3fa7ae3f7715ae6
base_tree: aa5825b1bfcdf09621922774662a47d1bfb804ae
verified: strong
---
# Guard: glob and brace write targets are checked as bash expands them
## Raw request
> Guard: glob and brace write targets (> {fhome}/plugin/li?/fmguard.py, > .../{lib}/fmguard.py) are taken as literal paths — evidence: T-0175 review finding 5 (pre-existing)
## Interpretation
T-0175 review finding 5: a write or tree target is classified as written, so > plugin/li?/fmguard.py (bash: the one existing match) and tee plugin/{lib,x}/fmguard.py (bash: two arguments) reach core unchecked. A redirect's {lib} without a comma stays literal in bash, so only comma lists and sequences matter.
## Assumptions (confidence)
## Acceptance criteria
- [x] glob and brace write targets are checked — verify with `python3 plugin/tests/run.py -k test_glob_and_brace_targets_are_checked`
## Non-goals
## Approach (options → choice → why)
A: in _target_cats, expand each resolved target into bash's alternatives — comma and sequence braces (innermost first, capped at 1024) and, for a part with * ? or [, the existing paths glob.glob matches — and classify each, plus the literal. B (rejected): treat any glob or brace target as unknown and fall back to the named-path scan — it can't see a match the command doesn't name (li? names nothing). Quoted globs are expanded too (the tokenizer drops quotes): over-checking only.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test rows (red)
2. [x] expand braces and globs in _target_cats
3. [x] gates, docs, audit
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (guard limits: expansions)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_glob_and_brace_targets_are_checked` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / FAILED (1 classes) [ran] [tree 76b08773a53b] (2026-10-03T09:53:43Z)
- (step 2) `python3 plugin/tests/run.py -k test_glob_and_brace_targets_are_checked` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / FAILED (1 classes) [ran] [tree e924786a4635] (2026-10-03T09:53:58Z)
- (step 2) `python3 plugin/tests/run.py -k test_glob_and_brace_targets_are_checked` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree dc56c444fa79] (2026-10-03T09:54:14Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.7    33.1     150  [0] / SessionEnd                  28.1    30.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:15 UTC; python3 plugin/tests/run.py → e [ran] [tree dc56c444fa79] (2026-10-03T09:54:54Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.6    32.3     150  [0] / SessionEnd                  27.5    30.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 09:15 UTC; python3 plugin/tests/run.py → e [ran] [tree f8c9524cf7de] (2026-10-03T09:56:00Z)
- (ac 1) `python3 plugin/tests/run.py -k test_glob_and_brace_targets_are_checked` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Core 0s) / OK [ran] [tree f8c9524cf7de] (2026-10-03T09:56:01Z)
- (audit intent) `self-review with a probe of the expansion (nested braces, sequences, the 1024 cap in 2 ms, lazy capped glob)` → the six review forms (? * [ ] globs, comma/sequence/nested braces) now block; {lib} without a comma and an unrelated /tmp glob don't, matching bash [tree f8c9524cf7de] (2026-10-03T09:56:01Z)
- (audit adversary) `self-review with a probe of the expansion (nested braces, sequences, the 1024 cap in 2 ms, lazy capped glob)` → a brace product past 1024 or a glob past 1024 matches is checked only that far (ponytail-marked); extglob @(…) and globstar ** need shopt first and aren't expanded (documented); quoted globs are expanded too, which only over-checks; touch isn't a write command to the guard (pre-existing, empty files only) [tree f8c9524cf7de] (2026-10-03T09:56:01Z)
## Log
- 2026-10-03T09:52:56Z created
- 2026-10-03T09:53:35Z planned from capture
- 2026-10-03T09:53:35Z focused
- 2026-10-03T09:56:01Z done
- 2026-10-03T09:56:01Z committed eab96c6 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0175 [SECURITY L, done, 3 steps] Guard: writes through a variable are checked — known NAME=literal values and $HOME resolve write, copy and cd targets (&& chains too);…
- research t0018-r5-maintainer: HIGH — plugin/lib/fmguard.py:188-198 (`_protected_roots`) vs plugin/lib/fmguard.py:165-171 (`_is_core`) — tree-write guard misses project-l…
- research t0018-final-adversary: HIGH** — `plugin/lib/fmguard.py:201-222` (`classify_tree` / `_new_context_file` / `_protected_roots`) — Tree-write commands (`cp -r`, `ta…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A path check is only as good as the path bash will really use: classify after the shell's own expansions (variables, braces, globs), not the word as typed.
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
