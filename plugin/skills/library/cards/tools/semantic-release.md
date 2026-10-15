---
name: semantic-release
title: semantic-release
area: tools
tags: [release, versioning, changelog, npm, ci, conventional-commits]
detect: [file:.releaserc*, file:release.config.*, dep:semantic-release]
related: [conventional-commits, commitlint, release-please, github-cli]
---
semantic-release: CI derives the next version from Conventional Commit messages, then tags, publishes and writes notes.

## Verify
- `npx semantic-release --dry-run`: what version and notes the next release would produce, with no publish (needs a branch it releases from and a token in CI).
- `npx semantic-release --dry-run --no-ci`: the same run from a local machine.
- `git log --oneline $(git describe --tags --abbrev=0)..HEAD`: the commits since the last tag that the analyzer will read.
- `node -e "console.log(JSON.stringify(require('./.releaserc.json')))"`: the config parses (when it is JSON).

## Test first
Reproduce the unwanted or missing release as a dry run.
```
git checkout -b scratch main
git commit --allow-empty -m "fix: handle empty input"
npx semantic-release --dry-run --no-ci --branches scratch
# expect: "The next release version is X.Y.(Z+1)"
```
A `chore:` commit must yield "no new version".

## Do
- Release from protected branches only, set in `branches`, with prerelease channels (`next`, `beta`) declared explicitly.
- Order plugins: commit-analyzer, release-notes-generator, changelog, npm or other publisher, git, then github.
- Give the git plugin the files it commits (`CHANGELOG.md`, `package.json`) and a `[skip ci]` message.
- Check out with full history in CI (`fetch-depth: 0`), so tags are visible.
- Give CI a token that can push to the branch and create releases; for npm provenance, grant the id-token permission.
- Enforce the message format with `commitlint` so the analyzer sees valid types.

## Avoid
- Shallow clones: the analyzer sees no tags and proposes 1.0.0. Fetch full history and tags.
- Hand-bumping the version in package.json: semantic-release owns it. Remove manual edits.
- Mixing `fix:` and `feat!:` in squash merges with a wrong title: the squash title is the commit that counts. Validate PR titles.
- Running on a pull request event: it should run on push to a release branch only.
- Expecting `chore:` or `docs:` to release: add a releaseRules entry only if you want that.
- Reusing the default GITHUB_TOKEN with a branch protection that blocks it: use a token or app that is allowed to push.

## Review
- [ ] `--dry-run` output matches the intended bump for the merged commits.
- [ ] The branches list matches the real release branches, including prerelease channels.
- [ ] The workflow checks out with full history and has write permissions for contents.
- [ ] Commit-message linting runs before merge.
