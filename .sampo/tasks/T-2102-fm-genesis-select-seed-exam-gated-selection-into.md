---
id: T-2102
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T05:35:24Z
updated: 2026-10-30T06:03:41Z
base: b550eb066f922ea852ec50ab51fe4dae358237f3
base_tree: 56bd49d52fc44a2fe536b566492dc40349005c0d
plan0_at: 2026-10-30T05:35:59Z
plan0_scope: []
verified: strong
---
# fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the…
## Raw request
> FEATURE: fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the next Seed
> CONTEXT: Genesis gen 1 Mission 2 brief 4 (research/genesis/gen-1/mission-genesis.md item 4). fm exam grade adds closed (train/holdout scenario ids fully closed, split from the run itself) and gen to each exam.jsonl line. select N compares gen N's train closed set with gen N-1's on the same run, per gen-0 §3.6 verbatim: it stays only if it closed more, otherwise the parent text comes back (a tie loses whatever the cost; cost is reported). A scenario the parent closed and the child reopens fails selection (ratchet); a one-scenario margin on a single line asks for a rerun and writes nothing. Each verdict is a lineage.md '## gen-N' section naming the seed base, plus an fm decide. seed N writes gen-N/seed.md from the newest kept ancestor's seed, a Missions table ranked by open coverage cells, every empty cell and not-yet item, the critiques' 'What the next Seed should change', exam scores and lineage. Held-out scenarios never feed selection.
> MUST: select reads the split recorded on the exam line, never re-drawn
> MUST: seed N output passes step's seed-row rules (<= 8 rows) and step reads it
> DONE-WHEN: a child that closes fewer loses; a tie loses; a reopened scenario fails; a one-scenario margin asks a rerun; seed N lists every not-yet item and empty cell
## Interpretation
Selection and the next Seed become fm verbs, so from gen 2 the feature writes the Seed (gen-0 #13) and keeps or reverts a generation on the exam's train split alone.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam grade lines carry closed {train, holdout} ids and gen — verify with `plugin/tests/run.py test_genesis`
- [x] select N: fewer, tie, reopened revert; +2 keeps; +1 on one line asks rerun and writes nothing; no parent is the baseline; lineage section + decision written — verify with `plugin/tests/run.py test_genesis`
- [x] seed N writes gen-N/seed.md from the kept ancestor with <= 8 parsed rows, every empty cell and not-yet item, critique changes; step reads it and points at select/seed — verify with `plugin/tests/run.py test_genesis`
- [x] MASTER.md and CHANGELOG name select/seed — verify with `grep -c 'genesis.*select' MASTER.md CHANGELOG.md`
## Non-goals
## Approach (options → choice → why)
Complete version: grade lines carry closed ids per split and gen; select N compares train closed sets on one run (ratchet, rerun on a one-line one-scenario margin, tie reverts per gen-0 §3.6), writes lineage + fm decide, names the seed base; seed N assembles gen-N/seed.md (kept ancestor's carried sections, ranked Missions table <= 8 rows, every empty cell and not-yet item, critique changes, scores, lineage); step points at both verbs. Approaches: (A) deterministic assembly in fmgenesis, chosen: testable, resumable, no model call; (B) a child claude writes the seed from the same material with A as fallback: nondeterministic and still needs A to hold the row/listing rules; (C) select only, the session writes the seed by hand: fails #13 'from gen 2 on the feature writes the Seed'. Selection reads closed ids recorded on the line (the run's own split) instead of re-loading the run, so an archived run still selects.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests for grade closed/gen, select verdicts, seed listing
2. [x] grade closed/gen + select N + lineage/decide
3. [x] seed N + step wiring + CLI
4. [x] docs: MASTER, CHANGELOG
5. [x] gates, review, finish, ship
## Resume here
<!-- auto -->
- 2026-10-30T05:52:16Z step 5/5: gates, review, finish, ship
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/templates/genesis.md, plugin/tests/test_exam.py, plugin/tests/test_genesis.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/mission-genesis.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/brief5.txt, plugin/tests/test_genesis.py, plugin/tests/test_exam.py, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py
## Docs impact
MASTER.md,CHANGELOG.md
## Verification evidence
- (step 1) `plugin/tests/run.py test_genesis` → red as expected (exit 1) · Ran 43 tests in 3.7s (7 classes, 16 at a time; slowest: GenesisLive 3s, GenesisCheck 2s, GenesisStep 2s) / FAILED (2 classes) [ran] [tree f3a1a937f089] (2026-10-30T05:42:12Z)
- (ac 1) `plugin/tests/run.py test_genesis 2>&1 | grep -B2 -A12 "exited 1" | grep -v "^ File" | tail -15` → ✗ exit 1 · Ran 43 tests in 3.7s (7 classes, 16 at a time; slowest: GenesisLive 3s, GenesisCheck 3s, GenesisStep 2s) / FAILED (1 classes) [ran] [tree 8f2dffe6568c] (2026-10-30T05:44:50Z)
- (ac 2) `plugin/tests/run.py test_genesis 2>&1 | grep -B2 -A12 "exited 1" | grep -v "^ File" | tail -15` → ✗ exit 1 · Ran 43 tests in 3.7s (7 classes, 16 at a time; slowest: GenesisLive 3s, GenesisCheck 3s, GenesisStep 2s) / FAILED (1 classes) [ran] [tree 8f2dffe6568c] (2026-10-30T05:44:50Z)
- (ac 3) `plugin/tests/run.py test_genesis 2>&1 | grep -B2 -A12 "exited 1" | grep -v "^ File" | tail -15` → ✗ exit 1 · Ran 43 tests in 3.7s (7 classes, 16 at a time; slowest: GenesisLive 3s, GenesisCheck 3s, GenesisStep 2s) / FAILED (1 classes) [ran] [tree 8f2dffe6568c] (2026-10-30T05:44:50Z)
- (step 2) `plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 60 tests in 18.4s (16 classes, 16 at a time; slowest: ExamGen 18s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 39271c8995ca] (2026-10-30T05:45:51Z)
- (step 3) `plugin/tests/run.py test_genesis` → exit 0 · Ran 43 tests in 3.7s (7 classes, 16 at a time; slowest: GenesisLive 3s, GenesisCheck 2s, GenesisStep 2s) / OK [ran] [tree 39271c8995ca] (2026-10-30T05:45:55Z)
- (step 4) `grep -c 'genesis.*select' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:2 [ran] [tree 98d362c14226] (2026-10-30T05:46:13Z)
- (audit intent) `reviewer pass on gen-0 §3.6 vs select: train ids only, tie reverts, ratchet, rerun on one-scenario single-line margin` → holds; bar = gen N-1 even when reverted, fm decide recorded [tree dc64f6cb0d63] (2026-10-30T05:54:48Z)
- (audit adversary) `critique ask bodies with | rows; select 0; concurrent select/seed` → fixed test-first: | lines stripped, n<1 refused, genesis-lineage lock [tree dc64f6cb0d63] (2026-10-30T05:54:48Z)
- (audit edge) `regrade after the next seed lands; gen-0 base; oracle agent seed` → fixed test-first: gen stamped at run, gen-0 base carries nothing, seed --agent reaches Exam [tree dc64f6cb0d63] (2026-10-30T05:54:48Z)
- (audit operator) `fm genesis select/seed output lines, exit codes, lineage.md readable` → ok: one verdict line + seed base; ValueError → usage exit [tree dc64f6cb0d63] (2026-10-30T05:54:48Z)
- (audit maintainer) `select/_select + seed/_seed lock wrappers, MADE/ASKS constants, MASTER + CHANGELOG` → ok: docs match the code [tree dc64f6cb0d63] (2026-10-30T05:54:48Z)
- (step 5) `plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 61 tests in 18.6s (16 classes, 16 at a time; slowest: ExamGen 18s, ExamRust 12s, ExamC 11s) / OK [ran] [tree dc64f6cb0d63] (2026-10-30T05:58:50Z)
- (ac 1) `plugin/tests/run.py test_genesis` → exit 0 · Ran 44 tests in 3.8s (7 classes, 16 at a time; slowest: GenesisLive 4s, GenesisCheck 3s, GenesisStep 2s) / OK [ran] [tree dc64f6cb0d63] (2026-10-30T05:59:00Z)
- (ac 2) `plugin/tests/run.py test_genesis` → exit 0 · Ran 44 tests in 3.8s (7 classes, 16 at a time; slowest: GenesisLive 4s, GenesisCheck 3s, GenesisStep 2s) / OK [ran] [tree dc64f6cb0d63] (2026-10-30T05:59:00Z)
- (ac 3) `plugin/tests/run.py test_genesis` → exit 0 · Ran 44 tests in 3.8s (7 classes, 16 at a time; slowest: GenesisLive 4s, GenesisCheck 3s, GenesisStep 2s) / OK [ran] [tree dc64f6cb0d63] (2026-10-30T05:59:00Z)
- (ac 4) `grep -c 'genesis.*select' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:2 [ran] [tree dc64f6cb0d63] (2026-10-30T05:59:00Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 6 findings fixed test-first, bar choice recorded via fm decide; full fm check green (4342 tests)` → regrade after the next seed keeps the run's gen; gen-0 base carries nothing [tree dc64f6cb0d63] (2026-10-30T05:59:00Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 6 findings fixed test-first, bar choice recorded via fm decide; full fm check green (4342 tests)` → critique | rows can't join the Missions table; select 0 refused; select/seed locked [tree dc64f6cb0d63] (2026-10-30T05:59:00Z)
## Log
- 2026-10-30T05:35:24Z created
- 2026-10-30T05:35:58Z planned: it has criteria and steps
- 2026-10-30T05:35:59Z focused
- 2026-10-30T05:59:27Z done
- 2026-10-30T05:59:28Z committed 6433fd26 (8 files)
- 2026-10-30T06:01:29Z guard authorization added: publish
- 2026-10-30T06:03:41Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: Genesis select: a tie on train scenarios closed reverts to the parent whatever the cost (gen-0 §3.6 verbatim: stays only if it closed more); cost pe…
- T-2099 [FEATURE M, done, 5 steps] fm genesis draft/spec — gen-0 from a line or nothing; per-project spec with a held-out… — lesson: cover() tag words counted as shared w…
- T-2077 [RESEARCH L, planned, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- similar finished tasks took 3–5 steps
## Lessons
- c.lock is not reentrant: a lock around code that calls put needs its own dir, not p.dir
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
- plugin/templates/genesis.md
