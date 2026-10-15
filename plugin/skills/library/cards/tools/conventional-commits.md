---
name: conventional-commits
title: Conventional Commits
area: tools
tags: [commits, changelog, semver, git, release, commitlint]
detect: [file:commitlint.config.js, file:.commitlintrc*, file:cliff.toml, file:.releaserc*]
related: [git, pre-commit, github-cli, git-rebase]
---
Conventional Commits: `type(scope): subject` messages that drive changelogs and semantic version bumps.

## Verify
- `git log --format=%s origin/main..HEAD`: every subject on the branch matches the format.
- `npx commitlint --from origin/main --to HEAD`: if commitlint is configured, all commits pass.
- `git log -1 --format=%B`: the body and footers (`BREAKING CHANGE:`, `Refs:`) are well formed.

## Test first
Practice check: lint a bad message and a good one before committing.
```sh
echo "updated stuff" | npx commitlint            # must fail
echo "fix(parser): reject empty input" | npx commitlint   # must pass
```
Without commitlint, a grep in CI works: `grep -Eq '^(feat|fix|docs|refactor|test|chore|perf|build|ci)(\(.+\))?!?: .+'`.

## Do
- Format: `type(optional-scope): imperative subject`, subject at most about 72 characters, no trailing period.
- `feat` is a minor bump, `fix` is a patch, a `!` after the type or a `BREAKING CHANGE:` footer is a major.
- Use the other types for what they say: `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
- Explain why in the body, wrapped, separated by a blank line.
- Put issue links in footers (`Refs: #12`, `Closes: #12`).
- One logical change per commit so the type is truthful; split mixed commits.
- Squash-merge flows: make the pull request title the conventional message.
- Enforce in a `commit-msg` hook and again in CI.

## Avoid
- `fix:` for a feature or `chore:` for behavior changes: releases and changelogs lie. Pick the type by user-visible effect.
- Hiding a breaking change in the body without `!` or the `BREAKING CHANGE:` footer: no major bump happens. Add the marker.
- Capitalized or past-tense subjects ("Fixed bug"): inconsistent with tooling. Use "fix: handle empty input".
- Vague subjects ("update", "wip"): useless in a changelog. Name the change.
- Scopes invented per commit: changelog groups fragment. Keep a short list in the lint config.
- Lowercase `breaking change:` footer: the spec token is uppercase.

## Review
- [ ] Every commit or the squash title parses as a conventional commit.
- [ ] Breaking changes are marked.
- [ ] Types match the real change; scopes come from the agreed list.
- [ ] The enforcement hook and CI check agree.
