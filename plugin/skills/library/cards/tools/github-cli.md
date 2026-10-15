---
name: github-cli
title: GitHub CLI
area: tools
tags: [github, gh, pull-requests, actions, issues, automation]
detect: [file:.github/workflows/*.yml, file:.github/workflows/*.yaml, file:.github/CODEOWNERS]
related: [git, conventional-commits, code-review, pre-commit]
---
The `gh` CLI for pull requests, issues, Actions runs and API calls from scripts.

## Verify
- `gh auth status`: logged in, with the host and token scopes you need.
- `gh pr checks`: CI status of the current branch's pull request.
- `gh run list --limit 5`: recent workflow runs and their conclusions.
- `gh pr diff`: the diff reviewers will see.

## Test first
Practice check: a read-only call fails first when auth or scope is wrong.
```sh
gh auth status && gh repo view --json nameWithOwner -q .nameWithOwner
gh pr create --draft --fill
```
Open a draft pull request early so CI is the failing test, then push the fix.

## Do
- Create with `gh pr create --title T --body-file FILE`; a file avoids shell quoting bugs.
- Watch CI with `gh pr checks --watch` or `gh run watch RUN_ID`.
- Read failures with `gh run view RUN_ID --log-failed`.
- Use `--json FIELDS` with `-q` (jq expression) for scripts instead of parsing table output.
- Call the REST API with `gh api PATH`; add `--paginate` for lists.
- Set `GH_TOKEN` in CI; do not run `gh auth login` there.
- Merge with an explicit strategy: `gh pr merge --squash --auto`.
- Check out a pull request locally with `gh pr checkout NUMBER`.

## Avoid
- Putting a token on the command line or in the repo: use `GH_TOKEN` from secrets.
- Parsing the human table output: it changes. Use `--json`.
- Inline multi-line `--body "..."` with backticks or `$`: the shell expands them. Use `--body-file`.
- `gh pr merge` without checking `gh pr checks`: merges a red branch. Use `--auto` with branch protection.
- Forgetting `--repo OWNER/NAME` in a script run outside a clone: it targets the wrong or no repository.
- Assuming `gh api` returns all pages: add `--paginate`.
- Workflow secrets echoed in logs: never print them, and use `gh secret set` to store them.

## Review
- [ ] Pull request title and body say what and why, and link the issue.
- [ ] CI is green via `gh pr checks` before merge.
- [ ] Scripts use `--json` and set `--repo` or run from a clone.
- [ ] No tokens appear in commands, logs or committed files.
