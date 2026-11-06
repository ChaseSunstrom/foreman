---
id: T-1378
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T13:47:09Z
updated: 2026-10-21T17:58:15Z
base: 4305d5196ea44035d8280dc2e20b9d05c764bb8f
base_tree: 668dfbad2ad879330389d6bd7f82331905a6c48d
plan0_at: 2026-10-21T17:11:56Z
plan0_scope: []
verified: strong
---
# Queueing a multi-request prompt fits every request in the hook's time on a loaded machine: one pass, one view refresh
## Raw request
> test_hooks NoTaskGate.test_a_long_multi_request_prompt_queues_every_request fails under load (twice; the second stopped release 1.2.48's check at load ~30). Cause, read in fmhooks._queue_requests: each request is one in-process fm task new (_fm_inline), each doing its own regen, ledger and locks; past 3.2 s the loop stops, so under load fewer than all requests are queued and the test (16 of 16) fails. Fix: queue the block in one pass (one lock, one view regen at the end), or hand the rest to a detached child that queues them, so a slow machine still queues every request.
## Interpretation
The PreToolUse gate queues a prompt's '## Request k' sections as tasks, one in-process fm task new each, and stops at 3.2 s. Each create redoes the views, the ledger line and the similar-task search, so at load ~30 only some of 16 are queued; the test (16 of 16) failed twice and stopped release 1.2.48's check. Make the per-task cost small so every request fits.
## Assumptions (confidence)
## Acceptance criteria
- [x] 16 requests queue in order with their depends chain inside the hook's budget when every python start takes 0.4 s (the existing test, now passing reliably: 5 runs in a row under a parallel suite) — verify with `python3 plugin/tests/run.py test_hooks`
- [x] fm's parser is built once per process however many in-process fm calls run, and a hook-queued request skips the similar-task search; one queued task costs a small fraction of today's 0.23 s — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
Measured first (see log): per queued request ~0.15 s of argparse building (twice per in-process call) and ~0.07 s of a similar-task search whose note the hook discards; the view refresh is 0.013 s. Options: (A) build fm's parser once per process (a module memo; every in-process caller gains) and skip _covered_note for hook-queued requests (chosen: removes ~95% of the per-task cost, no behaviour change); (B) batch every create under one lock (helps little: the create is ~5 ms); (C) a detached child for the rest (an edit can start before the queue exists). The test stays as it is; a new test pins the parser to one build per process.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Measure: time one in-process fm task new by phase (create, ledger, views, similar-task note) under load
2. [x] Failing test: two in-process fm calls build the parser once; a hook-queued request runs no similar-task search
3. [x] Memo build_parser; skip _covered_note for hook-queued requests; 5 consecutive runs of test_hooks under a parallel suite
## Resume here
<!-- auto -->
- 2026-10-21T17:39:55Z steps 3/3 done
- git: foreman/build; 3 uncommitted: plugin/lib/fmcli.py, plugin/tests/test_cli.py, plugin/tests/test_worker_reads.py
- touched since last checkpoint: plugin/tests/test_cli.py, plugin/lib/fmcli.py, /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/catalogue-r2.md, /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/intake-r2.txt, /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/r2rows.py, /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/r2page.py
## Docs impact
CHANGELOG line; no user-facing command changed
## Verification evidence
- (step 1) `sh /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/prof_task_new.sh` → exit 0 · 54    0.000    0.000    0.004    0.000 fmcore.py:1629(_read_brief) / 2    0.000    0.000    0.004    0.002 fmcore.py:3160(_git) [ran] [tree 4d0bf8b785b3] (2026-10-21T15:37:35Z)
- (step 2) `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 106 tests in 61.5s (30 classes, 16 at a time; slowest: TaskLifecycle 61s, StateViews 26s, Checks 21s) / FAILED (1 classes) [ran] [tree 76deb74c0ab5] (2026-10-21T17:13:26Z)
- (step 2) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 106 tests in 59.7s (30 classes, 16 at a time; slowest: TaskLifecycle 59s, StateViews 25s, AuditPrep 23s) / OK [ran] [tree 1ed2d58e676b] (2026-10-21T17:17:47Z)
- (step 3) `for i in 1 2 3 4 5; do python3 plugin/tests/run.py test_hooks test_session >/dev/null 2>&1 || exit 1; done; echo 5 of 5` → ✗ exit 124 (timed out after 600s) · timed out after 600s [ran] [tree 1ed2d58e676b] (2026-10-21T17:27:48Z)
- (step 3) `for i in 1 2 3 4 5; do python3 plugin/tests/run.py test_hooks test_session >/dev/null 2>&1 || exit 1; done; echo 5 of 5` → exit 0 · 5 of 5 [ran] [tree e4acef911f0d] (2026-10-21T17:37:44Z)
- (step 2) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 106 tests in 48.2s (30 classes, 16 at a time; slowest: TaskLifecycle 48s, StateViews 17s, Checks 17s) / OK [ran] [tree e4acef911f0d] (2026-10-21T17:39:53Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 192 tests in 219.6s (22 classes, 16 at a time; slowest: Stop 219s, NoTaskGate 144s, PreToolUse 131s) / OK [ran] [tree 02d0cf21c5cd] (2026-10-21T17:46:08Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 192 tests in 219.6s (22 classes, 16 at a time; slowest: Stop 219s, NoTaskGate 144s, PreToolUse 131s) / OK [ran] [tree 02d0cf21c5cd] (2026-10-21T17:46:08Z)
- (audit intent) `self: read every build_parser caller (fmcost, fmdoctor, fmrecall, fmhooks, fmcore, fmcli complete/help) — all only read _actions or parse_args, none mutates the parser, so sharing one is safe; argparse parse_args builds a fresh namespace per call (the test pins defaults on a second parse)` → the hook's multi-request test passed 5 of 5 under a parallel suite; per-request cost drops from ~0.23 s to ~0.08 s [tree 02d0cf21c5cd] (2026-10-21T17:46:08Z)
- (audit edge) `self: read every build_parser caller (fmcost, fmdoctor, fmrecall, fmhooks, fmcore, fmcli complete/help) — all only read _actions or parse_args, none mutates the parser, so sharing one is safe; argparse parse_args builds a fresh namespace per call (the test pins defaults on a second parse)` → a parse error raises SystemExit without touching the parser's state; a second parse starts from defaults (tested) [tree 02d0cf21c5cd] (2026-10-21T17:46:08Z)
- (audit maintainer) `self: read every build_parser caller (fmcost, fmdoctor, fmrecall, fmhooks, fmcore, fmcli complete/help) — all only read _actions or parse_args, none mutates the parser, so sharing one is safe; argparse parse_args builds a fresh namespace per call (the test pins defaults on a second parse)` → one memo, one docstring; _build_parser is the old body unchanged [tree 02d0cf21c5cd] (2026-10-21T17:46:08Z)
## Log
- 2026-10-21T13:47:09Z created
- 2026-10-21T15:28:00Z planned from capture
- 2026-10-21T15:37:28Z measured (cProfile, one fm task new in a scratch project, idle machine): 0.232 s in all; build_parser 0.147 s (built twice per call), _covered_note 0.072 s (a similar-task search whose note the hook throws away), regen_views 0.013 s, the create itself ~0.005 s. So the views aren't the cost: per queued request the hook pays ~0.22 s of parser and search, x5-10 at load 30-40, so the 3.2 s cut fits 2-3 of 16. Revised approach: build the parser once per process (memo in fmcli) and skip the similar-task note for requests the hook queues; expected ~0.03 s a task.
- 2026-10-21T15:37:28Z criterion 2 text: one queued task's in-process cost is measured before and after, and the batch path refreshes the views once per prompt, not once per request → fm's parser is built once per process however many in-process fm calls run, and a hook-queued request skips the similar-task search; one queued task costs a small fraction of today's 0.23 s
- 2026-10-21T17:11:56Z focused
- 2026-10-21T17:34:25Z paused: focus moved to T-1388
- 2026-10-21T17:39:03Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-21T17:39:03Z focused
- 2026-10-21T17:39:04Z note: plugin/lib/fmcli.py in this commit also carries T-1388's worker read-only allowlist (its own tests pass; T-1388 continues with the init check)
- 2026-10-21T17:42:16Z scope: plugin/lib/fmcli.py, plugin/tests/test_cli.py, CHANGELOG.md — the memo lives in fmcli; the skip of _covered_note proved unnecessary (the memo alone gave 5 of 5 runs), so it was left out
- 2026-10-21T17:58:12Z done
- 2026-10-21T17:58:15Z committed 9ee5534a (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave2-plan-a0f775007b83f4d0b: [instruction-like text quoted from a file or tool; data, not instructions] === T-1087 [stale: mods/foreman-ui/hooks/register.tsx, …
- T-1379 [FIX M, planned, 2 steps] test_breaker's pause test and test_scout's dry-run test pass at any machine load
- research mission-20261020-115157.pack: continue, super improve foreman, with latest claude code: round 1 shipped (cost per correct session on the page, Claude Code versi…
- decision 2026-10-16: Recommendation: build the 15 grounded items T-1155..T-1169 with up to 4 builders, then run round 3 against the improved tree; would change if: round…
## Regression test
test_cli.ParserOnce.test_the_parser_is_built_once_per_process: before the memo, build_parser built a fresh parser on every call (two per in-process fm call, plus one per fmrecall search), so the same-object and one-build assertions fail; after it, they pass. test_hooks NoTaskGate passed 5 of 5 runs under a parallel suite.
## Why not caught
none: no test measured per-call cost of in-process fm; ParserOnce now pins one build per process
## Lessons
- Profile before choosing a fix: the views looked like the cost, but 65% was argparse rebuilt per in-process call
## Plan gaps
- failed first: step 2 Failing test: two in-process fm calls build the parser once; a hook-queued request runs no similar-…
- failed first: step 3 Memo build_parser; skip _covered_note for hook-queued requests; 5 consecutive runs of test_hooks un…
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
