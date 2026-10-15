---
name: git-submodules
title: Git submodules
area: tools
tags: [git, submodules, vendoring, monorepo, ci]
detect: [file:.gitmodules]
related: [git, git-lfs, git-worktrees]
---
Git submodules: a repo pins another repo at an exact commit, so updates are explicit commits in the parent.

## Verify
- `git submodule status`: each pinned commit; a leading `-` means uninitialized, `+` means the checkout differs from the pin, `U` means conflict.
- `git submodule update --init --recursive`: every submodule, nested ones included, checks out at its pinned commit.
- `git diff --submodule=log`: which commits a submodule bump pulls in.
- `git status --short`: no unexpected `M path` lines for submodules (dirty or moved pointer).
- `git config -f .gitmodules --get-regexp url`: the URLs the team will clone.

## Test first
Reproduce the fresh-clone failure before fixing the setup.
```
d=$(mktemp -d) && git clone . "$d/c" && cd "$d/c"
git submodule status        # leading "-" on every line is expected here
git submodule update --init --recursive
git submodule status        # no "-" and no "+" remain
```

## Do
- Add with `git submodule add <url> <path>` and commit both `.gitmodules` and the new gitlink.
- Clone with `git clone --recurse-submodules`, or run `git submodule update --init --recursive` after.
- Bump deliberately: `git -C path fetch && git -C path checkout <tag>`, then commit the parent with the new pointer.
- Use relative or HTTPS URLs in `.gitmodules`, so CI does not need SSH keys.
- In CI, fetch submodules in the checkout step, with the credentials the submodule host needs.
- Remove with `git submodule deinit -f path`, `git rm -f path`, and delete `.git/modules/path`.

## Avoid
- Committing inside a submodule and not pushing it: others get a pointer to a missing commit. Push the submodule first, then the parent.
- Running `git pull` and expecting submodules to move: run `git submodule update --init --recursive` afterward, or set `submodule.recurse`.
- Working in detached HEAD in the submodule and losing commits: create a branch before committing.
- Using `git add .` on a moved submodule by accident: check `git diff --submodule=log` first.
- Pointing `.gitmodules` at a developer's fork or a local path: use the canonical URL, then run `git submodule sync`.
- Using `--remote` for reproducible builds: it follows a branch tip. Pin a commit or tag.

## Review
- [ ] `.gitmodules` URL and path are right, and no credentials are in the URL.
- [ ] The pointer bump commit shows the intended log range in `git diff --submodule=log`.
- [ ] The submodule commit exists on its remote.
- [ ] CI and Dockerfiles initialize submodules recursively.
