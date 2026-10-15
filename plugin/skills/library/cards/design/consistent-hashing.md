---
name: consistent-hashing
title: Consistent hashing
area: design
tags: [hashing, partitioning, ring, sharding, caching, load-balancing]
detect: []
related: [sharding, caching, cache-invalidation, leader-election, multi-region]
---
Map keys and nodes onto a hash ring with virtual nodes so adding or removing a node moves only about 1/N of the keys.

## Verify
- `pytest -q -k ring`: balance, movement and determinism tests.
- `python -c "import hashlib; print(hashlib.md5(b'k').hexdigest())"`: the hash is stable across processes (never the built-in `hash()` for strings).
- `git grep -nE "\bhash\(" -- src`: no use of the per-process randomised `hash()` for routing.

## Test first
Pin minimal movement on node add, and balance.
```python
def test_adding_node_moves_about_one_nth():
    keys = [f"k{i}" for i in range(10_000)]
    r1 = Ring(["a", "b", "c", "d"], vnodes=200)
    before = {k: r1.get(k) for k in keys}
    r2 = Ring(["a", "b", "c", "d", "e"], vnodes=200)
    moved = sum(before[k] != r2.get(k) for k in keys)
    assert 0.12 < moved / len(keys) < 0.30           # about 1/5
    assert all(r2.get(k) == "e" for k in keys if before[k] != r2.get(k))

def test_same_input_same_node_across_processes():
    assert Ring(["a", "b"], 100).get("user:1") == "a"   # pinned golden value
```

## Do
- Hash with a stable, well-mixed function (xxhash, murmur3, md5 or sha1 truncated). Same function on every client.
- Use 100 to 500 virtual nodes per physical node; weight by capacity with proportional vnode counts.
- Look up by binary search over the sorted ring; the owner is the first vnode clockwise.
- For replication, walk clockwise to the next N distinct physical nodes.
- Alternatives when you need tighter balance: rendezvous (highest random weight) hashing, or jump hash for numbered shards.
- Keep ring membership versioned and propagate it atomically; migrate data on change, with reads falling back to the old owner meanwhile.

## Avoid
- `hash(key) % N`: nearly every key moves when N changes. Use a ring or jump hash.
- Few vnodes: skewed load. Increase and measure the max/mean ratio.
- Python `hash()` or per-language-seeded hashes: routing differs between processes. Use a fixed algorithm.
- Different membership views across clients: split ownership. Distribute a versioned map.
- Forgetting hot keys: hashing does not fix them. Split or cache the key.

## Review
- [ ] Hash function fixed and identical across all clients.
- [ ] Movement on add and remove tested against 1/N.
- [ ] Balance measured with the chosen vnode count.
- [ ] Membership changes are versioned and migration path exists.
