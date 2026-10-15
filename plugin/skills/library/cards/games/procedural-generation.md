---
name: procedural-generation
title: Procedural generation
area: games
tags: [procedural, noise, seed, dungeon, terrain, wave-function-collapse]
detect: [dep:opensimplex, dep:simplex-noise, dep:noise, dep:fastnoiselite, dep:FastNoiseLite]
related: [game-loop, pathfinding]
---
Procedural content: seeded, deterministic generators with validated output, tested on many seeds, never on one lucky map.

## Verify
- Run the project's test target (for example `pytest -q` or `npm test`): the generator passes its property tests on many seeds.
- `grep -rnE "Math\.random|random\.random\(|rand\(\)|Random\(\)" src/gen`: finds unseeded randomness inside generators.
- `grep -rnE "for .* in .*dict|Object\.keys|HashSet|\.values\(\)" src/gen`: finds iteration over unordered collections that can break determinism.

## Test first
Test invariants over a range of seeds, plus same-seed equality.
```python
@pytest.mark.parametrize("seed", range(200))
def test_level_is_always_solvable(seed):
    lvl = generate(seed=seed, size=(40, 30))
    assert lvl.start != lvl.exit
    assert path_exists(lvl.grid, lvl.start, lvl.exit)

def test_same_seed_same_level():
    assert generate(seed=7) == generate(seed=7)
```

## Do
- Thread one seeded RNG object through the generator. Derive child seeds per layer or chunk by hashing (seed, coordinates), so generation order never matters.
- Generate in stages (layout, then connectivity, then decoration), and validate each stage before the next.
- Express rules as invariants (reachable, no overlaps, bounded size) and check them after generation. Retry with a derived seed or repair when they fail, capped at a fixed attempt count.
- Layer noise as octaves (frequency doubles, amplitude halves) and remap the result to the range you need. Normalise it once at the end.
- Chunk large worlds and generate each chunk from (world seed, chunk coordinates) so chunks are reproducible on demand.
- Log the seed with every bug report and every run. Provide a way to enter a seed.
- Keep generation separate from instantiation so the data can be tested without an engine.

## Avoid
- Global random state: replays and tests diverge. Pass an RNG instance.
- Depending on dict, set or hash iteration order: it changes between runs or platforms. Sort keys before use.
- Floating-point noise compared for equality across platforms: tiny differences change tiles. Quantise to integers before decisions.
- Unbounded retry loops: rare seeds hang. Cap attempts and fall back to a known-good template.
- Trusting visual inspection of one seed: failures live in the tail. Run hundreds of seeds in CI.
- Generating at spawn time on the main thread: frame hitch. Pre-generate or use a worker.

## Review
- [ ] Same seed always yields identical output, with a test.
- [ ] Invariants (reachable, in bounds, no overlap) are asserted over many seeds.
- [ ] Retries are capped and have a fallback.
- [ ] Seeds are logged and settable.
- [ ] No unordered iteration or global RNG in generation code.
