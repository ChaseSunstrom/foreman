<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Verify a Go change

Use when a Go package changed and you must show it is correct, race-free and tidy before calling it done.

Built on the cards `fm lib show go-testing`, `fm lib show go-fuzzing`, `fm lib show testify`, `fm lib show go-concurrency` and `fm lib show go-modules`.

1. **Test first, table-driven.** The failing case goes in the package's table with a named subtest; run only it: `go test ./store -run 'TestQuery/empty_input' -count=1`.
2. **Whole module, uncached, with the race detector:**
   ```bash
   go test ./... -race -count=1
   go vet ./...
   test -z "$(gofmt -l .)"
   ```
3. **Parsers and decoders get a fuzz target** (`func FuzzParse(f *testing.F)`); run it for a bounded time: `go test ./parse -fuzz FuzzParse -fuzztime 20s`. Commit any crashing input from `testdata/fuzz`.
4. **Goroutines:** every one has an owner that waits for it or a context that stops it. A test that leaks one fails under `-race` or a goroutine count check.
5. **Modules:** if go.mod or go.sum changed, `go mod tidy` then `git diff --exit-code go.mod go.sum`.

Pass: all three lines exit 0, the new test fails on the old code, and the module files are tidy.

Never use `-count=1` removal or `t.Skip` to get a green run.
