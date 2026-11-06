---
id: T-2104
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T06:03:48Z
updated: 2026-10-30T06:31:58Z
base: 6433fd26ea4bff06334602ed033d772541ef47d8
base_tree: dc64f6cb0d63280d3565b391493d31f8d782207c
plan0_at: 2026-10-30T06:04:15Z
plan0_scope: []
verified: strong
---
# fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in…
## Raw request
> FEATURE: fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in one command
> CONTEXT: Genesis gen 1 Mission 2 brief 5 (research/genesis/gen-1/mission-genesis.md item 5; gen-0 §3.7 and §7). drift N: every unfenced MUST:/NEVER: line in gen-N/seed.md and its mission files must be one of gen-0's verbatim (an added or reworded constraint is drift: a generation never rewrites the user's MUSTs; fenced intake blocks are briefs, whose own MUSTs are task constraints), each of those files must quote gen-0's constraints or point to gen-0, and one tool-less cold read (fmideas.run_child) compares the seed with gen-0's goal, MUSTs, NEVERs and DONE-WHEN and lists drifted lines; a named line counts only if it is in the seed. It writes gen-N/drift.md with a Verdict line (clean, drifted, or unread when the cold read can't run); anything but clean exits 1 and keeps fm genesis step on drift ("undo the lines drift.md names, then rerun"). sweep N: §7 in one command — fm genesis check, the generation's mission tasks closed or blocked with a reason, no planned/active/verifying task, no blocked task without a reason, no lane left unmerged, fm docs with no findings, fm doctor with no failures, a full fm check pass recorded on this exact tree, and an exam line graded for gen N — written to gen-N/sweep.md with a Verdict line (clean or red), exit 1 on red; step stays on sweep until it is clean.
> MUST: the cold read's text is untrusted data (c.plain) and never edits the tower by itself
> MUST: drift and sweep write only through fm genesis put's path rules
> MUST: sweep never runs the full suite itself; it reads the recorded pass for this tree
> DONE-WHEN: a seed that neither quotes nor points to gen-0 fails drift; a reworded MUST fails drift; an added NEVER fails drift; a clean seed passes; an unread cold read fails; a red sweep check exits 1 and step stays on it; a clean sweep moves step to the next seed
## Interpretation
Brief 5 of Mission 2: two new fm genesis verbs that close the tower's drift (§3.7) and sweep (§7) stages, so step can only move past them on a written clean verdict.
## Assumptions (confidence)
## Acceptance criteria
- [x] drift N: a seed that neither quotes nor points to gen-0, a reworded MUST, an added NEVER fail (exit 1, step stays on drift); a clean seed passes; a cold-read line counts only if the seed holds it; no read is verdict unread — verify with plugin/tests/run.py test_genesis
- [x] sweep N: each red §7 row (genesis check, tasks, doctor, gates, exam) keeps step on sweep and exits 1; a clean sweep moves step to seed; sweep reads the recorded gate pass, never runs the suite — verify with plugin/tests/run.py test_genesis
- [x] MASTER.md and CHANGELOG name drift/sweep — verify with grep -c 'genesis drift' MASTER.md CHANGELOG.md
## Non-goals
## Approach (options → choice → why)
Complete version: drift checks every unfenced MUST:/NEVER: line in the seed and mission files against gen-0's verbatim set, requires each file to quote gen-0 or point to it, and adds one tool-less cold read whose DRIFT: lines count only when the seed holds them (untrusted text through c.plain); sweep collects §7 into rows (genesis check, mission tasks, open tasks, unreasoned blocks, lanes, docs, doctor, the recorded gate pass on this tree, an exam line for gen N); both write through put with a Verdict line, and step stays on a stage until it reads Verdict: clean. Approaches: (A) deterministic checks plus one cold read, chosen: the verbatim rule catches any rewrite cheaply and the read catches meaning drift; (B) fm second only: costlier, can't be tested offline and misses exact rewording; (C) a hash seal of gen-0's constraints: that is brief 8's charter seal, kept there; (D) sweep reruns the full gate: violates 'never two suites' and doubles cost, so it reads the cached pass.
## Risks and rollback
A false drift on a seed that legitimately quotes gen-0 with different spacing: lines are whitespace-normalized before comparing. Rollback: git revert of the task commit; tower files are git-ignored state.
## Execution prompt
## Steps
1. [x] red tests for drift and sweep, step fixtures to Verdict lines
2. [x] drift N: constraint lines, pointer, cold read, drift.md
3. [x] sweep N: §7 rows into sweep.md; step stays until Verdict clean; CLI
4. [x] docs: MASTER, CHANGELOG, site
5. [x] gates, review, finish, ship
## Resume here
<!-- auto -->
- 2026-10-30T06:20:08Z step 5/5: gates, review, finish, ship
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py
- touched since last checkpoint: plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md
- failures met: bash: eval: line 0: unexpected eof while looking for matching ``'
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `plugin/tests/run.py test_genesis` → exit 0 · Ran 49 tests in 3.7s (9 classes, 16 at a time; slowest: GenesisLive 3s, GenesisSweep 3s, GenesisCheck 3s) / OK [ran] [tree 7bc7a6023c44] (2026-10-30T06:09:46Z)
- (step 2) `plugin/tests/run.py test_genesis.GenesisDrift` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: GenesisDrift 1s) / OK [ran] [tree 7bc7a6023c44] (2026-10-30T06:09:51Z)
- (step 3) `plugin/tests/run.py test_genesis.GenesisSweep test_genesis.GenesisStep` → exit 0 · Ran 11 tests in 2.9s (2 classes, 16 at a time; slowest: GenesisSweep 3s, GenesisStep 2s) / OK [ran] [tree 7bc7a6023c44] (2026-10-30T06:09:54Z)
- (step 4) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree 6768be6feb8b] (2026-10-30T06:10:37Z)
- (audit intent) `fm-reviewer pass over the diff` → cold read failed open on unparseable replies: fixed, fails closed (test_a_cold_read_fails_closed_…) [tree 90b5b1e86e7e] (2026-10-30T06:17:51Z)
- (audit edge) `fm-reviewer pass` → archived mission briefs read missing: fixed with include_archive; sweep guard for n<1/no seed; docs/doctor rows readable (2 new tests) [tree 90b5b1e86e7e] (2026-10-30T06:17:52Z)
- (audit adversary) `fm-reviewer pass` → seed could close its <seed> fence: defanged; stale pass during a 180 s read: drift.md dated at start. Forged put of drift.md is the same session's own write, not a boundary (decided) [tree 90b5b1e86e7e] (2026-10-30T06:17:52Z)
- (audit maintainer) `fm-reviewer pass` → lanes and mission-tasks rows now tested (lane ahead of HEAD, queued lane, archived brief) [tree 90b5b1e86e7e] (2026-10-30T06:17:52Z)
- (step 5) `plugin/tests/run.py test_genesis test_doctor.Checks.test_self_docs_match_the_code` → exit 0 · Ran 53 tests in 3.8s (10 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 3s, GenesisCheck 3s) / OK [ran] [tree 231a848c64b2] (2026-10-30T06:22:55Z)
- (ac 1) `plugin/tests/run.py test_genesis` → exit 0 · Ran 52 tests in 3.8s (9 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 3s, GenesisCheck 3s) / OK [ran] [tree 231a848c64b2] (2026-10-30T06:23:20Z)
- (ac 2) `plugin/tests/run.py test_genesis` → exit 0 · Ran 52 tests in 3.8s (9 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 3s, GenesisCheck 3s) / OK [ran] [tree 231a848c64b2] (2026-10-30T06:23:20Z)
- (ac 3) `plugin/tests/run.py test_genesis` → exit 0 · Ran 52 tests in 3.8s (9 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 3s, GenesisCheck 3s) / OK [ran] [tree 231a848c64b2] (2026-10-30T06:23:20Z)
- (audit intent) `fm-reviewer pass; 7 findings fixed test-first` → drift checks gen-0 MUST/NEVER verbatim plus a fail-closed cold read; sweep is gen-0 §7 in one command [tree 231a848c64b2] (2026-10-30T06:23:20Z)
- (audit edge) `fm-reviewer pass; 7 findings fixed test-first` → archived briefs counted, sweep guard, fail-closed cold read [tree 231a848c64b2] (2026-10-30T06:23:20Z)
## Log
- 2026-10-30T06:03:48Z created
- 2026-10-30T06:04:10Z planned: it has criteria and steps
- 2026-10-30T06:04:10Z set status=planned
- 2026-10-30T06:04:15Z focused
- 2026-10-30T06:23:41Z done
- 2026-10-30T06:23:43Z committed c6f0c9e1 (5 files)
- 2026-10-30T06:24:13Z guard authorization added: publish
- 2026-10-30T06:31:58Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2077 [RESEARCH L, planned, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- decision 2026-10-30: [cites: user: read SEED_PROMPT.md] Genesis setup: autonomy full, drive on, loop on, contract off, lane max 6, mandate until 2026-11-13; T-2077 is th…
- similar finished tasks took 3–5 steps
## Lessons
- Never write a literal triple backtick in MASTER.md prose: fm doctor's self-docs strips fenced spans across lines and every fm verb after it goes missing
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
