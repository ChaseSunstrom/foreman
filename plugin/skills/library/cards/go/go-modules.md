---
name: go-modules
title: Go modules
area: go
tags: [go, modules, dependencies, workspace, build, vendoring]
detect: [file:go.mod, file:go.sum, file:go.work]
related: [go-testing, go-concurrency, cobra]
---
Go modules: go.mod hygiene, reproducible builds, upgrades, workspaces and the build and vet loop.

## Verify
- `go build ./...`: every package compiles.
- `go vet ./...`: common mistakes the compiler allows.
- `go mod tidy -diff`: go.mod and go.sum are already tidy (exits non-zero if not; needs a recent Go toolchain, else run `go mod tidy` and check `git diff`).
- `go mod verify`: cached modules match go.sum hashes.
- `go list -m -u all`: available dependency upgrades.

## Test first
Tests are `*_test.go` beside the code, run per package or for the module. The first failing check for a dependency change is the build.
```go
// parse_test.go
package cfg

import "testing"

func TestParsePortRejectsRange(t *testing.T) {
	if _, err := ParsePort("70000"); err == nil {
		t.Fatal("expected error")
	}
}
```
Run `go test ./... -run TestParsePort`. After any `go.mod` edit, run `go build ./... && go test ./...`.

## Do
- Set the module path in `go.mod` to the import path used by consumers. A v2 or higher module ends in `/v2`.
- Run `go mod tidy` after adding or removing imports, and commit both `go.mod` and `go.sum`.
- Add deps with `go get module@version`. Upgrade one with `go get -u module`, not `go get -u ./...` blindly.
- Use the `go` and `toolchain` directives deliberately. Keep the `go` line to the minimum version actually required.
- Use `go.work` for multi-module local development, and don't commit it unless the repo is meant to work that way.
- Use `replace` only temporarily or for forks, with a comment on why and when to remove it.
- Build in CI with `-mod=readonly` (the default), so go.mod is never silently edited.
- Run `govulncheck ./...` when available for known-vulnerable dependencies.

## Avoid
- Editing `go.sum` by hand: run `go mod tidy` or `go mod download`.
- Committing a `replace` that points at a local path: other machines can't build. Use a version or a workspace.
- Importing `internal/` packages from another module: the compiler forbids it. Move the package out.
- Major-version import mismatches (`/v2` in go.mod but not in imports): "module declares its path as" errors. Fix the import paths.
- `GOFLAGS=-mod=mod` in CI: it hides drift. Keep readonly.
- `go get` for installing tools in a module: use `go install tool@version`, or the `tool` directive in recent Go.
- Vendoring without `go mod vendor` in CI: stale vendor dirs. Check with `go mod vendor` then `git diff`.

## Review
- [ ] go.mod and go.sum changes match the intended dependency edits.
- [ ] No stray `replace` directives.
- [ ] The `go` directive is not raised without need.
- [ ] New dependencies are justified, versioned and maintained.
- [ ] Build, vet and tests pass with the readonly default.
