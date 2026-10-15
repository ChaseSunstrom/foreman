---
name: sonarqube
title: SonarQube
area: tools
tags: [static-analysis, quality-gate, coverage, code-smells, ci]
detect: [file:sonar-project.properties]
related: [codecov, code-review, github-cli]
---
SonarQube and SonarCloud: static analysis with a quality gate over bugs, vulnerabilities, smells, duplication and coverage on new code.

## Verify
- `sonar-scanner -Dsonar.qualitygate.wait=true`: analysis runs and the step fails if the quality gate fails (needs host URL and token in env).
- `sonar-scanner -X`: debug output to see which files and settings were used.
- `grep -E "^sonar\." sonar-project.properties`: sources, tests, exclusions and report paths are what you expect.
- Run the test suite with coverage first and confirm the report file exists at the path in `sonar.*.reportPaths`.
- `git diff --stat origin/main...HEAD`: the scope of "new code" the gate judges.

## Test first
A gate failure is the test. Reproduce the failing condition locally.
```
# add the offending code or remove tests, then:
pytest --cov --cov-report=xml
sonar-scanner -Dsonar.qualitygate.wait=true
# expect: QUALITY GATE STATUS: FAILED, with the condition named
```
Fix, rerun, expect PASSED.

## Do
- Set `sonar.projectKey`, `sonar.sources`, `sonar.tests` and `sonar.exclusions` in `sonar-project.properties`.
- Generate coverage in a format Sonar reads (`sonar.python.coverage.reportPaths`, `sonar.javascript.lcov.reportPaths`, `sonar.coverage.jacoco.xmlReportPaths`) before the scan step.
- Pass the token through a secret env var (`SONAR_TOKEN`), never in the file.
- Fetch full git history in CI: blame and new-code detection need it.
- Judge by "new code" conditions, so legacy debt does not block fixes.
- Mark false positives in the UI with a reason, or use the supported `// NOSONAR` sparingly.

## Avoid
- Shallow clones: "new code" and SCM blame are wrong or missing. Use full fetch depth.
- Coverage shown as 0%: report path or relative file paths do not match sources. Align `sonar.sources` and the report's paths.
- Excluding whole directories to pass the gate: exclude only generated code and vendored files.
- Running analysis before tests produce the report: reorder CI steps.
- Committing the token: rotate it and use CI secrets.
- Blanket `NOSONAR`: it hides real issues. Scope it to one line with a reason.

## Review
- [ ] The quality gate passes on the PR, and conditions were not loosened to get there.
- [ ] Coverage report path resolves and the number is plausible.
- [ ] Exclusions cover only generated or third-party code.
- [ ] No secrets in properties, and CI uses full history.
