---
id: T-2482
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T16:35:27Z
updated: 2026-11-01T16:48:26Z
base: 21cbd8b7b667d74c8315ca17fa9dba67e1d2ef8e
base_tree: 76990d33d7345677e9ecad344bd595b6395e27a1
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-11-01T16:35:28Z
plan0_scope: []
verified: strong
---
# fm genesis seed's draft fails its cold read: it ranks polish areas above §2 capabilities with tier 3-4 gaps, carries gen-1's stale one-at-a-time Order of work, and loses the draft when the read fails
## Raw request
> fm genesis seed's draft fails its cold read: it ranks polish areas above §2 capabilities with tier 3-4 gaps, carries gen-1's stale one-at-a-time Order of work, and loses the draft when the read fails
## Interpretation
Readings: (a) fix the seed writer so its output meets the standing intent and the steers: capability areas first, a generated Order of work with parallel lanes, and a failed read keeps the draft for revision; (b) hand-write gen-2's seed only. (a): every later generation's seed comes from this writer (the tower advances itself).
## Assumptions (confidence)
## Acceptance criteria
- [x] the seed ranks §2 capability areas before other areas, writes its own Order of work with parallel lanes, and keeps its draft when the read fails — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) In _seed: sort key (not a §2 capability area, most empty cells, most open); a generated '## Order of work' (table order; independent Missions in parallel lanes up to fm lane max, each with its own critique, merged in table order; then drift, sweep, selection) added to MADE so the base's isn't carried; on a put ValueError, write the draft to p.dir/genesis-seed-draft-N.md and name it in the error. Fails if: a capability area with no open cell is ranked (it isn't: only open rows rank). 2) Rank by gap-map tier. Fails if: the gap map is per capability and absent for added areas. 3) Use what exists: all_caps(p, gen0) already names the capabilities in _seed; MADE already excludes generated headings. Likely outcome: ~20 lines. 4) Do less: hand-write gen-2's seed. Fails if: gen 3's seed fails the same way. Choice 1 (85%): it fixes the writer every generation uses, on what exists (3).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests
2. [x] ranking, Order of work, kept draft
## Resume here
## Docs impact
MASTER's seed line (T-2482), CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_seed_writes_the_next_seed_from_the_kept_ancestor -k test_a_seed_whose_cold_read_fails_keeps_its_draft test_genesis` → ✗ exit 1 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: GenesisSelect 0s) / FAILED (1 classes: test_genesis.GenesisSelect) [ran] [tree 63bba3af30b0] (2026-11-01T16:35:48Z)
- `python3 plugin/tests/run.py -k test_seed_writes_the_next_seed_from_the_kept_ancestor -k test_a_seed_whose_cold_read_fails_keeps_its_draft test_genesis` → ✗ exit 1 · Ran 2 tests in 1.6s (1 classes, 16 at a time; slowest: GenesisSelect 0s) / FAILED (1 classes: test_genesis.GenesisSelect) (start tree + this task's tests) [ran] [tree d44f13393842] (2026-11-01T16:36:49Z)
- `python3 plugin/tests/run.py -k test_seed_writes_the_next_seed_from_the_kept_ancestor -k test_a_seed_whose_cold_read_fails_keeps_its_draft test_genesis` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: GenesisSelect 0s) / OK [ran] [tree d44f13393842] (2026-11-01T16:36:49Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 184 tests in 11.1s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree d44f13393842] (2026-11-01T16:37:00Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 184 tests in 11.1s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree 95c2a5443215] (2026-11-01T16:37:20Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 184 tests in 11.0s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree 95c2a5443215] (2026-11-01T16:43:08Z)
- (audit intent) `main-thread lens pass over the _seed diff and its two tests; gen-2's seed then filed with the fixed writer (only rule 7 needed a hand edit in the kept draft)` → §2 capability areas rank first, then empty cells; the seed writes its own Order of work (parallel lanes, merged in table order, the sweep's fix-or-seed step) and never carries a base's; a failed read keeps the draft at p.dir/genesis-seed-draft-N.md, named in the error [tree 95c2a5443215] (2026-11-01T16:43:08Z)
- (audit edge) `main-thread lens pass over the _seed diff and its two tests; gen-2's seed then filed with the fixed writer (only rule 7 needed a hand edit in the kept draft)` → an area named like a capability with a number prefix still matches (the prefix is stripped); the kept draft is overwritten by the next failed attempt for the same generation [tree 95c2a5443215] (2026-11-01T16:43:08Z)
- (audit operator) `main-thread lens pass over the _seed diff and its two tests; gen-2's seed then filed with the fixed writer (only rule 7 needed a hand edit in the kept draft)` → the error says where the draft is and the put command that files it [tree 95c2a5443215] (2026-11-01T16:43:08Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 95c2a5443215] (2026-11-01T16:44:03Z)
## Log
- 2026-11-01T16:35:27Z created
- 2026-11-01T16:35:28Z focused
- 2026-11-01T16:35:28Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-11-01T16:37:08Z scope: plugin/lib/fmgenesis.py (_seed ranking, Order of work, kept draft; MADE), plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md
- 2026-11-01T16:43:33Z done
- 2026-11-01T16:43:36Z committed 3a3da713 (4 files)
- 2026-11-01T16:44:03Z guard authorization added: publish
- 2026-11-01T16:48:26Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2191 [FEATURE L, done, 4 steps] The user's standing intent (steer 2026-10-30 #7, STANDING INTENT): file it in the tower… — lesson: A rule that says 'a format check is …
- T-2160 [FEATURE M, done, 3 steps] Write the steer's standing rules (testing cadence, real coverage, long-horizon tier as… — lesson: Two readers of the same rows (steer_c…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
## Why not caught
no test read a seed against the newer steers; the cold read caught it the first time a seed was generated after them
## Lessons
- A generated document that carries sections forward verbatim goes stale exactly where the rules changed; generate the rule-bearing sections fresh
## Plan gaps
- failed first: step 1 red tests
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
