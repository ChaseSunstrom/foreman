---
name: refactoring
title: Refactoring
area: tools
tags: [refactoring, cleanup, tests, behavior, small-steps, dead-code]
detect: []
related: [ripgrep, code-review, git, dependency-upgrades]
---
Refactoring changes structure without changing behavior: pin behavior with tests, move in small steps, verify after each.

## Verify
- `git diff --stat`: the change touches only the files the refactor should.
- The project test command (for example `pytest -q`, `npm test`, `cargo test`, `go test ./...`): behavior is unchanged after every step.
- `rg -n '\bOLD_NAME\b'`: no stale references to a renamed or moved symbol remain.
- `git diff -w --color-moved=zebra`: moved code is visibly moved, not rewritten.

## Test first
Characterization test: pin current behavior, including odd behavior, before touching the code.
```python
def test_price_characterization():
    # recorded from the current implementation, not from the spec
    assert price(qty=0) == 0
    assert price(qty=3, coupon="X") == 27.0
    assert price(qty=1_000_000) == 9_500_000.0
```
Green before the refactor, green after. If a test fails, either the refactor changed behavior or the test was wrong; decide which on purpose.

## Do
- Do not mix a refactor with a feature or bug fix in one commit; make the structural change first.
- Take small steps: extract function, rename, move, inline, introduce parameter; run tests after each; commit when green.
- Use the language server or IDE rename and move refactorings, then search for string and config references they cannot see.
- Find usages with search before and after (see ripgrep), including tests, docs, configs and generated code.
- Delete dead code rather than commenting it out; the history keeps it.
- Keep public interfaces stable, or deprecate with a migration path before removal.
- Add tests at the seam you are about to cut where none exist; use seams such as parameters over mocks of internals.
- Stop when the target structure is reached; capture further ideas separately.

## Avoid
- Changing behavior and calling it a refactor: reviewers and tests do not expect it. Separate commits.
- Refactoring without tests: you cannot tell what broke. Write characterization tests first.
- A giant rename and reformat commit: unreviewable and conflict-prone. Do mechanical changes in their own commit or pull request.
- Renaming via search and replace: matches substrings and unrelated symbols. Use tooling or `-w` matches and read the diff.
- Removing "unused" code that is used by reflection, plugins, templates, serialization or external callers: search strings and config before deleting.
- Rewriting working code for taste: the risk is real, the benefit unproven. Refactor what you must change.
- Updating tests to match new behavior without noticing it was a regression.

## Review
- [ ] Tests existed or were added first, and pass unchanged after the refactor.
- [ ] No behavior change is hidden in the diff.
- [ ] Mechanical and logical changes are in separate commits.
- [ ] No stale references, dead code or commented-out code remain.
- [ ] Public API changes are intentional and documented.
