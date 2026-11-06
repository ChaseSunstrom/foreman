---
id: T-2244
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T00:26:28Z
updated: 2026-10-31T01:04:06Z
inferred_deps: [T-2163]
inferred_why: T-2163: named in its request
group: ledger-forgery gates on genesis select
base: 35040aae2fac3e7cfb6bf47d070e560ef3bc6c94
base_tree: 8ea83747868748842ff8ba4bd6829a8a2427aa4c
plan0_at: 2026-10-31T00:34:58Z
plan0_scope: []
verified: strong
---
# fm log EVENT appends any event name, so every gate that reads the ledger (genesis_select…
## Raw request
> SECURITY: fm log EVENT appends any event name, so every gate that reads the ledger (genesis_select before T-2163, check_run at fmcli.py:2569) can be forged by a session; reserve the names Foreman's own code logs (or make fm log namespace its events) and test each ledger-derived gate against a forged event
## Interpretation
fm log EVENT [DATA] (fmcli.cmd_log) appends any event name to the hash-chained ledger, so a session can forge an event a gate reads (genesis_select before T-2163; check_run, read at fmcli.py:2569). Foreman's own code logs 125 event names; the only fm log callers are skills telling sessions to record notes (final_verify, baseline), and no code reads those names.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm log EVENT records event 'log' with data.event EVENT, so no gate reading a Foreman event (check_run, genesis_*) can be satisfied by it; the skills' fm log notes still record — verify with `cd plugin/tests && python3 -m unittest -q test_cli.LogNamespace`
## Non-goals
## Approach (options → choice → why)
Options: (1) namespace: fm log records event 'log' with data.event = EVENT, so a session's note can never carry a Foreman event's name; (2) a reserved-name list (goes stale as names are added; one missed name reopens it); (3) signed events (heavy, and a session can call the signer). Choice 1: one line, no list to maintain, the skills' notes still record and read back by data.event. Then audit each ledger-derived gate for any other verb that can write its event.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: fm log check_run '{...}' doesn't count as a check run, and the recorded event is 'log'
2. [x] cmd_log namespaces; audit other ledger-derived gates for a verb that writes their event
3. [x] docs (MASTER, CHANGELOG, skills that say fm log), adversary review
## Resume here
## Docs impact
MASTER.md fm log line, CHANGELOG Unreleased
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_cli.LogNamespace 2>&1 | tail -6` → ✗ exit 1 · Ran 1 test in 0.272s / FAILED (failures=1) [ran] [tree cad675f83f60] (2026-10-31T00:35:14Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_cli.LogNamespace` → exit 0 · Ran 1 test in 0.207s / OK [ran] [tree 58af92fa54b8] (2026-10-31T00:35:40Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.57s] [ran] [tree 58af92fa54b8] (2026-10-31T00:36:39Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_mcp test_flywheel test_night test_recall 2>&1 | tail -15` → exit 0 · Ran 206 tests in 36.2s (70 classes, 16 at a time; slowest: TaskLifecycle 36s, Recall 29s, Night 20s) / OK [ran] [tree 805e68492371] (2026-10-31T00:40:00Z)
- `cd plugin/tests && python3 -m unittest -q test_cli.LogNamespace` → ✗ exit 1 · Ran 1 test in 0.171s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree c977cb506bda] (2026-10-31T00:57:14Z)
- `cd plugin/tests && python3 -m unittest -q test_cli.LogNamespace` → exit 0 · Ran 1 test in 0.115s / OK [ran] [tree c977cb506bda] (2026-10-31T00:57:14Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_cli.LogNamespace` → exit 0 · Ran 1 test in 0.242s / OK [ran] [tree c977cb506bda] (2026-10-31T00:59:49Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_cli.LogNamespace` → exit 0 · Ran 1 test in 0.229s / OK [ran] [tree c977cb506bda] (2026-10-31T00:59:49Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_cli.LogNamespace` → exit 0 · Ran 1 test in 0.218s / OK [ran] [tree c977cb506bda] (2026-10-31T00:59:50Z)
- (step 3) `grep -q 'T-2244' MASTER.md && grep -q 'records a note as event' CHANGELOG.md` → exit 0 · (no output) [ran] [tree d9e65fa0a315] (2026-10-31T00:59:50Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_cli.LogNamespace` → exit 0 · Ran 1 test in 0.245s / OK [ran] [tree d9e65fa0a315] (2026-10-31T00:59:53Z)
- (audit intent) `fm-reviewer adversary+edge on the builder's branch: no other argv-chosen event name reaches log_event (every non-literal call site traced); 1 HIGH (three tests seeded Foreman events through fm log) and the data order and help text fixed in f46588e8; 180 tests across cli/mcp/flywheel/night/recall green` → a session's fm log can't satisfy any gate that reads a Foreman event [tree d9e65fa0a315] (2026-10-31T00:59:53Z)
- (audit adversary) `fm-reviewer adversary+edge on the builder's branch: no other argv-chosen event name reaches log_event (every non-literal call site traced); 1 HIGH (three tests seeded Foreman events through fm log) and the data order and help text fixed in f46588e8; 180 tests across cli/mcp/flywheel/night/recall green` → fm log check_run, genesis_select and ledger_damage_ack now land as 'log'; no other verb takes an event name from argv [tree d9e65fa0a315] (2026-10-31T00:59:53Z)
- (audit edge) `fm-reviewer adversary+edge on the builder's branch: no other argv-chosen event name reaches log_event (every non-literal call site traced); 1 HIGH (three tests seeded Foreman events through fm log) and the data order and help text fixed in f46588e8; 180 tests across cli/mcp/flywheel/night/recall green` → a check_run forged before this change keeps its name and still counts (no cheap way to tell it apart); the skills' notes still record and fm recall finds them [tree d9e65fa0a315] (2026-10-31T00:59:53Z)
## Log
- 2026-10-31T00:26:28Z created
- 2026-10-31T00:34:23Z planned: it has criteria and steps
- 2026-10-31T00:34:23Z set approved=True
- 2026-10-31T00:34:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2244.builder.md
- 2026-10-31T00:34:57Z focused
- 2026-10-31T00:57:12Z merged worktree-agent-afeeb3bfd058243e2 (5 file(s))
- 2026-10-31T00:57:13Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afeeb3bfd058243e2
- 2026-10-31T00:57:13Z focused
- 2026-10-31T01:00:49Z done
- 2026-10-31T01:00:52Z committed 9c73f4c3 (1 file)
- 2026-10-31T01:01:10Z guard authorization added: publish
- 2026-10-31T01:04:06Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2113 [FEATURE M, done, 3 steps] fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals… — lesson: A seal file beside the file it seals …
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- research T-1456-review: Verdict: changes needed.** One HIGH adversary finding. I could not run code (read-only, no shell), so each finding is proved by tracing `fmledger…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar finished tasks took 3–3 steps
## Lessons
- A generic append verb next to gates that read the same log is a forgery path: namespace what sessions write
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- plugin/tests/test_mcp.py
- plugin/tests/test_flywheel.py
- plugin/tests/test_night.py
- CHANGELOG.md
