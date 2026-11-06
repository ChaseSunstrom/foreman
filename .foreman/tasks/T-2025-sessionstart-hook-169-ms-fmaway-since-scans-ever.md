---
id: T-2025
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T18:18:34Z
updated: 2026-10-29T18:36:28Z
base: 3d6a26f675ebcdeb759b612708e098095a546b82
base_tree: 38eefc5a578f2e5faa0b24979e7d8b07c9c46caa
plan0_at: 2026-10-29T18:24:16Z
plan0_scope: []
verified: strong
---
# SessionStart hook 169 ms: fmaway.since scans every prompt in every ledger file for the…
## Raw request
> SessionStart hook 169 ms: fmaway.since scans every prompt in every ledger file for the newest 2 h gap, and ledger_events filters lines with a per-line generator (225k calls); try the tail first, one compiled bytes pattern
## Interpretation
Every session start (and every return-after-gap check) pays for fmaway.since reading every prompt in the archive and live ledger, ~62k lines, and ledger_events runs a Python generator per line to filter by event. Make SessionStart faster with identical answers; record before/after numbers.
## Assumptions (confidence)
## Acceptance criteria
- [x] since() finds the same gap from the tail, falls back to the full scan, and ledger_events filters with one pattern — verify with `python3 plugin/tests/run.py test_away test_ledger_chain`
## Non-goals
## Approach (options → choice → why)
1) fmaway.since: look for the newest gap in the ledger tail first (consecutive prompts inside one contiguous tail are a true gap, newest first), scanning everything only when the tail holds none. 2) ledger_events: one compiled bytes pattern per call instead of any() over marks per line. Rejected: an on-disk prompt index (new state file to keep in sync); caching since() per process (each hook is a new process).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Baseline SessionStart timing; red tests for tail-first since() and the single-pattern filter
2. [x] Implement, measure against base, CHANGELOG line
## Resume here
## Docs impact
CHANGELOG Perf line under Unreleased
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_away test_ledger_chain 2>&1 | tail -3` → exit 0 · Ran 47 tests in 4.2s (3 classes, 16 at a time; slowest: Chain 4s, Receipt 2s, Away 1s) / OK [ran] [tree 470cc5571946] (2026-10-29T18:26:54Z)
- (step 1) `python3 plugin/tests/run.py test_away test_ledger_chain 2>&1 | tail -3` → exit 0 · Ran 47 tests in 4.2s (3 classes, 16 at a time; slowest: Chain 4s, Receipt 2s, Away 1s) / OK [ran] [tree 470cc5571946] (2026-10-29T18:26:54Z)
- (ac 1) `python3 plugin/tests/run.py test_away test_ledger_chain 2>&1 | tail -3` → exit 0 · Ran 47 tests in 4.2s (3 classes, 16 at a time; slowest: Chain 4s, Receipt 2s, Away 1s) / OK [ran] [tree 18902964b23f] (2026-10-29T18:27:26Z)
- (step 2) `python3 plugin/tests/run.py test_away test_ledger_chain 2>&1 | tail -3` → exit 0 · Ran 47 tests in 4.2s (3 classes, 16 at a time; slowest: Chain 4s, Receipt 2s, Away 1s) / OK [ran] [tree 18902964b23f] (2026-10-29T18:27:26Z)
- (step 1) `python3 plugin/tests/run.py test_away test_ledger_chain` → exit 0 · Ran 48 tests in 4.1s (3 classes, 16 at a time; slowest: Chain 4s, Receipt 1s, Away 1s) / OK [ran] [tree eb73013bb598] (2026-10-29T18:30:18Z)
- (step 2) `python3 plugin/tests/run.py test_away test_ledger_chain test_core` → exit 0 · Ran 139 tests in 4.2s (26 classes, 16 at a time; slowest: Chain 4s, BriefIndex 2s, WritesAndLocks 2s) / OK [ran] [tree eb73013bb598] (2026-10-29T18:30:23Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmaway.py, plugin/lib/fmcore.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn,; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.4    33.3     150  [0] / SessionEnd                  24.7    26.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree eb73013bb598] (2026-10-29T18:33:42Z)
- (ac 1) `python3 plugin/tests/run.py test_away test_ledger_chain` → exit 0 · Ran 48 tests in 4.1s (3 classes, 16 at a time; slowest: Chain 4s, Receipt 1s, Away 1s) / OK [ran] [tree eb73013bb598] (2026-10-29T18:34:00Z)
- (audit intent) `self-review (risk budget spent, no subagents): read the fmaway.since, fmcore._tail_rows/_kept and ledger_events diff; a tail chunk read mid-file always skips at least one line (the loop stops only at got > n), so a cut first line never parses; each line is matched once (the search resumes at its newline); since's loop always runs, and a tail without a silence falls back to the old full scan over archives` → session start finds the same silence (tests pin the tail answer, the widened tail and the archive fallback) and runs 177 -> 152 ms median; last_change's filtered tail shares the faster path [tree eb73013bb598] (2026-10-29T18:34:00Z)
- (audit edge) `self-review (risk budget spent, no subagents): read the fmaway.since, fmcore._tail_rows/_kept and ledger_events diff; a tail chunk read mid-file always skips at least one line (the loop stops only at got > n), so a cut first line never parses; each line is matched once (the search resumes at its newline); since's loop always runs, and a tail without a silence falls back to the old full scan over archives` → a damaged line holding the word is skipped, not a crash; a line holding only one of two words is not parsed; a live ledger with no silence costs two tail reads plus the old scan; an unterminated last line keeps one extra line, harmless for both callers [tree eb73013bb598] (2026-10-29T18:34:00Z)
## Log
- 2026-10-29T18:18:34Z created
- 2026-10-29T18:18:43Z planned: it has criteria and steps
- 2026-10-29T18:24:16Z focused
- 2026-10-29T18:34:07Z done
- 2026-10-29T18:34:08Z committed cef2323c (5 files)
- 2026-10-29T18:34:14Z guard authorization added: publish
- 2026-10-29T18:36:28Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2020 [PERFORMANCE M, done, 2 steps] Hooks compile regexes on first use: importing fmcore, fmguard and fmhooks compiles none of their 191 module-level patterns — lesson…
- T-2026 [PERFORMANCE M, done, 1 steps] UserPromptSubmit hook: compile only named cards, lazy module patterns, briefs and last_change once — lesson: Profiles taken in a co…
- research T-1065-review: Verdict: changes needed.** Two MEDIUM findings, both about failures breaking normal use. I only read the code. This session had no shell, so I ra…
- decision 2026-10-21: Accept foreman-ui's supply entry after T-1434 named its hooks module
- similar finished tasks took 1–2 steps
## Measurements
SessionStart median 177 -> 152 ms, min 172 -> 149 ms; Stop median 70 -> 64 ms (interleaved, 3 rounds x 15 runs, live ledger copy, against the T-2026 tree); filtered 16,000-line tail 15 -> 3.3 ms
## Lessons
- Benchmark against a fresh copy of the live data: my own timing runs had filled the copied ledger's tail with prompts, hiding the silence the change looks for. And when a filter discards most lines, search the raw bytes; decoding and splitting cost 12 of 15 ms.
## Files touched
- plugin/tests/test_away.py
- plugin/lib/fmaway.py
- plugin/lib/fmcore.py
- plugin/tests/test_ledger_chain.py
- CHANGELOG.md
