---
name: legacy-code
title: Working with Legacy Code
area: domains
tags: [legacy, refactoring, characterization-tests, strangler, migration]
detect: []
related: [cli-design, cron-jobs, web-scraping, timezones]
---
Changing code without tests or docs: pin current behavior first, make small reversible steps, and replace pieces behind seams.

## Verify
- `git log --follow --stat -- path/to/file | head -50`: how and why the file changed, and who touched it.
- `git grep -n "functionName"`: every caller and string-based reference, including config and scripts.
- Run the characterization suite before and after each step: output is byte-identical or differences are understood.
- Coverage report for the touched area (`coverage run -m pytest`, `nyc`, `go test -cover`): the lines you change are exercised.

## Test first
Write a characterization (golden master) test: record what the code does now, right or wrong.
```python
import json, pathlib
from legacy.pricing import quote

CASES = json.loads(pathlib.Path("tests/golden/inputs.json").read_text())

def test_quote_matches_recorded_behavior():
    golden = json.loads(pathlib.Path("tests/golden/quote.json").read_text())
    for name, args in CASES.items():
        assert quote(**args) == golden[name], name
```
Generate `quote.json` once by running the existing code over real or representative inputs, review it, commit it, then refactor against it.

## Do
- Read before editing: run it, trace one real flow, and note surprises.
- Characterize first with golden-master tests at the highest stable seam (function, HTTP endpoint, CLI output), using production-like inputs.
- Find or create a seam: extract the function, inject the dependency (clock, DB, network), wrap a global; pin the behavior with a test first.
- Make one change at a time: separate commits for refactors and behavior changes, each green.
- Rename and move with tooling (IDE, `jscodeshift`, `gofmt -r`, `rope`), not by hand.
- Replace gradually with the strangler pattern: route a slice of traffic to the new code behind a flag; compare outputs in shadow mode; then remove the old path.
- Delete dead code only with evidence: no callers (`git grep`), no runtime hits in logs or metrics over a full business cycle.
- Add logging and metrics around risky areas before changing them.
- Leave the campsite better: add one test and one comment explaining why for what you touch.
- Record decisions and discovered quirks in a short note next to the code.

## Avoid
- Rewriting from scratch: loses undocumented behavior and takes longer than planned. Strangle instead.
- "Fixing" odd behavior while refactoring: changes semantics and masks regressions. Pin it, refactor, then change deliberately.
- Large untested commits: no bisection and no rollback. Keep steps small.
- Trusting comments and names: they drift. Trust the tests and the runtime.
- Upgrading frameworks and refactoring together: unclear blame when it breaks. Do them separately.
- Deleting code that looks unused but is called by reflection, cron, templates or another repo: check strings and external users.
- Removing a flag or compatibility branch without checking data in the wild: old records still use it.
- Mocking everything to get a test running: the test proves the mock. Prefer real dependencies at a higher seam.

## Review
- [ ] Behavior-pinning tests existed and passed before the first change.
- [ ] Refactors and behavior changes are in separate, individually green commits.
- [ ] Deleted code has evidence of no callers; external uses were checked.
- [ ] A rollback path exists (flag, revert, old path kept in shadow).
- [ ] Newly learned quirks are documented where the next reader will see them.
