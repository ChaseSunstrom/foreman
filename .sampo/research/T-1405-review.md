**Verdict:** approve with nits. I found no CRITICAL or HIGH defect. I read the code and tests in the worktree and ran nothing, because the tools I had can't run `git show` or execute code.

## lens: adversary
- MEDIUM — fmcli.py:1316-1334 — `_live_gits` only counts a process whose `comm` is exactly `git` and whose `/proc/PID/cwd` is under `realpath(root)`. Three live holders are missed, so their lock can be deleted. Any one of them needs a lock older than 10 minutes, for example a hung hook or an open commit editor.
  - (a) A git in a container with the repo bind-mounted: its cwd reads as `/workspace`, not the host path.
  - (b) A client using libgit2, JGit or gitoxide in-process, where `comm` is the client's name.
  - (c) `GIT_DIR=<root>/.git git …` run from an unrelated cwd.
  - Fix: compare the lock's `(st_dev, st_ino)` against `os.stat(f"/proc/{pid}/fd/{n}")` for every process and every fd. That check is namespace-independent and `comm`-independent. Treat an unreadable fd directory as "may hold it". Keep the cwd scan as a second signal. Confidence: medium.
- LOW — fmcli.py:1355-1359 — The `_stale_index_lock` check-then-act has a gap between the `getmtime`, the `/proc` scan and `os.remove`. If the old holder finishes and a new git takes the lock in that gap, the new lock is deleted. Fix: record `st_ino` and `st_mtime_ns` before the scan, `os.stat` again just before removing, and abort if they changed. Confidence: high that the gap exists, low that it is ever hit.
- LOW — fmcli.py:6113-6141 — A verb killed by SIGTERM, SIGKILL or a timeout skips `finally`, so its empty `check-<pid>.txt` stays. A legitimate run past 15 minutes (`fm code`, `fm bench`, long `fm check`) leaves a non-empty dump every time. I found no pruning of `logs/stacks`; `fmtidy.py:610` rotates only `hooks.log`. Fix: have `_stack_dumps` delete empty files whose pid is dead, and have tidy prune old files. Confidence: high.

I read the linked-worktree and `GIT_DIR` handling and found it correct, so there is no finding. `git -C root rev-parse --git-path index.lock` gives the per-worktree lock. `_commit_task` runs git with the same environment, so the path matches the lock git complained about.

## lens: edge
- MEDIUM — fmcli.py:1324-1329 — The `except PermissionError: cwd = root` also covers the `comm` read. Under `hidepid=1`, every other-user process, such as pid 1, therefore counts as a live git. The lock is then never removed, and the message lists unrelated pids as "git is still running". Under `hidepid=2` other users' processes are absent from `listdir`, so their git is silently missed. Fix: keep unreadable processes in a separate list and report them as "couldn't inspect pid N". Document that `hidepid=2` is a known gap. Confidence: high for `hidepid=1`.
- LOW — fmdoctor.py:927-953 — The probe only proves exclusion between processes on one host, so it can't show that "NFS protects nothing". NFS flock emulated with POSIX locks would PASS. A child that dies at once gives "couldn't take a lock in 10s", which is the wrong message. A `.lock-probe-<pid>` file also stays if doctor is SIGKILLed. Fix: soften the FAIL text and report the child's exit separately. Confidence: medium.

## lens: maintainer
- LOW — plugin/tests/test_crash_hygiene.py:98-104 — The tests cover only `comm=git` with cwd equal to the repo. Nothing covers a cwd in a subdirectory, an unreadable `/proc` entry, a linked worktree or a non-`git` holder. Add at least the subdirectory and `PermissionError` cases. Confidence: high.

## Acceptance criteria
- Part 1, stack dumps: met. Tests cover SIGUSR1, the timeout, no empty file left, and short verbs installing nothing.
- Part 2, stale lock: met for the plain case. It is removed only when over 600 s old, no live `git` is found, and never without `/proc`. The gaps above are listed as findings.
- Part 3, lock probe: met. It forks a child holding the flock and checks the parent is refused; the tests cover both PASS and FAIL.

## Implicit decisions
- `faulthandler.register` without `chain` replaces SIGUSR1's default terminate action. A stray SIGUSR1 now dumps instead of killing fm.
- The 600 s age and 900 s default are hard-coded; only the 900 s default can be overridden.
- Unreadable `/proc` entries count as a live git.
- The lock path comes from `rev-parse --git-path`, run with the inherited `GIT_*` environment, not the scrubbed `c._git` one.
- The lock removal is logged as an `index_lock_removed` ledger event.
- Dump files are named `<verb>-<pid>.txt`.

## Not checked
- MASTER.md text, because the matching line was too long to display.
- Behaviour on a real container, `hidepid` mount or NFS.
- Whether git keeps the lock fd open during hooks. The fd-based fix depends on it.

**Noticed:** `fm check`/`fm code` leave a dump file on every run past 15 minutes. Whether that noise is wanted is a separate decision.
