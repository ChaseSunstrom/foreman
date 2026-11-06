---
id: T-2114
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T07:24:31Z
updated: 2026-10-30T07:51:11Z
base: e08d2d73fbafeb6bcc787a97bedc333257a3c2dc
base_tree: 5e26ab64d91e6b5604f801fc9548fb053342c17b
plan0_at: 2026-10-30T07:36:24Z
plan0_scope: []
verified: strong
---
# FIX S: genesis drift's cold read flags the seed's user-steer section (gen-0 doesn't name…
## Raw request
> FIX S: genesis drift's cold read flags the seed's user-steer section (gen-0 doesn't name later steers): pass decisions.md's '[cites: user steer' rows to the reader as additions that may only tighten gen-0, never weaken/widen/drop it
## Interpretation
fm genesis drift's cold read only sees gen-0, so a Seed restating the user's later standing rules (decisions.md rows tagged 'cites: user steer') reads as drift. Pass those rows to the reader in a <user-steers> fence, after gen-0, as additions that may only tighten it.
## Assumptions (confidence)
## Acceptance criteria
- [x] the cold read's prompt holds the user-steer decisions after gen-0, not plain decisions — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Collect c._decision_rows(p) rows whose tags hold 'cites: user steer', c.plain each, fence-escape like the seed; DRIFT_CHILD says a steer may only add to gen-0. Rejected: deterministic allow-list of steer lines (seed paraphrases them); letting steers into _constraints' verbatim check (would let a planted decision widen gen-0).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test first: the stub sees the steers fenced after gen-0 (red)
2. [x] pass the steers to the cold read; DRIFT_CHILD, MASTER, CHANGELOG; rerun fm genesis drift 1 live
## Resume here
<!-- auto -->
- 2026-10-30T07:40:06Z step 1/2: test first: the stub sees the steers fenced after gen-0 (red)
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py
- touched since last checkpoint: MASTER.md, plugin/lib/fmgenesis.py, CHANGELOG.md
- failures met: assertionerror: tuples differ: (0, 'unread') != (0, 'drifted'); indexerror: list index out of range
## Docs impact
MASTER.md cold-read sentence; CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisDrift.test_the_cold_read_sees_the_users_later_steers_as_tightening_only` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: GenesisDrift 0s) / FAILED (1 classes) [ran] [tree 1e3243da9884] (2026-10-30T07:36:35Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 146 tests in 8.4s (32 classes, 16 at a time; slowest: Fences 8s, GenesisLive 4s, GenesisSweep 4s) / OK [ran] [tree a5ce6e2a2036] (2026-10-30T07:36:57Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisDrift.test_a_cold_read_counts_only_seed_lines_and_no_read_fails` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: GenesisDrift 0s) / FAILED (1 classes) [ran] [tree 809ff94142d1] (2026-10-30T07:38:19Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 146 tests in 8.4s (32 classes, 16 at a time; slowest: Fences 8s, GenesisLive 4s, GenesisSweep 4s) / OK [ran] [tree 38f2d80e4507] (2026-10-30T07:39:49Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 66 tests in 3.9s (11 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 3s, GenesisCheck 3s) / OK [ran] [tree 38f2d80e4507] (2026-10-30T07:43:34Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisDrift.test_the_cold_read_sees_the_users_later_steers_as_tightening_only` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: GenesisDrift 0s) / OK [ran] [tree 38f2d80e4507] (2026-10-30T07:43:34Z)
- (audit edge) `self: diff re-read; steers come only from decisions.md rows tagged cites: user steer, c.plain'd and fence-escaped so a steer can't close <seed>/<gen-0>; the child prompt says a steer only adds to gen-0; quotes match on logical lines so a wrapped bullet counts; live gen-1 drift clean; full gates EXIT 0` → a seed line wrapped across two lines with a nested list marker stays separate (regex skips - * + 1.); no steers gives an empty fence, still clean [tree 38f2d80e4507] (2026-10-30T07:43:34Z)
- (audit adversary) `self: diff re-read; steers come only from decisions.md rows tagged cites: user steer, c.plain'd and fence-escaped so a steer can't close <seed>/<gen-0>; the child prompt says a steer only adds to gen-0; quotes match on logical lines so a wrapped bullet counts; live gen-1 drift clean; full gates EXIT 0` → a decision text holding </user-steers> or <seed> is fenced to ‹; only rows tagged by fm decide --cites user steer count, plain decisions don't reach the prompt [tree 38f2d80e4507] (2026-10-30T07:43:34Z)
- (audit intent) `self: diff re-read; steers come only from decisions.md rows tagged cites: user steer, c.plain'd and fence-escaped so a steer can't close <seed>/<gen-0>; the child prompt says a steer only adds to gen-0; quotes match on logical lines so a wrapped bullet counts; live gen-1 drift clean; full gates EXIT 0` → a steer may only tighten gen-0, said in the child prompt; the verbatim MUST/NEVER check (_constraints) is unchanged [tree 38f2d80e4507] (2026-10-30T07:43:34Z)
- (audit self) `self: diff re-read; steers come only from decisions.md rows tagged cites: user steer, c.plain'd and fence-escaped so a steer can't close <seed>/<gen-0>; the child prompt says a steer only adds to gen-0; quotes match on logical lines so a wrapped bullet counts; live gen-1 drift clean; full gates EXIT 0` → no findings [tree 38f2d80e4507] (2026-10-30T07:43:34Z)
## Log
- 2026-10-30T07:24:31Z created
- 2026-10-30T07:36:23Z set type=FIX, tier=S
- 2026-10-30T07:36:23Z planned: it has criteria and steps
- 2026-10-30T07:36:23Z focused
- 2026-10-30T07:38:11Z steer: widened — the live rerun showed a quote across a wrapped seed bullet scored 'didn't count' (the matcher reads physical lines); joined continuation lines, test-first; the seed's Completeness line itself drifted (dropped 'other agents, Desktop') and is restored to gen-0's surfaces
- 2026-10-30T07:43:36Z done
- 2026-10-30T07:43:37Z committed 5c844356 (4 files)
- 2026-10-30T07:43:42Z guard authorization added: publish
- 2026-10-30T07:51:11Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- research T-2104-review: Verdict: changes needed.** One HIGH finding makes sweep red for good once its Mission tasks are archived. A MEDIUM finding makes a cold read that…
- decision 2026-10-30: [cites: user steer 2026-10-29: NO IDEA IS KILLED FOR AMBITION] Genesis standing rule: no idea is killed for ambition — a failed spike gets ≥2 genuin…
## Lessons
- A seed that paraphrases gen-0 drifts: quote its MUST/NEVER lines verbatim; match a reader's quotes on logical (unwrapped) lines
## Plan gaps
- failed first: step 1 test first: the stub sees the steers fenced after gen-0 (red)
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmgenesis.py
- plugin/tests/test_genesis.py
