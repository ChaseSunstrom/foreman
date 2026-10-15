---
name: fuzzing
title: Fuzzing
area: testing
tags: [fuzz, coverage-guided, corpus, crashes, parsers, security]
detect: [file:fuzz/*, file:*_fuzz_test.go, dep:cargo-fuzz, dep:atheris, dep:jazzer]
related: [property-based-testing, regression-tests, mutation-testing]
---
Coverage-guided fuzzing feeds mutated inputs to parsers and decoders to find crashes, hangs and invariant breaks; every finding becomes a permanent test.

## Verify
- `go test -fuzz=FuzzParse -fuzztime=30s ./pkg`: native Go fuzzing runs the target; failures are written under `testdata/fuzz`.
- `cargo fuzz run parse_target -- -max_total_time=60`: libFuzzer target runs for a minute (needs cargo-fuzz).
- `go test ./...`: saved corpus entries run as normal tests.
- `python fuzz_target.py -atheris_runs=100000`: Atheris runs a bounded number of iterations (when the script calls `atheris.Fuzz()`).

## Test first
Write the harness and the invariant before fixing a bug; a crash input is the failing test.
```go
func FuzzParse(f *testing.F) {
	f.Add("1.2.3")
	f.Fuzz(func(t *testing.T, s string) {
		v, err := Parse(s)
		if err == nil && v.String() != s {
			t.Errorf("round trip: %q -> %q", s, v.String())
		}
	})
}
```
Targets live in `*_test.go` (Go) or `fuzz/fuzz_targets/` (cargo-fuzz).

## Do
- Target code that takes untrusted bytes: parsers, decoders, deserializers, protocol handlers.
- Assert invariants inside the target: no panic, round trip, decode then encode equality.
- Seed with real samples (`f.Add`, corpus directory) and a dictionary for formats with tokens.
- Keep the target fast and deterministic: no network, disk, global state or clock.
- Run short in CI, long on a schedule; cache the corpus between runs.
- Commit minimized crash files as regression inputs (`testdata/fuzz/FuzzX/...`).
- Run under sanitizers for native code (ASan, UBSan).

## Avoid
- Targets with randomness or state carried across calls: findings do not reproduce. Reset state per input.
- Only asserting "does not panic": misses logic errors. Add round trip or differential checks.
- Unbounded allocation or recursion in the target: out-of-memory noise. Cap input size.
- Fuzzing without seeds: slow to reach deep code. Add valid samples.
- Fixing the crash but dropping the input: it regresses silently. Keep it in the corpus.
- Running fuzz in the default PR job for minutes: slows feedback. Use a time box and a nightly job.

## Review
- [ ] Target checks an invariant beyond non-crash.
- [ ] Seed corpus has valid and edge samples.
- [ ] Crash inputs are committed as regression tests.
- [ ] Target is deterministic, hermetic and size-limited.
- [ ] CI time-boxes fuzzing and a longer run exists elsewhere.
