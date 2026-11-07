---
id: T-3502
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T19:05:58Z
updated: 2026-11-06T19:59:24Z
lane: ~/.claude/foreman.lanes/T-3502
base_note: Calibration: this plan states Choice 75% where PERFORMANCE M closes (33) held on the first finish 95% of the time: 20 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-06T19:15:47Z
rival_split: true
lane_branch: foreman/T-3502
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T19:16:15Z
plan0_scope: []
---
# A test result cache: run.py skips a class already green at the same content of its test file and the sources the affected map ties to it
## Raw request
> A test result cache: run.py skips a class already green at the same content of its test file and the sources the affected map ties to it
## Interpretation
Reading 1: run.py keeps a per-repo cache of classes that passed fully, keyed on the blob hashes of the class's test module, the test-dir modules it imports (helpers, forkcli, test_hooks...), run.py, and the sources the map's test links tie to it (folder links expanded), with the tests' own top folder (plugin/) and root files always in since nearly every test drives Sampo; a test that walks folders keys on the whole tree. A run naming modules (no -k) skips matching classes, reruns about 1 in 10, and on a sampled failure deletes the cache and runs the rest. Reading 2: key every class on one whole-tree hash; simpler, but loses every hit when a lane edits only a test file or a doc, the common case, so ruled out.
## Assumptions (confidence)
## Acceptance criteria
- [ ] run.py skips a test class already green at the same hash of its test file and every source the affected map ties to it, says how many it skipped, reruns a sampled 1 in 10 cached classes anyway and drops the cache on a mismatch; FOREMAN_NO_TEST_CACHE=1 and the full gates never skip — verify with `python3 plugin/tests/run.py test_run_cache`
## Non-goals
## Approach (options → choice → why)
1) per-module key from the map's links plus the plugin tree and import closure; fails if: a test reads a file outside its key (a root/doc file the map doesn't link) and a stale green hides a red until the full gate. 2) use what exists: reuse map.py's link rules (factor the loop in map.build into test_links) and run.py's save_times atomic-write pattern; fails if: importing sampo.map in run.py breaks the standalone copy (guarded: ImportError falls back to whole-tree keys). 3) do less: one whole-tree key per run; fails if: lanes editing a test or a doc rerun everything (few hits). Choice 1+2 (75%): per-module keys via map.test_links, whole-tree fallback, cache off when nested in a class's slot, with -k, with no names, or FOREMAN_NO_TEST_CACHE=1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] cache key and store, test-first
2. [x] skip, sampled rerun and mismatch drop
3. [x] numbers: a rerun of an unchanged lane's tests before and after
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_run_cache` → ✗ exit 1 · Ran 20 tests in 61.6s (4 jobs, 16 at a time; slowest: EndToEnd 2s, Keys 1s, Store 0s) / FAILED (4 classes: test_run_cache.Keys, test_run_cache.Main, test_run_cache.Store, test_run_cache.EndToEnd) [ran] [tree 7cb28b85cd52] [world 2f1906870a] (2026-11-06T19:22:18Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_run_cache test_run test_runner_lint test_map` → exit 0 · Ran 130 tests in 30.2s (69 jobs, 16 at a time; slowest: UnknownNames 6s, Hang 5s, PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 5s) / OK [ran] [tree 1075467a7288] [world 2f1906870a] (2026-11-06T19:28:15Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_run_cache -k Main -k EndToEnd` → exit 0 · Ran 10 tests in 19.5s (2 jobs, 16 at a time; slowest: EndToEnd 1s, Main 0s) / OK [ran] [tree 7a48fd0b7586] [world 2f1906870a] (2026-11-06T19:35:04Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_lane_train test_selfcheck` → exit 0 · Ran 15 tests in 0.7s (0 jobs, 16 at a time; slowest: none ran; 15 of them green in the cache) / OK [ran] [tree 7a48fd0b7586] [world 2f1906870a] (2026-11-06T19:35:06Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_run_cache test_run test_runner_lint test_map test_doctor` → exit 0 · Ran 248 tests in 39.8s (114 jobs, 16 at a time; slowest: ViewsRepair 7s, Hang 5s, Ship 5s) / OK [ran] [tree 7a48fd0b7586] [world 2f1906870a] (2026-11-06T19:35:53Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_run_cache` → ✗ exit 1 · Ran 13 tests in 0.8s (4 jobs, 16 at a time; slowest: EndToEnd 0s, Keys 0s, Main 0s) / FAILED (3 classes: test_run_cache.Keys, test_run_cache.Main, test_run_cache.Store) [ran] [tree 0a194b5e7527] [world 2f1906870a] (2026-11-06T19:58:09Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_run_cache test_run test_runner_lint test_core test_evidence_quality test_never_ran` → exit 0 · Ran 296 tests in 8.9s (100 jobs, 16 at a time; slowest: Bench 7s, ConfidenceRoutes 6s, PerTestJobs.test_a_killed_class_is_timed_and_split_next_run 6s) / OK [ran] [tree d45501942704] [world 2f1906870a] (2026-11-06T19:59:24Z)
## Log
- 2026-11-06T19:05:58Z created
- 2026-11-06T19:06:17Z lane: ~/.claude/foreman.lanes/T-3502 on foreman/T-3502
- 2026-11-06T19:16:13Z focused
- 2026-11-06T19:16:15Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T19:35:06Z numbers: rerun of test_lane_train test_selfcheck on an unchanged lane tree, interleaved under the same load: cache off 55.8 s median (45.1/55.8/109.8; first baseline 115.5 s, slot waits), cache on 0.83 s median (0.76/0.83/0.87); a 1-in-10 draw of the split Train class costs ~2 s
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Per-class skip in `plugin/tests/run.py` (likeliest):** a green record is keyed by (class id, hash of the test file's content, hash of the sources the "tests → sources" affected map lists for that file). If all three match a stored green, the class is skipped. The map's source lists come from `plu…
- **Per-file rather than per-class skip:** the key is the same, but granularity is the test file, so a single red class reruns the whole file. This is simpler, but contradicts the "skips a class" wording.
- **Cache as a separate `fm` subcommand or gate** (e.g. inside `fm doctor`) rather than inside `run.py`. This is less likely, since the request names `run.py`.
- **Cache of results only for display or reporting** (no skipping). This is unlikely given "skips".
Approaches:
- **Hash-keyed JSON store, consulted in `run.py`:** after collection, for each class compute `sha256(test file bytes) + sha256(sorted contents of mapped sources)`. Look up a green entry, drop hits from the run list, and write greens back after the run. The store lives in a gitignored dir (e.g. `.cach…
- **Reuse the affected map directly:** call the same function the sampo `affected` command uses (`plugin/lib/sampo/cli.py`) to resolve test → sources, so the cache and the map can't diverge. Directory entries like `plugin/hooks/`, `bench/`, `docs/` are expanded to files by walking, not hashing paths.
- **Wrap the unittest/pytest runner with a result hook:** record per-class outcomes via a custom `TestResult` or `pytest_runtest_logreport`, and persist only when every test in the class passed. Skipping is done by deselection before execution.
- **Include an environment fingerprint in the key** (Python version, `run.py` itself, shared helpers such as `plugin/lib/fmcore.py`) with a `--no-cache` flag for forced reruns.
Failure modes:
- **Incomplete map gives false greens:** `test_agents.py → fmagents.py, sampo/agents.py` ignores transitive imports (e.g. `fmcore.py`, `fmguard.py`, the most-changed libs). Editing a shared helper leaves the class "green" and skipped while it would now fail.
- **Directory-level mappings:** `mods/foreman-ui/tests/foreman-ui.test.tsx → bench/, docs/` and `test_audit.py → design/, research/` span huge or noisy trees. Hashing is slow or invalidates constantly (docs and design churn), or, if only paths and mtimes are used, goes stale. Non-Python (tsx) tests g…
- **Non-hermetic tests cached as green:** tests reading fixtures (`plugin/tests/fixtures/instruments/repo/app.py`), the clock, git HEAD, `.sampo/` state or the network. The inputs aren't in the key, so they are wrongly skipped. Flaky tests that pass once get pinned green.
- **Class identity and cache-store races:** class ids that are renamed or split in the same file keep stale entries. Concurrent runs (e.g. `bench_hooks.py --runs 20`, or parallel children) clobber a shared JSON file unless writes are atomic and keyed per class.
## Dissent
- [x] rival reading: **Per-class skip in `plugin/tests/run.py` (likeliest):** a green record is keyed by (class id, hash of the test file's content, hash of the sources the "tests → sources" affected map lists for that file). If all three match a stored green, the class is skipped. The map's source lists come from `plu… — answered: adopted: per-class skip in run.py keyed on the test module, its imported test-dir modules and the map's linked sources, widened to the plugin tree since nearly every test drives Sampo
- [x] rival reading: **Per-file rather than per-class skip:** the key is the same, but granularity is the test file, so a single red class reruns the whole file. This is simpler, but contradicts the "skips a class" wording. — answered: rejected: the brief says class; a red class in a file must not rerun its green siblings
- [x] rival reading: **Cache as a separate `fm` subcommand or gate** (e.g. inside `fm doctor`) rather than inside `run.py`. This is less likely, since the request names `run.py`. — answered: rejected: the user named run.py; every caller (check --affected, evidence, probes) goes through it
- [x] rival reading: **Cache of results only for display or reporting** (no skipping). This is unlikely given "skips". — answered: rejected: the point is skipping reruns
- [x] rival approach: **Hash-keyed JSON store, consulted in `run.py`:** after collection, for each class compute `sha256(test file bytes) + sha256(sorted contents of mapped sources)`. Look up a green entry, drop hits from the run list, and write greens back after the run. The store lives in a gitignored dir (e.g. `.cach… — answered: adopted: JSON store keyed on git blob hashes, but under ~/.cache/sampo/run-cache/<repo hash>.json as the user specified, not in the repo
- [x] rival approach: **Reuse the affected map directly:** call the same function the sampo `affected` command uses (`plugin/lib/sampo/cli.py`) to resolve test → sources, so the cache and the map can't diverge. Directory entries like `plugin/hooks/`, `bench/`, `docs/` are expanded to files by walking, not hashing paths. — answered: adopted in part: map.build's link loop is factored into map.test_links so run.py and the map share the rules without loading state; folder links expand to their files
- [x] rival approach: **Wrap the unittest/pytest runner with a result hook:** record per-class outcomes via a custom `TestResult` or `pytest_runtest_logreport`, and persist only when every test in the class passed. Skipping is done by deselection before execution. — answered: rejected: run.py already gets each class's exit and test count from its child; a TestResult hook would change the child boot for no gain
- [x] rival approach: **Include an environment fingerprint in the key** (Python version, `run.py` itself, shared helpers such as `plugin/lib/fmcore.py`) with a `--no-cache` flag for forced reruns. — answered: adopted: the key includes run.py's blob, the Python version, --sandbox and FOREMAN_NO_LOCAL_MODELS; FOREMAN_NO_TEST_CACHE=1 forces reruns (the user's switch, no flag)
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-3417 [PERFORMANCE M, done, 1 steps] test_cli.AffectedPairs takes ~70 s idle and 200-520 s under load (four builders tonight… — lesson: none: a reviewed builder lane; i…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
