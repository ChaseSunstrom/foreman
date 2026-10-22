<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Go build errors

Use when `go build`, `go vet` or `go test` fails to compile. The goal is a green build with the smallest diff that
fixes the cause: no refactors, no silenced checks. Built on the library cards `fm lib show go` (the baseline),
`fm lib show go-modules` (go.mod, go.sum, toolchains), `fm lib show go-errors` (multi-value returns, wrapping) and
`fm lib show go-testing` (when the failure is in a `_test.go` file).

## Diagnostic commands

```bash
go version                      # the toolchain actually running
go env GOOS GOARCH GOFLAGS GOTOOLCHAIN CGO_ENABLED
go build ./... 2>&1 | head -40  # compile every package
go vet ./...                    # type-checks too; catches printf, copylocks, unreachable code
go mod tidy -diff               # Go 1.23+: what tidy would change, without changing it
go list -deps ./... >/dev/null  # import cycles and missing packages, without compiling
```

## First error

Go prints one header per failing package, `# example.com/app/store`, then lines of the form
`store/db.go:42:9: message`. Read it this way:

1. **Find the lowest failing package.** When a package fails, the packages that import it are not compiled at all,
   so the first `#` header is usually the one to fix. If several headers appear, start with the one the others
   import (`go list -deps` order). Pass: you name the package and the `file:line:col` you are fixing.
2. **Fix the first line under that header**, then rebuild. The compiler stops after 10 errors per package
   (`too many errors`); errors after a broken declaration are often echoes of it.
3. **A `go:` prefix is not a compile error.** Lines starting `go: ` come from the go command (modules, toolchain,
   network), not the compiler: go to the module rows of the table, not the code.
4. **Build-constrained files.** `undefined: X` for a name you can see defined usually means its file is excluded by
   a `//go:build` line or a `_linux.go`/`_windows.go` suffix. Check with `go list -f '{{.GoFiles}} {{.IgnoredGoFiles}}' ./pkg`.

## Common causes

| Error text | Usual cause | Fix |
|---|---|---|
| `"strings" imported and not used` | Leftover import | Delete the import (or run `goimports -w FILE`) |
| `declared and not used: x` | Variable assigned, never read | Use it or delete it; never add `_ = x` to quiet it |
| `undefined: Foo` | Missing import, unexported name (`foo` vs `Foo`), file excluded by build tags | Import the package, export the name, or fix the constraint |
| `cannot use x (variable of type int) as string value in argument to f` | Type mismatch | Convert explicitly (`strconv.Itoa(x)`), not `fmt.Sprint` everywhere |
| `assignment mismatch: 1 variable but f returns 2 values` / `multiple-value f() ... in single-value context` | Ignored `error` return | `v, err := f(); if err != nil { return ..., fmt.Errorf("f: %w", err) }` |
| `T does not implement I (missing method M)` | Signature differs or method absent | Match the interface's exact signature |
| `T does not implement I (method M has pointer receiver)` | Value passed where `*T` has the method | Pass `&t` |
| `import cycle not allowed` | Two packages import each other | Move the shared types into a third package both import |
| `found packages a (a.go) and b (b.go) in DIR` | Mismatched `package` clauses in one directory | One package name per directory (`_test` suffix aside) |
| `no required module provides package X; to add it: go get X` | Dependency not in go.mod | `go get X@version`, then `go mod tidy` |
| `missing go.sum entry for module providing package X` | go.sum out of date | `go mod download X` or `go mod tidy`; commit go.sum |
| `go: go.mod requires go >= 1.24 (running go 1.22; GOTOOLCHAIN=local)` | Local toolchain older than the module needs | Install the newer Go or allow `GOTOOLCHAIN=auto`; do not lower the `go` line |
| `cgo: C compiler "gcc" not found` | cgo package, no C compiler | Install the compiler, or `CGO_ENABLED=0` if the package has a pure-Go path |

## Verify

```bash
go build ./... && go vet ./... && go test ./... && test -z "$(gofmt -l .)"
```

Pass: the line exits 0. When go.mod or go.sum changed, also `go mod tidy` followed by
`git diff --exit-code go.mod go.sum` exits 0, so the committed module files are already tidy.

## Rules

- No new `//nolint`, `_ = x` or `//go:build ignore` lines in the diff to make an error go away.
- No `replace` directive pointing at a local path left in go.mod.
- The `go` line in go.mod never moves down to suit the local toolchain.
- Rebuild after every fix; the next error you work on comes from a fresh run, not the old output.

## Stop conditions

Stop and report when the same error survives three fixes, a fix adds more errors than it removes, or the fix needs a
package to move (cycles across many packages, an API redesign).

## Report

```text
[FIXED] store/db.go:42:9  assignment mismatch: 1 variable but db.Query returns 2 values
Fix: handle the error and wrap it with %w
Build: go build ./... OK | vet OK | test OK | files: store/db.go
```
