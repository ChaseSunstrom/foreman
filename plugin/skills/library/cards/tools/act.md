---
name: act
title: act
area: tools
tags: [github-actions, ci, docker, local-testing, workflows]
detect: [file:.actrc]
related: [github-cli, yamllint, make]
---
act: runs GitHub Actions workflows locally in Docker containers, for fast iteration before pushing.

## Verify
- `act -l`: the workflows and jobs act detects, with their events.
- `act -n`: dry run, shows what would execute without starting containers.
- `act push -j test`: run one job for the push event.
- `act pull_request -W .github/workflows/ci.yml`: run one workflow file for a given event.
- `act -j test --secret-file .secrets`: pass secrets from a local file kept out of git.

## Test first
Reproduce the CI failure in the job that fails remotely.
```
act -l                       # find the job id
act push -j lint -v          # verbose, shows each step and the container
# expect the same step to fail as on GitHub, then fix and rerun
```
If it passes locally and fails remotely, compare images, env and secrets.

## Do
- Store defaults in `.actrc` (`-P ubuntu-latest=<image>`, `--container-architecture linux/amd64` when on ARM).
- Pick a runner image deliberately: slim images lack tools that hosted runners have, so install them or use a larger image.
- Pass event payloads with `-e event.json` for `pull_request` fields the workflow reads.
- Use `--env-file` and `--secret-file`, and add both to `.gitignore`.
- Keep workflows runnable offline by caching in steps, and use `--pull=false` to reuse local images.
- Use `act -n` first on a new workflow, then a single job.

## Avoid
- Treating a green act run as proof: hosted runner images, OIDC, caches and services differ. Confirm on real CI.
- Using `secrets.GITHUB_TOKEN` expecting a real token: provide one with `-s GITHUB_TOKEN`, scoped minimally.
- Running deploy jobs: they hit real systems. Filter with `-j` or guard steps with `if: ${{ !env.ACT }}`.
- Mounting the Docker socket carelessly in untrusted workflows: only run workflows you trust.
- Missing tools (jq, zip) in the default image causing a false failure: use a fuller image or install the tool in a step.
- Matrix explosion locally: select with `--matrix key:value`.

## Review
- [ ] The failing job was reproduced, then fixed, with the exact `act` command noted.
- [ ] Secrets files are ignored by git and contain test values.
- [ ] Deploy and publish steps are skipped under act.
- [ ] The change was also confirmed on hosted CI.
