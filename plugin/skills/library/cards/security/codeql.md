---
name: codeql
title: CodeQL
area: security
tags: [security, codeql, sast, github, dataflow, code-scanning]
detect: [file:.github/workflows/codeql.yml, file:.github/workflows/codeql-analysis.yml, file:.github/codeql/*.yml, file:codeql-pack.yml, file:qlpack.yml]
related: [semgrep, owasp-top-10, sql-injection, xss, dependency-audit]
---
CodeQL: build a database of the code, run query suites for deep dataflow findings, and gate pull requests on the alerts.

## Verify
- `codeql database create db --language=python --source-root .`: the code extracts into a database (swap the language, and add `--command` for compiled ones).
- `codeql database analyze db --format=sarif-latest --output=codeql.sarif codeql/python-queries:codeql-suites/python-security-and-quality.qls`: the query suite runs and writes SARIF.
- `codeql test run .github/codeql/queries`: custom queries pass their expected-output tests.

## Test first
For a custom query, write the test source and the expected results first; the test fails until the query is right.
```
.github/codeql/queries/
  NoShellTrue.ql
  test/NoShellTrue/
    test.py            # contains a bad call and a good call
    NoShellTrue.qlref  # NoShellTrue.ql
    NoShellTrue.expected
```
Run `codeql test run .github/codeql/queries/test`, inspect the `.actual` file it writes, and promote it to `.expected` once it matches your intent.

## Do
- Use the GitHub workflow with `github/codeql-action` steps (`init`, `autobuild` or a manual build, `analyze`) on push, pull request and a weekly schedule.
- Choose the `security-extended` or `security-and-quality` query suite for broader coverage than the default.
- Keep the config in `.github/codeql/codeql-config.yml` (`queries`, `paths`, `paths-ignore`) and reference it from the `init` step.
- For compiled languages (Java, C#, C++, Go), make sure the build step actually compiles the code CodeQL should see.
- Model your own sanitizers and sources with data extensions (`.yml` model packs) so findings are accurate.
- Triage alerts in the Security tab with a dismissal reason, and require a passing code-scanning check before merge.
- Pin the action to a commit SHA and update it regularly.

## Avoid
- Analyzing without a working build for compiled languages: the database is empty, so zero alerts mean nothing. Check that the extraction summary shows files.
- Excluding large paths to speed up a run: you exclude the vulnerable code. Use `paths-ignore` only for tests and generated code.
- Dismissing alerts as "false positive" with no note: they return and nobody knows why. Add a reason, or write a sanitizer model.
- Relying on the default suite only: it is narrow. Use `security-extended`.
- Assuming CodeQL replaces review: it follows known sinks and sources. Keep manual and test coverage.
- Letting the scan fail open in CI (`continue-on-error: true`): findings never gate anything. Remove it.

## Review
- [ ] The database includes the code that ships (extraction counts checked).
- [ ] A security query suite is selected.
- [ ] Alerts block merge or are triaged with reasons.
- [ ] Custom queries have expected-output tests.
- [ ] The workflow runs on PRs and on a schedule.
