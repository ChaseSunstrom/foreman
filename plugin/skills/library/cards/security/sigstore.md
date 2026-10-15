---
name: sigstore
title: Sigstore and cosign
area: security
tags: [security, sigstore, cosign, signing, supply-chain, provenance]
detect: [dep:sigstore, file:cosign.pub, file:cosign.key, file:.github/workflows/release.yml]
related: [sbom, dependency-audit, trivy, secrets-management]
---
Sigstore: sign artifacts with short-lived keyless identities from CI, and verify the signer identity and issuer before deploying.

## Verify
- `cosign sign --yes IMAGE@sha256:DIGEST`: the image digest is signed (keyless in CI with an OIDC token).
- `cosign verify IMAGE@sha256:DIGEST --certificate-identity-regexp "^https://github.com/ORG/REPO/" --certificate-oidc-issuer https://token.actions.githubusercontent.com`: the signature matches the expected workflow identity and issuer.
- `cosign verify-attestation --type cyclonedx IMAGE@sha256:DIGEST --certificate-identity-regexp "^https://github.com/ORG/REPO/" --certificate-oidc-issuer https://token.actions.githubusercontent.com`: the SBOM attestation verifies.

## Test first
The failing check is the verification step in the deploy gate: it fails for an unsigned or wrongly signed image.
```bash
#!/usr/bin/env bash
set -euo pipefail
img="$1"
cosign verify "$img" \
  --certificate-identity-regexp '^https://github.com/ORG/REPO/\.github/workflows/release\.yml@' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com >/dev/null \
  || { echo "unsigned or untrusted image: $img" >&2; exit 1; }
```
Run it against an image you did not sign and expect exit 1.

## Do
- Sign in CI with keyless signing: grant the job `id-token: write`, and install cosign with `sigstore/cosign-installer`.
- Sign by digest (`image@sha256:...`), not by mutable tag, and deploy by digest.
- Verify with both `--certificate-identity` (or regexp) and `--certificate-oidc-issuer`. Anchor the regexp.
- Enforce verification at admission with a policy controller (Kubernetes Sigstore policy-controller or Kyverno `verifyImages`).
- Attach attestations (SBOM, SLSA provenance) with `cosign attest` and check them before promotion.
- For Python or npm packages, use trusted publishing and the `sigstore` client to sign and verify release files.
- If keys are required (air-gapped), keep the private key in a KMS, protect it with a passphrase, and rotate it.

## Avoid
- `cosign verify` with no identity and issuer flags: any signer passes. Always pin both.
- Signing a tag: the tag can move after signing. Sign the digest.
- Unanchored identity regexps like `.*github.com/ORG`: another repo's workflow matches. Anchor with `^` and the full workflow path.
- Committing `cosign.key` or passphrases: use keyless or a KMS. Treat a leaked key as compromise.
- Signing in CI but never verifying at deploy time: signatures protect nothing unless checked. Add an admission policy.
- Using long-lived signing credentials as a CI secret where keyless works: prefer OIDC identity.

## Review
- [ ] CI signs by digest, keylessly or via KMS.
- [ ] Verification pins identity and issuer.
- [ ] Deploy or admission rejects unsigned images.
- [ ] Attestations are attached and verified.
- [ ] No private signing key is in the repo.
