---
name: commitlint
title: commitlint
area: tools
tags: [commits, lint, conventional-commits, git-hooks, ci]
detect: [file:commitlint.config.*, file:.commitlintrc*, dep:@commitlint/cli]
related: [conventional-commits, semantic-release, release-please, pre-commit]
---
commitlint: checks commit messages against a rule set (usually Conventional Commits) in a git hook and in CI.

## Verify
- `echo "fix: handle empty input" | npx commitlint`: a valid message exits 0.
- `echo "fixed stuff" | npx commitlint`: an invalid message exits nonzero with named rules.
- `npx commitlint --from origin/main --to HEAD`: every commit on the branch passes.
- `npx commitlint --edit .git/COMMIT_EDITMSG`: lint the message being committed (what a commit-msg hook does).
- `npx commitlint --print-config`: the resolved rules, to check which preset applies.

## Test first
Reproduce the rejected or wrongly accepted message with stdin.
```
echo "feat(api): Add search." | npx commitlint
# with the conventional preset: subject-case and subject-full-stop errors
echo "feat(api): add search" | npx commitlint ; echo $?   # 0
```

## Do
- Extend a preset: `extends: ['@commitlint/config-conventional']` in `commitlint.config.js`.
- Restrict scopes with `scope-enum` if the repo has fixed areas, and set `body-max-line-length` for long URLs.
- Run it from a `commit-msg` hook (husky, lefthook or pre-commit) with the message file argument.
- Run it in CI on the PR range (`--from` base `--to` head), and lint the PR title if you squash-merge.
- Add `ignores` for merge and revert messages, or bot commits, as functions in config.
- Make the hook skip nothing silently, and keep the install step in `prepare` or setup docs.

## Avoid
- Checking only the last commit in CI: earlier bad commits pass. Lint the full range.
- Shallow clones in CI: `--from` fails with an unknown revision. Fetch the base branch.
- Hook installed but the config file is ESM or CJS mismatched: load error. Match `.mjs`, `.cjs` or `type` in package.json.
- Squash-merging with a free-form title after linting commits: release tooling reads the title. Lint the PR title.
- Disabling `type-enum` to allow anything: release tools then cannot choose a bump. Extend the enum instead.
- Passing the message as a CLI argument with quotes mangled: use stdin or `--edit`.

## Review
- [ ] Valid and invalid sample messages behave as expected.
- [ ] The commit-msg hook and the CI range check both exist.
- [ ] Types and scopes match what the release tooling understands.
- [ ] Merge, revert and bot commits are handled in `ignores`.
