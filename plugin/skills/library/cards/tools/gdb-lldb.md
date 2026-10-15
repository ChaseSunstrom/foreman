---
name: gdb-lldb
title: gdb and lldb
area: tools
tags: [gdb, lldb, debugger, native, c, cpp, rust, core-dump]
detect: [file:.gdbinit, file:.lldbinit, file:launch.json]
related: [rr, memory-leaks, perf, pdb]
---
Native debugging with gdb or lldb: debug builds, breakpoints, backtraces, core dumps and batch mode.

## Verify
- `gdb -batch -ex run -ex bt --args ./prog ARGS`: run to a crash and print the backtrace non-interactively.
- `lldb -b -o run -o bt -- ./prog ARGS`: the same in lldb.
- `file ./prog`: the binary is not stripped and is built with debug info (look for "with debug_info").
- `gdb -batch -ex bt ./prog core`: a backtrace from a core file.

## Test first
Make the failure reproducible as a command with an input file, then debug that.
```sh
./prog crash-input.bin; echo $?        # expect a non-zero or signal exit
gdb -batch -ex run -ex bt --args ./prog crash-input.bin 2>&1 | tee /tmp/bt.txt
grep -q 'parse_header' /tmp/bt.txt
```
After the fix, the same input must exit 0, and it joins the test suite as a regression case.

## Do
- Build with symbols and no optimization: `-g -O0` (or `-Og`); Rust debug profile; keep frame pointers.
- Set breakpoints on functions or `file:line`; conditional with `break f if x > 3`.
- Inspect with `bt`, `frame N`, `info locals`, `print expr`, `x/16xb ADDR`; lldb: `bt`, `frame variable`, `p`, `memory read`.
- Use watchpoints (`watch var`) for who-changed-this bugs.
- Enable cores with `ulimit -c unlimited` and find them with `coredumpctl` on systemd hosts.
- Use `thread apply all bt` (gdb) or `bt all` (lldb) for hangs and deadlocks.
- Save repeating setup in `.gdbinit` or an lldb command script.
- Pair with a sanitizer build (`-fsanitize=address,undefined`) to find the cause before stepping.

## Avoid
- Debugging an optimized or stripped binary: variables show as optimized out, lines jump. Rebuild with `-g -O0`.
- Source and binary mismatch: stale build gives wrong lines. Rebuild, and check `info source`.
- Stepping through a Heisenbug and concluding it is fixed: timing changed. Use `rr` to record, or sanitizers.
- Printing through a corrupted pointer and trusting it: validate with `info proc mappings` or a sanitizer.
- Auto-loading `.gdbinit` from untrusted directories: gdb blocks this by default; do not disable the safe-path.
- Attaching to production without a plan: it halts the process. Use cores or `gdb -p` briefly with `detach`.
- Leaving breakpoints and debug prints in the committed code.

## Review
- [ ] The crash has a reproducing command and becomes a regression test.
- [ ] The fix addresses the root cause shown in the backtrace, not the symptom.
- [ ] A sanitizer or valgrind run is clean afterward.
- [ ] No debug scaffolding is committed.
