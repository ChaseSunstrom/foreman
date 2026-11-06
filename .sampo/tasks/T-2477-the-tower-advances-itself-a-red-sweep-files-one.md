---
id: T-2477
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T15:55:22Z
updated: 2026-11-01T16:08:32Z
base: b76e8b3964d4c1387e5379d8654967c11038cd37
base_tree: 3b0811b78eb6b127d2abe0079630db4900609ac9
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T15:55:23Z
plan0_scope: []
verified: strong
---
# The tower advances itself: a red sweep files one fix task per red row and is rerun when they close; a clean sweep writes the next Seed at once
## Raw request
> The tower advances itself: a red sweep files one fix task per red row and is rerun when they close; a clean sweep writes the next Seed at once
## Interpretation
Readings: (a) fm genesis sweep acts on its own verdict: red files a FIX task per red row (deduped by gen and row) and step routes to them, then to a rerun; clean calls the seed writer for gen N+1 at once, so the next Missions are the step's next action; (b) a scheduler runs the sweep unattended. (a): the user's rule names what a sweep does on each verdict; the drive and the hourly tick already carry step's next action.
## Assumptions (confidence)
## Acceptance criteria
- [x] a red sweep files one fix task per red row, never twice; step names the open one, then a rerun once they close — verify with `python3 plugin/tests/run.py test_genesis`
- [x] a clean sweep writes gen N+1's seed at once — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) In sweep(): red rows become FIX tasks via fmcli._create (source genesis, so round-first doesn't hold them; meta genesis_sweep=N:check dedupes), listed as a 'Fix tasks:' line in sweep.md; step()'s sweep stage names the first open one, then asks for a rerun when all are closed; a clean sweep calls _seed(n+1). Fails if: a fix task can't close its row (it stays open and holds the tower, which is the rule). 2) A trigger-table route (sweep_red → capture) through fmtriggers. Fails if: it splits one behaviour across two modules for no gain. 3) Use what exists: fmcli._create (fm scout's path), _seed, step's act(); nothing new beyond one helper. Likely outcome: ~30 lines in fmgenesis. 4) Do less: print the red rows as suggested fm capture lines. Fails if: the tower still waits on a session to act, which the rule forbids. Choice 1 (85%): the sweep owns its verdict's consequence, on what exists (3).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests
2. [x] sweep() files fixes and seeds on clean; step's sweep stage routes to the fixes
## Resume here
## Docs impact
MASTER's seed line (T-2477), CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_each_red_line_keeps_step_on_sweep_and_a_clean_one_moves_on test_genesis` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: GenesisSweep 0s) / FAILED (1 classes: test_genesis.GenesisSweep) [ran] [tree d74c6ec68564] (2026-11-01T15:55:36Z)
- `python3 plugin/tests/run.py -k test_each_red_line_keeps_step_on_sweep_and_a_clean_one_moves_on test_genesis` → ✗ exit 1 · Ran 1 tests in 2.4s (1 classes, 16 at a time; slowest: GenesisSweep 1s) / FAILED (1 classes: test_genesis.GenesisSweep) (start tree + this task's tests) [ran] [tree 8d8355faaa1a] (2026-11-01T15:56:48Z)
- `python3 plugin/tests/run.py -k test_each_red_line_keeps_step_on_sweep_and_a_clean_one_moves_on test_genesis` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: GenesisSweep 1s) / OK [ran] [tree 8d8355faaa1a] (2026-11-01T15:56:48Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 183 tests in 12.1s (18 classes, 16 at a time; slowest: GenesisRead 12s, GenesisCheck 9s, GenesisSweep 9s) / OK [ran] [tree 8d8355faaa1a] (2026-11-01T15:57:01Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 183 tests in 11.0s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree c91d3e9a9a80] (2026-11-01T15:57:27Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 183 tests in 11.1s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree c91d3e9a9a80] (2026-11-01T15:57:39Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 183 tests in 11.0s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree c91d3e9a9a80] (2026-11-01T16:03:06Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 183 tests in 11.0s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree c91d3e9a9a80] (2026-11-01T16:03:06Z)
- (audit intent) `main-thread lens pass over the sweep, _sweep_fixes and step diff plus the rewritten red-then-clean test` → a red sweep files one FIX task per red row (source genesis, so round-first never holds it), deduped by N:row, listed in sweep.md; step routes to the first open one, then to a rerun once all close; a clean sweep writes gen N+1's seed at once and prints the next action [tree c91d3e9a9a80] (2026-11-01T16:03:06Z)
- (audit edge) `main-thread lens pass over the sweep, _sweep_fixes and step diff plus the rewritten red-then-clean test` → a blocked fix task holds the tower as blocked (the rule: the tower can't pass a red sweep); a seed that can't be written (exists, stopped, no base) is a printed line, never a lost sweep; a fix task for a row that turns green on rerun is simply not refiled [tree c91d3e9a9a80] (2026-11-01T16:03:06Z)
- (audit operator) `main-thread lens pass over the sweep, _sweep_fixes and step diff plus the rewritten red-then-clean test` → the sweep prints its fix tasks, the seed it wrote and step's next action [tree c91d3e9a9a80] (2026-11-01T16:03:06Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree c91d3e9a9a80] (2026-11-01T16:04:03Z)
## Log
- 2026-11-01T15:55:22Z created
- 2026-11-01T15:55:22Z focused
- 2026-11-01T15:55:23Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T15:57:16Z scope: plugin/lib/fmgenesis.py (sweep, _sweep_fixes, step's sweep stage, the sweep printout), plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md
- 2026-11-01T16:03:32Z done
- 2026-11-01T16:03:34Z committed 044632b5 (4 files)
- 2026-11-01T16:03:42Z guard authorization added: publish
- 2026-11-01T16:08:32Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2095 [FEATURE M, done, 3 steps] fm genesis step: the tower's next action from its files, resumable after any kill — lesson: A resumable state machine over files has to…
- decision 2026-11-01: [cites: user steer 2026-11-01: standing rule, the tower advances itself: (2) a red sweep creates its own fix tasks and re-runs when they close; a cl…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
## Lessons
- A gate that reports red should also file the work that turns it green, or the loop waits on a session to read it
## Plan gaps
- failed first: step 1 red tests
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
