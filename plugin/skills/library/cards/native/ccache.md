---
name: ccache
title: ccache
area: native
tags: [cpp, c, build, cache, ci, cmake, speed]
detect: [file:ccache.conf, file:.ccache.conf]
related: [cmake, bazel, meson, clang-tidy, vcpkg]
---
ccache: compiler cache wired through CMake launchers, with hit-rate checks and the settings that make hits reliable in CI.

## Verify
- `ccache --zero-stats && cmake --build build -j && ccache --show-stats`: baseline cold build.
- `cmake --build build --clean-first -j && ccache --show-stats`: second pass should show mostly cache hits.
- `ccache --show-config | grep -E 'max_size|base_dir|compiler_check|sloppiness'`: effective settings.
- `ccache -z && ccache --show-stats -v`: verbose counters show why misses happen (for example "unsupported compiler option").

## Test first
The check that fails first is the hit rate: a rebuild with no changes must hit.
```sh
ccache -C -z
cmake -S . -B build -DCMAKE_CXX_COMPILER_LAUNCHER=ccache && cmake --build build -j
cmake --build build --clean-first -j
ccache --show-stats   # expect hits roughly equal to compiled files
```
If hits are zero, a flag or macro differs between runs (see Avoid).

## Do
- Enable per configure: `-DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache`. Prefer this over symlinking compilers.
- Set `max_size` (for example `ccache -M 5G`) and persist it in `ccache.conf` or the `CCACHE_MAXSIZE` env var.
- Set `CCACHE_BASEDIR` (or `base_dir`) to the repo root so absolute paths do not defeat hits across checkouts.
- Keep the cache across CI runs (cache the `CCACHE_DIR` directory keyed on the compiler version and OS).
- Add `CCACHE_COMPILERCHECK=content` when the compiler binary is replaced in place with the same mtime.
- With precompiled headers, set `sloppiness = pch_defines,time_macros` and read the ccache docs on your compiler.
- Use `-fdebug-prefix-map` or `-ffile-prefix-map` for path-independent debug info.

## Avoid
- `__DATE__`/`__TIME__` in sources: every build misses. Remove them or set `sloppiness = time_macros` for known-safe cases.
- Unity builds or huge precompiled headers with no measurement: they can reduce cache reuse. Measure with `--show-stats`.
- Running `ccache -C` as a fix for odd output: hides a real bug in flags. Find the miss reason with `-v`.
- Trusting stale cached objects after toolchain changes without compiler check: configure `compiler_check`.
- Passing launcher through MSVC with `/Zi`: ccache cannot cache it. Use `/Z7` (`CMAKE_MSVC_DEBUG_INFORMATION_FORMAT=Embedded`).
- Sharing a cache directory between users without matching umask: permission errors.

## Review
- [ ] Launcher variables are set in presets or CI, not hard-coded into CMakeLists.
- [ ] Hit rate on a no-change rebuild is high, and the number is recorded.
- [ ] `base_dir` is set and the cache size is bounded.
- [ ] No time macros or non-deterministic flags in the build.
