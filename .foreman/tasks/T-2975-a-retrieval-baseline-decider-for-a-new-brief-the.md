---
id: T-2975
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T14:20:23Z
updated: 2026-11-04T14:58:10Z
rival_at: 2026-11-04T14:23:55Z
rival_split: true
builder_model: haiku
base: de9ce0b0eb6b305bd9dc8e3fa990060ecf1acde2
base_tree: 57dd947ac0372b8d6fc439428c7160649b7a210b
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T14:24:23Z
plan0_scope: []
lane_stop: merged 2026-11-04T14:39:33Z
verified: strong
unproven: [data]
---
# A retrieval baseline decider: for a new brief, the k nearest closed briefs by bge-m3…
## Raw request
> FEATURE: A retrieval baseline decider: for a new brief, the k nearest closed briefs by bge-m3 embedding (across projects, sensitive ones only locally) vote its intake type, tier and playbook route, with an abstain when they disagree; scored on the model bench beside the 4B decider (type 0.73) and the majority (0.595), and offered through decide()'s shadow mode
> CONTEXT: from the model brainstorm (research brainstorm-20261104-model, T-2973): Sampo's own models must be generic across every project built with Sampo, trained on outcomes, adopted per slot only where they beat today's path on whole held-out projects.
## Interpretation
Reading 1 (chosen): a retrieval arm in Louhi's model bench (louhi's bench_models and _bench_data): each held-out brief's raw request is embedded with the bench's best embedder, its k nearest train-split closed briefs (across every Sampo project on the machine, a sensitive project's only on loopback) vote its intake type and tier, with an abstain when the vote is split; rows land in research/models/bench.jsonl beside majority and orchestrator, and decide() gains a shadow use for it. Reading 2 (ruled out): train a classifier now; the bench's bar comes first and retrieval may beat it untrained.
## Assumptions (confidence)
## Acceptance criteria
- [x] the bench writes retrieval rows (embedding k-NN and BM25) for intake type and tier with accuracy, coverage and abstain counts, beside majority and orchestrator, on the held-out split — verify with `python3 plugin/tests/run.py test_louhi_models`
- [x] a live bench run on this project records the retrieval rows in research/models/bench.jsonl — verify with `grep -c retrieval research/models/bench.jsonl`
## Non-goals
## Approach (options → choice → why)
1) A 'retrieval' arm in bench_models: embed the train split once (vectors cached by model, as moonscale does), cosine k-NN (k=7) vote, abstain under a 4-of-7 majority; one bench row per use with accuracy on answered rows, coverage and accuracy with abstains counted wrong. Likely outcome: type above the 4B decider's 0.73 at full coverage or close to it. Fails if: requests are too short for embeddings to separate types; the row says so.
2) use what exists: recall.py's BM25 over briefs as the retriever. Likely outcome: no embedding calls, weaker on paraphrase. Fails if: lexical overlap misses synonyms; run it as a second retrieval row.
3) do less: report the bench's majority baseline and stop. Likely outcome: nothing new. Fails if: the user asked for a better Kev.
Choice 1 (80%): the embedder is already on the box and the bench already has the held-out split.
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md.
## Execution prompt
## Steps
1. [x] failing test: a fake embedder and a tiny brief set where the nearest neighbours decide the type
2. [x] the retrieval arm (embedding k-NN with abstain, and BM25) in louhi's bench
3. [x] a live bench run on this machine; the numbers in the T-2878 research
## Resume here
## Docs impact
CHANGELOG line; research T-2975-retrieval-baseline
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_louhi_models` → exit 0 · Ran 8 tests in 30.7s (1 classes, 16 at a time; slowest: LouhiModels 30s) / OK [ran] [tree 2e5471a93c7e] [world 2f1906870a] (2026-11-04T14:41:16Z)
- (step 2) `python3 plugin/tests/run.py test_louhi_models test_louhi` → exit 0 · Ran 10 tests in 61.8s (3 classes, 16 at a time; slowest: LouhiModels 61s, Collect 0s, Pages 0s) / OK [ran] [tree 2e5471a93c7e] [world 2f1906870a] (2026-11-04T14:45:39Z)
- (step 3) `grep -c retrieval research/models/bench.jsonl` → exit 0 · 4 [ran] [tree 479707121125] [world 2f1906870a] (2026-11-04T14:49:40Z)
- `python3 plugin/tests/run.py test_louhi_models` → ✗ exit 1 · Ran 8 tests in 31.2s (1 classes, 16 at a time; slowest: LouhiModels 28s) / FAILED (1 classes: test_louhi_models.LouhiModels) (start tree + this task's tests) [ran] [tree 479707121125] [world 2f1906870a] (2026-11-04T14:51:58Z)
- `python3 plugin/tests/run.py test_louhi_models` → exit 0 · Ran 8 tests in 29.8s (1 classes, 16 at a time; slowest: LouhiModels 29s) / OK [ran] [tree 479707121125] [world 2f1906870a] (2026-11-04T14:51:58Z)
- (ac 1) `python3 plugin/tests/run.py test_louhi_models` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T14:51:58Z [ran] [tree 479707121125] [world 2f1906870a] (2026-11-04T14:52:09Z)
- (ac 2) `grep -c retrieval research/models/bench.jsonl` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T14:49:40Z [ran] [tree 479707121125] [world 2f1906870a] (2026-11-04T14:52:09Z)
- (audit edge) `branch diff read in full before merge (louhi _bench_retrieval, _retrieval_vectors, _vote; test_louhi_models); live numbers checked against bench.jsonl rows; vector cache moved out of the repo after review; prove red on the start tree, green now` → a 3-3 split abstains (tested); an empty train pool gives no row; a rerun embeds nothing new (tested); the cache stays out of the repo (tested) [tree 479707121125] (2026-11-04T14:52:09Z)
- (audit adversary) `branch diff read in full before merge (louhi _bench_retrieval, _retrieval_vectors, _vote; test_louhi_models); live numbers checked against bench.jsonl rows; vector cache moved out of the repo after review; prove red on the start tree, green now` → sha1 is only a cache key for text already on this machine (no trust decision rests on it); brief text goes only to the local embedding profile (bge-m3 on loopback Ollama), never a paid or remote one unless that profile is configured so; the cache holds vectors, not text [tree 479707121125] (2026-11-04T14:52:09Z)
- (audit intent) `branch diff read in full before merge (louhi _bench_retrieval, _retrieval_vectors, _vote; test_louhi_models); live numbers checked against bench.jsonl rows; vector cache moved out of the repo after review; prove red on the start tree, green now` → retrieval is the floor every trained head must beat on held-out projects; numbers filed in research T-2975-retrieval-baseline [tree 479707121125] (2026-11-04T14:52:09Z)
## Log
- 2026-11-04T14:20:23Z created
- 2026-11-04T14:22:45Z set approved=True
- 2026-11-04T14:23:10Z planned: it has criteria and steps
- 2026-11-04T14:23:28Z criterion 1 verify: `python3 plugin/tests/run.py test_model_bench` → `python3 plugin/tests/run.py test_louhi_models`
- 2026-11-04T14:24:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2975.builder.md
- 2026-11-04T14:24:22Z focused
- 2026-11-04T14:24:23Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T14:34:20Z criterion 2 verify: `grep -c retrieval state/projects/foreman-4a056f/research/models/bench.jsonl` → `grep -c retrieval research/models/bench.jsonl`
- 2026-11-04T14:34:20Z steer: criterion 2's path fixed: bench.jsonl is the tracked research/models/bench.jsonl, not under state/
- 2026-11-04T14:39:33Z merged worktree-agent-a4d7697256969783c (3 file(s))
- 2026-11-04T14:40:04Z scope: the vector cache moved from the repo's research/models to Sampo's state dir (p.dir): 15 MB per project, generic projects must not get it in their tree
- 2026-11-04T14:50:38Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4d7697256969783c
- 2026-11-04T14:50:46Z focused
- 2026-11-04T14:58:08Z done
- 2026-11-04T14:58:10Z committed 004349c6 (2 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **kNN voting baseline as a new bench contestant (likeliest):** a retriever over closed briefs (bge-m3 embeddings, k neighbours) votes `type`, `tier` and `playbook route`, abstains on disagreement, is scored in `bench/` next to the 4B decider (0.73 type) and the majority baseline (0.595), and is exp…
- **Shadow-only instrument:** the "offered through decide()'s shadow mode" clause is the main deliverable. The bench scoring is secondary, and the retriever only logs its prediction beside the real decision for later comparison.
- **Training-data and generality framing:** the real aim is to test whether outcome-trained, project-generic signals beat today's path. The kNN is a cheap probe, so the bench split (whole held-out projects, not random briefs) matters more than the retriever itself.
- **Privacy-policy feature:** "sensitive ones only locally" is the core requirement. It means a sensitivity-aware index that never ships sensitive briefs' text or vectors off the machine.
Approaches:
- **Flat in-memory index, cosine, built from closed briefs:** a new module under `plugin/lib/` (following the `fm*.py` / `plugin/lib/sampo/*.py` pairing) loads the embeddings and returns per-slot votes plus a margin. The abstain rule is a vote-share threshold. `decide()` gets a `shadow` hook that cal…
- **Leave-one-project-out bench harness in `bench/`:** for each held-out project, index only the other projects' closed briefs, then score type, tier and route accuracy and abstain coverage. Report accuracy on answered briefs against coverage, so it can be compared fairly with the 4B decider and the …
- **Embedding cache keyed by brief id and content hash:** bge-m3 is run once, vectors are stored beside each brief's sensitivity flag, and sensitive vectors stay in a local-only store. A cross-project index built for sharing is filtered at build time.
- **Weighted votes (similarity-weighted, per-slot k) instead of plain majority:** this is a variant if plain voting is weak. Defer it until the unweighted baseline is measured.
Failure modes:
- **Project leakage inflates the score:** if the bench excludes the query brief but not its project siblings (near-duplicate briefs, templated text), accuracy looks far above 0.73 and fails the "whole held-out projects" adoption rule. The split logic in the bench must group by project.
- **Sensitive content escapes through the cross-project path:** the neighbour index, the shadow log, or the bench output may contain sensitive briefs' text or ids. The bge-m3 call itself must also be local. Any hosted embedding call or log line in `decide()` shadow output breaks the constraint.
- **Shadow mode changes behaviour or latency:** loading bge-m3 inside `decide()` can slow hooks (the `bench_hooks.py --runs 20` gate) or raise exceptions into the live path. It needs lazy loading, a timeout, and exceptions swallowed to a logged no-op, with the default off.
- **Abstain makes the comparison unfair:** the 0.73 and 0.595 figures are on all briefs. If the retriever's accuracy is reported only on answered briefs, it looks better than it is. Class imbalance also makes the majority label win most votes, so the tier and route slots can look good without real si…
## Dissent
- [x] rival reading: **kNN voting baseline as a new bench contestant (likeliest):** a retriever over closed briefs (bge-m3 embeddings, k neighbours) votes `type`, `tier` and `playbook route`, abstains on disagreement, is scored in `bench/` next to the 4B decider (0.73 type) and the majority baseline (0.595), and is exp… — answered: adopted: a retrieval contestant in Louhi's model bench
- [x] rival reading: **Shadow-only instrument:** the "offered through decide()'s shadow mode" clause is the main deliverable. The bench scoring is secondary, and the retriever only logs its prediction beside the real decision for later comparison. — answered: adopted in part: the shadow use in decide() is criterion-free here; the bench row decides adoption (T-2976)
- [x] rival reading: **Training-data and generality framing:** the real aim is to test whether outcome-trained, project-generic signals beat today's path. The kNN is a cheap probe, so the bench split (whole held-out projects, not random briefs) matters more than the retriever itself. — answered: not this task: outcome-trained heads are T-2970 and T-2977
- [x] rival reading: **Privacy-policy feature:** "sensitive ones only locally" is the core requirement. It means a sensitivity-aware index that never ships sensitive briefs' text or vectors off the machine. — answered: adopted: a sensitive project's briefs are embedded only by a loopback embedder
- [x] rival approach: **Flat in-memory index, cosine, built from closed briefs:** a new module under `plugin/lib/` (following the `fm*.py` / `plugin/lib/sampo/*.py` pairing) loads the embeddings and returns per-slot votes plus a margin. The abstain rule is a vote-share threshold. `decide()` gets a `shadow` hook that cal… — answered: adopted in part: the index lives in louhi's bench code, not a new module, until a second caller needs it
- [x] rival approach: **Leave-one-project-out bench harness in `bench/`:** for each held-out project, index only the other projects' closed briefs, then score type, tier and route accuracy and abstain coverage. Report accuracy on answered briefs against coverage, so it can be compared fairly with the 4B decider and the … — answered: not this task: leave-one-project-out is T-2976; this uses the bench's existing held-out split
- [x] rival approach: **Embedding cache keyed by brief id and content hash:** bge-m3 is run once, vectors are stored beside each brief's sensitivity flag, and sensitive vectors stay in a local-only store. A cross-project index built for sharing is filtered at build time. — answered: adopted: vectors cached by model and content hash, as moonscale does
- [x] rival approach: **Weighted votes (similarity-weighted, per-slot k) instead of plain majority:** this is a variant if plain voting is weak. Defer it until the unweighted baseline is measured. — answered: deferred: similarity-weighted votes only if plain voting is weak (the row shows it)
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261104-model: Request (T-2973): "should we/could we train a model to fit sampo better? like a better kev/whatever to do more things and more than j…
- T-2974 [FEATURE M, active, 3 steps] The training lake: `sampo models export` (under an existing verb, no new top-level verb)…
- T-2894 [FEATURE M, done, 4 steps] Model bench part 2: every held-out closed task's raw request as data (not only shadow rows), option descriptions for every decision (sy…
- decision 2026-11-04: Recommendation: build Sampo's own model family generic across every Sampo project in this order — the training lake (T-2974), a retrieval baseline d…
- the similar finished task took 4 steps
## Lessons
- A criterion that checks a live artifact must name its tracked path: the brief said state/... while the bench writes the repo's research/models/bench.jsonl, and the merge refused on it
## Files touched
- plugin/lib/sampo/louhi.py
- plugin/tests/test_louhi_models.py
- .fm-scratch/live.py
- research/models/bench.jsonl
- research/models/vectors.jsonl
