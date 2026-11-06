---
id: T-0196
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmwatch.py,plugin/tests/test_ui.py,mods/foreman-ui/hooks/register.tsx,mods/foreman-ui/types/index.d.ts,mods/foreman-ui/tests/foreman-ui.test.tsx,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T19:48:54Z
updated: 2026-10-03T19:50:22Z
base: 4e73a59643ca6095cbf0c07a9bb23d069d16dc22
base_tree: b1e7176617380bcf445d3605d359899d78240473
verified: strong
---
# Dashboard: a brainstorm whose ideas were grounded into a slate folds to one line
## Raw request
> Dashboard: a brainstorm whose ideas were grounded into a slate folds to one line
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] grounded brainstorms are flagged and fold in the pane — verify with `python3 plugin/tests/run.py -k test_the_newest_brainstorm_shows_while_it_runs_and_after && cd mods/foreman-ui && claude plugin test .`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] grounded flag; the card folds
3. [x] gates, sync the dev copy
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_the_newest_brainstorm_shows_while_it_runs_and_after && cd mods/foreman-ui && claude plugin test .` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: UiView 0s) / FAILED (1 classes) [ran] [tree 7f5b4ac578c9] (2026-10-03T19:49:03Z)
- (step 2) `python3 plugin/tests/run.py -k test_the_newest_brainstorm_shows_while_it_runs_and_after && cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 59 tests across 1 file. [2.55s] [ran] [tree 1e66c6f15772] (2026-10-03T19:49:21Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 2 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.6    35.1     150  [0] / SessionEnd                  28.1    30.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 59 tests across 1 file. [2.49s]; python3 plugin/tests/run.py → exit 0 · Ran 613 tests in 22.4s (1 [ran] [tree ff77e8352a91] (2026-10-03T19:50:14Z)
- (ac 1) `python3 plugin/tests/run.py -k test_the_newest_brainstorm_shows_while_it_runs_and_after && cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 59 tests across 1 file. [2.57s] [ran] [tree ff77e8352a91] (2026-10-03T19:50:22Z)
- (audit self) `self-review: grounded means a brainstorm-*.md research note written after ideas.md (fm research add of the slate); a running brainstorm and one with no note keep their bullets; the live project reports grounded=true for round 4; the dev copy is synced and reloads when this turn ends` → no findings [tree ff77e8352a91] (2026-10-03T19:50:22Z)
## Log
- 2026-10-03T19:48:54Z created
- 2026-10-03T19:48:54Z focused
- 2026-10-03T19:50:22Z done
- 2026-10-03T19:50:22Z committed 5e06eaf (6 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0108-review: [instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
## Lessons
- A list on a dashboard needs a 'handled' state as well as an age: recent and done looked the same.
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/tests/test_ui.py
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmwatch.py
- CHANGELOG.md
