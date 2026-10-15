---
name: sbom
title: Software bill of materials
area: security
tags: [security, sbom, cyclonedx, spdx, supply-chain, compliance]
detect: [file:*.cdx.json, file:*.spdx.json, file:sbom.json, dep:cyclonedx-bom, dep:@cyclonedx/cyclonedx-npm, dep:cyclonedx-py]
related: [dependency-audit, trivy, sigstore, secrets-management]
---
SBOM: generate a CycloneDX or SPDX inventory from the built artifact on every release, sign it, and scan it for vulnerabilities.

## Verify
- `syft dir:. -o cyclonedx-json=sbom.cdx.json`: an SBOM is generated from the source tree.
- `syft IMAGE:TAG -o spdx-json=sbom.spdx.json`: an SBOM is generated from the built image.
- `trivy sbom sbom.cdx.json --severity HIGH,CRITICAL --exit-code 1`: the SBOM itself has no serious known vulnerabilities.
- `jq '.components | length' sbom.cdx.json`: the SBOM is non-empty.

## Test first
The failing check is an assertion on the generated file, wired into the release job.
```python
import json, subprocess
def test_sbom_lists_runtime_dependencies(tmp_path):
    out = tmp_path / "sbom.cdx.json"
    subprocess.run(["syft", "dir:.", "-o", f"cyclonedx-json={out}"], check=True)
    sbom = json.loads(out.read_text())
    names = {c["name"] for c in sbom["components"]}
    assert sbom["bomFormat"] == "CycloneDX"
    assert "requests" in names  # a known runtime dependency
```

## Do
- Generate the SBOM from the final artifact (image, wheel, binary) as well as from the lockfile, since they differ.
- Pick one standard format (CycloneDX or SPDX) and keep it consistent across projects.
- Publish the SBOM next to the release and attach it to the image as an attestation (`cosign attest --type cyclonedx`).
- Sign the SBOM or its attestation so consumers can verify provenance.
- Feed the SBOM to a vulnerability scanner on a schedule, so new advisories surface against old releases.
- Include direct and transitive dependencies with versions, licenses and hashes where the tool supports them.
- Store each release's SBOM under a version key so incidents can be answered quickly ("which releases ship library X").

## Avoid
- Generating the SBOM once, by hand, at audit time: it is stale at the next release. Generate it in CI.
- Producing it from `package.json` or `requirements.txt` alone: ranges differ from what shipped. Use the lockfile or the artifact.
- Treating an SBOM as a vulnerability report: it lists components only. Scan it.
- Omitting OS packages from container SBOMs: use an image scan, not only a language-level generator.
- Publishing unsigned SBOMs and expecting trust: tampering goes unseen. Sign or attest.
- Leaving internal path names or private package names in a public SBOM: review before publishing.

## Review
- [ ] The release pipeline generates an SBOM for the shipped artifact.
- [ ] The format is standard and the file is non-empty.
- [ ] It is signed or attested and published with the release.
- [ ] It is scanned on a schedule.
- [ ] It includes transitive and OS-level components.
