---
id: T-2437
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: [T-2374]
source: user
created: 2026-10-31T18:10:36Z
updated: 2026-11-01T17:07:16Z
rival_at: 2026-11-01T16:40:36Z
rival_split: true
base: 3a3da713e12056e204bafbf8d083f2e432c87bc7
base_tree: 95c2a5443215bb44ee60338bfd34af0d0ca8d6e8
plan0_at: 2026-11-01T16:48:28Z
plan0_scope: []
verified: strong
---
# Gen 2: a model layer (user steer 2026-10-31, start after round 1). (1) A…
## Raw request
> Gen 2: a model layer (user steer 2026-10-31, start after round 1). (1) A provider-agnostic decision interface (choice, score, probability with calibrated confidence), backends tried cheapest-first: deterministic rules, then local models (selfjev-4b or jeff behind the Jev-compatible API via TYPESAFE_BASE_URL, Von for intent routing, Jevlike for task-specific models Foreman trains from its own history), then TypeSafe's hosted Jev, then Claude as the fallback. (2) The same for other model types: embeddings for search, recall and dedupe; rerankers for leads; vision for UI checks; local code models through fm code and the user's existing vLLM / llama-swap servers. (3) Candidate uses: intake type and tier, fm find lead triage, coverage-cell and done-claim checks, the model router (#9), idea dedupe and scoring. (4) Rules: never inside the guard or the evidence gates (models advise, proof decides); sensitive repos use local backends only; installs and model downloads go through the install queue for the user's yes; each use kept only if the exam shows it beats the path it replaces on accuracy, cost or latency, its probabilities checked against outcomes. Record the layer in the coverage grid as a new area; selfjev, jeff, Jevlike and Von go in the not-yet ledger as candidates to evaluate, not assumptions.
## Interpretation
Readings: (a) T-2437 records the layer in the tower and makes it a gen-2 Mission, so its build runs in gen 2 as exam-gated briefs: a '## Model layer' coverage area (64 grounded cells), the four local candidates in not-yet.md as unevaluated candidates, and a Model layer row first in gen-2's seed (the user's steer names gen 2); (b) build the whole decision interface and every backend inside this one task. (a): the task's own criteria are the tower records, and the user's rule keeps each use only if the exam shows it beats the path it replaces, which is a Mission's briefs-and-exam loop, not one task.
## Assumptions (confidence)
## Acceptance criteria
- [x] gen 2's coverage grid has a '## Model layer' area with all 64 stage × surface cells (F, I or N/A, each grounded) — verify with `fm genesis check`
- [x] the not-yet ledger lists selfjev-4b, jeff, Jevlike and Von as candidates to evaluate (blocker: unevaluated; unblocks-with: an exam arm that beats the path it replaces), not as assumptions — verify with `grep -c -E 'selfjev|jeff|Jevlike|Von' state/projects/foreman-4a056f/research/genesis/not-yet.md`
- [x] a not-yet candidate (blocker: unevaluated) passes the ledger check without two tries until evaluated — verify with `python3 plugin/tests/run.py test_genesis`
- [x] gen-2's seed lists the Model layer Mission first — verify with `grep -q mission-model-layer state/projects/foreman-4a056f/research/genesis/gen-2/seed.md`
## Non-goals
## Approach (options → choice → why)
1) Tower records plus a small code change: not_yet() accepts a candidate item (blocker: unevaluated) without two tries until it is evaluated; coverage.md gains the Model layer area; not-yet.md lists selfjev-4b, jeff, Jevlike and Von; gen-2's seed gets a Model layer Mission row first, the 7th coverage row moving to the wait line; drift rerun. Fails if: a candidate never gets evaluated (its unblocks-with names the exam arm, and every seed retries not-yet items). 2) Build the decision interface now in this task. Fails if: it skips the Mission's exam gate the user's rule requires. 3) Use what exists: fmmodels (profiles, resolve: local and cloud backends), the prediction book and calibration ledger (probabilities checked against outcomes), fm second (cold reads) and the install queue (fm ask --later) are the pieces the Mission composes. Likely outcome: the Mission's briefs build on them rather than a new stack. 4) Do less: only the coverage area. Fails if: the user's steer for gen 2 is left out of gen 2. Choice 1 (85%): the user's steer lands in gen 2 as a Mission, on what exists (3).
## Risks and rollback
What fails: amending a filed seed changes drift (rerun it); the Model layer's 64 cells could read templated (each names its own file and use); a candidate exemption could hide stale not-yet items (it holds only while the blocker says unevaluated). Undo: revert the not_yet change; refile coverage.md, not-yet.md and the seed from their previous text (the tower keeps no history, so the previous texts are saved in the scratchpad first).
## Execution prompt
## Steps
1. [x] red test: not-yet candidates
2. [x] not_yet() accepts candidates
3. [x] coverage.md: the Model layer area, 64 grounded cells
4. [x] not-yet.md: the four candidates
5. [x] gen-2's seed: the Model layer Mission first; drift rerun
## Resume here
## Docs impact
MASTER.md (T-2437 candidate form) and CHANGELOG.md Unreleased; the tower's coverage grid, not-yet ledger and gen-2 seed were refiled through fm genesis put
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_an_unevaluated_candidate_needs_no_tries_until_it_is_evaluated test_genesis` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: GenesisCheck 1s) / FAILED (1 classes: test_genesis.GenesisCheck) [ran] [tree f4386bc95b95] (2026-11-01T16:48:51Z)
- `python3 plugin/tests/run.py -k test_an_unevaluated_candidate_needs_no_tries_until_it_is_evaluated test_genesis` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: GenesisCheck 0s) / FAILED (1 classes: test_genesis.GenesisCheck) (start tree + this task's tests) [ran] [tree 5f2bb68e2174] (2026-11-01T16:49:01Z)
- `python3 plugin/tests/run.py -k test_an_unevaluated_candidate_needs_no_tries_until_it_is_evaluated test_genesis` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: GenesisCheck 1s) / OK [ran] [tree 5f2bb68e2174] (2026-11-01T16:49:01Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 185 tests in 14.7s (18 classes, 16 at a time; slowest: GenesisRead 14s, GenesisCheck 12s, GenesisSweep 10s) / OK [ran] [tree 5f2bb68e2174] (2026-11-01T16:49:16Z)
- (step 3) `fm genesis check` → exit 0 · ✓ frame: 0 added categories / ✓ read [ran] [tree 5f2bb68e2174] (2026-11-01T16:54:00Z)
- (step 4) `grep -c -E 'selfjev|jeff|Jevlike|Von' state/projects/foreman-4a056f/research/genesis/not-yet.md` → exit 0 · 6 [ran] [tree 5f2bb68e2174] (2026-11-01T16:54:19Z)
- (step 5) `grep -q mission-model-layer state/projects/foreman-4a056f/research/genesis/gen-2/seed.md` → exit 0 · (no output) [ran] [tree 5f2bb68e2174] (2026-11-01T16:54:50Z)
- (ac 1) `fm genesis check` → exit 0 · ✓ frame: 0 added categories / ✓ read [ran] [tree ce004deed49e] (2026-11-01T16:55:00Z)
- (ac 2) `grep -c -E 'selfjev|jeff|Jevlike|Von' state/projects/foreman-4a056f/research/genesis/not-yet.md` → exit 0 · 6 [ran] [tree ce004deed49e] (2026-11-01T16:55:00Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 185 tests in 10.9s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisCheck 8s, GenesisSweep 8s) / OK [ran] [tree ce004deed49e] (2026-11-01T16:55:11Z)
- (ac 4) `grep -q mission-model-layer state/projects/foreman-4a056f/research/genesis/gen-2/seed.md` → exit 0 · (no output) [ran] [tree ce004deed49e] (2026-11-01T16:55:12Z)
- (ac 1) `fm genesis check` → exit 0 · ✓ frame: 0 added categories / ✓ read [ran] [tree ce004deed49e] (2026-11-01T17:01:04Z)
- (ac 2) `grep -c -E 'selfjev|jeff|Jevlike|Von' state/projects/foreman-4a056f/research/genesis/not-yet.md` → exit 0 · 6 [ran] [tree ce004deed49e] (2026-11-01T17:01:04Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 185 tests in 10.9s (18 classes, 16 at a time; slowest: GenesisRead 11s, GenesisCheck 8s, GenesisSweep 8s) / OK [ran] [tree ce004deed49e] (2026-11-01T17:01:04Z)
- (ac 4) `grep -q mission-model-layer state/projects/foreman-4a056f/research/genesis/gen-2/seed.md` → exit 0 · (no output) [ran] [tree ce004deed49e] (2026-11-01T17:01:04Z)
- (audit intent) `main-thread lens pass over the not_yet candidate change, its test and the three tower files; every tower put went through the Sonnet-decided read (coverage needed 11 older cells fixed, which Sonnet named with their rules)` → the user's gen-2 steer lands in gen 2: the Model layer area (64 grounded cells, 47 ideas) is in coverage.md, the four local candidates are in not-yet.md as unevaluated, and gen-2's seed opens with the Model layer Mission (#5 tools moved to the wait line, the cap of 8 kept) [tree ce004deed49e] (2026-11-01T17:01:04Z)
- (audit edge) `main-thread lens pass over the not_yet candidate change, its test and the three tower files; every tower put went through the Sonnet-decided read (coverage needed 11 older cells fixed, which Sonnet named with their rules)` → a candidate still needs its unblocks-with; once its blocker no longer starts 'unevaluated' it owes two tries like any item; the seed edit kept every other row and its wait line [tree ce004deed49e] (2026-11-01T17:01:04Z)
- (audit adversary) `main-thread lens pass over the not_yet candidate change, its test and the three tower files; every tower put went through the Sonnet-decided read (coverage needed 11 older cells fixed, which Sonnet named with their rules)` → the candidate form can't hide a failed spike: only a blocker that starts 'unevaluated' is exempt, and the critique and sweep read the ledger [tree ce004deed49e] (2026-11-01T17:01:04Z)
- (audit operator) `main-thread lens pass over the not_yet candidate change, its test and the three tower files; every tower put went through the Sonnet-decided read (coverage needed 11 older cells fixed, which Sonnet named with their rules)` → fm genesis status now names Mission 1 (model-layer) next; fm genesis check shows the candidates as items with no problem [tree ce004deed49e] (2026-11-01T17:01:04Z)
- (audit maintainer) `main-thread lens pass over the not_yet candidate change, its test and the three tower files; every tower put went through the Sonnet-decided read (coverage needed 11 older cells fixed, which Sonnet named with their rules)` → one boolean in not_yet() with the steer cited; the tower texts before this task are kept in the session scratchpad for rollback [tree ce004deed49e] (2026-11-01T17:01:04Z)
- (audit intent) `main-thread lens pass over the not_yet candidate change, its test and the three tower files; every tower put went through the Sonnet-decided read (coverage needed 11 older cells fixed, which Sonnet named with their rules)` → the user's gen-2 steer lands in gen 2: the Model layer area (64 grounded cells, 47 ideas) is in the coverage grid, the four local candidates are in the not-yet ledger as unevaluated, and gen-2's seed opens with the Model layer Mission (#5 tools moved to the wait line, the cap of 8 kept) [tree ce004deed49e] (2026-11-01T17:01:38Z)
- (audit edge) `main-thread lens pass over the not_yet candidate change, its test and the three tower files; every tower put went through the Sonnet-decided read (coverage needed 11 older cells fixed, which Sonnet named with their rules)` → a candidate still needs its unblocks-with; once its blocker no longer starts 'unevaluated' it owes two tries like any item; the seed edit kept every other row and its wait line [tree ce004deed49e] (2026-11-01T17:01:38Z)
- (audit adversary) `main-thread lens pass over the not_yet candidate change, its test and the three tower files; every tower put went through the Sonnet-decided read (coverage needed 11 older cells fixed, which Sonnet named with their rules)` → the candidate form can't hide a failed spike: only a blocker that starts 'unevaluated' is exempt, and the critique and sweep read the ledger [tree ce004deed49e] (2026-11-01T17:01:38Z)
- (audit operator) `main-thread lens pass over the not_yet candidate change, its test and the three tower files; every tower put went through the Sonnet-decided read (coverage needed 11 older cells fixed, which Sonnet named with their rules)` → fm genesis status now names Mission 1 (model-layer) next; fm genesis check shows the candidates as items with no problem [tree ce004deed49e] (2026-11-01T17:01:38Z)
- (audit maintainer) `main-thread lens pass over the not_yet candidate change, its test and the three tower files; every tower put went through the Sonnet-decided read (coverage needed 11 older cells fixed, which Sonnet named with their rules)` → one boolean in not_yet() with the steer cited; the tower texts before this task are kept in the session scratchpad for rollback [tree ce004deed49e] (2026-11-01T17:01:38Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree ce004deed49e] (2026-11-01T17:02:54Z)
## Log
- 2026-10-31T18:10:36Z created
- 2026-10-31T18:10:41Z set depends_on=['T-2374']
- 2026-10-31T18:20:24Z steer recorded 2026-10-31 (user, mid-round-1): filed into gen 2's tower at seed time with the coverage area and the four not-yet candidates; no round-1 work changes for it
- 2026-11-01T08:01:16Z blocked: starts after round 1, as the user's steer says (2026-10-31); round 1's last steps wait on the user's cold-read call
- 2026-11-01T16:39:12Z unblocked
- 2026-11-01T16:39:13Z round 1 done 2026-11-01: gen-2/seed.md filed; this starts now (user steer 2026-10-31: start after round 1)
- 2026-11-01T16:40:51Z set approved=True
- 2026-11-01T16:48:28Z focused
- 2026-11-01T16:54:59Z scope: plugin/lib/fmgenesis.py (not_yet candidates), plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md; tower: coverage.md (Model layer area, and 11 older cells the Sonnet read flagged), not-yet.md, gen-2/seed.md
- 2026-11-01T17:02:13Z done
- 2026-11-01T17:02:15Z committed 5b32e1ef (4 files)
- 2026-11-01T17:02:54Z guard authorization added: publish
- 2026-11-01T17:07:16Z publish grant used by fm ship
## Follow-ups captured
## Build vs reuse
Reuses fmmodels (backends), fmforesight's prediction book and fmoutcomes' calibration ledger (probabilities against outcomes), fm second (cold reads), fm ask --later (install queue); new code only for not-yet candidates.
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: a new `plugin/lib` module (e.g. `fmmodels.py`) providing one `decide()` interface with a cheapest-first backend cascade (rules → local → hosted Jev → Claude), plus an eval harness and calibration tracking, with only a thin first wiring.** Turns on the cascade/escalation contract and th…
- **Spec/roadmap-only reading:** "start after round 1" and the "candidate" wording could mean updating MASTER.md, the coverage grid, and the ledger with the Gen 2 plan, and writing no runtime code yet. Turns on MASTER.md and the grid file.
- **Full build reading:** every listed use (intake tier, `fm find` triage, coverage-cell checks, router #9, dedupe) gets wired, including embeddings, rerankers and vision. This is likely too broad for one pass, since each use must first pass its exam.
- **Policy-first reading:** the main deliverable is the rules (never in `fmguard.py` or the evidence gates, sensitive repos local-only, installs through the install queue), enforced as checks, with the model layer secondary.
Approaches:
- **Single `fmmodels.py` with a backend registry:** each backend declares cost, latency, a `sensitive_ok` flag and a `decide(kind, input)` returning value plus calibrated confidence. A cascade escalates when confidence falls below a per-use threshold. Deterministic rules are the first backend and nee…
- **Shadow-mode first:** each use runs the model path alongside the existing path, logs both to the existing replay/eval store (`fm replay`, `plugin/evals/`), and never changes behaviour until the exam records a win on accuracy, cost or latency. This directly implements "kept only if the exam shows i…
- **Install requests through the existing install queue:** backend discovery only proposes installs or model downloads and never fetches them. Find the install-queue entry point in `fmcli.py` and reuse it.
- **Ledger and grid first, code second:** add the new coverage-grid area and the four not-yet candidates in a small first commit, so the later code has a place to record exam results.
Failure modes:
- **Guard leakage:** a model call gets imported into or reached from `fmguard.py`, `fmhooks.py` or an evidence-gate path (done-claim check). It would make a model's advice decide a gate, and it would also add latency that `bench_hooks.py --runs 20` would catch. Needs a static test that those modules …
- **Sensitive-repo fallthrough:** the cascade reaches hosted Jev or Claude for a sensitive repo because a local backend is down or low-confidence. It must return "no decision" and fall back to the rules path rather than escalate. Turns on how the sensitivity flag is read in the cascade.
- **Uncalibrated confidence:** backends return raw scores that are treated as probabilities, so escalation thresholds are meaningless. Calibration needs outcome records per use, and with sparse history the layer should stay in shadow mode instead of promoting.
- **Unavailable-backend assumptions:** selfjev, jeff, Jevlike and Von get coded as if they exist, though the request says they are candidates. Tests that pass only with a fake backend can hide this. The ledger entries should stay "unverified" until an exam run against a real endpoint.
## Dissent
- [x] rival reading: **Likeliest: a new `plugin/lib` module (e.g. `fmmodels.py`) providing one `decide()` interface with a cheapest-first backend cascade (rules → local → hosted Jev → Claude), plus an eval harness and calibration tracking, with only a thin first wiring.** Turns on the cascade/escalation contract and th… — answered: adopted for the Mission, not this task: the decide() cascade on fmmodels is the Model layer Mission's first brief; this task records the layer and puts the Mission in gen 2
- [x] rival reading: **Spec/roadmap-only reading:** "start after round 1" and the "candidate" wording could mean updating MASTER.md, the coverage grid, and the ledger with the Gen 2 plan, and writing no runtime code yet. Turns on MASTER.md and the grid file. — answered: adopted in part: this task writes no runtime code beyond the not-yet candidate form; the runtime comes from the Mission's briefs
- [x] rival reading: **Full build reading:** every listed use (intake tier, `fm find` triage, coverage-cell checks, router #9, dedupe) gets wired, including embeddings, rerankers and vision. This is likely too broad for one pass, since each use must first pass its exam. — answered: rejected for one pass: each use is kept only if its exam beats the path it replaces, so the Mission wires them one at a time
- [x] rival reading: **Policy-first reading:** the main deliverable is the rules (never in `fmguard.py` or the evidence gates, sensitive repos local-only, installs through the install queue), enforced as checks, with the model layer secondary. — answered: adopted: the Mission's first criteria are the policy checks (no model in fmguard or the evidence gates, sensitive repos local only, installs via the queue); its seed row and coverage cells name them
- [x] rival approach: **Single `fmmodels.py` with a backend registry:** each backend declares cost, latency, a `sensitive_ok` flag and a `decide(kind, input)` returning value plus calibrated confidence. A cascade escalates when confidence falls below a per-use threshold. Deterministic rules are the first backend and nee… — answered: adopted for the Mission: a backend registry with cost, latency and a sensitive_ok flag in fmmodels; recorded in the Model layer cells
- [x] rival approach: **Shadow-mode first:** each use runs the model path alongside the existing path, logs both to the existing replay/eval store (`fm replay`, `plugin/evals/`), and never changes behaviour until the exam records a win on accuracy, cost or latency. This directly implements "kept only if the exam shows i… — answered: adopted for the Mission: shadow mode first, logged beside the existing path until the exam decides; recorded in the cells
- [x] rival approach: **Install requests through the existing install queue:** backend discovery only proposes installs or model downloads and never fetches them. Find the install-queue entry point in `fmcli.py` and reuse it. — answered: adopted: installs and model downloads go through fm ask --later (the install queue); the cells name it
## Plan review
Self-critique: the rival's full-build reading is the user's end state, but the user's own rule (keep a use only if the exam shows it beats the path it replaces) makes it a Mission's loop of briefs and exam arms, so this task records the layer, fixes the ledger form the user's candidates need, and puts the Model layer Mission first in gen 2. Shadow mode, the backend registry with sensitive_ok, the policy checks and the install queue are written into the Model layer cells for the Mission. Approved under full autonomy.
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-31: Standing rule (user steer 2026-10-31): gen 2 builds a model layer, small specialist models wherever a decision, ranking or lookup is the job, backen…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- research mission-20261031-083838: Request: Mission 8, Genesis gen 1: 7. Self-repair and self-improvement. Its own failures, friction, misses and my corrections become fi…
- research mission-20261031-083838.pack: Mission 8, Genesis gen 1: 7. Self-repair and self-improvement. Its own failures, friction, misses and my corrections become fixes,…
## Lessons
- A user's next-generation request has to reach the next seed explicitly: the auto-written seed ranks the coverage grid and can't see a task in the queue
## Plan gaps
- failed first: step 1 red test: not-yet candidates
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
