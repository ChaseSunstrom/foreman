---
id: T-2026
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T18:21:44Z
updated: 2026-10-29T18:24:07Z
base: 10f148a9faa123deca26235d7f3611b7261fdd0e
base_tree: 4a8a3291ed993306bf0c6fb84ef91e71bd06e526
plan0_at: 2026-10-29T18:21:44Z
plan0_scope: []
verified: strong
---
# UserPromptSubmit hook: compile only named cards, lazy module patterns, briefs and last_change once
## Raw request
> UserPromptSubmit hook: compile only named cards, lazy module patterns, briefs and last_change once
## Interpretation
Same as T-2024: the prompt hook runs every user turn; make it faster with identical output and record numbers.
## Assumptions (confidence)
## Acceptance criteria
- [x] card answers unchanged, one brief load, one ledger read per prompt — verify with `python3 plugin/tests/run.py test_cards_at_prompt test_ledger_chain test_nudges`
## Non-goals
## Approach (options → choice → why)
Same as T-2024: prefilter card names by substring, c.lazy for module patterns, one load_briefs for state and Next, memo last_change on the ledger's inode, size and mtime.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Implement and measure (done under T-2024)
## Resume here
<!-- auto -->
- 2026-10-29T18:21:45Z step 1/1: Implement and measure (done under T-2024)
- git: foreman/build; 9 uncommitted: CHANGELOG.md, plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmlib.py, plugin/lib/fmplugins.py, plugin/tests/test_cards_at_prompt.py, plugin/tests/test_ledger_chain.py, plugin/tests/test_nudges.py
- touched since last checkpoint: plugin/tests/test_cards_at_prompt.py, plugin/lib/fmbus.py, plugin/lib/fmcore.py, plugin/lib/fmlib.py, plugin/lib/fmplugins.py, plugin/lib/fmhooks.py, plugin/tests/test_ledger_chain.py, plugin/tests/test_nudges.py, CHANGELOG.md
## Docs impact
CHANGELOG Perf line under Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cards_at_prompt test_ledger_chain test_nudges` → exit 0 · Ran 53 tests in 4.0s (7 classes, 16 at a time; slowest: Chain 4s, Receipt 2s, Revisit 1s) / OK [ran] [tree 38eefc5a578f] (2026-10-29T18:23:04Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 18:21 UTC) [ran] [tree 38eefc5a578f] (2026-10-29T18:23:09Z)
- (ac 1) `python3 plugin/tests/run.py test_cards_at_prompt test_ledger_chain test_nudges` → exit 0 · Ran 53 tests in 4.0s (7 classes, 16 at a time; slowest: Chain 4s, Revisit 2s, Receipt 1s) / OK [ran] [tree 38eefc5a578f] (2026-10-29T18:23:27Z)
- (audit intent) `self-review (risk budget spent, no subagents): read the diff of fmlib.cards_named, fmcore.last_change, fmhooks.user_prompt_submit and the c.lazy swaps; the prefilter keeps every name a match needs (a regex hit implies the substring), the memo keys on inode, size and mtime so rotation, truncation and appends all miss` → the prompt hook answers the same cards and Next line, measured 127 -> 101 ms median; tests pin one brief load, one ledger read and named-only compiles [tree 38eefc5a578f] (2026-10-29T18:23:27Z)
- (audit edge) `self-review (risk budget spent, no subagents): read the diff of fmlib.cards_named, fmcore.last_change, fmhooks.user_prompt_submit and the c.lazy swaps; the prefilter keeps every name a match needs (a regex hit implies the substring), the memo keys on inode, size and mtime so rotation, truncation and appends all miss` → no names in the message returns [] before any compile; a rotated ledger has a new inode; an append changes size; a missing ledger skips the memo (sig None) and reads as before [tree 38eefc5a578f] (2026-10-29T18:23:27Z)
## Log
- 2026-10-29T18:21:44Z created
- 2026-10-29T18:21:44Z redo of T-2024: takes over its start point and edited files
- 2026-10-29T18:21:44Z focused
- 2026-10-29T18:24:06Z done
- 2026-10-29T18:24:07Z committed 3d6a26f6 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2024 [PERFORMANCE M, dropped, 2 steps] UserPromptSubmit hook: cards_named compiles a ~9 ms alternation of every card name each…
- T-2020 [PERFORMANCE M, done, 2 steps] Hooks compile regexes on first use: importing fmcore, fmguard and fmhooks compiles none of their 191 module-level patterns — lesson…
- T-2025 [PERFORMANCE M, planned, 2 steps] SessionStart hook 169 ms: fmaway.since scans every prompt in every ledger file for the…
- decision 2026-10-21: Accept foreman-ui's supply entry after T-1434 named its hooks module
- the similar finished task took 2 steps
- start here (files T-2020 touched): plugin/tests/test_core.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, CHANGELOG.md
## Measurements
UserPromptSubmit median 127 -> 101 ms, min 123 -> 98 ms (interleaved, 3 rounds x 15 runs, against the T-2023 tree)
## Lessons
- Profiles taken in a copied state dir miss inode-keyed caches (the brief index), so they overstate load_briefs; measure the live hook too. And a DONE-WHEN -k filter must match a test in every module named, or the criterion can never pass.
## Files touched
- plugin/tests/test_cards_at_prompt.py
- plugin/lib/fmbus.py
- plugin/lib/fmcore.py
- plugin/lib/fmlib.py
- plugin/lib/fmplugins.py
- plugin/lib/fmhooks.py
- plugin/tests/test_ledger_chain.py
- plugin/tests/test_nudges.py
- CHANGELOG.md
