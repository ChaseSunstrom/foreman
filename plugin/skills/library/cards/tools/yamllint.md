---
name: yamllint
title: yamllint
area: tools
tags: [yaml, lint, config, ci, formatting]
detect: [file:.yamllint*]
related: [hadolint, pre-commit, kubectl-debugging]
---
yamllint: checks YAML syntax and style (indentation, line length, truthy values, duplicate keys) against a rule config.

## Verify
- `yamllint .`: all YAML under the tree, with line, column and rule names.
- `yamllint -s .`: strict mode, so warnings also fail the run.
- `yamllint -c .yamllint.yaml file.yaml`: use an explicit config.
- `yamllint -f parsable .`: single-line output for CI and editors.
- `yamllint -d relaxed file.yaml`: try a built-in preset without a config file.

## Test first
Feed it the file that shows the problem.
```
printf 'on: push\nkey: 1\nkey: 2\n' > /tmp/t.yaml
yamllint /tmp/t.yaml
# expect truthy ("on") and key-duplicates errors, plus document-start warning
```
Fix, and it exits 0.

## Do
- Start from `extends: default` and override a few rules in `.yamllint.yaml`.
- Set `indentation: {spaces: 2, indent-sequences: consistent}` to match the repo's actual style.
- Set `line-length` with `max` and `allow-non-breakable-words: true` for long URLs and commands.
- Set `truthy: {allowed-values: ['true', 'false'], check-keys: false}` so CI files with `on:` pass.
- Use `ignore:` patterns (a multi-line string) for generated or vendored files.
- Disable one rule on one line: `# yamllint disable-line rule:line-length`.
- Run it in CI and in pre-commit on changed files only.

## Avoid
- Treating `on:` or `yes` as booleans unknowingly: YAML 1.1 parsers read `yes`, `no` and `on` as booleans. Quote strings, or use true and false.
- Tabs for indentation: they are a syntax error. Use spaces, and set the editor accordingly.
- Linting Helm templates (`{{ }}`) as YAML: they do not parse. Lint the rendered output, or ignore `templates/`.
- Turning off `key-duplicates`: a duplicate key silently drops the earlier value. Fix it.
- Raising `line-length` to a huge number to quiet it: use non-breakable words or fold strings with `>`.
- Missing quotes on version-like values (`1.10` becomes 1.1): quote them.

## Review
- [ ] `yamllint -s` passes on changed files with the repo config.
- [ ] No rule is disabled globally without a reason in the config.
- [ ] Ambiguous scalars (versions, `on`, `no`, octal-looking numbers) are quoted.
- [ ] Template files are excluded, or lint is run on rendered output.
