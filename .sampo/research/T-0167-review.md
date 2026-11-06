**Verdict:** changes needed. One HIGH finding (a hang) and two MEDIUM ones. I traced each finding below by reading the code. I did not run any of them.

## Findings

1. **HIGH — `plugin/lib/fmserve.py:304-308, 440-463`. A failed `fm lane new` loops `fm run` forever.**
   - Trigger: two disjoint S tasks where `lane new` fails for both. A leftover `foreman/T-x` branch checked out in another worktree makes `git worktree add` fail.
   - Path: `runs` stays empty, so `_run_lanes` returns `{}`. The loop at 448 does nothing and `finished` is unchanged. A failed task is never added to `skip` (only `skip.add(tid)` at 458 does that), so `_next_runnable` returns the same head and `_batch` rebuilds the same batch.
   - Result: every iteration spawns `fm lane new` again and prints "left in the queue", with no exit.
   - Fix: `skip.add(b.id)` when lane creation fails, or add every batch id missing from the results to `skip`.
   - Confidence: high, traced.

2. **MEDIUM — `fmserve.py:272-275`. `_overlap` is a literal string-prefix compare with no path normalisation.**
   - Same file, different spellings: `"./a/x.py"` vs `"a/x.py"` gives `x.startswith(y)` False both ways, so both tasks share a batch. The same happens for an absolute path vs a relative one and for `a//x`.
   - Brace globs: `"src/{a,b}.py"` has literal prefix `src/{a,b}.py`, which does not prefix `src/a.py`.
   - Impact: the rebase conflicts and the lane is kept, so no data is lost. The cost is wasted parallel usage.
   - Fix: normalise each scope with `os.path.normpath` after stripping a leading `./`, and treat `{` as a wildcard character.
   - I did not check whether the scope matcher itself normalises these spellings.
   - Confidence: high on the spelling cases, traced.
   - Trailing slashes (`plugin/`) and `plugin/**` vs `plugin/lib/x.py` are correctly flagged as overlapping. A task with no scope is correctly excluded by `free()`.

3. **MEDIUM — `fmserve.py:309-314`. A `Popen` failure leaves started lanes running.**
   - If `claude` is missing or `Popen` raises, the exception propagates out of `_run_lanes`. Lanes already launched keep running unwaited, their temp files stay open, and the run lock is released. If `claude` is missing, the first `Popen` fails anyway, so the serial path's friendly "claude isn't on PATH" message is lost too.
   - Fix: wrap the launch and kill and wait on already-started procs on error, plus a `try/finally` around the wait loop. Catch `FileNotFoundError` and convert it to `UsageError`.
   - Confidence: high, traced.

4. **MEDIUM — `fmserve.py:309, 347, 323-324`. Several failure modes are uncaught.**
   - `fm check` in `_integrate` (3600s timeout) and `git` (600s timeout) raise `TimeoutExpired` uncaught. That aborts the loop and leaves later finished lanes unintegrated; the tasks are done but unmerged and no longer reported.
   - `TemporaryFile("w+")` decodes with the locale encoding and strict errors. Non-UTF-8 model output makes `out.read()` raise `UnicodeDecodeError`. Fix: `errors="replace"`.
   - A timed-out lane is only `proc.kill()`ed, so child processes may survive.
   - Fix: catch `SubprocessError` in `_integrate` and return a "kept" message; start lanes with `start_new_session` and kill the process group.
   - Confidence: medium-high, traced.

5. **LOW — `fmserve.py:344-346`. The rebase failure message is misleading.**
   - A rebase refused because the lane has unstaged changes is reported as "conflicts with branch". It is safe, since `lane rm` refuses dirty lanes, but the message is wrong.
   - Fix: include `stderr` in the message.
   - Confidence: medium.

6. **LOW — `fmserve.py:448-459`. A task in a parallel batch gets less than a serial task.**
   - A lane that makes progress but isn't finished is skipped, with no retry sessions (compare `SESSIONS_PER_TASK`, line 515).
   - A usage-limited lane is also skipped permanently for the rest of the run, after which `parallel=1` waits and retries only other tasks.
   - No `run_session` token ledger entry is written for lanes (line 500 is serial-only), so `fm cost` under-reports parallel usage.
   - Fix: log `run_session` per lane, and drop usage-limited tasks from `skip`.
   - Confidence: high.

## Acceptance criteria
- Two disjoint S tasks run at once, are rebased, gated and fast-forwarded, and their lanes are removed: not verifiable here. The code path exists (`_integrate`), but I did not run the tests.
- Overlapping scopes, dependencies, L tasks and dirty main never run or merge in parallel, and a kept lane says why: mostly met. Finding 2 is the hole for overlap; dirty main is covered at 339 and by `ff-only`.
- All gates pass: not run.

## Lens results
- intent: partly done. The cap of 3, the S/M-only rule and the usage-limit stop are met. Findings 1 and 6 are gaps.
- adversary: ok on merge safety. `_integrate` cannot lose commits, because `lane rm` uses `branch -d` and refuses dirty lanes. It cannot merge an unrebased or ungated branch, and `--ff-only` into the branch read at the start prevents a wrong-branch merge. Finding 2 (path spellings) is the only workaround found.
- edge: changes needed (findings 1, 3 and 4). Detached HEAD is handled at 337. A main checkout that is mid-merge or mid-rebase reads as detached or dirty and is kept.
- operator: changes needed. Finding 6 under-reports cost, and finding 1 is a hang with no timeout. I did not check the docs.
- maintainer: changes needed for lane-launch duplication. The command-building code is duplicated between 310 and 466. Share one helper.

## Not checked
- `plugin/tests/test_parallel.py`.
- The CHANGELOG and MASTER.md edits.
- The `fmcli` flag wiring.
- The scope matcher.
