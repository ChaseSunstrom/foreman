<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Profiling

Use when you know something is slow but not where (pair with benchmark-loop.md for the before/after).

1. **Reproduce the slow path** with a fixed input and a timer; record the baseline (median of ≥ 5 runs).
2. **Profile before guessing:**
   - Python: `python -m cProfile -s cumtime script.py | head -40`; `py-spy record -o p.svg -- python script.py` for live processes.
   - Node/TS: `node --cpu-prof script.js`, open the .cpuprofile; `clinic flame` for servers.
   - Rust: `cargo build --release` then `perf record -g ./target/release/x; perf report`, or `cargo flamegraph`.
   - C/C++: `perf record -g`, `valgrind --tool=callgrind` + `kcachegrind`.
   - Shell/CI: `time` each step; `strace -c` for syscall-heavy work.
3. **Read the profile top-down:** the widest frames by inclusive time; distinguish CPU-bound, I/O-bound (waiting), and allocation-bound.
4. **Fix the biggest frame first**, one change at a time, re-measure after each; stop when the target is met.
5. **Record** baseline → after numbers as evidence (`--section Measurements`).
