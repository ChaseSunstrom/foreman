---
id: T-0669
type: SECURITY
tier: L
status: done
priority: urgent
scope: []
depends_on: []
source: discovered
created: 2026-10-09T15:33:09Z
updated: 2026-10-09T16:03:05Z
batch: [T-0577, T-0578, T-0579, T-0580, T-0582, T-0583, T-0584]
base: a7b6b7eb0ec48ca3ee92b94a2d36feb2fc28cf9c
base_tree: 93f725b649b59d464ee7e7f05da52af58323b2ba
verified: strong
---
# Guard hardening: fuzzer escape classes 2-5 and 7-9, one close-out run
## Raw request
> T-0577: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/guard_fuzz_escapes.txt): a backslash-newline inside single quotes that a second shell reads: eval 'claude plugin ins\<newline>tall x@y', bash -c 'r\<newline>m -rf ~', the same through trap. Fix so the fixture's open mark comes off; real-bash rows
> T-0578: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/guard_fuzz_escapes.txt): a backslash-newline inside double quotes joins a word the guard reads apart: "rm\<newline>" -rf ~. Fix so the fixture's open mark comes off; real-bash rows
> T-0579: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/guard_fuzz_escapes.txt): a case arm's ) ends a "$( … )" early in the guard's reading: echo "$(case a in a) r''m -rf ~;; esac)". Fix so the fixture's open mark comes off; real-bash rows
> T-0580: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/guard_fuzz_escapes.txt): $((1))#x inside "$( … )" hides a quoted name: … git ""push"" --force …. Fix so the fixture's open mark comes off; real-bash rows
> T-0582: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/guard_fuzz_escapes.txt): a quoted "x <<EOF" inside "$( … )" or backticks hides the next line. Fix so the fixture's open mark comes off; real-bash rows
> T-0583: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/guard_fuzz_escapes.txt): an escaped substitution in a string run by eval or sh -c: sh -c "echo \"\$(rm -rf ~)\"", eval "echo \`rm -rf ~\`", or one inside a heredoc. Fix so the fixture's open mark comes off; real-bash rows
> T-0584: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/guard_fuzz_escapes.txt): an escaped backtick in a heredoc inside backticks. Fix so the fixture's open mark comes off; real-bash rows
## Interpretation
Do T-0577, T-0578, T-0579, T-0580, T-0582, T-0583, T-0584 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0669.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0577: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/ works — verify with `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- [x] T-0578: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/ works — verify with `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- [x] T-0579: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/ works — verify with `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- [x] T-0580: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/ works — verify with `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- [x] T-0582: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/ works — verify with `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- [x] T-0583: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/ works — verify with `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- [x] T-0584: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/ works — verify with `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
## Non-goals
## Approach (options → choice → why)
One pass over the 16 open fixture rows (classes 2-5, 7-9, plus the two mixed rows 79-80) and the review's computed-name-reads-stdin step. Options per class: model the bash rule exactly (continuation removal when a second shell reads the text; case-arm parens; $((…))# not a comment; a quoted <<EOF is not a heredoc; one level of escape removal when eval/sh -c re-reads double-quoted text), or refuse the form outright when modelling is uncertain. Choice: model where it is a small rule, refuse otherwise; un-open every row at once (red), fix class by class running only the fixture test, then the full guard suites, replay and the default-seed fuzzer once at close.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0577: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/
2. [x] T-0578: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/
3. [x] T-0579: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/
4. [x] T-0580: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/
5. [x] T-0582: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/
6. [x] T-0583: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/
7. [x] T-0584: SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/
8. [x] review of T-0589/T-0587: a computed command name may read a heredoc or here-string as code (X=bash; $X <<EOF, $SHELL <<<)
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / FAILED (1 classes) [ran] [tree 2379420d317e] (2026-10-09T15:41:17Z)
- (step 2) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / OK [ran] [tree 981925cd1f98] (2026-10-09T16:02:22Z)
- (step 3) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / OK [ran] [tree 981925cd1f98] (2026-10-09T16:02:23Z)
- (step 4) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / OK [ran] [tree 981925cd1f98] (2026-10-09T16:02:23Z)
- (step 5) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / OK [ran] [tree 981925cd1f98] (2026-10-09T16:02:24Z)
- (step 6) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / OK [ran] [tree 981925cd1f98] (2026-10-09T16:02:24Z)
- (step 7) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / OK [ran] [tree 981925cd1f98] (2026-10-09T16:02:25Z)
- (step 8) `python3 plugin/tests/run.py -k ShellStdin` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: ShellStdin 0s) / OK [ran] [tree 981925cd1f98] (2026-10-09T16:02:25Z)
- (ac 1) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 2 tests in 2.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 2s) / OK [ran] [tree 793a5d5bf8fb] (2026-10-09T16:02:55Z)
- (ac 2) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 2 tests in 2.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 2s) / OK [ran] [tree 793a5d5bf8fb] (2026-10-09T16:02:55Z)
- (ac 3) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 2 tests in 2.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 2s) / OK [ran] [tree 793a5d5bf8fb] (2026-10-09T16:02:55Z)
- (ac 4) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 2 tests in 2.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 2s) / OK [ran] [tree 793a5d5bf8fb] (2026-10-09T16:02:55Z)
- (ac 5) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 2 tests in 2.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 2s) / OK [ran] [tree 793a5d5bf8fb] (2026-10-09T16:02:55Z)
- (ac 6) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 2 tests in 2.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 2s) / OK [ran] [tree 793a5d5bf8fb] (2026-10-09T16:02:55Z)
- (ac 7) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked` → exit 0 · Ran 2 tests in 2.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 2s) / OK [ran] [tree 793a5d5bf8fb] (2026-10-09T16:02:55Z)
- (audit intent) `self: all 16 open fixture rows un-opened at once (red), fixed class by class with only the fixture test per change; one close-out run of the guard, pipes, diff (fuzzer) and hooks suites green; 30-day replay: 0 newly blocked after narrowing two over-reads it caught (trimmed tails cutting quoted code; computed names reading every heredoc), 1 newly allowed = a JSON-reading python -c now parsed whole and proved data by the existing rule` → classes 2-5 and 7-9 blocked, plus the review's computed-name-reads-stdin case [tree 793a5d5bf8fb] (2026-10-09T16:02:55Z)
- (audit adversary) `self: all 16 open fixture rows un-opened at once (red), fixed class by class with only the fixture test per change; one close-out run of the guard, pipes, diff (fuzzer) and hooks suites green; 30-day replay: 0 newly blocked after narrowing two over-reads it caught (trimmed tails cutting quoted code; computed names reading every heredoc), 1 newly allowed = a JSON-reading python -c now parsed whole and proved data by the existing rule` → every new reading adds findings (tails, unescaped variants, unescaped heredoc ticks); the one newly allowed line is the existing data-python proof seeing correct code; comment quotes checked (mask is comment-aware) [tree 793a5d5bf8fb] (2026-10-09T16:02:55Z)
- (audit edge) `self: all 16 open fixture rows un-opened at once (red), fixed class by class with only the fixture test per change; one close-out run of the guard, pipes, diff (fuzzer) and hooks suites green; 30-day replay: 0 newly blocked after narrowing two over-reads it caught (trimmed tails cutting quoted code; computed names reading every heredoc), 1 newly allowed = a JSON-reading python -c now parsed whole and proved data by the existing rule` → heredocs inside $( ) still real when unquoted in their own context; trimmed tail only when the tail ends inside a quote [tree 793a5d5bf8fb] (2026-10-09T16:02:55Z)
- (audit intent) `self: all 16 open fixture rows un-opened at once (red), fixed class by class with only the fixture test per change; one close-out run of the guard, pipes, diff (fuzzer) and hooks suites green; 30-day replay: 0 newly blocked after narrowing two over-reads it caught (trimmed tails cutting quoted code; computed names reading every heredoc), 1 newly allowed = a JSON-reading python -c now parsed whole and proved data by the existing rule` → classes 2-5 and 7-9 blocked, plus the review's computed-name-reads-stdin case [tree 793a5d5bf8fb] (2026-10-09T16:03:04Z)
- (audit adversary) `self: all 16 open fixture rows un-opened at once (red), fixed class by class with only the fixture test per change; one close-out run of the guard, pipes, diff (fuzzer) and hooks suites green; 30-day replay: 0 newly blocked after narrowing two over-reads it caught (trimmed tails cutting quoted code; computed names reading every heredoc), 1 newly allowed = a JSON-reading python -c now parsed whole and proved data by the existing rule` → every new reading adds findings (tails, unescaped variants, unescaped heredoc ticks); the one newly allowed line is the existing data-python proof seeing correct code; comment quotes checked (mask is comment-aware) [tree 793a5d5bf8fb] (2026-10-09T16:03:04Z)
- (audit edge) `self: all 16 open fixture rows un-opened at once (red), fixed class by class with only the fixture test per change; one close-out run of the guard, pipes, diff (fuzzer) and hooks suites green; 30-day replay: 0 newly blocked after narrowing two over-reads it caught (trimmed tails cutting quoted code; computed names reading every heredoc), 1 newly allowed = a JSON-reading python -c now parsed whole and proved data by the existing rule` → heredocs inside $( ) still real when unquoted in their own context; trimmed tail only when the tail ends inside a quote [tree 793a5d5bf8fb] (2026-10-09T16:03:04Z)
- (audit operator) `self: all 16 open fixture rows un-opened at once (red), fixed class by class with only the fixture test per change; one close-out run of the guard, pipes, diff (fuzzer) and hooks suites green; 30-day replay: 0 newly blocked after narrowing two over-reads it caught (trimmed tails cutting quoted code; computed names reading every heredoc), 1 newly allowed = a JSON-reading python -c now parsed whole and proved data by the existing rule` → replay over 5000 real commands shows no new refusals, so no new friction for sessions; hook latency unchanged in the hooks suite [tree 793a5d5bf8fb] (2026-10-09T16:03:04Z)
- (audit maintainer) `self: all 16 open fixture rows un-opened at once (red), fixed class by class with only the fixture test per change; one close-out run of the guard, pipes, diff (fuzzer) and hooks suites green; 30-day replay: 0 newly blocked after narrowing two over-reads it caught (trimmed tails cutting quoted code; computed names reading every heredoc), 1 newly allowed = a JSON-reading python -c now parsed whole and proved data by the existing rule` → each rule sits in the helper it corrects (_lines, _join_continued, _subst_bodies, _heredoc_starts via _inner_quote, _readings) with a T-0669 note and a fixture row per class [tree 793a5d5bf8fb] (2026-10-09T16:03:04Z)
## Log
- 2026-10-09T15:33:09Z created
- 2026-10-09T15:40:39Z criterion 1 verify: `` → `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- 2026-10-09T15:40:39Z criterion 2 verify: `` → `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- 2026-10-09T15:40:40Z criterion 3 verify: `` → `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- 2026-10-09T15:40:40Z criterion 4 verify: `` → `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- 2026-10-09T15:40:40Z criterion 5 verify: `` → `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- 2026-10-09T15:40:40Z criterion 6 verify: `` → `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- 2026-10-09T15:40:40Z criterion 7 verify: `` → `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked -k test_fuzzed_forms_never_run_a_dangerous_call_unblocked`
- 2026-10-09T15:41:15Z set approved=True
- 2026-10-09T15:41:16Z focused
- 2026-10-09T16:03:04Z done
- 2026-10-09T16:03:05Z committed b70a350 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0158-review: Verdict: changes needed.** I found four verified bypasses and one regression. I could not run code here (read-only), so every trace is by hand ag…
- T-0576 [SECURITY M, done, 2 steps] Guard: ${IFS} as a word separator is read as bash splits it — lesson: A tokenizer that doesn't expand the separator variable can be to…
- T-0581 [SECURITY M, done, 2 steps] Guard: a download piped into a ( group ) is still piped, with a space or a line break before the paren — lesson: a subshell paren afte…
- decision 2026-10-04: Brainstorm pass 4: 4 grounded ideas (cd-prefixed python heredocs parsed by the guard, test lockout of the real claude, untrusted-text sinks in the a…
## Lessons
- batch close-out works: one red run for all rows, fixture-only checks per fix, and the single full run plus replay caught both over-reads the per-fix checks could not
## Files touched
- plugin/tests/fixtures/guard_fuzz_escapes.txt
- plugin/lib/fmguard.py
- plugin/tests/test_guard_pipes.py
- CHANGELOG.md
