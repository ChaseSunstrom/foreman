---
name: io-uring
title: io_uring
area: native
tags: [linux, io-uring, liburing, async, io, networking, c]
detect: [dep:liburing, dep:io-uring, dep:tokio-uring]
related: [cpp-concurrency, cpp-coroutines, ebpf, linux-kernel-modules, boost]
---
io_uring via liburing: submission and completion queues, user_data ownership, short reads, linked ops, buffer lifetime and kernel feature probing.

## Verify
- `gcc -Wall -Wextra -o app app.c -luring`: links liburing.
- `uname -r`: the kernel version supports the opcodes you use (probe at runtime too).
- `strace -f -e trace=io_uring_setup,io_uring_enter,io_uring_register ./app`: the app batches submissions rather than calling enter per op.
- `cat /proc/sys/kernel/io_uring_disabled`: shows whether the system restricts io_uring (a sandbox or hardened config may deny it).
- `./app --selftest`: a program-provided check that submits ops and verifies each CQE result.

## Test first
Submit one op and assert on the completion result. The failing case is a short or errored CQE.
```c
struct io_uring ring;
assert(io_uring_queue_init(8, &ring, 0) == 0);
char buf[16];
struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe, fd, buf, sizeof buf, 0);
io_uring_sqe_set_data64(sqe, 42);
assert(io_uring_submit(&ring) == 1);
struct io_uring_cqe *cqe;
assert(io_uring_wait_cqe(&ring, &cqe) == 0);
assert(cqe->user_data == 42 && cqe->res > 0);   // res < 0 is -errno
io_uring_cqe_seen(&ring, cqe);
```

## Do
- Create rings with `io_uring_queue_init(entries, &ring, flags)`; keep one ring per thread to avoid locking, sized for peak in-flight ops.
- Treat `cqe->res` as bytes or `-errno`; handle short reads and writes by resubmitting the remainder.
- Tie each request to a heap-allocated context via `user_data` and free it when its CQE arrives.
- Keep buffers alive and unmoved until the completion is reaped.
- Batch submissions: queue many SQEs, then one `io_uring_submit`; reap in bulk with `io_uring_peek_batch_cqe` and `io_uring_cq_advance`.
- Probe features with `io_uring_get_probe` and fall back to a simpler path when an opcode is unsupported.
- Use fixed files and registered buffers (`io_uring_register_files`, `io_uring_register_buffers`) for hot paths after measuring.
- Use `IOSQE_IO_LINK` for dependent operations, and check the chain's cancel results (`-ECANCELED`).
- Use multishot accept or recv with provided buffers for servers where the kernel supports them, and handle the `IORING_CQE_F_MORE` flag.

## Avoid
- Freeing or reusing a buffer or `struct iovec` before its CQE: kernel reads freed memory. Hold until completion.
- Ignoring `-EAGAIN`, `-EINTR` and short counts: lost data. Resubmit.
- Forgetting `io_uring_cqe_seen`: the CQ fills and completions stall. Mark each as seen.
- Overflowing the SQ or CQ without checking `io_uring_get_sqe` for NULL: dropped work. Submit and reap when full.
- Assuming operation order across independent SQEs: no ordering without links or drain. Link or sequence.
- Shipping with `io_uring` unconditional on containers that block it by seccomp: init fails with `-EPERM`. Fall back to epoll.
- Using SQPOLL without understanding its CPU cost: spinning kernel thread. Measure first.

## Review
- [ ] Every CQE `res` is checked for errors and short counts.
- [ ] Buffer and context lifetime extend to the matching completion.
- [ ] Unsupported opcodes or disabled io_uring have a fallback path.
- [ ] Ring sizes and per-thread ownership are documented.
- [ ] Tests cover an error CQE and a cancelled linked chain.
