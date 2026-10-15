---
name: go-fuzzing
title: Go native fuzzing
area: go
tags: [go, fuzzing, testing, security, corpus, parsers]
detect: [file:testdata/fuzz/*]
related: [go-testing, testify, go-errors, go-generics]
---
Native Go fuzzing (go test -fuzz): fuzz targets for parsers and decoders, round-trip properties and corpus management.

## Verify
- `go test ./...`: runs seed corpus and saved failures as regular tests.
- `go test -fuzz=FuzzParse -fuzztime=30s ./pkg/parse`: actively fuzzes one target for a bounded time (one package, one target at a time).
- `go test -run=FuzzParse/seed ./pkg/parse`: replays a specific corpus entry.
- `git status testdata/fuzz`: new failing inputs are committed.

## Test first
The fuzz target is the test: seed it, then let the fuzzer find the failing input.
```go
func FuzzRoundTrip(f *testing.F) {
	f.Add("hello")
	f.Add("")
	f.Fuzz(func(t *testing.T, s string) {
		got, err := Decode(Encode(s))
		if err != nil || got != s {
			t.Fatalf("roundtrip(%q) = %q, %v", s, got, err)
		}
	})
}
```
Failures are written to `testdata/fuzz/FuzzRoundTrip/<hash>`; keep them as regression tests.

## Do
- Name targets `FuzzXxx(f *testing.F)` in `_test.go` files; add seeds with `f.Add(...)` covering valid, edge and known-bad inputs.
- Use supported arg types only: `string`, `[]byte`, ints, floats, `bool`, `rune`.
- Assert properties: no panic, round trip equality, idempotence, equivalence with a simple reference, error-or-valid.
- Make the body fast and deterministic: no network, clock, global state or goroutines that outlive the call.
- Bound input work (reject huge lengths early) so the fuzzer explores breadth.
- Run longer in a scheduled CI job with `-fuzztime`, and cache `$GOCACHE/fuzz`.
- Commit crashers under `testdata/fuzz` and fix the bug, then keep the file.

## Avoid
- A fuzz target with side effects or shared state: results aren't reproducible. Reset or avoid state.
- Asserting on exact error text from mutated input: noisy. Assert error versus valid.
- Fuzzing several targets in one command: `-fuzz` must match exactly one target in one package.
- Deleting `testdata/fuzz` entries after the fix: loses the regression. Keep them.
- Seeds only of the happy path: the fuzzer starts blind. Add structurally varied seeds.
- Expecting fuzzing in plain `go test`: without `-fuzz` it only replays the corpus.
- Slow targets (ms per exec): coverage grows slowly. Trim work per call.

## Review
- [ ] Targets exist for every parser, decoder and untrusted-input boundary.
- [ ] Seeds cover valid and malformed inputs; crashers are committed.
- [ ] Properties go beyond "does not panic" where possible.
- [ ] Bodies are deterministic and fast.
- [ ] CI runs a bounded fuzz pass on a schedule.
