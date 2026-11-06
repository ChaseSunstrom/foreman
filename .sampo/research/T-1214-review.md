**Verdict: changes needed.** The judge works for the tested cases, but several simple moves get past it.

## lens: adversary
- HIGH — fmcode.py:129-138 — The tree is judged once, right after the turn. `run_bounded` kills only the process group. A worker that runs `setsid nohup sh -c 'sleep 5; printf "#!/bin/sh\n..." > .git/hooks/pre-commit; chmod +x ...' &` outlives the kill and plants the hook after `judge`. The hook then runs on the harness's own `fm task finish` commit, which has the full environment. The `run_bounded` docstring ("nothing it started in the background outlives it") is false, and the test only covers a same-group `sleep &`. Fix: run `judge` again just before `_finish`, and ideally after verify, or confine the worker to a PID namespace or cgroup. — high
- HIGH — fmcode.py:241-243,541 — `worker_env()` strips credentials from the worker, but `fm task evidence --run` runs the verify with `self.env()`, which keeps `GITHUB_TOKEN`, `AWS_*` and the rest. The guard checks only the verify command string. A worker that edits `test_calc.py` (an allowed file) to POST `os.environ` gets the withheld credentials when the verify runs. Fix: run the verify with `worker_env()` when `run.worker` is set. — high
- HIGH — fmcode.py:165 — Only newly ignored names (`_ignored(root) - ignored`) are judged. Anything already ignored is unwatched: an overwritten `.env` (the guard calls it "credentials"), `.venv/…/sitecustomize.py`, `node_modules`, `__pycache__/*.pyc`. The verify then runs that planted code. Fix: snapshot and compare ignored files too, at least credential-named files and the interpreter/venv folders. — high
- HIGH — fmcode.py:160,219 — `git update-index --assume-unchanged` (or `--skip-worktree`) on a tracked file, then an edit, leaves `git status` clean, so the judge never sees the change. Fix: clear those flags (or compare against `git ls-files -v`) before `_dirty`. — high
- HIGH — fmcode.py:152,245-247 — `_put` and `os.remove` are unguarded. A worker that plants a hook and runs `chmod 555 .git/hooks` makes the restore raise PermissionError. `cmd_code` catches only CodeError, ModelError and Blocked, so it crashes with the hook still in place and the remaining files unjudged. Fix: catch OSError per file, and Block the task listing what could not be reverted. — high
- HIGH — fmcode.py:766 — With `--worker --verify`, `offsite_ok` is never called, so a repo marked sensitive is sent to a remote CLI (`claude`, `codex`). The README promises "only a model on this machine". Fix: refuse `--worker` in a sensitive repo unless the user's own template is used. — high
- MEDIUM — fmcode.py:129 — Ctrl-C or an exception during `run_bounded` skips `judge`. `--resume` then snapshots the planted state as its baseline. Fix: put `judge` in a `finally`. — high
- MEDIUM — fmcode.py:146 — A user's `.git/hooks -> ~/.githooks` symlink is deleted after every turn, on the assumption it was planted. Fix: compare against the snapshot's link state. — medium
- MEDIUM — fmcode.py:303-304,165 — `_expand` returns on the first overflow and skips later entries. A newly ignored `aaa/` with 301 files stops the walk before a hidden `.github/workflows/x.yml` is looked at. Separately, a first `node_modules/` or `target/` build creates over 300 changed files, so everything is reverted, including the worker's real fix. Only 301 of the new files are deleted, so the folder is left half-removed. Fix: judge a folder as one unit and don't return early. — high
- MEDIUM — fmcode.py:154-158 — If the run started on a detached HEAD, a worker's `git switch other` is followed by `reset --soft <sha>`, which moves `other`'s tip. Fix: restore detached HEAD with `checkout --detach`. — medium
- LOW — fmcode.py:104-105 — The credential filter is a denylist and fails open: `PGPASSWORD`, `STRIPE_API_KEY` and `MYSQL_PWD` all survive. Fix: use an allowlist. — high

**What still escapes:**
- Everything outside the repo: `~/.gitconfig`, which the harness's own `git status` and commit then honour; Foreman state; and the guard files.
- Reads: `.env` and `~/.ssh` can be read and sent out over the network.
- Pre-existing uncommitted work, which is snapshotted but never restored.
- Submodule config and hooks under `.git/modules` (a lead, not proven).
- The worker editing the verify target itself, such as `test_calc.py`.

## lens: intent / operator
- LOW — fmcli.py:45 — `--worker` help lists `opencode` as a preset, but `WORKERS` has no such entry. `opencode <prompt>` would start the TUI and hang until the timeout. Fix: drop `opencode` from the help text. — high
- LOW — README.md:33, CHANGELOG, MASTER.md — "none is let run shell commands on its own say" is wrong for `codex --full-auto`, which runs commands inside its sandbox. Fix: reword. — high
- LOW — fmcode.py:803,378 — `msgs =[`, and the approach string lost a space after "):". — high

## Acceptance criteria
- Fake CLI fixes the bug: met (test 1).
- Fake CLI edits a protected file, reverted and reported: met for the in-repo, non-ignored, in-turn case (tests 2 and 9).
- Hanging CLI killed at the timeout: met (test 3).
- Missing CLI gives a one-line error: met (test 4).
- The harness's verify decides, never the worker's claim: partly met. Test 5 covers a worker that claims success without changing anything. The findings above show how a worker can steer or poison the verify.

## Implicit decisions
- Judging is done by `git status`, not by an OS sandbox.
- Credentials are filtered by name.
- `fm code` makes no new commits of its own beyond `fm task finish`.
- A turn that touches more than 300 files is reverted whole.
- `escalate` stays model-only.

## Not checked
- Whether the tests pass. I could not run them, so I could not explain why `test_a_worker_gets_no_forge…` expects `OPENAI_API_KEY=[REDACTED]
- `site/pages.py` against `test_docs` and `stats.json`.
- The pre-audit "secret-looking" hit: I read it as test fixtures and dismissed it.

**Noticed:**
- `_snapshot` reads every dirty file fully into memory, so a huge untracked file can exhaust RAM.
- A worker's `git stash` or `git clean` on the user's pre-existing dirty files is never undone.
