**Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower.

**Findings** (all traced by reading code; none executed)

1. **MEDIUM** — `plugin/lib/fmcore.py:1635-1643` (`regen_views`). It writes `STATE.md`, `INBOX.md`, `state.line`, `badge.txt` and `status.json` into the shared `p.dir` from the lane-filtered `state_dict`.
   - Trigger: any `mutate`, `checkpoint` or `fm focus` in lane L overwrites those files with L's view.
   - Effect: the main session's statusline (`status.json`), the foreman-ui chip and `fm watch` then show L's active task until main next writes. This is the "one side sees the other's task" case the brief asks about.
   - Fix: write per-lane view files (e.g. `status.<laneslug>.json`) or skip the shared files when `p.lane` is set. Test: focus a task in the main checkout and a lane, then read `status.json`.
   - Confidence: high.

2. **MEDIUM** — `plugin/lib/fmsync.py:40` (`<p.root>/.foreman`) with `regen_views` at `fmcore.py:1644`. With `sync` on, `p.root` is the lane worktree, so the export goes into the lane's own `.foreman`, which is a branch-point copy of the repo mirror. The import at `fmsync.py:150-172` reads that stale copy as "theirs". The task's `.foreman` is also swept into `task finish --commit` (`fmcli.py:373`). Result: two diverging mirrors and possible conflicts or reverts. Fix: use the main worktree root for sync. Confidence: medium (I did not read the merge logic).

3. **MEDIUM** — `plugin/lib/fmlanes.py:385-388`. `git worktree remove` without `--force` deletes ignored files without any warning (`.env`, `node_modules`, build output), and the `status --porcelain` guard doesn't list ignored files. This breaks the "never discards" promise in the CHANGELOG and docs. Fix: check `git status --porcelain --ignored` or `git clean -ndx`, and refuse or warn. Confidence: high.

4. **MEDIUM** — `fmlanes.py:380-388`, lane folder deleted by hand. `rm` skips the remove, never runs `git worktree prune`, and `branch -d` then fails because the stale registration still holds the branch. That reports "kept: not merged" falsely. A later `fm lane new` for the same task fails in `git worktree add` with "missing but already registered". Fix: run `worktree prune` before `branch -d`. Confidence: high on the git behaviour.

5. **LOW** — `fmlanes.py:344-349`. `lane list` shows only tasks whose lane path is in `git worktree list`. A task holding a hand-deleted lane is held forever by `held_elsewhere` (`fmcore.py:1529`), and `cmd_focus` (`fmcli.py:626`) tells the user to run `fm lane list`, where it doesn't appear. It shows only under `state.lanes`. Fix: list orphans in `lane list` as "missing".

6. **LOW** — `fmhooks.py:752`. The committed-fmcore fallback calls `cc.active_brief(cc.load_briefs(p))` without the lane. Once HEAD contains lane support, the main checkout's active task authorizes edits in a lane whenever the working fmcore is broken. Fix: pass `getattr(p, "lane", None)`.

7. **LOW** — `fmcli.py:15` (`SETTABLE_STATUS`). `fm task set ID status=active` bypasses lane and held checks, so two active tasks can end up in one checkout. `fm task finish` and `done` don't verify that the task belongs to this lane.

8. **LOW** — Tests. `test_lanes.py` covers none of these, and no test checks any hook besides the edit gate: auto-evidence, Stop/drive, scope notes in a lane, `find_project` for a submodule, a registered worktree or `GIT_DIR`, hand-deleted lane folders, or the `held_elsewhere` cases (planned, blocked).

**Acceptance criteria**
- Lane resolution, per-lane focus, queue skip, edit gate and the lane commit: met per `test_lanes.py`, which I did not run. The view-file overwrite in finding 1 is not covered.
- `lane new`, `list` and `rm`: met for the happy path. `rm` refuses uncommitted tracked or untracked work but not ignored files (finding 3).
- `fm check`: not verified.

**Lens results**
- intent: changes needed. The request was parallelism; this delivers isolation only (`fm run --parallel` is deferred), and the shared view files make the "each side sees only its own" claim leak (1).
- adversary: ok. `rm` and `new` take paths from state and git, and `git worktree remove` only removes registered worktrees. Residual: 6 and 7.
- edge: changes needed (4, 5; submodules and bare repos return None cleanly; git older than 2.31 degrades silently).
- operator: changes needed (3 and 2: sync and discard behaviour don't match the docs).
- maintainer: approve with nits. Tests are thin (8), and `lanes[...]` is built inline in `state_dict`.

**Pre-audit:** `fmhooks.py` needs no `test_hooks` change beyond the gap in finding 8. `fmwatch.py` needs no mod edit unless the UI should show lanes.

**Not checked**
- I did not run the tests.
- I did not read the `fmsync` merge details.
- I did not check `fmtidy` or `fmdoctor` behaviour with lane-held tasks.
