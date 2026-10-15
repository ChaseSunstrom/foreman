---
name: ebpf
title: eBPF
area: native
tags: [ebpf, bpf, libbpf, co-re, xdp, tracing, verifier, kernel]
detect: [dep:libbpf, dep:bcc, dep:aya, file:vmlinux.h, file:*.bpf.c, file:*.bpf.o]
related: [linux-kernel-modules, io-uring, cmake, clang-tidy]
---
eBPF programs with libbpf and CO-RE: clang BPF target, skeletons, maps, verifier constraints and bpftool inspection.

## Verify
- `clang -g -O2 -target bpf -D__TARGET_ARCH_x86 -c prog.bpf.c -o prog.bpf.o`: compiles to BPF bytecode (set the arch define for your platform).
- `bpftool gen skeleton prog.bpf.o > prog.skel.h`: generates the libbpf skeleton for the loader.
- `bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h`: type header for CO-RE.
- `sudo bpftool prog show && sudo bpftool map dump name my_map`: loaded programs and map contents.
- `sudo bpftool prog load prog.bpf.o /sys/fs/bpf/p`: load alone to read the verifier log on failure.

## Test first
Drive the program with a known event and assert on the map. For packet programs use `BPF_PROG_TEST_RUN`.
```c
// loader test (libbpf skeleton)
struct prog_bpf *s = prog_bpf__open_and_load();
ASSERT(s, "load");                              // verifier acceptance is the first failing check
prog_bpf__attach(s);
trigger_event();                                // e.g. call the traced syscall
int key = 0; __u64 val = 0;
bpf_map_lookup_elem(bpf_map__fd(s->maps.count), &key, &val);
ASSERT(val == 1, "count");
```

## Do
- Use CO-RE: include `vmlinux.h`, `<bpf/bpf_helpers.h>`, `<bpf/bpf_core_read.h>`, and read kernel fields with `BPF_CORE_READ(task, pid)`.
- Declare maps with BTF-style `struct { __uint(type, BPF_MAP_TYPE_HASH); __uint(max_entries, 1024); __type(key, u32); __type(value, u64); } m SEC(".maps");`.
- Put a license section: `char LICENSE[] SEC("license") = "GPL";` since many helpers are GPL-only.
- Use `bpf_ringbuf` (`BPF_MAP_TYPE_RINGBUF`) for events to user space over perf buffers where supported.
- Check every pointer returned by `bpf_map_lookup_elem` for NULL before use: the verifier demands it.
- Bound loops and keep stack under 512 bytes; use per-CPU array maps for large scratch data.
- Use `bpf_probe_read_user_str` and `bpf_probe_read_kernel` for memory outside the program context.
- Run the loader with the least privilege available (`CAP_BPF`, `CAP_PERFMON`) rather than full root where the kernel allows it.

## Avoid
- Dereferencing kernel or user pointers directly: verifier rejects or reads garbage. Use `bpf_probe_read_*` or CORE helpers.
- Skipping the NULL check on map lookups: "invalid mem access" at load. Add it.
- Unbounded loops or variable-size reads without clamping: verifier failure. Mask sizes (`size &= 0xff`) and use bounded `for`.
- Building without `-g`: no BTF, so CO-RE relocations fail. Add `-g` and clang with BTF support.
- Hard-coding struct offsets: breaks on other kernels. Use CORE.
- Printing with `bpf_printk` in production hot paths: slow and global. Use ring buffers or counters.
- Ignoring that tracepoint and kprobe names change across kernels: prefer stable tracepoints and check availability.

## Review
- [ ] Program loads on the minimum supported kernel, and the verifier log is clean.
- [ ] CO-RE reads replace direct field access.
- [ ] Map sizes and lifetimes are bounded, and per-CPU contention is considered.
- [ ] Privilege required by the loader is documented and minimal.
- [ ] A test triggers an event and asserts the map or ring-buffer output.
