**Verdict: approve with nits** (one MEDIUM to fix before merge).

**Findings**

1. MEDIUM — `plugin/lib/fmtidy.py:134` (called from `fmtidy.py:178` and `fmcost.py:355`) — Run from a lane (linked worktree), `p.root` is the worktree path. `find_project` returns `Project(m.slug, gr, m.dir, lane=gr)`, which pairs the project's state with the worktree's files. A worktree's files all carry the mtime of the checkout, and that is later than any older brief's `updated`. Scenario: `fm tidy` or `fm digest` inside a lane marks every planned brief that has a scope file as "X changed since it was planned". The task's own docstring admits this for fresh clones. Fix: resolve the root with `c.main_view(p).root` (fmcore.py:2716, which exists for this) at the top of `stale_plan`, or skip the mtime check when `p.lane` is set. A same-path re-clone has the same problem. `unblocked()` has it too, but this change adds the second copy.
2. LOW — `fmtidy.py:141` — The "is gone" check runs a `git log -1 -- <path>` subprocess for every missing scope path of every planned brief, on each tidy and digest run. Missing paths are the normal case when a plan creates the file. Git has to walk the whole history to prove a never-seen path has no match. On a large repo that could hit the 2 s timeout in `c._git`, which returns "" and so silently reports nothing. I couldn't run anything here (no Bash), and the task recorded no before/after timing. Fix: memoize per path across briefs within a run. Also consider `git ls-tree HEAD -- s` (tracked in HEAD but absent on disk) as the cheap test.
3. LOW — `fmtidy.py:133` — `save_brief` sets `updated` on every write (`fmcore.py:1478`). Any Foreman write to a planned brief therefore clears staleness without anyone re-reading the plan. That is a false negative, not a false positive. The fix hint `fm task set {b.id} …` is not a command anyone can copy and run. Name a real acknowledgement, such as `fm task log ID "plan re-read: still valid"`, and check that the log write bumps `updated`.
4. LOW — Feature reach: in the volt project, the planned briefs I sampled all have `scope: []`, so the mtime and gone checks never run there. Only the dropped-dependency check does.

**Lens verdicts**
- Intent: approve.
- Adversary: approve. The scope is `realpath`-confined to the project root, globs are skipped, and `--` guards the git call.
- Edge: changes needed for finding 1. Missing `updated` is handled, and directories and new files are skipped.
- Operator: approve with nits (findings 2 and 3).
- Maintainer: approve. The helper is small and reuses `parse_ts` and `c._git`. The `ponytail:` comment states the mtime ceiling.

**Acceptance criteria**
- A planned brief whose scope file is newer than `updated` appears in `fm digest` and `fm tidy`, and a fresh one doesn't: met by the code and by `StalePlans.test_a_scope_file_newer…`. The test passed per the brief's evidence. I did not re-run it.
- `fm tidy --apply` never acts on these items: met. The finding is `warn` with `auto=False`, and no `apply` branch or action is added. `cmd_tidy` prints it as DECIDE.

**Implicit decisions**
- Staleness is judged by mtime against `updated`, not by git history.
- Only `planned` status is checked.
- A missing scope file counts as "gone" only if git has history for it. Globs, directories and paths outside the root are ignored.
- The first reason found wins, so there is one reason per brief.
- Tidy emits one finding per brief. Digest caps its line at 5 and puts all of them in JSON `stale_plans`.

**Not checked**
- Timing, because there is no shell here.
- The full test suite.
- Whether `fm relate` or `fm batch` rewrite planned briefs.

**Noticed:**
- `fmtidy.unblocked` (fmtidy.py:118) has the same lane and fresh-clone mtime false positive as finding 1. It needs its own task.
- Add a test for `stale_plan` run from a lane worktree.
