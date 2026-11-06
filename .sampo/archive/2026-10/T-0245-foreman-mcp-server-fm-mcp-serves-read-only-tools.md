---
id: T-0245
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T05:27:19Z
updated: 2026-10-04T09:42:54Z
base: 75f52d85cd26f5f95e4450ce11d897eb4323f7e3
base_tree: 69b6af7ac1dbbecd298f64146d18263e54d6e4db
verified: strong
---
# Foreman MCP server — fm mcp serves read-only tools over stdio (state, next, recall, resear
## Raw request
> FEATURE: Foreman MCP server — fm mcp serves read-only tools over stdio (state, next, recall, research notes, brief show, check results) so other agents and clients can use Foreman's memory and gates
> CONTEXT: stdlib JSON-RPC over stdio; registering an MCP server is guard category plugin (user's yes)
> DONE-WHEN: an initialize + tools/list + tools/call round trip over stdio returns the state
## Interpretation
fm mcp: a stdio MCP server (JSON-RPC 2.0, one JSON message per line, stdlib only) that serves Foreman's memory and state read-only to other agents and clients: the project state, the next action, recall, research notes, a task's brief. Registering it (claude mcp add …) is the user's step, guard category plugin.
## Assumptions (confidence)
## Acceptance criteria
- [x] an initialize + tools/list + tools/call round trip over stdio returns the project's state, and the tools are read-only (state, next, recall, research_list, research_read, task_show) — verify with `python3 plugin/tests/run.py -p test_mcp.py -k RoundTrip`
- [x] bad input (unknown tool, a research name with a path, malformed JSON) comes back as a JSON-RPC error or isError result and the server keeps serving; a sensitive project serves nothing — verify with `python3 plugin/tests/run.py -p test_mcp.py -k Edges`
## Non-goals
## Approach (options → choice → why)
(a) an MCP SDK — not stdlib; (b) a small line-delimited JSON-RPC loop answering initialize, ping, tools/list and tools/call, each tool running the matching read-only fm command with --json in-process-free subprocess (the CLI stays the one implementation) → (b). Output redacted; a sensitive project serves nothing; research names validated; unknown tools and bad arguments come back as isError results, never crashes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first: plugin/tests/test_mcp.py
2. [x] fmmcp.py + parser + docs
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_mcp.py` → ✗ exit 1 · Ran 3 tests in 0.5s (2 classes, 16 at a time; slowest: Edges 0s, RoundTrip 0s) / FAILED (2 classes) [ran] [tree 7feeea7e3505] (2026-10-04T09:38:23Z)
- (step 2) `python3 plugin/tests/run.py -p test_mcp.py` → exit 0 · Ran 3 tests in 0.4s (2 classes, 16 at a time; slowest: Edges 0s, RoundTrip 0s) / OK [ran] [tree 94c03ecf900d] (2026-10-04T09:39:08Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (25 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.4    33.3     150  [0] / SessionEnd                  28.0    29.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 810 tests in [ran] [tree 94c03ecf900d] (2026-10-04T09:40:08Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_mcp.py && python3 plugin/tests/run.py -p "test_help*"` → 10/11 hunks proven; unproven: plugin/lib/fmmcp.py @@ new file, lines 14-14 @@ [inconclusive] [ran] [tree 94c03ecf900d] (2026-10-04T09:40:13Z)
- (step 2) `python3 plugin/tests/run.py -p test_mcp.py` → exit 0 · Ran 3 tests in 0.3s (2 classes, 16 at a time; slowest: Edges 0s, RoundTrip 0s) / OK [ran] [tree d08e1449c7d3] (2026-10-04T09:40:20Z)
- (step 1) `python3 plugin/tests/run.py -p test_mcp.py` → exit 0 · Ran 4 tests in 0.3s (3 classes, 16 at a time; slowest: Edges 0s, RoundTrip 0s, Review 0s) / OK [ran] [tree 3b1cf9c38a5e] (2026-10-04T09:41:50Z)
- (step 2) `python3 plugin/tests/run.py -p test_mcp.py` → exit 0 · Ran 4 tests in 0.3s (3 classes, 16 at a time; slowest: Edges 0s, RoundTrip 0s, Review 0s) / OK [ran] [tree 3b1cf9c38a5e] (2026-10-04T09:41:50Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (25 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.0    32.1     150  [0] / SessionEnd                  28.3    29.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 811 tests in [ran] [tree 3b1cf9c38a5e] (2026-10-04T09:42:43Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_mcp.py && python3 plugin/tests/run.py -p "test_help*"` → exit 0 · 12/12 hunks proven [ran] [tree 3b1cf9c38a5e] (2026-10-04T09:42:48Z)
- (ac 1) `python3 plugin/tests/run.py -p test_mcp.py -k RoundTrip` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: RoundTrip 0s) / OK [ran] [tree 3b1cf9c38a5e] (2026-10-04T09:42:54Z)
- (ac 2) `python3 plugin/tests/run.py -p test_mcp.py -k Edges` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Edges 0s) / OK [ran] [tree 3b1cf9c38a5e] (2026-10-04T09:42:54Z)
- (audit adversary) `one fm-reviewer pass, intent + adversary (T-0245-review-1): approve with nits — MEDIUM option injection through recall's query (--corrections exposed the user's corrections), LOW unbounded lines and symlinked notes, intent: the request's check results had no tool. All reproduced as failing tests, then fixed: queries can't start with -, lines over 1 MB refused without being held, notes resolved inside the research folder only, a checks tool reading the last check_run. Real round trip against this project answered initialize, next and recall. Hunks 12/12` → no shell, no writes, no flags through arguments, no paths out of research, redacted output, sensitive projects serve nothing [tree 3b1cf9c38a5e] (2026-10-04T09:42:54Z)
- (audit intent) `one fm-reviewer pass, intent + adversary (T-0245-review-1): approve with nits — MEDIUM option injection through recall's query (--corrections exposed the user's corrections), LOW unbounded lines and symlinked notes, intent: the request's check results had no tool. All reproduced as failing tests, then fixed: queries can't start with -, lines over 1 MB refused without being held, notes resolved inside the research folder only, a checks tool reading the last check_run. Real round trip against this project answered initialize, next and recall. Hunks 12/12` → every tool the request named (state, next, recall, research, briefs, check results) is served [tree 3b1cf9c38a5e] (2026-10-04T09:42:54Z)
## Log
- 2026-10-04T05:27:19Z created
- 2026-10-04T09:33:12Z set tier=M
- 2026-10-04T09:38:09Z focused
- 2026-10-04T09:42:54Z done
- 2026-10-04T09:42:54Z committed 8d047ae (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- playbook /search-first — Research Before You Code (skills/playbooks/references/ground/search-first.md)
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- research T-0278-review-1: Approve with nits. Both features do what was asked. I found no HIGH issues, and the pre-audit hit is dismissed: it is `no_verify=False` at `plu…
## Lessons
- An argument handed to a CLI subprocess needs a shape that can't start with '-', or it becomes a flag
## Files touched
- plugin/tests/test_mcp.py
- plugin/lib/fmmcp.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
