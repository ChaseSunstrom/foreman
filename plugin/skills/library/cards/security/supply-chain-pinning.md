---
name: supply-chain-pinning
title: Supply chain pinning
area: security
tags: [security, supply-chain, lockfile, pinning, ci, dependencies]
detect: []
related: [dependency-audit, sbom, sigstore, gitleaks, trivy]
---
Reproducible, verified dependencies: lockfiles with hashes, digest-pinned images and CI actions, install scripts off, and minimal CI token scope.

## Verify
- `npm ci --ignore-scripts`: installs exactly the lockfile, failing on drift and skipping install scripts.
- `npm audit signatures`: registry signatures and provenance for installed packages verify.
- `pip install --require-hashes -r requirements.txt`: every Python dependency matches a pinned hash.
- `git grep -nE "uses: *[^ ]+@(main|master|v[0-9]+)\b|FROM [^@ ]+(:latest)?$" -- '.github' 'Dockerfile*'`: unpinned actions and images.

## Test first
Fail CI when workflow actions or base images are not pinned by digest.
```python
import re, glob

def test_actions_and_images_are_pinned():
    for f in glob.glob(".github/workflows/*.yml"):
        for line in open(f):
            m = re.search(r"uses:\s*(\S+)@(\S+)", line)
            if m and not m.group(1).startswith("./"):
                assert re.fullmatch(r"[0-9a-f]{40}", m.group(2)), f"{f}: {line.strip()}"
    for f in glob.glob("**/Dockerfile*", recursive=True):
        for line in open(f):
            if line.startswith("FROM ") and "scratch" not in line:
                assert "@sha256:" in line, f"{f}: {line.strip()}"
```

## Do
- Commit lockfiles and install from them in CI (`npm ci`, `pip --require-hashes`, `cargo --locked`, `go mod verify`, `poetry install` or `uv sync --locked`).
- Generate hash-pinned requirements with `pip-compile --generate-hashes`.
- Pin GitHub Actions to full commit SHAs with a version comment, and pin base images by digest.
- Give CI jobs the minimum `permissions:` and prefer OIDC to stored cloud keys.
- Disable lifecycle scripts by default and allow them per package when needed.
- Update through reviewed bot PRs (Dependabot or Renovate) with a cooldown for brand-new releases.
- Check new dependencies for name typos, maintainers, and need before adding. Prefer the standard library.
- Verify provenance or signatures where the registry supports them, and keep an SBOM.

## Avoid
- `curl | sh` installers in CI or Dockerfiles: download, verify a checksum or signature, then run.
- Version ranges and `latest` in production builds: pin and update deliberately.
- Floating tags for Actions (`@v4`, `@main`): tags move. Use a SHA.
- AI-suggested packages you have not verified: hallucinated names can be squatted. Confirm the package exists and is the intended one.
- Committing a lockfile but running `npm install`: use `npm ci` so drift fails.
- Secrets exposed to pull-request workflows from forks: use restricted triggers and environments.

## Review
- [ ] Lockfiles are committed and CI installs from them strictly.
- [ ] Actions and images are pinned to immutable references.
- [ ] CI token permissions are minimal and scripts are off by default.
- [ ] New dependencies were vetted.
- [ ] Updates arrive as reviewed PRs.
