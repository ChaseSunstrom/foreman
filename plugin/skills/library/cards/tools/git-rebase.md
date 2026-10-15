---
name: git-rebase
title: Git rebase
area: tools
tags: [git, rebase, history, squash, conflicts, autosquash]
detect: []
related: [git, git-bisect, conventional-commits]
---
Rebase to linearize and tidy unpublished history, with a recovery path ready before you start.

## Verify
- `git range-diff origin/main@{1} origin/main HEAD`: for an update after a rebase, the patches are the same apart from intended changes. Use the old and new tips you actually have.
- `git diff ORIG_HEAD HEAD --stat`: a rebase that only reordered or squashed changed no file content.
- `git log --oneline origin/main..HEAD`: the final commit list is what you intended.
- `git reflog -n 10`: the pre-rebase commit is findable if you must go back.

## Test first
Practice check: record the safety net, then prove the tree is unchanged.
```sh
git branch backup/pre-rebase          # cheap undo: git reset --hard backup/pre-rebase
git rebase -i --autosquash origin/main
git diff backup/pre-rebase HEAD       # must be empty for a pure tidy-up
```
Run the test suite after the rebase; each commit should still build (`git rebase -x "make test" origin/main`).

## Do
- Rebase only commits that nobody else has based work on.
- Create fixes with `git commit --fixup SHA`, then `git rebase -i --autosquash BASE`.
- Use `git rebase --onto NEW OLD BRANCH` to move a branch off the wrong parent.
- Resolve a conflict, `git add` the files, then `git rebase --continue`; `git rebase --abort` returns to the start.
- Enable `git config rerere.enabled true` so repeated conflicts resolve themselves.
- After rebasing a pushed branch, `git push --force-with-lease`.
- Use `git rebase --rebase-merges` to keep a merge topology you want.

## Avoid
- Rebasing `main` or any shared branch: others' clones diverge. Merge or revert.
- Plain `--force` after a rebase: it overwrites a teammate's push. Use `--force-with-lease`.
- Taking "ours" and "theirs" at face value: during a rebase they are swapped (ours is the branch being rebased onto). Read the markers.
- `git rebase -i` with `pick` lines deleted: that drops the commit silently. Use `drop` deliberately.
- Rebasing after a long review without noting it: reviewers lose context. Say so, or use fixup commits until approval.
- Squashing unrelated work into one commit to hide a mess: split with `edit` and `git reset HEAD^`.

## Review
- [ ] A backup ref or reflog entry existed before the rebase.
- [ ] Content diff versus the backup is empty, or every difference is explained.
- [ ] Tests pass at the tip and, for bisectability, at each commit.
- [ ] The push uses `--force-with-lease` to a branch you own.
- [ ] No fixup, squash or WIP commits remain.
