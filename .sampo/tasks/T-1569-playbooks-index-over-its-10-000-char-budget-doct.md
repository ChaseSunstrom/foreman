---
id: T-1569
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/skills/playbooks/SKILL.md, plugin/skills/playbooks/references/ui/INDEX.md, plugin/tests/test_docs.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T18:07:44Z
updated: 2026-10-22T18:09:24Z
base: f5badffbb7888d6523ecc6f759af59843076dfb1
base_tree: e63cf3b049148ad1542910cae9b73a6a153cdded
plan0_at: 2026-10-22T18:07:47Z
plan0_scope: [plugin/skills/playbooks/SKILL.md]
verified: strong
---
# Playbooks index over its 10,000-char budget: doctor's footprint check and the release check fail
## Raw request
> Playbooks index over its 10,000-char budget: doctor's footprint check and the release check fail
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm doctor's footprint check passes and the playbook index still names every reference — verify with `cd plugin/tests && python3 -m unittest test_doctor.CoreIntegrity.test_description_budget test_docs.Skills`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] shorten the long index lines
## Resume here
## Docs impact
CHANGELOG.md line
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_doctor.CoreIntegrity.test_description_budget` → ✗ exit 1 · Ran 1 test in 0.002s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree ab5924c33b2f] (2026-10-22T18:08:56Z)
- `cd plugin/tests && python3 -m unittest test_doctor.CoreIntegrity.test_description_budget` → exit 0 · Ran 1 test in 0.001s / OK [ran] [tree ab5924c33b2f] (2026-10-22T18:08:56Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_doctor.CoreIntegrity.test_description_budget test_docs.Skills` → exit 0 · Ran 9 tests in 0.005s / OK [ran] [tree ab5924c33b2f] (2026-10-22T18:08:57Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_docs.Skills test_board_verbs.BoardVerbs.test_release_check_runs_doctor_and_demo_in_a_temporary_home` → exit 0 · Ran 9 tests in 11.376s / OK [ran] [tree ab5924c33b2f] (2026-10-22T18:09:08Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_doctor.CoreIntegrity.test_description_budget test_docs.Skills` → exit 0 · Ran 9 tests in 0.005s / OK [ran] [tree c90b26a3afb3] (2026-10-22T18:09:18Z)
- (audit edge) `self: red on the start tree (footprint 10111 > 10000 broke doctor's check and the release check), green now at 8870 chars; the UI entries moved to references/ui/INDEX.md with the Foreman's-own marker; the index test now accepts a path named in its top-level stage's INDEX.md when that index is named in SKILL.md (nested templates/ resolve to ui/INDEX.md); both failing gate tests pass` → an INDEX.md not named in SKILL.md doesn't count, so an orphan stage index can't hide files [tree c90b26a3afb3] (2026-10-22T18:09:18Z)
- (audit maintainer) `self: red on the start tree (footprint 10111 > 10000 broke doctor's check and the release check), green now at 8870 chars; the UI entries moved to references/ui/INDEX.md with the Foreman's-own marker; the index test now accepts a path named in its top-level stage's INDEX.md when that index is named in SKILL.md (nested templates/ resolve to ui/INDEX.md); both failing gate tests pass` → T-1505 (fm check playbooks) takes over the budget ratchet and moves other stages when they grow [tree c90b26a3afb3] (2026-10-22T18:09:18Z)
- (audit self) `self: red on the start tree (footprint 10111 > 10000 broke doctor's check and the release check), green now at 8870 chars; the UI entries moved to references/ui/INDEX.md with the Foreman's-own marker; the index test now accepts a path named in its top-level stage's INDEX.md when that index is named in SKILL.md (nested templates/ resolve to ui/INDEX.md); both failing gate tests pass` → no findings [tree c90b26a3afb3] (2026-10-22T18:09:18Z)
## Log
- 2026-10-22T18:07:44Z created
- 2026-10-22T18:07:45Z focused
- 2026-10-22T18:08:20Z set scope=['plugin/skills/playbooks/SKILL.md', 'plugin/skills/playbooks/references/ui/INDEX.md', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-22T18:09:21Z done
- 2026-10-22T18:09:24Z committed 50de3204 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1505 [FEATURE M, planned, 3 steps] fm check playbooks: index, duplicates, token budget and reach
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-1494 [FEATURE M, done, 2 steps] 3D playbook: scene composition, budget and survival contract — lesson: API facts from memory in a playbook need a reviewer who checks e…
- decision 2026-10-22: Slate: round 1 = T-1488..T-1506 (19 tasks over clusters 1-11), round 2 = T-1507..T-1519 (clusters 12-24); skipped: clusters 25-26 (built already, or…
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–3 steps
## Why not caught
the affected-test runner doesn't link SKILL.md edits to test_doctor's footprint check
## Lessons
- An index that every new file must join needs its size budget checked by the same task that adds the line.
## Files touched
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/ui/INDEX.md
- plugin/tests/test_docs.py
- CHANGELOG.md
