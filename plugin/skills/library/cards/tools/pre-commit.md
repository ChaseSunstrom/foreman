---
name: pre-commit
title: pre-commit
area: tools
tags: [pre-commit, hooks, git, lint, format, ci]
detect: [file:.pre-commit-config.yaml, dep:pre-commit]
related: [git, make, conventional-commits, github-cli]
---
The pre-commit framework: versioned git hooks defined in `.pre-commit-config.yaml`, run locally and in CI.

## Verify
- `pre-commit run --all-files`: every hook passes on the whole repo, not just staged files.
- `pre-commit validate-config`: the config file parses and has the required keys.
- `pre-commit autoupdate`: pins move to current tags (review the diff).
- `pre-commit install --install-hooks`: the git hook is installed and hook environments are built.

## Test first
Practice check: make a hook fail on a known-bad file, then fix.
```sh
printf 'x = 1   \n' > /tmp/bad.py && cp /tmp/bad.py ./bad.py
pre-commit run --files bad.py       # trailing-whitespace hook must fail and fix the file
rm bad.py
```
For a local hook, add a bad fixture and assert the hook exits non-zero.

## Do
- Pin every `rev:` to a tag or full SHA; update with `pre-commit autoupdate`.
- Use `repo: local` with `language: system` or `language: python` for project scripts; set `pass_filenames` deliberately.
- Scope with `files:`, `exclude:` and `types:` rather than hooks that scan everything.
- Run the same command in CI: `pre-commit run --all-files --show-diff-on-failure`.
- Use `stages: [pre-push]` for slow checks; `default_install_hook_types` to install several stages.
- Use `args:` to pass tool options; keep tool config in its own file (`pyproject.toml`).
- Cache `~/.cache/pre-commit` in CI keyed on the config hash.
- Run `pre-commit gc` to drop unused environments.

## Avoid
- `rev: main` or `master`: not reproducible, and `autoupdate` cannot track it. Pin a tag.
- `git commit --no-verify` as routine: CI then fails later. Fix the hook or fix the code.
- Hooks that modify files without telling devs: a failed run after auto-fix is normal; re-stage and commit again.
- Only running hooks on commit and not in CI: contributors who never installed them bypass checks.
- Slow hooks (full test suite) at commit time: move to `pre-push` or CI.
- `language: system` hooks depending on a tool not in the lockfile: they differ per machine. Use a hook repo or `language: python` with `additional_dependencies`.
- Old `stages: [commit]` names: current config uses `pre-commit`; run `pre-commit migrate-config`.

## Review
- [ ] All `rev:` values pinned and recently updated.
- [ ] CI runs `pre-commit run --all-files`.
- [ ] Slow hooks are in the right stage.
- [ ] `pre-commit run --all-files` is clean on a fresh clone.
