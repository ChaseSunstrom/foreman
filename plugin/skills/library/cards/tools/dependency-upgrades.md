---
name: dependency-upgrades
title: Dependency upgrades
area: tools
tags: [dependencies, upgrades, lockfile, semver, security, renovate]
detect: [file:renovate.json, file:.github/dependabot.yml, file:.github/dependabot.yaml]
related: [git, code-review, refactoring, pre-commit]
---
Upgrade dependencies in small, tested, reversible steps, with lockfile diffs and changelogs read.

## Verify
- `git diff --stat -- '*lock*' '*.lock'`: the lockfile moved only by the intended packages.
- The ecosystem's outdated command (`npm outdated`, `pip list --outdated`, `cargo outdated`, `go list -u -m all`): what is behind.
- The ecosystem's audit command (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck ./...`): known vulnerabilities before and after.
- The project test and build commands: the suite and a clean production build pass on the upgraded tree.

## Test first
Practice check: the existing suite is the failing test; make the upgrade expose what breaks.
```sh
git switch -c chore/upgrade-foo
<bump foo to the next version, regenerate lockfile>
<run tests and build>           # failures are the migration work list
```
Add a test for each usage of a changed API before changing the call site, and for any behavior the changelog says changed.

## Do
- Upgrade one package, or one tightly coupled group (framework and its plugins), per commit.
- Read the changelog and release notes for breaking changes and deprecations between your version and the target.
- Upgrade in steps through major versions when the project documents a migration path.
- Install through the lockfile commands and commit the lockfile with the manifest (`npm ci`, `uv sync --frozen`, `cargo build --locked`).
- Run deprecation warnings as errors where the tool allows, so deprecations surface.
- Separate security patches (urgent, minimal) from feature upgrades.
- Pin versions in applications; use ranges in libraries with tested bounds.
- Check licenses and the added transitive dependencies in the lockfile diff.

## Avoid
- Bulk "upgrade everything" commits: a failure cannot be traced. Upgrade in small groups.
- Editing the lockfile by hand: it breaks integrity hashes. Regenerate with the tool.
- Floating `latest` or `*` in manifests: builds are not reproducible. Pin or bound.
- Ignoring peer dependency and engine warnings: runtime breakage later. Resolve them.
- Assuming semver is honored: minor releases do break code. Run the suite regardless.
- Merging an automated upgrade pull request because CI is green when the tests do not cover the package's use.
- Upgrading a runtime and its dependencies in one change: do the runtime first.
- Suppressing audit findings without recording why.

## Review
- [ ] Lockfile diff reviewed; only expected packages and their dependencies changed.
- [ ] Changelogs read; breaking changes and deprecations handled.
- [ ] Tests and production build pass; new warnings addressed.
- [ ] Audit is not worse than before.
- [ ] Each commit is revertable on its own.
