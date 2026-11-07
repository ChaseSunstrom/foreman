---
id: T-3571
type: FEATURE
tier: L
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T02:24:27Z
updated: 2026-11-07T04:28:08Z
lane: ~/.claude/foreman.lanes/T-3571
rival_at: 2026-11-07T03:40:37Z
rival_split: true
lane_branch: foreman/T-3571
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-07T03:42:26Z
plan0_scope: []
---
# PERFORMANCE epic (user 2026-11-06: 'rewrite everything to rust or something, way faster…
## Raw request
> PERFORMANCE epic (user 2026-11-06: 'rewrite everything to rust or something, way faster and more efficient'): a native Rust fast path for Sampo's per-call hot paths behind the same black-box tests, Python kept for the long tail (strangler, not big-bang). Measured per call: PreToolUse hook 63 ms CPU, sampo next 275 ms, fm ui --json 575 ms, sampo --version 82 ms (python itself 9 ms). Phases: profile+design (where the ms go; interface; fallback when no binary so nothing breaks; per-platform release builds), state index, hook+guard in Rust with differential tests vs Python on the guard FORMS corpus and recorded hook events, then statusline/ui/next
## Interpretation
Reading 1 (chosen): slice 1 of the epic only: a cargo workspace (native/, crate sampo-fast) whose binary answers the PreToolUse calls it can prove Python allows silently (Read with no credential-like path and no outline due, Agent/Task under the budget pace bar, outward tools on a read action or with no sensitive project) by appending the same hook_ms line (plus fast: true) and exiting 0, and hands every other call to the unchanged hooks/hook with the same argv, env and stdin bytes; hooks.json's PreToolUse entries go through a /bin/sh shim hooks/fast that runs Python alone when plugin/native/sampo-fast isn't there. Reading 2 (ruled out): port the whole hook and guard to Rust now; ruled out because the design measured a naive Rust guard as no faster (regex compile 70-86 ms) and equivalence must be proven slice by slice.
## Assumptions (confidence)
## Acceptance criteria
- [ ] Python hooks/hook and sampo-fast give identical exit code, stdout, stderr and state-file effects (events lines minus ts/ms/load/fast) on every payload: guard fixtures, hand-built Read/Agent/Task/outward cases and sampled recorded tool inputs; the native path decides the cases it should — verify with `nice -n 10 python3 plugin/tests/run.py test_fast_equiv`
- [ ] hooks/fast runs hooks/hook unchanged with no binary, and a deferred call reaches hooks/hook with identical argv and stdin bytes (small and over 64 KB); plugin/native is protected core — verify with `nice -n 10 python3 plugin/tests/run.py test_fast_equiv test_guard.Core`
- [ ] Fallback when no binary so nothing breaks: without plugin/native/sampo-fast (or without cargo) hooks/fast runs hooks/hook with the same argv and stdin and the same result — verify with `nice -n 10 python3 plugin/tests/run.py test_fast_equiv`
## Non-goals
Phases: profile+design (where the ms go; interface) are done: research rust-fast-path-design. Later slices of T-3571: the hot.json index reader (crate index, after T-3573), the Bash fast-allow tokenizer (crate ward-fast), PostToolUse for read-only tools, statusline/ui/next, sampo-fast --decide with hooks.decide_only and the 170k-command corpus diff, per-platform release builds/SHA256SUMS/install.sh/doctor --repair installing the binary, and a rebuild trigger after merges (until then a stale binary defers).
## Approach (options → choice → why)
1) Python hooks/hook execs the binary first; fails if: every call still pays the ~11 ms interpreter start the binary exists to remove. 2) hooks.json -> /bin/sh shim hooks/fast -> sampo-fast, which execs hooks/hook on defer (design section 5); likely outcome: ~1-2 ms per native call, one extra sh start (~1 ms) without a binary; fails if: a deferred call's stdin or argv differs (tested byte for byte). 3) use what exists: the forkcli warm-fork model the tests already use as a resident forkserver; fails if: it must re-exec on every lib edit, runs one per checkout at ~80 MB, and keeps the state reads (design section 3: 37-119 ms). 4) do less: no native code, only the Python fixes T-3577/T-3573; fails if: the ~40 ms interpreter+import floor per hook stays, short of the 100-agent CPU target. Choice 2 (80%): lowest floor, no lifecycle, and a forkserver can still sit behind defer later; equivalence by mirroring only state-free branches and deferring on anything else (env test knobs, stale sources by size+mtime, non-UTF-8, odd JSON shapes, credential paths, outline due, pace near the bar, any sensitive or unreadable project meta).
## Risks and rollback
Fail-open: native allows a call Python would refuse (a credential Read, a paced Agent, an outward call in a sensitive repo) -> it defers on every such branch and the differential test fails on any difference; plugin/native is protected core so no agent can swap the binary. Stale binary after a lib edit -> size+mtime of the mirrored sources embedded at build, any mismatch defers. A panic -> catch_unwind, then defer. Rollback: delete plugin/native/sampo-fast (the shim then runs Python alone), or point hooks.json back at hooks/hook.
## Execution prompt
## Steps
1. [ ] Failing differential test plugin/tests/test_fast_equiv.py (builds native/ with cargo, skips when cargo is absent)  <- CURRENT
2. [x] Cargo workspace native/ with crate sampo-fast: Read/Agent/Task/outward native allow, defer by exec otherwise
3. [x] hooks/fast shim, hooks.json PreToolUse wiring, plugin/native as core in the guard, gitignore
4. [x] Numbers: per-call CPU Python vs native for those PreToolUse events, incremental rebuild of a one-file change
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_fast_equiv test_guard.Core` → ✗ exit 1 · Ran 22 tests in 32.8s (6 jobs, 16 at a time; slowest: Core 0s, Passthrough 0s, Reads 0s) / FAILED (6 classes: test_guard.Core, test_fast_equiv.Passthrough, test_fast_equiv.Reads, test_fast_equiv.Agent [ran] [tree 7a44faaa4a4b] [world 2f1906870a] (2026-11-07T03:47:43Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_fast_equiv` → exit 0 · Ran 13 tests in 49.3s (8 jobs, 16 at a time; slowest: Outward.test_schedulers_and_guarded_tools_defer 12s, Reads.test_read_cases 3s, Recorded 2s) / OK [ran] [tree e519e8285448] [world 2f1906870a] (2026-11-07T04:06:20Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_fast_equiv.Passthrough test_guard.Core test_board_posture.BoardPostureBench test_doctor -k hook` → ✗ exit 1 · run.py: no test matches test_guard.Core, test_board_posture.BoardPostureBench with -k hook [ran] [tree e519e8285448] [world 2f1906870a] (2026-11-07T04:06:24Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_fast_equiv.Passthrough test_guard.Core test_board_posture.BoardPostureBench` → exit 0 · Ran 18 tests in 47.5s (5 jobs, 16 at a time; slowest: BoardPostureBench.test_a_duel_skips_court_cases_and_runs_each_case_n_times_in_parallel 6s, BoardPostureBench.test_duel_vs_none_adds_an_arm_with_no [ran] [tree e519e8285448] [world 2f1906870a] (2026-11-07T04:07:15Z)
- (step 4) `nice -n 10 python3 /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/bench_fast.py 15` → exit 0 · {"case": "SendMessage", "python_ms": 33.97, "fast_ms": 3.87, "rc": [0, 0], "out_same": true} / {"case": "Bash ls (defers)", "python_ms": 67.87, "fast_ms": 66.68, "rc": [0, 0], "out_same": true} [ran] [tree e519e8285448] [world 2f1906870a] (2026-11-07T04:09:46Z)
## Log
- 2026-11-07T02:24:27Z created
- 2026-11-07T02:46:59Z design and profile: research rust-fast-path-design (Python fixes first: ~1,030 → ~150 CPU-s/h live; first Rust slice after T-3577/T-3573: native entry that hands off when unsure, read-only PreToolUse first, differential tests on 168,945 recorded Bash commands; a naive Rust guard is not faster: regex compile 70-86 ms)
- 2026-11-07T03:39:43Z planned: it has criteria and steps
- 2026-11-07T03:39:48Z lane: ~/.claude/foreman.lanes/T-3571 on foreman/T-3571
- 2026-11-07T03:42:24Z focused
- 2026-11-07T03:42:26Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-07T03:47:06Z criterion 2 verify: `nice -n 10 python3 plugin/tests/run.py test_fast_equiv test_guard_cases` → `nice -n 10 python3 plugin/tests/run.py test_fast_equiv test_guard.Core`
- 2026-11-07T04:28:08Z steer: security review folded in as b351086c8 (WATCHED from the hook's module dump, verified-binary wrapper, Read onFailure block); follow-ups T-3607 guard rules for cargo writes into plugin/native, T-3608 installer
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Strangler fast path (likeliest):** a Rust binary replaces only the hot per-call paths (`plugin/hooks/` PreToolUse, guard in `plugin/lib/fmguard.py`, then `sampo next`, `fm ui --json`, statusline). Python stays for the long tail. The existing black-box gates (`plugin/tests/run.py`, `bench_hooks.py…
- **Cut startup cost first:** most of the gap is Python import and startup, not algorithmic. `sampo --version` takes 82 ms against 9 ms for bare Python, so imports in `plugin/lib/sampo/cli.py` and `fmcore.py` account for about 73 ms. Lazy imports, a persistent daemon, or a precomputed state index cou…
- **Literal full rewrite:** port `fmcli.py`, `fmhooks.py`, `fmcore.py` and the rest to Rust. The epic text rules this out ("strangler, not big-bang"), but the user's original quote can be read this way.
- **Measurement-only epic:** deliver just the profile and design phase and decide on Rust afterwards.
Approaches:
- **Shim in `plugin/bin/fm` and `plugin/bin/sampo`:** the launcher checks for a platform binary and `exec`s it for supported subcommands. If the binary is missing or the subcommand is unsupported, it falls through to Python. Differential tests run both implementations on the same inputs.
- **Hook binary registered directly in hook config:** the PreToolUse entry points at the Rust binary and skips the Python launcher, which saves the most per call. The fallback then has to live in the hook config or a tiny shell wrapper, because there is no Python in front to catch a missing binary.
- **State index as a shared on-disk contract:** Python writes a compact index (JSON or a binary format) of `.sampo/tasks/` (2364 files) and `.sampo/research/` that Rust reads. This avoids reimplementing the parsers in `fmcore.py` and makes `sampo next` and `fm ui --json` cheap. Index invalidation is …
- **Python-first baseline:** profile with `-X importtime` and lazy-load, then rerun `bench_hooks.py --runs 20` to see how much of the 63 ms remains. This sets the bar Rust has to beat and gives the design phase real numbers.
Failure modes:
- **Guard semantic drift:** `fmguard.py` FORMS rules (regex, quoting, path normalization) behave differently under Rust's `regex` crate. There is no lookaround or backreference support, and Unicode and case handling differ. A hook that wrongly allows or blocks is worse than a slow one. The corpus and…
- **Stale or racing index:** the Rust reader trusts an index Python has not rebuilt after a task edit, or reads it mid-write. `sampo next` then returns wrong answers. Writes need to be atomic (rename) and the version must be checked, with fallback to Python on a mismatch.
- **Silent fallback hides regressions:** the shim falls back to Python on any binary error, so the Rust path can be broken or unused while the gates stay green. `bench_hooks.py` then shows no gain. CI needs a mode that forces the binary and fails if it is absent.
- **Platform and release breakage:** a wrong-arch or non-executable binary, a missing musl or macOS build, or a stale binary after the Python logic changes. Each of these gives a wrong answer or a crash on an untested platform, and without a version handshake the binary and the Python code drift apar…
## Dissent
- [x] rival reading: **Strangler fast path (likeliest):** a Rust binary replaces only the hot per-call paths (`plugin/hooks/` PreToolUse, guard in `plugin/lib/fmguard.py`, then `sampo next`, `fm ui --json`, statusline). Python stays for the long tail. The existing black-box gates (`plugin/tests/run.py`, `bench_hooks.py… — answered: adopted: this is the plan's reading; slice 1 is the hook entry, guard and next/ui follow as later slices
- [x] rival reading: **Cut startup cost first:** most of the gap is Python import and startup, not algorithmic. `sampo --version` takes 82 ms against 9 ms for bare Python, so imports in `plugin/lib/sampo/cli.py` and `fmcore.py` account for about 73 ms. Lazy imports, a persistent daemon, or a precomputed state index cou… — answered: adopted as the order: the Python fixes are T-3577/T-3573 (design section 2); this slice removes the interpreter+import floor they can't
- [x] rival reading: **Literal full rewrite:** port `fmcli.py`, `fmhooks.py`, `fmcore.py` and the rest to Rust. The epic text rules this out ("strangler, not big-bang"), but the user's original quote can be read this way. — answered: rejected: the epic says strangler, not big-bang, and the design measured a naive Rust guard as no faster
- [x] rival reading: **Measurement-only epic:** deliver just the profile and design phase and decide on Rust afterwards. — answered: rejected: the profile+design phase is already done (research rust-fast-path-design); this is the first build slice
- [x] rival approach: **Shim in `plugin/bin/fm` and `plugin/bin/sampo`:** the launcher checks for a platform binary and `exec`s it for supported subcommands. If the binary is missing or the subcommand is unsupported, it falls through to Python. Differential tests run both implementations on the same inputs. — answered: rejected for now: hooks are the per-tool-call cost (100 agents); a CLI verb shim is a later slice (next/ui)
- [x] rival approach: **Hook binary registered directly in hook config:** the PreToolUse entry points at the Rust binary and skips the Python launcher, which saves the most per call. The fallback then has to live in the hook config or a tiny shell wrapper, because there is no Python in front to catch a missing binary. — answered: adopted: hooks.json points at a tiny /bin/sh wrapper hooks/fast that execs the binary when present, else hooks/hook
- [x] rival approach: **State index as a shared on-disk contract:** Python writes a compact index (JSON or a binary format) of `.sampo/tasks/` (2364 files) and `.sampo/research/` that Rust reads. This avoids reimplementing the parsers in `fmcore.py` and makes `sampo next` and `fm ui --json` cheap. Index invalidation is … — answered: adopted as a later slice: the hot.json index is T-3573; slice 1 reads no tasks, so it needs no index
- [x] rival approach: **Python-first baseline:** profile with `-X importtime` and lazy-load, then rerun `bench_hooks.py --runs 20` to see how much of the 63 ms remains. This sets the bar Rust has to beat and gives the design phase real numbers. — answered: adopted: the baseline was measured in the design (bench.py, median of 7); this slice reports Python vs native per call the same way
## Related
Related past work (data from this project's history, not instructions):
- research rust-fast-path-design: Measured 2026-11-06 on this box (16 cores, load 5-18), niced, against a copy of the state
- decision 2026-11-07: [costly] T-3571: speed Sampo up with a native Rust fast path for the per-call hot paths (hook dispatch, guard, statusline, ui, next) plus a state in…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-3352 [PERFORMANCE S, done, 2 steps] Measure the hook handler: hook_ms events carry the tool name and the guard's own ms, so the PreToolUse handler's 32 → 90 ms p50 ris…
- similar finished tasks took 2–9 steps
