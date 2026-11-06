---
id: T-1605
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/tests/test_guard_hardening.py, plugin/tests/test_guard_evasions.py, plugin/tests/fixtures/gen_evasions.py, plugin/tests/fixtures/guard_evasions.jsonl, plugin/tests/fixtures/guard_gaps.jsonl, plugin/tests/fixtures/guard_untested.json, plugin/tests/fixtures/guard_cases.jsonl, plugin/lib/fmguard.py, plugin/lib/fmmutate.py, plugin/lib/fmreplay.py, plugin/tests/test_replay.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-22T20:38:48Z
updated: 2026-10-22T21:47:35Z
base: 1e291de418f740669423430edeade723ef4741c7
base_tree: 51fd4b8c8fa1c0091069b6514d477d721bd3b198
plan0_at: 2026-10-22T21:31:49Z
plan0_scope: [plugin/tests/test_guard_hardening.py, plugin/tests/test_guard_evasions.py, plugin/tests/fixtures/gen_evasions.py, plugin/tests/fixtures/guard_evasions.jsonl, plugin/tests/fixtures/guard_gaps.jsonl, plugin/tests/fixtures/guard_untested.json, plugin/lib/fmguard.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Guard mutation and seeded evasions (from T-1553)
## Raw request
> Guard mutation and seeded evasions (from T-1553)
## Interpretation
Two guard ratchets. (1) Mutation: for each guard category the labelled corpora (guard_cases, guard_allow, guard_evasions) are refused with, a mutant guard that lets that category through must turn the corpus red; the categories no case exercises are listed in plugin/tests/fixtures/guard_untested.json, and that list may only shrink. (2) Seeded stacked evasions: gen_evasions.py composes two obfuscations per variant (a fixed seed picks 3 pairs per dangerous command, composed only where the shell still runs the original), regenerates the corpus, and a gap that lets a dangerous command through fails the test instead of being written down. The T-1553 oracle checks, where bwrap exists, that each stacked variant really runs the original program.
## Assumptions (confidence)
## Acceptance criteria
- [x] a mutated guard rule (fm mutate) turns the labelled corpus red; gen_evasions grows a seeded set whose new gaps fail the ratchet — verify with `cd plugin/tests && python3 -m unittest test_guard_hardening.Mutation`
## Non-goals
## Approach (options → choice → why)
Options: run fm bench guard --mutate in the test (tens of seconds per mutant: too slow for the suite); random fuzzing at each run (not reproducible, flaky); an in-process category mutant over the labelled corpora plus a fixed-seed stacked generator whose output is committed. Choice: the last: fast, deterministic, and every new gap is a reviewed regeneration; fm bench guard --mutate stays the deep per-rule check. Only tightens or explains the guard.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: Mutation class, stacked rows, no dangerous gap
2. [x] seeded stacks in gen_evasions and the untested ratchet file; regenerate
3. [x] tighten the guard for any stacked variant that gets through
4. [x] review fixes: per-rule mutant, green baseline, in-bash stacks refused for the payload, sh-fed stacks checked one layer down, shrink-only against HEAD
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_hardening` → red as expected (exit 1) · Ran 19 tests in 1.4s (3 classes, 16 at a time; slowest: Oracle 1s, Mutation 0s, NoSandbox 0s) / FAILED (1 classes) [ran] [tree 4d00ba964988] (2026-10-22T21:32:41Z)
- (step 2) `python3 -I plugin/tests/fixtures/gen_evasions.py && git diff --quiet -- plugin/tests/fixtures/guard_gaps.jsonl && python3 plugin/tests/run.py test_guard_evasions test_guard_hardening.Mutation` → exit 0 · Ran 8 tests in 5.8s (2 classes, 16 at a time; slowest: Mutation 6s, GuardEvasions 1s) / OK [ran] [tree d55fcc2c48a7] (2026-10-22T21:34:47Z)
- (step 3) `python3 plugin/tests/run.py test_guard_hardening.Mutation.test_no_evasion_reaches_a_dangerous_command test_guard_hardening.Mutation.test_a_stack_inside_bash_still_runs_the_original` → exit 0 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: Mutation 1s) / OK [ran] [tree d55fcc2c48a7] (2026-10-22T21:34:48Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Mutation` → exit 0 · Ran 5 tests in 5.514s / OK [ran] [tree d55fcc2c48a7] (2026-10-22T21:34:54Z)
- (step 4) `python3 plugin/tests/run.py test_guard_hardening test_guard_cases test_guard_evasions` → exit 0 · Ran 49 tests in 9.4s (6 classes, 16 at a time; slowest: Mutation 9s, GuardCases 3s, Oracle 3s) / OK [ran] [tree 63373cbf2816] (2026-10-22T21:41:47Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Mutation` → exit 0 · Ran 7 tests in 8.456s / OK [ran] [tree 63373cbf2816] (2026-10-22T21:41:56Z)
- (step 3) `fm bench guard --mutate --only plugin --max 2 --timeout 600` → ✗ exit 1 (never ran: no tests ran) · Ran 226 tests in 9.3s (67 classes, 16 at a time; slowest: GuardCases 9s, GuardAgainstBash 8s, GuardMine 4s) / FAILED (1 classes) [ran] [tree 63373cbf2816] (2026-10-22T21:42:11Z)
- (step 3) `python3 plugin/tests/run.py test_replay` → red as expected (exit 1) · Ran 10 tests in 3.1s (3 classes, 16 at a time; slowest: Replay 3s, GuardCases 0s, Core 0s) / FAILED (1 classes) [ran] [tree 402cf44378e0] (2026-10-22T21:44:25Z)
- (step 3) `python3 plugin/tests/run.py test_replay && fm bench guard --mutate --only plugin --max 3 --timeout 600` → exit 0 · Guard mutation (drop): 3 of 8 mutants, 3 killed, 0 survived / not mutated (no rule site found): confirm [ran] [tree 23df35f3cde7] (2026-10-22T21:46:05Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Mutation` → exit 0 · Ran 7 tests in 8.692s / OK [ran] [tree bc1b48575274] (2026-10-22T21:46:23Z)
- (audit adversary) `fm-reviewer adversary pass (research/T-1605-review.md)` → per-rule mutant (findings filtered, next rule decides); in-bash stacks must trip a payload rule the plain command trips; 57 stacked variants all refused, no dangerous gap allowed [tree bc1b48575274] (2026-10-22T21:46:44Z)
- (audit edge) `review edge lens` → green baseline required before mutants; every dangerous command gets STACKS stacks; sha256 ordering, no random [tree bc1b48575274] (2026-10-22T21:46:44Z)
- (audit operator) `fm bench guard --mutate --only plugin --max 3 run for real` → 3 of 8 plugin mutants, 3 killed, 0 survived; the runner's copy works again (broken since T-1263) [tree bc1b48575274] (2026-10-22T21:46:44Z)
- (audit maintainer) `review maintainer lens` → sh-fed stacks checked one layer down by the oracle; untested list compared with HEAD so it only shrinks; unused import removed [tree bc1b48575274] (2026-10-22T21:46:45Z)
- (audit intent) `criterion: a mutated rule turns the labelled corpus red; seeded stacks whose new gaps fail the ratchet; names fm mutate` → met: Mutation class (7 tests) plus a real fm bench guard --mutate run; untested rules 7 → 4 (state-direct, confirm, confine, brief; confirm has no rule site) [tree bc1b48575274] (2026-10-22T21:46:45Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard_hardening.Mutation` → exit 0 · Ran 7 tests in 7.896s / OK [ran] [tree bc1b48575274] (2026-10-22T21:46:58Z)
- (audit adversary) `one fm-reviewer five-lens pass; 6 findings fixed test-first; a real AST-mutant run killed 3/3` → per-rule mutants and payload-aware stack checks [tree bc1b48575274] (2026-10-22T21:46:58Z)
- (audit edge) `one fm-reviewer five-lens pass; 6 findings fixed test-first; a real AST-mutant run killed 3/3` → green baseline, stack counts, version-independent seeding [tree bc1b48575274] (2026-10-22T21:46:58Z)
- (audit intent) `one fm-reviewer five-lens pass; 6 findings fixed test-first; a real AST-mutant run killed 3/3` → met with the Mutation class and a real fm bench guard --mutate run; untested rules 7 to 4 [tree bc1b48575274] (2026-10-22T21:46:58Z)
## Log
- 2026-10-22T20:38:48Z created
- 2026-10-22T20:48:13Z grounding: mutation testing already exists (fmmutate.py, fm bench guard --mutate, T-1066; fmreplay.mutate gives the categories a corpus catches). Remaining: (1) a Mutation test class: every guard category with a labelled block case, and a ratchet listing the categories no labelled case catches (may only shrink); (2) gen_evasions.py: seeded stacked obfuscations (random.Random(fixed seed), pairs of transforms over the dangerous commands), regenerated, with block->allow gaps failing the test; (3) fm replay --oracle (T-1553) as a second judge over the evasion corpus.
- 2026-10-22T21:31:43Z set scope=['plugin/tests/test_guard_hardening.py', 'plugin/tests/test_guard_evasions.py', 'plugin/tests/fixtures/gen_evasions.py', 'plugin/tests/fixtures/guard_evasions.jsonl', 'plugin/tests/fixtures/guard_gaps.jsonl', 'plugin/tests/fixtures/guard_untested.json', 'plugin/lib/fmguard.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T21:31:48Z focused
- 2026-10-22T21:34:13Z set scope=['plugin/tests/test_guard_hardening.py', 'plugin/tests/test_guard_evasions.py', 'plugin/tests/fixtures/gen_evasions.py', 'plugin/tests/fixtures/guard_evasions.jsonl', 'plugin/tests/fixtures/guard_gaps.jsonl', 'plugin/tests/fixtures/guard_untested.json', 'plugin/tests/fixtures/guard_cases.jsonl', 'plugin/lib/fmguard.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T21:44:21Z set scope=['plugin/tests/test_guard_hardening.py', 'plugin/tests/test_guard_evasions.py', 'plugin/tests/fixtures/gen_evasions.py', 'plugin/tests/fixtures/guard_evasions.jsonl', 'plugin/tests/fixtures/guard_gaps.jsonl', 'plugin/tests/fixtures/guard_untested.json', 'plugin/tests/fixtures/guard_cases.jsonl', 'plugin/lib/fmguard.py', 'plugin/lib/fmmutate.py', 'plugin/lib/fmreplay.py', 'plugin/tests/test_replay.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T21:44:21Z scope: fmmutate.py, fmreplay.py, test_replay.py: fm bench guard --mutate's baseline has failed in its plugin-only copy since T-1263 (test_guard_evasions imports site/bench_safety.py); the criterion names fm mutate, so the runner must copy that file
- 2026-10-22T21:47:33Z done
- 2026-10-22T21:47:35Z committed e9576124 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- research T-1263-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I could only read files here, so I did…
- T-1263 [SECURITY M, done, 3 steps] Guard evasion corpus for the 24 dangerous commands, and an audit of a cloned repo's .claude config — lesson: A guard corpus that store…
- decision 2026-10-22: T-1422: dropped the plan reach lint (hosts/paths in a planner's plan → refuse). Two reviews (research T-1422-review, -review2) showed it either refu…
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
the first mutant was written as a verdict filter, not a findings filter
## Lessons
- A category-level mutant must drop only that rule's findings and let the next rule decide; nulling the whole verdict credits a rule with cases another rule really catches
## Plan gaps
- added late: review fixes: per-rule mutant, green baseline, in-bash stacks refused for the payload, sh-fed stacks checked one layer …
## Files touched
- plugin/tests/test_guard_hardening.py
- plugin/tests/fixtures/gen_evasions.py
- plugin/tests/fixtures/guard_evasions.jsonl
- plugin/tests/fixtures/guard_untested.json
- plugin/tests/fixtures/guard_cases.jsonl
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_replay.py
- plugin/lib/fmmutate.py
- plugin/lib/fmreplay.py
