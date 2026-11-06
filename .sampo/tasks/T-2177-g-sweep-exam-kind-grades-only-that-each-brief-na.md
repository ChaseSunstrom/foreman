---
id: T-2177
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T15:35:59Z
updated: 2026-10-31T07:55:53Z
builder_model: sonnet
base: 2cbec9f5561df77a780f9138cd12581ccbe373ca
base_tree: e1ef079446e836a47446452f7518e5688a4a064b
plan0_at: 2026-10-31T07:48:49Z
plan0_scope: []
verified: strong
---
# G-sweep exam kind grades only that each brief names a tier (a format check): grade…
## Raw request
> G-sweep exam kind grades only that each brief names a tier (a format check): grade substance instead (the drafted briefs cover the planted gaps, tier earned by the gap) before the end-of-run exam (T-2166 cold read of critique-genesis.md)
## Interpretation
#13's G-sweep kind ('super improve this') is graded like the others on one planted defect plus a shape check (each §2 capability maps to an exam kind), so a draft that names one gap and maps kinds passes: the sweep's point, finding every gap unasked, isn't tested (T-2166's cold read of critique-genesis.md).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis exam's sweep scenarios plant 3 distinct defects and a draft closes one only when its §2 covers all 3 with matching exam kinds (each miss named); line and none still plant and grade one — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) a sweep scenario plants 3 distinct defects (from the kinds the generator already plants, different files), and _misses for sweep requires a §2 capability with a matching exam kind for each, naming the ones missed; line and none keep one defect. 2) grade tiers per gap — rejected: a tier is the writer's judgment, not checkable against a key. 3) a model judge — rejected: tokens, and the key already says what was planted. Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: a draft covering 1 of 3 sweep defects stays open with 2 named misses; covering all 3 closes; line and none unchanged
2. [x] multi-defect planting for sweep and the grader
3. [x] docs lines in the report
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -15` → exit 0 · Ran 156 tests in 11.9s (17 classes, 16 at a time; slowest: GenesisRead 12s, GenesisCheck 9s, GenesisDrift 8s) / OK [ran] [tree a3c92d2c44af] (2026-10-31T07:49:40Z)
- (step 1) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -15` → exit 0 · Ran 156 tests in 11.9s (17 classes, 16 at a time; slowest: GenesisRead 12s, GenesisCheck 9s, GenesisDrift 8s) / OK [ran] [tree a3c92d2c44af] (2026-10-31T07:49:40Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 156 tests in 12.6s (17 classes, 16 at a time; slowest: GenesisRead 12s, GenesisCheck 11s, GenesisDrift 10s) / OK [ran] [tree a3c92d2c44af] (2026-10-31T07:49:57Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_genesis && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [23.07s] [ran] [tree a3c92d2c44af] (2026-10-31T07:50:36Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis` → ✗ exit 1 · Ran 156 tests in 54.900s / FAILED (errors=1) (start tree + this task's tests) [ran] [tree a3c92d2c44af] (2026-10-31T07:54:44Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis` → exit 0 · Ran 156 tests in 46.048s / OK [ran] [tree a3c92d2c44af] (2026-10-31T07:54:44Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 239 tests in 8.5s (39 classes, 16 at a time; slowest: Fences 8s, GenesisRead 8s, GenesisCheck 7s) / OK [ran] [tree a3c92d2c44af] (2026-10-31T07:55:02Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 239 tests in 8.5s (39 classes, 16 at a time; slowest: Fences 8s, GenesisRead 8s, GenesisCheck 7s) / OK [ran] [tree a3c92d2c44af] (2026-10-31T07:55:11Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 239 tests in 8.5s (39 classes, 16 at a time; slowest: Fences 8s, GenesisRead 8s, GenesisCheck 7s) / OK [ran] [tree a3c92d2c44af] (2026-10-31T07:55:19Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 156 tests in 7.9s (17 classes, 16 at a time; slowest: GenesisRead 8s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree d46d0c6532cc] (2026-10-31T07:55:28Z)
- (audit intent) `self-review of the diff: sweep repos rendered with fmexam's rank kind (three planted defects), each graded; ids and line/none unchanged` → the sweep kind now tests finding every planted gap, not a format (test_genesis red-to-green) [tree d46d0c6532cc] (2026-10-31T07:55:28Z)
- (audit edge) `self-review of the diff: sweep repos rendered with fmexam's rank kind (three planted defects), each graded; ids and line/none unchanged` → covering one of three leaves two named misses; sweep scores before this don't compare with new ones (noted) [tree d46d0c6532cc] (2026-10-31T07:55:28Z)
## Log
- 2026-10-30T15:35:59Z created
- 2026-10-31T07:48:33Z set tier=M
- 2026-10-31T07:48:33Z planned: it has criteria and steps
- 2026-10-31T07:48:34Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2177.builder.md
- 2026-10-31T07:48:48Z focused
- 2026-10-31T07:53:01Z merged worktree-agent-a09f0afe0ee5d698a (2 file(s))
- 2026-10-31T07:53:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a09f0afe0ee5d698a
- 2026-10-31T07:53:02Z focused
- 2026-10-31T07:55:20Z scope: plugin/lib/fmgenesis.py (_defects, _misses, _oracle, exam), plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md
- 2026-10-31T07:55:51Z done
- 2026-10-31T07:55:53Z committed 57d32d93 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
## Lessons
- A 'super improve' exam with one planted gap measures one finding; plant several so the score reads breadth
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
