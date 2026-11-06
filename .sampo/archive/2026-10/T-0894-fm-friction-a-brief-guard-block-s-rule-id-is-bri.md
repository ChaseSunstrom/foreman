---
id: T-0894
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T16:40:34Z
updated: 2026-10-15T17:59:30Z
base: c059744919782bcc1b02aa987bac8d8f6769ce80
base_tree: 334b94561f8ea925373fa44c210bd9cf987da6bc
verified: strong
---
# Guard rule ids name the file kind of a path-only refusal (brief:path-py, not brief:path for every file)
## Raw request
> fm friction: a 'brief' guard block's rule id is brief:path for every tool and file; name the tool or file kind so distinct blocks don't merge
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] path-only refusals of different file kinds get distinct rule ids — verify with `python3 plugin/tests/run.py test_safety`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, then rule_id adds the extension
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_safety test_friction` → exit 0 · Ran 25 tests in 5.0s (8 classes, 16 at a time; slowest: Friction 5s, CleanupGate 1s, SecretsGate 1s) / OK [ran] [tree 334b94561f8e] (2026-10-15T17:30:46Z)
- (step 1) `python3 plugin/tests/run.py test_safety test_friction test_guard` → exit 0 · Ran 125 tests in 5.4s (50 classes, 16 at a time; slowest: Friction 5s, GuardAgainstBash 5s, Hook 2s) / OK [ran] [tree b3cd47438a0c] (2026-10-15T17:31:10Z)
- (ac 1) `python3 plugin/tests/run.py test_safety` → exit 0 · Ran 13 tests in 0.9s (6 classes, 16 at a time; slowest: SecretsGate 1s, CleanupGate 1s, RuleIds 1s) / OK [ran] [tree 7437f9fb679f] (2026-10-15T17:43:50Z)
- (audit adversary) `self review: a path-only refusal's rule id now carries the file's extension (brief:path-py, brief:path-md; extensionless stays brief:path), so fm friction counts distinct kinds apart; worded refusals unchanged` → rule ids only label refusals for reports and counting; no allow/deny decision reads them [tree 7437f9fb679f] (2026-10-15T17:43:50Z)
- (audit self) `self review: a path-only refusal's rule id now carries the file's extension (brief:path-py, brief:path-md; extensionless stays brief:path), so fm friction counts distinct kinds apart; worded refusals unchanged` → no findings [tree 7437f9fb679f] (2026-10-15T17:43:50Z)
## Log
- 2026-10-15T16:40:34Z created
- 2026-10-15T17:30:35Z planned from capture
- 2026-10-15T17:30:35Z focused
- 2026-10-15T17:41:30Z paused: focus moved to T-0902
- 2026-10-15T17:43:48Z focused
- 2026-10-15T17:43:50Z done
- 2026-10-15T17:43:51Z committed 23d528a (7 files)
- 2026-10-15T17:59:30Z commit redone as d0d01ab (its 2 files only); 23d528a had swept in T-0902's demo files
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0698 [FIX M, done, 4 steps] Friction batch 2026-10-09: IFS false block from heredoc data, an undefined-name gate, MASTER.md read hint, builder refused-command list — l…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–4 steps
## Files touched
- plugin/tests/test_safety.py
- plugin/lib/fmguard.py
- docs/demo.mp4
- demo/record.py
- plugin/lib/fmdoctor.py
- demo/demo.cast
- demo/demo.mp4
- demo/demo.svg
