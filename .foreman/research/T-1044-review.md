**Verdict: changes needed.** There is one MEDIUM regression, and the pid-reuse guard itself is sound.

**Findings**

1. MEDIUM — `plugin/lib/fmideas.py:214-228`. `run_children` handles only `TimeoutExpired`, so a `KeyboardInterrupt` or `SIGTERM` leaves every unfinished child running.
   - **Why it's worse than before:** `_popen` now uses `start_new_session=True`, so the terminal's ^C and SIGHUP no longer reach the children. They used to die with the foreground group.
   - **Scenario:** the user hits ^C during `fm ideas` or `fm research`. Python unwinds, but N `claude -p` children keep running and spending up to their budget caps. Their registry entries stay until a later SessionStart sweeps them at least 30 minutes on (`max(max_age, timeout+60)`).
   - **Fix:** wrap the communicate loop (and the stdin-write loop) in `except BaseException: for pr, _ in procs: _reap(pr); raise`. `run_child` already does this.
   - **Confidence:** high.

2. LOW — `plugin/lib/fmideas.py:150-161`. The sweep only kills when the group leader is still alive. If the leader exits but a grandchild survives, `/proc/<pid>/cmdline` is gone, so the entry is deleted and the group is never killed.
   - **Fix:** when the leader is gone, call `killpg` only if a member of the group verifiably remains. Otherwise document the limit. Confidence: medium.

3. LOW — `plugin/lib/fmideas.py:93-101`. The sweep kills processes without recording it. The operator never learns that orphans were reaped or how many.
   - **Fix:** have `session_start` log the count when it is greater than 0. Confidence: high.

4. LOW — `plugin/lib/fmideas.py:66`. The comment "not yet waited for" is not guaranteed. A `KeyboardInterrupt` inside `communicate` runs a short `_wait` that may reap the leader. The pid is not reused while group members exist, so the window is negligible.
   - **Fix:** none needed beyond softening the comment. Confidence: low.

**Checked against the focus list, no finding**
- **Pid reuse:** both checks must pass before a kill: `/proc/<pid>/stat` field 22 (index 19) equal to the stored value, and a `--no-session-persistence` argv element. A reboot would also need the same pid and the same tick count.
- **Crafted registry:** `state_dir` is `~/.claude/foreman/state`, not repo-synced. A crafted file needs the victim's exact start time plus that flag. A same-user attacker can already kill anyway.
- **`/proc` absent:** `_popen` swallows the `OSError`, so the child is unregistered but still reaped on timeout. The sweep returns 0.
- **Concurrent sweeps:** two sweeping sessions only produce `OSError`s that are caught. The pid-recycle window is microseconds.
- **Latency and errors:** the sweep is a `listdir` plus reads of the few entries present. The `fmideas` imports are light. The hook wraps the call in `try/except`.
- **Outputs and timeouts:** these match the old `subprocess.run` path, including the message text.
- **Callers:** `fmresearch.py:238` and `child_cmd` both carry the flag, so all four helpers can be swept.

**Acceptance criteria**
- **1 (child and grandchild gone after timeout):** met. `Timeout.test_run_child_kills_the_whole_group` and `test_run_children_kills_every_group` cover it, and the task log shows `test_reaper` OK. I did not run the tests myself.
- **2 (`sweep_orphans` kills a stale helper, spares a reused pid and a fresh helper, and SessionStart survives a sweep error):** met. `Sweep` and `Hook` cover it, and `test_relate` passed in the log.

**Implicit decisions**
- Registry file format is `"<starttime> <epoch> <timeout>"`, keyed by pid.
- Orphan age threshold is 30 minutes.
- Linux `/proc` only; macOS gets no registry.
- Kill signal is SIGKILL, with no grace period.
- The sweep runs on every SessionStart unless `FOREMAN_NO_BACKGROUND` is set.
- Stale or garbled entries are deleted silently.
- `fmbench._session`'s own `claude -p` is not covered.

**Not checked:** I ran no tests (read-only), did not review the Windows path (`os.killpg` does not exist there), and did not review `fmbench`.

**Noticed:**
- `_reap`'s final `pr.communicate()` has no timeout, so a grandchild that escaped the group via `setsid` and holds the pipes would hang it. This is unchanged from before but worth a bounded wait.
- The task file still shows step 1 as "CURRENT" even though steps 2 and 3 are done.
- No test covers the ^C/`BaseException` path in `run_children`.
