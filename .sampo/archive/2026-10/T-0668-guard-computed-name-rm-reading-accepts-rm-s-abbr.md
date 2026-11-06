---
id: T-0668
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:29:13Z
updated: 2026-10-09T15:33:04Z
base: 227a8f47617eff23507813b9278bf70abf9ac17d
base_tree: 616a34bc5801a4bdc970d03a1742251181183899
verified: strong
---
# Guard: computed-name rm reading accepts rm's abbreviated long options and stops at the first operand
## Raw request
> Guard: computed-name rm reading accepts rm's abbreviated long options and stops at the first operand
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] --rec/--forc and an invalid option after an operand still read as rm — verify with `python3 plugin/tests/run.py -k RmOptsOnly`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: RmOptsOnly rows
2. [x] _rm_opts_only: long-option prefixes, scan only up to the first operand
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k RmOptsOnly` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: RmOptsOnly 0s) / FAILED (1 classes) [ran] [tree d5cb34ea6849] (2026-10-09T15:29:22Z)
- (step 2) `python3 plugin/tests/run.py -k RmOptsOnly` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: RmOptsOnly 0s) / OK [ran] [tree ce0a4e4d937e] (2026-10-09T15:30:57Z)
- (step 2) `python3 plugin/tests/run.py -k RmOptsOnly -k EvalVars` → exit 0 · Ran 2 tests in 0.2s (2 classes, 16 at a time; slowest: EvalVarsAndComputedNames 0s, RmOptsOnly 0s) / OK [ran] [tree 881d36de6e2c] (2026-10-09T15:32:56Z)
- (ac 1) `python3 plugin/tests/run.py -k RmOptsOnly` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: RmOptsOnly 0s) / OK [ran] [tree ce7a7731b831] (2026-10-09T15:33:04Z)
- (audit adversary) `self: RmOptsOnly and EvalVars rows red then green; full suites, replay and fuzzer deferred to the guard batch's single close-out run (user: don't test every little change)` → abbreviated long options now count as recursive for plain rm too (a pre-existing hole); unknown computed names also read as bash -c and eval [tree ce7a7731b831] (2026-10-09T15:33:04Z)
- (audit self) `self: RmOptsOnly and EvalVars rows red then green; full suites, replay and fuzzer deferred to the guard batch's single close-out run (user: don't test every little change)` → no findings [tree ce7a7731b831] (2026-10-09T15:33:04Z)
## Log
- 2026-10-09T15:29:13Z created
- 2026-10-09T15:29:13Z focused
- 2026-10-09T15:33:04Z done
- 2026-10-09T15:33:04Z committed 0a77ebe (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0010 [SECURITY S, done, 2 steps] Reject abbreviated fm options so --allow can't be spelled past the guard
- T-0162 [SECURITY S, done, 3 steps] Guard: rm variable resolution stops at a computed command name — lesson: Every place the resolver reads a command word, ask what bash …
- research T-0338-review: Changes needed. I could not run anything (no execution tool), so each finding comes from tracing the code by hand. The two HIGH findings are bypa…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
- similar finished tasks took 2–3 steps
## Lessons
- getopt_long takes unique prefixes: any check keyed on a long option must accept its prefixes
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/lib/fmguard.py
- CHANGELOG.md
