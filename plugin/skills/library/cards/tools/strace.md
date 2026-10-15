---
name: strace
title: strace
area: tools
tags: [linux, syscalls, debugging, tracing, performance]
detect: []
related: [lsof, perf, gdb-lldb, tcpdump]
---
strace: traces the system calls a process makes, to see which files, sockets and errors sit behind a hang, a crash or a "file not found".

## Verify
- `strace -f -o /tmp/trace.txt cmd args`: trace a command and its children to a file.
- `strace -f -e trace=file -o /tmp/f.txt cmd`: only file-related calls (open, stat, exec).
- `strace -f -e trace=network cmd`: only socket calls (connect, sendto, recvfrom).
- `strace -p PID -f`: attach to a running process (needs permission to ptrace).
- `strace -c -f cmd`: a summary table of calls, errors and time per syscall.

## Test first
Reproduce the failure under strace, then search the output for the failing call.
```
strace -f -tt -T -o /tmp/t.txt ./app --config /etc/app.conf
grep -E 'ENOENT|EACCES|ECONNREFUSED' /tmp/t.txt | tail
# expect e.g. openat(AT_FDCWD, "/etc/app.conf", O_RDONLY) = -1 ENOENT
```
The last failing call before exit usually names the cause.

## Do
- Use `-f` for anything that forks or spawns threads, or you trace only the parent.
- Add `-tt` for timestamps and `-T` for time spent in each syscall, to find slow calls.
- Write to a file with `-o` and grep it: terminal output interleaves with the program's.
- Raise the string limit with `-s 256` when you need to read paths or payloads.
- Filter by syscall with `-e trace=openat,read` to cut noise, or by result with `-Z` (failures only) when supported.
- Read errors by name: ENOENT (missing path), EACCES (permission), EAGAIN (non-blocking retry), ETIMEDOUT.
- Use `-y` to print paths next to file descriptors.

## Avoid
- Running in production on a hot process: ptrace slows it a lot. Use a short window, a narrow filter, or perf.
- Forgetting `-f` and concluding the program makes no calls: children do the work. Add `-f`.
- Reading the first ENOENT as the cause: loaders probe many paths. Look at the last failure before the exit or the error message.
- Attaching to a process in a container without the capability: `Operation not permitted`. Use the right user, or the container's tracing capability.
- Trusting traces of programs that detect tracing: some exit when ptraced.
- Pasting traces with tokens or secrets: strings include arguments and payloads. Redact before sharing.

## Review
- [ ] The traced failing syscall and errno are quoted as evidence.
- [ ] Children were traced where relevant (`-f`).
- [ ] The root cause was fixed and the trace rerun to show the failure gone.
- [ ] No secrets from the trace were shared.
