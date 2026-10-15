---
name: goreleaser
title: GoReleaser
area: go
tags: [go, release, goreleaser, ci, packaging, checksums]
detect: [file:.goreleaser.yaml, file:.goreleaser.yml]
related: [go-modules, cobra, go-testing]
---
GoReleaser: reproducible cross-platform builds, archives, checksums, signing and changelog, validated locally before tagging.

## Verify
- `goreleaser check`: the config parses and is valid for your installed version.
- `goreleaser build --snapshot --clean --single-target`: a local build for your platform, no tag needed.
- `goreleaser release --snapshot --clean`: full pipeline dry run into `dist/` without publishing.
- `./dist/<binary>_*/<binary> --version`: ldflags injected the version.
- `sha256sum -c dist/checksums.txt` (run in `dist/`): checksums match the artifacts.

## Test first
The failing check is the config and a built binary reporting its version.
```yaml
# .goreleaser.yaml
version: 2
builds:
  - main: ./cmd/app
    env: [CGO_ENABLED=0]
    ldflags: ["-s -w -X main.version={{.Version}}"]
```
Run `goreleaser build --snapshot --clean --single-target`, then execute the binary and expect the snapshot version, not `dev`.

## Do
- Start the file with `version: 2` and let `goreleaser check` flag deprecated keys for your installed release.
- Set `CGO_ENABLED=0` for static binaries unless cgo is required; list `goos`/`goarch` explicitly and ignore unsupported combos.
- Inject version data with `-X main.version={{.Version}}` plus `{{.Commit}}` and `{{.Date}}`.
- Add `-trimpath` through `flags` and set `mod_timestamp: "{{ .CommitTimestamp }}"` for reproducible output.
- Produce `checksums.txt` and sign with cosign or GPG in the `signs` section; add an SBOM if required.
- Generate the changelog from commits with `changelog.filters` to exclude noise.
- Run in CI on tag push with `fetch-depth: 0` so git history and tags are present.
- Use `goreleaser release --snapshot` in PR CI to catch config rot early.

## Avoid
- Releasing without a snapshot run first: config errors surface at tag time. Dry run in CI.
- Shallow clone in CI: wrong version or empty changelog. Fetch full history and tags.
- Tokens hard-coded in config: pass `GITHUB_TOKEN` through the environment.
- Leaving `CGO_ENABLED` unset when cross-compiling: links against host libs and fails or isn't portable.
- Using old config keys from tutorials (v1 era names like `archives.replacements` or `brews` field renames): run `goreleaser check` and follow deprecation notices.
- Tagging from a dirty tree: the release is flagged dirty. Commit first, or `--clean` and verify `git status`.
- Publishing with `--skip=validate` to get past an error: ships a bad config. Fix it.

## Review
- [ ] `goreleaser check` and a snapshot release pass in CI.
- [ ] Version, commit and date are injected and visible in `--version`.
- [ ] Checksums are published and artifacts are signed where policy requires.
- [ ] CI fetches full history and tags; secrets come from the environment.
- [ ] Target OS and arch matrix matches what is supported.
