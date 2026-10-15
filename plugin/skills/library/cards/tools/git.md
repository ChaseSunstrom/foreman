---
name: git
title: Git
area: tools
tags: [git, vcs, commits, branches, history, workflow]
detect: []
related: [git-rebase, git-bisect, git-worktrees, conventional-commits, github-cli, pre-commit]
---
Git day to day: small reviewable commits, safe history edits, and recoverable mistakes.

## Verify
- `git status --short --branch`: what is staged, unstaged, untracked, and ahead or behind.
- `git diff --cached --check`: staged changes have no whitespace errors or conflict markers.
- `git log --oneline --graph -n 15`: the history you are about to push reads sensibly.
- `git diff --stat origin/main...HEAD`: the branch touches only the files the task intended.

## Test first
Practice check: a dry run fails before you act. Preview what a command will do.
```sh
git add -n .                 # lists what would be staged; secrets or build output here = fix .gitignore first
git push --dry-run origin HEAD
git clean -nd                # preview deletions; -f only after reading the list
```
Commit a failing test as its own commit when it helps review, then the fix.

## Do
- Stage deliberately: `git add -p` to pick hunks, `git restore --staged FILE` to unstage.
- One logical change per commit; the message says why, not just what.
- Undo safely: `git restore FILE` for working tree, `git revert SHA` for published commits, `git reflog` to find lost commits.
- Fix up your own unpublished commits with `git commit --fixup SHA` then `git rebase -i --autosquash`.
- Push forced updates with `git push --force-with-lease`, never bare `--force`.
- Keep `.gitignore` for build output, env files and editor junk; keep `.gitattributes` for line endings and binary markers.
- Use `git switch -c NAME` and `git restore` instead of overloaded `git checkout`.

## Avoid
- `git add .` or `git add -A` without reading `git status`: commits secrets, logs, `node_modules`. Review with `git diff --cached`.
- `git reset --hard` or `git checkout .` to "clean up" with uncommitted work: it is unrecoverable. Stash first (`git stash push -u`).
- Rewriting history on a shared branch: teammates diverge. Revert instead.
- Committing a secret then deleting it in a later commit: it stays in history. Rotate the secret, then purge history.
- `git commit --no-verify` to get past a failing hook: fix the hook failure.
- `git pull` creating surprise merge commits: use `git pull --ff-only` or `--rebase`.
- Committing generated lockfile churn or mass reformatting with a feature: split it into its own commit.

## Review
- [ ] `git diff --cached` read in full; no secrets, debug prints or unrelated files.
- [ ] Each commit builds and passes tests on its own.
- [ ] Commit messages explain the reason and match the repo's convention.
- [ ] No force push without `--force-with-lease`, none to a protected branch.
- [ ] Large or binary files are intentional (consider LFS).
