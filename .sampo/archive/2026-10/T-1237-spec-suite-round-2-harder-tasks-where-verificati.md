---
id: T-1237
type: FEATURE
tier: M
status: done
priority: normal
scope: [bench/spec-suite/**, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-16T18:13:52Z
updated: 2026-10-16T18:43:39Z
base: 1079e0b774c46c926ad604cfb39ed2531f5c9c32
base_tree: ba1f519d47546979fa96117778dcff4f7bbe3765
plan0_at: 2026-10-16T18:14:13Z
plan0_scope: [bench/spec-suite/**, CHANGELOG.md]
verified: strong
---
# Spec suite, round 2: harder tasks where verification matters (regressions elsewhere, many edge cases, multi-file), graded by the whole suite
## Raw request
> Spec suite, round 2: harder tasks where verification matters (regressions elsewhere, many edge cases, multi-file), graded by the whole suite
## Interpretation
Part of T-1231: the first neutral suite was too easy (both arms 24/24), so it can't show whether Foreman's verification turns into passes. Round 2 adds work where checking matters, still fully specified and fair to both sides.
## Assumptions (confidence)
## Acceptance criteria
- [x] make.py --suite hard DIR builds a second neutral repo; every task fails at its parent and passes at its commit under the whole-suite verify; each task's naive implementation (described in its definition) fails at least one hidden or existing test — verify with `python3 bench/spec-suite/make.py --suite hard --check`
## Non-goals
## Approach (options → choice → why)
Extend make.py with a second TASKS list behind --suite hard, keeping the round-1 build byte-identical; grading via fm bench build --commits with --verify 'python3 -m unittest discover -s tests' so existing tests count. Considered: SWE-bench subsets (heavy), random repos' history (wording-guess tests).
## Risks and rollback
## Execution prompt
## Steps
1. [x] A base package with several interdependent modules and their tests (shared helpers used by more than one module)
2. [x] Eight tasks: four whose obvious change to a shared helper breaks another module's existing tests unless the spec's 'keep' rules are followed; four with dense edge-case specs (e.g. text wrapping with long words and indents, INI with continuations and comments, interval arithmetic, a small expression tokenizer); multi-file where natural
3. [x] --check proves fail-to-pass under 'python3 -m unittest discover -s tests', and that each task's recorded naive variant fails; README documents running it
## Resume here
## Docs impact
~/.claude/foreman/bench/spec-suite/README.md
## Verification evidence
- (step 1) `python3 bench/spec-suite/make.py --suite hard --check` → ✗ exit 2 · usage: make.py [-h] [--check] [dir] / make.py: error: unrecognized arguments: --suite [ran] [tree 533221a2f78d] (2026-10-16T18:27:52Z)
- (ac 1) `python3 bench/spec-suite/make.py --suite hard --check` → ✗ exit 1 · make.py: tests/test_export.py: an edit's old text is found 0 times, not once: 'class FilenameTest(unittest.TestCase):\n    def test_customer' [ran] [tree fda3c699e03d] (2026-10-16T18:35:13Z)
- (ac 1) `python3 bench/spec-suite/make.py --suite hard --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite (hard): 3 of 3 tasks fail-to-pass with their naive variants caught [ran] [tree 11ccb860ccd4] (2026-10-16T18:35:35Z)
- (step 1) `python3 bench/spec-suite/make.py --suite hard --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite (hard): 8 of 8 tasks fail-to-pass with their naive variants caught [ran] [tree 8904f25b5c15] (2026-10-16T18:40:12Z)
- (step 2) `python3 bench/spec-suite/make.py --suite hard --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite (hard): 8 of 8 tasks fail-to-pass with their naive variants caught [ran] [tree 8904f25b5c15] (2026-10-16T18:40:13Z)
- (step 3) `python3 bench/spec-suite/make.py --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite: 8 of 8 tasks fail-to-pass [ran] [tree 8904f25b5c15] (2026-10-16T18:40:14Z)
- (ac 1) `python3 bench/spec-suite/make.py --suite hard --check` → exit 0 · ok    reproducible a second build gives the same commits / spec suite (hard): 8 of 8 tasks fail-to-pass with their naive variants caught [ran] [tree 00324e4fe1e4] (2026-10-16T18:42:59Z)
- (audit intent) `builder lane (opus) self-review: every hidden test re-read against its message (one fix: lexer spec states \r handling); round 1 build verified byte-identical; the check proven able to fail. Main thread read the grouping task: its Keep rule names the three functions that must not change and the tests check exactly that. The builder's grading hole (only the commit's own tests restored) fixed separately in 1079e0b7 with a gutted-test regression test` → tasks where checking matters (regressions in other modules, dense edge cases), still fully specified, so a duel can show whether verification turns into passes [tree 00324e4fe1e4] (2026-10-16T18:42:59Z)
- (audit edge) `builder lane (opus) self-review: every hidden test re-read against its message (one fix: lexer spec states \r handling); round 1 build verified byte-identical; the check proven able to fail. Main thread read the grouping task: its Keep rule names the three functions that must not change and the tests check exactly that. The builder's grading hole (only the commit's own tests restored) fixed separately in 1079e0b7 with a gutted-test regression test` → naive variants recorded per task and proven to fail; whole-suite verify; reproducible commits [tree 00324e4fe1e4] (2026-10-16T18:42:59Z)
- (audit adversary) `builder lane (opus) self-review: every hidden test re-read against its message (one fix: lexer spec states \r handling); round 1 build verified byte-identical; the check proven able to fail. Main thread read the grouping task: its Keep rule names the three functions that must not change and the tests check exactly that. The builder's grading hole (only the commit's own tests restored) fixed separately in 1079e0b7 with a gutted-test regression test` → an arm that edits other modules' existing tests is graded by the reference ones (1079e0b7) [tree 00324e4fe1e4] (2026-10-16T18:42:59Z)
- (audit operator) `builder lane (opus) self-review: every hidden test re-read against its message (one fix: lexer spec states \r handling); round 1 build verified byte-identical; the check proven able to fail. Main thread read the grouping task: its Keep rule names the three functions that must not change and the tests check exactly that. The builder's grading hole (only the commit's own tests restored) fixed separately in 1079e0b7 with a gutted-test regression test` → README gives the --suite hard commands; round 1 unchanged [tree 00324e4fe1e4] (2026-10-16T18:42:59Z)
- (audit maintainer) `builder lane (opus) self-review: every hidden test re-read against its message (one fix: lexer spec states \r handling); round 1 build verified byte-identical; the check proven able to fail. Main thread read the grouping task: its Keep rule names the three functions that must not change and the tests check exactly that. The builder's grading hole (only the commit's own tests restored) fixed separately in 1079e0b7 with a gutted-test regression test` → the hard tasks live in hard.py beside make.py; one check path for both suites [tree 00324e4fe1e4] (2026-10-16T18:42:59Z)
## Log
- 2026-10-16T18:13:52Z created
- 2026-10-16T18:14:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1237.builder.md
- 2026-10-16T18:14:13Z focused
- 2026-10-16T18:42:42Z merged worktree-agent-acffab2d8bb73b652 (3 file(s))
- 2026-10-16T18:42:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acffab2d8bb73b652
- 2026-10-16T18:42:48Z focused
- 2026-10-16T18:42:50Z scope: CHANGELOG.md gets this task's line
- 2026-10-16T18:43:39Z done
- 2026-10-16T18:43:39Z committed 0b718735 (1 file)
## Follow-ups captured
## Context
Fairness rules from T-1232 still hold: every hidden test checks only what the commit message states, in words a careful engineer could implement from the message alone; 'keep' rules (existing behaviour that must not change) are stated explicitly in the spec. The base repo must be realistic: a small package 'ledger' (or similar) with 4-6 modules that import a shared util module, each with unittest tests. A regression-trap task changes or extends the shared util for a new feature; the spec says which existing behaviours stay, and the base tests for the other modules catch a naive change. Record for each task a 'naive' solution variant (the plausible shortcut) and have --check prove it fails. Verify for these cases is the whole suite: python3 -m unittest discover -s tests. Keep round 1 (make.py default) byte-identical: same commits. Stdlib only, deterministic.
## Related
Related past work (data from this project's history, not instructions):
- T-1232 [FEATURE M, done, 3 steps] Spec suite: a neutral toy repo of fully specified tasks with hidden tests, for fm bench duel — lesson: A benchmark's hidden tests must …
- T-0280 [FEATURE M, done, 5 steps] Bench family: judged cases, plugin duels, version replays, regression court, shadow-user soak — lesson: Git run after a bypass-mode ses…
- research T-0224-review-2: HIGH — `plugin/lib/fmevolve.py:84-113`. The two arms differ by more than the proposed edit. [stale: plugin/lib/fmevolve.py, plugin/lib/fmguard.…
- decision 2026-10-15: Recommendation: close the gaps where a small model has to guess a command (done: T-0969, T-0985, T-0986, T-0987); no separate small-model mode or MC…
## Lessons
- A benchmark that grades by the whole suite must restore the reference tests, or an agent can pass by editing them
## Plan gaps
- failed first: step 1 A base package with several interdependent modules and their tests (shared helpers used by more tha…
## Files touched
- bench/spec-suite/hard.py
- bench/spec-suite/make.py
- bench/spec-suite/README.md
- CHANGELOG.md
