---
id: T-1298
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T21:55:32Z
updated: 2026-10-21T00:53:27Z
base: 6df511c7d81977236773e820f49904226d4943c9
base_tree: 31e7f09ea3dff407abdc74828a2ddf65b048251f
plan0_at: 2026-10-21T00:45:29Z
plan0_scope: []
verified: strong
---
# Each 'system' refusal the --allow system route can't authorize ('too deep', a script written earlier and run here) ends with its own way forward instead of 'To authorize: fm task set … --allow system'
## Raw request
> The guard's generic 'To authorize: fm task set … --allow system' is offered for system blocks it can't authorize ('too deep', script written earlier); list the system details without a _hint case and give each its own way forward
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the guard's system-category refusals are listed in a test; each one --allow system can't lift carries its own hint and no --allow route, the others keep it; no verdict changes — verify with `python3 plugin/tests/run.py test_guard test_guard_diff`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test listing the system details and what each refusal ends with
2. [x] _hint cases for the ones missing; the generic --allow line only where it works
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 196 tests in 17.7s (61 classes, 16 at a time; slowest: GuardAgainstBash 16s, GuardCases 9s, Hook 6s) / FAILED (1 classes) [ran] [tree 143a83130a9f] (2026-10-21T00:46:34Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases` → exit 0 · Ran 196 tests in 15.6s (61 classes, 16 at a time; slowest: GuardAgainstBash 15s, GuardCases 7s, Hook 5s) / OK [ran] [tree b371a4787b14] (2026-10-21T00:47:27Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 196 tests in 16.7s (61 classes, 16 at a time; slowest: GuardAgainstBash 15s, GuardCases 8s, Hook 6s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b371a4787b14] (2026-10-21T00:48:00Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 196 tests in 15.9s (61 classes, 16 at a time; slowest: GuardAgainstBash 15s, GuardCases 7s, Hook 6s) / OK [ran] [tree b371a4787b14] (2026-10-21T00:48:00Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_guard_diff` → exit 0 · Ran 196 tests in 15.9s (61 classes, 16 at a time; slowest: GuardAgainstBash 15s, GuardCases 8s, Hook 5s) / OK [ran] [tree e4c9a4d95d78] (2026-10-21T00:48:44Z)
- `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases` → exit 0 · Ran 196 tests in 16.2s (61 classes, 16 at a time; slowest: GuardAgainstBash 15s, GuardCases 7s, Hook 6s) / OK [ran] [tree e4c9a4d95d78] (2026-10-21T00:48:44Z)
- (audit edge) `self: read the diff; message-only change, verdicts locked by the System table, T-1289's test and the corpus; _unread matches only system details about unreadable programs (can't read / too deep / too long to parse)` → a system refusal about what a program does (crontab, iptables, systemctl) keeps the --allow route (tested) [tree e4c9a4d95d78] (2026-10-21T00:48:44Z)
- (audit self) `self: read the diff; message-only change, verdicts locked by the System table, T-1289's test and the corpus; _unread matches only system details about unreadable programs (can't read / too deep / too long to parse)` → no findings [tree e4c9a4d95d78] (2026-10-21T00:48:44Z)
- `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases` → exit 0 · Ran 196 tests in 15.8s (61 classes, 16 at a time; slowest: GuardAgainstBash 15s, GuardCases 7s, Hook 5s) / OK [ran] [tree e4c9a4d95d78] (2026-10-21T00:51:15Z)
- (audit edge) `self: read the diff; message-only change, verdicts locked by the System table, T-1289's test and the corpus; _unread matches only system details about unreadable programs (can't read / too deep / too long to parse)` → a system refusal about what a program does (crontab, iptables, systemctl) keeps the --allow route (tested) [tree e4c9a4d95d78] (2026-10-21T00:51:15Z)
- (audit adversary) `self: read the diff; message-only change, verdicts locked by the System table, T-1289's test and the corpus; _unread matches only system details about unreadable programs (can't read / too deep / too long to parse)` → no verdict path touched (check() and findings unchanged); an agent can't use the new text to get a command through, since the refusal still blocks and the hint only says how to make the program readable to the guard [tree e4c9a4d95d78] (2026-10-21T00:51:15Z)
- (audit self) `self: read the diff; message-only change, verdicts locked by the System table, T-1289's test and the corpus; _unread matches only system details about unreadable programs (can't read / too deep / too long to parse)` → no findings [tree e4c9a4d95d78] (2026-10-21T00:51:15Z)
## Log
- 2026-10-20T21:55:32Z created
- 2026-10-20T23:31:42Z planned from capture
- 2026-10-21T00:45:20Z grounding: --allow system does lift every system refusal (checked: 'written earlier' and crontab both pass with allow=system). Premise reframed: for the refusals where the guard couldn't read the program (written earlier and run here, nests too deep, reads its program from a pipe, too long to parse in time) the message leads with the rewrite that makes it readable and drops the --allow route, which would lift every system check (crontab, firewall, systemctl) for the whole task; the rest keep the route. No verdict changes.
- 2026-10-21T00:45:29Z focused
- 2026-10-21T00:53:24Z done
- 2026-10-21T00:53:27Z committed 00f2b5e3 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1289 [CLEAN S, done, 2 steps] The guard's refusal of a script written and run in one command says how to go on: write it in one command (cat > f <<'EOF' or the Write t…
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- research T-0978-small-models: Measured, not guessed. Sources: two recorded Sonnet demo sessions (T-0979; T-0983/T-0984 were written by them), one [stale: plugin/tests/ru…
- decision 2026-10-16: T-0275: a script over the guard's parse budget stays allowed after the literal scan, not refused
- similar finished tasks took 2–2 steps
## Behaviour lock
No verdict changes: every command refused as system before is refused as system after (the existing System table and the T-1289 test still pass). Only the message text changes, for refusals the guard couldn't read.
## Lessons
- Check a captured premise in code before planning: '--allow system can't lift it' was false; the real issue was an over-broad route
## Plan gaps
- failed first: step 1 Failing test listing the system details and what each refusal ends with
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
