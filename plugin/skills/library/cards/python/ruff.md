---
name: ruff
title: Ruff
area: python
tags: [python, lint, format, ruff, static-analysis]
detect: [dep:ruff, file:ruff.toml, file:.ruff.toml]
related: [mypy, pyright, pytest, uv, python-packaging]
---
Ruff: the linter and formatter for Python, configured in `pyproject.toml` or `ruff.toml`.

## Verify
- `ruff check .`: lint violations.
- `ruff format --check .`: formatting drift (`ruff format --diff .` shows it).
- `ruff check --select I .`: import ordering when isort rules are enabled.
- `ruff check --show-settings FILE`: the effective config for one file, to debug why a rule does or does not fire.

## Test first
Lint is the check. Reproduce the violation on the smallest file, confirm it fails, then fix.
```
printf 'import os\nx = 1\n' > /tmp/t.py
ruff check --select F401 /tmp/t.py     # fails: unused import
```
Add a regression case to the code, not a lint-testing harness.

## Do
- Configure under `[tool.ruff]` and `[tool.ruff.lint]`: set `select`, `ignore`, `line-length`, and `target-version` (or `requires-python`).
- Start with `select = ["E", "F", "I", "B", "UP"]` and add `S`, `SIM`, `RUF`, `ASYNC` deliberately.
- Run `ruff check --fix` first, then `ruff format`; commit them as separate changes from logic.
- Use `per-file-ignores` for tests (for example `"tests/*" = ["S101"]`).
- Justify inline suppressions: `# noqa: E501  reason`. Use `ruff check --add-noqa` only for a deliberate baseline.
- Use `--unsafe-fixes` only on a clean tree and review the diff.
- Pin the Ruff version in the lock or pre-commit so CI and local agree.

## Avoid
- `black` and `isort` configured beside Ruff's formatter and `I` rules: two tools fight over the same lines. Keep one.
- `ruff check --fix` followed by committing unreviewed: some fixes change semantics (`UP`, `B`). Read the diff.
- The old top-level `select`/`ignore` keys under `[tool.ruff]`: deprecated in favor of `[tool.ruff.lint]`.
- `# noqa` with no code: hides every rule on the line. Name the code.
- `ignore = ["E501"]` and a formatter set to a different `line-length`: wrapped and long lines disagree. Align them.
- Formatting with `ruff format` in a repo whose formatter was Black with a custom `skip-string-normalization`: set `quote-style = "preserve"`.

## Review
- [ ] `ruff check .` and `ruff format --check .` are clean in CI with a pinned version.
- [ ] The selected rule sets are listed in config with reasons for each ignore.
- [ ] `noqa` comments name a code and, if surprising, a reason.
- [ ] Only one formatter and one import sorter run.
- [ ] Auto-fixes landed as a reviewed, separate commit.
