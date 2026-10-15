---
name: circleci
title: CircleCI
area: infra
tags: [circleci, ci, orbs, workflows, config, caching]
detect: [file:.circleci/config.yml, file:.circleci/*.yml, file:.circleci/*.yaml]
related: [github-actions, gitlab-ci, jenkins, docker]
---
CircleCI: `.circleci/config.yml` version 2.1 with workflows, orbs, reusable commands, caching and contexts.

## Verify
- `circleci config validate`: the config parses and orb references resolve.
- `circleci config process .circleci/config.yml`: the expanded config after orbs and parameters (what actually runs).
- `circleci local execute --job build`: runs one job locally in Docker (executor limits apply, not workflows).
- `circleci config pack .circleci/src > .circleci/config.yml`: rebuilds from split config files, when used.

## Test first
The failing check is a job in a workflow that runs the test command. Validate, push, and read the run.
```yaml
version: 2.1
jobs:
  test:
    docker: [{ image: cimg/python:3.12 }]
    steps:
      - checkout
      - run: pytest -q   # red until the test exists
workflows:
  ci:
    jobs: [test]
```
`circleci config validate` is the pre-push gate.

## Do
- Use `version: 2.1` to get orbs, `parameters`, `commands` and `executors`.
- Use `cimg/*` convenience images and pin their tags.
- Define reusable `commands:` and `executors:` and pass `parameters:` with types and defaults.
- Cache with `restore_cache` and `save_cache` keyed by `{{ checksum "lockfile" }}` with fallback keys, and pass build outputs between jobs with `persist_to_workspace` and `attach_workspace`.
- Express order with `requires:` in workflows and filter with `filters: branches:` or `tags:`.
- Keep secrets in contexts or project env vars, and restrict contexts by security group.
- Use `resource_class` sized to need, `parallelism` with `circleci tests split`, and `store_test_results` for timing and the UI.
- Use `when`/`unless` conditionals on parameters or pipeline values to switch workflows.

## Avoid
- `version: 2` configs: no orbs or parameters and increasingly unsupported. Use 2.1.
- Using `latest` tags or `circleci/*` legacy images: deprecated and unstable. Use `cimg/*` with a pinned tag.
- Cache keys without a checksum (`v1-deps`): the cache never refreshes. Include `{{ checksum "package-lock.json" }}`.
- `save_cache` of paths that change every run: slow uploads and no hits. Cache only dependencies.
- Secrets echoed in `run` or stored in the repo config: use contexts and avoid printing them.
- Untrusted orbs unpinned (`orb@volatile`): changing code in your pipeline. Pin a semver.
- Forked PRs with secrets enabled: the PR author can read them. Leave "pass secrets to builds from forks" off.
- Over-long `run` blocks: hard to test. Move logic into scripts in the repo.

## Review
- [ ] `circleci config validate` passes and orbs are pinned.
- [ ] Cache keys include a lockfile checksum and workspaces carry build outputs.
- [ ] Contexts hold secrets with restricted access.
- [ ] Workflows use `requires` and filters, and tests are split with results stored.
