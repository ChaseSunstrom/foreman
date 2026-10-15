---
name: git-lfs
title: Git LFS
area: tools
tags: [git, lfs, binaries, large-files, storage]
detect: [file:.lfsconfig]
related: [git, git-submodules, github-cli]
---
Git LFS: large binaries live in the LFS store and the repo keeps small pointer files, routed by .gitattributes patterns.

## Verify
- `git lfs ls-files`: which tracked files are really stored as LFS objects.
- `git lfs track`: the patterns currently routed to LFS.
- `git lfs status`: staged and unstaged files, and whether each is an LFS pointer or a raw blob.
- `git lfs fsck --pointers`: every pointer file in history parses and is well formed.
- `git check-attr filter -- path/to/file`: the file actually resolves to the lfs filter.

## Test first
Prove the pattern catches the file before committing it. A file that is not listed is committed as a plain blob.
```
git lfs track "*.psd"
git add .gitattributes assets/hero.psd
git lfs ls-files        # must list assets/hero.psd, else the pattern missed
git commit -m "add hero"
git cat-file -p HEAD:assets/hero.psd | head -3   # must show "version https://git-lfs..."
```

## Do
- Run `git lfs install` once per machine (or `--local` per repo) so the smudge and clean filters exist.
- Commit `.gitattributes` in the same commit that first adds a tracked file, and before the file.
- Track by extension or directory (`assets/**`), not by single file name.
- In CI, fetch objects explicitly (`git lfs pull`) or enable the checkout action's lfs option, then verify with `git lfs ls-files`.
- Migrate existing blobs with `git lfs migrate import --include="*.psd"` on a branch, and coordinate a force push.
- Keep a quota in mind: bandwidth and storage are billed by the host, so avoid tracking build outputs.

## Avoid
- Adding a file, then running `git lfs track`: the blob is already committed raw. Use `git lfs migrate import` to rewrite it.
- Editing `.gitattributes` by hand with a typo (`filter=lfs diff=lfs merge=lfs -text` must stay intact): use `git lfs track`.
- Shallow or sparse CI checkouts without LFS: pointer files get built into artifacts. Fetch LFS and fail the job if a file starts with "version https://git-lfs".
- Cloning with `GIT_LFS_SKIP_SMUDGE=1` and forgetting to pull: tests read pointer text. Run `git lfs pull` afterward.
- Tracking files that diff or merge as text: LFS marks them `-text`, so conflicts become whole-file choices.
- Deleting the file and assuming storage shrinks: old objects stay in history until pruned on the server.

## Review
- [ ] `.gitattributes` is committed with the patterns and nothing matches generated output.
- [ ] `git lfs ls-files` lists every large binary in the diff, and none is a raw blob.
- [ ] CI and Docker builds fetch LFS objects before they use the files.
- [ ] A history rewrite is announced, with the force-push plan stated.
