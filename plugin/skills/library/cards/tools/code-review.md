---
name: code-review
title: Code review
area: tools
tags: [review, pull-requests, quality, diff, feedback, security]
detect: [file:.github/CODEOWNERS, file:CODEOWNERS, file:.github/pull_request_template.md]
related: [git, github-cli, refactoring, conventional-commits]
---
Review a diff for correctness, risk and tests first, style last, with findings you verified.

## Verify
- `git diff --stat origin/main...HEAD`: the size and shape of the change; large diffs get reviewed in parts.
- `git diff origin/main...HEAD -- tests/`: the tests that came with the change.
- `gh pr checks`: CI is green on the head commit being reviewed.
- `rg -n 'TODO|FIXME|XXX|console\.log|print\(|breakpoint\(\)' $(git diff --name-only origin/main...HEAD)`: leftover debug code in changed files.

## Test first
Practice check: for each suspected bug, write the failing test or command that shows it before commenting.
```sh
git checkout PR_BRANCH
./run-tests.sh                       # baseline
# craft the input from the finding; it must fail on the branch and pass after the fix
./repro-finding.sh; echo $?
```
A finding with a reproduction is a finding; a guess is a question.

## Do
- Read the description and linked issue first; check the diff does what they say and nothing else.
- Review in this order: behavior and edge cases, security and data safety, tests, API and compatibility, then naming and style.
- Trace each changed function's callers and its error paths, not only the hunk.
- Check what the change does not include: migrations, config, docs, feature flags, rollback.
- Look at tests: do they fail without the change, cover the edge and failure paths, and avoid asserting on mocks alone?
- Check trust boundaries: input validation, authorization, injection, secrets, logging of sensitive data.
- Mark comments as blocking or optional (nit); suggest a concrete fix.
- Let linters and formatters argue style; do not hand-review what a tool enforces.

## Avoid
- Approving from the diff alone when the logic depends on code outside it: open the callers and run it.
- Reporting issues you did not verify: run the code or read the surrounding source before asserting a bug.
- Style bikeshedding while missing correctness: spend attention on the risky lines.
- Reviewing a huge diff in one pass: ask to split it, or review by commit.
- Trusting passing CI as proof: check that the tests cover the new behavior.
- Vague feedback ("clean this up"): say what to change and why.
- Missing deleted code: removed checks, tests or error handling show up only in the red lines.

## Review
- [ ] Intent matches the diff; no unrelated changes.
- [ ] Edge, error and concurrency paths were considered.
- [ ] Security-relevant lines (auth, input, secrets, SQL, shell) were read closely.
- [ ] New or changed behavior has tests that would fail without it.
- [ ] Findings are verified, ranked, and each has a suggested fix.
