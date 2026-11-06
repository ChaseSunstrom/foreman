---
id: T-3140
type: PERFORMANCE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T04:53:35Z
updated: 2026-11-06T03:54:42Z
rival_at: 2026-11-05T04:54:18Z
rival_split: true
builder_model: haiku
lane_branch: worktree-agent-a5dd1a6557b592e6b
base: 9bb63c17fb770e1f5c44063ed82b088c495eb852
base_tree: 2e7b242512a823221cdc7407dd7cab033ede12bb
plan0_at: 2026-11-05T04:57:57Z
plan0_scope: []
base_note: Calibration: this plan states Choice 75% where PERFORMANCE M closes (27) held on the first finish 95% of the time: 20 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
builder_returned: 2026-11-05T06:41:42Z
paused_tree: dae032d6b1feb68bc5b0d7916ad2fb1e84cfd3c9
inferred_deps: [T-3138]
inferred_why: T-3138: named in its request
group: fast merges and merge trains
---
# Fast merges part 2: test results cached by a hash of every file each test imports, so a merge reruns only tests whose inputs changed (T-3138)
## Raw request
> Fast merges part 2: test results cached by a hash of every file each test imports, so a merge reruns only tests whose inputs changed (T-3138)
## Interpretation
Reading 1 (chosen): run.py records, per test class, the plugin and test files its process imported (sys.modules plus files it opened under plugin/ via an audit hook in the test child only) and the outcome; a later run skips a class whose recorded inputs all hash the same and whose last outcome passed, saying so; any changed input, a missing record, or FM_NO_TEST_CACHE runs it; the full suite still runs on main after landing (part 3). Reading 2: git diff paths mapped by name; rejected, sampo check --affected's name map misses indirect imports.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a second run.py with no file changed reruns no class and says how many it reused; changing one module reruns exactly the classes that imported it; a class that failed last time always reruns — verify with `python3 plugin/tests/run.py test_run_cache`
- [ ] subprocesses count: the test child's env carries a sitecustomize recorder so every python process a test spawns (fm, sampo, hooks) writes its imported and opened plugin files into the test's record; python version and FOREMAN_/SAMPO_ env values join the key — verify with `python3 plugin/tests/run.py test_run_cache`
- [ ] drift check: a full uncached run (nightly or sampo check --no-cache) compares each class's real outcome with what the cache would have reused; a mismatch turns the cache off for that class and files a task — verify with `python3 plugin/tests/run.py test_run_cache`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: run.py's per-class children (16 at a time, processes, so no GIL) and the evidence tree hash; likely outcome: a typical lane reruns a few classes, not 3,000 tests. 2. Do less: cache whole-module results; fails if: one changed import reruns everything. 3. Coverage.py per line; fails if: it isn't installed (Sampo installs nothing). Choice 1 (75%)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in a new test_run_cache with a fixture suite
2. [x] the input capture and the cache in run.py
## Resume here
<!-- auto -->
- 2026-11-05T05:48:52Z steps 2/2 done
- git: worktree-agent-a5dd1a6557b592e6b; 4 uncommitted: plugin/tests/helpers.py, plugin/tests/recorder/sitecustomize.py, plugin/tests/run.py, plugin/tests/test_run_cache.py
- touched since last checkpoint: plugin/tests/helpers.py, plugin/tests/recorder/sitecustomize.py, plugin/tests/test_run_cache.py, plugin/tests/run.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_run_cache` → exit 0 · Ran 10 tests in 1.5s (1 classes, 16 at a time; slowest: Cache 1s) / OK [ran] [tree d4de8baab907] [world 2f1906870a] (2026-11-05T05:04:27Z)
- (step 2) `FM_NO_TEST_CACHE=1 python3 plugin/tests/run.py test_hooks -k NoTaskGate.test_shell_writes 2>&1 | tail -4` → exit 0 · Ran 1 tests in 1.9s (1 classes, 16 at a time; slowest: NoTaskGate 1s) / OK [ran] [tree d38177ec6698] [world 2f1906870a] (2026-11-05T05:10:47Z)
- (step 1) `python3 plugin/tests/run.py test_run_cache` → exit 0 · Ran 12 tests in 1.7s (1 classes, 16 at a time; slowest: Cache 1s) / OK [ran] [tree 6ccc73dfc4b3] [world 2f1906870a] (2026-11-05T05:35:58Z)
- (step 2) `python3 plugin/tests/run.py test_run_cache` → exit 0 · Ran 12 tests in 0.5s (0 classes, 16 at a time; slowest: Cache 0s) / OK [ran] [tree 6ccc73dfc4b3] [world 2f1906870a] (2026-11-05T05:35:59Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ci_annotations test_doctor test_left_out test_models test_rename_scan test_run test_run_cache && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [12.26s] [ran] [tree 6ccc73dfc4b3] [world 2f1906870a] (2026-11-05T05:36:27Z)
- (ac 1) `python3 plugin/tests/run.py test_run_cache 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED"` → ✗ exit 1 · Ran 19 tests in 7.0s (1 classes, 16 at a time; slowest: Cache 4s) / FAILED (1 classes: test_run_cache.Cache) [ran] [tree 4868c45039cc] [world 2f1906870a] (2026-11-05T05:46:26Z)
- (ac 2) `python3 plugin/tests/run.py test_run_cache 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED"` → ✗ exit 1 · Ran 19 tests in 7.0s (1 classes, 16 at a time; slowest: Cache 4s) / FAILED (1 classes: test_run_cache.Cache) [ran] [tree 4868c45039cc] [world 2f1906870a] (2026-11-05T05:46:26Z)
- (ac 3) `python3 plugin/tests/run.py test_run_cache 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED"` → ✗ exit 1 · Ran 19 tests in 7.0s (1 classes, 16 at a time; slowest: Cache 4s) / FAILED (1 classes: test_run_cache.Cache) [ran] [tree 4868c45039cc] [world 2f1906870a] (2026-11-05T05:46:26Z)
- (ac 1) `python3 plugin/tests/run.py test_run_cache 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED|Error|assert" | head -20` → exit 0 · Ran 19 tests in 2.8s (1 classes, 16 at a time; slowest: Cache 2s) / OK [ran] [tree 45dab507cc13] [world 2f1906870a] (2026-11-05T05:48:48Z)
- (ac 2) `python3 plugin/tests/run.py test_run_cache 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED|Error|assert" | head -20` → exit 0 · Ran 19 tests in 2.8s (1 classes, 16 at a time; slowest: Cache 2s) / OK [ran] [tree 45dab507cc13] [world 2f1906870a] (2026-11-05T05:48:48Z)
- (ac 3) `python3 plugin/tests/run.py test_run_cache 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED|Error|assert" | head -20` → exit 0 · Ran 19 tests in 2.8s (1 classes, 16 at a time; slowest: Cache 2s) / OK [ran] [tree 45dab507cc13] [world 2f1906870a] (2026-11-05T05:48:48Z)
- (step 1) `python3 plugin/tests/run.py test_run_cache` → exit 0 · Ran 19 tests in 4.0s (1 classes, 16 at a time; slowest: Cache 3s) / OK [ran] [tree 60be7755b833] [world 2f1906870a] (2026-11-05T06:38:40Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ci_annotations test_doctor test_left_out test_models test_rename_scan test_run test_run_cache && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [15.11s] [ran] [tree 60be7755b833] [world 2f1906870a] (2026-11-05T06:41:27Z)
## Log
- 2026-11-05T04:53:35Z created
- 2026-11-05T04:53:47Z set approved=True
- 2026-11-05T04:57:29Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3140.builder.md
- 2026-11-05T04:57:56Z focused
- 2026-11-05T06:42:00Z blocked: built and review-fixed (branch worktree-agent-a5dd1a6557b592e6b, c5970e7a) but measured no warm gain (130/1366 reused, 12m24s vs 12m02s); kept for when slow classes become cacheable; see the decision
- 2026-11-05T12:44:14Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5dd1a6557b592e6b (branch worktree-agent-a5dd1a6557b592e6b kept: not merged); dropped: parked: test cache correct but no gain (warm 12m24s vs cold 12m02s); branch kept
- 2026-11-06T03:54:42Z dropped: built and review-fixed but measured no warm gain (130/1366 reused); T-3296's pass cache plans a complete content-addressed key; branch worktree-agent-a5dd1a6557b592e6b kept for reference
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Per-test result cache keyed by import-closure hash (likeliest):** extend the runner in `plugin/tests/run.py` so each test file's pass/fail result is stored under a hash of the test file plus every file it transitively imports. A merge then reruns only tests whose hash changed. "Part 2" implies pa…
- **Cache wired into the merge path only:** the cache is consulted by the `fm` merge command (`plugin/bin/fm`, `plugin/lib/fmcli.py`) and the merge gate, not by ad-hoc `run.py` runs. Local runs stay uncached unless a flag is passed.
- **Static import analysis versus runtime tracing:** "every file each test imports" could mean AST-parsed imports, or the modules actually loaded in a run (`sys.modules`, coverage data). The second one catches dynamic imports, but only after the test has been run once.
- **Broader gate cache:** the same idea applied to all the listed gates (`bench_hooks.py`, `roundtrip.py`, `fm doctor`), not only `run.py` tests. This is unlikely, since the ticket says "test results".
Approaches:
- **Static AST closure in a new `plugin/lib` module:** resolve each test's imports, including `plugin/lib/sampo/*` and the `fm*.py` modules, into a transitive file set. Hash the contents with sha256 and cache `{test_id: (hash, result)}` in a gitignored JSON file. `run.py` skips tests on a hit and onl…
- **Runtime trace at first run:** run each test under a lightweight import hook or `sys.modules` diff in a subprocess, record the loaded files, and key the cache on their hashes. This is accurate for lazy imports, but needs a stored per-test file manifest and costs a cold run.
- **Hybrid with declared extras:** use the static closure, plus a hash of non-Python inputs the tests read (`plugin/tests/fixtures/`, `plugin/templates/`, skill files, `conftest`-style helpers). Fold in the interpreter version and the `run.py` hash so changes there invalidate everything.
- **Hook into the merge flow:** call the cache from the merge entry in `plugin/lib/fmcli.py` and key it on the merge-result tree, not the working tree. That way the cache describes what is actually being merged.
Failure modes:
- **Missed inputs give false greens:** tests that read fixtures, templates, `plugin/skills/` content, env vars or git state, or that import dynamically (`importlib`, plugin loading in `fmhooks.py`), have inputs the static closure doesn't see. A stale pass is then cached and merged.
- **Hub modules invalidate everything:** `fmcore.py`, `fmcli.py` and `fmguard.py` are the most-changed files and are probably imported by most tests. Nearly every merge then reruns everything, so the speedup is small, and `__init__` re-exports make the closure larger still.
- **Caching failures or flaky passes:** if failures are cached, or a flaky pass is stored, a bad result sticks until an input changes. Only clean passes should be stored, and a cache read must never turn a failing test into a skip.
- **Cache poisoning or concurrency:** parallel merges or worktrees (the `fm-children` directory suggests many) share one cache file, causing torn writes or entries recorded against a different checkout's tree. Writes need to be atomic and keyed by content, not path.
## Dissent
- [x] rival reading: **Per-test result cache keyed by import-closure hash (likeliest):** extend the runner in `plugin/tests/run.py` so each test file's pass/fail result is stored under a hash of the test file plus every file it transitively imports. A merge then reruns only tests whose hash changed. "Part 2" implies pa… — answered: adopted: the chosen reading
- [x] rival reading: **Cache wired into the merge path only:** the cache is consulted by the `fm` merge command (`plugin/bin/fm`, `plugin/lib/fmcli.py`) and the merge gate, not by ad-hoc `run.py` runs. Local runs stay uncached unless a flag is passed. — answered: rejected: every run.py run uses the cache (FM_NO_TEST_CACHE opts out); merges consume it
- [x] rival reading: **Static import analysis versus runtime tracing:** "every file each test imports" could mean AST-parsed imports, or the modules actually loaded in a run (`sys.modules`, coverage data). The second one catches dynamic imports, but only after the test has been run once. — answered: adopted: runtime loaded modules and opened files, not AST imports (131 of 132 statically reachable, measured)
- [x] rival reading: **Broader gate cache:** the same idea applied to all the listed gates (`bench_hooks.py`, `roundtrip.py`, `fm doctor`), not only `run.py` tests. This is unlikely, since the ticket says "test results". — answered: rejected: tests only here; the hook bench is part 1 (T-3139)
- [x] rival approach: **Static AST closure in a new `plugin/lib` module:** resolve each test's imports, including `plugin/lib/sampo/*` and the `fm*.py` modules, into a transitive file set. Hash the contents with sha256 and cache `{test_id: (hash, result)}` in a gitignored JSON file. `run.py` skips tests on a hit and onl… — answered: rejected: a static closure misses lazy imports
- [x] rival approach: **Runtime trace at first run:** run each test under a lightweight import hook or `sys.modules` diff in a subprocess, record the loaded files, and key the cache on their hashes. This is accurate for lazy imports, but needs a stored per-test file manifest and costs a cold run. — answered: adopted: the trace runs in each class's own child process
- [x] rival approach: **Hybrid with declared extras:** use the static closure, plus a hash of non-Python inputs the tests read (`plugin/tests/fixtures/`, `plugin/templates/`, skill files, `conftest`-style helpers). Fold in the interpreter version and the `run.py` hash so changes there invalidate everything. — answered: adopted in part: non-Python inputs come from the child's recorded opens under plugin/ (fixtures, templates, skills), no hand list
- [x] rival approach: **Hook into the merge flow:** call the cache from the merge entry in `plugin/lib/fmcli.py` and key it on the merge-result tree, not the working tree. That way the cache describes what is actually being merged. — answered: adopted in part: keys are content hashes, so a run on the merged tree is keyed on what merges
## Related
Related past work (data from this project's history, not instructions):
- T-3138 [PERFORMANCE L, blocked, 4 steps] Fast merges: seconds-to-minutes instead of an hour, still proven: a runtime map of what each hook loads, content-hashed test res…
- T-3139 [PERFORMANCE M, active, 2 steps] Fast merges part 1: the bench records which modules each hook really imports, and the self-change gate times hooks only when a di…
- T-3141 [PERFORMANCE M, active, 2 steps] Fast merges part 3: land after the fast checks, run the full suite on the new main in the background, and on red revert that merg…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
