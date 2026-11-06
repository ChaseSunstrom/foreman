---
id: T-0701
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T17:01:23Z
base: 566e5e66ac15df285f69a894d39442e6bcd943e4
base_tree: ec9d64e4de6823500cc3fc1880eb2a72239cdcf3
verified: strong
---
# Frontier 01 — Zero-token instrument layer
## Raw request
> FEATURE: Frontier 01 — Zero-token instrument layer
> CONTEXT: Every common read, search, log, trace and diff question gets answered by a deterministic typed tool that costs the model no reasoning tokens.
> CONTEXT: first slice: fm instruments: one typed-tool registry (JSON schema, stable output) with the first five: symbol read, failure record, log templates, data-file schema, stack-trace mapper.
> CONTEXT: proof at close: Run each instrument on a fixed corpus (real failing run, 48k-line log, 212-file question); output must be under its line cap and keep the root cause; measured token ratio vs raw read logged.
> CONTEXT: members (21, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): Foreman's zero-token instruments as typed tools for every agent and harness; Symbol reads: a definition and its one-hop neighbourhood, never a whole file; Failure records: any test runner's 400-line failure becomes 15 lines with the right source; 48,000 log lines become 37 templates, and what's new since the good run; Schema, stats and samples for any data file instead of reading its bytes; A pasted stack trace arrives already mapped to code, age and task; Every thread's stack at the moment of a hang, in any language; Where the time and memory go, in 12 lines, against the last green baseline; Ask a question of 212 files; Opus reads one 19-row table; Program slicing: only the lines that can affect this value; Structural search and replace (comby/ast-grep style) with no binary dependency; One bisector over commits, dependency changes, config and evidence trees; Version-exact library docs from the installed source, offline; Dependency questions answered from the code you actually run; Reproduce a red CI job locally without docker; 'This already exists' at the moment a duplicate helper is written; Delete candidates proven by references and by runtime; Source-to-sink taint paths in seconds, so the security reviewer reads 4 slices; Offline advisories with reachability; Screenshot diffs that send the model crops, not screenshots; Merge conflicts pre-resolved; Claude sees only the real ones
## Interpretation
Frontier milestone 01, first slice: zero-token instruments the expensive model calls instead of reading raw files and output (user: save a crap ton of tokens, many new tools).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm instruments lists the five tools with schemas and caps — verify with `python3 plugin/tests/run.py -p test_instruments.py -k Registry`
- [x] fm sym keeps the root cause under its line cap on its fixture — verify with `python3 plugin/tests/run.py -p test_instruments.py -k Sym`
- [x] fm fail keeps the root cause under its line cap on its fixture — verify with `python3 plugin/tests/run.py -p test_instruments.py -k Fail`
- [x] fm logs keeps the root cause under its line cap on its fixture — verify with `python3 plugin/tests/run.py -p test_instruments.py -k Logs`
- [x] fm data keeps the root cause under its line cap on its fixture — verify with `python3 plugin/tests/run.py -p test_instruments.py -k Data`
- [x] fm trace keeps the root cause under its line cap on its fixture — verify with `python3 plugin/tests/run.py -p test_instruments.py -k Trace`
## Non-goals
## Approach (options → choice → why)
First slice only: plugin/lib/fminstr.py with a typed registry (fm instruments --json lists name, input schema, output cap) and five stdlib-only tools as fm subcommands, each with a line cap and stable output: fm sym PATH:NAME (the definition plus one-hop neighbours: callers and the names it uses; Python via ast, others via a brace/indent heuristic), fm fail (a test runner's failure output on stdin becomes ~15 lines: test id, assertion, the failing source lines with numbers), fm logs FILE [--since-good FILE] (Drain-style templates with counts; what's new against a good run), fm data FILE (schema, stats and 5 sample rows for csv/json/jsonl/sqlite), fm trace (a pasted Python/JS stack trace mapped to repo files, lines and the task that last touched each). Tests: plugin/tests/test_instruments.py, a class per tool plus Registry, each running the tool on a small fixed fixture and asserting the cap and that the root-cause line survives.
## Risks and rollback
## Execution prompt
## Steps
1. [x] all six failing classes first
2. [x] registry + the five tools, one class per step
3. [x] full suite once; MASTER/help lines
## Resume here
## Docs impact
CHANGELOG entry; MASTER.md CLI line; fm help tier (builder)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_instruments.py` → ✗ exit 1 · Ran 14 tests in 0.6s (6 classes, 16 at a time; slowest: Sym 1s, Data 1s, Trace 1s) / FAILED (6 classes) [ran] [tree fd2f77308638] (2026-10-09T16:39:22Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Registry` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Registry 0s) / OK [ran] [tree 81ebdcaa8644] (2026-10-09T16:44:47Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Sym` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Sym 0s) / OK [ran] [tree eb3028541201] (2026-10-09T16:45:15Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Fail` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Fail 0s) / OK [ran] [tree eb3028541201] (2026-10-09T16:45:20Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Fail` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Fail 0s) / OK [ran] [tree 2db8b50b6b17] (2026-10-09T16:45:39Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Logs` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Logs 0s) / OK [ran] [tree 2db8b50b6b17] (2026-10-09T16:45:42Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Data` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Data 0s) / OK [ran] [tree 2db8b50b6b17] (2026-10-09T16:45:50Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Data` → exit 0 · Ran 3 tests in 0.5s (1 classes, 16 at a time; slowest: Data 0s) / OK [ran] [tree 62e1aa3a1972] (2026-10-09T16:46:05Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Trace` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Trace 0s) / OK [ran] [tree 62e1aa3a1972] (2026-10-09T16:46:10Z)
- (step 3) `python3 plugin/tests/run.py` → exit 0 · Ran 1039 tests in 71.7s (267 classes, 16 at a time; slowest: Stop 63s, TaskLifecycle 41s, Bench 38s) / OK [ran] [tree 25d514438fa6] (2026-10-09T16:47:39Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: fm replay → ✗ exit 1 · 0 newly allowed (possible bypasses) / 266 new to the corpus · fm replay --accept takes these verdicts as the baseline [ran] [tree 25d514438fa6] (2026-10-09T16:49:49Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: fm replay → ✗ exit 1 · 0 newly allowed (possible bypasses) / 270 new to the corpus · fm replay --accept takes these verdicts as the baseline [ran] [tree 25d514438fa6] (2026-10-09T16:50:32Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Registry` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: Registry 0s) / OK [ran] [tree 5e941b299fbf] (2026-10-09T16:51:26Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Sym` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Sym 0s) / OK [ran] [tree 5e941b299fbf] (2026-10-09T16:51:27Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Fail` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Fail 0s) / OK [ran] [tree 5e941b299fbf] (2026-10-09T16:51:27Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Logs` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Logs 0s) / OK [ran] [tree 5e941b299fbf] (2026-10-09T16:51:28Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Data` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Data 0s) / OK [ran] [tree 5e941b299fbf] (2026-10-09T16:51:29Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py -k Trace` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Trace 0s) / OK [ran] [tree 5e941b299fbf] (2026-10-09T16:51:29Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (30 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.3    37.6     150  [0] / SessionEnd                  30.8    34.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 16:32 UTC; python3 plugin/tests/run.py → exit 0 · Ran 1039 tests i [ran] [tree 5e941b299fbf] (2026-10-09T16:53:13Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py` → ✗ exit 1 · Ran 16 tests in 2.0s (6 classes, 16 at a time; slowest: Logs 2s, Data 1s, Sym 1s) / FAILED (2 classes) [ran] [tree 90dade00ccc5] (2026-10-09T16:57:28Z)
- (step 2) `python3 plugin/tests/run.py -p test_instruments.py` → exit 0 · Ran 16 tests in 0.7s (6 classes, 16 at a time; slowest: Data 1s, Logs 1s, Fail 0s) / OK [ran] [tree 12f02e785b86] (2026-10-09T16:59:00Z)
- (step 1) `python3 plugin/tests/run.py -p test_instruments.py -k Registry` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: Registry 0s) / OK [ran] [tree f325a4cb655e] (2026-10-09T17:00:01Z)
- (step 1) `python3 plugin/tests/run.py -p test_instruments.py -k Sym` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Sym 0s) / OK [ran] [tree f325a4cb655e] (2026-10-09T17:00:02Z)
- (step 1) `python3 plugin/tests/run.py -p test_instruments.py -k Fail` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Fail 0s) / OK [ran] [tree f325a4cb655e] (2026-10-09T17:00:02Z)
- (step 1) `python3 plugin/tests/run.py -p test_instruments.py -k Logs` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Logs 1s) / OK [ran] [tree f325a4cb655e] (2026-10-09T17:00:03Z)
- (step 1) `python3 plugin/tests/run.py -p test_instruments.py -k Data` → exit 0 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: Data 1s) / OK [ran] [tree f325a4cb655e] (2026-10-09T17:00:04Z)
- (step 1) `python3 plugin/tests/run.py -p test_instruments.py -k Trace` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Trace 0s) / OK [ran] [tree f325a4cb655e] (2026-10-09T17:00:04Z)
- (step 3) `fm quiet -- python3 plugin/tests/run.py` → exit 0 · ✓ exit 0 (52.3 s) · OK [ran] [tree f325a4cb655e] (2026-10-09T17:01:08Z)
- (ac 1) `python3 plugin/tests/run.py -p test_instruments.py -k Registry` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: Registry 0s) / OK [ran] [tree c88e83c3598c] (2026-10-09T17:01:22Z)
- (ac 2) `python3 plugin/tests/run.py -p test_instruments.py -k Sym` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Sym 0s) / OK [ran] [tree c88e83c3598c] (2026-10-09T17:01:22Z)
- (ac 3) `python3 plugin/tests/run.py -p test_instruments.py -k Fail` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Fail 0s) / OK [ran] [tree c88e83c3598c] (2026-10-09T17:01:22Z)
- (ac 4) `python3 plugin/tests/run.py -p test_instruments.py -k Logs` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Logs 1s) / OK [ran] [tree c88e83c3598c] (2026-10-09T17:01:22Z)
- (ac 5) `python3 plugin/tests/run.py -p test_instruments.py -k Data` → exit 0 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: Data 1s) / OK [ran] [tree c88e83c3598c] (2026-10-09T17:01:22Z)
- (ac 6) `python3 plugin/tests/run.py -p test_instruments.py -k Trace` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Trace 0s) / OK [ran] [tree c88e83c3598c] (2026-10-09T17:01:22Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, maintainer) on the branch diff; 10 findings, 9 fixed test-first on the branch before merge, 1 non-issue (cmd_sym needs its own fmmap import)` → each tool keeps the root cause first under its cap; fm logs on 51,406 real journal lines → 40 lines with the crash-looping service first (7.6 MB → 4.5 KB) [tree c88e83c3598c] (2026-10-09T17:01:22Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge, maintainer) on the branch diff; 10 findings, 9 fixed test-first on the branch before merge, 1 non-issue (cmd_sym needs its own fmmap import)` → sqlite opened read-only with a quoted URI, list-argv git with --; fixed unredacted output (redact + redact_obj in _emit), unbounded reads (20 MB / 1M lines / first 100k jsonl rows), symlink escapes in trace mapping [tree c88e83c3598c] (2026-10-09T17:01:22Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, maintainer) on the branch diff; 10 findings, 9 fixed test-first on the branch before merge, 1 non-issue (cmd_sym needs its own fmmap import)` → non-UTF-8 sqlite text, ints over 1e308, mostly-numeric log lines, new INFO templates hiding a new ERROR — each a test now [tree c88e83c3598c] (2026-10-09T17:01:22Z)
- (audit maintainer) `one fm-reviewer pass (intent, adversary, edge, maintainer) on the branch diff; 10 findings, 9 fixed test-first on the branch before merge, 1 non-issue (cmd_sym needs its own fmmap import)` → reuses c.fit/plain_lines/_git/fmmap.outline; Drain similarity documented where it differs [tree c88e83c3598c] (2026-10-09T17:01:22Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T16:30:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0701.builder.md
- 2026-10-09T16:31:03Z focused
- 2026-10-09T16:59:50Z merged worktree-agent-a7cb650345469474f (17 file(s))
- 2026-10-09T16:59:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7cb650345469474f
- 2026-10-09T16:59:54Z focused
- 2026-10-09T17:01:22Z done
- 2026-10-09T17:01:23Z committed bd1505c (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0682 [FEATURE L, planned, 8 steps] Milestone: Features — Verification and product checking
- playbook Whole-repo cleanup sweep (Foreman's own, T-0364) (skills/playbooks/references/clean/repo-sweep.md)
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
## Lessons
- Measure a log summarizer on a mostly-numeric log: dividing by template length hides the access-log case, dividing by fixed tokens lets templates drift; fold on a full fixed-token match instead.
## Files touched
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/repo/shop.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/repo/checkout.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/repo/price.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/repo/tests/price_test.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/repo/app.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/repo/web/cart.js
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/bad.log
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/good.log
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/node_trace.txt
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/python_trace.txt
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/unittest_run.txt
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/events.jsonl
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/fixtures/instruments/orders.csv
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/test_instruments.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/lib/fminstr.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/lib/fmcli.py
- .claude/worktrees/agent-a7cb650345469474f/MASTER.md
- .claude/worktrees/agent-a7cb650345469474f/CHANGELOG.md
- .claude/worktrees/agent-a7cb650345469474f/plugin/lib/fmcore.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/lib/fmguard.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/lib/fmideas.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/test_autonomy_user.py
- .claude/worktrees/agent-a7cb650345469474f/plugin/tests/test_guard_pipes.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- plugin/lib/fmideas.py
- plugin/lib/fminstr.py
