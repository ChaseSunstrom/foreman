---
name: dependabot
title: Dependabot
area: infra
tags: [dependabot, github, dependencies, updates, security, automation]
detect: [file:.github/dependabot.yml, file:.github/dependabot.yaml]
related: [renovate, github-actions, docker, terraform]
---
Dependabot version updates: a per-ecosystem .github/dependabot.yml with schedules, grouping, limits and a review path.

## Verify
- `python -c "import yaml; d=yaml.safe_load(open('.github/dependabot.yml')); assert d['version']==2 and d['updates']"`: file parses and has version 2 with updates.
- `gh api repos/:owner/:repo/vulnerability-alerts -i | head -1`: alerts enabled (204 means on).
- `gh pr list --author 'app/dependabot'`: its open PRs and volume.
- `git ls-files | grep -E 'package.json|requirements|go.mod|Dockerfile|\.github/workflows'`: every ecosystem present in the repo is covered by an entry.

## Test first
Fail on a missing ecosystem before writing the entry.
```python
import yaml, pathlib
cfg = yaml.safe_load(open(".github/dependabot.yml"))
eco = {u["package-ecosystem"] for u in cfg["updates"]}
if list(pathlib.Path(".").glob(".github/workflows/*.y*ml")):
    assert "github-actions" in eco
if pathlib.Path("Dockerfile").exists():
    assert "docker" in eco
```

## Do
- Set `version: 2` and one `updates` entry per ecosystem and directory: `package-ecosystem`, `directory` (or `directories`), `schedule.interval`.
- Use ecosystem names exactly: `npm`, `pip`, `gomod`, `cargo`, `docker`, `github-actions`, `terraform`, `maven`, `gradle`, `bundler`, `composer`.
- Add `groups` to batch related updates (by `patterns` and `update-types`) and reduce PR count.
- Set `open-pull-requests-limit`, `labels`, `reviewers` or CODEOWNERS routing, and a `commit-message.prefix` matching your conventions.
- Add `cooldown` settings to delay fresh releases where your plan supports them.
- Use `ignore` with `dependency-name` and `update-types` for known-bad majors, with a comment why.
- Enable Dependabot security updates and alerts in repository settings separately from this file.
- Let CI run on Dependabot PRs; note its secrets come from the Dependabot secrets store, not Actions secrets.

## Avoid
- Missing the `github-actions` ecosystem: workflow actions go stale. Add an entry.
- `directory: "/"` only in monorepos: nested manifests are ignored. List each or use `directories`.
- Auto-approving and merging every PR with a broad token: supply chain risk. Limit to patch and minor with required checks.
- Expecting `.github/dependabot.yml` to configure security alerts: those are settings. Enable them in the repo.
- Daily schedule on a large repo without groups: PR flood. Use weekly and groups.
- Private registries without `registries` config: updates fail. Declare the registry and secret name.

## Review
- [ ] Every ecosystem and directory in the repo has an entry.
- [ ] Groups and limits keep volume manageable.
- [ ] Merge policy requires CI and review.
- [ ] Private registries are configured with secrets.
- [ ] Security alerts and updates are enabled in settings.
