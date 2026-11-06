---
id: T-0952
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-15T21:07:00Z
updated: 2026-10-15T21:16:17Z
base: 6e4ab3f7d77da802461a522b340723af6f41091e
base_tree: cbb20bb41788ce724eb2224182a1c82cfb446cc6
verified: strong
---
# --affected also runs tests that historically change together with the edited files (the map's co-change pairs), so a hooks.json edit runs test_docs and test_doctor
## Raw request
> T-0951 (Doctor and docs tests know the PostToolUseValidate handler (T-0947 follow-up)) wasn't caught before it shipped: the T-0947 close ran only its affected tests; the wiring tests live in test_docs and test_doctor — fm check affected now covers lanes, and the full gates run before release
## Interpretation
T-0951's why-not-caught: the T-0947 lane ran only its name-linked tests, so the wiring tests (test_docs, test_doctor) that check hooks.json weren't affected and broke at release. The map already records co-change pairs (fmmap._co_change). Tests that historically change with a file are the ones most likely to break when it changes.
## Assumptions (confidence)
## Acceptance criteria
- [x] fmcli.affected adds the test files the map pairs with any changed file (fm map's co-change pairs, both directions) to the linked tests; a fixture repo where hooks.json and a test changed together in 3+ commits selects that test when only hooks.json changes — verify with `python3 plugin/tests/run.py -k AffectedPairs`
## Non-goals
## Approach (options → choice → why)
Options: co-change pairs from the map (chosen: generic, already computed); a hand-kept table of file → tests (drifts); always run test_docs and test_doctor (wasteful, and only fixes this case).
## Risks and rollback
## Execution prompt
## Steps
1. [x] AffectedPairs test, then use m['pairs'] in affected() for test files
## Resume here
## Docs impact
none: fm check --affected selects more tests; the help text already says 'linked tests'
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k AffectedPairs` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: AffectedPairs 0s) / FAILED (1 classes) [ran] [tree b69be58aa7aa] (2026-10-15T21:15:36Z)
- (step 1) `python3 plugin/tests/run.py -k AffectedPairs` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: AffectedPairs 0s) / OK [ran] [tree d20e3643710d] (2026-10-15T21:15:50Z)
- (ac 1) `python3 plugin/tests/run.py -k AffectedPairs` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: AffectedPairs 0s) / OK [ran] [tree d20e3643710d] (2026-10-15T21:15:50Z)
- (ac 1) `python3 plugin/tests/run.py -k AffectedPairs` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: AffectedPairs 0s) / OK [ran] [tree d20e3643710d] (2026-10-15T21:16:16Z)
- (audit intent) `main-thread: test proves red then green; in this repo hooks.json now pairs with test_docs.py` → ok: the T-0947 miss (wiring tests not run for a hooks.json edit) is now caught by the lanes' own affected run [tree d20e3643710d] (2026-10-15T21:16:16Z)
- (audit edge) `main-thread: test proves red then green; in this repo hooks.json now pairs with test_docs.py` → ok: pairs need 3+ shared commits and a 60% share, capped at 3 per file, so a sweeping commit adds nothing [tree d20e3643710d] (2026-10-15T21:16:16Z)
- (audit self) `main-thread: test proves red then green; in this repo hooks.json now pairs with test_docs.py` → no findings [tree d20e3643710d] (2026-10-15T21:16:16Z)
## Log
- 2026-10-15T21:07:00Z created
- 2026-10-15T21:12:29Z planned from capture
- 2026-10-15T21:14:50Z focused
- 2026-10-15T21:16:17Z done
- 2026-10-15T21:16:17Z committed e932532 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0953 [FEATURE S, done, 1 steps] Release 1.2.30 to GitHub main (user asked to push) — lesson: Run the full suite before release.py when a session changed hook wiring: t…
- T-0879 [FEATURE S, done, 0 steps] Catch it earlier: the test only covered tracked, already-linked tests; the map is built fr
- T-0214 [FEATURE M, deferred, 0 steps] Edit-time test sentinel — after Claude edits files, the tests linked to them (fm map test
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- similar finished tasks took 0–1 steps
## Lessons
- Name-based test links miss config files; the co-change history already knows which tests move with them.
## Plan gaps
- failed first: step 1 AffectedPairs test, then use m['pairs'] in affected() for test files
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
