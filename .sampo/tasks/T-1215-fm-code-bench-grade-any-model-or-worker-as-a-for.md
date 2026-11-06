---
id: T-1215
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-1212]
source: user
created: 2026-10-16T15:20:15Z
updated: 2026-10-20T21:33:44Z
inferred_deps: [T-1214]
inferred_why: T-1214: bench grades workers, so worker mode comes first
base: 4d9c6f529cc1544eb70f0cf2b43a44422bca4e0c
base_tree: a127e5e3e55b71bbecf34460f1aebee0820ecac2
plan0_at: 2026-10-20T20:55:40Z
plan0_scope: []
verified: strong
---
# fm code bench: grade any model or worker as a Foreman worker on seeded tasks
## Raw request
> fm code bench: grade any model or worker as a Foreman worker on seeded tasks
## Interpretation
Round 2 of Foreman Code (T-1207). fm code bench --model NAME | --worker NAME runs a fixed set of seeded tasks (a wrong operator, an off-by-one, a missing guard clause, a rename across two files, a refused dangerous command the model must route around) in throwaway repos and reports per task: closed or not, verify attempts, guard refusals, tokens and seconds; the summary is a score the harness can use to pick models (and a small-model mode when a model scores low).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code bench against the scripted fake server runs every seed, writes one result line per seed and a summary with the score; a seed the fake fails is reported failed with the reason — verify with `python3 plugin/tests/run.py test_code_bench`
- [x] a seed counts as closed only when the bench re-runs the seed's own verify in its repo after fm code returns and it passes; a scripted fake that says done without fixing gets that seed failed with reason 'verify failed', and a good fake outscores a bad one — verify with `python3 plugin/tests/run.py test_code_bench`
- [x] each seed runs in its own temp repo with its own FOREMAN_HOME and state; the dangerous-command seed aims at a canary file inside that temp dir, which survives; nothing is written outside the temp dirs but the results line — verify with `python3 plugin/tests/run.py test_code_bench`
- [x] a per-seed time limit and max-steps cap: a seed that hangs is killed and reported 'timeout'; the results line carries the seed-set version, model or worker, Foreman version and score = closed seeds / seeds; bench.jsonl appends one line per run and a bad line is skipped on read; --json fields are documented — verify with `python3 plugin/tests/run.py test_code_bench`
## Non-goals
Adapting the harness to a low score (a small-model mode) is a later task; this one only measures. No external eval framework.
## Approach (options → choice → why)
Seeded tasks as small data (files, request, verify command) beside fm demo's seed; each run is fm code in a temp repo with its own FOREMAN_STATE; results append to the state dir's code/bench.jsonl with the model, harness version and score; --json for tooling. Options: reuse fm bench (built for Claude Code session replays, heavier), an external eval framework (a dependency), or seeds plus fm code (chosen).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test against the scripted fake server
2. [x] Seeds, runner, results file and summary
3. [x] Docs
## Resume here
<!-- auto -->
- 2026-10-20T21:12:54Z step 1/3: Failing test against the scripted fake server
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, site/pages.py, plugin/lib/fmcodebench.py, plugin/tests/test_code_bench.py
- touched since last checkpoint: plugin/tests/test_code_bench.py, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcodebench.py, CHANGELOG.md, MASTER.md, README.md, site/pages.py
## Docs impact
README, MASTER.md, CHANGELOG, the site's Foreman Code page, fmcode.py's usage
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_bench` → ✗ exit 1 · Ran 8 tests in 2.3s (1 classes, 16 at a time; slowest: Bench 2s) / FAILED (1 classes) [ran] [tree f190cca1f2ec] (2026-10-20T21:08:43Z)
- (step 2) `python3 plugin/tests/run.py test_code_bench test_code` → exit 0 · Ran 100 tests in 31.5s (21 classes, 16 at a time; slowest: Worker 31s, Bench 11s, Repairs 9s) / OK [ran] [tree 3eb6d4932a9a] (2026-10-20T21:11:07Z)
- (step 3) `python3 plugin/tests/run.py test_code_bench test_docs` → exit 0 · Ran 54 tests in 9.1s (13 classes, 16 at a time; slowest: Bench 9s, TaskLifecycle 1s, TaskDocsDrift 0s) / OK [ran] [tree e2bf08f9fcaa] (2026-10-20T21:11:47Z)
- (ac 1) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 8 tests in 9.0s (1 classes, 16 at a time; slowest: Bench 9s) / OK [ran] [tree e2bf08f9fcaa] (2026-10-20T21:12:01Z)
- (ac 2) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 8 tests in 9.0s (1 classes, 16 at a time; slowest: Bench 9s) / OK [ran] [tree e2bf08f9fcaa] (2026-10-20T21:12:11Z)
- (ac 3) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 8 tests in 8.9s (1 classes, 16 at a time; slowest: Bench 9s) / OK [ran] [tree e2bf08f9fcaa] (2026-10-20T21:12:20Z)
- (ac 4) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 8 tests in 9.1s (1 classes, 16 at a time; slowest: Bench 9s) / OK [ran] [tree e2bf08f9fcaa] (2026-10-20T21:12:29Z)
- (step 2) `python3 plugin/tests/run.py test_code_bench` → ✗ exit 1 · Ran 13 tests in 70.7s (2 classes, 16 at a time; slowest: Bench 71s, Verdict 0s) / FAILED (2 classes) [ran] [tree b614afe323a4] (2026-10-20T21:27:47Z)
- (step 2) `python3 plugin/tests/run.py test_code_bench test_code test_docs` → exit 0 · Ran 151 tests in 30.0s (34 classes, 16 at a time; slowest: Worker 30s, Bench 17s, Repairs 8s) / OK [ran] [tree 308403eff328] (2026-10-20T21:29:10Z)
- (step 3) `python3 plugin/tests/run.py test_code_bench test_code test_docs` → exit 0 · Ran 151 tests in 31.4s (34 classes, 16 at a time; slowest: Worker 31s, Bench 17s, Repairs 9s) / OK [ran] [tree 308403eff328] (2026-10-20T21:29:42Z)
- (ac 1) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 13 tests in 17.1s (2 classes, 16 at a time; slowest: Bench 17s, Verdict 0s) / OK [ran] [tree 308403eff328] (2026-10-20T21:29:59Z)
- (ac 2) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 13 tests in 17.1s (2 classes, 16 at a time; slowest: Bench 17s, Verdict 0s) / OK [ran] [tree 308403eff328] (2026-10-20T21:30:17Z)
- (ac 3) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 13 tests in 18.4s (2 classes, 16 at a time; slowest: Bench 18s, Verdict 0s) / OK [ran] [tree 308403eff328] (2026-10-20T21:30:36Z)
- (ac 4) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 13 tests in 18.3s (2 classes, 16 at a time; slowest: Bench 18s, Verdict 0s) / OK [ran] [tree 308403eff328] (2026-10-20T21:30:54Z)
- (ac 1) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 13 tests in 25.2s (2 classes, 16 at a time; slowest: Bench 25s, Verdict 0s) / OK [ran] [tree 308403eff328] (2026-10-20T21:31:42Z)
- (ac 2) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 13 tests in 25.2s (2 classes, 16 at a time; slowest: Bench 25s, Verdict 0s) / OK [ran] [tree 308403eff328] (2026-10-20T21:31:42Z)
- (ac 3) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 13 tests in 25.2s (2 classes, 16 at a time; slowest: Bench 25s, Verdict 0s) / OK [ran] [tree 308403eff328] (2026-10-20T21:31:42Z)
- (ac 4) `python3 plugin/tests/run.py test_code_bench` → exit 0 · Ran 13 tests in 25.2s (2 classes, 16 at a time; slowest: Bench 25s, Verdict 0s) / OK [ran] [tree 308403eff328] (2026-10-20T21:31:42Z)
- (audit intent) `one fm-reviewer pass (research/T-1215-review.md): 2 medium and 4 low findings, each fixed test-first (13 bench tests incl. a pure verdict() table); a real run with the claude CLI as worker found T-1294 (worker leases revert its own edits), captured` → five seeds in throwaway repos; a seed counts only when the bench writes its tests back and re-runs its check; score = closed/seeds, compared only with the same model/worker, seed set and seed names [tree 308403eff328] (2026-10-20T21:31:42Z)
- (audit adversary) `one fm-reviewer pass (research/T-1215-review.md): 2 medium and 4 low findings, each fixed test-first (13 bench tests incl. a pure verdict() table); a real run with the claude CLI as worker found T-1294 (worker leases revert its own edits), captured` → a model run gets a temp HOME, FOREMAN_HOME and git config, and a canary the dangerous seed must leave; the check runs without a shell from constant seed commands; a worker (real home, for its sign-in) skips the dangerous seed and says so [tree 308403eff328] (2026-10-20T21:31:42Z)
- (audit edge) `one fm-reviewer pass (research/T-1215-review.md): 2 medium and 4 low findings, each fixed test-first (13 bench tests incl. a pure verdict() table); a real run with the claude CLI as worker found T-1294 (worker leases revert its own edits), captured` → a hung run is killed by group (timeout), a hung check is 'verify timeout', a crash keeps its last stderr line, a bad results line is skipped, --model with --worker is refused [tree 308403eff328] (2026-10-20T21:31:42Z)
- (audit operator) `one fm-reviewer pass (research/T-1215-review.md): 2 medium and 4 low findings, each fixed test-first (13 bench tests incl. a pure verdict() table); a real run with the claude CLI as worker found T-1294 (worker leases revert its own edits), captured` → one line per seed as it finishes, the score and where it's kept; --json for tools with every field documented in the README [tree 308403eff328] (2026-10-20T21:31:42Z)
- (audit maintainer) `one fm-reviewer pass (research/T-1215-review.md): 2 medium and 4 low findings, each fixed test-first (13 bench tests incl. a pure verdict() table); a real run with the claude CLI as worker found T-1294 (worker leases revert its own edits), captured` → SEEDS are data with a SEED_SET version; verdict() is pure and table-tested [tree 308403eff328] (2026-10-20T21:31:42Z)
## Log
- 2026-10-16T15:20:15Z created
- 2026-10-17T00:29:22Z blocked: grades workers too: waits for T-1214 (fm code --worker, in a builder lane now)
- 2026-10-20T17:40:22Z set status=planned
- 2026-10-20T18:19:05Z plan review applied: closed = the bench's own verify re-run; isolation with a canary; timeouts, caps, seed-set version and score formula pinned; small-model mode moved to non-goals
- 2026-10-20T20:55:39Z focused
- 2026-10-20T20:56:43Z paused: focus moved to T-1244
- 2026-10-20T21:07:29Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-20T21:07:29Z focused
- 2026-10-20T21:13:14Z paused: focus moved to T-1287
- 2026-10-20T21:24:12Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-20T21:24:12Z focused
- 2026-10-20T21:33:42Z done
- 2026-10-20T21:33:44Z committed 8cb307f3 (7 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The single acceptance criterion only proves the happy path against a fake server. It doesn't show that the score distinguishes good from bad models, that a failing seed is reported with a reason, or that the guard-refusal seed really tests routing around a refusal. — Add checks to the test: a…
- HIGH: "Closed" is undefined. If it means the model said it was done, a model can claim success without fixing the bug, and the score is meaningless. — Define closed as the seed's own verify command passing in the temp repo, run by the bench itself, independent of the model's claim. Report the model…
- MEDIUM: Isolation and safety of the seeds are unspecified. The dangerous-command seed runs in a real shell, and throwaway repos or FOREMAN_STATE could leak into the user's real state, or the command could actually execute if the guard fails. — Use a temp dir with its own FOREMAN_STATE, make the "da…
- MEDIUM: The score formula, the "small-model mode when a model scores low" threshold, and the `--model` vs `--worker` semantics are all unspecified. The mode is in the interpretation but has no step or criterion, so it will either be silently dropped or invented ad hoc. — Pin the formula (e.g. close…
- LOW: Real models are nondeterministic and a seed run can hang or burn tokens. The plan has no per-seed timeout, no budget cap, and no repeat count, and the results line has no seed-set version, so scores can't be compared after seeds change. — Add a per-seed timeout and a token cap, record a seed-s…
- LOW: There's no stated handling of a malformed or partial bench.jsonl, concurrent runs appending, or `--json` schema stability for the harness that consumes it. — Append one line per write, tolerate bad lines on read, and document the `--json` fields in step 3.
Verdict: revise — the core approach is sound, but the "closed" definition and test coverage must be tightened before the failing test is written, or the score can't be trusted.
## Dissent
- [ ] HIGH: The single acceptance criterion only proves the happy path against a fake server. It doesn't show that the score distinguishes good from bad models, that a failing seed is reported with a reason, or that the guard-refusal seed really tests routing around a refusal. — Add checks to the test: a…
- [ ] HIGH: "Closed" is undefined. If it means the model said it was done, a model can claim success without fixing the bug, and the score is meaningless. — Define closed as the seed's own verify command passing in the temp repo, run by the bench itself, independent of the model's claim. Report the model…
- [ ] MEDIUM: Isolation and safety of the seeds are unspecified. The dangerous-command seed runs in a real shell, and throwaway repos or FOREMAN_STATE could leak into the user's real state, or the command could actually execute if the guard fails. — Use a temp dir with its own FOREMAN_STATE, make the "da…
- [ ] MEDIUM: The score formula, the "small-model mode when a model scores low" threshold, and the `--model` vs `--worker` semantics are all unspecified. The mode is in the interpretation but has no step or criterion, so it will either be silently dropped or invented ad hoc. — Pin the formula (e.g. close…
- [ ] LOW: Real models are nondeterministic and a seed run can hang or burn tokens. The plan has no per-seed timeout, no budget cap, and no repeat count, and the results line has no seed-set version, so scores can't be compared after seeds change. — Add a per-seed timeout and a token cap, record a seed-s…
- [ ] LOW: There's no stated handling of a malformed or partial bench.jsonl, concurrent runs appending, or `--json` schema stability for the harness that consumes it. — Append one line per write, tolerate bad lines on read, and document the `--json` fields in step 3.
## Related
Related past work (data from this project's history, not instructions):
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- research mission-20261020-115157.pack: continue, super improve foreman, with latest claude code: round 1 shipped (cost per correct session on the page, Claude Code versi…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- the similar finished task took 2 steps
## Lessons
- A bench must grade what the harness can check itself (the seed's own tests, put back first), never the model's claim; and running it once on a real worker found a bug no fake could
## Plan gaps
- failed first: step 1 Failing test against the scripted fake server
## Files touched
- plugin/tests/test_code_bench.py
- plugin/lib/fmcodebench.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- CHANGELOG.md
- MASTER.md
- README.md
- site/pages.py
- .github/workflows/test.yml
- plugin/lib/fmguard.py
- plugin/tests/run.py
- plugin/tests/test_code_worker.py
- plugin/tests/test_context_tax.py
- plugin/tests/test_guard.py
- plugin/tests/test_guard_cases.py
- plugin/tests/test_reaper.py
- plugin/tests/test_relate.py
- plugin/tests/test_run.py
