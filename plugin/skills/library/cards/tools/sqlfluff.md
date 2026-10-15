---
name: sqlfluff
title: SQLFluff
area: tools
tags: [sql, lint, format, dialect, dbt, ci]
detect: [file:.sqlfluff, dep:sqlfluff]
related: [pre-commit, ruff]
---
SQLFluff: dialect-aware SQL linter and formatter, configured in .sqlfluff, with templater support for dbt and Jinja.

## Verify
- `sqlfluff lint path/ --dialect postgres`: rule violations with codes (use the project's dialect).
- `sqlfluff fix path/ --dialect postgres`: safe auto-fixes applied; then re-run lint.
- `sqlfluff parse file.sql --dialect postgres`: the file parses, and shows the tree when a rule misbehaves.
- `sqlfluff lint --dialect postgres -`: lint SQL from stdin, for a quick reproduction.
- `sqlfluff rules`: the rule codes and names available to enable or exclude.

## Test first
Lint a file that holds the violation, and see the code.
```
printf 'select a,b from t\n' > /tmp/bad.sql
sqlfluff lint /tmp/bad.sql --dialect ansi
# expect CP01 (keyword case), LT01 (spacing) and similar findings
```
After the fix, lint exits 0. Add such a file as a fixture only if the repo tests its own config.

## Do
- Set `dialect` in `.sqlfluff` under `[sqlfluff]`, so no one has to pass it.
- Pick the templater (`jinja`, `dbt`, `placeholder`) that matches how the SQL is built, and set its context.
- Tune with `exclude_rules` and `[sqlfluff:rules:...]` sections rather than inline noqa where policy is global.
- Use `-- noqa: LT05` on one line only for real exceptions, with a reason nearby.
- Run `sqlfluff fix` on small sets and review the diff: auto-fix can change layout widely.
- Ignore generated or vendored SQL in `.sqlfluffignore`.

## Avoid
- Linting with the wrong dialect: parse errors (PRS) flood the output. Set the right dialect once in config.
- Linting dbt models with the plain jinja templater when refs and macros are used: use the dbt templater with the dbt profile available.
- Disabling the whole parse rule family to get green: fix the SQL or dialect.
- Running `fix` across the whole repo in a feature PR: the diff drowns the change. Do it in a separate formatting commit.
- Slow runs on large trees: pass changed files, or use `--processes N`.
- Treating warnings as noise: set `warnings` for rules in rollout and move them to errors later.

## Review
- [ ] `.sqlfluff` sets dialect and templater and is committed.
- [ ] `sqlfluff lint` exits 0 on changed SQL in CI.
- [ ] Any `noqa` is single-rule and justified.
- [ ] Formatting-only changes are separate from logic changes.
