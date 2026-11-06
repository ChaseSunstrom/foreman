---
id: T-1456
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmledger.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_ledger_chain.py, CHANGELOG.md, README.md]
depends_on: []
source: discovered
created: 2026-10-22T13:42:41Z
updated: 2026-10-22T13:57:08Z
base: 46935c5f837dc4187d0a43d0e8ab92d8f9612008
base_tree: 74e200996640b266e4c688fd85fc484235fc5d4c
plan0_at: 2026-10-22T13:46:30Z
plan0_scope: [plugin/lib/fmledger.py, plugin/lib/fmcli.py, plugin/tests/test_ledger_chain.py, CHANGELOG.md, README.md]
verified: strong
---
# Ledger names crash damage and accepts it once
## Raw request
> Ledger: an unclean shutdown (2026-10-22 08:37, after the disk filled) left ledger.jsonl:34916 as 668 NUL bytes; every finish receipt now says 'chain broken' for good, so a later tamper hides behind it. Recognise an all-NUL line as crash damage, have fm verify-ledger --accept-damage record it as a ledger line (where, bytes, the bounding timestamps, the next line's claimed prev) and chain on past exactly that acknowledged line; and fsync ledger appends from fm commands (not hooks, which are over their SLO) so a crash can't zero them
## Interpretation
An unclean shutdown zero-filled the ledger's last unflushed block (foreman ledger.jsonl:34916, 668 NULs; volt's too). verify reads it as 'not a whole JSON line' and every receipt says broken for good, so a later tamper would hide behind it. Name a NUL-tailed line as crash damage; one acknowledgement (a chained ledger line naming the damaged line's hash) turns it into a known gap; new damage reads broken again.
## Assumptions (confidence)
## Acceptance criteria
- [x] a NUL-tailed line is named as crash damage with its bytes and stays broken until --accept-damage; after it verify passes naming the gap; a second damage (even the same size) is broken again; an edit is never accepted — verify with `cd plugin/tests && python3 -m unittest test_ledger_chain.Chain.test_crash_damage_is_named_until_accepted_once test_ledger_chain.Chain.test_an_ack_counts_only_for_the_damage_before_it test_ledger_chain.Chain.test_accept_damage_never_accepts_an_edit`
## Non-goals
## Approach (options → choice → why)
Options: (a) treat any NUL line as a gap silently: hides a deliberate wipe; (b) truncate/rewrite the damaged line: destroys evidence and breaks the next line's prev; (c) name it + explicit ack line keyed by the damaged line's hash (survives tidy's monthly roll, unlike a line number) → chosen. fsync on every append skipped: 5 ms each, hooks already over SLO, and briefs are written with fsync already.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] chain() names NUL-tailed lines, acks by hash; --accept-damage writes the ack
3. [x] accept today's damage in foreman and volt ledgers
## Resume here
<!-- auto -->
- 2026-10-22T13:48:18Z step 1/3: failing tests
- git: foreman/build; 3 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmledger.py, plugin/tests/test_ledger_chain.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/lib/fmledger.py, plugin/tests/test_ledger_chain.py
## Docs impact
CHANGELOG line; fm verify-ledger --help names --accept-damage
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_ledger_chain.Chain.test_crash_damage_is_named_until_accepted_once test_ledger_chain.Chain.test_an_ack_counts_only_for_the_damage_before_it test_ledger_chain.Chain.test_accept_damage_never_accepts_an_edit` → ✗ exit 1 · Ran 3 tests in 0.467s / FAILED (failures=3) [ran] [tree b30572c20ed9] (2026-10-22T13:46:36Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_ledger_chain.Chain.test_crash_damage_is_named_until_accepted_once test_ledger_chain.Chain.test_an_ack_counts_only_for_the_damage_before_it test_ledger_chain.Chain.test_accept_damage_never_accepts_an_edit` → exit 0 · Ran 3 tests in 1.938s / OK [ran] [tree abce3c8d2ddd] (2026-10-22T13:47:50Z)
- (step 3) `python3 plugin/bin/fm verify-ledger` → exit 0 · Ledger OK: head 0ad32bd1280d2b6e, 14538 chained lines from ledger.jsonl:20431 (the 21921 lines before it predate the chain); an edit to the last line shows only with --head (a finish receipt's). / Cra [ran] [tree abce3c8d2ddd] (2026-10-22T13:48:03Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_ledger_chain` → ✗ exit 1 · Ran 31 tests in 6.570s / FAILED (failures=4) [ran] [tree 273828135614] (2026-10-22T13:53:30Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_ledger_chain` → exit 0 · Ran 31 tests in 6.415s / OK [ran] [tree c53204e43256] (2026-10-22T13:54:46Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_ledger_chain.Chain.test_crash_damage_is_named_until_accepted_once test_ledger_chain.Chain.test_an_ack_counts_only_for_the_damage_before_it test_ledger_chain.Chain.test_accept_damage_never_accepts_an_edit` → exit 0 · Ran 3 tests in 0.857s / OK [ran] [tree 1cae68b25448] (2026-10-22T13:55:08Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-1456-review): 1 HIGH, 1 MEDIUM, 2 LOW, all fixed test-first (31/31 ledger tests). Real foreman ledger: damage at 34916 accepted after checking the lines before it chained; volt's NUL lines predate its chain.` → deletion before damage → caught via after_damage pin; forged/pre-planted ack only pops earlier pending keys; same-size zero runs keyed by the line before; --accept-damage refuses edits and a missing --head [tree 1cae68b25448] (2026-10-22T13:55:08Z)
- (audit edge) `fm-reviewer five-lens pass (research T-1456-review): 1 HIGH, 1 MEDIUM, 2 LOW, all fixed test-first (31/31 ledger tests). Real foreman ledger: damage at 34916 accepted after checking the lines before it chained; volt's NUL lines predate its chain.` → a zeroed line before the chain start predates it; a zeroed line keeping its prev prefix is checked against it [tree 1cae68b25448] (2026-10-22T13:55:08Z)
- (audit intent) `fm-reviewer five-lens pass (research T-1456-review): 1 HIGH, 1 MEDIUM, 2 LOW, all fixed test-first (31/31 ledger tests). Real foreman ledger: damage at 34916 accepted after checking the lines before it chained; volt's NUL lines predate its chain.` → fsync on append deliberately skipped (5 ms each, hooks over SLO; briefs already fsync via write_atomic) — decision in the brief's approach [tree 1cae68b25448] (2026-10-22T13:55:08Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-1456-review): 1 HIGH, 1 MEDIUM, 2 LOW, all fixed test-first (31/31 ledger tests). Real foreman ledger: damage at 34916 accepted after checking the lines before it chained; volt's NUL lines predate its chain.` → one pending dict + damage pointer in chain(); ack is a normal chained event [tree 1cae68b25448] (2026-10-22T13:55:08Z)
## Log
- 2026-10-22T13:42:41Z created
- 2026-10-22T13:44:58Z planned from capture
- 2026-10-22T13:46:29Z focused
- 2026-10-22T13:48:18Z paused: focus moved to T-1455
- 2026-10-22T13:52:44Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-22T13:52:44Z focused
- 2026-10-22T13:54:12Z set scope=['plugin/lib/fmledger.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_ledger_chain.py', 'CHANGELOG.md', 'README.md']
- 2026-10-22T13:54:12Z scope: + plugin/lib/fmcore.py — review HIGH: log_event must pin the line before crash damage (after_damage)
- 2026-10-22T13:57:06Z done
- 2026-10-22T13:57:08Z committed df577908 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- research T-1065-review: Verdict: changes needed.** Two MEDIUM findings, both about failures breaking normal use. I only read the code. This session had no shell, so I ra…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar finished tasks took 2–6 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
no test simulated an unclean shutdown's zero-filled tail; the first real crash found it
## Lessons
- A tamper-evident chain needs a defined, explicit path through accidental damage, or the first crash leaves it permanently 'broken' and blind; pin what the damage hides with the first write after it.
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_ledger_chain.py
- plugin/lib/fmcli.py
- plugin/lib/fmledger.py
- plugin/lib/fmcore.py
- CHANGELOG.md
