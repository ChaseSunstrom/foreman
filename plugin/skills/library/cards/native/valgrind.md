---
name: valgrind
title: Valgrind
area: native
tags: [valgrind, memcheck, helgrind, leaks, debugging, c, cpp]
detect: [file:*.supp, file:valgrind.supp]
related: [sanitizers, googletest, cmake, meson, embedded-c]
---
Valgrind on Linux: Memcheck for invalid access and leaks, Helgrind/Callgrind for races and profiling, on unmodified debug binaries.

## Verify
- `valgrind --leak-check=full --show-leak-kinds=all --error-exitcode=1 ./build/mytests`: any memory error or leak gives a non-zero exit.
- `valgrind --track-origins=yes ./build/app`: uninitialised-value reports point to where the value came from.
- `valgrind --tool=helgrind ./build/app`: potential data races and lock-order problems.
- `valgrind --tool=callgrind ./build/app && callgrind_annotate callgrind.out.*`: where instructions go.

## Test first
Reproduce the leak or invalid access in a test, run it under Memcheck with `--error-exitcode`, watch it fail, then fix.
```c
void test_parse_frees_on_error(void) {
    for (int i = 0; i < 100; i++)
        assert(parse("bad input") == NULL);   /* leaks 100 blocks before the fix */
}
```
```
valgrind --leak-check=full --error-exitcode=1 ./test_parse
```
Non-zero before the fix, zero after ("All heap blocks were freed").

## Do
- Compile with `-g -O0` (or `-O1`) and no sanitizers; keep frame info so stacks have file and line.
- Read the first error in the log first; later ones are often consequences.
- Keep a suppression file for third-party noise (`--gen-suppressions=all`, then `--suppressions=valgrind.supp`) with a comment per entry.
- Use `--num-callers=30` for deeper stacks, and `--log-file=vg.%p.log` for multi-process programs (`--trace-children=yes`).
- Wire it into the test runner (`meson test --wrap=valgrind`, CTest `MemoryCheckCommand` with `ctest -T memcheck`).
- Read the leak categories: "definitely lost" and "indirectly lost" are real, "still reachable" is usually a global.
- Use `--vgdb=yes` with `gdb` and `target remote | vgdb` to break at the first error.

## Avoid
- Running optimised (-O2/-O3) binaries: reports become hard to map and some uninitialised-value reports are false. Use a debug build.
- Combining Valgrind with ASan/TSan binaries: they clash. Run one at a time on separate builds.
- Ignoring "conditional jump depends on uninitialised value": it is a real bug even if the program seems to work.
- Treating "still reachable" as clean or "definitely lost" as fine at exit: audit ownership, then free or document.
- Running without `--error-exitcode` in CI: errors print but the job passes.
- Expecting Valgrind on macOS arm64 or Windows: unsupported or unreliable; use sanitizers there.

## Review
- [ ] Memcheck is clean with no unexplained suppressions.
- [ ] CI uses `--error-exitcode` and a debug build.
- [ ] Every suppression has a comment and names a third-party frame.
- [ ] Threaded code was also run under Helgrind or TSan.
- [ ] Fixes come with a test that fails under Memcheck first.
