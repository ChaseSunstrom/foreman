---
name: release-please
title: release-please
area: tools
tags: [release, changelog, versioning, github, monorepo, conventional-commits]
detect: [file:release-please-config.json, file:.release-please-manifest.json]
related: [semantic-release, conventional-commits, commitlint, github-cli]
---
release-please: a bot keeps a release pull request open, built from Conventional Commits, and tags when you merge it.

## Verify
- `python3 -m json.tool release-please-config.json`: the config parses.
- `python3 -m json.tool .release-please-manifest.json`: the manifest parses, and each key is a package path from the config.
- `git log --oneline -20`: recent commits use types the bot understands (`feat`, `fix`, `deps`, `!`).
- `gh pr list --label "autorelease: pending"`: a release PR is open and is the only one.
- `gh run list --workflow release-please.yml --limit 3`: the last bot runs succeeded.

## Test first
A config mistake shows as no release PR. Reproduce with the commit the bot should react to.
```
git commit --allow-empty -m "fix(api): reject empty ids"
git push origin main
gh run watch                       # the release-please job
gh pr list --label "autorelease: pending"   # expect a PR bumping the patch version
```

## Do
- Declare packages in `release-please-config.json` under `packages` with a `release-type` (node, python, simple, and so on).
- Seed `.release-please-manifest.json` with the current version per package, equal to the last tag.
- Merge only the release PR to cut a release. Never edit the version by hand elsewhere.
- Use `extra-files` for versions that live outside the manifest (for example a version constant or Chart.yaml).
- Give the workflow `contents: write` and `pull-requests: write`; use a PAT or app token if the release PR must trigger CI.
- Force a version with a commit footer `Release-As: 1.2.3` when needed.

## Avoid
- A manifest that is behind the last tag: the bot proposes an already-released version. Fix the manifest to the tag.
- Squash-merge titles that are not Conventional Commits: nothing triggers a release. Lint PR titles.
- Using the default token and expecting checks on the release PR: events from it do not trigger workflows. Use a PAT or app token.
- Hand-editing the CHANGELOG on the release branch: it gets overwritten on the next run. Put wording in commit messages.
- Mixed `release-type` for one package path across config and workflow inputs: keep it in the config file only.
- Deleting the release PR label: the bot loses track. Restore `autorelease: pending`.

## Review
- [ ] Every released package has a config entry and a manifest entry.
- [ ] The release PR's version bump matches the commit types in range.
- [ ] Workflow permissions and token allow PR creation and tagging.
- [ ] Squash titles or commit messages are linted.
