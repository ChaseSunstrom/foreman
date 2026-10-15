---
name: codecov
title: Codecov
area: tools
tags: [coverage, ci, pull-requests, reporting, flags]
detect: [file:codecov.yml, file:.codecov.yml]
related: [sonarqube, pytest, github-cli]
---
Codecov: receives coverage reports from CI, comments on pull requests and sets status checks from codecov.yml targets.

## Verify
- `curl -s --data-binary @codecov.yml https://codecov.io/validate`: the config validates (needs network).
- `pytest --cov --cov-report=xml`: a coverage report exists before upload (use the runner's own equivalent).
- `ls coverage.xml lcov.info coverage/lcov.info 2>/dev/null`: the file the uploader will find is present.
- `codecov-cli upload-process --dry-run`: the files and commit the uploader would send, if the CLI is installed.
- `git rev-parse HEAD`: the commit SHA the report must be attached to.

## Test first
Reproduce a missing or empty upload locally.
```
pytest --cov=app --cov-report=xml
head -c 300 coverage.xml            # has <source> and packages with line-rate > 0
grep -c "<class " coverage.xml      # nonzero, else paths or sources are wrong
```
Then confirm the CI log of the upload step shows a processed report.

## Do
- Upload from the CI job that ran the tests, after the report is written, with the token in a secret.
- Use `flags` per component or test type, and carryforward for flags that run in some jobs only.
- Set project and patch statuses in `codecov.yml` with `target` and `threshold`; patch coverage checks the diff itself.
- Use `ignore:` for generated code, migrations and tests.
- Enable `fail_ci_if_error` in the upload step so a failed upload is visible.
- Fetch enough history so base and head commits resolve.

## Avoid
- Uploading from fork PRs expecting a token: it is absent. Use tokenless upload settings the platform supports, or accept no report.
- Path mismatch between the report and the repo root (Docker build paths): coverage shows 0 or files are missing. Fix with `fixes:` in codecov.yml or run tests at repo root.
- A project target of 100% or a tight threshold: noisy red checks. Use patch coverage with a realistic target.
- Combining reports in unrelated jobs and shipping each as full: totals jump. Use flags or merge first.
- Silent failure of upload (`|| true`): the check goes missing without notice. Keep the step strict.
- Counting test files as source: add them to `ignore`.

## Review
- [ ] The config validates and targets reflect an agreed policy.
- [ ] CI uploads once per report, with flags where components differ.
- [ ] Generated code and tests are ignored.
- [ ] A PR shows both the project and patch status.
