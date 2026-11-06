## Verdict: changes needed

## Findings

**HIGH — `~/.claude/foreman/plugin/lib/fmsync.py:57-65` (`_walk`) and `:47-49` (`_read`), reached from `incoming()` (:213-217) and `import_()` (:143-210)** — `_walk` filters out symlinks but not other non-regular dirents (FIFO, socket, device node); anything under `.foreman/` matching `*.md` that isn't a plain file is still yielded. `_read` then does a plain blocking `open(path).read()` with no type check. `incoming()`'s size guard (`os.path.getsize(...) <= MAX_IMPORT`) does not protect against this: `getsize` on a FIFO returns 0, so it passes the check and `_read` still blocks forever waiting for a writer.
Trigger: `mkfifo .foreman/tasks/T-9999-x.md` in a synced project, then run any `fm` command or start a session. `fmcli.py:786-801` (`_sync_in`, called from every `fm` command dispatch at `fmcli.py:1070`) and `fmhooks.py:152-165` (`_sync_import`, called from `session_start` at `fmhooks.py:135-144` **inside** `c.lock(p.dir, timeout=LOCK_QUICK)`) both call `fmsync.incoming`/`import_` unconditionally when sync is on. The SessionStart path holds the project lock while it hangs, so every subsequent `fm` command / guard hook that needs the same lock also stalls or times out — effectively a project-wide DOS from one stray non-regular file.
This is exactly the failure class the brief calls out ("non-regular files hanging a reader") and that round 9 already fixed for `fm audit prep`'s research-file walk (`fmcli.py:711`, `os.path.isfile(...) and not os.path.islink(...)`); that fix was never applied to `fmsync._walk`/`_read`, so a narrower per-round review of round 9 (audit prep) or of the earlier `fm sync` round would not have caught this cross-round regression.
Fix: in `_walk`, only yield entries where `os.path.isfile(os.path.join(d, f))` (which already excludes FIFOs/sockets/devices), mirroring `fmcli.py:711`.
Confidence: high (read both code paths and the callers/lock context).

**MEDIUM — `~/.claude/foreman/plugin/lib/fmdoctor.py:236`** — `check_core_integrity` gates entirely on `os.path.isdir(os.path.join(home, ".git"))`. In a git worktree (which is exactly what MASTER.md §8 says Foreman's own self-improve flow uses: `improve/<date>` worktree) `.git` at the worktree root is a **file** containing `gitdir: …`, not a directory, so `isdir` is False and the check silently reports `PASS — not a git checkout: nothing to compare`, skipping the very half-applied-edit detection round 7 added. This is inconsistent with the codebase's own established convention for the same problem: `fmcore.py:240` (`git_root`) uses `os.path.exists(os.path.join(d, ".git"))`, which is worktree-safe. A per-round review of round 7 alone would see a plausible-looking git check and not notice the divergence from `fmcore.git_root`'s already-correct pattern elsewhere in the same codebase.
Fix: use `os.path.exists(...)` (or resolve `.git` via `git rev-parse --git-dir`) instead of `os.path.isdir(...)`.
Confidence: high (verified git's file-based `.git` for worktrees, and the inconsistent sibling implementation in fmcore.py).

## Other observations
- `fmsync.py` locking discipline is otherwise correct (`cmd_sync` and `_sync_in` both take `c.lock(p.dir)`); the hang above is a liveness problem, not a state-corruption one.
- `fmcore.record` (`fmcore.py:248-275`) correctly anticipates Python 3.14's lazy `__annotations__` via `getattr(cls, "__annotations__", {})`; no issue found there.
- `plugin/hooks/hook`'s `committed_library()` correctly handles missing `git`, a repo with no commits, and detached HEAD/shallow clones (all funnel into `except Exception: return False`, then fail-closed for `PreToolUse`).

## Not checked
- `fmrepeats.py`, `fmserve.py` usage-limit backoff/timezone arithmetic, `fmcli.py` evidence `--run`/`fm check` beyond what's shown above, `fmdoctor.py` footprint budget logic, and the remaining ~2900 lines of the diff (docs-only hunks were skimmed, not exhaustively verified). Concurrency between two simultaneous `fm` processes both attempting `fmsync.export`/`import_` was not traced beyond confirming both take the project lock. No commands were executed (read-only review).
