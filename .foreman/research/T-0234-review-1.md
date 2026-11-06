**Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose only. I read the diff and the code it calls but did not run any tests.

## Findings

**MEDIUM — `~/.claude/foreman/plugin/lib/fmlanes.py:138-139,152` — `remove()` deletes whatever branch the worktree is on.**
- The branch name now comes from `git branch --show-current` in the lane, and `branch -d` runs against it.
- Trigger, in the main checkout's current state (`foreman/build` is checked out there and `main` is not):
  1. A lane, or a builder that broke contract item 5 ("never switch branches"), runs `git switch main`.
  2. `fm lane rm ID` removes the worktree first, so the branch is no longer checked out anywhere else.
  3. `git branch -d main` succeeds when `main` is merged into the main checkout's HEAD.
- `fm tidy --apply` reaches the same code through `stale()` at line 176.
- Only merged branches go, so no commits are lost. But the user's `main` or any other merged branch is deleted without being asked.
- Fix: delete only a branch that is `foreman/{b.id}` or a harness builder prefix. Never delete a branch named `main`, `master` or the default branch. Otherwise report it as kept. Add a test that switches the lane to another merged branch and checks it survives `rm`.
- Confidence: high on the code path. I did not run the exploit.

**MEDIUM — contract item 5 and `builder_brief` — nothing stops a builder from closing its own task, so it can self-authorize.**
- The only barrier is the sentence "never close the task".
- An S task needs only a self audit (`fmcli.py:449-450`, `:484`). The builder can run `fm task finish ID --audit "ok" --commit "…"` from its worktree.
- On an M task it can pass `--lens "intent: ok" --lens "edge: ok"`. Those strings are self-supplied, and `fm task audit` (`fmcli.py:330-335`) accepts any lens.
- The task then closes with no independent review, which defeats the main-thread review that delegate.md step 3 depends on.
- Fix: refuse `task done`, `finish` and `audit` when the active lane is a builder worktree. For example, key off `meta["builder"]` plus `p.lane` set, and require a flag only the main thread can pass. At minimum, add a guard rule and a test for it.
- Confidence: high that no enforcement exists. I grepped the hooks and the finish/done paths and found nothing builder-aware.

**MEDIUM — `~/.claude/foreman/plugin/lib/fmhooks.py:1139-1143` and `fmlanes.py:99` — "nothing outside its worktree" is not enforced.**
- Edit and Write by absolute path to the main checkout, to another worktree or to files under `~/.claude` are only logged as `touched`. Scope violations are only a note (`fmhooks.py:1035-1049`).
- The guard's `_under` and `project_root_for` do path checks, but nothing confines edits to `p.lane`.
- The builder can edit the main checkout while it is in use, and the merge review would never see those edits.
- Fix: in the PreToolUse edit check, when `p.lane` is set and a builder is flagged, block paths outside `p.lane`. Use `realpath`, so symlinks and `..` are covered.
- Confidence: medium-high. I did not read the whole guard.

**LOW — `fmlanes.py:99,121` — a builder slot leaks.**
- `meta["builder"]` is never cleared except by closing the task.
- The failed-builder flow in delegate.md step 4 is `fm lane rm`, then "work it in the main thread". Until that task closes, it still counts toward the two-builder cap.
- If the task is abandoned but not dropped, the slot is lost permanently.
- Fix: `take_back` in `remove()` should pop `builder`. A task that is briefed but never launched needs the same.

**LOW — `fmlanes.py:138` — branch cleanup is incomplete in two cases.**
- When `os.path.isdir(path)` is false (the folder was deleted by hand), `branch` falls back to `foreman/{id}`, so a builder's branch is never deleted.
- A detached HEAD does the same.
- Both fail safe, but they leave stray branches.

**LOW — `~/.claude/foreman/plugin/tests/test_builder.py:279-297` — test gaps.**
- The Flow test checks only that the branch is deleted after a merge.
- It does not check that an unmerged builder branch is kept, that a different or default branch survives, or that a builder cannot close its task.

## Acceptance criteria
- **Agent file with Edit/Write/Bash and a lane-only contract:** met as text. The tools line and the contract are present, but the contract is not enforced (see findings 2 and 3).
- **`fm lane brief` — refuses an L task, a held or active task, or a third builder, and prints the Agent call:** met. The checks are at `fmlanes.py:91-101` and the Agent call is built at `:124`.
- **Flow works end to end in a linked worktree:** met for the happy path. The `focus`/`held`/`rm`/`focus` sequence follows `fmcli.py:1002-1009`.
- **delegate.md documents when to use a builder and how to review, merge, re-verify and close:** met (the new sections in the diff).

## Not checked
- I did not run the test suite.
- I did not read the rest of `fmguard.py` or `fmbudget`.
- I did not check how Claude Code's worktree isolation names branches or where it places worktrees, for example inside the repo.
- I did not check the `fm tidy` interaction beyond `stale()`.
