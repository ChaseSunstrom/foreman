---
name: git-worktrees
title: Git worktrees
area: tools
tags: [git, worktree, branches, parallel, isolation, builds]
detect: []
related: [git, git-bisect, git-rebase]
---
Git worktrees give several branches checked out at once in separate directories sharing one repository.

## Verify
- `git worktree list`: every checkout, its path, head and branch.
- `git worktree prune --dry-run -v`: stale entries for deleted directories.
- `git -C ../wt-fix status --short`: the worktree has the state you expect.
- `git branch --show-current`: which branch this directory has.

## Test first
Practice check: prove isolation by reproducing the failure in a clean checkout.
```sh
git worktree add ../wt-repro -b repro/issue-42 origin/main
cd ../wt-repro && make test      # fails here = not caused by your uncommitted edits
```
A test that fails only in your main checkout points at local state, not the commit.

## Do
- Create with `git worktree add PATH -b NEW BASE`; place worktrees outside the repo directory.
- Use one for reviews, hotfixes, or a long build while you keep working in the main tree.
- Use `git worktree add --detach PATH SHA` for inspecting a commit with no branch.
- Remove with `git worktree remove PATH`; add `--force` only for a dirty tree you have inspected.
- Run `git worktree prune` after deleting a directory by hand.
- Lock a worktree on removable media with `git worktree lock PATH`.
- Install dependencies per worktree; build output and `node_modules` are not shared.

## Avoid
- Checking out the same branch in two worktrees: git refuses. Create a new branch or use `--detach`.
- `rm -rf` on a worktree directory: it leaves stale metadata. Use `git worktree remove` or prune.
- Placing a worktree inside the main work tree: the main repo sees it as untracked content. Put it next to the repo.
- Assuming the working directory and index are shared: each has its own. Stash does not move between them, but the stash list does.
- Leaving a worktree on a deleted branch: later `gc` or branch deletion surprises you. Remove it with its branch.
- Submodules in a worktree without `git submodule update --init`: they are empty.

## Review
- [ ] Each worktree has its own branch and a purpose.
- [ ] No uncommitted work is lost when a worktree is removed.
- [ ] `git worktree list` shows no stale or prunable entries.
- [ ] Per-worktree dependencies and env files are set up.
