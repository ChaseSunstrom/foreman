---
id: T-1066
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmreplay.py, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/tests/test_replay.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T06:20:08Z
base: de89974f006a9fcdcf27f230231ddcc884f5a266
base_tree: 172f0a284dd30dbc72fbae5e660e4a9bb655ef43
verified: strong
---
# Mutation-test the guard: fm bench guard --mutate drops or weakens one guard rule at a time
## Raw request
> SECURITY: Mutation-test the guard: fm bench guard --mutate drops or weakens one guard rule at a time and shows which bench/replay cases notice; a rule no case notices is untested (wild C10)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
`fm bench guard --mutate` weakens one guard rule at a time and shows which cases notice. A "case" is a command from the replay corpus plus the fixed deny/allow commands the guard tests use. A rule no case flips is listed as untested (wild C10). Existing parts: `fm replay --candidate` loads a guard module from a file and scores it (`fmreplay.py:90`, `:111`), `verdicts` takes another guard module (`fmreplay.py:67`), and `fm bench` has no `guard` subcommand (`fmcli.py:4704`).
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm bench guard --mutate --cmds FILE` names a rule with no case as "untested" and one with a case as "caught" — verify with `python3 plugin/tests/run.py test_replay`
## Non-goals
## Approach (options → choice → why)
(a) mutate source text with regex edits per rule; (b) AST-mutate `fmguard.py`'s `check` branches (`if` tests become False, one at a time); (c) wrap the module's `CATEGORIES` and drop one category at a time. Choose (c): the guard returns a `category` per block (`fmreplay.py:80`), so a rule is "a category." Dropping one means its verdicts become "allow", which needs no source rewriting. Mutate by patching `check` to return None when `b.category == X`, and run the corpus: a mutant "survives" when no case's verdict changes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: with a corpus of `rm -rf /` (and nothing else), the mutate run reports that category caught and every other category in `fmguard.CATEGORIES` untested; exit 1 when any is untested; `--json` has `caught` and `untested` lists.
2. [x] `fmreplay.mutate(cmds)` builds `verdicts` once, then per category re-derives from that same table (no re-run, a mutant only changes entries equal to X). Cheap, and needs no module patching.
3. [x] Add the `guard` subparser (`--mutate`, `--days`, `--cmds FILE`) near `fmcli.py:4712`, dispatched from `cmd_bench` before `refuse_if_paused`.
## Resume here
## Docs impact
MASTER.md Guard mutation; CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_replay` → ✗ exit 1 · Ran 3 tests in 5.7s (2 classes, 16 at a time; slowest: Replay 3s, Core 0s) / FAILED (1 classes) [ran] [tree b7eae9d4e2ff] (2026-10-16T05:37:39Z)
- (step 1) `python3 plugin/tests/run.py test_replay` → exit 0 · Ran 3 tests in 4.8s (2 classes, 16 at a time; slowest: Replay 4s, Core 1s) / OK [ran] [tree b6bfe42eb563] (2026-10-16T05:38:04Z)
- (step 2) `python3 plugin/tests/run.py test_replay` → exit 0 · Ran 3 tests in 3.4s (2 classes, 16 at a time; slowest: Replay 3s, Core 1s) / OK [ran] [tree b6bfe42eb563] (2026-10-16T05:38:09Z)
- (step 3) `python3 plugin/tests/run.py test_replay test_bench` → exit 0 · Ran 29 tests in 43.0s (11 classes, 16 at a time; slowest: Bench 43s, Judged 36s, Duel 28s) / OK [ran] [tree b6bfe42eb563] (2026-10-16T05:38:53Z)
- (step 1) `python3 plugin/tests/run.py test_replay` → exit 0 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: Replay 1s, Core 0s) / OK [ran] [tree 4e4147c4e5ff] (2026-10-16T05:41:07Z)
- (step 2) `python3 plugin/tests/run.py test_replay` → exit 0 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: Replay 1s, Core 0s) / OK [ran] [tree cc5941627308] (2026-10-16T05:58:59Z)
- (step 3) `python3 plugin/tests/run.py test_replay` → exit 0 · Ran 6 tests in 2.8s (2 classes, 16 at a time; slowest: Replay 3s, Core 0s) / OK [ran] [tree 85ec7f321308] (2026-10-16T06:16:15Z)
- (ac 1) `python3 plugin/tests/run.py test_replay` → exit 0 · Ran 6 tests in 4.0s (2 classes, 16 at a time; slowest: Replay 4s, Core 0s) / OK [ran] [tree 27a00cc42b2c] (2026-10-16T06:18:41Z)
- (audit intent) `review: one fm-reviewer pass (combined with T-1073); the builder fixed all findings test-first (every rule shape matched, process-group kill, baseline timeout and output, progress log, low items); real run over all 66 sites: 53 killed, 13 survivors handed to T-1120` → a guard rule no test catches is named, file:line, by a run anyone can repeat [tree 27a00cc42b2c] (2026-10-16T06:18:41Z)
- (audit adversary) `review: one fm-reviewer pass (combined with T-1073); the builder fixed all findings test-first (every rule shape matched, process-group kill, baseline timeout and output, progress log, low items); real run over all 66 sites: 53 killed, 13 survivors handed to T-1120` → mutants live only in a temp copy; the real tree and state are never written; a hung mutant's process group is killed [tree 27a00cc42b2c] (2026-10-16T06:18:41Z)
- (audit edge) `review: one fm-reviewer pass (combined with T-1073); the builder fixed all findings test-first (every rule shape matched, process-group kill, baseline timeout and output, progress log, low items); real run over all 66 sites: 53 killed, 13 survivors handed to T-1120` → every site shape (append, extend, +=, list/tuple/comprehension returns, Block); categories with no site named; a failing baseline refuses with its output [tree 27a00cc42b2c] (2026-10-16T06:18:41Z)
- (audit operator) `review: one fm-reviewer pass (combined with T-1073); the builder fixed all findings test-first (every rule shape matched, process-group kill, baseline timeout and output, progress log, low items); real run over all 66 sites: 53 killed, 13 survivors handed to T-1120` → progress per mutant on stderr; --only/--max/--timeout bound the run (all 66 sites ≈11 min) [tree 27a00cc42b2c] (2026-10-16T06:18:41Z)
- (audit maintainer) `review: one fm-reviewer pass (combined with T-1073); the builder fixed all findings test-first (every rule shape matched, process-group kill, baseline timeout and output, progress log, low items); real run over all 66 sites: 53 killed, 13 survivors handed to T-1120` → fmmutate (sites, mutants, run) and fmreplay.cmd_mutate; --coverage keeps the corpus view [tree 27a00cc42b2c] (2026-10-16T06:18:41Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:52Z set scope=['plugin/lib/fmreplay.py', 'plugin/lib/fmbench.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_replay.py']
- 2026-10-16T04:22:52Z set tier=M
- 2026-10-16T05:37:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1066.builder.md
- 2026-10-16T05:37:12Z focused
- 2026-10-16T06:18:18Z merged worktree-agent-a76d2e1ddbceeaab1 (5 file(s))
- 2026-10-16T06:18:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a76d2e1ddbceeaab1
- 2026-10-16T06:18:25Z focused
- 2026-10-16T06:18:26Z scope: CHANGELOG.md, MASTER.md — docs for guard mutation
- 2026-10-16T06:20:07Z done
- 2026-10-16T06:20:08Z committed 67b6aed (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1079 [PERFORMANCE S, active, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-1072 [CLEAN M, active, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_cli.py, plugin/tests/test_replay.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmreplay.py, plugin/tests/test_replay.py; re-ground the plan against them before editing
## Lessons
- Coverage by category is not mutation testing: drop each rule and see a test fail, or the rule is unproven
## Plan gaps
- failed first: step 1 Failing tests: with a corpus of `rm -rf /` (and nothing else), the mutate run reports that category…
## Files touched
- plugin/tests/test_replay.py
- plugin/lib/fmreplay.py
- plugin/lib/fmcli.py
- plugin/lib/fmbench.py
- plugin/lib/fmmutate.py
- CHANGELOG.md
- MASTER.md
