---
name: gitlab-ci
title: GitLab CI/CD
area: infra
tags: [gitlab, ci, pipeline, runners, rules, artifacts]
detect: [file:.gitlab-ci.yml, file:.gitlab/ci/*.yml, file:.gitlab/ci/*.yaml]
related: [github-actions, docker, kubernetes, terraform, circleci]
---
GitLab CI/CD: `.gitlab-ci.yml` pipelines with `rules`, `needs` DAGs, cache versus artifacts, includes and protected variables.

## Verify
- `glab ci lint`: validates `.gitlab-ci.yml` against the server (needs the `glab` CLI and auth).
- `glab ci status`: the current pipeline's jobs and state.
- `glab ci trace <job>`: live or finished log of one job.
- `yamllint .gitlab-ci.yml`: YAML structure, anchors and merges.
- `gitlab-ci-local --list`: lists jobs and runs them locally, when `gitlab-ci-local` is installed.

## Test first
The failing check is a pipeline run on a branch. Add the job with its assertion command, push, and read the job log.
```yaml
stages: [test]
unit:
  stage: test
  image: python:3.12-slim
  script:
    - pip install -r requirements.txt
    - pytest -q   # red until the test exists and passes
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

## Do
- Use `rules:` (with `if`, `changes`, `exists`, `when`) to control job creation, and `workflow: rules:` to stop duplicate branch and MR pipelines.
- Use `needs:` to run jobs as a DAG instead of waiting for whole stages.
- Use `cache:` (keyed by `files: [lockfile]`) for dependencies and `artifacts:` (with `expire_in`) for outputs passed between jobs.
- Share config with `include:` (`local`, `project`, `template`) and `extends:` plus hidden `.template` jobs.
- Mark secrets as masked and protected CI/CD variables, and scope them to environments.
- Use `id_tokens:` for OIDC to clouds and Vault instead of stored keys.
- Use `environment:` with `on_stop` for deploys, `resource_group:` to serialize them, and `interruptible: true` on CI jobs.
- Set `retry:` with `when: runner_system_failure` and `timeout:` per job.

## Avoid
- `only:` and `except:`: legacy. Use `rules:`.
- Mixing `rules` with `only`, or `rules` without a final fallback: jobs vanish or run twice. State every case.
- Using `cache` to pass build outputs: it is best effort and not guaranteed. Use `artifacts` (or `dependencies` and `needs`).
- Secrets in the YAML or unmasked variables: exposed in job logs. Use masked, protected variables.
- Deploy jobs without `rules` on the default or protected branch: forks or MRs can deploy. Gate them.
- `image: foo:latest` for jobs: nondeterministic. Pin a tag or digest.
- `script:` lines using a YAML-special character (`:` followed by space, leading `*`): parse errors or silent changes. Quote the line or use a block `|`.
- Large artifacts kept forever: storage cost. Set `expire_in`.

## Review
- [ ] `glab ci lint` passes and `workflow: rules` avoids duplicate pipelines.
- [ ] Deploy jobs are limited by `rules`, `environment` and protected variables.
- [ ] Cache keys derive from lockfiles and artifacts expire.
- [ ] Images are pinned and secrets are masked.
