---
id: T-2547
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T05:35:10Z
updated: 2026-11-02T06:16:06Z
base: b51f41f1856b45b9b479801fdb247c7e95b0ef72
base_tree: 0bae73d0979349aeb815551a7b9dcd678b7b312f
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T05:43:58Z
plan0_scope: [plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, CHANGELOG.md]
verified: strong
---
# fm genesis put refuses a Mission whose intake block has more briefs than grounding lines (a ## Grounding bullet per brief naming the code and the record)
## Raw request
> FEATURE: grounded Missions: fm genesis put refuses a Mission file whose intake block has a brief with no grounding line (a '## Grounding' section naming, per brief, the code that lacks it and the record that its failure happened)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] put of gen-N/mission-X.md with an intake block of 2 briefs and a ## Grounding section of 2 bullets, each naming a code file (word.py, word.md or an fm verb) passes; 1 bullet, or a bullet with no code reference, refuses naming what's missing; a mission with no intake block and other tower files are unaffected — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_genesis: the three cases (grounded, short, no code reference) and a non-mission file
2. [x] fmgenesis.put checks mission files: bullets under ## Grounding >= the intake block's items, each with a code reference
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GroundedMission` → ✗ exit 1 · Ran 1 tests in 2.5s (1 classes, 16 at a time; slowest: GroundedMission 0s) / FAILED (1 classes: test_genesis.GroundedMission) [ran] [tree 37d9bba60f4a] [world 2f1906870a] (2026-11-02T05:44:17Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GroundedMission` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: GroundedMission 0s) / FAILED (1 classes: test_genesis.GroundedMission) [ran] [tree f5eb48577f94] [world 2f1906870a] (2026-11-02T05:44:38Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 208 tests in 17.1s (24 classes, 16 at a time; slowest: GenesisRead 17s, GenerationReview 15s, GenesisCheck 14s) / FAILED (1 classes: test_genesis.GroundedMission) [ran] [tree 24337f0ab050] [world 2f1906870a] (2026-11-02T05:45:08Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 208 tests in 20.1s (24 classes, 16 at a time; slowest: GenerationReview 18s, ProofBeforePresentation 17s, GenesisRead 14s) / FAILED (1 classes: test_genesis.GenesisStep) [ran] [tree a7a1a24e6ab2] [world 2f1906870a] (2026-11-02T05:46:12Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 208 tests in 23.8s (24 classes, 16 at a time; slowest: GenesisRead 23s, GenerationReview 19s, GenesisCheck 17s) / FAILED (1 classes: test_genesis.GenesisStep) [ran] [tree ba98785c73ca] [world 2f1906870a] (2026-11-02T05:46:54Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 208 tests in 22.8s (24 classes, 16 at a time; slowest: GenesisRead 22s, GenerationReview 20s, GenesisCheck 17s) / OK [ran] [tree bd051fc624a4] [world 2f1906870a] (2026-11-02T05:47:42Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 208 tests in 12.2s (24 classes, 16 at a time; slowest: GenesisRead 11s, GenerationReview 10s, ProofBeforePresentation 9s) / OK [ran] [tree 5b91756ce840] [world 2f1906870a] (2026-11-02T05:55:47Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GroundedMission` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: GroundedMission 0s) / OK [ran] [tree 5b91756ce840] [world 2f1906870a] (2026-11-02T05:55:47Z)
- (audit edge) `self-review: the check runs only for gen-N/mission-*.md with an intake block, before the cold read; bullets counted under ## Grounding only; each needs a file, fm verb or module.function` → a Mission with no intake block, and every other tower file, pass untouched; a grounding section placed after the fence still counts; the name clash with the charter check's _grounded was caught by the test and renamed [tree 5b91756ce840] (2026-11-02T05:55:47Z)
- (audit self) `self-review: the check runs only for gen-N/mission-*.md with an intake block, before the cold read; bullets counted under ## Grounding only; each needs a file, fm verb or module.function` → no findings [tree 5b91756ce840] (2026-11-02T05:55:47Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 9f855b335e9b] [world 2f1906870a] (2026-11-02T06:16:06Z)
## Log
- 2026-11-02T05:35:10Z created
- 2026-11-02T05:37:23Z planned from capture
- 2026-11-02T05:43:56Z focused
- 2026-11-02T05:43:58Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T05:46:54Z tried: `python3 plugin/tests/run.py test_genesis` ×3 on step 2, failing the same way
- 2026-11-02T05:47:53Z scope: fmgenesis.put runs _mission_grounded (renamed: _grounded already names the charter check) for gen-N/mission-*.md before the cold read; test_genesis.GroundedMission plus the MISSION template and the wrapped-paragraph test gain grounding lines
- 2026-11-02T05:56:13Z done
- 2026-11-02T05:56:16Z committed 0c6813fb (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research T-2095-review: Verdict:** approve with nits. It meets the criteria as written. One resumability gap and one silent-skip case are worth fixing. I did not run `pl…
- decision 2026-10-31: [costly] Tower filing waits for the user's call on the cold-read rule: Missions 5-8's files and the Mission 3-4 critiques stay unfiled after 4-12 pu…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_genesis.py
## Lessons
- a module-level helper name can be silently shadowed by a later def of the same name; grep the module for the name before adding one
## Plan gaps
- failed first: step 1 red test in test_genesis: the three cases (grounded, short, no code reference) and a non-mission fi…
- failed first: step 2 fmgenesis.put checks mission files: bullets under ## Grounding >= the intake block's items, each wi…
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
