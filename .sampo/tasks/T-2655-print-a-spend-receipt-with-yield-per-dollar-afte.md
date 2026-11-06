---
id: T-2655
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcontract.py, plugin/lib/fmcli.py, plugin/tests/test_receipt_yield.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T20:05:49Z
builder_model: sonnet
base: 6148fe2abb2b466b486b246af9a013dcd12915f1
base_tree: 3e6249e0b6bc281dc2e93580817fb4fc3e5c0a69
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T20:00:29Z
plan0_scope: [plugin/lib/fmcontract.py, plugin/lib/fmcli.py, plugin/tests/test_receipt_yield.py, CHANGELOG.md]
lane_stop: merged 2026-11-02T20:04:16Z
verified: strong
---
# The drive's end-of-run receipt adds yield per dollar (tasks closed per dollar, dollars per task) beside spend and tokens, and prints it when a drive run ends, not only when a contract ends
## Raw request
> FEATURE: Print a spend receipt with yield per dollar after each drive run (c22: Spend planning, quota and idle-yield; value 3, effort M, risk med)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a run that closed 3 tasks for 1.50 USD prints 0.50 USD a task (2.0 tasks a dollar); zero spend or zero tasks print no ratio, never a division error — verify with `python3 plugin/tests/run.py test_receipt_yield`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the ratio in fmcontract._receipt and its print at drive end
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_receipt_yield 2>&1 | head -30` → ✗ exit 1 (never ran: the test module test_receipt_yield couldn't import) · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: ReceiptYield 0s) / FAILED (1 classes: test_receipt_yield.ReceiptYield) [ran] [tree 381d825103ad] [world 2f1906870a] (2026-11-02T20:01:06Z)
- (step 1) `python3 plugin/tests/run.py test_receipt_yield` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: ReceiptYield 0s) / OK [ran] [tree 004f76eb3e7e] [world 2f1906870a] (2026-11-02T20:01:10Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_contract test_receipt_yield test_serve test_unattended && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [23.43s] [ran] [tree 004f76eb3e7e] [world 2f1906870a] (2026-11-02T20:02:02Z)
- (step 2) `python3 plugin/tests/run.py test_receipt_yield test_contract` → exit 0 · Ran 14 tests in 11.1s (2 classes, 16 at a time; slowest: Contract 11s, ReceiptYield 0s) / OK [ran] [tree 7d0d0811b2de] [world 2f1906870a] (2026-11-02T20:04:43Z)
- (step 3) `grep -q 'tasks a dollar' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 7d0d0811b2de] [world 2f1906870a] (2026-11-02T20:04:44Z)
- (ac 1) `python3 plugin/tests/run.py test_receipt_yield` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: ReceiptYield 0s) / OK [ran] [tree 7d0d0811b2de] [world 2f1906870a] (2026-11-02T20:04:53Z)
- (audit edge) `self: read the builder diff; yield_text guards zero/None spend and zero tasks; run_usd is defined at fm run's start and only grows under --max-usd, so the print is gated on measured spend; the contract receipt reuses the same spend value it already printed` → zero tasks, zero spend and None spend print no ratio (tested); a plain fm run measures no spend and prints no line [tree 7d0d0811b2de] (2026-11-02T20:04:53Z)
- (audit self) `self: read the builder diff; yield_text guards zero/None spend and zero tasks; run_usd is defined at fm run's start and only grows under --max-usd, so the print is gated on measured spend; the contract receipt reuses the same spend value it already printed` → no findings [tree 7d0d0811b2de] (2026-11-02T20:04:53Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T20:00:13Z planned from capture
- 2026-11-02T20:00:18Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2655.builder.md
- 2026-11-02T20:00:28Z focused
- 2026-11-02T20:00:29Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T20:04:16Z merged worktree-agent-a319979aa5169f146 (3 file(s))
- 2026-11-02T20:04:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a319979aa5169f146
- 2026-11-02T20:04:20Z focused
- 2026-11-02T20:04:23Z scope: plugin/lib/fmserve.py — fm run's end is where a drive run ends; the receipt line prints there
- 2026-11-02T20:05:44Z done
- 2026-11-02T20:05:49Z committed b05aae76 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2651 [FEATURE S, planned, 3 steps] fm task evidence --bench CMD --under MS: a benchmark that is a pass/fail proof, failing when the median is over the threshold (today…
- T-2653 [FEATURE S, active, 3 steps] Every nonzero fm exit prints one Next: command, not only a UsageError that carries one: a PolicyError, LockTimeout, CorruptState or V…
- T-2641 [FEATURE S, done, 3 steps] A removed fm verb or flag prints its tombstone (what replaced it and the task that removed it) instead of argparse's bare error; first …
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_contract.py
## Files touched
- plugin/tests/test_receipt_yield.py
- plugin/lib/fmcontract.py
- plugin/lib/fmserve.py
- CHANGELOG.md
