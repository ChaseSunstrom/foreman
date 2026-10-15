---
name: lsof
title: lsof
area: tools
tags: [linux, files, ports, processes, debugging]
detect: []
related: [strace, tcpdump, kubectl-debugging]
---
lsof: lists open files, sockets and ports per process, to find what holds a port, a deleted file or a leaked descriptor.

## Verify
- `lsof -i :8080`: which process listens on or uses port 8080.
- `lsof -nP -iTCP -sTCP:LISTEN`: all listening TCP sockets, with numeric hosts and ports (no DNS delay).
- `lsof -p PID`: everything one process has open.
- `lsof +L1`: open files with link count zero, meaning deleted but still held (disk space not freed).
- `lsof -c nginx`: open files for processes whose command starts with nginx.

## Test first
Reproduce "address already in use" and name the holder.
```
python3 -m http.server 8080 &
lsof -nP -i :8080 -sTCP:LISTEN      # shows COMMAND python3 and the PID
kill %1
lsof -nP -i :8080 -sTCP:LISTEN      # now prints nothing and exits 1
```

## Do
- Use `-n -P` to skip DNS and port-name lookups, which are slow and mislead.
- Combine selections with `-a` (AND): `lsof -a -p PID -i` for one process's sockets only. Without `-a` the options are OR.
- Run as root (or the owner) to see other users' processes; otherwise rows are missing.
- Use `-t` for PIDs only: `kill $(lsof -t -i :8080)` after checking the process is the right one.
- Count descriptors with `lsof -p PID | wc -l` and compare with `ulimit -n` for a leak.
- For a deleted-but-open file, restore or truncate through `/proc/PID/fd/N` rather than hunting the path.
- Use `ss -ltnp` as a lighter alternative for listeners.

## Avoid
- `kill -9 $(lsof -t -i :PORT)` without looking: you may kill a proxy, a database or your own shell. Check the name first.
- Running it without `-n -P` on a busy host: it hangs on reverse DNS. Add the flags.
- Reading no output as "free" when you were not root: other users' sockets are hidden. Use sudo.
- Mixing `-i` and `-p` without `-a` and getting everything: the filters OR together. Add `-a`.
- Looking for a deleted log by its path: it has none. Use `lsof +L1` and the `/proc/PID/fd` entry.
- Using lsof inside a container and expecting host processes: it sees only that PID namespace.

## Review
- [ ] The holder process is identified by name and PID before any kill.
- [ ] Commands used numeric output and the needed privilege.
- [ ] The port or file is confirmed free or released after the fix.
- [ ] A leak case compares the descriptor count with the limit and over time.
