---
id: T-0581
type: SECURITY
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: discovered
created: 2026-10-09T14:43:55Z
updated: 2026-10-09T14:52:23Z
base: f5734785abfe14500ebb59d7c6fea68ad5917215
base_tree: 7cc0ca1e9904b8d6a093499cf222c66ca0959554
verified: strong
---
# Guard: a download piped into a ( group ) is still piped, with a space or a line break before the paren
## Raw request
> SECURITY!: guard escape found by the T-0433 fuzzer (open fixture in plugin/tests/fixtures/guard_fuzz_escapes.txt): a download piped into | (bash) with a space, or |<newline>(bash) on the next line (T-0421 closed only |(bash)). Fix so the fixture's open mark comes off; real-bash rows
## Interpretation
The parser records the separator before a command as its op; 'curl … | (bash)' and '|<newline>(bash)' give bash the op '(' or ';(' — the pipe is lost, so pipe-shell never sees a shell reading a download (T-0421 caught only '|(' with no space).
## Assumptions (confidence)
## Acceptance criteria
- [x] the class-6 fuzz fixtures are blocked (open marks removed) — verify with `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked`
## Non-goals
## Approach (options → choice → why)
(A, chosen) keep the pipe in the op when a ( or { follows it across spaces or line breaks, at the root in _split, so every check sees the pipe. (B, rejected) patch only the pipe-shell check: other checks keyed on piped would stay wrong.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: un-open the class-6 fixtures
2. [x] _split keeps a pipe before ( or {
## Resume here
<!-- auto -->
- 2026-10-09T14:48:29Z step 1/2: test-first: un-open the class-6 fixtures
- git: foreman/build; 2 uncommitted: plugin/lib/fmguard.py, plugin/tests/fixtures/guard_fuzz_escapes.txt
- touched since last checkpoint: plugin/tests/fixtures/guard_fuzz_escapes.txt, plugin/lib/fmguard.py
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / FAILED (1 classes) [ran] [tree 8d441f64ce4f] (2026-10-09T14:48:04Z)
- (step 2) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / OK [ran] [tree c18d4ed03438] (2026-10-09T14:51:46Z)
- (ac 1) `python3 plugin/tests/run.py -k test_saved_fuzz_escapes_stay_blocked` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardAgainstBash 0s) / OK [ran] [tree 95e9b90f6d4a] (2026-10-09T14:52:18Z)
- (audit edge) `self: _split keeps piped/op across an empty ( token; probed | (bash), |\n(bash), | ( ( bash ) ), | { bash; }, echo hi | (cat) parses; guard+pipes+hooks suites green` → nested parens and brace group stay piped; a non-download pipe into ( ) is unchanged (op only) [tree 95e9b90f6d4a] (2026-10-09T14:52:18Z)
- (audit adversary) `self: _split keeps piped/op across an empty ( token; probed | (bash), |\n(bash), | ( ( bash ) ), | { bash; }, echo hi | (cat) parses; guard+pipes+hooks suites green` → | ( ( bash ) ) blocked; a security review of T-0576 raised IFS operator/set escapes, captured separately [tree 95e9b90f6d4a] (2026-10-09T14:52:18Z)
- (audit intent) `self: _split keeps piped/op across an empty ( token; probed | (bash), |\n(bash), | ( ( bash ) ), | { bash; }, echo hi | (cat) parses; guard+pipes+hooks suites green` → both class-6 fixtures un-opened and blocked; criterion's verify passes [tree 95e9b90f6d4a] (2026-10-09T14:52:23Z)
- (audit edge) `self: _split keeps piped/op across an empty ( token; probed | (bash), |\n(bash), | ( ( bash ) ), | { bash; }, echo hi | (cat) parses; guard+pipes+hooks suites green` → nested parens and brace group stay piped; a non-download pipe into ( ) is unchanged (op only) [tree 95e9b90f6d4a] (2026-10-09T14:52:23Z)
- (audit adversary) `self: _split keeps piped/op across an empty ( token; probed | (bash), |\n(bash), | ( ( bash ) ), | { bash; }, echo hi | (cat) parses; guard+pipes+hooks suites green` → | ( ( bash ) ) blocked; a security review of T-0576 raised IFS operator/set escapes, captured separately [tree 95e9b90f6d4a] (2026-10-09T14:52:23Z)
## Log
- 2026-10-09T14:43:55Z created
- 2026-10-09T14:47:53Z planned from capture
- 2026-10-09T14:47:53Z focused
- 2026-10-09T14:52:23Z done
- 2026-10-09T14:52:23Z committed f632a49 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0576 [SECURITY M, done, 2 steps] Guard: ${IFS} as a word separator is read as bash splits it — lesson: A tokenizer that doesn't expand the separator variable can be to…
- T-0421 [SECURITY M, done, 3 steps] Guard: any download on the line counts when a shell reads a pipe — lesson: Check the property (a download reaches a shell; a word may …
- T-0433 [SECURITY M, done, 3 steps] Guard fuzzer: mutated real-bash forms never run a dangerous call unblocked — lesson: A guard's own tests find what its authors imagine…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- similar finished tasks took 2–3 steps
## Lessons
- a subshell paren after a pipe arrives as its own token, so per-command flags (piped) must carry across it
## Files touched
- plugin/tests/fixtures/guard_fuzz_escapes.txt
- plugin/lib/fmguard.py
- CHANGELOG.md
