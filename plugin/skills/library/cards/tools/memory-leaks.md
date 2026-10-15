---
name: memory-leaks
title: Memory leaks
area: tools
tags: [memory, leaks, valgrind, asan, heap, profiling]
detect: []
related: [gdb-lldb, perf, node-inspector, py-spy]
---
Find and prove memory leaks: measure growth over repeated work, then locate the allocation with a heap tool.

## Verify
- `valgrind --leak-check=full --show-leak-kinds=all ./prog ARGS`: definite and possible leaks with allocation stacks (native code).
- `ASAN_OPTIONS=detect_leaks=1 ./prog`: AddressSanitizer's LeakSanitizer report from a `-fsanitize=address` build.
- `python -X tracemalloc=10 script.py`: Python allocation tracking with 10-frame stacks (read with `tracemalloc.take_snapshot()`).
- `node --heap-prof script.js`: allocation sampling profile for Node.
- `ps -o rss= -p PID`: resident memory sampled over time shows whether it plateaus.

## Test first
The failing test repeats an operation and asserts that memory is flat.
```python
import tracemalloc

def test_handler_does_not_leak():
    handle()                       # warm up caches
    tracemalloc.start()
    a = tracemalloc.take_snapshot()
    for _ in range(1000): handle()
    b = tracemalloc.take_snapshot()
    growth = sum(s.size_diff for s in b.compare_to(a, "filename"))
    assert growth < 100_000
```
Native: run the same loop under ASan or valgrind in CI.

## Do
- Distinguish a leak (unbounded growth with repeated work) from a high but stable footprint: sample RSS over time.
- Warm up first, then compare snapshots before and after N iterations.
- Take two heap snapshots and diff them: in Chrome DevTools for Node, `tracemalloc` for Python, `heaptrack` or `valgrind --tool=massif` for native.
- Look for classic roots: unbounded caches and maps, listeners never removed, global lists, timers and closures holding objects, threads that never exit.
- Bound caches with a size or TTL (`functools.lru_cache(maxsize=...)`, LRU maps); remove listeners on teardown.
- In C and C++ use RAII and smart pointers; in Rust look for reference cycles (`Rc` plus `RefCell`) and use `Weak`.
- Fix, then run the same repetition test to show growth is flat.

## Avoid
- Calling steady RSS growth a leak without checking: allocators keep freed memory and caches warm up. Look for growth that continues past warm-up.
- Reading valgrind "still reachable" as a leak: those are reachable at exit. Focus on "definitely lost" first.
- Running leak tests only once: noise. Loop many iterations and compare.
- Forgetting memory outside the language heap (native extensions, file descriptors, mmap, GPU): the language tool shows nothing. Check `/proc/PID/status` and `lsof -p PID | wc -l`.
- `del` or `gc.collect()` as the fix without finding the reference holding the object: use `gc.get_referrers` or a heap diff.
- Testing a debug build only: behavior differs. Verify on the release build too.

## Review
- [ ] Growth reproduced with a repeatable loop and measured.
- [ ] The retaining reference or allocation site was identified, not guessed.
- [ ] A test or CI sanitizer run shows flat memory after the fix.
- [ ] Caches and registries have bounds and cleanup.
