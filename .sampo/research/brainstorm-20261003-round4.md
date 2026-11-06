# Brainstorm round 4 (2026-10-03): grounded slate

127 new ideas (6 lenses x 2 rounds, past the 152 of rounds 1-3). Grounded against the code and this session.

## Slate
1. Guard replay corpus (user value, reliability, simplicity, bold bets: 4 lenses) — value 5, M, low risk. Replay the real Bash commands from Claude Code session logs through the current guard, compare with a stored baseline of verdicts, report newly blocked (likely false positives) and newly allowed (possible bypasses), accept to rebaseline; a gate when fmguard.py changes. Grounded: no replay exists; 121 session logs in this project alone; this session's guard work found two real bypasses only by accident and most friction was guard false positives.
2. Version pin for the mod (reliability) — value 3, S. fm doctor warns when the installed foreman-ui is older than the repo's. Grounded: fmdoctor has no such check; installed 0.4.0 lagged for a day.

## Inbox (followup)
- Guard block messages name one safe rewrite (simplicity/user value) — value 3, S; partly there for state-direct/core.
- Stale-lane sweeper in fm tidy (reliability) — value 2, S; fm lane list already reports orphans.
- Self-improvement scoreboard: did each fix's friction stop (bold bets) — value 3, M.
- Turn latency trace: time to first useful action (user value) — value 3, M.

## Dropped (already done, premise false, or cost over value now)
Secrets audits (T-0132), resume/stale checks (T-0113), shared palette/frame (kit.ts), removing the band duplicate (T-0181), atomic state writes (write_atomic), panel lint (every row kind already tested), policy-table guard and one view function (rewrites), shadow sessions, competing fix agents, nightly red team (costly), boring mode (the band already goes quiet).
