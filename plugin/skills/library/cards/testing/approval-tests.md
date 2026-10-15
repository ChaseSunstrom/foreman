---
name: approval-tests
title: Approval tests
area: testing
tags: [testing, approval, golden, snapshot, verify, legacy, output]
detect: [dep:approvaltests, dep:ApprovalTests, dep:Verify.Xunit, dep:Verify.NUnit, dep:Verify, dep:com.approvaltests*, file:*.approved.txt, file:*.verified.txt]
related: [golden-files, snapshot-testing, characterization-tests, regression-tests]
---
Approval tests compare output to a human-reviewed approved file: the diff is the review, and a scrubbed, stable output is the contract.

## Verify
- `pytest -q` (approvaltests) or `dotnet test` (Verify): each test compares to its `.approved` or `.verified` file and fails on any diff.
- `git status --short '*.received.*'`: leftover received files mean unreviewed or failing output; none should be committed.
- `git diff -- '*.approved.*' '*.verified.*'`: the approved files changed only where the behavior change was intended.
- `git ls-files '*.received.*'`: prints nothing, so no received files were committed.

## Test first
Write the test, run it to produce the received file, review it by eye, approve it, then change the code.
```python
from approvaltests import verify

def test_invoice_renders_totals_and_tax():
    invoice = build_invoice(items=[("pen", 2, 150)], tax_rate=0.2)
    verify(render_text(invoice))
```
The first run fails and writes the received file next to the test. Approve by moving it to the approved name once it reads correctly.

## Do
- Review the received output line by line before approving; it is the assertion.
- Scrub nondeterminism before verifying: timestamps, ids, absolute paths, random order, ports, GUIDs (scrubbers or sorting).
- Verify human-readable text (text, JSON pretty-printed with sorted keys, HTML) so diffs are reviewable.
- Keep each approved file small and about one scenario; name tests for the scenario.
- Use approvals for wide, hard-to-assert outputs: reports, generated code, serialized objects, legacy behavior.
- Commit the approved files; add the received files to the ignore list.
- Pair with combination or parametrized inputs for coverage of many cases, one file per case.
- Update approvals only in a commit that explains the intended output change.

## Avoid
- Approving without reading (bulk "accept all"): the test becomes a rubber stamp. Read the diff.
- Unscrubbed timestamps and ids: flaky failures every run. Scrub or inject fixed values.
- Huge approved files for one test: nobody reviews them. Split by scenario or verify the relevant slice.
- Replacing precise assertions with an approval where one value matters: unclear intent. Assert the key value directly.
- Committing received files: noise and confusion. Ignore them.
- Environment-dependent output (locale, line endings, OS paths): fails on CI. Normalize it.

## Review
- [ ] Approved files were read, and diffs match the intended change.
- [ ] Output is scrubbed and deterministic.
- [ ] Files are small and named per scenario.
- [ ] Received files are ignored and not committed.
- [ ] Key values are asserted directly where they matter.
