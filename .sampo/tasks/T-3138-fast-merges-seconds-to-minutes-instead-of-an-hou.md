---
id: T-3138
type: PERFORMANCE
tier: L
status: blocked
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T04:53:13Z
updated: 2026-11-05T04:57:16Z
rival_at: 2026-11-05T04:56:49Z
rival_split: true
group: fast merges and merge trains
---
# Fast merges: seconds-to-minutes instead of an hour, still proven: a runtime map of what each hook loads, content-hashed test results with impact analysis, land-then-verify with automatic revert, and parallel checks in separate processes
## Raw request
> Fast merges: seconds-to-minutes instead of an hour, still proven: a runtime map of what each hook loads, content-hashed test results with impact analysis, land-then-verify with automatic revert, and parallel checks in separate processes
## Interpretation
The user (2026-11-05): 'feel free to invent/make new tech to make it so merges can happen very very quickly without the almost hour of verifications and such, but still making sure everything works, and multiple merges at the same time', after 'what about merges in parallel', 'make sure it isnt bottlenecked by the python GIL'. Reading 1 (chosen): a merge is seconds of git and minutes of proof (the self-change gate's three bench pairs, then each close's full suite); make the proof incremental and parallel without weakening it: (1) a runtime map of the modules each hook actually imports (recorded by the bench, not the static 131-of-132 closure), so the timing bench runs only when a diff touches them; (2) test results cached by a hash of every file each test loads (recorded per test), so a merge runs only tests whose inputs changed; (3) land after the fast checks, run the full suite on the new main in the background, and on red revert that merge commit automatically and reopen its lane (bisecting a train); (4) T-3119's parallel checks, one process per lane. Reading 2: only parallelism; rejected, N lanes at an hour each in parallel still take an hour each.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a typical finished lane (the last 10 merged, replayed) merges in under 2 minutes from start to main moved, with the same checks deciding: the bench where a hook loads a changed module, every test whose inputs changed — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] a lane that turns main red after landing is reverted automatically and its lane reopened with the failing test named, within the background suite's run — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] five finished lanes merge with their checks running at the same time in separate processes, total time under 1.5x one lane's — verify with `python3 plugin/tests/run.py test_lanes`
- [ ] measured, not self-tested: a replay of the last 10 real merges through the new path, timed start to main moved, before and after, with every check that ran named, filed in research — verify with `test -f ~/.claude/foreman/state/projects/foreman-4a056f/research/T-3138-merge-speed.md`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: bench_hooks (add a sys.modules dump per hook), run.py (per-test import capture and a result cache), lanes.merge and the red_after_merge cause (revert and reopen), T-3119's train; likely outcome: a typical lane lands in under 2 minutes, the suite runs after, red is reverted within its run. 2. Do less: only the test cache; fails if: the bench's three pairs still cost minutes per merge. 3. Skip checks for small diffs; fails if: 'still making sure everything works' is the user's condition. Choice 1 (75%)
## Risks and rollback
Risks: (1) the test cache reuses a stale pass: an input it didn't record changed (a subprocess import, an env value, a data file); mitigated by the subprocess recorder, the env and python version in the key, and the uncached drift check that turns the cache off per class on any mismatch. (2) land-then-verify leaves main red for one suite's run; mitigated by verify-before-land while any verify is red, and an automatic revert of exactly that merge commit. (3) the hook map misses a module a hook loads only on some input; mitigated by the union over runs, refresh on change, and timing as today when the map is stale. (4) a revert conflicts with merges stacked on it; it stops and is marked for the main thread, never forced. Rollback: each part has a switch (FM_NO_TEST_CACHE, the gate times every lane when the map file is absent, lane merge --verify-first restores verify-before-land); reverting a part's merge commit restores today's path.
## Execution prompt
## Steps
1. [ ] part 1: the runtime hook map and the bench skip  <- CURRENT
2. [ ] part 2: the content-hashed test cache and impact selection
3. [ ] part 3: land then verify, auto-revert and reopen
4. [ ] part 4: parallel checks and trains (T-3119)
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-05T04:53:13Z created
- 2026-11-05T04:53:32Z set approved=True
- 2026-11-05T04:55:39Z plan review adopted (all six): a red verify stops further land-then-verify and a revert re-queues stacked verifies (T-3141); subprocess imports, python version and env join the cache key, with an uncached drift check (T-3140); measured criterion (a replay of the last 10 merges, in research); a bench lock keeps timing benches apart while other checks run in parallel (T-3119); the hook map is a union refreshed on change (T-3139); order: T-3139, then T-3141 (the safety net), then T-3140 (the cache), then T-3119
- 2026-11-05T04:57:05Z blocked: umbrella: parts T-3139 (building), T-3141 (building), then T-3140 and T-3119
## Follow-ups captured
## Build vs reuse
Reuses bench_hooks (a sys.modules dump per hook run), plugin/tests/run.py (per-test import capture, the result cache beside its existing class sharding), lanes.merge with its red_after_merge stop cause, T-3131's every-pair gate, T-3119's train; new: the hook module map, the test input-hash cache, the post-land suite with revert.
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Land-then-verify with a background suite means main is red (broken) for the whole suite duration, and other lanes merging in that window build on or rebase onto a bad commit. Auto-revert then has to handle later merges stacked on top (conflicts, dependent commits), and the revert itself is an…
- HIGH: The content-hash cache and impact analysis are only sound if the recorded inputs are complete. Runtime import capture misses data files, fixtures, subprocess-spawned code, env/config, git state, Python version, and conditionally imported modules (a different path in the new code may import a …
- HIGH: Acceptance criteria don't prove the request. All three are "verify with `test_lanes`", which is a suite the plan itself modifies, and the first is "last 10 merged, replayed", which depends on historical data that may not be replayable (those lanes' inputs may not exist). No criterion checks s…
- MEDIUM: The "1.5x one lane's time" criterion for five parallel lanes may be unachievable or flaky: CPU core count, I/O, shared git index/locks, and the timing bench itself (which is sensitive to contention and gives noisy results when run in parallel) all interfere. Parallel runs make the bench's t…
- MEDIUM: The bench skip rule ("runs only when a diff touches a loaded module") relies on the same runtime map, which is recorded on one machine/config. Hooks that load different modules depending on input or environment will be recorded only for the exercised path. Record the map across all hook eve…
- LOW: Step ordering delivers value late: the auto-revert (part 3) is the safety net that makes the cache's risk acceptable, yet it comes after the cache (part 2). Consider building the revert-on-red and the periodic uncached full run before turning on skipping, or ship the cache in shadow mode (comp…
Verdict: revise — the direction is sound, but the plan needs a concurrency/failure protocol for land-then-verify, completeness guarantees (and a drift check) for the cache's inputs, and acceptance criteria that tes…
## Dissent
- [x] HIGH: Land-then-verify with a background suite means main is red (broken) for the whole suite duration, and other lanes merging in that window build on or rebase onto a bad commit. Auto-revert then has to handle later merges stacked on top (conflicts, dependent commits), and the revert itself is an… — answered: adopted: the chosen reading; the gate sequence named is what each part shortens
- [x] HIGH: The content-hash cache and impact analysis are only sound if the recorded inputs are complete. Runtime import capture misses data files, fixtures, subprocess-spawned code, env/config, git state, Python version, and conditionally imported modules (a different path in the new code may import a … — answered: rejected as the whole: the cache alone leaves the bench's minutes per merge (part 1) and the serial wait (part 4)
- [x] HIGH: Acceptance criteria don't prove the request. All three are "verify with `test_lanes`", which is a suite the plan itself modifies, and the first is "last 10 merged, replayed", which depends on historical data that may not be replayable (those lanes' inputs may not exist). No criterion checks s… — answered: rejected as the whole: land-then-verify without the cache still runs the full suite per merge, only later
- [x] MEDIUM: The "1.5x one lane's time" criterion for five parallel lanes may be unachievable or flaky: CPU core count, I/O, shared git index/locks, and the timing bench itself (which is sensitive to contention and gives noisy results when run in parallel) all interfere. Parallel runs make the bench's t… — answered: rejected as a standalone: the hook map exists to skip the timing bench (part 1), not as its own feature
- [x] MEDIUM: The bench skip rule ("runs only when a diff touches a loaded module") relies on the same runtime map, which is recorded on one machine/config. Hooks that load different modules depending on input or environment will be recorded only for the exercised path. Record the map across all hook eve… — answered: adopted: runtime tracing (sys.modules and an audit hook on open) for hooks and tests, never settrace (too slow)
- [x] LOW: Step ordering delivers value late: the auto-revert (part 3) is the safety net that makes the cache's risk acceptable, yet it comes after the cache (part 2). Consider building the revert-on-red and the periodic uncached full run before turning on skipping, or ship the cache in shadow mode (comp… — answered: adopted: a fast tier (affected and cached tests, the gate) blocks the merge, the full tier runs after landing (part 3)
- [x] rival reading: **Merge pipeline speedup (likeliest):** the ~1h gate sequence (`fm doctor`, `plugin/tests/run.py`, `e2e/roundtrip.py`, `bench_hooks.py --runs 20`, `claude plugin test mods/foreman-ui`, `fm replay`) is cut to seconds-to-minutes by running only impacted checks, caching by content hash, and verifying … — answered: adopted: part 3's detached verifier records the merge sha and reverts with git revert -m 1
- [x] rival reading: **Cache and impact analysis only:** the core ask is the content-hashed result store plus the tests→sources map (the "tests → sources" section of the project map, e.g. `test_agents.py → fmagents.py`). Land-then-verify and parallelism are secondary or later work. — answered: adopted: any unmapped file or missing trace falls back to the full check (over-select, never trust a gap)
- [x] rival reading: **Land-then-verify only:** the merge path in `plugin/lib/fmcli.py` is changed so merges go in immediately and the gates run afterwards, with auto-revert on failure. Speed comes from moving the gates off the critical path, not from making them faster. — answered: rejected as the whole: land-then-verify without the cache still runs the full suite per merge, only later
- [x] rival reading: **Runtime hook map as a standalone feature:** "what each hook loads" is its own deliverable, a traced import/file-read map of `plugin/lib/fmhooks.py` and `plugin/hooks/` that feeds impact analysis. It is not tied to the merge path. — answered: rejected as a standalone: the hook map exists to skip the timing bench (part 1)
- [x] rival approach: **Trace-based dependency map:** run each hook and test under an import/file-open tracer (`sys.settrace`, `sys.addaudithook`, or `-X importtime`). Write the observed set to a map file keyed by HEAD. Hash the contents of those files to form the cache key, and a test reruns only if a hash it touched c… — answered: adopted: runtime tracing (sys.modules and an audit hook on open) for hooks and tests, never settrace
- [x] rival approach: **Tiered gate runner in `plugin/tests/run.py`:** split the gates into a fast impacted tier that blocks the merge and a full tier (`roundtrip.py`, `bench_hooks.py`, `fm replay`, `foreman-ui`) that runs after landing. Run the tiers as separate subprocesses with a worker pool, each writing a result re… — answered: adopted: a fast tier (affected and cached tests, the gate) blocks the merge, the full tier runs after landing (part 3)
- [x] rival approach: **Land-then-verify via a post-merge verifier:** the merge command in `fmcli.py` fast-forwards, records the pre-merge SHA, and spawns a detached verifier. On failure it runs `git revert` or a reset to the recorded SHA and writes a notice. `fmguard.py` would hold a lock so later merges queue behind o… — answered: adopted: part 3's detached verifier records the merge sha and reverts with git revert -m 1
- [x] rival approach: **Fallback on cache miss:** an unmapped file or a missing trace triggers the full suite. Safety comes from over-selection rather than trusting the map. — answered: adopted: an unmapped file or a missing trace falls back to the full check
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Merge pipeline speedup (likeliest):** the ~1h gate sequence (`fm doctor`, `plugin/tests/run.py`, `e2e/roundtrip.py`, `bench_hooks.py --runs 20`, `claude plugin test mods/foreman-ui`, `fm replay`) is cut to seconds-to-minutes by running only impacted checks, caching by content hash, and verifying …
- **Cache and impact analysis only:** the core ask is the content-hashed result store plus the tests→sources map (the "tests → sources" section of the project map, e.g. `test_agents.py → fmagents.py`). Land-then-verify and parallelism are secondary or later work.
- **Land-then-verify only:** the merge path in `plugin/lib/fmcli.py` is changed so merges go in immediately and the gates run afterwards, with auto-revert on failure. Speed comes from moving the gates off the critical path, not from making them faster.
- **Runtime hook map as a standalone feature:** "what each hook loads" is its own deliverable, a traced import/file-read map of `plugin/lib/fmhooks.py` and `plugin/hooks/` that feeds impact analysis. It is not tied to the merge path.
Approaches:
- **Trace-based dependency map:** run each hook and test under an import/file-open tracer (`sys.settrace`, `sys.addaudithook`, or `-X importtime`). Write the observed set to a map file keyed by HEAD. Hash the contents of those files to form the cache key, and a test reruns only if a hash it touched c…
- **Tiered gate runner in `plugin/tests/run.py`:** split the gates into a fast impacted tier that blocks the merge and a full tier (`roundtrip.py`, `bench_hooks.py`, `fm replay`, `foreman-ui`) that runs after landing. Run the tiers as separate subprocesses with a worker pool, each writing a result re…
- **Land-then-verify via a post-merge verifier:** the merge command in `fmcli.py` fast-forwards, records the pre-merge SHA, and spawns a detached verifier. On failure it runs `git revert` or a reset to the recorded SHA and writes a notice. `fmguard.py` would hold a lock so later merges queue behind o…
- **Fallback on cache miss:** an unmapped file or a missing trace triggers the full suite. Safety comes from over-selection rather than trusting the map.
Failure modes:
- **Incomplete runtime map:** the trace only records the paths a given run exercised. Conditionally loaded files in `plugin/skills/` (1396 files) or data and config read through dynamic paths never enter a test's hash set. A change to one is declared "no impact" and a real regression lands unverified.
- **Non-hermetic test results:** `bench_hooks.py` (timing), `fm replay`, and `roundtrip.py` depend on the clock, environment, `~/.claude` state, or ports. Caching them by source hash returns stale passes, and running them in parallel processes creates port, temp-dir or state collisions and flaky fail…
- **Unsafe auto-revert:** while verification runs, further merges land on top. Reverting the bad commit then conflicts or silently drops dependent work. Hot files (`fmcore.py`, `fmcli.py`, `CHANGELOG.md`, `MASTER.md`) make this likely, and the project is not a git repo here, so a rollback path that a…
- **Weakened "still proven" claim:** if the gates that remain blocking (impacted tests only) are not a superset of what can break, the guarantee degrades into "proven eventually". Exposure during the unverified window, such as other agents or users pulling a broken HEAD, is then not accounted for.
