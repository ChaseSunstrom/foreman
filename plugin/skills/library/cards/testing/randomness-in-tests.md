---
name: randomness-in-tests
title: Randomness in tests
area: testing
tags: [testing, random, seed, determinism, flaky, property, fuzz]
detect: []
related: [property-based-testing, flaky-tests, fuzzing, time-in-tests]
---
Control randomness: inject or seed the generator, print the seed on failure, and assert properties instead of values.

## Verify
- `pytest -p randomly --randomly-seed=1234 -q`: reruns a failing order with a fixed seed (needs pytest-randomly).
- `go test -shuffle=1234 ./...`: reruns with a recorded shuffle seed.
- `for i in 1 2 3 4 5; do pytest -q -x || break; done`: repeats the suite to expose seed-dependent failures.
- `grep -rnE "random\.|Math\.random|rand\.(Int|Float)" src/`: finds unseeded randomness in the code under test.

## Test first
Reproduce a flaky failure by fixing the seed, then pin it as a regression.
```python
import random

def test_shuffle_keeps_all_cards():
    rng = random.Random(42)
    deck = list(range(52))
    shuffled = shuffle(deck, rng=rng)
    assert sorted(shuffled) == deck          # property, holds for any seed
    assert shuffled == shuffle(deck, rng=random.Random(42))  # reproducible
```

## Do
- Pass the generator in (`rng` parameter, injected source) so tests supply a seeded one; do not reseed the global one.
- Log the seed at test start and in the failure message so any failure can be replayed.
- Assert invariants that hold for every seed: length, ordering, membership, ranges.
- Pin a specific seed only to reproduce a known bug, with a comment on what it reproduces.
- Use property-based tools (Hypothesis, fast-check, `testing/quick`) and keep their saved failing examples.
- Generate ids and names from a counter or a seeded source in fixtures so runs are repeatable.
- Run the suite many times (a nightly loop) across seeds to find rare failures.
- Stub UUIDs, tokens and nonces at the boundary when the exact value matters.

## Avoid
- `random.seed(0)` at module top: it hides bugs and breaks other tests sharing the global state. Use a local generator.
- Asserting an exact random output from an unseeded call: flaky. Assert properties or inject the seed.
- Swallowing the seed: a failure that cannot be replayed is a wasted failure. Print it.
- Random test data without bounds (huge strings, NaN, negative lengths) in example tests: unrelated failures. Bound them or use property tests that shrink.
- Retrying a failed test until it passes: the bug stays. Replay with the seed instead.
- Using real crypto randomness in unit tests and comparing outputs: nondeterministic. Inject a deterministic source.

## Review
- [ ] Code under test accepts an injected random source.
- [ ] Seeds are logged and can be fixed on rerun.
- [ ] Assertions are invariants or use seeded values.
- [ ] No global reseeding in test modules.
- [ ] Previously failing seeds are kept as regression cases.
