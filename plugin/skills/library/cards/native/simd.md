---
name: simd
title: SIMD Vectorization
area: native
tags: [simd, avx2, neon, sse, intrinsics, vectorization, performance]
detect: [dep:highway, dep:xsimd, dep:simde, file:*simd*.h]
related: [cpp-modern, eigen, sanitizers, cmake]
---
SIMD in C/C++: auto-vectorization reports, intrinsics with runtime CPU dispatch, alignment, tails and scalar-reference testing.

## Verify
- `gcc -O3 -march=native -fopt-info-vec-optimized -fopt-info-vec-missed -c src/k.c`: GCC reports which loops vectorized and why others did not.
- `clang -O3 -Rpass=loop-vectorize -Rpass-missed=loop-vectorize -c src/k.c`: the same from Clang.
- `objdump -d --no-show-raw-insn build/k.o | grep -E 'vmovdqu|vpaddd|vfmadd'`: vector instructions are present.
- `grep -m1 -o 'avx2\|avx512f\|neon' /proc/cpuinfo`: what the host supports (Linux).
- `ctest --test-dir build --output-on-failure`: scalar-vs-SIMD equivalence tests pass.

## Test first
Compare the SIMD kernel against a scalar reference over awkward sizes and unaligned data.
```cpp
TEST(Sum, MatchesScalarForAllTails) {
    std::vector<float> v(1031);
    std::iota(v.begin(), v.end(), 1.0f);
    for (size_t n : {0u, 1u, 7u, 8u, 9u, 31u, 1031u})
        EXPECT_FLOAT_EQ(sum_simd(v.data() + 1, n), sum_scalar(v.data() + 1, n)); // +1: unaligned
}
```

## Do
- Write the scalar version first; check whether the compiler vectorizes it with the report flags before using intrinsics. Add `restrict`/`__restrict` and `#pragma omp simd` to help.
- When intrinsics are needed, use a portable layer (Highway, xsimd, or `std::experimental::simd`) before raw `_mm256_*` or `vld1q_*`.
- Dispatch at runtime: compile each variant with its own target (`__attribute__((target("avx2")))` or per-file `-mavx2`) and pick with `__builtin_cpu_supports("avx2")`. Never compile the whole binary with `-mavx2` if it ships to unknown CPUs.
- Use unaligned loads (`_mm256_loadu_ps`) by default; use aligned ones only with guaranteed alignment (`alignas(32)`).
- Handle the tail (n not a multiple of the width) with a scalar loop or a masked op.
- Process multiple accumulators to hide latency, then reduce horizontally once at the end.
- Test floating-point reductions with a tolerance, since reordering changes rounding.
- Benchmark on the target CPU with the compiler flags used in production; keep the scalar fallback.

## Avoid
- `-march=native` in distributed builds: illegal instruction on older CPUs. Use baseline flags plus dispatch.
- Aligned loads (`_mm256_load_ps`) on arbitrary pointers: crash. Use `loadu` or guarantee alignment.
- Reading past the end of a buffer in the tail "because it is only padding": ASan or page-fault risk. Mask or use scalar.
- Mixing AVX and legacy SSE code without `vzeroupper` between: performance penalty. Compilers insert it; hand-assembly must too.
- Assuming 512-bit is faster: downclocking on some CPUs. Measure.
- Signed overflow or shifting by counts at or above the lane width: undefined or implementation-specific results. Mask the count.
- Using intrinsics in header code compiled without the target flag: build errors or wrong dispatch. Isolate per-ISA translation units.

## Review
- [ ] A scalar reference exists, and tests cover empty, tail and unaligned inputs.
- [ ] Runtime dispatch protects older CPUs, and baseline flags are used.
- [ ] No out-of-bounds loads in tail handling (checked with ASan).
- [ ] The vectorization report or benchmark shows the intended gain.
- [ ] Float-reduction tests use tolerances.
