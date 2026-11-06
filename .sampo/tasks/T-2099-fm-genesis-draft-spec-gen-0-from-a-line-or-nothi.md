---
id: T-2099
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T05:11:00Z
updated: 2026-10-30T05:36:31Z
base: 62b95b2c3192f31a8dad83911cba70e019bcaab8
base_tree: d086a4a15a07b178952e6740464889da2c3a4e4f
plan0_at: 2026-10-30T05:14:26Z
plan0_scope: []
verified: ok
---
# fm genesis draft/spec — gen-0 from a line or nothing; per-project spec with a held-out…
## Raw request
> FEATURE: fm genesis draft/spec — gen-0 from a line or nothing; per-project spec with a held-out exam
## Interpretation
Genesis #13, brief 3: fm genesis draft writes a gen-0 from a line, a sweeping request or nothing, from the project (name, languages, gates, README head), the user's recent corrections and open briefs' MUST/NEVER lines (non-user ones marked unconfirmed), via one tool-less child with a deterministic fallback; cover(ref, draft) names what a draft misses of a reference gen-0 (the #13 exam's grader); fm genesis spec maps gen-0 §2 to exam kinds and generates a held-out exam in the project's languages, filed as spec.md.
## Assumptions (confidence)
## Acceptance criteria
- [x] draft from SEED_PROMPT.md's first line covers every MUST, NEVER and section of SEED_PROMPT.md; empty input gives a valid fallback draft; a stub child's capabilities are used; a non-user brief's MUST is marked unconfirmed; spec maps caps to kinds and files spec.md with a held-out exam — verify with `python3 plugin/tests/run.py test_genesis`
- [x] full gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) the child writes the whole gen-0: unvalidatable, drifts from the tower's shape; (b) a fixed template whose slots the facts fill, the child only adding context and capabilities, with a deterministic fallback: chosen, shape guaranteed, offline-testable; (c) the hand gen-0 with names swapped: Foreman-specific. Spec: (a) child-authored scenarios: costly; (b) caps mapped to fmexam kinds (an 'Exam:' suffix, else keywords) and fmexam.gen with author self: chosen, deterministic. Carry-over from a past run belongs to brief 4 (select/seed).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: draft cover, fallback, stub child caps, unconfirmed MUST, spec
2. [x] template plugin/templates/genesis.md + draft() + cover() + fm genesis draft
3. [x] spec(): caps to exam kinds, fmexam.gen held out, spec.md in SHAPE + fm genesis spec
4. [x] docs: MASTER.md, CHANGELOG, README if it belongs, plugin skill/command surface
5. [x] gates, review, finish, ship
## Resume here
<!-- auto -->
- 2026-10-30T05:31:17Z step 5/5: gates, review, finish, ship
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/templates/genesis.md
- touched since last checkpoint: plugin/tests/test_genesis.py, plugin/lib/fmgenesis.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `6 GenesisDraft tests written before the code` → Ran 6 tests: FAILED (red) before fmgenesis.draft/cover/spec existed [tree 6a311841edc7] (2026-10-30T05:23:09Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisDraft` → exit 0 · Ran 6 tests in 1.3s (1 classes, 16 at a time; slowest: GenesisDraft 1s) / OK [ran] [tree 6a311841edc7] (2026-10-30T05:23:11Z)
- (step 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 37 tests in 3.7s (6 classes, 16 at a time; slowest: GenesisLive 3s, GenesisCheck 2s, GenesisStep 2s) / OK [ran] [tree 6a311841edc7] (2026-10-30T05:23:14Z)
- (step 4) `grep -c 'fm genesis draft' CHANGELOG.md MASTER.md` → exit 0 · CHANGELOG.md:1 / MASTER.md:0 [ran] [tree 8c6b1297564c] (2026-10-30T05:24:40Z)
- (step 4) `grep -c 'genesis.*draft' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:1 [ran] [tree 56bd49d52fc4] (2026-10-30T05:29:24Z)
- (audit intent) `fm-reviewer intent lens over the T-2099 diff` → fallback now says why on stderr and in --json reason; unconfirmed brief lines stay marked + stderr (accepted) [tree 56bd49d52fc4] (2026-10-30T05:29:24Z)
- (audit adversary) `fm-reviewer adversary lens: README injection, secrets` → README head redacted and '<' neutralised so it can't close the <project> fence; child lines can't add MUST/NEVER (test 3) [tree 56bd49d52fc4] (2026-10-30T05:29:24Z)
- (audit edge) `fm-reviewer edge lens + red tests` → secret-shaped lines dropped before init; per-kind<3 refused; cover tag-word bug and short lines fixed; shared-kind total counted once [tree 56bd49d52fc4] (2026-10-30T05:29:25Z)
- (audit operator) `cost and side effects of draft/spec` → draft: one sonnet call, budget-checked; spec makes a fresh exam run per call (once per generation by design) [tree 56bd49d52fc4] (2026-10-30T05:29:25Z)
- (audit maintainer) `tests and structure` → 39 test_genesis green incl. bad-JSON child fallback, fence, secrets round trip, per-kind floor, shared-kind total [tree 56bd49d52fc4] (2026-10-30T05:29:25Z)
- (step 5) `plugin/tests/run.py test_genesis` → exit 0 · Ran 39 tests in 3.7s (6 classes, 16 at a time; slowest: GenesisLive 3s, GenesisCheck 2s, GenesisStep 2s) / OK [ran] [tree 56bd49d52fc4] (2026-10-30T05:33:26Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 39 tests in 3.7s (6 classes, 16 at a time; slowest: GenesisLive 3s, GenesisCheck 2s, GenesisStep 2s) / OK [ran] [tree 56bd49d52fc4] (2026-10-30T05:33:35Z)
- (ac 2) `fm check` → exit 0 · ✓ all 6 gates passed on this exact tree already (run at 05:32 UTC); cached (fm check --fresh reruns) [ran] [tree 56bd49d52fc4] (2026-10-30T05:33:35Z)
## Log
- 2026-10-30T05:11:00Z created
- 2026-10-30T05:14:19Z planned: it has criteria and steps
- 2026-10-30T05:14:25Z focused
- 2026-10-30T05:33:56Z done
- 2026-10-30T05:33:58Z committed b550eb06 (6 files)
- 2026-10-30T05:34:17Z guard authorization added: publish
- 2026-10-30T05:36:31Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261029-233102: Request: Genesis Mission 2 (#13 Genesis as a feature): fm genesis runs the whole tower by itself in any project — writes its own gen-0 …
- research mission-20261029-233102.pack: Genesis Mission 2 (#13 Genesis as a feature): fm genesis runs the whole tower by itself in any project — writes its own gen-0 from…
- T-2077 [RESEARCH L, planned, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
## Lessons
- cover() tag words counted as shared words; strip tags before fuzzy matching
## Files touched
- plugin/templates/genesis.md
- plugin/tests/test_genesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
