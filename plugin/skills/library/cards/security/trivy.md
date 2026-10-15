---
name: trivy
title: Trivy
area: security
tags: [security, trivy, containers, vulnerabilities, iac, scanning]
detect: [file:trivy.yaml, file:trivy.yml, file:.trivyignore, file:.trivyignore.yaml, file:trivy-secret.yaml]
related: [sbom, dependency-audit, secrets-management, sigstore]
---
Trivy: scan images, filesystems and IaC for vulnerabilities, secrets and misconfiguration, and fail CI at a chosen severity.

## Verify
- `trivy image --severity HIGH,CRITICAL --exit-code 1 IMAGE:TAG`: the built image has no high or critical findings.
- `trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1 .`: the repo has no vulnerable lockfile entries, secrets or risky config.
- `trivy config --exit-code 1 .`: Dockerfile, Terraform and Kubernetes manifests pass misconfiguration checks.
- `trivy image --format cyclonedx --output sbom.cdx.json IMAGE:TAG`: an SBOM is produced.

## Test first
The failing check is the scan: run it on the current image, see the findings, then fix them. Keep it in CI.
```yaml
# .github/workflows/trivy.yml
name: trivy
on: [pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t app:ci .
      - run: trivy image --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed app:ci
```
Store defaults in `trivy.yaml` so CI and local runs match.

## Do
- Scan the image you ship, after the final build, not just the source tree.
- Use `--exit-code 1` with `--severity HIGH,CRITICAL` so the job fails, and `--ignore-unfixed` to skip issues with no patch.
- Choose the scanners explicitly with `--scanners vuln,secret,misconfig`.
- Fix by updating the base image tag or digest and rebuilding, then pin the base by digest.
- Record accepted findings in `.trivyignore` (one id per line) or `.trivyignore.yaml` with a reason and `expired_at` date.
- Rescan published images on a schedule, since new advisories appear after the build.
- Cache the vulnerability database in CI (`TRIVY_CACHE_DIR`) to avoid rate limits and slow runs.
- Use minimal base images (distroless, slim, alpine) to shrink the findings.

## Avoid
- Running without `--exit-code`: the default exit status is 0 even with findings, so CI always passes. Add `--exit-code 1`.
- Scanning only `latest` or an old tag: you audit the wrong artifact. Scan the exact tag or digest that deploys.
- A `.trivyignore` full of bare CVE ids: they never get reviewed. Add comments and expiry dates.
- Treating vulnerability scans as a secrets or config check by default: pick scanners explicitly.
- Ignoring base-image OS packages because "the app is fine": they run in your container. Update the base.
- Using `--skip-db-update` on a stale cache: results are outdated. Refresh the database on a schedule.

## Review
- [ ] CI scans the built image and fails at HIGH and CRITICAL.
- [ ] Scanner types are explicit.
- [ ] Ignored ids carry reasons and expiry.
- [ ] Base images are pinned and kept current.
- [ ] Published images are rescanned on a schedule.
