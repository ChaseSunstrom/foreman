---
id: T-3223
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard_overrefusal.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T17:38:47Z
updated: 2026-11-05T18:28:03Z
base: 98a29e7fc0cf154a29032fa8d4981e9e886c433b
base_tree: 56dba25d3391f2bbb4de1084bebbfe50fc886e5c
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T18:19:39Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard_overrefusal.py, CHANGELOG.md]
verified: strong
unproven: [red]
---
# Guard over-refusal: a for loop over literal words with an unquoted $t and printf '%s=%s'…
## Raw request
> Guard over-refusal: a for loop over literal words with an unquoted $t and printf '%s=%s' plus $(command -v $t) is blocked as 'IFS may be changed on a line that splits words on it' though nothing sets IFS (2026-11-05)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a printf whose -v appears only later in its arguments (command -v inside a substitution) with a quoted format passes; printf -v with a computed name, a quoted "-v", or a first word that could expand to -v ($X, {-v,…}, backticks) beside an unquoted expansion stays refused — verify with `python3 plugin/tests/run.py test_guard_overrefusal test_guard test_guard_evasions test_guard_diff`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: the loop passes; the computed-name printf forms stay refused
2. [x] read printf's first word with quotes removed in its own rule
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_overrefusal.PrintfFirstWord` → ✗ exit 1 · Ran 2 tests in 1.9s (1 jobs, 16 at a time; slowest: PrintfFirstWord 0s) / FAILED (1 classes: test_guard_overrefusal.PrintfFirstWord) [ran] [tree d7b2a612a53e] [world 2f1906870a] (2026-11-05T18:20:22Z)
- (step 2) `python3 plugin/tests/run.py test_guard_overrefusal test_guard test_guard_evasions test_guard_diff test_guard_exec_vectors test_guard_pipes test_guard_cases` → ✗ exit 1 · Ran 336 tests in 65.6s (136 jobs, 16 at a time; slowest: Mutation 64s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 27s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 7d620a19bcc8] [world 2f1906870a] (2026-11-05T18:22:38Z)
- (step 2) `python3 plugin/tests/run.py test_guard_overrefusal test_guard test_guard_evasions test_guard_diff test_guard_exec_vectors test_guard_pipes test_guard_cases` → exit 0 · Ran 337 tests in 25.3s (131 jobs, 16 at a time; slowest: Mutation 25s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 12s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree 2cfb4e17bc3a] [world 2f1906870a] (2026-11-05T18:25:30Z)
- `python3 plugin/tests/run.py test_guard_overrefusal.PrintfFirstWord` → ✗ exit 1 · Ran 2 tests in 4.4s (1 jobs, 16 at a time; slowest: PrintfFirstWord 0s) / FAILED (1 classes: test_guard_overrefusal.PrintfFirstWord) (start tree + this task's tests) [ran] [tree 74b4a042feb3] [world 2f1906870a] (2026-11-05T18:25:38Z)
- `python3 plugin/tests/run.py test_guard_overrefusal.PrintfFirstWord` → exit 0 · Ran 2 tests in 1.2s (1 jobs, 16 at a time; slowest: PrintfFirstWord 0s) / OK [ran] [tree 74b4a042feb3] [world 2f1906870a] (2026-11-05T18:25:38Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_overrefusal test_guard test_guard_evasions test_guard_diff` → exit 0 · Ran 337 tests in 43.9s (120 jobs, 16 at a time; slowest: Mutation 43s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 22s, GuardAgainstBash.test_every_form_that_runs_a_dangero [ran] [tree ec07dfd8cea8] [world 2f1906870a] (2026-11-05T18:26:35Z)
- (audit adversary) `self + adversary: the printf rule now stops its gap at a quote or expansion, so it reads printf's own first word; tried quoted '-v' and "-v", -v$(...) glued, $X holding -v, {-v,...} brace and backtick first words: all refused; a later -v inside $(command -v ...) and quoted formats pass; replay of recorded commands (test_guard_cases) unchanged; known gap kept as before: fmt=-v; printf "$fmt" "$n" with no substitution is masked and unread, as it was` → every computed or hidden -v form in PrintfFirstWord stays refused; X=-vD printf now refused earlier, as system [tree ec07dfd8cea8] (2026-11-05T18:26:35Z)
- (audit edge) `self + adversary: the printf rule now stops its gap at a quote or expansion, so it reads printf's own first word; tried quoted '-v' and "-v", -v$(...) glued, $X holding -v, {-v,...} brace and backtick first words: all refused; a later -v inside $(command -v ...) and quoted formats pass; replay of recorded commands (test_guard_cases) unchanged; known gap kept as before: fmt=-v; printf "$fmt" "$n" with no substitution is masked and unread, as it was` → printf -v name with a plain name is still not a computed name; a -v after -- is still read as one (over, never under) [tree ec07dfd8cea8] (2026-11-05T18:26:35Z)
- (audit intent) `self + adversary: the printf rule now stops its gap at a quote or expansion, so it reads printf's own first word; tried quoted '-v' and "-v", -v$(...) glued, $X holding -v, {-v,...} brace and backtick first words: all refused; a later -v inside $(command -v ...) and quoted formats pass; replay of recorded commands (test_guard_cases) unchanged; known gap kept as before: fmt=-v; printf "$fmt" "$n" with no substitution is masked and unread, as it was` → the session's for loop with printf and command -v passes [tree ec07dfd8cea8] (2026-11-05T18:26:35Z)
- (audit self) `self + adversary: the printf rule now stops its gap at a quote or expansion, so it reads printf's own first word; tried quoted '-v' and "-v", -v$(...) glued, $X holding -v, {-v,...} brace and backtick first words: all refused; a later -v inside $(command -v ...) and quoted formats pass; replay of recorded commands (test_guard_cases) unchanged; known gap kept as before: fmt=-v; printf "$fmt" "$n" with no substitution is masked and unread, as it was` → no findings [tree ec07dfd8cea8] (2026-11-05T18:26:35Z)
## Log
- 2026-11-05T17:38:47Z created
- 2026-11-05T18:19:31Z planned: it has criteria and steps
- 2026-11-05T18:19:32Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard_overrefusal.py', 'CHANGELOG.md']
- 2026-11-05T18:19:33Z focused
- 2026-11-05T18:19:39Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T18:25:03Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard_overrefusal.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-11-05T18:25:03Z scope: test_guard.py's RmOutside row now reports system first (still refused); its rm-outside finding is pinned by a new test
- 2026-11-05T18:27:58Z done
- 2026-11-05T18:28:03Z committed b1cc0051 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0411-review: Verdict: changes needed.** I found three bypasses in `_expand_literal_loops`. I could not run bash (read-only), so each one is traced from the co…
- research T-1473-review: Verdict: changes needed.** I found one regression: a command the old code refused and the new code lets through. I read the code and did not run …
- research T-1929-review: Changes needed. The three caps are now unliftable and `check()` ordering is sound. One refusal in the same class is still liftable, and the `unan…
- decision 2026-11-03: [revisited: The rename's guard step comes first] [check: python3 plugin/tests/run.py test_guard_sampo] The rename's guard step comes first: Ward ref…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_guard.py, plugin/tests/test_rename_scan.py
## Why not caught
no over-refusal test had a printf whose arguments held a command -v; PrintfFirstWord adds it
## Lessons
- a regex hunting an option must stop at the first quote or expansion, or it finds the option inside a later argument
## Plan gaps
- failed first: step 1 failing tests: the loop passes; the computed-name printf forms stay refused
- failed first: step 2 read printf's first word with quotes removed in its own rule
## Files touched
- plugin/tests/test_guard_overrefusal.py
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py
- CHANGELOG.md
