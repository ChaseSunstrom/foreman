---
id: T-0576
type: SECURITY
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: discovered
created: 2026-10-09T14:43:54Z
updated: 2026-10-09T14:46:59Z
base: 799455a0683728bb353850b0d4c4a3f8147e4e36
base_tree: 1c7534581e869b2794729d0fd4bd2140a929830f
verified: strong
---
# Guard: ${IFS} as a word separator is read as bash splits it
## Raw request
> SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/guard_fuzz_escapes.txt): ${IFS} as the space between words hides the command: rm${IFS}-rf ~, git${IFS}push …, timeout 5${IFS}rm -rf ~ (most of the fuzzer's 3.1k escapes). Fix so the fixture's open mark comes off; real-bash rows
## Interpretation
The fuzzer's biggest escape class: rm${IFS}-rf ~ — bash splits the expansion into words (default IFS is space/tab/newline), the guard reads one word 'rm${IFS}-rf' and sees no rm. Read $IFS / ${IFS…} as the space it is before parsing; when the line reassigns IFS and expands it, the split can't be known, so refuse.
## Assumptions (confidence)
## Acceptance criteria
- [x] every IFS escape in the fuzz fixtures is blocked (open mark removed) and the fuzz test still finds no new bypass — verify with `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
## Non-goals
## Approach (options → choice → why)
(A, chosen) substitute a space for every $IFS / ${IFS…} expansion right after continuation-joining in check_bash (every depth); a line that both assigns and expands IFS is refused. (B, rejected) model IFS splitting in the tokenizer: large and error-prone.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: un-open the IFS fixtures (they fail now)
2. [x] the substitution + reassign refusal in check_bash; real-bash rows
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / FAILED (1 classes) [ran] [tree 5b68ece8ce50] (2026-10-09T14:45:13Z)
- (step 2) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 2 tests in 3.0s (1 classes, 16 at a time; slowest: GuardAgainstBash 3s) / OK [ran] [tree 7cc0ca1e9904] (2026-10-09T14:46:42Z)
- (step 1) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: GuardAgainstBash 1s) / OK [ran] [tree 7cc0ca1e9904] (2026-10-09T14:46:50Z)
- (ac 1) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 2 tests in 8.0s (1 classes, 16 at a time; slowest: GuardAgainstBash 8s) / OK [ran] [tree 7cc0ca1e9904] (2026-10-09T14:46:58Z)
- (audit adversary) `self: substitution right after continuation joining, so every depth sees it; a line that sets and expands IFS refuses (system); 37 fixtures un-opened and blocked; guard + diff + hooks suites OK; fm replay 0 newly allowed of 5000` → ${IFS} variants with operators and ${#IFS}/${!IFS} are covered by the regex; a reassigned IFS is refused rather than modelled [tree 7cc0ca1e9904] (2026-10-09T14:46:58Z)
- (audit edge) `self: substitution right after continuation joining, so every depth sees it; a line that sets and expands IFS refuses (system); 37 fixtures un-opened and blocked; guard + diff + hooks suites OK; fm replay 0 newly allowed of 5000` → a quoted "${IFS}" becomes a quoted space, close to bash's literal IFS characters; harmless lines with IFS reassigned and expanded now refuse (rare) [tree 7cc0ca1e9904] (2026-10-09T14:46:58Z)
- (audit intent) `self: substitution right after continuation joining, so every depth sees it; a line that sets and expands IFS refuses (system); 37 fixtures un-opened and blocked; guard + diff + hooks suites OK; fm replay 0 newly allowed of 5000` → closes the fuzzer's largest escape class [tree 7cc0ca1e9904] (2026-10-09T14:46:58Z)
## Log
- 2026-10-09T14:43:54Z created
- 2026-10-09T14:45:01Z planned from capture
- 2026-10-09T14:45:02Z focused
- 2026-10-09T14:46:58Z done
- 2026-10-09T14:46:59Z committed f573478 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0411-review: Verdict: changes needed.** I found three bypasses in `_expand_literal_loops`. I could not run bash (read-only), so each one is traced from the co…
- T-0433 [SECURITY M, done, 3 steps] Guard fuzzer: mutated real-bash forms never run a dangerous call unblocked — lesson: A guard's own tests find what its authors imagine…
- T-0411 [FEATURE M, done, 3 steps] FEATURE: the guard reads a for loop over literal words (for w in agent-a agent-b; do … $w — lesson: A text rewrite ahead of the guard m…
- decision 2026-10-04: Brainstorm pass 4: 4 grounded ideas (cd-prefixed python heredocs parsed by the guard, test lockout of the real claude, untrusted-text sinks in the a…
## Lessons
- A tokenizer that doesn't expand the separator variable can be told any word boundary: normalise it before parsing.
## Files touched
- plugin/tests/fixtures/guard_fuzz_escapes.txt
- plugin/lib/fmguard.py
- CHANGELOG.md
