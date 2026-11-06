---
id: T-1917
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-29T04:48:19Z
updated: 2026-10-29T05:35:37Z
base: 4f3b5f352f14bbcd33e24d7b10f30ab84b767f02
base_tree: 5a8fbaf2dff73ac2eaf0ac33bf3587d9e94cfab3
plan0_at: 2026-10-29T05:29:17Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Guard lets a quoted heredoc write a scratch draft that fm edit or an on-disk script reads
## Raw request
> FIX: the guard reads a quoted-marker heredoc written to a scratchpad .txt/.patch draft as interpreter code when its body names fm modules (fmguard _writes_unrun_source only exempts Foreman source paths); exempt data heredocs to non-executable scratch files, with adversarial cases (a later run of that file still blocks)
## Interpretation
Only the data-draft case relaxes; the guard never reads script files, so draft-then-run-existing-script in one command is no wider than the two-command form
## Assumptions (confidence)
## Acceptance criteria
- [x] A quoted heredoc writing a .txt/.patch/.diff/.md/.json draft under scratch, named again only as fm edit's input or an existing plain script's argument, is not 'driving Foreman's modules'; every other spelling (python3 draft, -c exec, glob, quotes, escapes, cd, symlinked or same-command script, .py, non-scratch, unquoted marker, PYTHONSTARTUP) still blocks — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
rejected: tell Claude to always use the Write tool for drafts (already the workaround; the block costs a turn each time, 87 blocks in the ledger)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Adversarial test first (allowed + blocked cases), red on the current guard
2. [x] Add _writes_unrun_draft, OR it into _interpreter_writes' heredoc filter; green
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 293 tests in 8.7s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree c3f8a73f7364] (2026-10-29T05:29:42Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 293 tests in 7.8s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree c3f8a73f7364] (2026-10-29T05:29:42Z)
- (step 1) `python3 plugin/tests/run.py test_guard.Heredocs` → ✗ exit 1 · run.py: no test matches test_guard.Heredocs [ran] [tree c3f8a73f7364] (2026-10-29T05:29:48Z)
- (step 1) `python3 plugin/tests/run.py test_guard.InterpreterWrites` → exit 0 · Ran 15 tests in 0.6s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree c3f8a73f7364] (2026-10-29T05:29:55Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_safety test_risk` → exit 0 · Ran 327 tests in 8.6s (96 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, SafetyGate 6s) / OK [ran] [tree c3f8a73f7364] (2026-10-29T05:30:04Z)
- (step 2) `python3 plugin/tests/run.py test_guard_cases test_guard_debris test_guard_diff test_guard_evasions test_guard_exec_vectors test_guard_git test_guard_hardening test_guard_mine test_guard_pipes test_guard test_guard_state_key test_guard_try test_safety test_risk` → exit 0 · Ran 327 tests in 8.6s (96 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, SafetyGate 6s) / OK [ran] [tree 6911a75f9eb4] (2026-10-29T05:35:02Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 293 tests in 7.9s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / OK [ran] [tree 6911a75f9eb4] (2026-10-29T05:35:25Z)
- (audit adversary) `one fm-reviewer pass, adversary-weighted: 3 bypasses ($? mid-word, -W/-X flag values, extglob), all red-tested then fixed` → d$?.txt, python3 -W/-X tool draft and shopt extglob @(…) now block; globs, quotes, expansion, cd, a second heredoc, a linked or new script, -m pdb and PYTHONSTARTUP still block [tree 6911a75f9eb4] (2026-10-29T05:35:25Z)
- (audit intent) `one fm-reviewer pass, adversary-weighted: 3 bypasses ($? mid-word, -W/-X flag values, extglob), all red-tested then fixed` → writing a scratch draft and feeding it to fm edit or an existing script is one command [tree 6911a75f9eb4] (2026-10-29T05:35:25Z)
- (audit edge) `one fm-reviewer pass, adversary-weighted: 3 bypasses ($? mid-word, -W/-X flag values, extglob), all red-tested then fixed` → .patch and .diff drafts pass; a .py draft, a repo-path draft and an unquoted heredoc still block [tree 6911a75f9eb4] (2026-10-29T05:35:25Z)
- (audit operator) `one fm-reviewer pass, adversary-weighted: 3 bypasses ($? mid-word, -W/-X flag values, extglob), all red-tested then fixed` → one regex pass per heredoc line that writes a scratch file; no cost elsewhere [tree 6911a75f9eb4] (2026-10-29T05:35:25Z)
- (audit maintainer) `one fm-reviewer pass, adversary-weighted: 3 bypasses ($? mid-word, -W/-X flag values, extglob), all red-tested then fixed` → each review fix carries a one-line why at its regex [tree 6911a75f9eb4] (2026-10-29T05:35:25Z)
## Log
- 2026-10-29T04:48:19Z created
- 2026-10-29T04:48:25Z set tier=S
- 2026-10-29T05:04:36Z planned from capture
- 2026-10-29T05:29:16Z focused
- 2026-10-29T05:35:35Z done
- 2026-10-29T05:35:37Z committed b58a8673 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- T-0766 [FIX S, done, 2 steps] Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman — lesson: a guard relaxation keyed on what a…
- T-0761 [FIX S, dropped, 2 steps] Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
none: the draft exemption is new in this task; its first tests missed name-hiding spellings, which the review's three cases now pin
## Lessons
- A guard exemption keyed on a filename must reject every way bash can spell that name differently from the guard's reading: strip specials only as whole words, never substrings.
## Plan gaps
- failed first: step 1 Adversarial test first (allowed + blocked cases), red on the current guard
## Files touched
- CHANGELOG.md
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py
