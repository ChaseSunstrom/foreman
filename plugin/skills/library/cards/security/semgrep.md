---
name: semgrep
title: Semgrep
area: security
tags: [security, semgrep, sast, static-analysis, ci, rules]
detect: [file:.semgrep.yml, file:.semgrep.yaml, file:.semgrepignore, file:.semgrep/*, dep:semgrep]
related: [codeql, owasp-top-10, sql-injection, xss, dependency-audit]
---
Semgrep: run a curated ruleset plus project rules in CI, write a rule test before each custom rule, and triage findings instead of muting them.

## Verify
- `semgrep scan --config p/default --error`: the default ruleset reports nothing and the exit code is non-zero on findings.
- `semgrep scan --config .semgrep/ --error`: the project's own rules pass on the code.
- `semgrep --test .semgrep/`: every custom rule passes its annotated test cases.
- `semgrep scan --config p/security-audit --sarif -o semgrep.sarif`: a SARIF report is produced for upload.

## Test first
Write the rule and its test file side by side; the test fails until the rule matches.
```yaml
# .semgrep/no-shell-true.yml
rules:
  - id: no-shell-true
    languages: [python]
    severity: ERROR
    message: subprocess with shell=True; pass an argv list
    pattern: subprocess.$F(..., shell=True, ...)
```
```python
# .semgrep/no-shell-true.py
import subprocess
# ruleid: no-shell-true
subprocess.run(cmd, shell=True)
# ok: no-shell-true
subprocess.run(["ls", d])
```

## Do
- Start with `p/default` and `p/security-audit`, add language packs (`p/python`, `p/javascript`, `p/owasp-top-ten`) as needed.
- Keep project rules in `.semgrep/` and test them with `# ruleid:` and `# ok:` comments in same-named files.
- In pull requests, scan the diff only for speed (`--baseline-commit`), and run the full scan on the main branch on a schedule.
- Use taint mode (`mode: taint` with `pattern-sources` and `pattern-sinks`) for injection rules instead of plain patterns.
- Silence a single false positive with `# nosemgrep: rule-id` plus a reason comment, not by disabling the rule.
- Exclude vendored and generated code in `.semgrepignore`.
- Export SARIF to the code-scanning dashboard so findings track over time.

## Avoid
- Running without `--error`: findings print but CI passes. Add it so findings fail the build.
- A blanket bare `# nosemgrep` with no rule id: it hides every rule on that line. Name the rule and the reason.
- Treating a clean run as a clean bill: patterns miss flows across files. Pair with tests and review, and consider CodeQL for deep dataflow.
- Writing rules with no test cases: they silently stop matching after a syntax change. Use `semgrep --test`.
- Pinning to unreviewed remote rules from unknown registries: use official packs or vendor rules into the repo.
- Overbroad `pattern-either` rules: they flood noise and teach people to ignore results. Narrow with `pattern-not` and `metavariable-regex`.

## Review
- [ ] CI fails on findings from the chosen rulesets.
- [ ] Custom rules have passing `semgrep --test` cases.
- [ ] Each suppression names a rule and a reason.
- [ ] Generated and vendored code is excluded.
- [ ] Results reach a dashboard or PR annotation.
