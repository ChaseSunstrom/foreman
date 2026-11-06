---
id: T-0802
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-14T16:05:40Z
updated: 2026-10-14T17:04:28Z
base: 55e64ebdf3d1aff303f024184e23e456416813e3
base_tree: a430fb82bb64faf07e1dcf1a57b250d7044e5a52
verified: strong
---
# fm research list and fm research show NAME
## Raw request
> fm research list and fm research show NAME: 6 criteria in this project's history (T-0082, T-0195, T-0277, T-0717, T-0760) assumed they exist; only add and ask do
## Interpretation
fm research has add and ask only (fmcli.py:3480), yet six criteria in this project's history (T-0082, T-0195, T-0277, T-0717, T-0760) assumed list and show. list prints the project's research files newest first (name, date, first heading or line, size); show NAME prints one (name with or without .md; a directory like brainstorm-<time> prints its ideas.md). Both read only the project's research/ folder.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm research list names saved research newest first and fm research show NAME prints it (a brainstorm folder prints its ideas.md); an unknown name exits non-zero naming the closest — verify with `cd plugin/tests && python3 -m unittest test_cli.ResearchListShow`
## Non-goals
## Approach (options → choice → why)
Options: tell users to ls the state folder (fm owns state; paths shift); add list/show (two small subcommands); fold into fm recall (different job). Chose list/show.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing CLI test
2. [x] list and show subcommands; MASTER.md CLI line
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_cli.ResearchListShow` → exit 0 · Ran 2 tests in 1.114s / OK [ran] [tree a902658d32db] (2026-10-14T16:41:10Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_cli.ResearchListShow` → exit 0 · Ran 2 tests in 1.026s / OK [ran] [tree a902658d32db] (2026-10-14T16:41:11Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification                68.7    94.9     150  [0] / SessionEnd                  58.9    76.2     150  [0]; python3 plugin/tests/run.py → ✗ exit 1 · Ran 1278 tests in 199.3s (432 classes, 16 at a time; slowest: Stop 109s, Judged 58s, Recall 57s) / FAILED (3 classes) [ran] [tree a902658d32db] (2026-10-14T16:45:25Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification               275.2   642.8     150  [0]  OVER BUDGET / SessionEnd                 247.1   424.7     150  [0]  OVER BUDGET; python3 plugin/tests/run.py → ✗ exit 1 · Ran 1278 tests in 282.5s (432 classes, 16 at a time; slowest: Stop 199s, TaskLifecycle 106s, Bench 99s) / FAILED (5 classes) [ran] [tree a902658d32db] (2026-10-14T16:50:44Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification               143.5   370.4     150  [0]  OVER BUDGET / SessionEnd                  94.6   269.4     150  [0]  OVER BUDGET; python3 plugin/tests/run.py → ✗ exit 1 · Ran 1278 tests in 304.4s (432 classes, 16 at a time; slowest: Stop 215s, TaskLifecycle 110s, Bench 105s) / FAILED (4 classes) [ran] [tree a902658d32db] (2026-10-14T16:51:19Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 1278 tests in 87.1s (432 classes, 16 at a time; slowest: Stop 60s, Recall 32s, TaskLifecycle 30s) / FAILED (1 classes) (pre-existing: it also failed before this task) [ran] [tree a902658d32db] (2026-10-14T16:55:36Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification                79.7   112.4     150  [0] / SessionEnd                  75.0   101.5     150  [0] [ran] [tree 77947b909935] (2026-10-14T17:00:15Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_cli.ResearchListShow` → exit 0 · Ran 2 tests in 0.523s / OK [ran] [tree 8f08906305dc] (2026-10-14T17:02:43Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_cli.ResearchListShow test_cli.VerifyLint` → exit 0 · Ran 3 tests in 1.156s / OK [ran] [tree 8f08906305dc] (2026-10-14T17:02:44Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cli.ResearchListShow` → exit 0 · Ran 2 tests in 0.528s / OK [ran] [tree 8f08906305dc] (2026-10-14T17:02:45Z)
- `cd plugin/tests && python3 -m unittest test_cli.ResearchListShow` → ✗ exit 1 · Ran 2 tests in 0.451s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree 8f08906305dc] (2026-10-14T17:02:46Z)
- `cd plugin/tests && python3 -m unittest test_cli.ResearchListShow` → exit 0 · Ran 2 tests in 0.531s / OK [ran] [tree 8f08906305dc] (2026-10-14T17:02:46Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cli.ResearchListShow` → exit 0 · Ran 2 tests in 0.538s / OK [ran] [tree 8f08906305dc] (2026-10-14T17:04:28Z)
- (audit edge) `self: merged diff read; list reads only the project's research/ (symlinks skipped), newest first by mtime, with name, date, size and first heading; show takes a name with or without .md and prints a brainstorm folder's ideas.md; unknown names exit non-zero naming the closest; real list on this project shows today's catalogue and runs` → VerifyLint's unrunnable example moved to 'fm research nosuch' since list now exists; order follows mtime, so a copied state folder may reorder (noted by the builder) [tree 8f08906305dc] (2026-10-14T17:04:28Z)
- (audit self) `self: merged diff read; list reads only the project's research/ (symlinks skipped), newest first by mtime, with name, date, size and first heading; show takes a name with or without .md and prints a brainstorm folder's ideas.md; unknown names exit non-zero naming the closest; real list on this project shows today's catalogue and runs` → no findings [tree 8f08906305dc] (2026-10-14T17:04:28Z)
## Log
- 2026-10-14T16:05:40Z created
- 2026-10-14T16:40:24Z planned from capture
- 2026-10-14T16:40:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0802.builder.md
- 2026-10-14T16:40:33Z focused
- 2026-10-14T17:02:38Z merged worktree-agent-ae11f44fd9551e68d (3 file(s))
- 2026-10-14T17:02:38Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae11f44fd9551e68d
- 2026-10-14T17:02:42Z focused
- 2026-10-14T17:04:27Z scope: the builder changed test_cli.VerifyLint's example of an unrunnable fm command from 'fm research list' (now real) to 'fm research nosuch'
- 2026-10-14T17:04:28Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- research T-0245-review-1: Verdict: approve with nits.** I found no shell, write or path-escape route from `tools/call`. The one real hole is option injection through rec…
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–7 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- when users and criteria keep reaching for a command that doesn't exist, add it
## Files touched
- .claude/worktrees/agent-ae11f44fd9551e68d/plugin/tests/test_cli.py
- .claude/worktrees/agent-ae11f44fd9551e68d/plugin/lib/fmcli.py
- .claude/worktrees/agent-ae11f44fd9551e68d/MASTER.md
- MASTER.md
- plugin/agents/fm-builder.md
- plugin/hooks/hooks.json
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/tests/bench_hooks.py
- plugin/tests/test_bench_hooks.py
- plugin/tests/test_cli.py
- plugin/tests/test_docs.py
- plugin/tests/test_hooks.py
- plugin/tests/test_lanes.py
