---
name: renovate
title: Renovate
area: infra
tags: [renovate, dependencies, automation, updates, presets, security]
detect: [file:renovate.json, file:renovate.json5, file:.renovaterc, file:.renovaterc.json, file:.github/renovate.json]
related: [dependabot, github-actions, docker, terraform]
---
Renovate: config-as-code dependency updates with presets, grouping, automerge rules and pinned digests.

## Verify
- `renovate-config-validator`: validates the config file in the repo (ships with the renovate package).
- `npx --yes --package renovate -- renovate-config-validator --strict`: same, without a global install and with strict checks.
- `LOG_LEVEL=debug renovate --platform=local`: dry-run of what Renovate detects in the working tree (local mode).
- `git diff --stat`: a preset change did not alter unrelated files.

## Test first
Make the validator a CI check, then change the config.
```bash
npx --yes --package renovate -- renovate-config-validator --strict renovate.json
# then assert the rule by running local mode and reading the report
LOG_LEVEL=debug npx --yes renovate --platform=local 2>&1 | grep -E 'packageFile|depName' | head
```

## Do
- Extend a base: `"extends": ["config:recommended"]`; add `helpers:pinGitHubActionDigests` for Actions pinning and `docker:pinDigests` for images.
- Group related updates with `packageRules` and `groupName`, matching with `matchPackageNames` or `matchManagers`.
- Automerge only low-risk updates: `matchUpdateTypes: ["patch", "minor"]` with `automerge: true` and required passing status checks.
- Add `minimumReleaseAge` (for example `"3 days"`) to delay brand-new releases.
- Set `schedule` and `prConcurrentLimit` to control PR volume, and `labels` for triage.
- Enable `vulnerabilityAlerts` so security fixes bypass schedules.
- Use `customManagers` with regex for versions in Makefiles or scripts.
- Pin dependencies (`rangeStrategy`, pin digests) so builds are reproducible.

## Avoid
- Automerge of major updates without tests: breakage lands on main. Restrict to patch and minor and require checks.
- Old option names (`extends: ["config:base"]`, `matchPackagePatterns` for plain names): migrate with `renovate-config-validator` messages and the migration prompts. Use current presets and `matchPackageNames`.
- Letting Renovate open dozens of PRs: set `prConcurrentLimit` and grouping.
- Config JSON with comments in `renovate.json`: use `renovate.json5` when comments are needed.
- Pinning Actions by tag only: tags move. Use digest pinning.
- Forgetting `ignorePaths` for vendored or example directories: noisy PRs.

## Review
- [ ] Config validates with the strict validator.
- [ ] Automerge rules are narrow and gated by CI.
- [ ] Release age and concurrency limits are set.
- [ ] Docker images and Actions are digest-pinned.
- [ ] Security updates are not delayed by schedules.
