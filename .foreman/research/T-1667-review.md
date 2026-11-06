**Verdict: changes needed.** One MEDIUM and one more MEDIUM-ish lead, both small to fix. I could only read files (no shell), so I did not run the tests or time doctor.

## lens: adversary
- MEDIUM — plugin/lib/fmdoctor.py:158-173 and :77-94 — The "dead pid" test is `os.kill(pid, 0)` raising ProcessLookupError, which also fires for a live holder in another PID namespace. Foreman's own notes name the Claude Code Bash sandbox, which often unshares PIDs. An `fm fsck --fix` run inside such a sandbox would see the real sentinel's or ambient run's pid as gone and delete a live `sentinel.pid` or `run.pid`. The next `_sentinel` or `fmambient.run` then starts a second run alongside it. The code comment admits a microsecond race but not this case, and the tests only use a same-namespace dead pid. Fix: in `fsck_fix`, also require the file to be old (at least 3600 s, the age `fmcli._sentinel` already treats as stale), or refuse `--fix` when `/proc/self/ns/pid` differs from the host's. — PLAUSIBLE (read-only, not run).
- LOW — fmdoctor.py:111 — `json.loads` on a 64 KB last line of `[[[[…` raises RecursionError, which is not a ValueError. `cmd_fsck` then dies with a traceback; doctor's `check_fsck` catches it. Fix: `except (ValueError, RecursionError)`.
- Cleared: symlink `.pid` files are never opened or removed (O_NOFOLLOW, and os.walk does not follow symlinked folders). FIFOs never block (O_NONBLOCK, then S_ISREG). `os.kill(0)` is avoided. A reused pid keeps the lock, which fails safe. Only `*.pid` files under the state dir are unlinked, and only two writers produce them (`sentinel.pid`, `run.pid`), both bare digits. The unlink follows an intermediate symlinked folder, but that needs write access to the state dir, which is already game over.

## lens: edge
- MEDIUM — fmdoctor.py:126-129 — This is the builder's weakest link, and it is real. A lane whose folder exists but whose `.git` file points at a pruned `.git/worktrees/<x>` passes both checks. `os.path.exists(lane/.git)` is true, and `git worktree prune` leaves the branch, so the `rev-parse` also passes. fsck reports nothing, and git fails inside that lane. The `continue` branch hides it, and no test plants this case. Fix: if `.git` is a file, parse `gitdir: <path>` and require `os.path.isdir` on it. Or run `c._git(lane, "rev-parse", "--git-dir", proc=True)` and flag returncode 128. — CONFIRMED by reading.
- LOW — fmdoctor.py:62-64 — `_tail` returns `(None, None)` on EACCES and on symlinks. An unreadable pid file or journal is skipped silently, and fsck prints "OK". Fix: report "unreadable" for EACCES, or at least count skipped files.
- LOW — fmdoctor.py:103-104 — A journal being appended at that moment (events.jsonl, written on every hook call) can show "no newline" and give a transient false positive. Fix: re-read once before reporting.

## lens: intent
- MEDIUM — fmdoctor.py:136 and 199 — fsck scans every project, but the text output prints no project, and the detail carries the hint "fm lane rm T-xxxx frees the task". Task ids repeat across projects. Run from project A, it tells you to remove T-0012 in A when the broken one is in B. Fix: print `p.slug` in the text line, and only give the `fm lane rm` hint when the project is the current one.

## Acceptance criteria
- fsck reports a broken lane, a stale lock and a torn journal, and `--fix` repairs only the lock: met by `test_reports_…` and `test_fix_removes_only_the_stale_lock` (not run). It does not cover a pruned `.git` target or other projects' lanes.
- Other projects' worktrees are never touched: met. The code only calls `isdir`/`exists` on lane paths and runs `git rev-parse` from each project's root.
- The torn-journal check reads only the last 64 KB: met (`_tail` seeks to `size-n`, and an over-long last line is not judged).
- Doctor is not noticeably slower: probably met. The walk is `endswith` on about 12.5k names with no stat, and it reads about 40 journal tails. The `git rev-parse` calls run one per open task with a lane, each with a 10 s timeout, so a hung git would cost up to 10 s per task. Not measured.

## Implicit decisions
- It scans `*.jsonl` files anywhere in state, not a named list. The skip list applies only at the state root.
- An empty pid file counts as stale after 60 s.
- Exit code 1 on any finding, including ones that `--fix` could not repair.
- Doctor reports WARN, never FAIL.

## Not checked
I did not run the tests, time doctor, or inspect the other journals in state for non-JSON last lines.

**Noticed:** none
