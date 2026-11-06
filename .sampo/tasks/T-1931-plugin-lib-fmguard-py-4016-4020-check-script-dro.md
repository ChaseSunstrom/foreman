---
id: T-1931
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T07:20:37Z
updated: 2026-10-29T08:13:01Z
base: e03ea2bb35480d3649871922163b55119ad850a3
base_tree: e835d5b0c7d9c5fb5c3151124ebc060587f11bd5
plan0_at: 2026-10-29T08:08:49Z
plan0_scope: []
verified: strong
---
# - plugin/lib/fmguard.py:4016-4020 — `_check_script` drops "too deep" findings unless 3 scr
## Raw request
> - plugin/lib/fmguard.py:4016-4020 — `_check_script` drops "too deep" findings unless 3 scripts are chained (`len(_IN_SCRIPT) < 3`). Content nested past depth 4 inside a script file is then never read…
> (noticed by an agent; research T-1929-review)
## Interpretation
A script's own bash -c or eval nesting past the depth cap was dropped as no chain, so its innermost part was never read: rm -rf ~ five layers deep inside a script ran unrefused.
## Assumptions (confidence)
## Acceptance criteria
- [x] A script with rm -rf ~ under 5 bash -c or eval layers is refused as system and no grant lifts it; the same nesting around date passes — verify with `python3 plugin/tests/run.py test_guard_exec_vectors test_guard`
## Non-goals
## Approach (options → choice → why)
When _check_script drops a too-deep finding (fewer than 3 scripts in the chain), scan that chunk with _literal_scan and refuse its literal hits as system with a 'nested too deep to read in full' detail; _unread counts that detail so no grant lifts it; _hint says to flatten the layers. Rejected: refusing every too-deep script (5 of 330 real scripts nest deep, all clean); raising the depth cap (moves the hole, costs time).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Apply S/e1931.txt test-first: test red on HEAD, fix, green
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py -k test_a_script_nested_too_deep test_guard_exec_vectors` → ✗ exit 1 · Ran 43 tests in 2.3s (7 classes, 16 at a time; slowest: ScriptCache 1s, ScriptHook 1s, Review 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6858bdad2adf] (2026-10-29T08:09:01Z)
- `python3 plugin/tests/run.py -k test_a_script_nested_too_deep test_guard_exec_vectors` → exit 0 · Ran 43 tests in 1.5s (7 classes, 16 at a time; slowest: ScriptCache 1s, ScriptHook 1s, Review 0s) / OK [ran] [tree 6858bdad2adf] (2026-10-29T08:09:01Z)
- (step 1) `python3 plugin/tests/run.py test_guard_exec_vectors test_guard` → exit 0 · Ran 300 tests in 8.9s (88 classes, 16 at a time; slowest: Mutation 9s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 6858bdad2adf] (2026-10-29T08:09:13Z)
- (step 1) `python3 plugin/tests/run.py test_guard_exec_vectors test_guard test_guard_evasions test_hooks` → exit 0 · Ran 505 tests in 46.2s (114 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 33s, PreToolUse 29s) / OK [ran] [tree b315a806e29e] (2026-10-29T08:12:21Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_exec_vectors test_guard` → exit 0 · Ran 300 tests in 8.8s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree b315a806e29e] (2026-10-29T08:12:48Z)
- (audit intent) `One fm-reviewer pass: 1 HIGH (a wrapper script dropped the refusal) fixed test-first; grant and chain cases added; suffix now one constant; exact too-deep matching captured as T-1936. Guard case replay: 124 labelled, 0 drifted` → criterion met directly, under grants and through a wrapper script [tree b315a806e29e] (2026-10-29T08:12:48Z)
- (audit adversary) `One fm-reviewer pass: 1 HIGH (a wrapper script dropped the refusal) fixed test-first; grant and chain cases added; suffix now one constant; exact too-deep matching captured as T-1936. Guard case replay: 124 labelled, 0 drifted` → rm -rf ~ under 5 bash -c or eval layers is refused directly, under a system and rm-outside grant, and from a wrapper script [tree b315a806e29e] (2026-10-29T08:12:48Z)
- (audit edge) `One fm-reviewer pass: 1 HIGH (a wrapper script dropped the refusal) fixed test-first; grant and chain cases added; suffix now one constant; exact too-deep matching captured as T-1936. Guard case replay: 124 labelled, 0 drifted` → the same nesting around date passes; the literal scan runs only when a chunk was too deep [tree b315a806e29e] (2026-10-29T08:12:48Z)
- (audit maintainer) `One fm-reviewer pass: 1 HIGH (a wrapper script dropped the refusal) fixed test-first; grant and chain cases added; suffix now one constant; exact too-deep matching captured as T-1936. Guard case replay: 124 labelled, 0 drifted` → literals only, marked ponytail; a core write that deep still goes unseen [tree b315a806e29e] (2026-10-29T08:12:48Z)
## Log
- 2026-10-29T07:20:37Z created
- 2026-10-29T08:08:47Z set type=FIX, tier=M
- 2026-10-29T08:08:48Z planned: it has criteria and steps
- 2026-10-29T08:08:49Z focused
- 2026-10-29T08:12:59Z done
- 2026-10-29T08:13:01Z committed 914eef1b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1929-review: Changes needed. The three caps are now unliftable and `check()` ordering is sound. One refusal in the same class is still liftable, and the `unan…
- T-1813 [FEATURE M, dropped, 0 steps] FIX: guard 'script nests too deep to read' refuses a harmless 3-deep sh chain (fmguard.py:
- research T-1480-review: Verdict: changes needed.** This was a read-only review: I could not run anything, so neither finding has been executed against the guard. Both co…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
## Why not caught
The depth cap's no-chain branch had no test with a dangerous innermost command
## Lessons
- A finding that marks unread text must pass through every outer layer unchanged: test it through a wrapper script, not only directly
## Files touched
- plugin/lib/fmguard.py
- plugin/tests/test_guard_exec_vectors.py
- CHANGELOG.md
