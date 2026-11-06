---
id: T-2171
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T15:07:09Z
updated: 2026-10-30T18:04:16Z
base: 9d2f5423fedf98638b02f727f048925eb317b4bd
base_tree: e595737ad29edbdb18905ef24d6494ec40c576d0
plan0_at: 2026-10-30T17:53:28Z
plan0_scope: []
verified: strong
---
# fm genesis select doesn't mark lineage.md choices provisional (steer 1 rule 4): until…
## Raw request
> FIX: fm genesis select doesn't mark lineage.md choices provisional (steer 1 rule 4): until the end-of-run exam each select/seed choice is written 'provisional' and names the signals it used (free arms, Haiku smoke, fm outcomes, cold fm second); the end-of-run exam confirms or reverses each, and fm genesis check flags an unmarked choice
## Interpretation
Steer 1 rule 4: until the end-of-run exam on the production model, every selection is provisional. fm genesis select writes each '## gen-N' lineage section with a '- provisional:' line naming the signals it used (the exam run, its agent and the train counts: free arms or the Haiku smoke run), and fm genesis check reports a lineage section with neither a provisional line nor an end-of-run '- confirmed:' or '- reversed:' line, so the sweep stays red on an unmarked choice. Confirming or reversing at the end is the end-of-run exam's job (T-2160); this task only makes the mark and the check. Once it lands, steer rule 254 gets its check.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis select writes '- provisional:' with the run, agent and train counts it used into its lineage section — verify with `python3 plugin/tests/run.py test_genesis.GenesisSelect`
- [x] fm genesis check (and so the sweep) names a lineage gen section with no provisional, confirmed or reversed line — verify with `python3 plugin/tests/run.py test_genesis.GenesisCheck test_genesis.GenesisSweep`
- [x] steer rule 273's check moves from pending T-2171 to a passing test id, and fm doctor passes it — verify with `fm doctor --full -v`
## Non-goals
## Approach (options → choice → why)
Options: (a) select writes a '- provisional:' line naming its run, agent and graded lines, and check() gains a lineage part (each '## gen-N' needs provisional, confirmed or reversed) that fails the check's exit and the sweep's genesis check row (chosen: the mark is made where the choice is made, and the gate reads it back); (b) a provisional flag in exam.jsonl (rejected: lineage.md is where a choice is read, and select writes it); (c) only a doc rule (rejected: steer 2 wants an automatic check). No live lineage.md exists yet (no select has run), so the live part is steer rule 273's check moving from pending to a test id.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: select's provisional line; check names an unmarked lineage section
2. [x] implement: the line in _select, a lineage part in check(), the sweep row picks it up
3. [x] mark the live lineage.md (re-put through the cold read), fm decide --check for rule 254, docs
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisSelect test_genesis.GenesisCheck` → ✗ exit 1 · Ran 19 tests in 8.6s (2 classes, 16 at a time; slowest: GenesisCheck 8s, GenesisSelect 1s) / FAILED (2 classes) [ran] [tree f3a366c746b6] (2026-10-30T17:53:56Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 89 tests in 10.9s (13 classes, 16 at a time; slowest: GenesisCheck 10s, GenesisLive 8s, GenesisSweep 8s) / OK [ran] [tree 3b15d955ba95] (2026-10-30T17:54:28Z)
- (ac 3) `fm doctor --full -v` → exit 0 · PASS  upstream issues      no error seen twice in 7 days matches the 4 known Claude Code issue(s) / fm doctor: OK (47 pass, 8 warn, 0 fail) [ran] [tree 3b15d955ba95] (2026-10-30T17:56:23Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 89 tests in 6.0s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree 18369c62762d] (2026-10-30T17:57:44Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 89 tests in 6.8s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree c09eef84a852] (2026-10-30T17:58:10Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 89 tests in 5.9s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree c09eef84a852] (2026-10-30T17:58:10Z)
- (audit intent) `foreman:fm-reviewer` → approve with nits: honest signal line; confirm writer captured as T-2197 [tree c09eef84a852] (2026-10-30T17:58:20Z)
- (audit maintainer) `foreman:fm-reviewer` → sweep row tested; hand-written gen headings checked; message names the fix [tree c09eef84a852] (2026-10-30T17:58:20Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GenesisSelect` → exit 0 · Ran 7 tests in 1.0s (1 classes, 16 at a time; slowest: GenesisSelect 1s) / OK [ran] [tree c09eef84a852] (2026-10-30T18:00:05Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis.GenesisCheck test_genesis.GenesisSweep` → exit 0 · Ran 19 tests in 5.5s (2 classes, 16 at a time; slowest: GenesisCheck 5s, GenesisSweep 4s) / OK [ran] [tree c09eef84a852] (2026-10-30T18:00:05Z)
- (ac 3) `fm doctor --full -v` → exit 0 · PASS  upstream issues      no error seen twice in 7 days matches the 4 known Claude Code issue(s) / fm doctor: OK (48 pass, 7 warn, 0 fail) [ran] [tree c09eef84a852] (2026-10-30T18:00:05Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 89 tests in 5.9s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree c09eef84a852] (2026-10-30T18:00:05Z)
- (step 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 89 tests in 5.9s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree c09eef84a852] (2026-10-30T18:00:05Z)
- (audit intent) `one foreman:fm-reviewer pass (five lenses); 2 MEDIUM + 3 LOW: 4 fixed test-first, the confirm writer captured as T-2197` → select marks each choice provisional and names the one exam run it rests on; check and sweep fail an unmarked choice; steer rule 273's check is a passing test id [tree c09eef84a852] (2026-10-30T18:00:05Z)
- (audit edge) `one foreman:fm-reviewer pass (five lenses); 2 MEDIUM + 3 LOW: 4 fixed test-first, the confirm writer captured as T-2197` → hand-written '## gen-2 (kept)' headings are checked; _stopped and seed's verdict read the first bullet, untouched [tree c09eef84a852] (2026-10-30T18:00:05Z)
- (audit adversary) `one foreman:fm-reviewer pass (five lenses); 2 MEDIUM + 3 LOW: 4 fixed test-first, the confirm writer captured as T-2197` → the line carries only c.plain'd run ids, counts and the agent name [tree c09eef84a852] (2026-10-30T18:00:05Z)
## Log
- 2026-10-30T15:07:09Z created
- 2026-10-30T16:21:38Z planned: it has criteria and steps
- 2026-10-30T17:53:27Z criterion 3 text: the live lineage.md sections carry the mark and steer rule 254 has a passing check → steer rule 273's check moves from pending T-2171 to a passing test id, and fm doctor passes it
- 2026-10-30T17:53:27Z focused
- 2026-10-30T18:00:28Z done
- 2026-10-30T18:00:29Z committed 65aca49e (4 files)
- 2026-10-30T18:01:05Z guard authorization added: publish
- 2026-10-30T18:04:16Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: [revisited: until the end-of-run exam, selection] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pendi…
- T-2161 [FEATURE M, dropped, 0 steps] fm genesis select marks each lineage.md choice provisional until the end-of-run exam…
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Until the end-of-run exam, selection between rewritten Seeds an…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- the similar finished task took 5 steps
## Why not caught
no test read lineage.md for a provisional mark; steer rule 273 sat on a pending check until this task
## Lessons
- A mark that a later stage must settle needs both halves or a captured task for the missing one: T-2171 makes 'provisional', T-2197 writes 'confirmed'
## Plan gaps
- failed first: step 1 red tests: select's provisional line; check names an unmarked lineage section
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
