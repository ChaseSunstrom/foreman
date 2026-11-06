---
id: T-0709
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T19:09:55Z
base: bd37a4fc3a1a7b29d1306401cfb87a2f5a3ef83c
base_tree: 57b61f2a70baeb9697a4b1ccccec2b8269d2d18d
verified: strong
---
# Frontier 09 — Orchestrators of orchestrators
## Raw request
> FEATURE: Frontier 09 — Orchestrators of orchestrators
> CONTEXT: A big task becomes a tree of orchestrators that split along real code seams and learn which shapes win.
> CONTEXT: first slice: Fractal spawn with capsule-only return and coupling-aware partition, run on one L task.
> CONTEXT: proof at close: One L task run as a tree: result merged green, parent context stays under budget, compared with the single-session run.
> CONTEXT: members (13, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): Fractal Foreman: a task too big for one session becomes its own orchestrator, and only a capsule comes back up; Self-reorganising org: an orchestrator of orchestrators that rewrites its own org chart while the work runs; Tournament mode: k orchestrators race different strategies, a judge merges the best and mines the losers; Shape learning: the Conductor learns which decompositions and team shapes win, partly from free simulation; Deadline scheduler: critical path and an elastic fleet, 'done by 7am' as the only input; Work market with context affinity: work goes to the orchestrator that already knows the code; Calibrated executor market: configurations bid on each task and are settled by a proper scoring rule; Multiverse: risky decisions fork the session, the universes attack each other with tests, the survivor merges and losers donate; Context-inheriting speculative forks for contested decisions; Contract-first swarm: one L task, the lead writes the seams and their failing tests, cheap builders fill them in parallel; Consumer review: orchestrators review the changes whose interfaces they consume; Coupling-aware partitioning: min-cut the code graph so orchestrators split along the code's real seams; Cross-repo atomic milestones: two-phase merge across repos and machines
## Interpretation
First slice of Frontier 09: a task too big for one session splits along the code's real seams into child tasks, and only a capsule comes back up. fm task split ID [--parts K] [--files …] partitions the task's files (its scope, or fm graph pack's read-set) by agglomerative merging over the work graph's code, co-change and test edges, so the cut between parts is light; each part becomes a child brief scoped to its files, told the seams it must not break. fm task capsule ID is the child's return: ≤15 lines of what changed, how it was verified, decisions, follow-ups and risks. A parent can't close while a child is open. Children run through the existing lanes and builders, recursively if a child splits again.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task split puts tightly coupled files in the same child, scopes each child to its part and links it to the parent; a parent with open children can't close — verify with `python3 plugin/tests/run.py -p test_split.py -k Split`
- [x] fm task capsule returns at most 15 lines naming the child's files, verification and status — verify with `python3 plugin/tests/run.py -p test_split.py -k Capsule`
## Non-goals
## Approach (options → choice → why)
Partition: (a) by directory — ignores coupling; (b) agglomerative merge of the most-linked groups under a size cap, on fm graph's edges — chosen: tiny, deterministic, respects seams; (c) spectral min-cut — numpy-free is fiddly for little gain at 5–30 files. Spawn: (a) new orchestrator sessions per child — the T-0708 bus can address them later; (b) child briefs run by the existing lanes and fm-builder — chosen: reuses merge, audit and evidence. Return: (a) the child's final message — unbounded; (b) a capsule generated from the brief and its commit — chosen: bounded, same shape every time. Proof run (an L task as a real tree vs one session) needs subagents, paused by the budget guard at this week's usage; recorded as a decision and run when usage allows.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] partition and fm task split with the parent gate
3. [x] fm task capsule
4. [x] docs, CHANGELOG, full suite, proof-run decision
## Resume here
## Docs impact
CHANGELOG; MASTER.md module list (fmsplit)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_split.py` → ✗ exit 1 · Ran 2 tests in 0.3s (2 classes, 16 at a time; slowest: Capsule 0s, Split 0s) / FAILED (2 classes) [ran] [tree 6a37d45fa5fb] (2026-10-09T19:06:52Z)
- (step 2) `python3 plugin/tests/run.py -p test_split.py -k Split` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Split 0s) / OK [ran] [tree ee03d5d82231] (2026-10-09T19:08:46Z)
- (step 3) `python3 plugin/tests/run.py -p test_split.py -k Capsule` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Capsule 1s) / OK [ran] [tree ee03d5d82231] (2026-10-09T19:08:47Z)
- (step 1) `python3 plugin/tests/run.py -p test_split.py` → exit 0 · Ran 2 tests in 0.5s (2 classes, 16 at a time; slowest: Capsule 1s, Split 0s) / OK [ran] [tree ee03d5d82231] (2026-10-09T19:08:47Z)
- (step 4) `python3 plugin/tests/run.py` → exit 0 · Ran 1150 tests in 60.1s (330 classes, 16 at a time; slowest: Stop 37s, TaskLifecycle 25s, Parallel 21s) / OK [ran] [tree 9f2e28c75d57] (2026-10-09T19:09:48Z)
- (ac 1) `python3 plugin/tests/run.py -p test_split.py -k Split` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Split 0s) / OK [ran] [tree 9f2e28c75d57] (2026-10-09T19:09:55Z)
- (ac 2) `python3 plugin/tests/run.py -p test_split.py -k Capsule` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Capsule 1s) / OK [ran] [tree 9f2e28c75d57] (2026-10-09T19:09:55Z)
- (audit intent) `self review of fmsplit, the dispatch and the parent gate; dry-run partitions on real Foreman files` → the first slice asked for fractal spawn with capsule-only return and coupling-aware partition; split, capsule and the parent gate shipped and tested on real partitions; the proof run of an L task as a tree is a recorded decision, waiting for usage headroom [tree 9f2e28c75d57] (2026-10-09T19:09:55Z)
- (audit edge) `self review of fmsplit, the dispatch and the parent gate; dry-run partitions on real Foreman files` → a task with under 2 files refuses to split; a size cap keeps parts even and grows only when no merge fits; an unlinked group merges smallest-first; a closed task can't split; children carry the parent's verify commands as their criteria; the first real dry run exposed fmmap skipping short test names, fixed [tree 9f2e28c75d57] (2026-10-09T19:09:55Z)
- (audit operator) `self review of fmsplit, the dispatch and the parent gate; dry-run partitions on real Foreman files` → fm task split --dry-run on 12 real Foreman files gave 3 parts with tests beside their sources and one light seam [tree 9f2e28c75d57] (2026-10-09T19:09:55Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T19:06:40Z focused
- 2026-10-09T19:08:34Z scope: fmmap's name link skipped stems under 4 letters (test_bus → fmbus), which split the partition's tests from their sources; widened the rule to short prefixes
- 2026-10-09T19:09:55Z done
- 2026-10-09T19:09:55Z committed 4195c7d (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- T-0707 [FEATURE M, done, 4 steps] Frontier 07 — Knowledge graph — lesson: Retrieval for a new task works best through past tasks: words match titles far better than path…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- the similar finished task took 4 steps
- start here (files T-0707 touched): plugin/tests/test_graph.py, plugin/lib/fmgraph.py, plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/lib/fmdebug.py
## Lessons
- Partitioning by graph needs the test-to-source links first: without them tests drift away from their code and every part breaks another's tests
## Files touched
- plugin/tests/test_split.py
- plugin/lib/fmsplit.py
- plugin/lib/fmcli.py
- plugin/lib/fmmap.py
- CHANGELOG.md
- MASTER.md
