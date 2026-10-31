<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Profile a slow or memory-hungry Go program

Use when a Go service or CLI is slow, uses too much memory, or has a latency tail.

Built on the cards `fm lib show go-pprof`, `fm lib show go-concurrency`, `fm lib show go-testing` and `fm lib show go-slog`.

1. **Benchmark the suspect path** so the number is repeatable: `go test -bench BenchmarkParse -benchmem -count=10 ./parse | tee old.txt`.
2. **Capture a profile on that benchmark, not on guesswork:**
   ```bash
   go test -bench BenchmarkParse -cpuprofile cpu.out -memprofile mem.out ./parse
   go tool pprof -top -cum cpu.out | head -20
   go tool pprof -sample_index=alloc_space -top mem.out | head -20
   ```
3. **Read the biggest cumulative entry that is your code**, not the runtime's. High `runtime.mallocgc` means allocations; fix those with preallocation or reuse.
4. **Goroutine and lock trouble:** a service with `net/http/pprof` shows `/debug/pprof/goroutine?debug=2` and mutex and block profiles; a growing goroutine count is a leak.
5. **Change one thing, rerun the benchmark, compare** with `benchstat old.txt new.txt`; the noise band must be smaller than the gain.
6. **Keep `go test ./... -race` green** after the change.

Pass: benchstat shows a significant delta, the allocation count or time in the profile fell where predicted, and tests still pass.

Never optimise a function that is not in the profile.
