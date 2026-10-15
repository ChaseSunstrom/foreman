---
name: dependency-audit
title: Dependency auditing
area: security
tags: [security, dependencies, supply-chain, cve, lockfile, audit]
detect: [file:package-lock.json, file:yarn.lock, file:pnpm-lock.yaml, file:poetry.lock, file:uv.lock, file:Cargo.lock, file:go.sum, file:Gemfile.lock, file:composer.lock]
related: [sbom, trivy, sigstore, secrets-management, semgrep]
---
Dependency auditing: lockfiles committed, a vulnerability audit that fails CI, and review of every new or updated package.

## Verify
- `npm audit --audit-level=high`: no high or critical advisories in the npm tree (use `pnpm audit` or `yarn npm audit` for those managers).
- `pip-audit`: no known vulnerabilities in the installed Python environment (add `-r requirements.txt` to audit a file).
- `cargo audit`: the RustSec database reports no advisories for `Cargo.lock`.
- `govulncheck ./...`: Go vulnerabilities that are actually reachable in your code.
- `npm ci`: the lockfile and `package.json` agree and install cleanly.

## Test first
The failing check is the audit command itself in CI; add it, see it fail on a pinned vulnerable version, then upgrade.
```yaml
# .github/workflows/audit.yml
name: audit
on: [pull_request, schedule]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm audit --audit-level=high
```
Also keep a test that asserts the lockfile is committed (`git ls-files --error-unmatch package-lock.json`).

## Do
- Commit lockfiles and install from them in CI and builds (`npm ci`, `pip install --require-hashes -r`, `uv sync --frozen`, `cargo build --locked`).
- Run the ecosystem audit on every pull request and on a nightly schedule, and block merge on high and critical.
- Enable automated update pull requests (Dependabot or Renovate) and review the changelog and diff of each.
- Check a new package before adding: maintainers, recent activity, download history, install scripts, and whether the stdlib already covers it.
- Pin exact versions for production, and pin GitHub Actions to a commit SHA.
- Remove unused dependencies, and prefer fewer, well-maintained ones.
- Track suppressed advisories with a reason and an expiry date.

## Avoid
- `npm audit fix --force` blindly: it applies breaking major bumps. Review, then run the tests.
- Typosquatted or hallucinated package names that assistants suggest: confirm the name, publisher and repository before installing.
- Ranges like `^1.0.0` or unpinned `latest` in deployed images: builds drift and a poisoned release flows in. Pin and use the lock.
- Ignoring install scripts: `postinstall` runs arbitrary code. Use `npm ci --ignore-scripts` where feasible and audit exceptions.
- Muting an advisory with no note: it stays forever. Record the reason and recheck date.
- Auditing only direct dependencies: most CVEs are transitive. Audit the full resolved tree.

## Review
- [ ] Lockfiles are committed and used in CI.
- [ ] The audit runs on PRs and on a schedule, and fails on high.
- [ ] New packages were vetted.
- [ ] Suppressions have reasons and expiry.
- [ ] Action references are pinned.
