---
name: hadolint
title: Hadolint
area: tools
tags: [docker, dockerfile, lint, containers, shellcheck]
detect: [file:.hadolint.yaml, file:.hadolint.yml]
related: [shellcheck, yamllint, kubectl-debugging]
---
Hadolint: lints Dockerfiles against best practices and runs ShellCheck on RUN instructions.

## Verify
- `hadolint Dockerfile`: findings with DL codes (Dockerfile rules) and SC codes (shell rules).
- `hadolint --config .hadolint.yaml Dockerfile`: lint with an explicit config.
- `hadolint -f json Dockerfile`: machine-readable output for CI annotations.
- `hadolint --failure-threshold warning Dockerfile`: nonzero exit at the chosen severity and above.
- `docker build --no-cache -t t .`: the file also builds, which lint alone cannot show.

## Test first
Lint a Dockerfile holding the violation.
```
cat > /tmp/Dockerfile <<'EOF'
FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl
EOF
hadolint /tmp/Dockerfile
# expect DL3007 (pin the tag), DL3009 and DL3015 (apt cache, recommends)
```
After the fix it exits 0.

## Do
- Pin base images to a specific tag or digest, not `latest`.
- Combine `apt-get update` with install in one RUN, add `--no-install-recommends`, and remove lists in the same layer.
- Pin package versions where reproducibility matters (`apt-get install pkg=version`).
- Use `COPY` over `ADD` unless extracting an archive, and set `WORKDIR` instead of `cd`.
- Add `SHELL ["/bin/bash", "-o", "pipefail", "-c"]` before pipes in RUN.
- Set `USER` to a non-root user and add `HEALTHCHECK` for services.
- Configure `ignored:` and `trustedRegistries:` in `.hadolint.yaml`, listing rule IDs with a comment each.

## Avoid
- Ignoring DL3008 everywhere because pinning is annoying: ignore per project only when the base is itself pinned.
- Piping curl to a shell without `pipefail` (DL4006): the failure is swallowed. Set the shell, or download then verify a checksum.
- Several consecutive RUN lines: extra layers (DL3059). Merge related commands, keep cache boundaries sensible.
- Inline `# hadolint ignore=DL3018` without the reason: others cannot judge it. Put the reason on the line above.
- Linting only the root Dockerfile: lint `**/Dockerfile*` in CI, including `Dockerfile.dev`.
- Secrets in `ARG` or `ENV`: they stay in image history. Use build secrets (`RUN --mount=type=secret`).

## Review
- [ ] hadolint exits 0 at the project's failure threshold.
- [ ] Base image tags are pinned, and the final stage runs as non-root.
- [ ] Every ignore has a rule ID and a reason.
- [ ] The image still builds and the container starts.
