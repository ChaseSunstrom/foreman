---
name: github-actions
title: GitHub Actions
area: infra
tags: [github, actions, ci, workflows, permissions, supply-chain]
detect: [file:.github/workflows/*.yml, file:.github/workflows/*.yaml, file:.github/actions/*/action.yml]
related: [docker, gitlab-ci, circleci, terraform, kubernetes]
---
GitHub Actions workflows: least-privilege tokens, pinned actions, caching, concurrency control and safe handling of untrusted input.

## Verify
- `actionlint`: workflow syntax, expression types, shell errors and unknown action inputs.
- `yamllint .github/workflows`: YAML structure.
- `act -n`: dry-lists the jobs a local run would execute (needs `act` installed).
- `gh workflow run ci.yml --ref my-branch && gh run watch`: the workflow runs on the real runner.
- `gh run view --log-failed`: logs of failed steps only.

## Test first
The failing check is the workflow itself on a branch. Add the job and the assertion step, push, and watch it fail for the right reason.
```yaml
name: ci
on: { pull_request: {} }
permissions: { contents: read }
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test   # red until the target exists and passes
```
`actionlint` is the pre-push gate for syntax.

## Do
- Set top-level `permissions: { contents: read }` and grant more per job (`id-token: write` for OIDC, `pull-requests: write` only where needed).
- Pin third-party actions to a full commit SHA with a version comment, and let Dependabot update them.
- Add `concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }` for CI on branches.
- Use OIDC (`id-token: write` plus the cloud's login action) rather than long-lived cloud keys in secrets.
- Cache with `actions/cache` or a setup action's `cache:` input, keyed on the lockfile hash.
- Set `timeout-minutes` on each job and `fail-fast: false` for matrices where all results matter.
- Pass untrusted values through `env:` and reference `"$VAR"` in the script.
- Use `workflow_call` reusable workflows and composite actions to avoid copy-paste.

## Avoid
- `${{ github.event.pull_request.title }}` or `head_ref` interpolated directly into `run:`: script injection. Assign to `env:` and quote the variable.
- `pull_request_target` that checks out the PR head and runs its code: runs with secrets and a write token. Keep it to labeling, or check out only the base.
- Default token permissions: repo-wide write on older settings. Declare `permissions`.
- `uses: org/action@main` or `@v1` for third-party: a moved tag runs new code. Pin the SHA.
- `set-output` and `save-state` commands, and `::set-env`: removed. Write to `$GITHUB_OUTPUT`, `$GITHUB_STATE`, `$GITHUB_ENV`.
- Secrets in `echo` or `-x` shells: masking is best effort. Do not print them, and do not pass them as CLI args.
- Self-hosted runners on public repos: fork PRs can run code on them. Use hosted runners or restrict.
- Matrix `if:` using `secrets.*`: the `secrets` context is unavailable there. Map to `env` at the job level.

## Review
- [ ] `permissions` is minimal at workflow and job level.
- [ ] Third-party actions are SHA-pinned and `actionlint` passes.
- [ ] No untrusted event data flows into shell or `github-script` unescaped.
- [ ] Deploy jobs use OIDC, environments with protection rules, and concurrency.
