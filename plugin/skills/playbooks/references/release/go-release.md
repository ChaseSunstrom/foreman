<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Release a Go module or binary

Use when you tag a Go library or ship a CLI built with GoReleaser.

Built on the cards `fm lib show goreleaser`, `fm lib show go-modules`, `fm lib show cobra` and `fm lib show go-testing`.

1. **Gate the commit:** `go build ./... && go vet ./... && go test ./... -race -count=1`.
2. **Tidy modules:** `go mod tidy` then `git diff --exit-code go.mod go.sum`. No local `replace` directives.
3. **Library:** a major version 2 or higher changes the module path (`/v2`); a breaking API change without it breaks every importer.
4. **Binary:** check the config and dry-run the whole build, publishing nothing:
   ```bash
   goreleaser check
   goreleaser release --snapshot --clean
   ```
   Run one built binary: `./dist/app_linux_amd64_v1/app --version`.
5. **Version is injected by ldflags**, not hand-edited; the binary prints the tag.
6. **Tag after the gates;** the push of the tag and any upload are outward and need the owner's grant.

Pass: snapshot release exits 0, the artifact runs and prints the right version, and go.mod is tidy.

Never retag a published version; Go's proxy caches it forever.
